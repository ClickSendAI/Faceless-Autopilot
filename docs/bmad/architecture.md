# Architecture Document
## Faceless Autopilot AI

**Version:** 1.1  
**Date:** 2026-05-17  
**Status:** Current  
**Author:** Raphael Bernardo Gonzalez Nunes da Rocha

---

## 1. Introduction

### 1.1 Purpose

This document describes the technical architecture of Faceless Autopilot AI as derived from the current codebase. It serves as the reference for engineering decisions, onboarding, and future development.

### 1.2 Architectural Goals

- **Separation of concerns** — each microservice owns one domain (content generation, platform distribution, analytics)
- **Async-first** — all I/O operations use Python `async/await` to avoid blocking the event loop
- **Containerized** — each service ships as a Docker image; Docker Compose orchestrates the full stack locally
- **Extensible** — adding a new platform (e.g., Pinterest Video) requires only a new service class and a new route handler

---

## 2. System Context

```
┌─────────────────────────────────────────────────────────┐
│ Browser                                                 │
│  Next.js 15 dashboard (port 8560)                       │
└───────┬─────────────────────────────────────────────────┘
        │ HTTP fetch (browser → service, no API gateway)
        │
┌───────▼──────────┐  ┌───────────────────┐  ┌──────────────────┐
│ ai-content       │  │ platform-apis     │  │ analytics        │
│ FastAPI :8561    │  │ FastAPI :8562     │  │ FastAPI :8563    │
└───────┬──────────┘  └────────┬──────────┘  └────────┬─────────┘
        │                      │                       │
        └──────────────────────┴───────────────────────┘
                               │
               ┌───────────────┴────────────┐
               │                            │
       ┌───────▼────────┐         ┌─────────▼──────┐
       │ PostgreSQL 15  │         │ Redis 7        │
       │ port 5432      │         │ port 6379      │
       └────────────────┘         └────────────────┘
```

External API dependencies:
- **OpenAI** — GPT-4 chat completions (script generation)
- **ElevenLabs** — text-to-speech API (voiceover synthesis)
- **Pexels** — video search API (stock footage)
- **YouTube Data API v3** — video upload
- **TikTok for Business API** — video upload
- **Instagram Graph API** — Reels upload

---

## 3. Component Architecture

### 3.1 ai-content Service

**Technology:** FastAPI 0.104, SQLAlchemy 2.0, asyncio  
**Port:** 8561  
**Docker context:** `services/ai-content/`

#### Module Breakdown

```
app/
├── __init__.py
├── main.py              FastAPI app, route handlers, background task dispatch
├── models.py            SQLAlchemy ORM: User, Content, Analytics, PlatformIntegration
├── schemas.py           Pydantic: ContentRequest, ContentResponse, ContentStatus, etc.
├── database.py          Engine, SessionLocal, get_db dependency, init_db()
├── core/
│   ├── __init__.py
│   └── config.py        pydantic-settings Settings class; reads .env
└── services/
    ├── __init__.py
    ├── openai_service.py    AsyncOpenAI client; generate_script(), optimize_script(), generate_trending_topics()
    ├── elevenlabs_service.py httpx async client; generate_voiceover(), get_available_voices()
    └── video_service.py     Pexels search, FFmpeg composition; assemble_video()
```

#### Key Design Decisions

- `process_content_generation` runs as a FastAPI BackgroundTask. It opens its own `SessionLocal` session (not the request session, which closes at response time).
- `Content.status` drives the status polling API. Values: `processing`, `completed`, `failed`.
- Audio files are saved to `generated_audio/` directory; video files to `generated_videos/`. In production these should be replaced with S3 pre-signed URLs.
- ElevenLabs voice resolution: if `voice_id == "default"`, the service fetches available voices and prefers any voice with "professional" or "business" in the name.

#### API Surface

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service liveness |
| POST | `/api/content/generate` | Start async content generation |
| GET | `/api/content/{id}/status` | Poll generation status |
| POST | `/api/content/{id}/regenerate` | Re-run generation pipeline |

---

### 3.2 platform-apis Service

**Technology:** FastAPI 0.104, SQLAlchemy 2.0, httpx  
**Port:** 8562  
**Docker context:** `services/platform-apis/`

#### Module Breakdown

```
app/
├── __init__.py
├── main.py              Routes: upload, status, schedule
├── models.py            Shared ORM models (same schema as ai-content)
├── schemas.py           UploadRequest, UploadResponse, UploadStatus, PlatformCredentials, ScheduleRequest
├── database.py          Session management
├── core/
│   ├── __init__.py
│   └── config.py
└── services/
    ├── __init__.py
    ├── youtube_service.py    YouTubeService.upload_video() — currently stubbed
    ├── tiktok_service.py     TikTokService.upload_video() — currently stubbed
    └── instagram_service.py  InstagramService.upload_reel() — currently stubbed
```

#### Scheduling

`POST /api/platforms/schedule` receives a `schedule_time` datetime parameter. The background task calculates delay as `(schedule_time - utcnow()).total_seconds()` and `await asyncio.sleep(delay)` before calling `process_platform_uploads`. This is suitable for development/testing; production should use a task queue (Celery + Redis or equivalent).

#### Upload Flow

```
POST /api/platforms/upload
  └── background task: process_platform_uploads(upload_id, request)
        ├── youtube_service.upload_video()   → {video_id, url, status}
        ├── tiktok_service.upload_video()    → {video_id, url, status}
        └── instagram_service.upload_reel()  → {video_id, url, status}
```

---

### 3.3 analytics Service

**Technology:** FastAPI 0.104, SQLAlchemy 2.0, pandas, numpy  
**Port:** 8563  
**Docker context:** `services/analytics/`

#### Module Breakdown

```
app/
├── __init__.py
├── main.py              Routes: overview, content, insights, sync, revenue, trends
├── models.py            Pydantic response models (not ORM; analytics reads from shared DB)
├── schemas.py           AnalyticsOverview, ContentAnalytics, PerformanceInsights
├── database.py          Session management
├── core/
│   ├── __init__.py
│   └── config.py
└── services/
    ├── __init__.py
    └── analytics_service.py  AnalyticsService: all analytics methods (currently returning static mock data)
```

#### Current State

All `AnalyticsService` methods return static mock data. The intended implementation is to query the `analytics` table in PostgreSQL and supplement with live pulls from platform APIs. The schemas and method signatures are in place; only the data layer is missing.

---

### 3.4 user-management Service

**Status: not implemented.**  
Directory `services/user-management/` exists with a `Dockerfile` but `app/` is empty. The other services reference `USER_MANAGEMENT_URL` in their configs but make no actual calls to it. JWT validation is absent from all routes.

---

### 3.5 Frontend (faceless-frontend)

**Technology:** Next.js 15, React 19, TypeScript, Tailwind CSS 4, shadcn/ui (Radix UI)  
**Port:** 8560 (dev and production)  
**Build:** pnpm, next build

#### Component Hierarchy

```
app/
└── page.tsx              Renders <Dashboard />

components/
├── dashboard.tsx          Tab shell, state management (activeTab, generatedContent)
├── content-generator.tsx  Step form → POST /api/content/generate → poll status
├── analytics-dashboard-real.tsx  Recharts charts from analytics service
├── services-status.tsx    Health checks for all three services, 30s auto-refresh
├── content-upload.tsx     Triggers POST /api/platforms/upload
├── content-management.tsx Lists and manages content records
├── stats-cards.tsx        Summary KPI cards
├── content-grid.tsx       Grid of recent content thumbnails
├── quick-actions.tsx      Shortcut buttons
├── sidebar.tsx            Navigation sidebar
└── header.tsx             Top bar with menu toggle

lib/
└── api.ts                 Typed fetch wrappers: aiContentAPI, platformAPI, analyticsAPI, checkAllServicesHealth
```

#### API Client Design

`lib/api.ts` exports three namespace objects (`aiContentAPI`, `platformAPI`, `analyticsAPI`) and a `checkAllServicesHealth()` utility. All are re-exported as `api.aiContent`, `api.platform`, `api.analytics`. `checkAllServicesHealth` is a named top-level export (not on `api`).

---

## 4. Data Model

All services share one PostgreSQL database. SQLAlchemy models are duplicated across service codebases (no shared library); this is a deliberate microservice boundary trade-off.

```
users
  id UUID PK
  email VARCHAR(255) UNIQUE NOT NULL
  name VARCHAR(255) NOT NULL
  password_hash VARCHAR(255) NOT NULL
  subscription_tier VARCHAR(50) DEFAULT 'free'
  api_keys JSONB
  created_at TIMESTAMPTZ
  updated_at TIMESTAMPTZ

content
  id UUID PK
  user_id UUID FK→users.id NOT NULL
  title VARCHAR(500) NOT NULL
  description TEXT
  script TEXT
  voice_file_url VARCHAR(500)
  video_file_url VARCHAR(500)
  status VARCHAR(50) DEFAULT 'processing'  -- processing | completed | failed
  platforms JSONB
  content_metadata JSONB
  created_at TIMESTAMPTZ
  updated_at TIMESTAMPTZ

analytics
  id UUID PK
  content_id UUID FK→content.id NOT NULL
  user_id UUID FK→users.id NOT NULL
  platform VARCHAR(100) NOT NULL
  views INTEGER DEFAULT 0
  engagement_rate FLOAT DEFAULT 0.0
  revenue FLOAT DEFAULT 0.0
  date TIMESTAMPTZ
  analytics_metrics JSONB
  created_at TIMESTAMPTZ

platform_integrations
  id UUID PK
  user_id UUID FK→users.id NOT NULL
  platform VARCHAR(100) NOT NULL
  api_key_encrypted TEXT
  is_active BOOLEAN DEFAULT FALSE
  last_sync TIMESTAMPTZ
  settings JSONB
  created_at TIMESTAMPTZ
```

---

## 5. Infrastructure

### Docker Compose

```yaml
services: postgres, redis, ai-content, platform-apis, analytics, user-management, frontend
```

- `postgres` and `redis` have health checks; all application services depend on their health.
- Application images are built from per-service Dockerfiles.
- Shared volumes: `postgres_data`, `redis_data`, `./generated_content`, `./generated_audio`.

### Environment Configuration

Each service reads configuration from environment variables via `pydantic-settings`. Required variables:

```
DATABASE_URL        postgresql://<user>:<pass>@<host>:5432/faceless_autopilot_ai
REDIS_URL           redis://<host>:6379
OPENAI_API_KEY      (ai-content only)
ELEVENLABS_API_KEY  (ai-content only)
PEXELS_API_KEY      (ai-content only)
SECRET_KEY          JWT signing secret
```

---

## 6. Key Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| External API rate limits (OpenAI, ElevenLabs, Pexels) throttle generation | Medium | High | Implement exponential backoff and per-user quota tracking |
| FFmpeg video assembly fails for edge-case footage clips | Medium | Medium | Validate stock footage download before composition; fallback to text-only video |
| Platform API OAuth tokens expire | High | High | Implement token refresh logic and notify user on auth failure |
| DB tables not created on first run | High | High | Call `init_db()` in service startup event (`@app.on_event("startup")`) |
| Background task progress not visible to user | Medium | Low | Add intermediate DB updates (e.g., `script_generated`, `voice_ready`, `video_ready`) as sub-statuses |
