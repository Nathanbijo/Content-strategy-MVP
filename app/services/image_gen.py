import urllib.parse
import re
from typing import Optional


def generate_post_image(brand_name: str, post_caption: str, platform: str, tone: str, hashtags: list = None) -> Optional[str]:
    """
    Generate BACKGROUND-ONLY marketing image (no text).
    Text will be overlaid cleanly in the frontend.
    """
    
    platform_specs = {
        "Instagram": {"size": "1080x1080", "desc": "square format"},
        "LinkedIn": {"size": "1200x627", "desc": "wide horizontal"},
        "X": {"size": "1200x675", "desc": "wide card"}
    }
    
    tone_styles = {
        "startup": "futuristic tech gradient with neon accents and geometric shapes",
        "cafe": "warm cozy coffee shop with natural wood textures and soft lighting",
        "ngo": "uplifting nature scene with warm hopeful colors",
        "enterprise": "professional clean corporate blue gradient minimal"
    }
    
    style = "modern professional gradient background"
    for key in tone_styles:
        if key in tone.lower():
            style = tone_styles[key]
            break
    
    specs = platform_specs.get(platform, platform_specs["Instagram"])
    width, height = specs["size"].split("x")
    
    # SIMPLE PROMPT: Background + Product/Subject ONLY (no text)
    prompt = (
        f"{brand_name} marketing background. "
        f"{style}. "
        f"Premium product photography. "
        f"Clean spacious layout. "
        f"No text, no words, no letters. "
        f"Photorealistic 8K quality."
    )
    
    encoded_prompt = urllib.parse.quote(prompt, safe="")
    
    image_url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&model=flux&nologo=true&enhance=true"
        f"&seed={abs(hash(brand_name + platform)) % 9999}"
    )
    
    print(f"✅ {platform} background generated")
    
    return image_url


def generate_multiple_images(brand_name: str, posts: list) -> dict:
    image_urls = {}
    
    for idx, post in enumerate(posts):
        try:
            if isinstance(post, dict):
                caption = post.get("caption", "")
                platform = post.get("platform", "Instagram")
                tone = post.get("tone", "Professional")
                hashtags = post.get("hashtags", [])
            else:
                caption = post.caption
                platform = post.platform
                tone = post.tone
                hashtags = post.hashtags
            
            image_url = generate_post_image(
                brand_name=brand_name,
                post_caption=caption,
                platform=platform,
                tone=tone,
                hashtags=hashtags
            )
            image_urls[idx] = image_url
            
        except Exception as e:
            print(f"❌ Error: {e}")
            image_urls[idx] = None
    
    return image_urls
