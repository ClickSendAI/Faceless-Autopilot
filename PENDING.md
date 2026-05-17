# PENDING — Faceless Autopilot AI

Generated: 2026-05-17

## Project Purpose

Faceless Autopilot AI is a multi-service SaaS platform that automates end-to-end creation and distribution of short-form video content without showing a human face. A user provides a topic and niche; the system generates an AI script (OpenAI GPT-4), synthesizes a voiceover (ElevenLabs), assembles a video with stock footage (Pexels + FFmpeg), and distributes it to YouTube, TikTok, and Instagram. A Next.js 15 dashboard provides status monitoring, analytics, and content management.

## Current State

- Backend: 3 FastAPI microservices (ai-content :8561, platform-apis :8562, analytics :8563) with PostgreSQL + Redis. Fourth service (user-management) is directory-only — no app code.
- Frontend: Next.js 15 / React 19 dashboard with Tailwind + shadcn/ui. All major tabs wired to real backend APIs.
- Build status: unverified (no DB/Redis running in this environment; services require external deps).

## Prioritized Pending Items

1. **User Management service is empty** — `services/user-management/app/` contains no Python files. JWT authentication is referenced by all other services but never implemented. No signup, login, or token-issuance endpoints exist. This blocks multi-user use.

2. **Platform upload stubs** — YouTube, TikTok, and Instagram services simulate uploads with `asyncio.sleep(2)` and mock responses. No real OAuth flow, no actual API calls. Content cannot actually be published.

3. **No DB migrations / init_db() call** — `init_db()` is defined but never called at startup in any service. Tables are never created automatically. Services will crash on first DB query unless tables are created manually.

4. **Content status polling uses arbitrary hardcoded delay** — frontend polls every 2 seconds with no timeout or max-retries. Long-running video assembly will leave users polling indefinitely.

5. **`pydantic-settings` missing from all requirements.txt** — all three services import `pydantic_settings.BaseSettings` but the package was not listed. Fixed in this maintenance pass.

6. **Missing `__init__.py` in all service packages** — relative imports break without package markers. Fixed in this maintenance pass.

7. **`services-status.tsx` called `api.checkAllServicesHealth()`** — `checkAllServicesHealth` is a named export, not a method on the `api` object. Fixed in this maintenance pass.

8. **No `.env.example`** — credentials and env-var names are scattered across config.py files; no template for new developers.

9. **No test suite** — test files exist (`test_apis.py`, `test_integration.py`, `simple_test.py`) but require running services. No unit tests that run offline.

10. **docker-compose.yml exposes DB password in plaintext** — password `tjq5uxt3` is hardcoded. Should reference `${POSTGRES_PASSWORD}` env var.
