# CORS Configuration Guide

## Overview

CORS (Cross-Origin Resource Sharing) allows your Next.js frontend on Vercel to make requests to your FastAPI backend. When the frontend and backend are on different domains, the browser sends an **OPTIONS preflight request** before the actual request.

## Current Configuration

**Backend (`backend/app/main.py`):**
```python
def _configure_cors(app: FastAPI) -> None:
    """Configures CORS middleware for frontend calls with session cookies."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(),           # List of allowed domains
        allow_credentials=True,                      # Required for cookies
        allow_methods=["GET", "POST", "OPTIONS"],   # Explicit (no wildcards with credentials)
        allow_headers=["Content-Type", "Authorization"],  # Request headers
        expose_headers=["Content-Type"],            # Response headers visible to JS
        max_age=600,                                 # Cache preflight for 10 min
    )
```

**Environment Variables:**
```bash
# .env (backend)
FRONTEND_ORIGIN=https://your-project.vercel.app    # Production Vercel domain
# or
FRONTEND_ORIGIN=http://localhost:3000               # Local development
```

## How CORS Works with Credentials

### Browser Preflight Flow (Automatic)

```
1. Browser detects cross-origin request with credentials
   ↓
2. Browser sends OPTIONS preflight request:
   OPTIONS /v1/health-checks HTTP/1.1
   Origin: https://your-project.vercel.app
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: content-type
   ↓
3. Backend responds with CORS headers:
   Access-Control-Allow-Origin: https://your-project.vercel.app
   Access-Control-Allow-Credentials: true
   Access-Control-Allow-Methods: GET, POST, OPTIONS
   Access-Control-Allow-Headers: Content-Type, Authorization
   ↓
4. Browser checks: Origin in allow_origins? ✓
   Methods include POST? ✓
   Headers include Content-Type? ✓
   ↓
5. Browser proceeds with actual request:
   POST /v1/health-checks HTTP/1.1
   Content-Type: application/json
   Cookie: sessionHash=...
```

### Frontend Code (Next.js)

```typescript
// lib/api-client.ts
export async function createHealthCheck(payload: {
  passwordCount: number;
  oldestPasswordAgeDays: number;
}): Promise<HealthCheckResponse> {
  const response = await fetch(`${apiBase()}/v1/health-checks`, {
    method: "POST",
    credentials: "include",  // ← Includes cookies in request
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await parseErrorMessage(response));
  }

  return (await response.json()) as HealthCheckResponse;
}
```

**Key:** `credentials: "include"` is required to send session cookies. Without it, cookies won't be sent.

## Common CORS Issues & Fixes

### ❌ Issue: "Access to XMLHttpRequest has been blocked by CORS policy"

**Symptom:**
```
Access to XMLHttpRequest at 'https://api.example.com/v1/health-checks' 
from origin 'https://my-app.vercel.app' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check.
```

**Causes & Fixes:**

1. **Wrong domain in FRONTEND_ORIGIN**
   ```bash
   # ❌ Wrong
   FRONTEND_ORIGIN=http://localhost:3000  # Production build uses Vercel domain!
   
   # ✅ Correct
   FRONTEND_ORIGIN=https://my-app.vercel.app
   ```

2. **Wildcard with credentials not allowed**
   ```python
   # ❌ Wrong
   CORSMiddleware(
       allow_origins=["*"],  # Wildcard not allowed with credentials
       allow_credentials=True,
   )
   
   # ✅ Correct
   CORSMiddleware(
       allow_origins=["https://my-app.vercel.app"],  # Explicit domain
       allow_credentials=True,
   )
   ```

3. **Method not allowed**
   ```python
   # ❌ Wrong
   allow_methods=["GET"],  # POST not in list
   
   # ✅ Correct
   allow_methods=["GET", "POST", "OPTIONS"]
   ```

4. **Header not allowed**
   ```python
   # ❌ Wrong
   allow_headers=[]  # Content-Type not allowed
   
   # ✅ Correct
   allow_headers=["Content-Type", "Authorization"]
   ```

### ❌ Issue: "Credentials mode is 'include', but Access-Control-Allow-Credentials is missing"

**Fix:**
```python
CORSMiddleware(
    allow_origins=["https://my-app.vercel.app"],
    allow_credentials=True,  # ← Must be True when sending cookies
)
```

### ❌ Issue: "Cookie not being sent or received"

**Checklist:**
- [ ] Frontend uses `credentials: "include"` in fetch
- [ ] Backend has `allow_credentials=True`
- [ ] Backend sets `Set-Cookie` header with `HttpOnly`, `SameSite=Lax`
- [ ] Cookie domain matches or is `None` with `Secure` flag
- [ ] Check browser DevTools: Network tab → Response Headers for `Set-Cookie`

**Backend session store example:**
```python
def set_session_cookie(response: Response, session_hash: str) -> None:
    """Sets secure HTTP-only session cookie."""
    cookie_secure = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    
    response.set_cookie(
        key="sessionHash",
        value=session_hash,
        httponly=True,        # Not accessible from JavaScript
        secure=cookie_secure, # HTTPS only in production
        samesite="lax",       # CSRF protection
        max_age=30 * 24 * 60 * 60,  # 30 days
    )
```

## Debugging Steps

### 1. Check Environment Variables
```bash
# SSH into backend and verify
echo $FRONTEND_ORIGIN
# Output should be: https://my-app.vercel.app
```

### 2. Test with cURL
```bash
# Preflight request
curl -X OPTIONS https://api.example.com/v1/health-checks \
  -H "Origin: https://my-app.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  -v

# Look for these response headers:
# Access-Control-Allow-Origin: https://my-app.vercel.app
# Access-Control-Allow-Credentials: true
# Access-Control-Allow-Methods: GET, POST, OPTIONS
```

### 3. Check Browser Console & Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Make API call from your app
4. Look for OPTIONS request (preflight)
5. Check Response Headers:
   ```
   Access-Control-Allow-Origin: https://my-app.vercel.app
   Access-Control-Allow-Credentials: true
   Access-Control-Allow-Methods: GET, POST, OPTIONS
   Access-Control-Allow-Headers: Content-Type, Authorization
   ```

### 4. Check Backend Logs
```bash
# FastAPI logs should show both requests
[INFO] OPTIONS /v1/health-checks  # Preflight
[INFO] POST /v1/health-checks     # Actual request
```

### 5. Test Frontend Env Var
```typescript
// In browser console
console.log(process.env.NEXT_PUBLIC_API_BASE_URL)
// Output: https://api.example.com
```

## Production Deployment Checklist

**Before deploying backend:**
- [ ] Set `FRONTEND_ORIGIN=https://your-project.vercel.app`
- [ ] Set `APP_ENV=production`
- [ ] Set `COOKIE_SECURE=true`
- [ ] Verify CORSMiddleware is added BEFORE other middleware
- [ ] Test preflight request with cURL

**Before deploying frontend (Vercel):**
- [ ] Set `NEXT_PUBLIC_API_BASE_URL=https://your-backend.example.com`
- [ ] Verify backend is publicly accessible
- [ ] Test API calls work from deployed site

**After deployment:**
- [ ] Open browser DevTools
- [ ] Make API call from app
- [ ] Verify OPTIONS preflight succeeds
- [ ] Verify POST request succeeds
- [ ] Check cookies are being set/sent

## Complete FastAPI Example

```python
# backend/app/main.py

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.dependencies.error_handlers import install_error_handlers
from app.api.routes.health_checks import router as health_checks_router
from app.db.prisma_client import prisma_facade

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("password_health_api")

app = FastAPI(title="Password Health Checker API", version="0.1.0")


def _allowed_origins() -> list[str]:
    """Builds CORS allow-list from environment with safe local default."""
    origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    return [origin]


def _configure_cors(app: FastAPI) -> None:
    """Configures CORS middleware for frontend calls with session cookies.
    
    When credentials (cookies) are included, wildcards (*) are not allowed for
    origins, methods, or headers. All must be explicitly listed.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(),           # Frontend domain only
        allow_credentials=True,                      # Required for Set-Cookie
        allow_methods=["GET", "POST", "OPTIONS"],   # Explicit methods
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type"],
        max_age=600,  # Cache preflight for 10 minutes
    )


# Add CORS middleware FIRST (before other middleware)
_configure_cors(app)

install_error_handlers(app)
app.include_router(health_checks_router)


@app.on_event("startup")
async def on_startup() -> None:
    """Initializes database connectivity during application startup."""
    app_env = os.getenv("APP_ENV", "development").lower()
    cookie_secure = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    if app_env == "production" and not cookie_secure:
        logger.warning("COOKIE_SECURE should be true in production environments.")
    await prisma_facade.connect()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Closes database connectivity during graceful application shutdown."""
    await prisma_facade.disconnect()


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Simple health check endpoint (no CORS restrictions needed)."""
    return {"status": "healthy"}
```

## Environment Setup

**.env (backend)**
```bash
# Development
FRONTEND_ORIGIN=http://localhost:3000
APP_ENV=development
COOKIE_SECURE=false

# Production
FRONTEND_ORIGIN=https://your-project.vercel.app
APP_ENV=production
COOKIE_SECURE=true
```

**.env.local (frontend)**
```bash
# Development
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Production (set in Vercel UI)
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.example.com
```

## Testing CORS Locally

```bash
# Terminal 1: Start backend
cd backend
uv run uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev

# Terminal 3: Test preflight
curl -X OPTIONS http://localhost:8000/v1/health-checks \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  -v
```

## Summary

| Config | Value | Why |
|--------|-------|-----|
| `allow_origins` | Explicit list (no `*`) | Wildcard forbidden with credentials |
| `allow_credentials` | `True` | Required to send/receive cookies |
| `allow_methods` | `["GET", "POST", "OPTIONS"]` | Explicit list required |
| `allow_headers` | `["Content-Type", "Authorization"]` | Explicit list required |
| `max_age` | `600` | Reduce preflight requests |
| Middleware order | First in app | Must run before other middleware |

