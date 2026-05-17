# Faceless Autopilot AI

Automated end-to-end short-form video production and multi-platform distribution. Provide a topic and niche; the system generates a GPT-4 script, synthesizes an ElevenLabs voiceover, assembles a video with Pexels stock footage via FFmpeg, and distributes to YouTube, TikTok, and Instagram. A Next.js 15 dashboard provides real-time status, analytics, and content management.

## Architecture

Four FastAPI microservices backed by PostgreSQL 15 and Redis 7, orchestrated via Docker Compose. A Next.js 15 frontend communicates with the services directly from the browser.

| Service | Port | Purpose |
|---------|------|---------|
| ai-content | 8561 | Script generation, voice synthesis, video assembly |
| platform-apis | 8562 | Social media upload and scheduling |
| analytics | 8563 | Performance tracking and insights |
| user-management | 8004 | Authentication (not yet implemented) |
| frontend | 8560 | Next.js dashboard |

## Prerequisites

- Docker and Docker Compose, OR Python 3.11+ with PostgreSQL 15 and Redis 7 running locally
- FFmpeg installed in PATH (for non-Docker local runs)
- API keys: `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `PEXELS_API_KEY`

## Quick Start (Docker)

```bash
# Copy and fill in credentials
cp .env.example .env

docker compose up -d
```

Frontend: http://localhost:8560  
API docs: http://localhost:8561/docs, http://localhost:8562/docs, http://localhost:8563/docs

## Quick Start (Local Python)

```bash
# Install dependencies for each service
pip install -r services/ai-content/requirements.txt
pip install -r services/platform-apis/requirements.txt
pip install -r services/analytics/requirements.txt

# Set environment variables (see .env.example)
export OPENAI_API_KEY=...
export ELEVENLABS_API_KEY=...
export PEXELS_API_KEY=...
export DATABASE_URL=postgresql://postgres:<password>@localhost:5432/faceless_autopilot_ai
export REDIS_URL=redis://localhost:6379

# Start services (each in its own terminal)
cd services/ai-content && uvicorn app.main:app --host 0.0.0.0 --port 8561
cd services/platform-apis && uvicorn app.main:app --host 0.0.0.0 --port 8562
cd services/analytics && uvicorn app.main:app --host 0.0.0.0 --port 8563

# Start frontend
cd faceless-frontend && pnpm dev
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | GPT-4 script generation |
| `ELEVENLABS_API_KEY` | Yes | Voice synthesis |
| `PEXELS_API_KEY` | Yes | Stock footage search |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REDIS_URL` | Yes | Redis connection string |
| `SECRET_KEY` | Yes | JWT signing secret |

## Content Generation Flow

1. User submits topic, niche, format, and target platforms via the dashboard.
2. `ai-content` service generates a GPT-4 script, produces an ElevenLabs voiceover, and assembles an FFmpeg video with Pexels stock footage.
3. Dashboard polls `/api/content/{id}/status` until `status == "completed"`.
4. User triggers upload via the Upload tab; `platform-apis` service distributes to selected platforms.
5. `analytics` service aggregates performance data from each platform.

## Project Structure

```
faceless-frontend/     Next.js 15 dashboard
services/
  ai-content/          Script + voice + video pipeline (FastAPI, port 8561)
  platform-apis/       YouTube / TikTok / Instagram upload (FastAPI, port 8562)
  analytics/           Performance analytics (FastAPI, port 8563)
  user-management/     Auth service (not yet implemented)
  shared/              Shared utilities (currently empty)
docs/                  PRD, architecture stories
docker-compose.yml     Full-stack orchestration
```

## Known Limitations

- Platform upload services (YouTube, TikTok, Instagram) simulate uploads. Real OAuth and API integration is pending.
- User Management service has no implementation. All endpoints run without authentication.
- Database tables must exist before first run; no automatic migration is triggered at startup.

See `PENDING.md` for the full prioritized backlog.
