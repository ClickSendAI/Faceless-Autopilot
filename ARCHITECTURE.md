# Architecture — Faceless Autopilot AI

## Overview

The system follows a microservices pattern. All backend services are FastAPI applications that share a single PostgreSQL database and a single Redis instance. The Next.js frontend communicates with each service directly (no API gateway).

```
Browser (Next.js :8560)
    │
    ├── POST /api/content/generate   → ai-content  (:8561)
    │                                      │
    │                                      ├── OpenAI GPT-4 (script)
    │                                      ├── ElevenLabs API (voice)
    │                                      └── Pexels API + FFmpeg (video)
    │
    ├── POST /api/platforms/upload   → platform-apis (:8562)
    │                                      │
    │                                      ├── YouTube Data API v3
    │                                      ├── TikTok for Business API
    │                                      └── Instagram Graph API
    │
    └── GET  /api/analytics/...      → analytics (:8563)
                                           │
                                           └── Aggregated from DB + platform pull
```

## Services

### ai-content (port 8561)

**Responsibilities:** Script generation, voiceover synthesis, video assembly.

**Key modules:**
- `app/main.py` — FastAPI app, route definitions, background task dispatch
- `app/services/openai_service.py` — GPT-4 chat completions for script and topic generation
- `app/services/elevenlabs_service.py` — ElevenLabs TTS, voice selection, audio file persistence
- `app/services/video_service.py` — Pexels search, FFmpeg composition, platform-specific dimension handling
- `app/models.py` — SQLAlchemy ORM: `User`, `Content`, `Analytics`, `PlatformIntegration`
- `app/schemas.py` — Pydantic request/response models
- `app/database.py` — SQLAlchemy engine, session factory, `get_db` dependency
- `app/core/config.py` — `pydantic-settings` Settings class, reads `.env`

**Data flow:**
1. `POST /api/content/generate` creates a `Content` row (status=`processing`) and enqueues `process_content_generation` as a FastAPI background task.
2. Background task calls OpenAI → ElevenLabs → Pexels/FFmpeg sequentially. On completion it updates `Content.status` to `completed` and stores file URLs.
3. `GET /api/content/{id}/status` reads the `Content` row and returns current status + video URL.

### platform-apis (port 8562)

**Responsibilities:** Upload content to YouTube, TikTok, and Instagram; schedule future uploads.

**Key modules:**
- `app/main.py` — Routes: `/api/platforms/upload`, `/api/platforms/status/{id}`, `/api/platforms/schedule`
- `app/services/youtube_service.py` — YouTube Data API v3 wrapper (currently stubbed)
- `app/services/tiktok_service.py` — TikTok for Business API wrapper (currently stubbed)
- `app/services/instagram_service.py` — Instagram Graph API wrapper (currently stubbed)
- `app/schemas.py` — `UploadRequest`, `UploadResponse`, `UploadStatus`, `PlatformCredentials`, `ScheduleRequest`

**Data flow:** `POST /api/platforms/upload` creates an upload record and dispatches a background task that iterates over requested platforms, calling each service's `upload_video` / `upload_reel` method. Results are aggregated and stored.

### analytics (port 8563)

**Responsibilities:** Aggregate performance data, serve insights, provide revenue projections.

**Key modules:**
- `app/main.py` — Routes: overview, content analytics, insights, sync, revenue, trends
- `app/services/analytics_service.py` — All analytics logic (currently returns static mock data)
- `app/schemas.py` / `app/models.py` — Pydantic and SQLAlchemy models

**Data flow:** Endpoints delegate to `AnalyticsService` methods. Platform sync (`/api/analytics/sync`) is intended to pull live data from YouTube/TikTok/Instagram APIs; currently returns mock results.

### user-management (port 8004)

**Status: not implemented.** Directory structure exists (`services/user-management/app/`) but contains no Python source files. JWT-based authentication referenced in other services' configs has no backing implementation.

## Database Schema

All services share one PostgreSQL database (`faceless_autopilot_ai`). Four tables:

| Table | Description |
|-------|-------------|
| `users` | Account, email, password hash, subscription tier, API key storage |
| `content` | Generated content record: script text, voice URL, video URL, status, target platforms |
| `analytics` | Per-content per-platform metrics: views, engagement rate, revenue |
| `platform_integrations` | Encrypted OAuth tokens per user per platform |

## Frontend (faceless-frontend)

Next.js 15 / React 19 / TypeScript. UI built with Tailwind CSS + shadcn/ui (Radix UI primitives). Charts via Recharts.

**Key components:**
- `components/dashboard.tsx` — Tab shell: Overview, Generate, Analytics, Upload, Manage
- `components/content-generator.tsx` — Multi-step form that calls `ai-content` POST and polls for status
- `components/analytics-dashboard-real.tsx` — Recharts visualizations sourced from the analytics service
- `components/services-status.tsx` — Health check panel polling all three service `/health` endpoints
- `components/content-upload.tsx` — Triggers platform-apis upload flow
- `components/content-management.tsx` — Lists and manages generated content
- `lib/api.ts` — Typed fetch wrappers for all three backend services

## Deployment

Docker Compose orchestrates all services, PostgreSQL, and Redis. Services depend on healthy DB and Redis before starting. Frontend is built as a Next.js production image on port 8560.

For production: replace hardcoded database credentials with environment variables, add an API gateway or reverse proxy (nginx/Traefik) in front of all services, and implement OAuth flows for each platform integration.
