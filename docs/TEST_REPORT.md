# AI Sentiment Analyzer — Test Report

## Environment

- Backend: FastAPI
- Frontend: React + TypeScript + Vite
- Primary provider: Google Gemini API
- Comparison provider: Text-Processing API
- Automated testing: Pytest + FastAPI TestClient

Provider calls are mocked, so the automated suite is repeatable and does not require external services or a live API key.

Command: `cd backend; python -m pytest -v`  
Latest result: **10 passed**, with one non-blocking Starlette/httpx deprecation warning.

| Test area | Expected | Actual | Status |
|---|---|---|---|
| Root endpoint | HTTP 200 | HTTP 200 | PASS |
| Health endpoint | HTTP 200 | HTTP 200 | PASS |
| Positive Gemini analysis | Structured positive result | Passed | PASS |
| Empty input | HTTP 422 | HTTP 422 | PASS |
| Text over 5,000 characters | HTTP 422 | HTTP 422 | PASS |
| Gemini timeout/error | HTTP 504 with detail | Passed | PASS |
| Public provider result | Result with probabilities | Passed | PASS |
| Public provider error | HTTP 502 with detail | Passed | PASS |
| Gemini response parsing | Validated sentiment result | Passed | PASS |
| Phase 3 route smoke test | Valid route behavior | Passed | PASS |

## Frontend verification

The production frontend build passed with `npm run build`.

These live browser checks require local servers and are not represented as automated passes:

- [ ] Gemini, Public API, and Compare modes against live providers
- [ ] Compare mode with one provider unavailable
- [ ] Browser loading and error states
- [ ] Screenshots of dashboard and Swagger evidence

## Security checks

- Gemini credentials remain backend-only.
- `.env` files are excluded by `.gitignore`.
- `.env.example` contains only a placeholder key.
