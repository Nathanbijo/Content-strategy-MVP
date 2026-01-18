import json
from app.schemas import BrandProfile
from app.services.llm_client import get_client


def generate_brand_profile(text: str, tone_preset: str) -> BrandProfile:
    """
    Uses LLM to extract a structured brand profile from website text.
    """
    client = get_client()

    system_prompt = (
        "You are a senior marketing strategist. "
        "Given raw website text, extract a concise brand profile. "
        "Return ONLY valid JSON with keys: "
        "brand_name, description, products_services, target_audience, tone, keywords."
    )

    user_prompt = f"""
Website text:
{text[:3000]}

Tone preset: {tone_preset}

Return JSON exactly like:
{{
  "brand_name": "...",
  "description": "...",
  "products_services": ["...", "..."],
  "target_audience": ["...", "..."],
  "tone": "...",
  "keywords": ["...", "..."]
}}
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )

    raw = resp.choices[0].message.content

    try:
        data = json.loads(raw)
    except Exception:
        return BrandProfile(
            brand_name="Unknown Brand",
            description="Brand description not available.",
            products_services=[],
            target_audience=[],
            tone=tone_preset,
            keywords=[],
            colors=[],
        )

    return BrandProfile(
        brand_name=data.get("brand_name", "Unknown Brand"),
        description=data.get("description", "Brand description not available."),
        products_services=data.get("products_services", []) or [],
        target_audience=data.get("target_audience", []) or [],
        tone=data.get("tone", tone_preset),
        keywords=data.get("keywords", []) or [],
        colors=[],  # can be filled later from scraper if needed
    )
