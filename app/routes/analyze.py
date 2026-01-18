import logging
from fastapi import APIRouter, HTTPException
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.scraper import WebScraper
from app.services.brand_profile import generate_brand_profile
from app.services.posts import generate_posts

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze a website and generate brand profile with social media posts.

    Flow:
    1. Scrape the website URL to extract content
    2. Generate structured brand profile from content using LLM
    3. Generate 5 social media posts based on brand profile
    4. Return complete analysis with brand and posts

    Args:
        req: AnalyzeRequest with url, tonePreset, and optional fallbackText

    Returns:
        AnalyzeResponse with brand_profile and list of generated posts

    Raises:
        HTTPException: 400 for invalid input, 500 for processing errors
    """
    try:
        # Validate input
        if not req.url:
            raise HTTPException(
                status_code=400,
                detail="URL is required"
            )

        # Step 1: Scrape website content
        logger.info(f"Scraping website: {req.url}")
        try:
            website_text = WebScraper.scrape_website(req.url, req.fallbackText)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to scrape website: {str(e)}"
            )

        if not website_text or not website_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Website content is empty or could not be extracted"
            )

        # Step 2: Generate brand profile
        logger.info("Generating brand profile...")
        try:
            brand_profile = generate_brand_profile(website_text, req.tonePreset)
        except Exception as e:
            logger.error(f"Brand profile generation failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate brand profile"
            )

        # Step 3: Generate social media posts
        logger.info("Generating social media posts...")
        try:
            posts = generate_posts(brand_profile, req.tonePreset)
        except Exception as e:
            logger.error(f"Post generation failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate social media posts"
            )

        # Step 4: Return complete analysis
        response = AnalyzeResponse(brand_profile=brand_profile, posts=posts)
        logger.info(f"Analysis complete: {brand_profile.brand_name} with {len(posts)} posts")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during analysis"
        )
