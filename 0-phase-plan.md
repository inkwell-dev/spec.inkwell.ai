# 🗺️ Inkwell.ai — Phase Plan

> **Target defense:** September 2026 (~16-week timeline from May 21, 2026 — re-baselined 2026-07-26)
> **Stack:** Next.js 15 · NestJS 11 · PostgreSQL + pgvector · Redis · MinIO · Groq · Gemini · OpenAI (embeddings) · Drizzle ORM
> **Repos:** `frontend.inkwell.ai` · `backend.inkwell.ai` · `docker.inkwell.ai` · `mobile.inkwell.ai` (deferred)
> **Core pivot (post-mentor-review):** Inkwell is a **writer ↔ magazine marketplace**. Analytics is now decision support for magazine licensing decisions, not just writer vanity.
> **Re-baseline (2026-07-26):** The June–July design track (Stitch prompts, desktop refinement, Figma inventory, design QA) was executed between Phase 1 and Phase 2 but was never modeled in the original plan. It is now recorded as **Phase D**, the remaining implementation phases are re-dated from Jul 27, and scope is frozen to the defensible core (see *Post-MVP Descope*). Phase numbers 2–6 are unchanged so cross-references from other spec docs remain valid.

---

## 🏃 Sprint Map (report alignment)

The report presents the plan as fixed 2-week Scrum sprints. Each sprint's goal maps onto the phases below:

| Sprint | Dates | Sprint goal (phase mapping) | Status |
|--------|-------|-----------------------------|--------|
| **S0** | May 22 – May 28 | Phase 0 — Foundation (repos, Docker, CI/CD) | ✅ Done |
| **S1** | May 29 – Jun 11 | Phase 1 — Schema, Auth, Core CRUD | ✅ Done (exit criteria verified Jun 13) |
| **S2** | Jun 12 – Jun 25 | Phase D — Design system + mobile (375px) screen set | ✅ Done |
| **S3** | Jun 26 – Jul 9 | Phase D — Desktop (1440px) screen set + refinement | ✅ Done |
| **S4** | Jul 10 – Jul 26 | Phase D — Figma audit, design QA, spec alignment + re-baseline | ✅ Done |
| **S5** | Jul 27 – Aug 9 | Phase 2 — Editor + AI + event capture · Phase 3 (start) — likes/comments · **Q — codebase quality pass** | 🚧 In progress — editor, social + notifications verified end-to-end; **AI streaming unblocked and verified 2026-07-30**; a cross-repo quality pass (Phase Q) landed mid-sprint |
| **S6** | Aug 10 – Aug 23 | Phase 3 — Aggregation + dashboards · Phase 4 — RAG + Insights + Search | 🔜 |
| **S7** | Aug 24 – Sep 6 | Phase 5 — Marketplace + Premium · Phase 6 — Deploy + Defense prep | 🔜 |

> Sprints S5–S7 compress the original Phases 2–6 (10 planned weeks) into 6 weeks. This assumes increased weekly effort and the scope freeze below. **Contingency rule (decided 2026-07-26):** if S6 runs late, the magazine-facing BI dashboard panels (audience / content / quality charts) are reduced to summary cards and documented as future work in the report — but **event capture, article metrics, and the eligibility counters always ship**, because the marketplace gate and the demo narrative depend on them.

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
- [x] Push all repos to GitHub remotes
- [x] Verify `docker compose up --build` brings up all 7 containers locally
- [x] Confirm Swagger UI accessible at `http://localhost/api/docs`

---

## Phase 1 — Auth + Core CRUD
> Weeks 2–3 · May 29–Jun 11

### Backend
- [x] Install Drizzle ORM + `drizzle-kit` + `pg` driver
- [x] Define full Drizzle schema per [`6-database-schema.md`](./6-database-schema.md):
  - [x] `users` (account_type: personal/magazine, role/plan orthogonal, username unique, earnings_balance, is_marketplace_eligible + eligibility fields, soft delete)
  - [x] `magazine_profiles` (1-to-1 with users; subscription_status, credit_balance, monthly_credit_allowance, subscription timestamps)
  - [x] `magazine_subscriptions` (renewal history per billing cycle)
  - [x] `articles` (slug, TipTap JSON, placement + marketplace_price, tsvector for search, soft delete)
  - [x] `tags` + `article_tags` join
  - [x] `comments` (threaded, soft delete)
  - [x] `likes`, `follows`, `reposts` (with unique constraints)
  - [x] `article_purchases` (two-stage: preview_unlock + full_purchase, parent_purchase_id self-ref)
  - [x] `transactions` (updated types: subscription_charge, monthly_credit_grant, credit_topup, preview_unlock, article_full_purchase, writer_payout, platform_fee, refund)
  - [x] `writer_eligibility_audit_log` (threshold + admin_grant entries with snapshots)
  - [x] `notifications` (incl. new types: article_previewed, article_purchased, earnings_credited)
  - [x] `reports` (status, admin_notes, resolved_by)
  - [x] `ai_interactions` (incl. portfolio_insight action type)
  - [x] `user_ai_memory` (structured: tone, style, vocabulary, topics)
  - [x] `portfolio_insights` (cache table with expires_at)
  - [x] `article_chunks` (embedding vector(1536) + HNSW index)
  - [x] `analytics_events`, `article_metrics`
  - [x] `writer_audience_metrics`, `writer_content_metrics`, `writer_quality_metrics`
- [x] Run first migration with `drizzle-kit push`
- [x] `@nestjs/swagger` configured — Swagger UI at `/docs`
- [x] `@nestjs/config` — environment validation with Zod
- [x] Auth module:
  - [x] Email/password registration + login (with account_type selection: personal or magazine)
  - [x] Magazine self-signup flow (extra fields: name, slug, website, description, logo) + mandatory subscription wall before dashboard access
  - [x] Google OAuth (Passport.js, personal accounts only)
  - [x] JWT access token (15 min) + refresh token (7 days)
  - [x] Guards: `JwtAuthGuard`, `RolesGuard`, `PlansGuard`, `AccountTypeGuard`
- [x] Users module — GET /u/:username, GET /m/:slug, PATCH /users/me
- [x] Articles module:
  - [x] POST /articles (create draft)
  - [x] PATCH /articles/:id (update)
  - [x] POST /articles/:id/publish (includes placement choice: public or marketplace; eligibility guard on marketplace)
  - [x] DELETE /articles/:id (soft delete)
  - [x] PATCH /articles/:id/placement — switch marketplace → public (one-way only)
  - [x] GET /articles (feed — paginated, public articles only)
  - [x] GET /articles/:slug (single article — respects visibility + purchase state for marketplace)
  - [x] Slug auto-generation from title
- [x] Tags module — GET /tags, POST /tags
- [x] `@nestjs/throttler` — basic rate limiting on all endpoints
- [ ] **Ledger invariant tests** — first tests in the project:
  - [ ] `earnings_balance == SUM(completed writer_payout)` for every writer
  - [ ] `credit_balance == grants + topups − debits` for every magazine
  - [ ] Run after every transaction-related test

### Frontend
- [x] Install shadcn/ui + configure components
- [x] Install TanStack Query v5 + Zustand
- [x] Install Auth.js (NextAuth.js) — email + Google OAuth (implemented as custom JWT auth with axios interceptors)
- [x] Layout: navbar, footer, responsive shell (+ sidebar, bottom-tab-bar)
- [x] Feed page (`/`) — article cards, pagination, tag filter (+ filter chips, right sidebar widgets)
- [x] Article reader page (`/articles/[slug]`) — full article, premium gate, "Licensed by" badge
- [x] Sign-up flow with **account type selection**: Personal | Magazine (separate forms linked together per Figma)
- [x] Magazine sign-up form (additional fields + logo upload zone)
- [x] Login page (Figma-aligned with heading, reordered form)
- [x] Personal profile page (`/u/[username]`) — articles, follow button, stats (hero + tabbed content)
- [x] Magazine profile page (`/m/[slug]`) — library, branding (hero + tabbed articles/about/writers)
- [x] Editor page (`/editor/[id]`) — basic textarea + publish dialog (TipTap in Phase 2)
- [x] OpenAPI client codegen configured (`openapi-typescript` — `pnpm api:codegen`)
- [x] Protected route wrapper for auth-required pages (Next.js Edge Middleware)

### Exit criteria
- [x] Personal sign-up → create article → publish → view on feed works (verified 2026-06-13)
- [x] Magazine sign-up → see (empty) library page works (verified 2026-06-13)
- [x] Premium article is gated for free users
- [x] OpenAPI spec is accessible and frontend client auto-generates from it

---

## Phase D — Design & Prototyping
> Sprints S2–S4 · Jun 12 – Jul 26 · **Completed** (backfilled into the plan on 2026-07-26 from git history)

> **Why this phase exists:** the original plan jumped from Phase 1 directly into the TipTap editor. In practice, June–July was spent producing the complete design layer that the remaining frontend phases build from. The work was real and load-bearing — recording it keeps the plan (and the report generated from it) aligned with the project's actual execution.

- [x] Design specification document ([`9-design.md`](./9-design.md)) — tooling, design tokens, breakpoints, 104-frame sitemap, role variants
- [x] Stitch AI prompt set for all screens — mobile 375px (`design/prompts/00`–`17`)
- [x] Premium design-system enhancement pass across all prompts
- [x] Prompts synced with the revised marketplace + subscription model
- [x] Desktop (1440px) Stitch prompts for all screens (`design/prompts/DESKTOP-PROMPTS.md`)
- [x] Desktop refinement pass (`design/prompts/desktop-refinement.md`)
- [x] Figma inventory + audit (`design/figma-inventory.md`)
- [x] Design quality review (`design/quality-review.md`)
- [x] Spec alignment pass + plan re-baseline (2026-07-26)

---

## Phase 2 — Editor + Basic AI
> Sprint S5 · Jul 27 – Aug 9 *(re-dated from Jun 12–25)*

### Editor
- [x] Install TipTap + extensions (StarterKit, Placeholder, Image, CodeBlock, Typography)
- [x] Replace textarea with TipTap editor in `/editor/[id]`
- [x] Image upload — paste/drag into editor → upload to MinIO → embed URL
- [ ] Thumbnail upload for article cover
- [x] Auto-save draft on change (debounced PATCH, 1.5s)
- [x] Word count + estimated read-time display

### AI Gateway (Backend)
- [x] Install Vercel AI SDK (`ai`, `@ai-sdk/groq`, `@ai-sdk/google`)
- [x] `AiModule` — provider abstraction, prompt builder
- [x] Token quota middleware — check `ai_tokens_remaining` before each AI request, decrement after
- [x] Daily token reset cron job (BullMQ scheduled job)
- [x] Log every AI interaction to `ai_interactions` table
- [x] POST /ai/chat — contextual chat assistant (article context injected)
- [x] POST /ai/inline — inline editing actions (reformulate/shorten/expand/simplify/improve)
- [x] SSE streaming for all AI endpoints (Vercel AI SDK `streamText`)

### AI Features (Frontend)
- [x] AI chat panel (slide-out sidebar in editor)
  - [x] Chat history UI
  - [ ] "Insert into article" button on AI responses
  - [x] Token usage indicator
- [x] Inline editing popup — appears on text selection
  - [x] 5 action buttons (Reformulate / Shorten / Expand / Simplify / Improve)
  - [x] Streaming result preview
  - [ ] Replace / Insert below / Cancel actions
- [ ] Token quota warning + "upgrade" prompt when tokens depleted

### Analytics Event Capture (Early — data accrual starts here)
- [x] Backend: POST /analytics/events — batch event ingestion endpoint
- [x] Frontend analytics event capture on article pages (`useArticleTracking`):
  - [x] View event on load — *(country detection from headers still missing)*
  - [x] Scroll depth — implemented as a max-scroll **percentage** on page leave, **not** the specified per-paragraph `IntersectionObserver`
  - [x] Time-on-page via `visibilitychange` + `beforeunload` + `sendBeacon`
- [x] Events stored in `analytics_events` table (raw, no aggregation yet)

> **Rationale:** Starting event capture in Phase 2 (instead of Phase 3) ensures weeks of real engagement data accumulate before the September defense. Aggregation workers and dashboards are still built in Phase 3.
>
> **Reality check (2026-07-30):** capture is live and verified — `analytics_events` holds view / scroll / time_on_page rows. But the accrual argument does **not** currently hold: all events to date span a single article, because the dev database has only 2 articles and no real readers. Data volume is blocked on *content*, not on capture code. This is the main reason a **seed script** is now a prerequisite for demonstrating Phase 3 dashboards and the Phase 4 RAG comparison, not a nice-to-have.
>
> Two deviations from the original spec are recorded above rather than silently closed: scroll depth is a single page-level percentage, so the **per-paragraph heatmap** promised in Phase 3 cannot be built from it without changing this capture; and no country is recorded, so the **geo distribution** panel in the magazine-facing audience report has no source. Both are cheap to add now and expensive to backfill, since events already captured cannot be re-derived.

### Observability
- [x] `GET /health` — liveness probe (process running)
- [x] `GET /ready` — readiness probe (DB + Redis connectivity)
- [ ] Sentry integration (free tier) — backend + frontend error tracking

### Exit criteria
- [ ] Writer can edit with TipTap and upload images *(editor works; thumbnail/cover upload still open)*
- [x] AI chat streams tokens in real-time — **verified 2026-07-30**: chunks arrive incrementally (~7 ms apart, not buffered) and the model responds. Browser-side "visible in UI" still to be confirmed in the editor panel.
- [x] Inline popup works on text selection — backend path verified end-to-end for `shorten`; the other four actions share the same handler and prompt map
- [x] Token counter decrements correctly per AI action — **verified**: 1000 → 673 across two calls (214 + 113), matching the `ai_interactions` rows exactly
- [x] Analytics events are being captured and stored on article page visits — verified in `analytics_events` (see the reality check above on volume)
- [x] `/health` and `/ready` endpoints respond correctly

> **AI unblocked (2026-07-30).** The blocker recorded against S5 was "a valid `GROQ_API_KEY`", but the key was only half the story. `docker.inkwell.ai/.env` wrote the key as `GROQ_API_KEY=   # https://console.groq.com — free tier`, and docker compose does not strip a trailing comment — so the container received the *comment text* as the key. The comment contains an em-dash (U+2014), which is illegal in an HTTP header, so `@ai-sdk/groq` threw inside the `Headers` constructor before any request was made. Because `streamText` defers the model call until the stream is consumed — by which point the 200 and its headers are already written — every AI request returned an empty `200 OK` with no error, no billing, no `ai_interactions` row and nothing in the logs. A valid key pasted onto that line would have failed the same way. Comments now sit on their own line in `.env` and `.env.example`.
>
> A second defect was fixed alongside it: `users.ai_tokens_remaining` defaults to 0 and only the nightly reset job ever wrote it, so a user who became premium at 00:05 UTC had no AI for ~24 h, and if the worker was down at midnight nobody got tokens at all. `AiQuotaGuard` now grants the plan allowance on demand, atomically, which demotes the cron to a pre-warm. Free-plan users remain at 0 by design (spec §6.1).

---

## Phase Q — Codebase Quality Pass
> Sprint S5 · 2026-07-29 → 07-30 · **Completed** (backfilled into the plan on 2026-07-30, in the same spirit as Phase D)

> **Why this phase exists:** a full audit of both repos was run before starting Phase 3, on the reasoning that Phases 3–5 add far more UI and endpoints than exist today, and that duplication is cheapest to remove before it is copied. It produced 48 findings and **11 real defects**, several of which would have surfaced during the defense demo. Recording it keeps the plan honest about where S5 time actually went, and several Phase 3 line items were delivered early as a side effect.

**Executed in three tiers**, one branch per tier per repo, merged into `feat/sprint-s5`:

- [x] **Tier 0 — defects** (13 commits): rate limiting was entirely inert (`ThrottlerGuard` never registered); the daily AI-token job was never scheduled; re-liking spammed unlimited notifications; SSE auth errors returned 500 instead of 401; the auth cookie was never refreshed, so **every session silently died after 15 minutes**, losing unsaved editor work; the AI chat auto-scroll was a no-op; `Math.random()` ran in a render body
- [x] **Tier 1 — shared abstractions** (21 commits): composite `@Auth()` decorator (22 repeated guard stacks → 1); `{ items, page, limit, total, hasMore }` pagination envelope; `withTx()` — the codebase had **zero** `db.transaction()` calls; typed notification payloads; one 404-missing / 403-not-yours ownership policy; 12 shared frontend primitives (`StatTile`, `EmptyState`, `ErrorState`, skeleton kit, `FollowButton`, `UserAvatar`, `IconActionButton`, `WriterCard`, `Notice`, `FilterPill`, `FormField`, query-key factory)
- [x] **Tier 2 — cleanup** (18 commits): global Postgres exception filter (constraint violations were leaking as 500s); `strict: true` enabled; ESLint 45 problems → **0** in both repos; `next/image`; dark mode made reachable; three article-card implementations merged into one
- [x] **Infrastructure**: dev containers ran as root and wrote root-owned `.next`/`dist` into the working tree, breaking host builds permanently; `NEXT_PUBLIC_API_URL` pointed at a port nothing listened on, so **no client-side request in the browser ever succeeded**; tabs rendered beside their panel due to a Tailwind variant that matched nothing

**Delivered early (ticked in their own phases above):** the Phase 3 follow button, and the article-tag loop end to end — publish accepts `tagIds`, `article_tags` is finally written, and `?tag=` filters for real. That last one matters beyond the feed: Phase 3's `writer_content_metrics` aggregates `topicDistribution` and `topTags` from `article_tags`, a table **no code had ever written to**.

**Verification:** both repos typecheck clean under `strict: true` with zero lint errors; a 24-check integration suite passes against the live stack; the feed was confirmed rendering live API data in a real browser.

> **Cost/benefit for the report:** ~2 days of S5. The counter-argument is that it consumed schedule in the tightest sprint; the argument for is that four of the defects (dead sessions, inert rate limiting, silent AI failure, unreachable browser API) would each have been demo-stopping, and Phase 3's dashboards and Phase 5's marketplace UI now assemble from existing primitives rather than starting from raw markup.

---

## Phase 3 — Social + Analytics
> Sprints S5–S6 · Jul 27 – Aug 23 *(re-dated from Jun 26–Jul 9; likes/comments/notifications land in S5, aggregation + dashboards in S6)*

### Social (Backend)
- [x] Likes module — POST /articles/:id/like, DELETE /articles/:id/like
- [x] Comments module — POST/GET/DELETE for threaded comments
- [x] Follows module — POST /users/:username/follow, DELETE unfollow *(stretch — first social cut under time pressure)*
- [ ] Reposts module — POST /articles/:id/repost *(stretch — first social cut under time pressure)*
- [x] Notifications module:
  - [x] Create notification on like / comment / follow events
  - [x] GET /notifications (paginated list)
  - [x] PATCH /notifications/:id/read
  - [x] SSE endpoint GET /notifications/stream — live delivery

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
- [x] Like button with optimistic UI
- [x] Comment section under articles — threaded replies
- [x] Follow button on profile pages — one shared `<FollowButton>` (handles self / logged-out / pending), replacing three disabled `TODO(Phase 3)` stubs. Delivered early by the quality pass; see the Tier 0–2 note below.
- [ ] Repost button
- [x] Notification bell — live SSE connection, unread count badge
- [x] Notification dropdown list

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
- [x] Live notification arrives via SSE without page refresh
- [ ] Writer dashboard shows real engagement data after a test read
- [ ] Magazine can browse writers and view writer evaluation dashboard with real metrics

---

## Phase 4 — RAG (Headline Differentiator)
> Sprint S6 · Aug 10 – Aug 23 *(re-dated from Jul 10–23)*

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

## Phase 5 — Marketplace + Premium + Moderation
> Sprint S7 · Aug 24 – Sep 6 *(re-dated from Jul 24–Aug 6; voice, email, AI eval harness and the mobile go/no-go moved to Post-MVP Descope)*

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

### Exit criteria
- [ ] Upgrade flow changes user plan and unlocks premium articles + AI features
- [ ] Reported content appears in admin queue
- [ ] **Marketplace end-to-end demo**: Admin grants eligibility to demo writer → Writer publishes article to marketplace → Magazine (with active subscription) browses → views writer evaluation + Portfolio Insights → previews article (credits debited 10%) → purchases full (credits debited remaining 90%) → article appears in magazine library → writer earnings reflect both the preview payout and the purchase payout

---

## Phase 6 — Polish, Deploy & Defense Prep
> Sprint S7 (parallel with Phase 5) · Aug 24 – defense · *(re-dated from Aug 7–end of August)*

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
- [ ] Dynamic OG images for articles (Next.js `ImageResponse`) *(stretch — zero demo value)*
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

## 📦 Post-MVP Descope (2026-07-26 re-baseline)
> Features formally removed from the MVP commitment so the report's sprint plan only promises what will ship. Each is documented as "future work" in the report, not as a missed deliverable. Removed from the phases above; listed here with their original phase for traceability.

- **Voice-to-article** *(was Phase 5)* — architecturally isolated, pure additive feature; POST /ai/voice + recorder UI
- **Transactional email (Resend)** *(was Phase 5)* — welcome / password-reset / follower emails + `send-email` job
- **AI eval harness** *(was Phase 5, optional)* — LLM-as-judge scoring of AI actions; competes with must-ship marketplace work
- **Mobile app (`mobile.inkwell.ai`)** *(was a Phase 5 go/no-go)* — decision resolved: deferred post-MVP
- **Cookie consent / analytics opt-out** *(was Phase 6 polish)* — GDPR polish, not needed for the demo
- **Advanced moderation** beyond the basic report queue

**Contingency (only if S6 slips) — "BI trim":** magazine-facing dashboard panels (audience / content / quality charts) reduce to summary cards; full BI dashboards documented as future work. The event capture pipeline, `article_metrics`, and eligibility counters are **not** part of this trim — the marketplace gate depends on them.

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
- [x] Add rate limiting strategy *(covered in [`9-implementation-guide.md`](./9-implementation-guide.md) §12)*
- [x] Update DevOps spec with actual deployment plan (Hetzner + GitHub Actions + GHCR) *(updated 2026-05-29)*
- [x] Remove stale Python AI service references from system architecture + DevOps specs *(updated 2026-05-29)*
- [x] Add ledger integrity & concurrency section to database schema *(updated 2026-05-29)*
- [x] Specify AI memory extraction pipeline in AI design *(updated 2026-05-29)*
- [x] Add hybrid search fusion (RRF) specification *(updated 2026-05-29)*
- [x] Add demo/seed mode tasks to Phase 6 *(updated 2026-05-29)*
- [x] Move analytics event capture to Phase 2 *(updated 2026-05-29)*
- [x] Add observability tasks (/health, /ready, Sentry) to Phase 2 *(updated 2026-05-29)*
- [x] Mark mobile as deferred post-MVP *(resolved by 2026-07-26 re-baseline — see Post-MVP Descope)*

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

## Re-Baseline Log (2026-07-26)
> Third plan revision, after the 2026-05-21 marketplace pivot and 2026-05-25 subscription pivot

- [x] Backfill Phase D (Design & Prototyping, Jun 12 – Jul 26) from git history — the design track was executed but never modeled in the original plan
- [x] Re-date Phases 2–6 from Jul 27 onward (phase numbers unchanged to preserve cross-doc references)
- [x] Add sprint map (S0–S7, 2-week Scrum sprints) for report alignment
- [x] Freeze scope: move voice, email, AI eval harness, mobile go/no-go, cookie consent, advanced moderation to Post-MVP Descope
- [x] Define the BI-trim contingency rule (magazine dashboard panels → summary cards if S6 slips; eligibility pipeline never trimmed)

---

## Notes

- **AI providers used:** Groq (LLM + Whisper, free tier), Gemini 2.0 Flash (free tier), OpenAI (embeddings, $0.02/1M tokens)
- **Shared types strategy:** Backend OpenAPI → auto-generated TS client in frontend CI + `@inkwell/shared` package for non-API types
- **Worker container** shares the backend image but runs `node dist/worker` — handles BullMQ jobs for embedding, analytics aggregation, email
- **RAG scope:** Only the writer's own articles (not platform-wide) — makes the demo story "it writes like *me*"
- **Mobile:** deferred post-MVP (resolved by the 2026-07-26 re-baseline — see Post-MVP Descope)

## Droppable Features (Priority Order)
> Mobile, voice, email, AI eval, cookie consent, and advanced moderation were already descoped in the 2026-07-26 re-baseline. If further time pressure builds, drop the remaining features in this order (top = first to cut):

1. **Reposts** — one quality signal, low demo value
2. **Follows / follower-growth chart** — vanity metrics
3. **Dynamic OG images** — SEO polish, not load-bearing
4. **BI trim** (last resort, per contingency rule) — magazine dashboard panels reduced to summary cards; eligibility pipeline untouched

**Never cut:** Editor, AI chat/inline, RAG (write-like-me + Portfolio Insights), Analytics (event capture + dashboards), Marketplace (preview/purchase + locked ledger), Likes + Comments (feed eligibility computation)
