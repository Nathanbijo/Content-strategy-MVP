import urllib.parse
from typing import Optional

def generate_post_image(brand_name: str, post_caption: str, platform: str, tone: str, hashtags: list = None) -> Optional[str]:
    """
    Generate COMPLETE marketing graphic with text overlay using Pollinations AI.
    Returns ready-to-post image URL.
    """
    
    # Platform-specific dimensions and styles
    platform_specs = {
        "Instagram": {
            "size": "1080x1080",
            "style": "Instagram post format, square 1:1 ratio, mobile-optimized, vibrant modern design"
        },
        "LinkedIn": {
            "size": "1200x627",
            "style": "LinkedIn banner format, 16:9 ratio, professional business design, corporate aesthetic"
        },
        "X": {
            "size": "1200x675",
            "style": "Twitter/X card format, 16:9 ratio, bold attention-grabbing design, high contrast"
        }
    }
    
    # Tone-specific visual styles
    tone_styles = {
        "startup": "modern tech gradient background, futuristic elements, bold sans-serif typography",
        "cafe": "warm cozy coffee shop aesthetic, natural wood textures, handwritten script fonts",
        "ngo": "inspiring humanitarian imagery, nature backgrounds, compassionate warm colors",
        "enterprise": "professional corporate blue/gray palette, clean minimalist layout, serif fonts"
    }
    
    # Detect style from tone
    visual_style = "modern professional gradient background"
    for key in ["startup", "cafe", "ngo", "enterprise"]:
        if key in tone.lower():
            visual_style = tone_styles[key]
            break
    
    # Extract main message (first 60 chars of caption for text overlay)
    main_text = post_caption[:60].strip()
    if len(post_caption) > 60:
        main_text += "..."
    
    # Get platform specs
    specs = platform_specs.get(platform, platform_specs["Instagram"])
    
    # BUILD COMPLETE MARKETING GRAPHIC PROMPT
    prompt = f"""Create a professional {platform} marketing graphic for {brand_name}.

VISUAL DESIGN:
- {visual_style}
- {specs['style']}
- High-quality polished design
- Brand colors and aesthetic

TEXT OVERLAY (MUST INCLUDE):
Main headline text: "{main_text}"
- Large bold readable typography
- Proper text placement and hierarchy
- Professional text effects and shadows
- Text should be prominent and clear

LAYOUT:
- {platform} optimized dimensions
- Text in upper or center area
- Balanced composition
- Professional marketing quality
- Ready to post on social media

Style: Premium social media marketing graphic with text overlay"""
    
    # URL encode
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Extract dimensions
    width, height = specs["size"].split("x")
    
    # Generate image URL with Pollinations AI
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&enhance=true&seed={hash(post_caption) % 10000}"
    
    print(f"🎨 Generated {platform} marketing graphic with text overlay")
    print(f"   Main text: {main_text}")
    
    return image_url


def generate_multiple_images(brand_name: str, posts: list) -> dict:
    """
    Generate complete marketing graphics for all posts.
    Returns dict mapping post index to image URL.
    """
    image_urls = {}
    
    for idx, post in enumerate(posts):
        try:
            # Handle both dict and object formats
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
            print(f"❌ Error generating image for post {idx}: {e}")
            image_urls[idx] = None
    
    return image_urls
