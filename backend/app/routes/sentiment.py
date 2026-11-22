import logging

from fastapi import APIRouter, HTTPException

from app.schemas.sentiment import AnalyzeRequest, SentimentResult
from app.services.gemini_service import GeminiService, GeminiServiceError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Sentiment Analysis"])
gemini_service = GeminiService()


@router.post(
    "/analyze",
    response_model=SentimentResult,
    summary="Analyze text sentiment",
    description="Analyzes text using Google Gemini AI.",
)
async def analyze_sentiment(request: AnalyzeRequest) -> SentimentResult:
    try:
        return await gemini_service.analyze_sentiment(request.text)
    except GeminiServiceError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error
