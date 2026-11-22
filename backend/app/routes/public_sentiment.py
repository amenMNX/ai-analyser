from fastapi import APIRouter, HTTPException

from app.schemas.sentiment import AnalyzeRequest, PublicSentimentResult
from app.services.public_sentiment_service import (
    PublicSentimentError,
    PublicSentimentService,
)

router = APIRouter(prefix="/api", tags=["Public Sentiment API"])
public_service = PublicSentimentService()


@router.post(
    "/analyze/public",
    response_model=PublicSentimentResult,
    summary="Analyze sentiment using a public API",
)
async def analyze_public(request: AnalyzeRequest) -> PublicSentimentResult:
    try:
        return await public_service.analyze(request.text)
    except PublicSentimentError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error
