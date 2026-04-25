<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Template Principle 1 -> I. Contracted Web Stack
- Template Principle 2 -> II. Validate Every Input
- Template Principle 3 -> III. Mobile-Ready Friendly UX
- Template Principle 4 -> IV. Commented Functions, Clear Ownership
- Template Principle 5 -> V. Structured AI Responses
Added sections:
- Product Constraints
- Delivery Workflow
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ Reviewed .github/prompts/*.prompt.md for outdated agent-specific wording; no changes required
- ✅ Reviewed .specify/extensions/git/commands/*.md for outdated agent-specific wording; no changes required
Follow-up TODOs:
- None
-->

# Password Health Manager Constitution

## Core Principles

### I. Contracted Web Stack
This product MUST be delivered as a web application with a Next.js 15 frontend in
TypeScript and a FastAPI backend in Python. Frontend status and summary surfaces MUST
use shadcn/ui components for cards and progress bars. Any deviation from this stack or
component rule requires an explicit constitution amendment because a fixed stack keeps
delivery, maintenance, and review consistent.

### II. Validate Every Input
Every user-provided value MUST be validated at the first boundary it crosses and again
at the backend contract when trust changes. Invalid, missing, malformed, or out-of-range
input MUST produce a friendly error message that explains what to fix without exposing
internal details. This is non-negotiable because the app evaluates sensitive password
manager health signals and cannot rely on best-effort input handling.

### III. Mobile-Ready Friendly UX
All primary flows MUST work on mobile screens as a first-class target, not as a desktop
layout compressed after the fact. Specifications, plans, and acceptance checks MUST
include responsive behavior and readable error states for narrow viewports. This keeps
the product usable where people actually inspect personal security posture: on phones as
well as larger screens.

### IV. Commented Functions, Clear Ownership
Every application function MUST include a concise comment describing its purpose and any
important side effects, assumptions, or contract details. New code MUST keep validation,
presentation, and integration responsibilities separated so reviews can verify where each
 rule is enforced. The rationale is simple: this project mixes frontend, API, and agent
logic, so maintainability depends on explicit function-level intent and traceable control
boundaries.

### V. Structured AI Responses
Any Python agent built with the OpenAI Agent SDK MUST return structured JSON on every
success and failure path. Response shapes MUST be intentionally defined, validated, and
documented so the frontend and API can consume them without guessing. This principle
exists because password-health guidance is only reliable when AI outputs are machine-
checkable and operationally predictable.

## Product Constraints

- The frontend MUST use Next.js 15 with TypeScript.
- The backend MUST use FastAPI with typed request and response models.
- Cards and progress bars MUST use shadcn/ui components or wrapper components built on
	top of shadcn/ui primitives.
- Validation rules MUST be enforced for forms, query parameters, API payloads, and agent
	inputs.
- Error handling MUST provide user-friendly messages in the UI and structured error JSON
	at service boundaries.
- Mobile support MUST be part of the definition of done for every feature.

## Delivery Workflow

- Every specification MUST capture validation rules, mobile behavior, friendly error
	states, and structured JSON expectations when a feature touches the agent or API.
- Every implementation plan MUST pass a constitution check for stack compliance,
	validation coverage, mobile responsiveness, function comments, and AI response schema
	design before detailed design begins.
- Every task list MUST include work items for validation, responsive UI verification,
	friendly error handling, and structured JSON response handling where applicable.
- Code review MUST reject changes that add functions without comments, bypass boundary
	validation, or introduce unstructured agent responses.

## Governance

This constitution overrides conflicting local conventions for this repository.
Amendments require a documented rationale, an impact review across templates and runtime
guidance, and an updated Sync Impact Report in this file. Semantic versioning applies to
governance changes: MAJOR for incompatible principle removals or redefinitions, MINOR
for new principles or materially expanded obligations, and PATCH for wording-only
clarifications. Compliance reviews MUST verify stack alignment, input validation,
friendly error messaging, mobile behavior, function comments, and structured AI outputs
before implementation is approved and again before release.

**Version**: 1.0.0 | **Ratified**: 2026-04-25 | **Last Amended**: 2026-04-25
