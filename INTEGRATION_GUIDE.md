# Frontend-Backend Integration Guide

## Overview

The Next.js frontend communicates with the FastAPI backend via HTTP requests using the `NEXT_PUBLIC_API_BASE_URL` environment variable. All requests include session cookies for user identity tracking.

## Architecture

```
Next.js Frontend (Vercel)
    ↓ (fetch + credentials: include)
FastAPI Backend (Separate Host)
    ↓ (CORS checks FRONTEND_ORIGIN)
PostgreSQL + Prisma (Neon)
```

## Environment Setup

### Frontend (.env.local)

```bash
# Local development
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Production (deployed on Vercel)
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.example.com
```

### Backend (.env)

```bash
# Local development
FRONTEND_ORIGIN=http://localhost:3000
COOKIE_SECURE=false
APP_ENV=development

# Production deployment
FRONTEND_ORIGIN=https://your-project.vercel.app
COOKIE_SECURE=true
APP_ENV=production
```

## API Endpoints

### POST /v1/health-checks

**Request:**
```json
{
  "passwordCount": 20,
  "oldestPasswordAgeDays": 180
}
```

**Response:**
```json
{
  "assessmentId": "uuid",
  "score": 75,
  "status": "Healthy",
  "color": "green",
  "guidance": [
    {
      "priorityRank": 1,
      "title": "Strong Foundation",
      "detail": "You're maintaining good password hygiene."
    }
  ]
}
```

**Error Response:**
```json
{
  "message": "Invalid input values",
  "detail": "passwordCount must be between 0 and 1000000"
}
```

### GET /v1/health-checks/history

**Response:**
```json
{
  "items": [
    {
      "assessmentId": "uuid",
      "score": 75,
      "status": "Healthy",
      "createdAt": "2025-04-25T10:30:00Z"
    }
  ],
  "trend": {
    "direction": "IMPROVING",
    "deltaFromPrevious": 5
  }
}
```

## Frontend Implementation

### API Client (lib/api-client.ts)

Features:
- ✅ Environment variable support (`NEXT_PUBLIC_API_BASE_URL`)
- ✅ Type-safe request/response (TypeScript)
- ✅ Session cookies (`credentials: "include"`)
- ✅ Error parsing with friendly messages
- ✅ Fallback to localhost

```typescript
// Returns API base URL from environment with localhost fallback.
function apiBase(): string {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
}

// Parses a friendly message from API error response payload.
async function parseErrorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json();
    if (typeof data?.message === "string") return data.message;
    if (typeof data?.detail?.message === "string") return data.detail.message;
  } catch {
    // Keeps fallback message when response is not JSON.
  }
  return "Something went wrong. Please try again.";
}

// Calls POST endpoint to create a new health check and returns typed result.
export async function createHealthCheck(payload: {
  passwordCount: number;
  oldestPasswordAgeDays: number;
}): Promise<HealthCheckResponse> {
  const response = await fetch(`${apiBase()}/v1/health-checks`, {
    method: "POST",
    credentials: "include",  // ← Sends session cookies
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await parseErrorMessage(response));
  }

  return (await response.json()) as HealthCheckResponse;
}

// Calls GET endpoint for historical assessments of current session.
export async function getHistory(): Promise<HistoryResponse> {
  const response = await fetch(`${apiBase()}/v1/health-checks/history`, {
    method: "GET",
    credentials: "include",  // ← Sends session cookies
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    throw new Error(await parseErrorMessage(response));
  }

  return (await response.json()) as HistoryResponse;
}
```

### Frontend Page (app/page.tsx)

Features:
- ✅ Form input validation (Zod)
- ✅ Error state management
- ✅ Loading state during submission
- ✅ Mobile-responsive layout
- ✅ Session-based history

```typescript
async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();
  setErrorMessage(null);

  // 1. Validate input before sending
  const parsed = healthInputSchema.safeParse({
    passwordCount: Number(passwordCount),
    oldestPasswordAgeDays: Number(oldestPasswordAgeDays),
  });

  if (!parsed.success) {
    setErrorMessage(parsed.error.issues[0]?.message ?? "Please review your input values.");
    return;
  }

  setIsSubmitting(true);
  try {
    // 2. Make API call with proper error handling
    const response = await createHealthCheck(parsed.data);
    setResult(response);
  } catch (error) {
    // 3. Show friendly error message
    setErrorMessage(error instanceof Error ? error.message : "Unable to complete check right now.");
  } finally {
    setIsSubmitting(false);
  }
}
```

## Backend Implementation

### CORS Configuration (main.py)

```python
def _allowed_origins() -> list[str]:
    """Builds CORS allow-list from environment with safe local default."""
    origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    return [origin]

# Configures CORS for frontend calls that include session cookies.
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,  # ← Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Input Validation (api/dependencies/validation.py)

```python
# Validates password count and age are within acceptable ranges.
def validate_input_ranges(password_count: int, oldest_password_age_days: int) -> None:
    if not (0 <= password_count <= 1_000_000):
        raise ValueError("passwordCount must be between 0 and 1,000,000")
    if not (0 <= oldest_password_age_days <= 36_500):  # 100 years
        raise ValueError("oldestPasswordAgeDays must be between 0 and 36,500 days")
```

### Health Check Route (api/routes/health_checks.py)

```python
@router.post("", response_model=HealthCheckResponse)
async def create_health_check(
    payload: HealthCheckRequest, 
    request: Request, 
    response: Response
) -> HealthCheckResponse:
    """Creates a new password health assessment and returns score, status, color, and guidance."""
    
    logger.info("create_health_check.started")
    
    # 1. Validate input ranges
    validate_input_ranges(payload.passwordCount, payload.oldestPasswordAgeDays)
    
    # 2. Get or create session (returns HTTP-only cookie)
    session_hash = get_or_create_session_hash(request, response)
    
    # 3. Calculate score, status, color
    score = compute_score(payload.passwordCount, payload.oldestPasswordAgeDays)
    status = get_status(score)
    color = get_color(status)
    
    # 4. Get AI-powered guidance
    guidance = await get_recommendations(
        password_count=payload.passwordCount,
        oldest_password_age_days=payload.oldestPasswordAgeDays,
        score=score,
        status=status,
    )
    
    # 5. Persist to database
    entry = await save_assessment(
        session_hash=session_hash,
        password_count=payload.passwordCount,
        oldest_age_days=payload.oldestPasswordAgeDays,
        score=score,
        status=status,
        color=color,
        guidance=guidance,
        prisma_client=prisma_facade.client,
    )
    
    logger.info("create_health_check.completed status=%s score=%s", status, score)
    
    return HealthCheckResponse(
        assessmentId=entry["assessmentId"],
        score=score,
        status=status,
        color=color,
        guidance=guidance,
    )


@router.get("/history", response_model=HistoryResponse)
async def get_health_check_history(
    request: Request, 
    response: Response
) -> HistoryResponse:
    """Returns chronological assessment history and trend metadata for current session."""
    
    logger.info("get_health_check_history.started")
    
    # 1. Get session hash from cookie
    session_hash = get_or_create_session_hash(request, response)
    
    # 2. Query history from database
    history = await get_history(session_hash, prisma_client=prisma_facade.client)
    
    # 3. Transform response
    items = [
        HistoryItemResponse(
            assessmentId=item["assessmentId"],
            score=item["score"],
            status=item["status"],
            createdAt=item["createdAt"],
        )
        for item in history
    ]
    
    # 4. Calculate trend
    trend = compute_trend(history)
    
    logger.info("get_health_check_history.completed items=%s", len(items))
    return HistoryResponse(items=items, trend=trend)
```

## Troubleshooting

### "CORS error" when calling API
- ✅ Check `FRONTEND_ORIGIN` environment variable on backend matches frontend domain
- ✅ Verify `allow_credentials=True` in CORSMiddleware
- ✅ Confirm backend is running and accessible

### "No session cookie" or "Invalid session"
- ✅ Verify `credentials: "include"` in fetch calls
- ✅ Check `SESSION_COOKIE_SECRET` is set in backend .env
- ✅ Ensure cookies are HTTP-only (not accessible from JavaScript)

### "Unable to parse response" errors
- ✅ Check API response matches `HealthCheckResponse` or `HistoryResponse` types
- ✅ Verify backend is not throwing 500 errors (check logs)
- ✅ Test API manually: `curl -X POST http://localhost:8000/v1/health-checks -H "Content-Type: application/json" -d '{"passwordCount":20,"oldestPasswordAgeDays":180}' -v`

### Production deployment issues
- ✅ Set `FRONTEND_ORIGIN=https://your-project.vercel.app` on backend
- ✅ Set `COOKIE_SECURE=true` on backend (production only)
- ✅ Update frontend `.env.production` with backend URL
- ✅ Backend must be accessible from internet (not localhost)

## Deployment Checklist

**Frontend (Vercel)**
- [ ] Deploy from `001-build-password-health-checker` branch
- [ ] Set `NEXT_PUBLIC_API_BASE_URL` environment variable to backend URL
- [ ] Verify build succeeds (Next.js detection working)
- [ ] Test API calls work from deployed site

**Backend (e.g., Railway, Render, AWS)**
- [ ] Set `FRONTEND_ORIGIN` to Vercel URL
- [ ] Set `DATABASE_URL` to Neon connection string
- [ ] Set `OPENAI_API_KEY` for agent guidance
- [ ] Set `SESSION_COOKIE_SECRET` to secure random string
- [ ] Set `APP_ENV=production`
- [ ] Set `COOKIE_SECURE=true`
- [ ] Run `prisma migrate deploy` before startup
- [ ] Start with: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Response Flow Diagram

```
User submits form on frontend
  ↓
Frontend validates input (Zod schema)
  ↓
Frontend calls POST /v1/health-checks
  ├─ Includes: passwordCount, oldestPasswordAgeDays
  ├─ Headers: Content-Type: application/json, credentials: include
  ↓
Backend receives request
  ├─ CORS check: is origin in FRONTEND_ORIGIN? ✓
  ├─ Input validation: ranges OK? ✓
  ├─ Get/create session cookie
  ├─ Compute score (0-100)
  ├─ Generate status (Healthy/Okay/Critical)
  ├─ Call OpenAI Agent for guidance
  ├─ Persist to database
  ↓
Backend returns HealthCheckResponse
  ├─ Set-Cookie: sessionHash (HTTP-only, SameSite)
  ├─ JSON body: score, status, color, guidance[]
  ↓
Frontend receives response
  ├─ Parse JSON to HealthCheckResponse
  ├─ Display ScoreCard component
  ├─ Display GuidanceList component
  ↓
User views results + recommendations
```

