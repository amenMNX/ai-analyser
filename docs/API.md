# REST API Documentation

Base URL: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

## Common request schema

```json
{
  "text": "This product is excellent!"
}
```

`text` is trimmed, must contain at least one non-whitespace character, and cannot exceed 5,000 characters.

## `GET /`

Checks that the backend process is running.

```json
{
  "message": "AI Sentiment Analyzer API",
  "status": "running"
}
```

## `GET /api/health`

Returns backend health status.

```json
{
  "status": "healthy",
  "service": "sentiment-analyzer-backend"
}
```

## `POST /api/analyze`

Analyzes text through Google Gemini.

```json
{
  "sentiment": "positive",
  "confidence": 0.98,
  "explanation": "The text expresses satisfaction.",
  "keywords": ["excellent", "satisfaction"]
}
```

Statuses: `200` success, `422` invalid input, `502` Gemini failure, `504` Gemini timeout.

## `POST /api/analyze/public`

Analyzes text through the Text-Processing comparison provider.

```json
{
  "sentiment": "positive",
  "confidence": 0.8,
  "probabilities": {
    "positive": 0.8,
    "negative": 0.1,
    "neutral": 0.1
  }
}
```

Statuses: `200` success, `422` invalid input, `502` public provider failure, `504` public provider timeout.

The public provider is English-oriented and is an additional comparison service, not a replacement for Gemini. React calls only FastAPI; the Gemini key is never sent to the frontend.
