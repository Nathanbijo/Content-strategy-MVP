from fastapi import APIRouter, HTTPException
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.scraper import fetch_website_text
from app.services.brand_profile import generate_brand_profile
from app.services.posts import generate_posts

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    try:
        text = fetch_website_text(req.url, req.fallbackText)
        if not text.strip():
            raise ValueError("Empty website text")

        brand_profile = generate_brand_profile(text, req.tonePreset)
        posts = generate_posts(brand_profile, req.tonePreset)

        return AnalyzeResponse(brand_profile=brand_profile, posts=posts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
