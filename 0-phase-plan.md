# 🗺️ Inkwell.ai — Phase Plan

> **Target defense:** September 2026 (14-week timeline from May 21, 2026)
> **Stack:** Next.js 15 · NestJS 11 · PostgreSQL + pgvector · Redis · MinIO · Groq · Gemini · OpenAI (embeddings) · Drizzle ORM
> **Repos:** `frontend.inkwell.ai` · `backend.inkwell.ai` · `docker.inkwell.ai` · `mobile.inkwell.ai` (deferred)
> **Core pivot (post-mentor-review):** Inkwell is a **writer ↔ magazine marketplace**. Analytics is now decision support for magazine licensing decisions, not just writer vanity.

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
- [ ] Define full Drizzle schema per [`6-database-schema.md`](./6-database-schema.md):
  - [ ] `users` (account_type: personal/magazine, role/plan orthogonal, username unique, earnings_balance, is_marketplace_eligible + eligibility fields, soft delete)
  - [ ] `magazine_profiles` (1-to-1 with users; subscription_status, credit_balance, monthly_credit_allowance, subscription timestamps)
  - [ ] `magazine_subscriptions` (renewal history per billing cycle)
  - [ ] `articles` (slug, TipTap JSON, placement + marketplace_price, tsvector for search, soft delete)
  - [ ] `tags` + `article_tags` join
  - [ ] `comments` (threaded, soft delete)
  - [ ] `likes`, `follows`, `reposts` (with unique constraints)
  - [ ] `article_purchases` (two-stage: preview_unlock + full_purchase, parent_purchase_id self-ref)
  - [ ] `transactions` (updated types: subscription_charge, monthly_credit_grant, credit_topup, preview_unlock, article_full_purchase, writer_payout, platform_fee, refund)
  - [ ] `writer_eligibility_audit_log` (threshold + admin_grant entries with snapshots)
  - [ ] `notifications` (incl. new types: article_previewed, article_purchased, earnings_credited)
  - [ ] `reports` (status, admin_notes, resolved_by)
  - [ ] `ai_interactions` (incl. portfolio_insight action type)
  - [ ] `user_ai_memory` (structured: tone, style, vocabulary, topics)
  - [ ] `portfolio_insights` (cache table with expires_at)
  - [ ] `article_chunks` (embedding vector(1536) + HNSW index)
  - [ ] `analytics_events`, `article_metrics`
  - [ ] `writer_audience_metrics`, `writer_content_metrics`, `writer_quality_metrics`
- [ ] Run first migration with `drizzle-kit push`
- [ ] `@nestjs/swagger` configured — Swagger UI at `/docs`
- [ ] `@nestjs/config` — environment validation with Zod
- [ ] Auth module:
  - [ ] Email/password registration + login (with account_type selection: personal or magazine)
  - [ ] Magazine self-signup flow (extra fields: name, slug, website, description, logo) + mandatory subscription wall before dashboard access
  - [ ] Google OAuth (Passport.js, personal accounts only)
  - [ ] JWT access token (15 min) + refresh token (7 days)
  - [ ] Guards: `JwtAuthGuard`, `RolesGuard`, `PlansGuard`, `AccountTypeGuard`
- [ ] Users module — GET /u/:username, GET /m/:slug, PATCH /users/me
- [ ] Articles module:
  - [ ] POST /articles (create draft)
  - [ ] PATCH /articles/:id (update)
  - [ ] POST /articles/:id/publish (includes placement choice: public or marketplace; eligibility guard on marketplace)
  - [ ] DELETE /articles/:id (soft delete)
  - [ ] PATCH /articles/:id/placement — switch marketplace → public (one-way only)
  - [ ] GET /articles (feed — paginated, public articles only)
  - [ ] GET /articles/:slug (single article — respects visibility + purchase state for marketplace)
  - [ ] Slug auto-generation from title
- [ ] Tags module — GET /tags, POST /tags
- [ ] `@nestjs/throttler` — basic rate limiting on all endpoints
- [ ] **Ledger invariant tests** — first tests in the project:
  - [ ] `earnings_balance == SUM(completed writer_payout)` for every writer
  - [ ] `credit_balance == grants + topups − debits` for every magazine
  - [ ] Run after every transaction-related test

### Frontend
- [ ] Install shadcn/ui + configure components
- [ ] Install TanStack Query v5 + Zustand
- [ ] Install Auth.js (NextAuth.js) — email + Google OAuth
- [ ] Layout: navbar, footer, responsive shell
- [ ] Feed page (`/`) — article cards, pagination, tag filter
- [ ] Article reader page (`/articles/[slug]`) — full article, premium gate, "Licensed by" badge
- [ ] Sign-up flow with **account type selection**: Personal | Magazine
- [ ] Magazine sign-up form (additional fields)
- [ ] Login page
- [ ] Personal profile page (`/u/[username]`) — articles, follow button, stats
- [ ] Magazine profile page (`/m/[slug]`) — library, branding (placeholder; library empty in Phase 1)
- [ ] Editor page (`/editor/[id]`) — basic textarea (TipTap in Phase 2)
- [ ] OpenAPI client codegen configured (`openapi-typescript` or `orval`)
- [ ] Protected route wrapper for auth-required pages

### Exit criteria
- [ ] Personal sign-up → create article → publish → view on feed works
- [ ] Magazine sign-up → see (empty) library page works
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

### Analytics Event Capture (Early — data accrual starts here)
- [ ] Backend: POST /analytics/events — batch event ingestion endpoint
- [ ] Frontend analytics event capture on article pages:
  - [ ] View event on load (with country detection from headers)
  - [ ] Scroll depth via `IntersectionObserver` (per paragraph)
  - [ ] Time-on-page via `visibilitychange` + `beforeunload` + `sendBeacon`
- [ ] Events stored in `analytics_events` table (raw, no aggregation yet)

> **Rationale:** Starting event capture in Phase 2 (instead of Phase 3) ensures weeks of real engagement data accumulate before the September defense. Aggregation workers and dashboards are still built in Phase 3.

### Observability
- [ ] `GET /health` — liveness probe (process running)
- [ ] `GET /ready` — readiness probe (DB + Redis connectivity)
- [ ] Sentry integration (free tier) — backend + frontend error tracking

### Exit criteria
- [ ] Writer can edit with TipTap and upload images
- [ ] AI chat streams tokens in real-time (SSE visible in UI)
- [ ] Inline popup works on text selection with all 5 actions
- [ ] Token counter decrements correctly per AI action
- [ ] Analytics events are being captured and stored on article page visits
- [ ] `/health` and `/ready` endpoints respond correctly

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

### Analytics (Backend) — Aggregation + Dashboards
> Note: event ingestion endpoint and frontend capture moved to Phase 2 (early data accrual).
- [ ] BullMQ worker `aggregate-article-metrics` (every 5 min) → `article_metrics`
- [ ] BullMQ worker `aggregate-writer-audience` (every 15 min) → `writer_audience_metrics`
- [ ] BullMQ worker `aggregate-writer-content` (every 15 min) → `writer_content_metrics`
- [ ] BullMQ worker `aggregate-writer-quality` (every 15 min) → `writer_quality_metrics`
- [ ] GET /articles/:id/analytics — writer-only endpoint (self-improvement)
- [ ] GET /writers/:username/evaluation — magazine-only endpoint (decision support)
  - Combines audience + content + quality rollups in one response
  - Returns 403 if requester is not a magazine

### Social (Frontend)
- [ ] Like button with optimistic UI
- [ ] Comment section under articles — threaded replies
- [ ] Follow button on profile pages
- [ ] Repost button
- [ ] Notification bell — live SSE connection, unread count badge
- [ ] Notification dropdown list

### Analytics (Frontend) — Dashboards
> Note: frontend event capture moved to Phase 2 (early data accrual).
- [ ] Writer analytics dashboard (`/dashboard`):
  - [ ] Views per article (chart)
  - [ ] Avg read time
  - [ ] Scroll depth heatmap (bar chart per paragraph)
  - [ ] Top performing articles

### Analytics (Frontend) — Magazine-Facing
- [ ] Writer evaluation page (`/u/[writer-username]?as=magazine` or `/discover/writers/[username]`)
  - [ ] **Audience panel**: unique readers, returning rate, geo distribution, device split
  - [ ] **Content panel**: topic distribution, posting frequency sparkline, consistency, avg length, top tags
  - [ ] **Quality panel**: engagement rate, completion rate, repost rate, comment depth, retention curve
  - [ ] **Portfolio Insights panel** (loaded async, see Phase 4 for AI implementation)
- [ ] Magazine discover page (`/discover`) — browse writers with filters

### Exit criteria
- [ ] Like/comment/follow/repost all work with correct notifications
- [ ] Live notification arrives via SSE without page refresh
- [ ] Writer dashboard shows real engagement data after a test read
- [ ] Magazine can browse writers and view writer evaluation dashboard with real metrics

---

## Phase 4 — RAG (Headline Differentiator)
> Weeks 8–9 · Jul 10–23

### RAG Pipeline (Backend)
- [ ] Install OpenAI SDK (embeddings) + pgvector Drizzle helpers
- [ ] Article chunking on publish:
  - [ ] Split TipTap JSON into paragraph-level chunks
  - [ ] Each chunk embedded via OpenAI `text-embedding-3-small`
  - [ ] Stored in `article_chunks` with `embedding vector(1536)` + HNSW index
  - [ ] BullMQ job: `embed-article` triggered on publish/update
- [ ] Retrieval service:
  - [ ] `findSimilarChunks(authorId, queryEmbedding, topK)` — cosine similarity with pgvector `<=>` operator
  - [ ] Filter by author for writer-facing RAG (writer's own corpus only)
  - [ ] No author filter for cross-corpus search (Phase 4.4 search)
- [ ] Prompt template update — inject top-K retrieved chunks as context

### Writer-Facing RAG (Use Case #1)
- [ ] POST /ai/chat — enhanced with RAG retrieval from the user's own articles
- [ ] GET /ai/retrieval-debug — returns chunks used in last request (for demo/transparency)

### Magazine-Facing RAG — Portfolio Insights (Use Case #2)
- [ ] POST /ai/portfolio-insights/:writerUsername
  - [ ] Auth guard: only magazine accounts can call
  - [ ] Retrieves representative chunks from writer's full corpus
  - [ ] Builds structured prompt (voice / topics / consistency / fit / strengths-gaps)
  - [ ] LLM call with Zod-validated structured output
  - [ ] Caches result in `portfolio_insights` table for 24h
  - [ ] Invalidation: cache deleted when writer publishes a new article
- [ ] GET /writers/:username/portfolio-insights — returns cached or triggers generation
- [ ] Frontend: Portfolio Insights panel on writer evaluation page (`/u/[username]?as=magazine`)
  - [ ] Loading state during async generation
  - [ ] Cached result rendered with last-updated timestamp

### Search
- [ ] Postgres full-text search — `tsvector` on `articles.title + content + excerpt`
- [ ] GET /search?q= — hybrid: full-text + semantic search
  - [ ] Lexical results via `ts_rank` on `tsvector`
  - [ ] Semantic results via pgvector cosine similarity (`<=>`) on query embedding
  - [ ] **Reciprocal Rank Fusion (RRF)** to merge both result sets: `score = Σ 1/(k + rank_i)` with k=60
- [ ] Frontend: search bar in navbar → search results page

### Frontend
- [ ] Search bar in navbar → search results page
- [ ] "Sources used" expandable section below AI responses (shows which past articles were referenced)
- [ ] RAG demo notice in writer chat: "AI trained on your X published articles"
- [ ] Portfolio Insights panel renders structured report

### Exit criteria
- [ ] Publish 5+ articles with distinct topics/vocabulary
- [ ] **Writer demo**: AI chat generates a new article that demonstrably uses retrieved vocabulary and style
- [ ] **Magazine demo**: Magazine views a writer's profile → Portfolio Insights panel shows AI-generated voice/topics/score/fit
- [ ] `/ai/retrieval-debug` shows correct chunk IDs pulled from the user's articles
- [ ] Search returns relevant results for both keyword and semantic queries
- [ ] Cache invalidation works (publish a new article → next insights request regenerates)

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

### Marketplace — Subscription + Preview/Purchase Transactions
- [ ] Backend subscription module:
  - [ ] POST /subscriptions/magazine — activate magazine subscription (simulated payment, sets subscription_status + initial credit_balance)
  - [ ] BullMQ cron job `renew-magazine-subscriptions` — monthly credit grant + renewal row insert
  - [ ] POST /credits/topup — optional extra credits for magazines (simulated)
  - [ ] Subscription guard middleware — 403 if magazine subscription inactive on marketplace endpoints
- [ ] Backend marketplace module:
  - [ ] Writer eligibility BullMQ worker `check-writer-eligibility` — runs after each analytics aggregation, flips eligible writers
  - [ ] GET /discover/writers — magazine-only writer browse with filters/sort (subscription required)
  - [ ] GET /discover/marketplace — magazine-only browse of marketplace-listed articles
  - [ ] POST /purchases/preview — preview unlock (atomic DB transaction):
    - [ ] Validates `subscription_status = active` + `credit_balance >= preview_price`
    - [ ] Debits magazine `credit_balance`
    - [ ] Credits writer `earnings_balance` (preview_price - platform_fee)
    - [ ] Inserts `article_purchases` row (`stage = preview_unlock`)
    - [ ] Inserts transaction rows (preview_unlock + writer_payout)
    - [ ] Idempotency key prevents double-charge
  - [ ] POST /purchases/buy — full purchase (atomic DB transaction):
    - [ ] Looks up prior preview row for (article_id, magazine_id)
    - [ ] Validates credit_balance >= remaining amount (price - preview_paid)
    - [ ] Debits magazine, credits writer, inserts full_purchase row with parent_purchase_id
    - [ ] Idempotency key
  - [ ] GET /magazines/me/library — magazine's fully purchased articles
  - [ ] GET /me/earnings — writer's earnings summary (preview payouts + purchase payouts)
  - [ ] Admin: POST /admin/eligibility/:writerId — grant eligibility manually + audit log entry
- [ ] Notifications:
  - [ ] Writer notified when article previewed by a magazine
  - [ ] Writer notified when article purchased by a magazine
  - [ ] Writer notified when earnings credited
- [ ] Frontend marketplace UI:
  - [ ] Marketplace placement option + price input in publish flow (greyed + eligibility progress if not eligible)
  - [ ] Magazine subscription screen (sign-up wall and settings)
  - [ ] Magazine Discover page with writer cards + filters
  - [ ] Writer evaluation page: marketplace article list with "Preview" / "Purchase" buttons
  - [ ] Preview confirmation modal (shows 10% cost + credit balance)
  - [ ] Purchase confirmation modal (shows remaining 90% + credit balance + preview-credit note)
  - [ ] Magazine library page (fully purchased articles)
  - [ ] Writer earnings dashboard (preview + purchase transactions itemized)
  - [ ] Magazine credit balance display + top-up flow
  - [ ] Writer eligibility progress bar on dashboard
  - [ ] Admin: eligibility grant UI in admin panel

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
- [ ] **Marketplace end-to-end demo**: Admin grants eligibility to demo writer → Writer publishes article to marketplace → Magazine (with active subscription) browses → views writer evaluation + Portfolio Insights → previews article (credits debited 10%) → purchases full (credits debited remaining 90%) → article appears in magazine library → writer earnings reflect both the preview payout and the purchase payout

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

### Demo & Seed Mode
- [ ] `DEMO_MODE=true` environment flag:
  - [ ] Lowered eligibility thresholds (e.g., 5 readers + 2 reactions)
  - [ ] Seed script: pre-populate demo writers, 10+ substantive articles, analytics events, magazine account
  - [ ] Demo scenario: writer crosses eligibility live → publishes to marketplace → magazine previews + purchases
- [ ] `reconcile-balances` background job — asserts snapshot == ledger sum, alerts on drift

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
> Most addressed in the 2026-05-21 spec update pass

- [x] Fix subscription model in spec — `role` + `plan` (not mutex enum) + `account_type`
- [x] Add `slug` field to articles spec
- [x] Add `username` field to users spec
- [x] Commit to TipTap JSON as article content format
- [x] Add tags/categories to MVP feature list
- [x] Add search (full-text + semantic) to MVP feature list
- [x] Add soft deletes to database schema spec
- [x] Specify LLM providers (Groq primary, Gemini fallback)
- [x] Specify voice provider (Groq Whisper-large-v3-turbo)
- [x] Specify embeddings provider (OpenAI text-embedding-3-small, 1536-dim) *(switched from Cohere 2026-05-29 — trial expiry risk)*
- [x] Structured AI memory schema (not JSON blob)
- [x] Add SSE real-time strategy doc *(referenced in flows + analytics)*
- [ ] Add rate limiting strategy *(stub in features; expand in DevOps before Phase 1)*
- [x] Update DevOps spec with actual deployment plan (Hetzner + GitHub Actions + GHCR) *(updated 2026-05-29)*
- [x] Remove stale Python AI service references from system architecture + DevOps specs *(updated 2026-05-29)*
- [x] Add ledger integrity & concurrency section to database schema *(updated 2026-05-29)*
- [x] Specify AI memory extraction pipeline in AI design *(updated 2026-05-29)*
- [x] Add hybrid search fusion (RRF) specification *(updated 2026-05-29)*
- [x] Add demo/seed mode tasks to Phase 6 *(updated 2026-05-29)*
- [x] Move analytics event capture to Phase 2 *(updated 2026-05-29)*
- [x] Add observability tasks (/health, /ready, Sentry) to Phase 2 *(updated 2026-05-29)*
- [ ] Mark mobile as deferred post-MVP *(noted in plan header; not yet in spec docs)*

## Marketplace Pivot Backlog (2026-05-21)
> Spec changes from the writer-magazine marketplace redesign

- [x] Add Magazine account type to product overview + features
- [x] Redesign analytics into writer-facing + magazine-facing surfaces
- [x] Add article licensing flow (listings, purchases, library)
- [x] Add Portfolio Insights as second RAG use case in AI design
- [x] Add marketplace tables to database schema (licenses, transactions, magazine_profiles, writer rollup metrics)
- [x] Add marketplace flows to user-flows.md
- [x] Add Marketplace + Transactions modules to system architecture
- [x] Distribute marketplace tasks across Phases 1, 3, 4, 5

## Subscription + Preview Model Pivot (2026-05-25)
> Spec changes from the magazine subscription + three-stage article flow redesign

- [x] Replace per-article wallet licensing with subscription + monthly credit budget model
- [x] Add three-stage magazine article flow (free browse → preview unlock 10% → full purchase 90%)
- [x] Add writer eligibility gating (5K readers + 1K reactions, lifetime, admin bypass)
- [x] Add article placement (public vs marketplace, mutually exclusive, one-way switch)
- [x] Replace `article_licenses` table with `article_purchases` (two-stage, parent_purchase_id self-ref)
- [x] Add `magazine_subscriptions` renewal history table
- [x] Add `writer_eligibility_audit_log` table
- [x] Update `magazine_profiles` with subscription state fields
- [x] Update `users` with earnings_balance + eligibility fields (replace wallet_balance)
- [x] Update transaction types for new money flows
- [x] Add eligibility computation section to analytics model
- [x] Gate Portfolio Insights behind magazine subscription in ai-design.md
- [x] Update all user flows (sign-up wall, publish flow, preview/purchase flows)
- [x] Update Phase 1 schema tasks and Phase 5 marketplace tasks in phase plan

---

## Notes

- **AI providers used:** Groq (LLM + Whisper, free tier), Gemini 2.0 Flash (free tier), OpenAI (embeddings, $0.02/1M tokens)
- **Shared types strategy:** Backend OpenAPI → auto-generated TS client in frontend CI + `@inkwell/shared` package for non-API types
- **Worker container** shares the backend image but runs `node dist/worker` — handles BullMQ jobs for embedding, analytics aggregation, email
- **RAG scope:** Only the writer's own articles (not platform-wide) — makes the demo story "it writes like *me*"
- **Mobile decision point:** Phase 5, week 10 — only if web is fully stable

## Droppable Features (Priority Order)
> If time pressure builds, drop features in this order (top = first to cut):

1. **Mobile app** (already deferred)
2. **Voice-to-article** — architecturally isolated, pure additive feature
3. **Reposts** — one quality signal, low demo value
4. **Transactional email** — nice-to-have polish, not a differentiator
5. **Dynamic OG images** — SEO polish, not load-bearing
6. **Follows / follower-growth chart** — vanity metrics
7. **Advanced moderation** (beyond basic report queue)

**Never cut:** Editor, AI chat/inline, RAG (write-like-me + Portfolio Insights), Analytics (event capture + dashboards), Marketplace (preview/purchase + locked ledger), Likes + Comments (feed eligibility computation)
