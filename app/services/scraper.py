from typing import Optional
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraper for extracting content from URLs."""

    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
    DEFAULT_TIMEOUT = 10
    MAX_CONTENT_LENGTH = 3000

    @classmethod
    def scrape_website(cls, url: str, fallback_text: Optional[str] = None) -> str:
        """
        Scrape website content from URL and extract text.

        Extracts: title, meta description, headings (h1-h3), paragraphs, 
        and navigation links.

        Args:
            url: Website URL to scrape
            fallback_text: Text to return if scraping fails

        Returns:
            Extracted text content (max 3000 chars)
        """
        if fallback_text:
            return fallback_text[:cls.MAX_CONTENT_LENGTH]

        try:
            # Fetch HTML with timeout and user agent
            response = requests.get(
                url,
                headers={"User-Agent": cls.DEFAULT_USER_AGENT},
                timeout=cls.DEFAULT_TIMEOUT,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            parts = []

            # Extract title
            if soup.title and soup.title.string:
                parts.append(f"Title: {soup.title.string.strip()}")

            # Extract meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                parts.append(f"Description: {meta_desc.get('content').strip()}")

            # Extract h1 headings
            for h1 in soup.find_all("h1", limit=3):
                text = h1.get_text(strip=True)
                if text:
                    parts.append(f"H1: {text}")

            # Extract h2 headings
            for h2 in soup.find_all("h2", limit=5):
                text = h2.get_text(strip=True)
                if text:
                    parts.append(f"H2: {text}")

            # Extract h3 headings
            for h3 in soup.find_all("h3", limit=5):
                text = h3.get_text(strip=True)
                if text:
                    parts.append(f"H3: {text}")

            # Extract main paragraphs
            for p in soup.find_all("p", limit=10):
                text = p.get_text(strip=True)
                if text and len(text) > 20:  # Only meaningful paragraphs
                    parts.append(text)

            # Extract navigation links and their text
            nav_sections = soup.find_all(["nav", "footer"], limit=2)
            for nav in nav_sections:
                for link in nav.find_all("a", limit=5):
                    link_text = link.get_text(strip=True)
                    if link_text:
                        parts.append(f"Link: {link_text}")

            # Combine all parts
            full_text = "\n\n".join(parts)
            
            # Truncate to max length
            if len(full_text) > cls.MAX_CONTENT_LENGTH:
                full_text = full_text[: cls.MAX_CONTENT_LENGTH] + "..."

            if not full_text.strip():
                raise ValueError("No content extracted from website")

            return full_text

        except requests.RequestException as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            if fallback_text:
                return fallback_text[:cls.MAX_CONTENT_LENGTH]
            raise ValueError(f"Could not fetch website at {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing website content: {str(e)}")
            if fallback_text:
                return fallback_text[:cls.MAX_CONTENT_LENGTH]
            raise ValueError(f"Error processing website content: {str(e)}")


def fetch_website_text(url: str, fallback_text: Optional[str] = None) -> str:
    """Backward compatibility wrapper."""
    return WebScraper.scrape_website(url, fallback_text)
