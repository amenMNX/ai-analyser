# Setup and operation

See the repository [README](../README.md) for complete installation, operation, API, and testing instructions.

Verification endpoints:

- Frontend: http://localhost:5173
- Backend root: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/api/health
- Dashboard: http://localhost:5173

Run backend tests from `backend` with `python -m pytest -v`. Provider calls are mocked and do not consume API quota.
