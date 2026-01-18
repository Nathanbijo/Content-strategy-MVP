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
    """
    
    print("=== generate_posts called ===")
    
    system_prompt = """You are an expert social media strategist.
Create engaging, platform-specific social media posts from the given brand profile.

Generate EXACTLY 5 posts total:
- 2 for Instagram (visual, emotional, emojis OK, shorter)
- 2 for LinkedIn (professional, value-focused, slightly longer)
- 1 for X/Twitter (punchy, hook-driven, concise)

Each post must have:
- platform: "Instagram" or "LinkedIn" or "X"
- caption: engaging text (use brand details, products, audience)
- hashtags: array of 3-6 relevant, non-spammy hashtags
- cta: clear call-to-action (vary these: "Learn more", "Shop now", "Join us", "Get started", "Follow us")
- tone: phrase describing the post tone

Rules:
- Use specific details from brand_profile (products, services, audience)
- Make each post unique with different angles (awareness, feature, story, value, offer)
- Keep hashtags relevant and professional
- Output ONLY valid JSON array, no extra text"""

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

Tone preset: {tone_preset}

Create 5 platform-specific social media posts as a JSON array."""

    try:
        print("Calling Groq API for posts...")
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
            post = GeneratedPost(
                platform=post_data.get("platform", "Instagram"),
                caption=post_data.get("caption", ""),
                hashtags=post_data.get("hashtags", [])[:6],
                cta=post_data.get("cta", "Learn more"),
                tone=post_data.get("tone", tone_preset),
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
                tone=tone_preset,
                engagement_score_label="Medium"
            )
        ]
