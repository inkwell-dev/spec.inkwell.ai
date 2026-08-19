# 08 - DevOps & Infrastructure

## 1. Overview

This document defines the DevOps strategy, infrastructure setup, and deployment workflow for the Inkwell platform.

The system runs as **7 Docker containers** orchestrated by Docker Compose, deployed to a single VPS via GitHub Actions CI/CD.

---

## 2. DevOps Objectives

The DevOps setup must:

- Automate build and deployment processes  
- Ensure consistent environments across development and production  
- Enable fast and safe updates  
- Provide observability and debugging tools
- Keep infrastructure simple enough for a solo engineer  

---

## 3. Infrastructure Architecture

### Production Stack

| Component | Service | Notes |
|-----------|---------|-------|
| Frontend | Next.js 15 (standalone build) | Served by Nginx |
| Backend API | NestJS 11 | REST + SSE endpoints |
| Worker | NestJS (same image, different entrypoint) | BullMQ job processor |
| Database | PostgreSQL 16 + pgvector | Relational + vector + full-text search |
| Cache & Queues | Redis 7 | BullMQ queues + rate limiting + caching |
| Object Storage | MinIO | S3-compatible, article images + avatars |
| Reverse Proxy | Nginx | TLS termination, routing, SSE support |

All services run on a single VPS (Hetzner CX22 or equivalent).

---

## 4. Containerization

### 4.1 Docker Compose Services

```yaml
services:
  nginx       # Reverse proxy + TLS
  web         # Next.js frontend
  api         # NestJS backend
  worker      # BullMQ worker (shares api image)
  db          # PostgreSQL 16 + pgvector
  redis       # Redis 7
  minio       # MinIO object storage
```

### 4.2 Multi-Stage Builds

**Production** images are built from the `Dockerfile` in each app repo, in four
stages:
- **base:** Node 22 Alpine with pnpm enabled, inherited by every later stage
- **deps:** manifests only, then install — so the install layer caches
- **build:** compile TypeScript / build the Next.js standalone output
- **runner:** fresh base, production dependencies plus the build output only

The worker container reuses the backend image with a different entrypoint
(`node dist/src/worker`).

**Development** images are built separately, from `.infra/dockerfiles/` in the
infra repo:
- `web.dev.dockerfile`, `api.dev.dockerfile` — target `development`
- One stage: install dependencies, nothing else. Source is bind-mounted at
  runtime, so hot reload is unaffected and only a dependency change requires a
  rebuild (`make dci-dev-build`).
- They install as the host UID/GID, which is what keeps the `node_modules` named
  volume from being seeded root-owned (Docker seeds an empty named volume from
  the image, ownership included).
- `api` and `worker` share one dev image; they differ only in `command:`.

The app repos' own Dockerfiles have no `development` target, which is why these
are separate files rather than an extra stage.

### 4.3 Docker Networking

- All services communicate via an internal Docker bridge network (`inkwell`)
- Services are referenced by service name (e.g., `db`, `redis`, `minio`)
- In production only Nginx is published publicly (80, 443). The MinIO console is
  published to `127.0.0.1:9001` only — it authenticates with the root credentials
  — and is reached over an SSH tunnel. The S3 API is not published at all; Nginx
  proxies it.
- In development the datastores additionally publish on `127.0.0.1` (`5433`,
  `6379`, `9000`, `9001`) for local clients. The loopback prefix is required:
  omitting it binds every interface, which exposes them to the local network.
- Nginx also declares network **aliases** for the three dev hostnames, so
  `storage.inkwell.ai` resolves inside the network as well as on the host —
  without it the API cannot presign upload URLs.

### 4.4 Health Checks

Every service defines a Docker health check:
- `api` + `worker`: `GET /health` (liveness)
- `db`: `pg_isready`
- `redis`: `redis-cli ping`
- `minio`: `curl -f http://localhost:9000/minio/health/live`
- `web`: `curl -f http://localhost:3000`

---

## 5. CI/CD Pipeline

### 5.1 Version Control

- Source code managed with Git, hosted on GitHub
- Repos: `frontend.inkwell.ai`, `backend.inkwell.ai`, `docker.inkwell.ai`
- `docker.inkwell.ai` vendors the two app repos as **git submodules** under
  `src/`, each pinned to `main`. The dev compose file bind-mounts
  `../../src/<repo>`, so a checkout is self-contained and `git clone
  --recurse-submodules` is the entire setup step.
- A submodule pins a commit, not a branch tip: after pulling new work in a
  submodule, the updated pointer must be committed in the infra repo too. That
  commit is what identifies a deployable revision of the whole system.

### 5.2 Continuous Integration (GitHub Actions)

On each push to `main`:

**Backend CI** (`backend.inkwell.ai/.github/workflows/ci.yml`):
1. Install pnpm dependencies
2. Run ESLint
3. Run TypeScript typecheck (`tsc --noEmit`)
4. Run tests (`pnpm test`)
5. Build Docker image (multi-stage)
6. Push image to GHCR (`ghcr.io/<org>/backend.inkwell.ai`)

**Frontend CI** (`frontend.inkwell.ai/.github/workflows/ci.yml`):
1. Install pnpm dependencies
2. Run ESLint
3. Run TypeScript typecheck
4. Build Next.js (standalone)
5. Push image to GHCR (`ghcr.io/<org>/frontend.inkwell.ai`)

### 5.3 Continuous Deployment

Deploy workflow in `docker.inkwell.ai`:
1. Triggered by `repository_dispatch` from backend/frontend CI on successful push to `main`
2. SSH to VPS
3. Pull latest images from GHCR
4. Run `docker compose up -d` (zero-downtime with health checks)
5. Run database migrations (`drizzle-kit push`)
6. Verify health endpoints respond

### 5.4 Container Registry

- GitHub Container Registry (GHCR) for Docker images
- Images tagged with `latest` and git SHA

---

## 6. Deployment Strategy

### 6.1 Environment Types

| Environment | Purpose | Infrastructure |
|-------------|---------|---------------|
| Development | Local development | `docker compose up` on developer machine |
| Production | Live demo + defense | Single VPS with full Docker Compose stack |

### 6.2 Hosting

- **VPS**: Hetzner CX22 (2 vCPU, 4 GB RAM, 40 GB SSD) or Oracle Cloud free tier
- All 7 services run on a single VPS via Docker Compose
- Optional: lift PostgreSQL to managed (Neon or Render Postgres) if ops overhead becomes a concern

### 6.3 Domain & TLS

- Domain configured via Cloudflare DNS
- TLS via Let's Encrypt with certbot (auto-renewal via cron)
- Nginx handles HTTPS termination

### 6.4 Reverse Proxy (Nginx)

Nginx configuration:
- `/` → frontend (`web:3000`)
- `/api` → backend (`api:3000`)
- `/storage` → object storage (`minio:9000`), prefix stripped
- SSE support: `proxy_buffering off`, `X-Accel-Buffering: no`
- WebSocket-ready headers (for future use)

Development uses a separate `dev.conf` that additionally serves
`frontend.inkwell.ai`, `backend.inkwell.ai` and `storage.inkwell.ai` as named
vhosts, and resolves upstreams at request time so the proxy starts even when the
application containers are stopped.

---

## 7. Storage Strategy

### 7.1 Database

- PostgreSQL 16 with pgvector extension
- Data directory mounted as a Docker volume for persistence
- Migrations managed by Drizzle Kit (`drizzle-kit push`)

### 7.2 File Storage

- MinIO for S3-compatible object storage
- Used for: article images, thumbnails, avatars, magazine logos
- Public read policy on the article images bucket
- Data directory mounted as a Docker volume

### 7.3 Backup Strategy

- Scheduled PostgreSQL backups via `pg_dump` cron (daily, retain 7 days)
- Backup files stored on VPS or synced to remote storage
- MinIO data backed up via volume snapshots

---

## 8. Environment Management

### 8.1 Environment Variables

Managed via `.env` files:
- `.env.example` in `docker.inkwell.ai` (committed, no secrets)
- `.env` on VPS (not committed, contains production secrets)

Variables include:
- Database credentials
- Redis connection
- AI provider API keys (Groq, Gemini — Gemini covers both LLM fallback and embeddings)
- MinIO credentials and public endpoint (`MINIO_ENDPOINT`, `MINIO_USE_SSL`)
- JWT secrets
- Public URLs (`FRONTEND_URL`, `CORS_ORIGINS`, `GOOGLE_CALLBACK_URL`)
- Resend API key (email)

**Build-time vs runtime.** `NEXT_PUBLIC_*` variables are inlined into the browser
bundle by `next build`, so they are passed as Docker **build args** from CI (via
GitHub repository variables), not through the runtime `environment:` block.
Setting them in `.env` has no effect on the shipped JavaScript, and changing one
requires rebuilding the frontend image.

> **Current status (2026-08-10): the repository variables are intentionally
> unset.** The project is still local-only — no domain registered, no VPS
> provisioned — so pointing them at a hostname nobody owns would bake it into
> every published image. With them absent, `next build` receives **empty
> strings**, and the code falls back to its localhost defaults.
>
> That fallback only works because the fallbacks use `||` rather than `??`. An
> absent build arg does not arrive as `undefined`: the Dockerfile promotes each
> ARG to an ENV, so it arrives as the empty string, which `??` keeps. The first
> CI build on `main` failed exactly this way — `new URL('')` threw in the root
> layout and took the whole build down. Any new `NEXT_PUBLIC_*` fallback must use
> `||` for the same reason.
>
> CI still builds and pushes images to GHCR on every `main` push. Those images
> are **not deployable** and are not intended to be; they keep the pipeline
> exercised. Setting the variables is the first step of the deploy block.

Presigned upload URLs are generated against `MINIO_ENDPOINT`, which must be the
**public** hostname: the browser performs the upload, so an internal container
name is unreachable. `MINIO_USE_SSL` controls the scheme, since a presigned
signature covers the `Host` header.

### 8.2 Secrets Management

- Production secrets stored only on the VPS, never in Git
- API keys injected via Docker Compose environment section
- `.env` excluded from all `.gitignore` files

---

## 9. Background Jobs & Queues

### 9.1 Queue System

- Redis + BullMQ for job queue management
- Worker container runs as a separate process (`node dist/src/worker`)
- Worker shares the backend codebase and database connections

### 9.2 Scheduled Jobs

| Job | Schedule | Description |
|-----|----------|-------------|
| `aggregate-article-metrics` | Every 5 min | Raw events → per-article metrics |
| `aggregate-writer-audience` | Every 15 min | → writer audience rollups |
| `aggregate-writer-content` | Every 15 min | → writer content rollups |
| `aggregate-writer-quality` | Every 15 min | → writer quality rollups |
| `check-writer-eligibility` | After aggregation | Auto-flip eligible writers |
| `renew-magazine-subscriptions` | Monthly | Credit grant + renewal record |
| `reset-ai-tokens` | Daily | Reset daily AI token quotas |

### 9.3 Event-Triggered Jobs

| Job | Trigger | Description |
|-----|---------|-------------|
| `embed-article` | Article publish/update | Generate/refresh article chunks via Gemini embeddings |
| `extract-writer-memory` | Article publish | LLM extracts structured memory (tone, style, topics) |
| `send-email` | User action | Transactional email via Resend |

---

## 10. Observability

### 10.1 Health Endpoints (Mandatory)

- `GET /health` — liveness probe: returns 200 if the process is running. Used by Docker healthcheck.
- `GET /ready` — readiness probe: checks PostgreSQL and Redis connectivity. Used for compose dependency ordering and demo confidence.

### 10.2 Error Tracking

- **Sentry** (free tier) integrated in both backend and frontend
- Captures unhandled exceptions, failed BullMQ jobs, and AI provider errors
- Alerts on critical failures

**As built (2026-08-10).** Four runtimes are instrumented: the NestJS API, the
BullMQ worker, the Next.js server, and the browser.

- `src/instrument.ts` in the backend is imported **first** in both `main.ts` and
  `worker.ts`. Sentry patches Node's HTTP and database modules at require time,
  and ES imports are hoisted, so an init call inside `bootstrap()` runs too late
  to instrument anything.
- `SentryGlobalFilter` is registered **before** `DatabaseExceptionFilter` in the
  providers array. Nest gives later-registered global filters higher precedence,
  so this ordering leaves the database filter with first refusal on driver
  errors; reversed, the catch-all would swallow them and every constraint
  violation would become a bare 500 again.
- **Two variables, two mechanisms.** `SENTRY_DSN` is ordinary runtime config for
  the api and worker containers. `NEXT_PUBLIC_SENTRY_DSN` is **build-time** —
  `next build` inlines it into the browser bundle, so it must be a Docker build
  arg fed from a GitHub repository variable, exactly like the other
  `NEXT_PUBLIC_*` values (§8.1). Setting it in the VPS `.env` configures nothing.
- Both are **optional**: with no DSN the SDK initialises and no-ops, so local
  development and CI need no Sentry project.
- `tracesSampleRate` is 0.1 and session replay is off, to stay inside the free
  tier's quota and to avoid recording drafts keystroke by keystroke.
  `sendDefaultPii` is false in every runtime.

### 10.3 Logging

- Structured JSON logging from NestJS (via built-in Logger or Pino)
- Request/response logging on API endpoints
- BullMQ job lifecycle logging (start, success, failure, retry)
- Logs accessible via `docker compose logs -f <service>`

---

## 11. Security Practices

- HTTPS enforced on all endpoints (Nginx + Let's Encrypt)
- JWT-secured API endpoints with short-lived access tokens
- Input validation via Zod schemas
- Content sanitization (XSS prevention on articles and comments)
- Rate limiting via `@nestjs/throttler`
- Signed upload URLs for MinIO (no direct public write access)
- Idempotency keys on financial transactions
- Datastore ports bound to `127.0.0.1`, never `0.0.0.0` — an omitted host
  interface publishes on every network the machine has joined

---

## 12. Scalability Strategy

- Stateless API design (JWT, no server-side sessions)
- Horizontal scaling: add more `api` and `worker` containers behind Nginx
- Database indexing strategy (see `6-database-schema.md` §11)
- Queue-based async processing prevents API blocking

---

## 13. Failure Handling

- BullMQ job retry with exponential backoff (3 attempts)
- AI provider fallback chain (Groq → Gemini for LLM; Gemini for embeddings — single provider, free tier)
- Docker Compose `restart: unless-stopped` on all services
- Health check-based dependency ordering (API waits for DB + Redis)
- Graceful shutdown handling (SIGTERM → drain connections → exit)

---

## 14. Testing Strategy

- CI runs lint + typecheck + unit tests on every push
- Integration tests validate critical API flows (auth → publish → purchase → ledger)
- **Ledger invariant tests** run after every transaction test
- E2E tests with Playwright in Phase 6
- All tests must pass before Docker image push

---

## 15. Demo & Seed Mode

A `DEMO_MODE=true` environment flag enables:
- Lowered eligibility thresholds (e.g., 5 readers + 2 reactions instead of 5K/1K)
- Pre-seeded demo data (writers, articles, analytics events, magazine account)
- Deterministic demo scenario: writer crosses eligibility → publishes to marketplace → magazine previews + purchases

This ensures the data-driven differentiator can be demonstrated live during the defense.

---

## 16. Future Improvements

- Kubernetes for orchestration (if scale demands it)
- Advanced monitoring (Prometheus + Grafana)
- Auto-scaling infrastructure
- Blue/Green deployments
- Managed PostgreSQL (Neon) if self-hosted ops becomes a burden

---

## Summary

The DevOps architecture runs 7 Docker containers on a single VPS, deployed via GitHub Actions CI/CD to GHCR. Nginx handles routing and TLS, Redis + BullMQ manages background jobs, and PostgreSQL serves as the sole data layer. Observability is provided by mandatory health endpoints and Sentry error tracking. A demo/seed mode ensures reliable defense demonstrations.
