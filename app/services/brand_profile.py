import logging
from app.schemas import BrandProfile
from app.services.llm_client import LLMClient

logger = logging.getLogger(__name__)


def generate_brand_profile(text: str, tone_preset: str) -> BrandProfile:
    """
    Extract structured brand profile from website text using LLM.

    Args:
        text: Website content text
        tone_preset: Desired tone/brand voice

    Returns:
        Structured BrandProfile with brand information

    Raises:
        ValueError: If profile extraction fails
    """
    system_prompt = (
        "You are a senior marketing strategist. "
        "Given raw website text, extract a concise brand profile. "
        "Return ONLY valid JSON with keys: "
        "brand_name, description, products_services, target_audience, tone, keywords, colors. "
        "Ensure all values are properly formatted and arrays are valid."
    )

    user_prompt = f"""
Website text:
{text[:3000]}

Tone preset: {tone_preset}

Return JSON exactly like:
{{
  "brand_name": "Company Name",
  "description": "Brief description of the brand",
  "products_services": ["Product/Service 1", "Product/Service 2"],
  "target_audience": ["Audience 1", "Audience 2"],
  "tone": "professional",
  "keywords": ["keyword1", "keyword2"],
  "colors": ["#FF0000", "#00FF00"]
}}
"""

    try:
        result = LLMClient.call_with_json_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="gpt-4o-mini",
            temperature=0.4,
            max_tokens=1000,
        )

        # Validate and extract fields
        brand_profile = BrandProfile(
            brand_name=result.get("brand_name", "Unknown Brand"),
            description=result.get("description", "Brand description not available."),
            products_services=result.get("products_services", []) or [],
            target_audience=result.get("target_audience", []) or [],
            tone=result.get("tone", tone_preset),
            keywords=result.get("keywords", []) or [],
            colors=result.get("colors", []) or [],
        )

        return brand_profile

    except Exception as e:
        logger.error(f"Failed to generate brand profile: {str(e)}")
        # Return fallback profile
        return BrandProfile(
            brand_name="Unknown Brand",
            description="Brand description not available.",
            products_services=[],
            target_audience=[],
            tone=tone_preset,
            keywords=[],
            colors=[],
        )
