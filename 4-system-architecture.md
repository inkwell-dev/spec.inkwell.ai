# 04 - System Architecture

## 1. Overview

This document describes the overall system architecture of the AI-powered writing platform.

The system is designed to be:
- Modular  
- Scalable  
- Maintainable  
- AI-ready  

It follows a **modular monolith** architecture: all business logic — including AI orchestration — lives inside the NestJS backend, structured as independent modules communicating through well-defined interfaces. AI calls to external providers (Groq, Gemini, OpenAI) are made directly from the backend via the Vercel AI SDK — no separate AI service exists.

---

## 2. High-Level Architecture

The system is composed of the following main components:

- Frontend Application (Next.js 15)
- Backend API + AI Gateway (NestJS 11)
- Background Worker (shares backend image, runs BullMQ jobs)
- Database Layer (PostgreSQL 16 + pgvector)
- Caching & Queue System (Redis + BullMQ)
- Object Storage (MinIO, S3-compatible)
- Reverse Proxy (Nginx)
- External AI APIs (Groq, Gemini, OpenAI)

---

## 3. Architecture Diagram

```
[ Client (Browser) ]
        |
        v
[ Nginx (Reverse Proxy + TLS) ]
        |
   ---------------------
   |                   |
   v                   v
[ Frontend          [ Backend API
  (Next.js 15) ]      (NestJS 11) ]
                       |
          -----------------------------------------
          |          |           |          |      |
          v          v           v          v      v
       [Auth]   [Core API]  [AI Gateway] [SSE]  [REST]
                                |
                    --------------------------
                    |          |             |
                    v          v             v
                 [Groq]    [Gemini]     [OpenAI]
                 (LLM +    (LLM         (Embeddings)
                  Whisper)  fallback)

[ Worker (BullMQ) ] ← shares backend image
        |
        v
   -----------------------------------------
   |              |              |          |
   v              v              v          v
[Embed        [Aggregate     [Renew      [Send
 Articles]     Metrics]       Subs]       Email]

        ------- Data Layer -------
        |            |           |
        v            v           v
[ PostgreSQL ]   [ Redis ]   [ MinIO ]
  (relational      (cache      (images
   + pgvector      + queues)    + media)
   + tsvector)
```

---

## 4. Frontend Layer

### Responsibilities

- User interface rendering  
- Rich text editor integration (TipTap)
- AI interaction (chat panel, inline editing popup)
- Analytics event capture (view, scroll, time-on-page)
- State management (Zustand + TanStack Query)
- API communication (auto-generated OpenAPI client)

---

### Key Modules

- Authentication UI  
- Article Editor (TipTap)
- AI Assistant Panel (chat + inline editing)
- Analytics Dashboard (writer-facing + magazine-facing)
- Feed & Article Viewer  
- Marketplace UI (discover, preview, purchase, library)

---

### Communication

- REST API calls to backend  
- SSE for AI streaming responses and live notifications

---

## 5. Backend Layer (Core API + AI Gateway)

### Responsibilities

- Business logic  
- Authentication & authorization  
- Article management  
- Social features (likes, comments, follows)  
- Analytics event ingestion and aggregation orchestration
- **AI orchestration** — prompt construction, context injection, structured memory, RAG retrieval, provider calls via Vercel AI SDK
- Marketplace transactions (atomic ledger operations)
- Magazine subscription management

---

### Modular Structure

- Auth Module
- Users Module (personal + magazine profiles)
- Articles Module (incl. tags, slugs, soft deletes)
- Comments Module
- Likes Module
- Follow Module
- Reposts Module
- **AI Module** — provider abstraction (Vercel AI SDK), prompt builder, token quota
  - ChatService — contextual chat with RAG retrieval
  - InlineEditService — reformulate/shorten/expand/simplify/improve
  - VoiceService — Groq Whisper transcription → structured article generation
  - RagService — chunk retrieval via pgvector cosine similarity
  - EmbeddingService — OpenAI `text-embedding-3-small` (1536 dimensions)
  - MemoryService — structured writer memory extraction and injection
  - PortfolioInsightsService — magazine-facing writer evaluation via RAG
- **Marketplace Module** — writer eligibility gating, marketplace article browsing, preview unlock + full purchase flow
- **Subscriptions Module** — magazine subscription activation, renewal, credit management
- **Transactions Module** — atomic financial ledger (credit/debit, idempotency, row locking)
- Analytics Module (event ingestion, writer-facing + magazine-facing aggregation)
- Storage Module (MinIO uploads)
- Notifications Module (SSE delivery)
- Moderation / Reports Module  

---

### API Design

- RESTful API  
- JSON-based communication  
- JWT-secured endpoints  
- SSE endpoints for AI streaming and notifications

---

## 6. AI Integration Layer

### Architecture Decision

AI orchestration is consolidated inside the NestJS backend rather than separated into a dedicated Python service. This decision was made because:

- All AI functionality consists of API calls to external providers (Groq, Gemini, OpenAI) — no custom ML training or local model hosting
- The Vercel AI SDK provides a unified TypeScript interface for all providers with built-in SSE streaming
- A single codebase eliminates inter-service HTTP hops, reduces deployment complexity, and keeps the type system end-to-end (Zod-validated structured outputs flow directly into Drizzle)
- For a solo engineer, one language and one deploy unit is significantly easier to maintain and debug

A separate AI service should only be introduced if: local models are hosted, fine-tuning is added, or heavy NLP pipelines are required.

---

### Key Pipelines

Text Processing:
- User action → Backend enriches with article context + structured memory + RAG chunks → Prompt built → Vercel AI SDK `streamText` → SSE response to frontend

Voice Processing:
- Audio blob → Groq Whisper transcription → LLM structures transcript → TipTap JSON article draft

RAG Retrieval:
- Query embedded via OpenAI → pgvector cosine similarity search (`<=>`) → top-K chunks returned → injected into prompt context

Portfolio Insights:
- Magazine requests evaluation → representative chunks retrieved from writer's corpus → structured prompt → LLM generates Zod-validated report → cached in `portfolio_insights` for 24h

---

### Provider Abstraction

LLM provider switching is handled by the Vercel AI SDK — changing from Groq to Gemini requires a one-line config change, not a code rewrite. The `EmbeddingService` uses OpenAI `text-embedding-3-small` directly (1536 dimensions, $0.02/1M tokens) — no provider abstraction needed for embeddings since there is a single stable paid provider.

---

## 7. Data Layer

### Primary Database (PostgreSQL 16 + pgvector)

A single PostgreSQL instance serves as the sole data, search, and vector layer:

- **Relational data** — users, articles, comments, likes, follows, transactions, subscriptions
- **Full-text search** — `tsvector` + GIN index on article title/content/excerpt
- **Vector storage** — `pgvector` extension with HNSW index on `article_chunks.embedding` for RAG retrieval
- **Hybrid search** — combined full-text + semantic search using Reciprocal Rank Fusion (RRF) to merge lexical and vector results

No additional search engine (Elasticsearch) or vector database (Pinecone, Weaviate) is needed at this scale.

---

### Data Consistency

- Strong consistency for core entities and financial transactions (row-level locking on balance operations)
- Eventual consistency for analytics (batch aggregation every 5–15 minutes)

---

## 8. Caching & Queue Layer (Redis + BullMQ)

### Purpose

- Improve performance  
- Handle asynchronous processing  
- Manage background jobs  

---

### Use Cases

- Rate limiting (`@nestjs/throttler`)
- Caching frequently accessed data (portfolio insights, article metrics)
- Analytics aggregation (article metrics, writer rollups)
- Writer eligibility computation (runs after each analytics batch)
- Magazine subscription renewal (monthly cron — grant credits + update subscription state)
- Article embedding on publish (OpenAI API calls)
- Email dispatch (transactional emails via Resend)

---

### Scheduled Jobs

| Job | Frequency | Description |
|-----|-----------|-------------|
| `aggregate-article-metrics` | Every 5 min | Raw events → `article_metrics` |
| `aggregate-writer-audience` | Every 15 min | → `writer_audience_metrics` |
| `aggregate-writer-content` | Every 15 min | → `writer_content_metrics` |
| `aggregate-writer-quality` | Every 15 min | → `writer_quality_metrics` |
| `check-writer-eligibility` | After each aggregation | Flip eligible writers |
| `renew-magazine-subscriptions` | Monthly | Credit grant + renewal row |
| `reset-ai-tokens` | Daily | Reset daily AI token quotas |
| `embed-article` | On publish/update | Generate/refresh article chunks |
| `extract-writer-memory` | On publish | LLM extracts structured memory |
| `send-email` | On trigger | Transactional email via Resend |

---

## 9. Analytics Architecture

### Event Collection

Frontend captures and batches events (bursts of 10 or every 5 seconds):
- Page view (with country detection from headers)
- Scroll tracking (per paragraph via `IntersectionObserver`)
- Time spent (`visibilitychange` + `beforeunload` + `sendBeacon`)

---

### Processing Flow

Client Event → Batched POST `/analytics/events` → `analytics_events` table (raw) → BullMQ aggregation workers → Metrics tables → Dashboards

---

### Aggregation Strategy

- Per-article aggregation every 5 minutes
- Per-writer rollups every 15 minutes
- Writer eligibility check after each aggregation run
- Portfolio Insights on-demand with 24-hour cache

---

## 10. Security Architecture

### Authentication

- JWT-based authentication  
- Access token (15 min) + refresh token (7 days)

---

### Authorization

- Role-based access control (RBAC)
- Guards: `JwtAuthGuard`, `RolesGuard`, `PlansGuard`, `AccountTypeGuard`
- Subscription guard for magazine marketplace endpoints

---

### Data Protection

- Input validation (Zod schemas)
- Sanitization of user-generated content (XSS prevention)
- Secure file uploads (signed MinIO URLs)
- Idempotency keys on financial transactions

---

## 11. Media Storage

### Image Handling

- Uploaded by users (article thumbnails, inline images, avatars, magazine logos)
- Stored in MinIO (S3-compatible object storage)
- Upload via signed POST URLs to avoid routing media through the backend

---

### Access

- Public read URLs for rendering  
- Controlled upload endpoints (authenticated)

---

## 12. Notification System

### Flow

Event Trigger → Backend → Notification Created → Stored → Delivered via SSE

---

### Types

- Follow notifications  
- Likes  
- Comments / replies
- Article previewed by magazine (writer-facing)
- Article purchased by magazine (writer-facing)
- Earnings credited (writer-facing)
- Subscription renewed (magazine-facing)

---

## 13. Observability

### Health Checks

- `GET /health` — liveness probe (returns 200 if the process is running). Used by Docker Compose healthcheck and Nginx upstream checks.
- `GET /ready` — readiness probe (checks PostgreSQL + Redis connectivity). Used for dependency ordering in compose and for demo confidence.

### Error Tracking

- Sentry (free tier) for error tracking and alerting in both backend and frontend.

### Logging

- Structured JSON logging from NestJS
- Request/response logging on API endpoints
- BullMQ job success/failure logging

---

## 14. Deployment Architecture

### Services (Docker Compose)

7 containers in a single `docker-compose.yml`:

| Service | Image | Port |
|---------|-------|------|
| `nginx` | nginx:alpine | 80, 443 |
| `web` | frontend (multi-stage build) | 3000 |
| `api` | backend (multi-stage build) | 3001 |
| `worker` | backend (same image, `node dist/worker`) | — |
| `db` | postgres:16 + pgvector | 5432 |
| `redis` | redis:7-alpine | 6379 |
| `minio` | minio/minio | 9000 |

---

### Containerization

- Multi-stage Docker builds for frontend and backend (deps → build → runner)
- Worker shares backend image with different entrypoint
- All services communicate over an internal Docker network
- Health checks defined for all services

---

### Reverse Proxy

- Nginx routes `/` to frontend, `/api` to backend
- SSE support configured (proxy buffering disabled)
- HTTPS termination via Let's Encrypt (certbot)

---

## 15. Scalability Considerations

- Stateless API design (JWT, no server-side sessions)
- Queue-based async processing for AI calls and analytics aggregation
- Database indexing strategy (see `6-database-schema.md` §11)
- Horizontal scaling: add more API/worker containers behind Nginx

---

## 16. Failure Handling

- Retry mechanism for AI API calls (Vercel AI SDK built-in retry)
- Provider fallback chain: Groq → Gemini for LLM; OpenAI for embeddings (single provider, paid tier)
- Graceful degradation if AI providers are unavailable (non-AI features continue working)
- BullMQ job retry with exponential backoff
- Health check endpoints for container orchestration

---

## 17. Testing Strategy (High-Level)

- Unit tests for backend modules (NestJS testing utilities)
- **Ledger invariant tests** — assert `earnings_balance == sum(writer_payout)` and `credit_balance == grants + topups − debits` after every transaction test
- Integration tests for critical API flows (auth → publish → purchase → verify ledger)
- E2E tests with Playwright for frontend flows (Phase 6)

---

## Summary

The system architecture consolidates all logic — including AI orchestration — into a single NestJS backend with a dedicated worker process for background jobs. PostgreSQL serves as the sole data, search, and vector layer. This keeps the deployment footprint minimal (7 Docker containers) while supporting the full feature set: AI-assisted writing, RAG-powered personalization, decision-support analytics, and a transactional marketplace with a locked financial ledger.
