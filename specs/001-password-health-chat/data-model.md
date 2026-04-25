# Data Model: Chat-Based Password Health Checker

## Entity: SessionContext
- Purpose: Represents anonymous or semi-anonymous user continuity via session cookie.
- Fields:
  - `id` (uuid, primary key)
  - `session_token_hash` (string, unique, indexed)
  - `created_at` (timestamp)
  - `last_seen_at` (timestamp)
- Constraints:
  - Session token hash must be unique.
  - Token value is never stored in plaintext.

## Entity: HealthAssessment
- Purpose: Stores each password health check result.
- Fields:
  - `id` (uuid, primary key)
  - `session_context_id` (uuid, foreign key -> SessionContext.id)
  - `password_count` (integer, >= 0)
  - `oldest_password_age_days` (integer, >= 0)
  - `score` (integer, 0..100)
  - `status` (enum: HEALTHY, OKAY, CRITICAL)
  - `agent_model` (string, default `gpt-4o-mini`)
  - `created_at` (timestamp)
- Constraints:
  - `score` must be integer in [0,100].
  - `status` must match score band.
  - Record always linked to one session context.

## Entity: GuidanceItem
- Purpose: Persist prioritized recommendations generated for an assessment.
- Fields:
  - `id` (uuid, primary key)
  - `assessment_id` (uuid, foreign key -> HealthAssessment.id)
  - `priority_rank` (integer, >= 1)
  - `title` (string, max 120)
  - `detail` (string, max 400)
- Constraints:
  - `priority_rank` unique within one assessment.
  - Guidance list length in [1,5] for UI readability.

## Derived View: ScoreTrend
- Purpose: API-level projection over historical assessments.
- Inputs: Ordered list of previous `score` values per session.
- Output:
  - `direction` enum: IMPROVING, STABLE, DECLINING
  - `delta_from_previous` integer
- Rules:
  - IMPROVING when latest score > previous score.
  - STABLE when latest score == previous score.
  - DECLINING when latest score < previous score.
