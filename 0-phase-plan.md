# 🗺️ Inkwell.ai — Phase Plan

> **Target defense:** September 2026 (14-week timeline from May 21, 2026)
> **Stack:** Next.js 15 · NestJS 11 · PostgreSQL + pgvector · Redis · MinIO · Groq · Gemini · Drizzle ORM
> **Repos:** `frontend.inkwell.ai` · `backend.inkwell.ai` · `docker.inkwell.ai` · `mobile.inkwell.ai` (deferred)

---

## Phase 0 — Foundation
> Week 1 · May 22–28

- [x] Rename `docker.inkewell.ai` → `docker.inkwell.ai` (fix typo)
- [x] Node.js upgraded to v22.22.3 via nvm
- [x] pnpm v11 configured across all repos
- [x] `backend.inkwell.ai` — NestJS 11 scaffold with strict TypeScript
- [x] `frontend.inkwell.ai` — Next.js 15 (App Router) + Tailwind CSS + shadcn/ui scaffold
- [x] `docker.inkwell.ai` — `docker-compose.yml` with all 7 services (nginx, web, api, worker, db, redis, minio)
- [x] `docker.inkwell.ai` — `.env.example` with all required environment variables
- [x] `docker.inkwell.ai` — Nginx reverse proxy config with SSE support
- [x] `backend.inkwell.ai` — Dockerfile (multi-stage: deps → build → runner)
- [x] `frontend.inkwell.ai` — Dockerfile (multi-stage, standalone output, non-root user)
- [x] `backend.inkwell.ai` — GitHub Actions CI (lint + typecheck + test + push image to GHCR)
- [x] `frontend.inkwell.ai` — GitHub Actions CI (lint + typecheck + build + push image to GHCR)
- [x] `.nvmrc` added to backend and frontend repos
- [ ] Push all repos to GitHub remotes
- [ ] Verify `docker compose up --build` brings up all 7 containers locally
- [ ] Confirm Swagger UI accessible at `http://localhost/api/docs`

---

## Phase 1 — Auth + Core CRUD
> Weeks 2–3 · May 29–Jun 11

### Backend
- [ ] Install Drizzle ORM + `drizzle-kit` + `pg` driver
- [ ] Define full Drizzle schema (`src/db/schema.ts`):
  - [ ] `users` — id, email, username, name, bio, avatar_url, role (reader/writer/admin), plan (free/premium), password_hash, provider, ai_tokens_remaining, deleted_at
  - [ ] `articles` — id, author_id, title, slug (unique), excerpt, content (TipTap JSON), thumbnail_url, status (draft/published), visibility (free/premium), read_time, tags, deleted_at, published_at
  - [ ] `tags` + `article_tags` join table
  - [ ] `comments` — threaded (parent_id self-ref), deleted_at
  - [ ] `likes` — unique(user_id, article_id)
  - [ ] `follows` — unique(follower_id, following_id)
  - [ ] `reposts` — unique(user_id, article_id)
  - [ ] `notifications` — type enum, data JSON, is_read
  - [ ] `reports` — target_type, target_id, status
  - [ ] `ai_interactions` — action_type, tokens_used
  - [ ] `user_ai_memory` — tone, style_examples, vocabulary JSON
  - [ ] `article_chunks` — content, embedding vector(1024), chunk_index (for RAG)
  - [ ] `analytics_events` — event_type, metadata JSON
  - [ ] `article_metrics` — aggregated views, read_time, engagement_rate
- [ ] Run first migration with `drizzle-kit push`
- [ ] `@nestjs/swagger` configured — Swagger UI at `/docs`
- [ ] `@nestjs/config` — environment validation with Zod or `joi`
- [ ] Auth module:
  - [ ] Email/password registration + login
  - [ ] Google OAuth (Passport.js)
  - [ ] JWT access token (15 min) + refresh token (7 days)
  - [ ] `JwtAuthGuard` + `RolesGuard` + `PlansGuard`
- [ ] Users module — GET /users/:username, PATCH /users/me, GET /users/me
- [ ] Articles module:
  - [ ] POST /articles (create draft)
  - [ ] PATCH /articles/:id (update)
  - [ ] POST /articles/:id/publish
  - [ ] DELETE /articles/:id (soft delete)
  - [ ] GET /articles (feed — paginated, filtered by visibility/plan)
  - [ ] GET /articles/:slug (single article)
  - [ ] Slug auto-generation from title (slugify + unique suffix)
- [ ] Tags module — GET /tags (list), POST /tags
- [ ] `@nestjs/throttler` — basic rate limiting on all endpoints

### Frontend
- [ ] Install shadcn/ui + configure components
- [ ] Install TanStack Query v5 + Zustand
- [ ] Install Auth.js (NextAuth.js) — email + Google OAuth
- [ ] Layout: navbar, footer, responsive shell
- [ ] Feed page (`/`) — article cards, pagination, tag filter
- [ ] Article reader page (`/articles/[slug]`) — full article, premium gate
- [ ] Sign-up / Login pages
- [ ] Profile page (`/u/[username]`) — articles, follow button, stats
- [ ] Editor page (`/editor/[id]`) — basic textarea (TipTap in Phase 2)
- [ ] OpenAPI client codegen configured (`openapi-typescript` or `orval`)
- [ ] Protected route wrapper for auth-required pages

### Exit criteria
- [ ] Full sign-up → create article → publish → view on feed cycle works end-to-end
- [ ] Premium article is gated for free users
- [ ] OpenAPI spec is accessible and frontend client auto-generates from it

---

## Phase 2 — Editor + Basic AI
> Weeks 4–5 · Jun 12–25

### Editor
- [ ] Install TipTap + extensions (StarterKit, Placeholder, Image, CodeBlock, Typography)
- [ ] Replace textarea with TipTap editor in `/editor/[id]`
- [ ] Image upload — paste/drag into editor → upload to MinIO → embed URL
- [ ] Thumbnail upload for article cover
- [ ] Auto-save draft on change (debounced PATCH, 1.5s)
- [ ] Word count + estimated read-time display

### AI Gateway (Backend)
- [ ] Install Vercel AI SDK (`ai`, `@ai-sdk/groq`, `@ai-sdk/google`)
- [ ] `AiModule` — provider abstraction, prompt builder
- [ ] Token quota middleware — check `ai_tokens_remaining` before each AI request, decrement after
- [ ] Daily token reset cron job (BullMQ scheduled job)
- [ ] Log every AI interaction to `ai_interactions` table
- [ ] POST /ai/chat — contextual chat assistant (article context injected)
- [ ] POST /ai/inline — inline editing actions (reformulate/shorten/expand/simplify/improve)
- [ ] SSE streaming for all AI endpoints (Vercel AI SDK `streamText`)

### AI Features (Frontend)
- [ ] AI chat panel (slide-out sidebar in editor)
  - [ ] Chat history UI
  - [ ] "Insert into article" button on AI responses
  - [ ] Token usage indicator
- [ ] Inline editing popup — appears on text selection
  - [ ] 5 action buttons (Reformulate / Shorten / Expand / Simplify / Improve)
  - [ ] Streaming result preview
  - [ ] Replace / Insert below / Cancel actions
- [ ] Token quota warning + "upgrade" prompt when tokens depleted

### Exit criteria
- [ ] Writer can edit with TipTap and upload images
- [ ] AI chat streams tokens in real-time (SSE visible in UI)
- [ ] Inline popup works on text selection with all 5 actions
- [ ] Token counter decrements correctly per AI action

---

## Phase 3 — Social + Analytics
> Weeks 6–7 · Jun 26–Jul 9

### Social (Backend)
- [ ] Likes module — POST /articles/:id/like, DELETE /articles/:id/like
- [ ] Comments module — POST/GET/DELETE for threaded comments
- [ ] Follows module — POST /users/:username/follow, DELETE unfollow
- [ ] Reposts module — POST /articles/:id/repost
- [ ] Notifications module:
  - [ ] Create notification on like / comment / follow events
  - [ ] GET /notifications (paginated list)
  - [ ] PATCH /notifications/:id/read
  - [ ] SSE endpoint GET /notifications/stream — live delivery

### Analytics (Backend)
- [ ] POST /analytics/events — batch event ingestion endpoint
- [ ] BullMQ worker: aggregate raw events → `article_metrics` (runs every 15 min)
- [ ] GET /articles/:id/analytics — writer-only stats endpoint

### Social (Frontend)
- [ ] Like button with optimistic UI
- [ ] Comment section under articles — threaded replies
- [ ] Follow button on profile pages
- [ ] Repost button
- [ ] Notification bell — live SSE connection, unread count badge
- [ ] Notification dropdown list

### Analytics (Frontend)
- [ ] Analytics event capture on article pages:
  - [ ] View event on load
  - [ ] Scroll depth via `IntersectionObserver` (per paragraph)
  - [ ] Time-on-page via `visibilitychange` + `beforeunload`
- [ ] Writer analytics dashboard (`/dashboard`):
  - [ ] Views per article (chart)
  - [ ] Avg read time
  - [ ] Scroll depth heatmap (bar chart per paragraph)
  - [ ] Top performing articles

### Exit criteria
- [ ] Like/comment/follow/repost all work with correct notifications
- [ ] Live notification arrives via SSE without page refresh
- [ ] Writer dashboard shows real engagement data after a test read

---

## Phase 4 — RAG (Headline Differentiator)
> Weeks 8–9 · Jul 10–23

### RAG Pipeline (Backend)
- [ ] Install Cohere SDK (embeddings) + pgvector Drizzle helpers
- [ ] Article chunking on publish:
  - [ ] Split TipTap JSON into paragraph-level chunks
  - [ ] Each chunk embedded via Cohere `embed-multilingual-v3.0`
  - [ ] Stored in `article_chunks` with `embedding vector(1024)`
  - [ ] BullMQ job: `embed-article` triggered on publish/update
- [ ] Retrieval service:
  - [ ] `findSimilarChunks(userId, queryEmbedding, topK)` — cosine similarity with pgvector `<=>` operator
  - [ ] Filter by `author_id = userId` (RAG over writer's own corpus only)
- [ ] Prompt template update — inject top-K retrieved chunks as context
- [ ] POST /ai/chat — enhanced with RAG retrieval
- [ ] GET /ai/retrieval-debug — returns chunks used in last request (for demo/transparency)
- [ ] Postgres full-text search — `tsvector` on `articles.title + content`
- [ ] GET /search?q= — full-text + semantic hybrid search endpoint

### Frontend
- [ ] Search bar in navbar → search results page
- [ ] "Sources used" expandable section below AI responses (shows which past articles were referenced)
- [ ] RAG demo notice: "AI trained on your X published articles"

### Exit criteria
- [ ] Publish 5+ articles with distinct topics/vocabulary
- [ ] AI chat generates a new article that demonstrably uses retrieved vocabulary and style
- [ ] `/ai/retrieval-debug` shows correct chunk IDs pulled from the user's articles
- [ ] Search returns relevant results for both keyword and semantic queries

---

## Phase 5 — Voice + Premium + Moderation
> Weeks 10–11 · Jul 24–Aug 6

### Voice-to-Article
- [ ] Backend POST /ai/voice — receives audio blob, transcribes via Groq Whisper-large-v3-turbo, generates structured article draft
- [ ] Frontend voice recorder component in editor toolbar:
  - [ ] MediaRecorder API — start/stop/preview
  - [ ] Upload audio → poll for result → insert draft into TipTap editor
  - [ ] Loading state while processing

### Premium + Subscription
- [ ] Backend subscription simulation:
  - [ ] POST /subscriptions/upgrade — sets `user.plan = premium`
  - [ ] POST /subscriptions/downgrade
  - [ ] Token top-up endpoint (simulated purchase)
- [ ] Frontend upgrade flow:
  - [ ] Upgrade modal / page with plan comparison
  - [ ] Payment mock (no real Stripe in MVP — just a button that confirms)
  - [ ] Premium badge on profile

### Moderation
- [ ] Reports module — POST /reports (article or user), admin GET /reports
- [ ] Admin panel (`/admin`):
  - [ ] Reports queue with article preview
  - [ ] Actions: dismiss / delete article / ban user (soft delete)
  - [ ] User management table with role/plan editing
- [ ] Content moderation on article publish: OpenAI Moderation API (free) — auto-flag violating content

### Email (Transactional)
- [ ] Install Resend SDK
- [ ] Email templates: welcome, password reset, new follower notification
- [ ] BullMQ worker: `send-email` job

### AI Eval Harness (optional — do if time permits)
- [ ] Define 10 test cases per action type (reformulate/expand/shorten/simplify/improve)
- [ ] `pnpm ai:eval` script — runs test cases against current prompts, scores with LLM-as-judge
- [ ] Output: pass/fail report per action type

### Mobile Go/No-Go Decision
- [ ] Evaluate: is web fully stable and production-ready?
  - [ ] YES → start read-only Expo app (feed + article reader + likes)
  - [ ] NO → mark `mobile.inkwell.ai` as post-MVP in spec, move to Phase 6

### Exit criteria
- [ ] Record voice → structured article appears in TipTap editor
- [ ] Upgrade flow changes user plan and unlocks premium articles + AI features
- [ ] Reported content appears in admin queue
- [ ] Transactional emails send correctly (test with Resend dev mode)

---

## Phase 6 — Polish, Deploy & Defense Prep
> Weeks 12–14 · Aug 7–end of August

### Quality
- [ ] Playwright E2E tests — cover all critical flows:
  - [ ] Sign up → create → publish → read cycle
  - [ ] AI chat interaction
  - [ ] Inline editing
  - [ ] Like / comment / follow
  - [ ] Premium gate
- [ ] Lighthouse audit — target score >90 on article pages (Performance, Accessibility, SEO)
- [ ] Accessibility pass — `axe-core` scan, fix critical issues
- [ ] Fix all TypeScript strict errors
- [ ] Input sanitization audit (XSS on article content, comments)

### SEO
- [ ] Dynamic OG images for articles (Next.js `ImageResponse`)
- [ ] Sitemap (`/sitemap.xml`) — auto-generated from published articles
- [ ] Structured data (JSON-LD `Article` schema on article pages)
- [ ] `<meta>` description from article excerpt

### Production Deploy
- [ ] Provision VPS (Hetzner CX22 or Oracle Cloud free tier)
- [ ] Configure domain + Cloudflare DNS
- [ ] TLS via Let's Encrypt (Nginx + certbot or Caddy)
- [ ] GitHub Actions deploy workflow in `docker.inkwell.ai`:
  - [ ] Trigger on push to `main` in backend/frontend repos (via `repository_dispatch`)
  - [ ] SSH to VPS → pull new images → `docker compose up -d`
- [ ] Production `.env` configured on VPS (secrets, AI API keys)
- [ ] Database migration runs automatically on deploy
- [ ] MinIO bucket created + public read policy for article images
- [ ] Verify full stack running at production URL

### Defense Preparation
- [ ] `docs/ARCHITECTURE.md` — full system architecture diagram + explanation
- [ ] `docs/RAG.md` — how the RAG pipeline works (chunking → embedding → retrieval → prompt injection)
- [ ] `docs/AI-DESIGN.md` — update original spec with actual implementation decisions
- [ ] `spec.inkwell.ai` — update all specs to reflect what was actually built
- [ ] Demo script — 10-minute walkthrough covering all key features
- [ ] Slide deck (15–20 slides):
  - [ ] Problem + solution
  - [ ] Architecture diagram
  - [ ] RAG pipeline deep-dive
  - [ ] Live demo screenshots/video
  - [ ] Tech stack choices + rationale
  - [ ] Metrics / results
- [ ] Record backup demo video (in case live demo fails)
- [ ] Defense rehearsal × 2

---

## Spec Fixes Backlog
> Complete these before coding the relevant feature

- [ ] Fix subscription model in spec — `role` + `plan` (not mutex enum)
- [ ] Add `slug` field to articles spec
- [ ] Add `username` field to users spec
- [ ] Commit to TipTap JSON as article content format
- [ ] Add tags/categories to MVP feature list
- [ ] Add search (full-text + semantic) to MVP feature list
- [ ] Add soft deletes to database schema spec
- [ ] Specify LLM providers (Groq primary, Gemini fallback)
- [ ] Specify voice provider (Groq Whisper-large-v3-turbo)
- [ ] Specify embeddings provider (Cohere embed-multilingual-v3.0)
- [ ] Structured AI memory schema (not JSON blob)
- [ ] Add SSE real-time strategy doc
- [ ] Add billing flow documentation (simulated Stripe)
- [ ] Add rate limiting strategy
- [ ] Update DevOps spec with actual deployment plan (Hetzner + GitHub Actions + GHCR)
- [ ] Mark mobile as deferred post-MVP

---

## Notes

- **AI providers used:** Groq (LLM + Whisper, free tier), Gemini 2.0 Flash (free tier), Cohere (embeddings, free trial)
- **Shared types strategy:** Backend OpenAPI → auto-generated TS client in frontend CI + `@inkwell/shared` package for non-API types
- **Worker container** shares the backend image but runs `node dist/worker` — handles BullMQ jobs for embedding, analytics aggregation, email
- **RAG scope:** Only the writer's own articles (not platform-wide) — makes the demo story "it writes like *me*"
- **Mobile decision point:** Phase 5, week 10 — only if web is fully stable
