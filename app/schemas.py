from typing import List, Literal, Optional
from pydantic import BaseModel


from typing import List, Literal, Optional
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    url: str
    tonePreset: str = "auto"   # default to auto-detect
    fallbackText: Optional[str] = None


class BrandProfile(BaseModel):
    brand_name: str
    description: str
    products_services: List[str]
    target_audience: List[str]
    tone: str
    keywords: List[str]
    colors: List[str]  # hex codes like "#RRGGBB"


class GeneratedPost(BaseModel):
    platform: Literal["Instagram", "LinkedIn", "X"]
    caption: str
    hashtags: List[str]
    cta: str
    tone: str
    engagement_score_label: str
    image_url: Optional[str] = None  # NEW FIELD FOR MARKETING IMAGES

class AnalyzeResponse(BaseModel):
    brand_profile: BrandProfile
    posts: List[GeneratedPost]
