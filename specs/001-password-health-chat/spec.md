# Feature Specification: Chat-Based Password Health Checker

**Feature Branch**: `[001-build-password-health-checker]`  
**Created**: 2026-04-25  
**Status**: Draft  
**Input**: User description: "Build a chat-based Password Management Health Checker where the user tells the agent how many passwords they have and how old their oldest password is. The agent calculates a password health score from 0 to 100 and displays the result in a color-coded shadcn/ui card: green for Healthy, yellow for Okay, and red for Critical. The agent should also provide a short, prioritized list of what the user should fix first, written in an encouraging and non-scary tone. The app must remember past scores so users can track whether their password health is improving over time. Historical score data will be stored in a Neon serverless database. The frontend will use Next.js 15 with TypeScript, and the backend will use Python FastAPI with the OpenAI Agent SDK returning structured JSON for every response."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get an Immediate Health Score (Priority: P1)

As a user, I can enter how many passwords I have and how old my oldest password is, then receive a score from 0 to 100 with a clear health label and a color-coded result card so I can quickly understand my password-management risk.

**Why this priority**: This is the core value proposition. Without a score and clear status, the product does not deliver its primary benefit.

**Independent Test**: Can be fully tested by submitting valid input values and verifying a returned numeric score, matching health status category, and correct card color mapping.

**Acceptance Scenarios**:

1. **Given** a user provides valid input for password count and oldest password age, **When** they submit the chat request, **Then** the system returns a score between 0 and 100 with a health label and displays it in a color-coded result card.
2. **Given** a returned score is in the healthy range, **When** the result is shown, **Then** the card uses the green Healthy state.
3. **Given** a returned score is in the middle range, **When** the result is shown, **Then** the card uses the yellow Okay state.
4. **Given** a returned score is in the highest-risk range, **When** the result is shown, **Then** the card uses the red Critical state.

---

### User Story 2 - Receive Encouraging Prioritized Guidance (Priority: P2)

As a user, I receive a short prioritized list of the most important fixes to do first, written in an encouraging and non-scary tone, so I know what actions matter most and feel motivated to improve.

**Why this priority**: Actionable guidance is what converts a score into practical behavior change.

**Independent Test**: Can be tested by submitting valid input and verifying the output includes a concise ordered action list that uses supportive language and avoids alarmist phrasing.

**Acceptance Scenarios**:

1. **Given** a score has been calculated, **When** guidance is generated, **Then** the response includes a prioritized list of recommended fixes.
2. **Given** guidance is generated, **When** text is displayed, **Then** wording is encouraging, non-scary, and focused on practical next steps.

---

### User Story 3 - Track Improvement Over Time (Priority: P3)

As a user, I can view my historical scores so I can tell whether my password health is improving over time and stay accountable.

**Why this priority**: Progress tracking increases retention and reinforces healthy security habits.

**Independent Test**: Can be tested by saving multiple assessments and confirming historical entries and trend direction are visible and accurate.

**Acceptance Scenarios**:

1. **Given** a user has completed at least two assessments, **When** they open history, **Then** they can see previous scores in chronological order.
2. **Given** historical scores exist, **When** trend information is displayed, **Then** users can tell whether their health is improving, stable, or declining.

### Edge Cases

- User enters non-numeric, negative, or unrealistically large values for password count or password age.
- User submits one field but leaves the other empty.
- User has no historical assessments yet and opens history.
- Historical storage is temporarily unavailable when saving or reading scores.
- Score lands exactly on status boundaries and must map consistently to a single health label and color.
- User accesses the flow from a mobile-width screen with limited horizontal space.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept user-provided values for total password count and oldest-password age as the minimum required scoring input.
- **FR-002**: System MUST validate all user input before scoring and provide a friendly, corrective error message when input is invalid.
- **FR-003**: System MUST compute and return a password health score on a 0 to 100 scale.
- **FR-004**: System MUST classify the score into one of three statuses: Healthy, Okay, or Critical.
- **FR-005**: System MUST display the result in a color-coded card using green for Healthy, yellow for Okay, and red for Critical.
- **FR-006**: System MUST provide a short, prioritized list of recommended fixes for the user to perform first.
- **FR-007**: System MUST ensure recommendation language is encouraging and non-scary.
- **FR-008**: System MUST persist each completed score result with timestamped history for later retrieval.
- **FR-009**: System MUST allow users to view historical score entries and understand direction of change over time.
- **FR-010**: System MUST support mobile-width usage for scoring, result viewing, and history viewing flows.
- **FR-011**: System MUST use structured JSON contracts for every AI-agent response and every backend response consumed by the frontend.
- **FR-012**: System MUST handle backend, agent, and storage failures with user-friendly messages while preserving system stability.

### Key Entities *(include if feature involves data)*

- **Health Assessment**: A single scoring event containing user inputs, calculated score, status label, prioritized guidance, and assessment timestamp.
- **Score History Record**: A persisted historical entry associated with a user profile, used for chronological display and trend determination.
- **User Profile Context**: The logical user identity context under which assessments are stored and retrieved.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of users can complete a new assessment and view their score in under 60 seconds.
- **SC-002**: 100% of successful assessments return a score in the inclusive range of 0 to 100 with exactly one status label.
- **SC-003**: 100% of invalid input submissions show a friendly and actionable correction message.
- **SC-004**: 90% of users report that recommendations are clear, encouraging, and not fear-inducing.
- **SC-005**: 100% of completed assessments are retrievable in history within 2 seconds under normal operating conditions.
- **SC-006**: 95% of users can correctly identify whether their password health trend is improving, stable, or declining from the history view.
- **SC-007**: 100% of agent and backend responses consumed by the UI conform to documented structured JSON response shapes.

## Assumptions

- A valid user profile context is available so score history can be associated with the correct person.
- The product will store historical score data in an existing managed relational data service configured for this project.
- Trend direction is determined from chronological historical scores and is displayed as improving, stable, or declining.
- The initial release supports English-language guidance text.
- The score model uses only the provided minimum inputs unless later expanded by a future feature.
