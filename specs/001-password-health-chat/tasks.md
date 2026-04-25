# Tasks: Chat-Based Password Health Checker

**Input**: Design documents from `/specs/001-password-health-chat/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Dedicated test tasks are not listed because tests were not explicitly requested in the feature spec.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`US1`, `US2`, `US3`)
- All descriptions include exact file paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize frontend/backend workspaces and baseline tooling.

- [X] T001 Create backend project skeleton per plan in `backend/app/`, `backend/tests/`, and `backend/prisma/`
- [X] T002 Initialize Python backend with uv and dependencies in `backend/pyproject.toml`
- [X] T003 Create frontend Next.js 15 TypeScript app with Tailwind in `frontend/package.json`, `frontend/app/`, and `frontend/tailwind.config.ts`
- [X] T004 Install and initialize shadcn/ui in `frontend/components/ui/` and `frontend/components.json`
- [X] T005 [P] Add environment templates in `backend/.env.example` and `frontend/.env.example`
- [X] T006 [P] Add repo-level ignore and scripts updates in `.gitignore` and `README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement cross-story building blocks that all user stories depend on.

**⚠️ CRITICAL**: No user story work begins until this phase is complete.

- [X] T007 Define Prisma schema for `SessionContext`, `HealthAssessment`, and `GuidanceItem` in `backend/prisma/schema.prisma`
- [X] T008 Generate Prisma client and db bootstrap wrapper in `backend/app/db/prisma_client.py`
- [X] T009 Implement session cookie identity helpers in `backend/app/db/session_store.py`
- [X] T010 Create shared FastAPI request/response models in `backend/app/models/request_models.py` and `backend/app/models/response_models.py`
- [X] T011 Implement global API error model and handlers in `backend/app/api/dependencies/error_handlers.py`
- [X] T012 Implement request validation boundaries and friendly error mapping in `backend/app/api/dependencies/validation.py`
- [X] T013 Add FastAPI app entrypoint with CORS and router registration in `backend/app/main.py`
- [X] T014 Build frontend API client and typed response guards in `frontend/lib/api-client.ts`
- [X] T015 Build frontend form validation schema in `frontend/lib/validation.ts`
- [X] T016 Create score color/status mapping utility in `frontend/lib/score-color.ts`
- [X] T017 Add structured JSON schema enforcement for agent output in `backend/app/agents/password_health_agent.py` using `specs/001-password-health-chat/contracts/agent-response.schema.json`
- [X] T018 Confirm all new backend functions include comments in `backend/app/**/*.py`

**Checkpoint**: Foundation is complete; user story work can start.

---

## Phase 3: User Story 1 - Immediate Health Score (Priority: P1) 🎯 MVP

**Goal**: User submits two inputs and receives a 0-100 score with status and color-coded shadcn/ui card + progress bar.

**Independent Test**: Submit valid values from homepage and verify score/status/color mapping is correct with friendly validation errors for invalid input.

### Implementation for User Story 1

- [X] T019 [P] Implement deterministic scoring service with band mapping in `backend/app/services/scoring_service.py`
- [X] T020 [P] Implement initial assessment persistence service in `backend/app/services/history_service.py`
- [X] T021 Implement health check POST route in `backend/app/api/routes/health_checks.py`
- [X] T022 Implement homepage chat/input flow in `frontend/app/page.tsx`
- [X] T023 Build score card feature component using shadcn/ui card in `frontend/components/features/score-card.tsx`
- [X] T024 Build score progress component using shadcn/ui progress in `frontend/components/features/score-progress.tsx`
- [X] T025 Connect homepage submit flow to API client and render score components in `frontend/app/page.tsx`
- [X] T026 Add mobile-first layout and responsive states for score flow in `frontend/app/page.tsx` and `frontend/components/features/score-card.tsx`
- [X] T027 Add friendly user-facing validation and failure messages in `frontend/app/page.tsx`
- [X] T028 Add backend function comments and route-level comments for US1 changes in `backend/app/services/scoring_service.py` and `backend/app/api/routes/health_checks.py`

**Checkpoint**: US1 is fully functional as an MVP.

---

## Phase 4: User Story 2 - Encouraging Prioritized Guidance (Priority: P2)

**Goal**: User receives short prioritized recommendations in an encouraging, non-scary tone.

**Independent Test**: Run scoring flow and verify guidance list is ordered, concise, and supportive in tone.

### Implementation for User Story 2

- [X] T029 [P] Implement recommendation prompt and schema-constrained agent call in `backend/app/agents/password_health_agent.py`
- [X] T030 [P] Implement recommendation orchestration service in `backend/app/services/recommendation_service.py`
- [X] T031 Extend POST response model with guidance payload in `backend/app/models/response_models.py`
- [X] T032 Persist guidance items linked to assessments in `backend/app/services/history_service.py`
- [X] T033 Render prioritized guidance list component in `frontend/components/features/guidance-list.tsx`
- [X] T034 Integrate guidance rendering into score result area in `frontend/app/page.tsx`
- [X] T035 Add friendly fallback guidance when agent call fails in `backend/app/services/recommendation_service.py`
- [X] T036 Add function comments for all new backend/frontend functions touched in US2 files

**Checkpoint**: US1 + US2 work independently and together.

---

## Phase 5: User Story 3 - Historical Trend Tracking (Priority: P3)

**Goal**: User sees chronological score history and trend direction from session-linked records.

**Independent Test**: Create multiple assessments in one session and verify history list plus improving/stable/declining trend output.

### Implementation for User Story 3

- [X] T037 [P] Implement history query and trend calculation in `backend/app/services/history_service.py`
- [X] T038 Implement history GET route in `backend/app/api/routes/health_checks.py`
- [X] T039 Build history page route in `frontend/app/history/page.tsx`
- [X] T040 Build history visualization component in `frontend/components/features/history-chart.tsx`
- [X] T041 Integrate history API retrieval with session cookie behavior in `frontend/lib/api-client.ts` and `frontend/app/history/page.tsx`
- [X] T042 Add empty-state and error-state UX for history view in `frontend/app/history/page.tsx`
- [X] T043 Ensure mobile responsiveness for history page and chart in `frontend/app/history/page.tsx` and `frontend/components/features/history-chart.tsx`
- [X] T044 Add function comments for US3 backend/frontend changes in touched files

**Checkpoint**: All user stories are independently functional.

---

## Phase 6: Polish & Cross-Cutting

**Purpose**: Harden quality, docs, and deployment readiness.

- [X] T045 [P] Align API implementation with OpenAPI contract in `specs/001-password-health-chat/contracts/api.openapi.yaml`
- [X] T046 [P] Validate agent response shape against JSON schema in `specs/001-password-health-chat/contracts/agent-response.schema.json`
- [X] T047 Add production cookie security settings and verification in `backend/app/main.py` and `backend/app/db/session_store.py`
- [X] T048 Add observability logging for scoring, agent, and persistence paths in `backend/app/api/routes/health_checks.py`
- [X] T049 Update quickstart and deployment notes with final commands in `specs/001-password-health-chat/quickstart.md`
- [X] T050 Run end-to-end manual walkthrough for mobile + desktop flows and record checklist in `specs/001-password-health-chat/checklists/implementation-validation.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1; blocks all stories.
- **Phase 3 (US1)**: Depends on Phase 2 completion.
- **Phase 4 (US2)**: Depends on Phase 2 and integrates with US1 output.
- **Phase 5 (US3)**: Depends on Phase 2 and uses persisted assessments from US1/US2 paths.
- **Phase 6 (Polish)**: Depends on completion of selected story phases.

### User Story Dependencies

- **US1 (P1)**: Independent after foundational phase.
- **US2 (P2)**: Independent after foundational phase but reuses US1 result rendering path.
- **US3 (P3)**: Independent after foundational phase but relies on stored assessment data from completed submissions.

### Parallel Opportunities

- Setup tasks `T005`, `T006` can run with other setup tasks.
- Foundational tasks `T014`, `T015`, `T016`, `T017` can run in parallel after core backend skeleton exists.
- US1 tasks `T019` and `T020` can run in parallel.
- US2 tasks `T029` and `T030` can run in parallel.
- US3 tasks `T037` and `T039` can run in parallel.
- Polish tasks `T045` and `T046` can run in parallel.

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3.
3. Validate scoring flow on desktop and mobile.
4. Demo/deploy MVP.

### Incremental Delivery

1. Deliver US1 (score + status card).
2. Add US2 (encouraging prioritized guidance).
3. Add US3 (history + trend tracking).
4. Finish with hardening and deployment polish.

## Notes

- Every backend and frontend function added in this feature must include a concise comment.
- Friendly error handling is required in all user-facing forms and responses.
- Agent outputs must remain structured JSON on both success and failure paths.
