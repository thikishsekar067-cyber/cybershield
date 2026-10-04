# Cyber Shield AI

AI-assisted phishing detection, cyber awareness and citizen safety platform for India.

## Architecture
- `frontend`: Next.js + TypeScript + Tailwind-style CSS architecture, responsive UI.
- `backend`: FastAPI + SQLAlchemy + MySQL, layered detection engine and upload/OCR/QR pipeline.
- `prisma/schema.prisma`: portable database model reference matching the requested domain model. The Python backend uses SQLAlchemy/Alembic because Prisma is not the appropriate runtime ORM for FastAPI.

## Quick start
1. Copy `backend/.env.example` to `backend/.env` and set `DATABASE_URL`.
2. Create a MySQL database named `cybershield`.
3. `cd backend && python -m venv .venv && .venv/Scripts/activate` (Windows) or `source .venv/bin/activate`.
4. `pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000`.
5. `cd frontend && npm install && npm run dev`.
6. Open `http://localhost:3000`.

## Environment
See `backend/.env.example` and `frontend/.env.example`. Never commit secrets.

## Production notes
- Put FastAPI behind a TLS reverse proxy and restrict CORS.
- Use a managed MySQL instance, Redis-backed rate limiting, object storage with short-lived private objects, and a real identity provider for Google OAuth.
- Keep screenshot/email content ephemeral unless the user explicitly saves an analysis.
- Threat-intelligence and AI providers are optional adapters. If unavailable, deterministic rules remain active.
- The official Indian resources in `backend/app/core/config.py` are centralized so they can be audited/updated without changing UI code.
