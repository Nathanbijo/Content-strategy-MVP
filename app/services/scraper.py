from typing import Optional


def fetch_website_text(url: str, fallback_text: Optional[str] = None) -> str:
    """
    TODO: Replace this with real HTML fetch + parsing.
    For now, return fallback_text if provided, else demo text.
    """
    if fallback_text:
        return fallback_text

    demo_text = """
    Welcome to Demo Cafe, your friendly neighborhood coffee shop.
    We serve freshly brewed coffee, pastries and light snacks.
    Our cozy space is perfect for students and young professionals.
    """
    return demo_text.strip()
