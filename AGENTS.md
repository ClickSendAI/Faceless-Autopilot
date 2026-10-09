# Base44 Dev Environment — Faceless Autopilot AI

## Architecture

Microservices stack: Next.js frontend + 3 FastAPI backend services + PostgreSQL + Redis.

- **Frontend** (port 3000): Next.js 15, pnpm, `faceless-frontend/`
- **AI Content Service** (port 8561): FastAPI, `services/ai-content/`
- **Platform APIs Service** (port 8562): FastAPI, `services/platform-apis/`
- **Analytics Service** (port 8563): FastAPI, `services/analytics/`
- **PostgreSQL** (port 5432): database `faceless_autopilot_ai`
- **Redis** (port 6379): cache

## Running

```bash
docker compose -f docker-compose.base44.yml up -d --build
```

The frontend is the user-facing entry point on port 3000. Backend services are
proxied through the Next.js dev server via rewrites (see `next.config.mjs`,
gated on `BASE44_PREVIEW_MODE`). The frontend API client (`lib/api.ts`) uses
env-configurable base URLs with `localhost` defaults for local dev.

## Key Setup Notes

- **Missing `pydantic-settings`**: The service `config.py` files import
  `from pydantic_settings import BaseSettings` but the original `requirements.txt`
  files did not list `pydantic-settings`. It has been added to all three services.
- **No `user-management` service**: The original `docker-compose.yml` references a
  `user-management` service, but that directory does not exist in the repo. It is
  omitted from the Base44 compose.
- **No `__init__.py` files**: The service packages rely on Python 3 namespace
  packages (no `__init__.py`). This works with `uvicorn app.main:app`.
- **API keys are optional at boot**: The services start and respond to health
  checks without `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, or `PEXELS_API_KEY`.
  Content generation features require real keys, delivered via `/run/base44/app.env`.
- **FFmpeg**: The ai-content service needs FFmpeg for video assembly, but it is
  not installed in the dev container. Health checks and non-video endpoints work
  without it. Video generation would require adding FFmpeg to the image.

## Verifying

```bash
# Check all services are up
docker compose -f docker-compose.base44.yml ps

# Health checks
curl http://localhost:8561/health
curl http://localhost:8562/health
curl http://localhost:8563/health

# Frontend
curl http://localhost:3000
```

## Secrets

External API keys (optional, for AI content generation only):
- `OPENAI_API_KEY` — https://platform.openai.com/api-keys
- `ELEVENLABS_API_KEY` — https://elevenlabs.io/app/settings/api-keys
- `PEXELS_API_KEY` — https://www.pexels.com/api/
