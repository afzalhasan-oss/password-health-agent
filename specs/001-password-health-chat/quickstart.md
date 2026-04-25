# Quickstart: Chat-Based Password Health Checker

## Prerequisites
- Node.js 20+
- Python 3.12+
- `uv` package manager
- Prisma CLI
- Neon PostgreSQL database URL
- OpenAI API key with access to `gpt-4o-mini`

## 1. Environment setup

Create `.env` files for frontend and backend.

Backend required variables:
- `OPENAI_API_KEY`
- `OPENAI_MODEL=gpt-4o-mini`
- `DATABASE_URL` (Neon PostgreSQL)
- `SESSION_COOKIE_SECRET`
- `FRONTEND_ORIGIN`

Frontend required variables:
- `NEXT_PUBLIC_API_BASE_URL`

## 2. Backend setup (FastAPI + uv)

```bash
cd backend
uv sync
uv run prisma generate
uv run prisma db push
uv run uvicorn app.main:app --reload --port 8000
```

## 3. Frontend setup (Next.js 15 + Tailwind + shadcn/ui)

```bash
cd frontend
npm install
npm run dev
```

## 4. Contract check

- Submit a scoring request from UI.
- Confirm API returns:
  - score card payload with `score`, `status`, and color token mapping.
  - structured recommendation list.
  - persisted history item ID.

## 5. Local validation checklist

- Invalid inputs show friendly actionable messages.
- Healthy/Okay/Critical mapping matches thresholds:
  - Healthy: 75-100
  - Okay: 40-74
  - Critical: 0-39
- Score card and progress bar render with shadcn/ui components.
- History endpoint returns chronological records for current session cookie.
- Mobile viewport (375px width) supports full submit -> result -> history flow.

## 6. Deploy

Frontend (Vercel):
- Import `frontend/` project in Vercel.
- Set `NEXT_PUBLIC_API_BASE_URL` to backend URL.

Backend:
- Deploy FastAPI service on Python-compatible host.
- Set production env vars and Neon `DATABASE_URL`.
- Enable CORS for Vercel frontend domain.
- Ensure secure cookie settings (`HttpOnly`, `Secure`, `SameSite=Lax`).

## 7. Implementation validation checklist

- Confirm all tasks are checked in `specs/001-password-health-chat/tasks.md`.
- Review `specs/001-password-health-chat/checklists/implementation-validation.md` and verify each item.
