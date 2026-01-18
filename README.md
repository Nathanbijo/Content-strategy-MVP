# MarketFlow AI — Social Content & Creative Generator

MarketFlow AI turns any website URL into a brand profile, platform-specific post copy, and ready-to-post marketing creatives (images with text overlays). It reduces the time to create a full content pack from hours to under a minute, enabling SMBs and agencies to ship consistent, on-brand social campaigns faster.

## What it does

Input: a website URL  
Output: a complete “content pack”
- Brand profile (voice/tone, offerings, audience, keywords, suggested colors)
- 5 platform-specific posts (2 Instagram, 2 LinkedIn, 1 X)
- Engagement score labels for each post
- Marketing creatives (platform-sized images with the post headline overlaid)
- Exports (CSV/JSON) for handoff to teams or scheduling tools


## How it works (architecture)

User (Web UI / API)
|
| POST /analyze (url, tone_preset)
v
FastAPI Backend
|
|-- Scraper Service (Requests + BeautifulSoup)
| - Extracts readable website text
| - If blocked (403/Cloudflare), uses AI fallback summary
|
|-- Brand Profile Generator (Groq Llama 3.3 70B)
| - Produces structured brand_profile JSON
|
|-- Post Generator (Groq Llama 3.3 70B)
| - Generates 5 posts with hashtags + CTA
| - Enforces strict platform enum: Instagram / LinkedIn / X
|
|-- Engagement Scoring (heuristics)
| - Returns High / Medium / Low label
|
|-- Image Generator (Pollinations AI / Flux)
| - Creates platform-sized marketing creative per post
| - Adds headline text overlay (Option B)
|
v
JSON Response (brand_profile + posts + image_url)

text

## Tech stack (and why)

### Backend
- **FastAPI**: high-performance API layer with automatic Swagger docs (`/docs`) and strong request/response validation via Pydantic. [web:46]
- **Pydantic**: schema enforcement prevents invalid outputs (ex: platform must be `Instagram | LinkedIn | X`) and makes the API contract reliable.
- **Requests + BeautifulSoup**: fast website text extraction for brand analysis; lightweight compared to browser automation.
- **Groq (OpenAI-compatible)**: very fast LLM inference for structured brand profiling and post generation.
- **Pollinations AI (Flux)**: free, no-key image generation via URL endpoints—ideal for hackathon velocity and zero-cost demos. [web:40][web:43]

### Frontend
- **React 18**: component-based UI for quick iteration and clean separation of concerns. [web:17]
- **Tailwind CSS**: rapid UI styling without maintaining large CSS files.
- **Axios**: consistent API calls with better error handling than native fetch for many teams.

## Core API

### POST `/analyze`
Generates brand profile + posts + images.

Request:
```json
{
  "url": "https://www.tesla.com",
  "tone_preset": "auto"
}
Response (shape):

json
{
  "brand_profile": { "...": "..." },
  "posts": [
    {
      "platform": "Instagram",
      "caption": "...",
      "hashtags": ["#..."],
      "cta": "...",
      "tone": "...",
      "engagement_score_label": "High",
      "image_url": "https://image.pollinations.ai/prompt/..."
    }
  ]
}
Local setup (quick)
Backend
bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env
# GROQ_API_KEY=your_key_here

uvicorn app.main:app --reload
Open docs: http://localhost:8000/docs

Frontend
bash
cd frontend
npm install
npm start
UI: http://localhost:3000
