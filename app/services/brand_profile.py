import json
import os
from openai import OpenAI
from app.schemas import BrandProfile

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_brand_profile(website_text: str, tone_preset: str) -> BrandProfile:
    """
    Generate a brand profile from website text using OpenAI.
    """
    
    system_prompt = """You are a marketing analyst expert.
Extract a concise BRAND PROFILE from the given website text.
Always infer as much as possible from context.

Output ONLY valid JSON with exactly these keys:
- brand_name: string (never use "Unknown Brand" - infer from text)
- description: string (1-2 sentences describing what the brand does)
- products_services: array of 3-8 short strings (specific offerings)
- target_audience: array of 3-8 short strings (who they serve)
- tone: short phrase describing communication style (e.g. "friendly and innovative", "professional and authoritative")
- keywords: array of 5-15 short strings (relevant marketing keywords)
- colors: array of 3-6 color names or hex codes if mentioned (e.g. "#123456" or "navy blue")

Rules:
- Do NOT return any extra keys, explanations, or comments
- Never use placeholders like "Unknown Brand" or "not available"
- If something is unclear, make a reasonable guess from the text
- If colors aren't mentioned, suggest 2-3 colors that fit the brand type"""

    user_prompt = f"""Website text:
---
{website_text[:3000]}
---

Tone preset: {tone_preset}

Using ONLY the information above, extract and return the BRAND PROFILE as valid JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        profile_json = json.loads(response.choices[0].message.content)
        
        return BrandProfile(
            brand_name=profile_json.get("brand_name", "Brand"),
            description=profile_json.get("description", "A leading brand in its industry."),
            products_services=profile_json.get("products_services", []),
            target_audience=profile_json.get("target_audience", []),
            tone=profile_json.get("tone", tone_preset),
            keywords=profile_json.get("keywords", []),
            colors=profile_json.get("colors", [])
        )
        
    except Exception as e:
        print(f"Error generating brand profile: {e}")
        # Minimal fallback only if API call completely fails
        return BrandProfile(
            brand_name="Brand",
            description="A business offering quality products and services.",
            products_services=[],
            target_audience=[],
            tone=tone_preset,
            keywords=[],
            colors=[]
        )
