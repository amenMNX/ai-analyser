import asyncio
import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.routes import public_sentiment, sentiment
from app.services.public_sentiment_service import PublicSentimentService


class FakeGeminiService:
    async def analyze_sentiment(self, text: str):
        return {
            "sentiment": "positive",
            "confidence": 0.9,
            "explanation": f"Analyzed: {text}",
            "keywords": ["excellent"],
        }


async def _test_public_service_maps_provider_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.content == b"text=This+is+excellent%21"
        return httpx.Response(
            200,
            json={
                "label": "pos",
                "probability": {"neg": 0.1, "neutral": 0.2, "pos": 0.9},
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await PublicSentimentService(client).analyze("This is excellent!")
    assert result.sentiment == "positive"
    assert result.confidence == 0.9


def test_routes_validate_input_and_return_provider_results() -> None:
    original_gemini = sentiment.gemini_service
    sentiment.gemini_service = FakeGeminiService()
    try:
        client = TestClient(app)
        response = client.post("/api/analyze", json={"text": "Great product"})
        assert response.status_code == 200
        assert response.json()["sentiment"] == "positive"
        assert client.post("/api/analyze", json={"text": "   "}).status_code == 422
        assert client.post("/api/analyze", json={"text": "x" * 5001}).status_code == 422
    finally:
        sentiment.gemini_service = original_gemini


if __name__ == "__main__":
    asyncio.run(_test_public_service_maps_provider_response())
    test_routes_validate_input_and_return_provider_results()
    print("Phase 3 offline tests passed")
