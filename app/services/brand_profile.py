import json
import os
from openai import OpenAI
from app.schemas import BrandProfile

# Groq client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_brand_profile(website_text: str, tone_preset: str) -> BrandProfile:
    """
    Generate a brand profile from website text using Groq.
    Tone preset can be 'auto' for LLM to detect, or specific preset to enforce.
    """
    
    print(f"=== generate_brand_profile called ===")
    print(f"website_text length: {len(website_text)}")
    print(f"website_text preview: {website_text[:200]}")
    print(f"tone_preset: {tone_preset}")
    
    # Normalize tone
    tone_key = (tone_preset or "auto").lower()
    
    # Define tone-specific interpretation guidelines
    tone_instructions = {
        "startup": {
            "style": "innovative, energetic, growth-focused, disruptive",
            "focus": "Focus on innovation, disruption, rapid growth, and future potential. Frame as a tech-forward, ambitious venture.",
            "keywords_hint": "Include words like: innovation, disrupt, scale, future, tech, growth"
        },
        "cafe": {
            "style": "warm, friendly, community-focused, welcoming",
            "focus": "Emphasize warmth, community connections, local experience, and cozy atmosphere. Frame as a neighborhood gathering place.",
            "keywords_hint": "Include words like: community, cozy, local, artisan, fresh, welcoming"
        },
        "ngo": {
            "style": "mission-driven, compassionate, impact-focused, purposeful",
            "focus": "Highlight social impact, mission, positive change, and humanitarian values. Frame as a force for good.",
            "keywords_hint": "Include words like: impact, mission, change, community, support, sustainable"
        },
        "enterprise": {
            "style": "professional, authoritative, established, corporate",
            "focus": "Stress reliability, scale, professional excellence, and industry leadership. Frame as a trusted, established leader.",
            "keywords_hint": "Include words like: enterprise, solution, reliable, professional, industry, leader"
        }
    }
    
    # Handle auto vs specific tone
    if tone_key == "auto":
        tone_label = "AUTO"
        style = "automatically detected brand voice based on the website content"
        focus = "Detect whether the brand feels like a startup, cafe, NGO, or enterprise based on their content, offerings, and language. Apply that style naturally."
        keywords_hint = "Choose keywords that best match the detected brand type (startup/cafe/NGO/enterprise)."
        system_instruction = f"""You are a marketing analyst expert.

Extract a concise BRAND PROFILE from the given website text.

TONE MODE: AUTO-DETECT
- Analyze the website content and determine if it's best described as: startup (tech/innovation), cafe (local/community), NGO (impact/mission), or enterprise (corporate/professional)
- Apply that brand voice naturally throughout the profile
- {focus}
- {keywords_hint}

Output ONLY valid JSON with exactly these keys:
- brand_name: string (never use "Unknown Brand" - infer from text)
- description: string (1-2 sentences with appropriate brand voice)
- products_services: array of 3-8 short strings
- target_audience: array of 3-8 short strings
- tone: short phrase describing the communication style you detected and applied
- keywords: array of 5-15 short strings (aligned with detected style)
- colors: array of 3-6 color names or hex codes if mentioned (e.g. "#123456" or "navy blue")

Rules:
- Do NOT return any extra keys, explanations, or comments
- Never use placeholders like "Unknown Brand" or "not available"
- If something is unclear, make a reasonable guess from the text
- If colors aren't mentioned, suggest 2-3 colors that fit the brand type"""
        
        user_instruction = f"""Website text:
---
{website_text[:3000]}
---

Analyze this text and extract a BRAND PROFILE. First detect the most appropriate brand style (startup/cafe/NGO/enterprise), then apply that voice throughout. Return ONLY valid JSON."""
        
    else:
        # Specific tone requested
        guidelines = tone_instructions.get(tone_key, tone_instructions["startup"])
        tone_label = tone_key.upper()
        style = guidelines["style"]
        focus = guidelines["focus"]
        keywords_hint = guidelines["keywords_hint"]
        
        system_instruction = f"""You are a marketing analyst expert specializing in {tone_label} brands.

Extract a concise BRAND PROFILE from the given website text.

CRITICAL: Interpret everything through a **{tone_label}** lens.
- Brand voice MUST be: {style}
- {focus}
- {keywords_hint}

Output ONLY valid JSON with exactly these keys:
- brand_name: string (never use "Unknown Brand" - infer from text)
- description: string (1-2 sentences with {tone_key} voice and perspective)
- products_services: array of 3-8 short strings (frame through {tone_key} lens)
- target_audience: array of 3-8 short strings (who they serve, {tone_key} perspective)
- tone: MUST describe as "{style}"
- keywords: array of 5-15 short strings ({tone_key}-relevant marketing keywords)
- colors: array of 3-6 color names or hex codes if mentioned (e.g. "#123456" or "navy blue")

Rules:
- Do NOT return any extra keys, explanations, or comments
- Never use placeholders like "Unknown Brand" or "not available"
- If something is unclear, make a reasonable guess from the text
- If colors aren't mentioned, suggest 2-3 colors that fit the {tone_key} brand type
- ALWAYS apply {tone_label} perspective to your interpretation"""
        
        user_instruction = f"""Website text:
---
{website_text[:3000]}
---

Tone preset: {tone_key}

Analyze this text and extract a BRAND PROFILE that strongly reflects a {tone_label} brand identity and voice. Return ONLY valid JSON."""

    try:
        print(f"Calling Groq API with tone mode: {tone_label}")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_instruction}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        print("Groq response received")
        profile_json = json.loads(response.choices[0].message.content)
        print(f"Parsed JSON: {profile_json}")
        
        return BrandProfile(
            brand_name=profile_json.get("brand_name", "Brand"),
            description=profile_json.get("description", "A leading brand in its industry."),
            products_services=profile_json.get("products_services", []),
            target_audience=profile_json.get("target_audience", []),
            tone=profile_json.get("tone", style),
            keywords=profile_json.get("keywords", []),
            colors=profile_json.get("colors", [])
        )
        
    except Exception as e:
        print(f"!!! ERROR in generate_brand_profile: {type(e).__name__}: {e}")
        return BrandProfile(
            brand_name="Brand",
            description="A business offering quality products and services.",
            products_services=[],
            target_audience=[],
            tone=tone_preset,
            keywords=[],
            colors=[]
        )
