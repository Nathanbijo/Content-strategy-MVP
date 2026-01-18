import logging
from typing import List
from app.schemas import BrandProfile, GeneratedPost
from app.services.analytics import score_post
from app.services.llm_client import LLMClient

logger = logging.getLogger(__name__)


def generate_posts(profile: BrandProfile, tone_preset: str) -> List[GeneratedPost]:
    """
    Generate 5 platform-specific social media posts using LLM.

    Creates posts for Instagram, LinkedIn, and X with engagement scoring.

    Args:
        profile: Brand profile with brand information
        tone_preset: Desired tone for posts

    Returns:
        List of 5 GeneratedPost objects with platform, caption, hashtags, CTA, tone, and engagement score
    """
    system_prompt = (
        "You are a social media manager specializing in brand content creation. "
        "Using the given brand profile, create engaging social media posts. "
        "Return ONLY valid JSON: a list of objects with keys "
        "platform, caption, hashtags, cta, tone."
    )

    user_prompt = f"""
Brand profile:
- Name: {profile.brand_name}
- Description: {profile.description}
- Products/Services: {', '.join(profile.products_services) if profile.products_services else 'N/A'}
- Target Audience: {', '.join(profile.target_audience) if profile.target_audience else 'General'}
- Keywords: {', '.join(profile.keywords) if profile.keywords else 'N/A'}

Requirements:
- Generate 5 posts total
- Distribute across platforms: Instagram (2), LinkedIn (2), X/Twitter (1)
- Each post must have:
  - "platform": one of "Instagram", "LinkedIn", "X"
  - "caption": engaging text (Instagram: 100-200 chars, LinkedIn: 200-300 chars, X: max 280 chars)
  - "hashtags": array of 3-7 hashtags (start with #)
  - "cta": short call-to-action (e.g., "Learn more", "Shop now")
  - "tone": descriptive phrase (e.g., "professional", "casual", "inspiring")

Return JSON array like:
[
  {{
    "platform": "Instagram",
    "caption": "...",
    "hashtags": ["#brand", "#marketing"],
    "cta": "Follow for more",
    "tone": "casual"
  }}
]
"""

    try:
        data = LLMClient.call_with_json_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=2000,
        )

        # Ensure data is a list
        if not isinstance(data, list):
            data = []

    except Exception as e:
        logger.error(f"Failed to generate posts: {str(e)}")
        data = []

    posts: List[GeneratedPost] = []

    # Parse generated posts
    for item in data:
        try:
            platform = item.get("platform", "Instagram")
            caption = item.get("caption", "")
            hashtags = item.get("hashtags", []) or []
            cta = item.get("cta", "Learn more")
            tone = item.get("tone", profile.tone or tone_preset)

            # Score engagement
            label = score_post(caption, hashtags)

            # Validate and create post
            posts.append(
                GeneratedPost(
                    platform=platform,  # type: ignore[arg-type]
                    caption=caption,
                    hashtags=hashtags,
                    cta=cta,
                    tone=tone,
                    engagement_score_label=label,
                )
            )
        except Exception as e:
            logger.warning(f"Failed to create post from LLM response: {str(e)}")
            continue

    # If no posts were created, generate fallbacks
    if not posts:
        logger.warning("No posts generated from LLM, using fallbacks")
        posts = _generate_fallback_posts(profile, tone_preset)

    return posts


def _generate_fallback_posts(profile: BrandProfile, tone_preset: str) -> List[GeneratedPost]:
    """Generate fallback posts when LLM response fails."""
    brand_mention = f"{profile.brand_name}: {profile.description}"
    fallback_posts = [
        GeneratedPost(
            platform="Instagram",
            caption=f"Discover {brand_mention}. Quality products for everyone. 🌟",
            hashtags=["#brand", "#marketing", "#quality"],
            cta="Learn more",
            tone=profile.tone or tone_preset,
            engagement_score_label="Medium",
        ),
        GeneratedPost(
            platform="Instagram",
            caption=f"Elevate your experience with {profile.brand_name}. Check us out!",
            hashtags=["#trending", "#innovation", "#brand"],
            cta="Shop now",
            tone=profile.tone or tone_preset,
            engagement_score_label="Medium",
        ),
        GeneratedPost(
            platform="LinkedIn",
            caption=f"Introducing {profile.brand_name}: {profile.description} We're committed to excellence and innovation in our industry.",
            hashtags=["#business", "#professional", "#company"],
            cta="Learn more",
            tone="professional",
            engagement_score_label="Medium",
        ),
        GeneratedPost(
            platform="LinkedIn",
            caption=f"Join us as we revolutionize the industry with {profile.brand_name}. Together, we create value and drive growth.",
            hashtags=["#industry", "#growth", "#leadership"],
            cta="Connect with us",
            tone="professional",
            engagement_score_label="Medium",
        ),
        GeneratedPost(
            platform="X",
            caption=f"{profile.brand_name}: Your go-to for amazing products & services 🚀",
            hashtags=["#brand", "#social", "#trending"],
            cta="Follow us",
            tone=profile.tone or tone_preset,
            engagement_score_label="Medium",
        ),
    ]
    return fallback_posts
