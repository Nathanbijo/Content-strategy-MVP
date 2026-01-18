import json
from typing import List
from app.schemas import BrandProfile, GeneratedPost
from app.services.analytics import score_post
from app.services.llm_client import get_client


def generate_posts(profile: BrandProfile, tone_preset: str) -> List[GeneratedPost]:
    """
    Uses LLM to generate 5 social posts for Instagram, LinkedIn, and X.
    """
    client = get_client()

    system_prompt = (
        "You are a social media manager. "
        "Using the given brand profile, create engaging social media posts. "
        "Return ONLY valid JSON: a list of objects with keys "
        "platform, caption, hashtags, cta, tone."
    )

    user_prompt = f"""
Brand profile JSON:
{profile.model_dump()}

Requirements:
- Generate 5 posts total.
- Use platforms among: "Instagram", "LinkedIn", "X".
- Each post JSON object must have:
  - "platform": one of "Instagram", "LinkedIn", "X"
  - "caption": string
  - "hashtags": array of 3-7 strings starting with '#'
  - "cta": short call-to-action
  - "tone": short phrase describing tone of voice
Return JSON like:
[
  {{
    "platform": "Instagram",
    "caption": "...",
    "hashtags": ["#...", "#..."],
    "cta": "...",
    "tone": "..."
  }}
]
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    raw = resp.choices[0].message.content

    try:
        data = json.loads(raw)
    except Exception:
        data = []

    posts: List[GeneratedPost] = []

    for item in data:
        platform = item.get("platform", "Instagram")
        caption = item.get("caption", "")
        hashtags = item.get("hashtags", []) or []
        cta = item.get("cta", "Learn more")
        tone = item.get("tone", profile.tone or tone_preset)

        label = score_post(caption, hashtags)

        try:
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
        except Exception:
            continue

    if not posts:
        fallback_caption = f"Discover {profile.brand_name}: {profile.description}"
        hashtags = ["#brand", "#marketing"]
        label = score_post(fallback_caption, hashtags)
        posts.append(
            GeneratedPost(
                platform="Instagram",
                caption=fallback_caption,
                hashtags=hashtags,
                cta="Learn more",
                tone=profile.tone or tone_preset,
                engagement_score_label=label,
            )
        )

    return posts
