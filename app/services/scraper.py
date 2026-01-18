import requests
from bs4 import BeautifulSoup
from typing import Optional
import time
import os
from openai import OpenAI

# Groq client for fallback generation
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_fallback_from_url(url: str) -> str:
    """Use LLM to intelligently guess website content from URL when scraping fails"""
    
    try:
        domain = url.split('/')[2].replace('www.', '')  # Extract clean domain
    except:
        domain = url
    
    prompt = f"""Based on the domain name '{domain}', generate a brief 2-3 sentence description of what this company/website likely does, their main products/services, and target audience.

Be specific and realistic. Output plain text only, no formatting."""
    
    try:
        print(f"🤖 Generating AI fallback for {domain}...")
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        generated = response.choices[0].message.content.strip()
        print(f"✓ Generated fallback: {generated[:100]}...")
        return generated
    except Exception as e:
        print(f"Fallback generation failed: {e}")
        return f"A business website at {domain} offering products and services to customers."


def fetch_website_text(url: str, fallback_text: Optional[str] = None) -> str:
    """
    Fetch and extract text content from a website URL.
    Falls back to fallback_text, then AI-generated fallback if scraping fails.
    """
    
    print(f"\n=== Scraping {url} ===")
    
    # Set browser-like headers to avoid 403/bot detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    max_retries = 2
    timeout = 8
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}")
            
            response = requests.get(
                url, 
                headers=headers, 
                timeout=timeout,
                allow_redirects=True
            )
            
            # Check status
            if response.status_code != 200:
                print(f"Status code: {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    raise Exception(f"HTTP {response.status_code}")
            
            # Check content type
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' not in content_type:
                print(f"Non-HTML content type: {content_type}")
                raise Exception(f"Content-Type is {content_type}, not HTML")
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text from key elements
            text_parts = []
            
            # Title
            title = soup.find('title')
            if title:
                text_parts.append(title.get_text().strip())
            
            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                text_parts.append(meta_desc.get('content').strip())
            
            # Headings
            for tag in ['h1', 'h2', 'h3']:
                for heading in soup.find_all(tag):
                    text = heading.get_text().strip()
                    if text and len(text) > 3:
                        text_parts.append(text)
            
            # Paragraphs
            for p in soup.find_all('p'):
                text = p.get_text().strip()
                if text and len(text) > 20:
                    text_parts.append(text)
            
            # Combine and clean
            full_text = ' '.join(text_parts)
            full_text = ' '.join(full_text.split())
            
            # Limit length
            if len(full_text) > 4000:
                full_text = full_text[:4000] + "..."
            
            if len(full_text) < 50:
                print(f"Extracted text too short ({len(full_text)} chars)")
                raise Exception("Insufficient text extracted")
            
            print(f"✓ Successfully scraped {len(full_text)} characters")
            print(f"Preview: {full_text[:150]}...")
            return full_text
            
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(1)
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    # All scraping attempts failed - use fallbacks
    print("⚠️  Scraping failed, using fallback strategy")
    
    if fallback_text:
        print(f"✓ Using user-provided fallback ({len(fallback_text)} chars)")
        return fallback_text
    else:
        # Generate intelligent fallback using AI
        print("🤖 No fallback provided, generating AI-based content...")
        ai_fallback = generate_fallback_from_url(url)
        return ai_fallback
