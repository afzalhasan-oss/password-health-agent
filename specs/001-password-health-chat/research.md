# Research: Chat-Based Password Health Checker

## Decision 1: Score band thresholds
- Decision: Use fixed bands: Healthy 75-100, Okay 40-74, Critical 0-39.
- Rationale: Deterministic thresholds simplify QA, allow predictable color mapping, and support stable trend analysis.
- Alternatives considered:
  - Dynamic banding from model output: rejected due to unstable UX and non-deterministic testing.
  - Higher Healthy floor at 80: rejected to avoid discouraging users early in adoption.

## Decision 2: Agent output contract
- Decision: OpenAI Agent SDK must return strict structured JSON validated against a schema before sending to client.
- Rationale: Prevent malformed outputs and preserve compatibility with frontend rendering.
- Alternatives considered:
  - Free-form text parsing: rejected due to fragility.
  - Partial JSON with fallback text: rejected because it weakens contract guarantees.

## Decision 3: Session-based user history
- Decision: Use a signed HTTP-only session cookie as primary history identity in v1.
- Rationale: Minimal onboarding friction and supports immediate usage.
- Alternatives considered:
  - Mandatory account login: rejected for higher user friction in MVP.
  - Local storage only: rejected because history must be persisted server-side in Neon.

## Decision 4: Neon persistence with Prisma in Python backend
- Decision: Manage schema with Prisma and consume via `prisma-client-py` from FastAPI services.
- Rationale: Satisfies explicit Prisma requirement while preserving Python backend.
- Alternatives considered:
  - SQLAlchemy with Alembic: rejected due to explicit Prisma requirement.
  - Direct SQL via psycopg only: rejected due to lower schema governance and migration ergonomics.

## Decision 5: Deployment topology
- Decision: Deploy frontend to Vercel and backend to a separate Python host endpoint exposed to Vercel.
- Rationale: Vercel is explicit target for frontend, while FastAPI remains runtime-flexible.
- Alternatives considered:
  - Single monolith runtime: rejected due to mixed runtime complexity.
  - Edge-only backend: rejected due to Python + Prisma operational constraints.
