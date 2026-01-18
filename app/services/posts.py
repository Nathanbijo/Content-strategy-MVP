import json
import os
from typing import List
from openai import OpenAI
from app.schemas import BrandProfile, GeneratedPost
from app.services.analytics import score_post


# Groq client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_posts(brand_profile: BrandProfile, tone_preset: str) -> List[GeneratedPost]:
    """
    Generate platform-specific social media posts using Groq.
    Uses brand_profile.tone if tone_preset is 'auto'.
    """
    
    print("=== generate_posts called ===")
    print(f"tone_preset: {tone_preset}")
    print(f"brand_profile.tone: {brand_profile.tone}")
    
    # Normalize tone - use detected tone from brand_profile if auto
    tone_key = (tone_preset or "auto").lower()
    
    if tone_key == "auto":
        # Use the tone that was detected in brand_profile
        effective_tone = brand_profile.tone
        tone_label = f"AUTO (detected as: {effective_tone})"
        print(f"Using auto-detected tone: {effective_tone}")
    else:
        effective_tone = tone_preset
        tone_label = tone_preset.upper()
    
    # Tone-specific post guidelines
    tone_guidelines = {
        "startup": {
            "style": "Bold, energetic, future-focused. Use emojis sparingly. Talk about innovation and growth.",
            "themes": ["disruption", "innovation", "scaling", "future"],
            "ctas": ["Join the revolution", "Get started", "Try it free", "Build with us"],
            "instagram_hint": "High energy, forward-looking, emoji: 🚀💡⚡",
            "linkedin_hint": "Professional but ambitious, focus on innovation and growth",
            "x_hint": "Punchy tech/innovation hooks"
        },
        "cafe": {
            "style": "Warm, friendly, conversational. Use 2-3 relevant emojis. Focus on community and experience.",
            "themes": ["community", "experience", "cozy", "local"],
            "ctas": ["Visit us today", "Stop by", "Join us", "Taste the difference"],
            "instagram_hint": "Inviting, warm, emoji: ☕🥐❤️",
            "linkedin_hint": "Community-focused, local business story",
            "x_hint": "Quick invitation or daily special"
        },
        "ngo": {
            "style": "Compassionate, mission-driven, inspiring. Minimal emojis. Focus on impact and change.",
            "themes": ["impact", "mission", "change", "together"],
            "ctas": ["Join our mission", "Make a difference", "Get involved", "Support us"],
            "instagram_hint": "Inspiring, impact-focused, emoji: 🌍💚🤝",
            "linkedin_hint": "Professional impact story, social good focus",
            "x_hint": "Urgent call to action for cause"
        },
        "enterprise": {
            "style": "Professional, authoritative, value-focused. No emojis. Emphasize trust and results.",
            "themes": ["excellence", "reliability", "results", "leadership"],
            "ctas": ["Learn more", "Contact sales", "Schedule demo", "Partner with us"],
            "instagram_hint": "Professional, no emojis, polished brand image",
            "linkedin_hint": "Thought leadership, industry authority",
            "x_hint": "Quick stat or insight, no emojis"
        }
    }
    
    # Detect which guidelines to use based on effective tone
    detected_type = "startup"  # default
    for key in ["startup", "cafe", "ngo", "enterprise"]:
        if key in effective_tone.lower():
            detected_type = key
            break
    
    guidelines = tone_guidelines.get(detected_type, tone_guidelines["startup"])
    
    system_prompt = f"""You are an expert social media strategist.

Create engaging, platform-specific social media posts from the given brand profile.

TONE REQUIREMENT: {guidelines['style']}
Key themes: {', '.join(guidelines['themes'])}
Preferred CTAs: {', '.join(guidelines['ctas'])}

Generate EXACTLY 5 posts:
- 2 for Instagram ({guidelines['instagram_hint']})
- 2 for LinkedIn ({guidelines['linkedin_hint']})
- 1 for X ({guidelines['x_hint']})

CRITICAL PLATFORM NAMES - Use these EXACT values only:
- "Instagram" (NOT "instagram" or "IG")
- "LinkedIn" (NOT "linkedin" or "Linkedin")  
- "X" (NOT "Twitter" or "X/Twitter" or "twitter")

Each post MUST:
- Match the brand voice: {effective_tone}
- Use specific brand details (products, services, audience)
- Have 3-6 relevant, non-spammy hashtags
- Include appropriate call-to-action
- Vary in angle: awareness, feature, value, story, or offer

Platform rules:
- Instagram: Shorter (1-2 sentences), visual language, emojis based on tone
- LinkedIn: Professional (2-3 sentences), value-driven, industry context
- X: Punchy (1 sentence), hook-driven, under 200 chars

Required JSON format:
{{
  "posts": [
    {{
      "platform": "Instagram",
      "caption": "Your engaging caption here",
      "hashtags": ["#tag1", "#tag2", "#tag3"],
      "cta": "Shop now",
      "tone": "{effective_tone}"
    }},
    {{
      "platform": "LinkedIn",
      "caption": "Professional content here",
      "hashtags": ["#business", "#innovation"],
      "cta": "Learn more",
      "tone": "{effective_tone}"
    }},
    {{
      "platform": "X",
      "caption": "Short punchy tweet",
      "hashtags": ["#hashtag"],
      "cta": "Join us",
      "tone": "{effective_tone}"
    }}
  ]
}}

Output ONLY valid JSON object with a "posts" array. No additional text."""

    brand_json = {
        "brand_name": brand_profile.brand_name,
        "description": brand_profile.description,
        "products_services": brand_profile.products_services,
        "target_audience": brand_profile.target_audience,
        "tone": brand_profile.tone,
        "keywords": brand_profile.keywords
    }

    user_prompt = f"""Brand Profile:
{json.dumps(brand_json, indent=2)}

Create 5 platform-specific social media posts that strongly match the brand tone: "{effective_tone}". 
Make each post unique with different marketing angles. 
Remember: Use "Instagram", "LinkedIn", and "X" as exact platform names.
Return as JSON object with "posts" array."""

    try:
        print(f"Calling Groq API for posts with tone: {tone_label}")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        print("Groq response received for posts")
        result = json.loads(response.choices[0].message.content)
        
        # Handle both array and object with "posts" key
        posts_data = result if isinstance(result, list) else result.get("posts", [])
        
        posts = []
        for post_data in posts_data:
            # Normalize platform name just in case
            platform = post_data.get("platform", "Instagram")
            if platform.lower() in ["twitter", "x/twitter"]:
                platform = "X"
            elif platform == "instagram":
                platform = "Instagram"
            elif platform == "linkedin":
                platform = "LinkedIn"
            
            post = GeneratedPost(
                platform=platform,
                caption=post_data.get("caption", ""),
                hashtags=post_data.get("hashtags", [])[:6],
                cta=post_data.get("cta", "Learn more"),
                tone=post_data.get("tone", effective_tone),
                engagement_score_label=score_post(
                    post_data.get("caption", ""),
                    post_data.get("hashtags", [])
                )
            )
            posts.append(post)
        
        print(f"Generated {len(posts)} posts")
        return posts
        
    except Exception as e:
        print(f"!!! ERROR generating posts: {type(e).__name__}: {e}")
        # Fallback posts
        return [
            GeneratedPost(
                platform="Instagram",
                caption=f"Discover {brand_profile.brand_name}! 🌟",
                hashtags=["#brand", "#marketing"],
                cta="Learn more",
                tone=effective_tone,
                engagement_score_label="Medium"
            )
        ]
