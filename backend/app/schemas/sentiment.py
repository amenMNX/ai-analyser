from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Text to analyze",
    )

    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Text cannot be empty.")
        return value


class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(
        ge=0,
        le=1,
        description="Estimated confidence between 0 and 1",
    )
    explanation: str = Field(min_length=1)
    keywords: list[str]


class PublicSentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1)
    probabilities: dict[str, float]
