# Changelog

## [Unreleased] — 2026-05-17

### Fixed

- **`pydantic-settings` missing from all three service requirements.txt** — `ai-content`, `platform-apis`, and `analytics` all import `pydantic_settings.BaseSettings` but the `pydantic-settings==2.1.0` package was absent from their dependency lists, causing import errors on fresh installs.
- **Missing `__init__.py` in all service packages** — `app/`, `app/services/`, and `app/core/` directories in all three services had no `__init__.py`, breaking Python's relative import resolution (`from .schemas import ...`, `from ..core.config import settings`, etc.).
- **`services-status.tsx` called `api.checkAllServicesHealth()`** — `checkAllServicesHealth` is a named export from `lib/api.ts`, not a property on the `api` object. The component now imports and calls it correctly.
- **`process_content_generation` never persisted results to DB** — The background task ran the full pipeline (OpenAI → ElevenLabs → FFmpeg) but had only stub comments where DB updates belonged. It now updates `Content.script`, `Content.voice_file_url`, `Content.video_file_url`, and `Content.status` on completion, and sets `status=failed` on error.
- **`process_content_generation` leaked DB session into background task** — FastAPI's `Depends(get_db)` sessions must not be passed to background tasks (the request context is closed by the time the task runs). The task now opens and closes its own `SessionLocal()` session.
- **`process_content_regeneration` was an empty stub** — The regeneration background task now reads the existing content record, re-runs the full generation pipeline, and persists updated results to DB.
- **`get_content_status` returned hardcoded `progress=75` always** — The endpoint now queries the `Content` table by ID, returns 404 if not found, and derives progress from the actual `status` field (`processing=50`, `completed=100`, `failed=0`).
- **Background task signature mismatch** — `process_content_generation` and `process_content_regeneration` were registered with `db` as a positional argument but the corrected versions manage their own sessions; call sites updated accordingly.

### Added

- `README.md` — Full project overview, quick-start instructions (Docker and local Python), environment variable table, content generation flow, and project structure.
- `ARCHITECTURE.md` — Service-by-service breakdown, module inventory, data flow diagrams, database schema, and frontend component inventory.
- `PENDING.md` — Prioritized backlog of 10 pending work items derived from the actual codebase.
- `CHANGELOG.md` — This file.
- `docs/bmad/prd.md` — BMAD v6 PRD document authored from the real codebase.
- `docs/bmad/architecture.md` — BMAD v6 architecture document authored from the real codebase.
