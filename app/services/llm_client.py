import os
import json
import re
from typing import Any, Dict, Optional
from openai import OpenAI


class LLMClient:
    """Singleton LLM client for OpenAI API with JSON response handling."""
    
    _client: Optional[OpenAI] = None

    @classmethod
    def get_client(cls) -> OpenAI:
        """Get or create OpenAI client singleton."""
        if cls._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set")
            cls._client = OpenAI(api_key=api_key)
        return cls._client

    @classmethod
    def call_with_json_response(
        cls,
        system_prompt: str,
        user_prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        """
        Call OpenAI API and parse JSON response with fallback handling.
        
        Handles both plain JSON and markdown-wrapped JSON (```json...```).
        
        Args:
            system_prompt: System context for the LLM
            user_prompt: User query
            model: Model ID (default: gpt-4o-mini)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Max response tokens
            
        Returns:
            Parsed JSON response as dictionary
            
        Raises:
            ValueError: If JSON cannot be parsed after fallback attempts
        """
        client = cls.get_client()
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            raw_response = response.choices[0].message.content
            
            # Try direct JSON parsing first
            try:
                return json.loads(raw_response)
            except json.JSONDecodeError:
                # Fallback: Extract JSON from markdown code blocks
                json_match = re.search(
                    r"```(?:json)?\s*([\s\S]*?)```",
                    raw_response
                )
                if json_match:
                    json_str = json_match.group(1).strip()
                    return json.loads(json_str)
                
                # Last attempt: find JSON object/array in response
                for start_char, end_char in [("{", "}"), ("[", "]")]:
                    try:
                        start = raw_response.find(start_char)
                        if start == -1:
                            continue
                        # Try progressively shorter substrings from the end
                        for end_offset in range(len(raw_response) - start):
                            end = len(raw_response) - end_offset
                            candidate = raw_response[start:end]
                            if candidate.endswith(end_char):
                                return json.loads(candidate)
                    except json.JSONDecodeError:
                        continue
                
                raise ValueError(
                    f"Could not parse JSON from LLM response:\n{raw_response}"
                )
                
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {str(e)}")

    @classmethod
    def call_simple(
        cls,
        system_prompt: str,
        user_prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """
        Call OpenAI API and return raw text response.
        
        Args:
            system_prompt: System context for the LLM
            user_prompt: User query
            model: Model ID
            temperature: Sampling temperature
            max_tokens: Max response tokens
            
        Returns:
            Raw text response
        """
        client = cls.get_client()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


# Backward compatibility
def get_client() -> OpenAI:
    """Backward compatibility wrapper."""
    return LLMClient.get_client()
