import asyncio

from app.services.gemini_service import GeminiService, GeminiServiceError


async def main() -> None:
    service = GeminiService()
    text = "This product is excellent. I am very satisfied!"

    try:
        result = await service.analyze_sentiment(text)
    except GeminiServiceError as error:
        print(f"ERROR: {error}")
        return

    print("\n===== SENTIMENT ANALYSIS =====")
    print("Sentiment:", result.sentiment)
    print("Confidence:", result.confidence)
    print("Explanation:", result.explanation)
    print("Keywords:", result.keywords)


if __name__ == "__main__":
    asyncio.run(main())
