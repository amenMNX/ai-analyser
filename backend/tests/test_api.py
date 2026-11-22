from fastapi.testclient import TestClient

from app.main import app
from app.routes import public_sentiment, sentiment
from app.schemas.sentiment import PublicSentimentResult, SentimentResult
from app.services.gemini_service import GeminiServiceError
from app.services.public_sentiment_service import PublicSentimentError

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "sentiment-analyzer-backend",
    }


def test_analyze_positive(monkeypatch) -> None:
    async def fake_analyze(text: str) -> SentimentResult:
        assert text == "This product is excellent."
        return SentimentResult(
            sentiment="positive",
            confidence=0.98,
            explanation="The text expresses satisfaction.",
            keywords=["excellent", "satisfaction"],
        )

    monkeypatch.setattr(sentiment.gemini_service, "analyze_sentiment", fake_analyze)
    response = client.post("/api/analyze", json={"text": "This product is excellent."})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"
    assert response.json()["confidence"] == 0.98


def test_empty_text_is_rejected() -> None:
    response = client.post("/api/analyze", json={"text": "   "})
    assert response.status_code == 422


def test_text_over_5000_characters_is_rejected() -> None:
    response = client.post("/api/analyze", json={"text": "x" * 5001})
    assert response.status_code == 422


def test_gemini_service_error_is_returned_as_http_error(monkeypatch) -> None:
    async def fake_analyze(text: str) -> SentimentResult:
        raise GeminiServiceError("Gemini request timed out.", status_code=504)

    monkeypatch.setattr(sentiment.gemini_service, "analyze_sentiment", fake_analyze)
    response = client.post("/api/analyze", json={"text": "Test timeout"})
    assert response.status_code == 504
    assert response.json()["detail"] == "Gemini request timed out."


def test_public_provider_result(monkeypatch) -> None:
    async def fake_analyze(text: str) -> PublicSentimentResult:
        return PublicSentimentResult(
            sentiment="positive",
            confidence=0.9,
            probabilities={"positive": 0.9, "negative": 0.1, "neutral": 0.2},
        )

    monkeypatch.setattr(public_sentiment.public_service, "analyze", fake_analyze)
    response = client.post("/api/analyze/public", json={"text": "Great product"})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"
    assert "probabilities" in response.json()


def test_public_provider_error_is_returned_as_http_error(monkeypatch) -> None:
    async def fake_analyze(text: str) -> PublicSentimentResult:
        raise PublicSentimentError("Public sentiment API unavailable.")

    monkeypatch.setattr(public_sentiment.public_service, "analyze", fake_analyze)
    response = client.post("/api/analyze/public", json={"text": "Test failure"})
    assert response.status_code == 502
    assert response.json()["detail"] == "Public sentiment API unavailable."
