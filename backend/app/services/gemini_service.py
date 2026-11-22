import json
from typing import Any

import httpx

from app.config import settings
from app.schemas.sentiment import SentimentResult

GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


class GeminiServiceError(Exception):
    """Raised when Gemini cannot return a valid sentiment result."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


class GeminiService:
    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def analyze_sentiment(self, text: str) -> SentimentResult:
        prompt = self._build_prompt(text)
        endpoint = (
            f"{GEMINI_API_BASE_URL}/models/"
            f"{settings.GEMINI_MODEL}:generateContent"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "sentiment": {
                            "type": "STRING",
                            "enum": ["positive", "negative", "neutral"],
                        },
                        "confidence": {"type": "NUMBER"},
                        "explanation": {"type": "STRING"},
                        "keywords": {"type": "ARRAY", "items": {"type": "STRING"}},
                    },
                    "required": ["sentiment", "confidence", "explanation", "keywords"],
                },
            },
        }
        headers = {
            "x-goog-api-key": settings.GEMINI_API_KEY,
            "content-type": "application/json",
        }

        try:
            if self._client is None:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(endpoint, headers=headers, json=payload)
            else:
                response = await self._client.post(endpoint, headers=headers, json=payload)

            response.raise_for_status()
            return self._parse_response(response.json())
        except httpx.TimeoutException as exc:
            raise GeminiServiceError("Gemini request timed out.", status_code=504) from exc
        except httpx.HTTPStatusError as exc:
            raise GeminiServiceError(
                f"Gemini API returned HTTP {exc.response.status_code}."
            ) from exc
        except httpx.RequestError as exc:
            raise GeminiServiceError("Could not connect to Gemini API.") from exc
        except (AttributeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise GeminiServiceError(
                "Gemini returned an invalid sentiment response."
            ) from exc

    @staticmethod
    def _build_prompt(text: str) -> str:
        return (
            "Analyze the sentiment of the text below. Return only a JSON object with "
            "sentiment (positive, negative, or neutral), confidence (0 to 1), "
            "explanation, and keywords. Do not include markdown or extra text.\n\n"
            f"Text:\n{text}"
        )

    @staticmethod
    def _parse_response(data: dict[str, Any]) -> SentimentResult:
        candidates = data.get("candidates", [])
        if not candidates:
            raise GeminiServiceError("Gemini returned no candidates.")

        candidate = candidates[0]
        if candidate.get("finishReason") == "MAX_TOKENS":
            raise GeminiServiceError("Gemini response was truncated.")

        parts = candidate.get("content", {}).get("parts", [])
        generated_text = "".join(part.get("text", "") for part in parts)
        if not generated_text:
            raise GeminiServiceError("Gemini returned an empty response.")

        if generated_text.strip().startswith("```"):
            generated_text = generated_text.strip().removeprefix("```json").removesuffix("```").strip()

        result_data = json.loads(generated_text)
        return SentimentResult.model_validate(result_data)
