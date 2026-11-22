from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.public_sentiment import router as public_sentiment_router
from app.routes.sentiment import router as sentiment_router

app = FastAPI(
    title="AI Sentiment Analyzer API",
    description="REST API for AI-powered sentiment analysis",
    version="1.0.0",
)

app.include_router(sentiment_router)
app.include_router(public_sentiment_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "AI Sentiment Analyzer API",
        "status": "running",
    }


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "sentiment-analyzer-backend",
    }
