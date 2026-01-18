# MarketFlow AI — React Frontend Implementation Guide

**Project**: Content Strategy MVP  
**Backend API**: FastAPI (CORS enabled, all origins allowed)  
**API Base URL**: `http://localhost:8000` (or your deployed endpoint)  

---

## 1. API OVERVIEW

### Health Check
- **Endpoint**: `GET /health`
- **Response**: `{ "status": "ok" }`
- **Purpose**: Verify backend is running

### Main Endpoint: Analyze Website
- **Endpoint**: `POST /analyze`
- **Description**: Submit a website URL and receive a complete content pack (brand profile, social posts, images)
- **Base URL for local development**: `http://localhost:8000`

---

## 2. REQUEST/RESPONSE SCHEMAS

### 2.1 AnalyzeRequest (Input)
```typescript
interface AnalyzeRequest {
  url: string;                    // Full website URL (e.g., "https://example.com")
  tonePreset: string;             // "auto" | "startup" | "cafe" | "ngo" | "enterprise" (default: "auto")
  fallbackText?: string;          // Optional fallback if scraping fails
}
```

**Example Request**:
```json
{
  "url": "https://example.com",
  "tonePreset": "startup",
  "fallbackText": null
}
```

### 2.2 AnalyzeResponse (Output)
```typescript
interface AnalyzeResponse {
  brand_profile: BrandProfile;
  posts: GeneratedPost[];
}

interface BrandProfile {
  brand_name: string;              // Extracted or inferred brand name
  description: string;             // 1-2 sentence brand summary
  products_services: string[];     // 3-8 product/service descriptions
  target_audience: string[];       // 3-8 audience segment descriptions
  tone: string;                    // Brand communication style (e.g., "innovative, energetic, growth-focused")
  keywords: string[];              // 5-15 marketing keywords
  colors: string[];                // 3-6 color names or hex codes (e.g., "#FF5733" or "navy blue")
}

interface GeneratedPost {
  platform: "Instagram" | "LinkedIn" | "X";
  caption: string;                 // Post content
  hashtags: string[];              // 3-6 hashtags (already include # symbol)
  cta: string;                     // Call-to-action ("Learn more", "Shop now", "Join us", etc.)
  tone: string;                    // Post tone descriptor
  engagement_score_label: string;  // "Low" | "Medium" | "High"
  image_url?: string;              // URL to generated marketing image (may be null if generation failed)
}
```

**Example Response**:
```json
{
  "brand_profile": {
    "brand_name": "TechFlow",
    "description": "A cutting-edge SaaS platform revolutionizing how teams collaborate on digital projects.",
    "products_services": ["Project Management", "Real-time Collaboration", "AI Analytics Dashboard"],
    "target_audience": ["Tech Startups", "Design Teams", "Remote-first Companies"],
    "tone": "innovative, energetic, growth-focused, disruptive",
    "keywords": ["innovation", "disrupt", "scale", "future", "tech", "growth", "collaboration", "AI"],
    "colors": ["#007AFF", "#F0F0F0", "navy blue"]
  },
  "posts": [
    {
      "platform": "Instagram",
      "caption": "🚀 Transform how your team works. Real-time collaboration, powered by AI. TechFlow makes project management effortless.",
      "hashtags": ["#ProductLaunch", "#TeamWork", "#TechInnovation", "#Collaboration"],
      "cta": "Learn more",
      "tone": "energetic, relatable",
      "engagement_score_label": "High",
      "image_url": "https://image.pollinations.ai/prompt/... [URL truncated]"
    },
    {
      "platform": "LinkedIn",
      "caption": "Introducing TechFlow: The Future of Team Collaboration. We believe the best teams deserve the best tools. Our new AI-powered collaboration platform helps teams ship faster, communicate clearer, and scale smarter.",
      "hashtags": ["#ProductAnnouncement", "#TeamProductivity", "#Enterprise", "#Innovation"],
      "cta": "Get started",
      "tone": "professional, forward-thinking",
      "engagement_score_label": "High",
      "image_url": "https://image.pollinations.ai/prompt/... [URL truncated]"
    }
  ]
}
```

---

## 3. TONE PRESETS & BEHAVIOR

### Auto-Detect Mode (tonePreset: "auto")
- Backend analyzes website content and **automatically detects** whether the brand is a startup, cafe, NGO, or enterprise
- Applies appropriate brand voice throughout the profile
- Best for unknown brands or exploratory analysis

### Preset Modes
Each preset enforces a specific brand voice across all outputs:

| Preset | Style | Use Case |
|--------|-------|----------|
| `startup` | Innovative, energetic, growth-focused, disruptive | Tech companies, SaaS, accelerators |
| `cafe` | Warm, friendly, community-focused, welcoming | Cafes, local businesses, lifestyle brands |
| `ngo` | Mission-driven, compassionate, impact-focused | Nonprofits, charities, social enterprises |
| `enterprise` | Professional, authoritative, established, corporate | Large companies, B2B, traditional industries |

---

## 4. GENERATED CONTENT STRUCTURE

### Brand Profile
- **Purpose**: Single source of truth for brand identity
- **Fields**: All 7 fields (name, description, products, audience, tone, keywords, colors)
- **Usage**: Display in brand overview section; use for context/reference

### Social Posts (5 total, platform-distributed)
- **Instagram Posts**: 2 posts (visual, emotional, emoji-friendly, shorter)
- **LinkedIn Posts**: 2 posts (professional, value-focused, slightly longer)
- **X/Twitter Posts**: 1 post (punchy, hook-driven, concise)

Each post includes:
- **Platform**: Ensures correct formatting/dimensions
- **Caption**: Ready-to-copy text
- **Hashtags**: Pre-selected, relevant tags (3-6 per post)
- **CTA**: Varied ("Learn more", "Shop now", "Join us", "Get started", "Follow us")
- **Tone**: Describes communication style (for context)
- **Engagement Score**: Heuristic label (Low/Medium/High) based on length and hashtag count
- **Image URL**: Generated marketing graphic specific to platform

### Images
- **Auto-generated** for each post using Pollinations AI (Flux model)
- **Platform-optimized dimensions**:
  - Instagram: 1080x1080 (square, mobile)
  - LinkedIn: 1200x627 (16:9 banner)
  - X/Twitter: 1200x675 (16:9 card)
- **Content**: Professional marketing graphic with post headline overlaid as text
- **Visual styling**: Adapts to detected/selected tone (e.g., startup = modern tech gradients, cafe = warm wood textures)
- **URL Format**: `https://image.pollinations.ai/prompt/[encoded_prompt]?width=...&height=...&model=flux&nologo=true&enhance=true`

---

## 5. FRONTEND COMPONENTS & USER FLOW

### Page Structure Recommendation

#### Page 1: Input Form
- **URL Input**: Text field for website URL
- **Tone Selector**: Dropdown or buttons for tone preset
  - Options: Auto, Startup, Cafe, NGO, Enterprise
- **Fallback Text (Optional)**: Textarea for manual content if scraping fails
- **Submit Button**: Triggers POST /analyze
- **Loading State**: Show spinner/loader during API call (typically 15-30 seconds)

#### Page 2: Results Display
- **Brand Profile Card/Panel**:
  - Brand name (large, prominent)
  - Description (italicized or highlighted)
  - Key badges: 
    - Products & Services (pill-style badges)
    - Target Audience (pill-style badges)
    - Keywords (smaller, secondary badges)
  - Tone label
  - Color palette display (hex swatches or color names)

- **Posts Grid**:
  - 5 cards, one per post
  - Card layout (platform-specific styling):
    ```
    [Instagram Icon] Instagram
    [Image Preview - Square]
    [Caption Text] (truncated with "read more")
    [Hashtags] (gray, smaller font)
    [CTA Button]
    Engagement: 🟢 High / 🟡 Medium / 🔴 Low
    [Copy to Clipboard] [Download Image] [Share]
    ```

  - Platform colors:
    - Instagram: Purple/Pink (#E4405F)
    - LinkedIn: Blue (#0A66C2)
    - X/Twitter: Black (#000000)

- **Action Buttons** (for each post):
  - Copy Caption
  - Copy Hashtags
  - Copy All (caption + hashtags + CTA)
  - Download Image
  - Preview Full Post
  - Open in Native App (optional, deep links)

- **Export Options** (for entire pack):
  - Export as JSON
  - Export as CSV (spreadsheet-friendly)
  - Generate scheduling template

---

## 6. HTTP CLIENT INTEGRATION

### Setup (React Example)

```typescript
// api/client.ts
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function analyzeWebsite(
  url: string,
  tonePreset: string = "auto",
  fallbackText?: string
): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url,
      tonePreset,
      fallbackText,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to analyze website");
  }

  return response.json();
}

export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error("Health check failed");
  return response.json();
}
```

### Usage in Component

```typescript
// pages/AnalysisPage.tsx
import { useState } from "react";
import { analyzeWebsite } from "../api/client";

export function AnalysisPage() {
  const [url, setUrl] = useState("");
  const [tonePreset, setTonePreset] = useState("auto");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<AnalyzeResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await analyzeWebsite(url, tonePreset);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error} />;
  if (response) return <ResultsDisplay data={response} />;

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="url"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://example.com"
        required
      />
      <select value={tonePreset} onChange={(e) => setTonePreset(e.target.value)}>
        <option value="auto">Auto-Detect</option>
        <option value="startup">Startup</option>
        <option value="cafe">Cafe</option>
        <option value="ngo">NGO</option>
        <option value="enterprise">Enterprise</option>
      </select>
      <button type="submit">Analyze Website</button>
    </form>
  );
}
```

---

## 7. IMAGE HANDLING

### Image URL Format
Images are generated dynamically from Pollinations AI. They follow this pattern:
```
https://image.pollinations.ai/prompt/[URL_ENCODED_PROMPT]?width=[W]&height=[H]&model=flux&nologo=true&enhance=true&seed=[SEED]
```

### Displaying Images
```typescript
<img
  src={post.image_url}
  alt={`${post.platform} marketing graphic`}
  style={{ width: "100%", maxWidth: "1080px", borderRadius: "8px" }}
  loading="lazy"
/>
```

### Image Caching Strategy
- Images are generated fresh for each request but have consistent seeds
- Consider caching image URLs in localStorage if needed
- Browser caching will handle subsequent loads

### Fallback for Failed Images
```typescript
<img
  src={post.image_url}
  alt={`${post.platform} post`}
  onError={(e) => {
    (e.target as HTMLImageElement).src = "/placeholder-image.png";
  }}
/>
```

---

## 8. ERROR HANDLING

### Common Error Scenarios

| Scenario | HTTP Status | Response Format | Handle |
|----------|------------|-----------------|--------|
| Invalid URL | 500 | `{"detail": "Invalid URL or unreachable"}` | Show error message, suggest retrying |
| Scraping blocked (403/Cloudflare) | 200 | Uses fallback_text or AI-generated summary | Works transparently; may have less info |
| LLM failure | 500 | `{"detail": "Error generating brand profile"}` | Show error; suggest manual input |
| Image generation failed | 200 | `image_url: null` | Show placeholder; allow download of caption only |
| Network timeout | Network Error | Exception | Retry mechanism or show timeout message |

### Error Response Example
```json
{
  "detail": "Error generating brand profile: API rate limit exceeded"
}
```

### Retry Logic Recommendation
```typescript
async function analyzeWithRetry(
  url: string,
  tonePreset: string,
  maxRetries: number = 3
) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await analyzeWebsite(url, tonePreset);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1))); // Exponential backoff
    }
  }
}
```

---

## 9. PERFORMANCE CONSIDERATIONS

### API Response Time
- **Typical duration**: 15-30 seconds
- **Breakdown**:
  - Website scraping: 2-5 seconds
  - Brand profile generation: 5-10 seconds
  - Post generation: 3-8 seconds
  - Image generation: 3-5 seconds (parallel per post)

### Frontend Optimizations
1. **Show progressive loading states**:
   - "Fetching website content..."
   - "Analyzing brand..."
   - "Generating posts..."
   - "Creating images..."

2. **Lazy load images**: Use `loading="lazy"` on post images

3. **Implement request cancellation**:
   ```typescript
   const abortController = new AbortController();
   fetch(url, { signal: abortController.signal });
   ```

4. **Cache results locally** (optional):
   - Store last analysis result in sessionStorage
   - Allow user to return to previous results

---

## 10. DATA EXPORT OPTIONS

### CSV Export
Flatten structure for spreadsheet:
```csv
Platform,Caption,Hashtags,CTA,Tone,Engagement_Score,Image_URL
Instagram,"Post text here","#tag1 #tag2 #tag3","Learn more","energetic","High","https://..."
LinkedIn,"Post text here","#tag1 #tag2 #tag3","Get started","professional","High","https://..."
```

### JSON Export
Full structured data with brand profile

### Scheduling Template
Pre-formatted for common scheduling tools (Buffer, Later, Hootsuite):
```json
{
  "brand_name": "...",
  "content_pack": [
    {
      "platform": "Instagram",
      "scheduled_date": "2024-01-25",
      "scheduled_time": "10:00 AM",
      "caption": "...",
      "media_url": "...",
      "tags": ["#tag1", "#tag2"]
    }
  ]
}
```

---

## 11. ENVIRONMENT VARIABLES

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
# or for production:
# REACT_APP_API_URL=https://api.example.com
```

### Backend (.env) — For Reference
```env
GROQ_API_KEY=your_groq_api_key
# Backend also uses Pollinations AI (free, no key required)
```

---

## 12. RECOMMENDED TECH STACK (React)

- **HTTP Client**: `fetch` (native) or `axios`
- **State Management**: `useState` hook (small) or `Zustand` / `Redux` (larger app)
- **UI Components**: Material-UI, Shadcn, Tailwind CSS, or custom
- **Form Validation**: `react-hook-form` + `zod`
- **Image Optimization**: `next/image` (if Next.js) or `<img>` with lazy loading
- **Clipboard**: `navigator.clipboard.writeText()` or `copy-to-clipboard` package
- **Copy Feedback**: Toast notifications (React Toastify, Sonner, etc.)

---

## 13. QUICK START CHECKLIST

- [ ] Set up React project
- [ ] Create API client module (see section 6)
- [ ] Build input form component
- [ ] Build results display component
- [ ] Add loading/error states
- [ ] Implement copy-to-clipboard for captions/hashtags
- [ ] Add image preview functionality
- [ ] Implement export (JSON/CSV)
- [ ] Style for mobile responsiveness
- [ ] Test with sample URLs
- [ ] Set environment variables
- [ ] Deploy frontend
- [ ] Update `REACT_APP_API_URL` for production API

---

## 14. SAMPLE API CALLS FOR TESTING

### Using curl:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.nike.com",
    "tonePreset": "startup",
    "fallbackText": null
  }'
```

### Using Node.js (fetch):
```javascript
fetch("http://localhost:8000/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "https://www.nike.com",
    tonePreset: "startup",
  }),
})
  .then((r) => r.json())
  .then((data) => console.log(data));
```

### Using Python (requests):
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "url": "https://www.nike.com",
        "tonePreset": "startup"
    }
)
print(response.json())
```

---

## 15. DEPLOYMENT NOTES

### CORS
- Backend is configured to allow **all origins** (`allow_origins=["*"]`)
- Suitable for MVP; restrict origins in production

### API Documentation
- Swagger UI available at: `http://localhost:8000/docs`
- ReDoc available at: `http://localhost:8000/redoc`

### Frontend Deployment
- Deploy React app to Vercel, Netlify, AWS Amplify, etc.
- Update `REACT_APP_API_URL` environment variable to production API endpoint
- Ensure CORS origin is whitelisted on backend

---

## 16. EXAMPLE COMPONENT STRUCTURE

```
src/
├── api/
│   ├── client.ts           # API functions
│   └── types.ts            # TypeScript interfaces
├── components/
│   ├── InputForm.tsx       # URL + tone input
│   ├── ResultsDisplay.tsx  # Brand + posts display
│   ├── PostCard.tsx        # Single post component
│   ├── BrandProfile.tsx    # Brand profile panel
│   └── LoadingSpinner.tsx  # Spinner component
├── pages/
│   ├── Home.tsx            # Main page
│   └── Analysis.tsx        # Results page
├── hooks/
│   └── useAnalyze.ts       # Custom hook for analysis logic
├── utils/
│   ├── clipboard.ts        # Copy utilities
│   ├── export.ts           # Export to JSON/CSV
│   └── formatting.ts       # Format/display helpers
└── App.tsx                 # Main app component
```

---

## 17. KNOWN LIMITATIONS & FUTURE ENHANCEMENTS

### Current Limitations
- Images generated on Pollinations AI are free but may have rate limits
- Scraping fails on heavily JavaScript-rendered or protected sites (graceful fallback)
- Post generation is synchronous; larger batches not currently supported

### Future Enhancements
- Batch analysis (multiple URLs)
- Custom brand profile editing before post generation
- Social media scheduling integration (Buffer, Later)
- A/B testing different tones for same URL
- Analytics dashboard (post performance tracking)
- User authentication & saved profiles
- Team collaboration features
- Advanced image customization

---

**Version**: 1.0  
**Last Updated**: January 18, 2025  
**Backend**: FastAPI + Groq LLM + Pollinations AI
