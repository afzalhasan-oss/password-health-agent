# Implementation Plan: Chat-Based Password Health Checker

**Branch**: `[001-build-password-health-checker]` | **Date**: 2026-04-25 | **Spec**: `specs/001-password-health-chat/spec.md`
**Input**: Feature specification from `/specs/001-password-health-chat/spec.md`

## Summary

Build a chat-driven password health checker with a Next.js 15 + TypeScript frontend and a FastAPI backend that uses OpenAI Agent SDK (`gpt-4o-mini`) to produce structured JSON recommendations. Users submit password count and oldest password age, receive a 0-100 score with a color-coded shadcn/ui card and progress bar, then review persisted history from Neon PostgreSQL to track trend direction over time.

## Technical Context

**Language/Version**: TypeScript 5.x (Next.js 15), Python 3.12 (FastAPI)  
**Primary Dependencies**: Next.js 15, Tailwind CSS, shadcn/ui, FastAPI, Pydantic v2, OpenAI Agents SDK, Prisma ORM, prisma-client-py, psycopg driver  
**Storage**: Neon serverless PostgreSQL for assessment history  
**Testing**: Frontend: Vitest + React Testing Library; Backend: pytest + httpx + contract/schema validation  
**Target Platform**: Web (mobile + desktop), backend API hosted for Vercel frontend consumption  
**Project Type**: Web application (frontend + backend)  
**Performance Goals**: P95 score request latency < 1500 ms; history list retrieval < 2000 ms for 100 records/user  
**Constraints**: Input validation on every boundary, friendly error messages, session cookie for history identity, structured JSON from agent every time, use shadcn/ui card and progress bar for score display  
**Scale/Scope**: Initial release for single-region deployment, up to 10k users, up to 500 assessments per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Mandated stack compliance: **PASS** (Next.js 15 + TypeScript + FastAPI)
- shadcn/ui card + progress usage: **PASS** (required in UI components)
- Input validation and friendly errors: **PASS** (frontend zod + backend pydantic + API error model)
- Mobile-screen behavior defined: **PASS** (mobile-first layouts and acceptance checks)
- Function comments requirement: **PASS** (coding rule in implementation tasks)
- Structured JSON agent responses: **PASS** (contracted schema and runtime validation)

## Project Structure

### Documentation (this feature)

```text
specs/001-password-health-chat/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── api.openapi.yaml
│   └── agent-response.schema.json
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── health_checks.py
│   │   └── dependencies/
│   ├── agents/
│   │   └── password_health_agent.py
│   ├── models/
│   │   ├── request_models.py
│   │   └── response_models.py
│   ├── services/
│   │   ├── scoring_service.py
│   │   ├── recommendation_service.py
│   │   └── history_service.py
│   ├── db/
│   │   ├── prisma_client.py
│   │   └── session_store.py
│   └── main.py
├── prisma/
│   └── schema.prisma
├── tests/
│   ├── contract/
│   ├── integration/
│   └── unit/
└── pyproject.toml

frontend/
├── app/
│   ├── page.tsx
│   └── history/page.tsx
├── components/
│   ├── ui/
│   └── features/
│       ├── score-card.tsx
│       ├── score-progress.tsx
│       ├── guidance-list.tsx
│       └── history-chart.tsx
├── lib/
│   ├── api-client.ts
│   ├── validation.ts
│   └── score-color.ts
├── tests/
│   ├── integration/
│   └── unit/
└── package.json
```

**Structure Decision**: Use a two-app web architecture (`frontend/` and `backend/`) to keep Vercel UI deployment independent from Python API lifecycle while preserving strict API contracts.

## Phase 0: Research Output

Key design decisions are documented in `research.md`:
1. Deterministic score-band mapping for Healthy/Okay/Critical.
2. Session-cookie identity strategy for unauthenticated user history.
3. Prisma with Neon from Python via `prisma-client-py` for model consistency.
4. Structured JSON contract enforcement between OpenAI agent and API.

## Phase 1: Design Output

1. Data model defined in `data-model.md` for assessment, guidance item, session context.
2. API and JSON contracts defined in `contracts/`.
3. Local/dev quickstart defined in `quickstart.md` with `uv`, Prisma, Next.js, and Vercel deployment notes.

## Risk Tracking

| Risk | Why It Matters | Mitigation |
|------|----------------|------------|
| Prisma in Python stack complexity | Prisma tooling is Node-first and adds generation step | Pin Prisma versions and automate `prisma generate` in CI |
| Session-cookie-only identity | Device/browser changes may fragment history | Document behavior and plan optional account link in future |
| LLM output drift | Non-JSON output can break UI flow | Strict schema validation and fallback safe response |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Prisma in FastAPI backend | Required by product constraint for Neon persistence | Raw SQL/SQLAlchemy rejected due to explicit Prisma requirement |
