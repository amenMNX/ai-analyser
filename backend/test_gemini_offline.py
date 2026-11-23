import json

import httpx

from app.schemas.sentiment import SentimentResult
from app.services.gemini_service import GeminiService


async def _test_service_parses_a_valid_gemini_response() -> None:
    response_body = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": json.dumps(
                                {
                                    "sentiment": "positive",
                                    "confidence": 0.96,
                                    "explanation": "The customer expresses satisfaction.",
                                    "keywords": ["excellent", "satisfied"],
                                }
                            )
                        }
                    ]
                }
            }
        ]
    }

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-goog-api-key"]
        assert request.url.path.endswith("/models/gemini-3.5-flash-lite:generateContent")
        return httpx.Response(200, json=response_body)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await GeminiService(client).analyze_sentiment("This is excellent!")

    assert isinstance(result, SentimentResult)
    assert result.sentiment == "positive"
    assert result.confidence == 0.96


def test_service_parses_a_valid_gemini_response() -> None:
    import asyncio

    asyncio.run(_test_service_parses_a_valid_gemini_response())
