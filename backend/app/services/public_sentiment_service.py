import httpx

from app.schemas.sentiment import PublicSentimentResult

PUBLIC_API_URL = "https://text-processing.com/api/sentiment/"


class PublicSentimentError(Exception):
    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


class PublicSentimentService:
    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    async def analyze(self, text: str) -> PublicSentimentResult:
        try:
            if self._client is None:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    response = await client.post(PUBLIC_API_URL, data={"text": text})
            else:
                response = await self._client.post(PUBLIC_API_URL, data={"text": text})
            response.raise_for_status()

            data = response.json()
            label = data["label"]
            raw_probabilities = data["probability"]
            label_map = {"pos": "positive", "neg": "negative", "neutral": "neutral"}
            sentiment = label_map[label]
            probabilities = {
                "positive": float(raw_probabilities["pos"]),
                "negative": float(raw_probabilities["neg"]),
                "neutral": float(raw_probabilities["neutral"]),
            }
            return PublicSentimentResult(
                sentiment=sentiment,
                confidence=probabilities[sentiment],
                probabilities=probabilities,
            )
        except httpx.TimeoutException as exc:
            raise PublicSentimentError(
                "Public sentiment request timed out.", status_code=504
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise PublicSentimentError(
                f"Public sentiment API returned HTTP {exc.response.status_code}."
            ) from exc
        except httpx.RequestError as exc:
            raise PublicSentimentError(
                "Could not connect to the public sentiment API."
            ) from exc
        except (KeyError, TypeError, ValueError) as exc:
            raise PublicSentimentError(
                "Public sentiment API returned an invalid response."
            ) from exc
