# AI Sentiment Analyzer

The application combines a React dashboard, a FastAPI REST gateway, and two independent sentiment providers.

## Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS v4
- Backend: FastAPI, Uvicorn, Pydantic Settings
- Primary AI provider: Google Gemini REST API
- Comparison provider: Text-Processing Sentiment API

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`, with docs at `/docs` and a health check at `/api/health`.

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The page checks the backend health endpoint and provides Gemini, Public API, and Compare analysis modes.

Do not put a Gemini API key in the frontend. Frontend variables prefixed with `VITE_` are public.

## Gemini integration

Add a real key to `backend/.env` locally, then test the external service from the backend directory:

```powershell
cd backend
python test_gemini.py
```

The key is sent only in the backend `x-goog-api-key` header. The standalone script reports a clear error when the placeholder key is still configured.

## REST API

Once the backend is running, Swagger is available at `http://localhost:8000/docs`.

- `POST /api/analyze` — Gemini-backed sentiment analysis
- `POST /api/analyze/public` — comparison analysis through Text-Processing.com

Both endpoints accept `{ "text": "..." }`. Input is trimmed and limited to 5,000 characters. The public provider is intended primarily for English comparison text; Gemini remains the primary multilingual provider.

## Security

The Gemini API key is loaded only by the backend and is never exposed in React code or browser requests. `.env` and `.venv` files are excluded by `.gitignore`; `backend/.env.example` contains only a placeholder key.

## Documentation

- [Setup guide](docs/SETUP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [REST API](docs/API.md)
- [Test report](docs/TEST_REPORT.md)
- [Screenshot evidence guide](docs/screenshots/README.md)
