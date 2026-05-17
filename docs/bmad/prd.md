# Product Requirements Document
## Faceless Autopilot AI

**Version:** 1.1  
**Date:** 2026-05-17  
**Status:** Active  
**Author:** Raphael Bernardo Gonzalez Nunes da Rocha

---

## 1. Introduction

### 1.1 Purpose

This PRD defines the product requirements for Faceless Autopilot AI, a SaaS platform that automates end-to-end production and multi-platform distribution of faceless short-form video content using AI-generated scripts, synthesized voiceovers, and stock footage.

### 1.2 Scope

The platform covers:
- AI script generation from user-supplied topic and niche
- Voice synthesis and video assembly
- Automated upload and scheduling to YouTube, TikTok, and Instagram
- Performance analytics and optimization insights
- Web dashboard for configuration and monitoring

Out of scope: video editing features requiring a human on camera, podcast or long-form content, non-English language support in the initial version.

### 1.3 Definitions

| Term | Definition |
|------|-----------|
| Content | A single generated video asset plus its associated script, voiceover, and platform metadata |
| Niche | A content category (e.g. productivity, personal finance, tech) used to guide AI generation |
| Platform | A social media destination: YouTube Shorts, TikTok, or Instagram Reels |
| Pipeline | The sequential process: script → voice → video → upload |

---

## 2. Product Vision and Goals

### 2.1 Vision

Enable content entrepreneurs to scale faceless short-form video operations to dozens of videos per day across multiple platforms without manual production work.

### 2.2 Goals

| Priority | Goal | Metric |
|----------|------|--------|
| P0 | Generate a complete video from topic input | Latency < 5 min per video |
| P0 | Distribute to at least two platforms automatically | Upload success rate > 95% |
| P1 | Surface actionable analytics per video | Analytics available within 24h of upload |
| P1 | Support scheduling of uploads | Schedule accuracy within 5 minutes |
| P2 | Multi-user SaaS with subscription tiers | Subscription billing functional |

---

## 3. User Personas

### 3.1 Content Entrepreneur (Primary)

Solo creator or small team running multiple niche channels. Goal: maximize passive income from ad revenue and sponsorships with minimal time investment. Values automation, reliability, and scale. Willing to pay $50–200/month for a platform that replaces 20+ hours of manual production.

### 3.2 Agency Operator (Secondary)

Manages content operations for multiple clients. Needs white-label capability, bulk generation, and per-client analytics. Values reliability and reporting. Willing to pay $300–1000/month for an agency plan.

---

## 4. Functional Requirements

### 4.1 Content Generation

| ID | Requirement | Priority |
|----|------------|---------|
| FR-1 | User provides topic, niche, format (short/medium/long), target duration, and target platforms | P0 |
| FR-2 | System generates a GPT-4 script optimized for the selected format and niche | P0 |
| FR-3 | System synthesizes a voiceover from the script using ElevenLabs with configurable voice | P0 |
| FR-4 | System searches Pexels for relevant stock footage clips based on script keywords | P0 |
| FR-5 | System assembles video using FFmpeg: stock footage + voiceover + optional background music | P0 |
| FR-6 | Output video dimensions are optimized per target platform (9:16 for TikTok/Instagram, 16:9 for YouTube) | P0 |
| FR-7 | User can trigger regeneration of any content piece | P1 |
| FR-8 | User can specify voice style (professional, casual, energetic) | P1 |

### 4.2 Platform Distribution

| ID | Requirement | Priority |
|----|------------|---------|
| FR-9 | System uploads completed video to YouTube Shorts via YouTube Data API v3 | P0 |
| FR-10 | System uploads completed video to TikTok via TikTok for Business API | P0 |
| FR-11 | System uploads completed video to Instagram Reels via Instagram Graph API | P0 |
| FR-12 | User can schedule an upload for a future date/time | P1 |
| FR-13 | System stores OAuth credentials per user per platform | P0 |
| FR-14 | System reports upload status per platform (pending, uploading, published, failed) | P0 |

### 4.3 Analytics

| ID | Requirement | Priority |
|----|------------|---------|
| FR-15 | System aggregates views, engagement rate, and revenue per video per platform | P1 |
| FR-16 | Dashboard displays top-performing content ranked by views and engagement | P1 |
| FR-17 | System provides optimization recommendations (best posting times, top niches) | P2 |
| FR-18 | Revenue analytics with monthly and projected figures | P2 |
| FR-19 | Platform data sync triggered on demand or on a schedule | P1 |

### 4.4 User Management

| ID | Requirement | Priority |
|----|------------|---------|
| FR-20 | User registration and login with email/password | P0 |
| FR-21 | JWT-based session management | P0 |
| FR-22 | Subscription tier enforcement (free: 5 videos/month; pro: unlimited) | P1 |
| FR-23 | Per-user API key storage (encrypted at rest) | P0 |

### 4.5 Dashboard

| ID | Requirement | Priority |
|----|------------|---------|
| FR-24 | Overview tab: service health, stats, recent content | P0 |
| FR-25 | Generate tab: multi-step form to configure and launch content generation | P0 |
| FR-26 | Analytics tab: charts for views, engagement, revenue by platform | P1 |
| FR-27 | Upload tab: trigger and monitor platform distribution | P0 |
| FR-28 | Manage tab: list, filter, and delete generated content | P1 |

---

## 5. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-1 | End-to-end content generation latency | < 5 minutes per video |
| NFR-2 | API availability | 99.5% uptime |
| NFR-3 | Platform upload success rate | > 95% |
| NFR-4 | Dashboard initial load time | < 3 seconds |
| NFR-5 | API credentials stored encrypted | AES-256 or equivalent |
| NFR-6 | All service communication over HTTPS in production | Mandatory |
| NFR-7 | Database passwords and secrets via environment variables, never hardcoded | Mandatory |

---

## 6. Constraints and Assumptions

- OpenAI, ElevenLabs, and Pexels API rate limits apply; the system must handle 429 responses with retry and backoff.
- YouTube upload quotas (10,000 units/day default) limit upload throughput.
- TikTok and Instagram APIs require OAuth 2.0 user-level tokens; the platform must implement OAuth flows.
- FFmpeg must be available in the runtime environment (pre-installed in Docker image).
- Initial target market is English-language content.

---

## 7. Open Issues

| Issue | Owner | Status |
|-------|-------|--------|
| User Management service not implemented | Engineering | Open |
| Platform upload services are stubs (no real OAuth) | Engineering | Open |
| No automatic DB migration at service startup | Engineering | Open |
| No .env.example template for new developers | Engineering | Open |
| DB password hardcoded in docker-compose.yml | DevOps | Open |
