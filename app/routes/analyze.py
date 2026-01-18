from fastapi import APIRouter, HTTPException
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.scraper import fetch_website_text
from app.services.brand_profile import generate_brand_profile
from app.services.posts import generate_posts

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    try:
        # Get website text (from scraper or fallback)
        website_text = fetch_website_text(request.url, request.fallbackText)
        
        # If website_text is empty or None, use fallback or raise error
        if not website_text or len(website_text.strip()) < 10:
            if request.fallbackText:
                website_text = request.fallbackText
            else:
                raise HTTPException(status_code=400, detail="Could not extract content from URL and no fallback provided")
        
        # Generate brand profile
        brand_profile = generate_brand_profile(website_text, request.tonePreset)
        
        # Generate posts
        posts = generate_posts(brand_profile, request.tonePreset)
        
        return AnalyzeResponse(
            brand_profile=brand_profile,
            posts=posts
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {str(e)}")
