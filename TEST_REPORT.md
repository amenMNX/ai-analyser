# AI Sentiment Analyzer — Test Report

## Environment

- Backend: FastAPI
- Frontend: React + TypeScript + Vite
- Primary provider: Google Gemini API
- Comparison provider: Text-Processing API
- Automated testing: Pytest + FastAPI TestClient

## Automated tests

All provider calls in the automated suite are mocked; no external API key or network service is required.

Command: `python -m pytest -v`  
Result: **10 passed**, 1 non-blocking Starlette deprecation warning.

| Test area | Expected | Result | Status |
|---|---|---|---|
| Root endpoint | HTTP 200 | Verified | PASS |
| Health endpoint | HTTP 200 | Verified | PASS |
| Positive Gemini analysis | Structured positive result | Verified | PASS |
| Empty input | HTTP 422 | Verified | PASS |
| Text over 5,000 characters | HTTP 422 | Verified | PASS |
| Gemini timeout/error | HTTP 504 with detail | Verified | PASS |
| Public provider result | Structured result with probabilities | Verified | PASS |
| Public provider error | HTTP 502 with detail | Verified | PASS |
| Frontend production build | Vite build succeeds | Verified | PASS |

## Manual/live checks

These require the backend and frontend servers to be started locally and are intentionally not marked as passed automatically:

- [ ] Gemini positive, negative, and neutral requests through Swagger
- [ ] Public API English positive, negative, and neutral requests
- [ ] Frontend Gemini mode
- [ ] Frontend Public API mode
- [ ] Frontend Compare mode
- [ ] Compare mode with one provider unavailable
- [ ] Browser loading and error states
- [ ] Screenshots of Swagger and dashboard results

## Security checks

- Gemini credentials remain backend-only.
- `.env` files are excluded by `.gitignore`.
- `.env.example` contains only a placeholder key.
