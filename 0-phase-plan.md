# 🗺️ Inkwell.ai — Phase Plan

> **Target defense:** September 2026 (~16-week timeline from May 21, 2026 — re-baselined 2026-07-26)
> **Stack:** Next.js 15 · NestJS 11 · PostgreSQL + pgvector · Redis · MinIO · Groq · Gemini (LLM fallback + embeddings) · Drizzle ORM
> **Repos:** `frontend.inkwell.ai` · `backend.inkwell.ai` · `docker.inkwell.ai` · `mobile.inkwell.ai` (deferred)
> **Core pivot (post-mentor-review):** Inkwell is a **writer ↔ magazine marketplace**. Analytics is now decision support for magazine licensing decisions, not just writer vanity.
> **Re-baseline (2026-07-26):** The June–July design track (Stitch prompts, desktop refinement, Figma inventory, design QA) was executed between Phase 1 and Phase 2 but was never modeled in the original plan. It is now recorded as **Phase D**, the remaining implementation phases are re-dated from Jul 27, and scope is frozen to the defensible core (see *Post-MVP Descope*). Phase numbers 2–6 are unchanged so cross-references from other spec docs remain valid.

---

## 🏃 Sprint Map (report alignment)

The report presents the plan as fixed 2-week Scrum sprints. Each sprint's goal maps onto the phases below:

| Sprint | Dates | Sprint goal (phase mapping) | Status |
|--------|-------|-----------------------------|--------|
| **S0** | May 22 – May 28 | Phase 0 — Foundation (repos, Docker, CI/CD) | ✅ Done |
| **S1** | May 29 – Jun 11 | Phase 1 — Schema, Auth, Core CRUD | ✅ Done (exit criteria verified Jun 13; the deferred ledger invariant tests closed 2026-07-30) |
| **S2** | Jun 12 – Jun 25 | Phase D — Design system + mobile (375px) screen set | ✅ Done |
| **S3** | Jun 26 – Jul 9 | Phase D — Desktop (1440px) screen set + refinement | ✅ Done |
| **S4** | Jul 10 – Jul 26 | Phase D — Figma audit, design QA, spec alignment + re-baseline | ✅ Done |
| **S5** | Jul 27 – Aug 9 | Phase 2 — Editor + AI + event capture · Phase 3 (start) — likes/comments · **Q — codebase quality pass** | ✅ Done — editor, social + notifications verified end-to-end; **AI streaming unblocked and verified 2026-07-30**; a cross-repo quality pass (Phase Q) landed mid-sprint; **dev/prod URL topology reworked 2026-08-05/06**, which fixed image upload and pulled four Phase 6 deploy items forward. Six trailing items were closed out on **2026-08-10**, one day past the window — see *S5 Close-out* below |
| **S6** | Aug 10 – Aug 23 | ~~Phase 3 — Aggregation + dashboards~~ *(pulled forward into S5)* · Phase 4 — RAG + Insights + Search | ✅ Done — opened on Aug 10 with the S5 close-out running in parallel on day 1. Phases 2 and 3 were already closed, so S6 was Phase 4 only. **All six Phase 4 exit criteria verified 2026-08-15**, eight days inside the window; the magazine-facing Portfolio Insights demo had never been run before that day and passed on first execution |
| **S7** | Aug 24 – Sep 6 | Phase 5 — Marketplace + Premium · Phase 6 — Deploy + Defense prep | 🔜 — **deployment is the last work of the last sprint** (decision of 2026-08-10). Phase 5 and the quality/SEO/demo parts of Phase 6 come first; the deploy block is blocked on buying a domain and a VPS and is scheduled after them |

> **Development is local-only until the end (decided 2026-08-10).** No domain has
> been registered and no VPS provisioned; both are purchases, not engineering, and
> nothing in Phases 4–5 depends on either. All deployment work is therefore
> consolidated into one block at the end of Phase 6 — see *Production Deploy*.
> The production configuration is already written and tested against live
> containers (Phase I), so this is a deferral of execution, not of design.

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
- [x] **Ledger invariant tests** — first tests in the project *(completed 2026-07-30)*:
  - [x] `earnings_balance == SUM(completed writer_payout)` for every writer
  - [x] `credit_balance == grants + topups − debits` for every magazine
  - [x] Run after every transaction-related test — exposed as
    `expectLedgerConsistent(tx)` in `test/support/ledger.ts`, which Phase 5's
    purchase specs call at the end of each case

> **What this actually required.** The item is written as two queries; it was
> not. There was no working test infrastructure at all — `pnpm test` collected
> zero specs, CI passed on `--passWithNoTests`, and *no* test could import from
> `src` because 242 relative imports end in `.js` and jest-resolve has no
> `extensionAlias`. And because nothing writes `transactions`,
> `article_purchases` or `magazine_subscriptions` yet, the invariants were
> vacuously true: they would have passed while proving nothing.
>
> So the deliverable is a harness plus **27 tests, most of them negative** —
> fixtures build a coherent purchase, then corrupt one column at a time and
> assert the right invariant fires. The suite was validated by sabotage rather
> than by passing: deleting `status = 'completed'` from the earnings query fails
> exactly the pending-payout test, and dropping `preview_unlock` from the debit
> list fails seven. That exercise found a genuine coverage gap (nothing pinned
> the *grant* type filter), which was then closed.
>
> **A third invariant was added:** `credits_paid == platform_fee + writer_payout`
> per purchase row. No constraint enforces it, and it is the arithmetic that
> makes the other two meaningful.
>
> **The ledger's sign convention is now defined and enforced.** `amount` is
> always positive; direction comes from `type` plus `from_user_id`/`to_user_id`.
> Nothing had ever written the table, so no convention existed — these tests set
> it, backed by a `transactions_amount_positive` CHECK.
>
> **The seed was inconsistent and is fixed.** It set `credit_balance = 500` with
> no transaction behind it — exactly the drift the invariant exists to catch.
> It now writes a subscription and a completed `monthly_credit_grant`.
>
> The queries live in `src/database/ledger-invariants.ts`, not the test tree,
> because [`6-database-schema.md`](./6-database-schema.md) specifies a nightly
> `reconcile-balances` job asserting the same properties — one definition, two
> callers, so the tests remain evidence about the job.
>
> **CI now enforces tests**: a `pgvector/pgvector:pg16` service was added and
> `--passWithNoTests` removed, so a green build finally means something.
>
> Two constraints this places on Phase 5, both deliberate: services must accept
> `DbOrTx` and thread it (rollback isolation depends on `withTx` joining rather
> than nesting), and the `credits_paid = platform_fee + writer_payout` CHECK is
> deliberately **not** added, because it would make that invariant untestable at
> the application level.

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
- [x] Image upload — paste/drag into editor → upload to MinIO → embed URL — *ticked prematurely twice over. The transport could not have worked until **2026-08-06** (see Phase I), and paste/drag itself did not exist until **2026-08-10**: there was no `handlePaste` and no `handleDrop`, and with `allowBase64: false` the default handler produced a data URL the Image extension refused, so dropping a screenshot did nothing at all, silently.*
- [x] Thumbnail upload for article cover — *2026-08-10. The column, both DTOs, the feed card, the reader page and the OG tag had all existed since Phase 1; nothing had ever set the value.*
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
  - [x] "Insert into article" button on AI responses — *2026-08-10; required lifting the TipTap instance out of `TipTapEditor`, since the chat panel is its sibling and had no handle on the document at all*
  - [x] Token usage indicator
- [x] Inline editing popup — appears on text selection
  - [x] 5 action buttons (Reformulate / Shorten / Expand / Simplify / Improve)
  - [x] Streaming result preview
  - [x] Replace / Insert below / Cancel actions — *2026-08-10; "Reject" was renamed "Cancel", and the selection range is now captured once instead of re-read after the stream (see the close-out note)*
- [x] Token quota warning + "upgrade" prompt when tokens depleted — *2026-08-10; copy branches on plan, because a free account's allowance is 0 by design and so is permanently "depleted"*

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
- [x] Sentry integration (free tier) — backend + frontend error tracking — *2026-08-10; API, worker, Next.js server and browser. `SENTRY_DSN` is runtime config, `NEXT_PUBLIC_SENTRY_DSN` is build-time and needs the same ARG/build-arg/repository-variable treatment as the other `NEXT_PUBLIC_*`. **The code is done; creating the Sentry project and supplying the DSNs is deferred to the deploy block in Phase 6** — both are optional and the SDK no-ops without them, so nothing local is affected.*

### Exit criteria
- [x] Writer can edit with TipTap and upload images — **closed 2026-08-10**: toolbar, paste, drag, and a cover image on the publish dialog
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

**Also delivered unplanned, because Phase 3 could not be demonstrated without them:**

- [x] **Demo seed** (`pnpm db:seed`) — 5 writers / 12 published articles / a subscribed magazine / 3 readers / 12 one-off visitors / 8 tags / ~1,250 analytics events spread day by day. The dev database held 2 articles and engagement on one of them, so every dashboard would have rendered empty and the Phase 4 RAG comparison would have been untestable. The writers have deliberately non-overlapping vocabularies (tides and tackle, inference latency, zoning setbacks, koji and brine, tempo and orchestration) because Phase 4's exit criterion requires showing that retrieval *demonstrably* borrows a writer's voice — on a homogeneous corpus, retrieval is indistinguishable from no retrieval. Idempotent and non-destructive; hand-made accounts survive.
- [x] **`GET /articles/me`** — no endpoint returned a writer's own articles including drafts (the public feed filters to published + public). The dashboard needs it, and it is why the profile tabs still render placeholder arrays.

**Verification:** both repos typecheck clean under `strict: true` with zero lint errors; a 24-check integration suite passes against the live stack; the feed was confirmed rendering live API data in a real browser.

> **Cost/benefit for the report:** ~2 days of S5. The counter-argument is that it consumed schedule in the tightest sprint; the argument for is that four of the defects (dead sessions, inert rate limiting, silent AI failure, unreachable browser API) would each have been demo-stopping, and Phase 3's dashboards and Phase 5's marketplace UI now assemble from existing primitives rather than starting from raw markup.

---

## Phase I — Dev/Prod URL Topology
> Sprint S5 · 2026-08-05 → 08-06 · **Completed** (backfilled into the plan, in the same spirit as Phase D and Phase Q)

> **Why this phase exists:** it started as a workflow request — run each service in its own terminal instead of having `make dciup-dev` start them all — and as a cosmetic one: serve the stack at named hostnames rather than `localhost:8080`. Tracing what those two changes touched surfaced **six defects in how URLs were configured**, four of which made the production deploy impossible and one of which meant a feature already ticked in Phase 2 had never worked.

### Developer workflow
- [x] `web` / `api` / `worker` moved behind an **`apps` compose profile** — `make dciup-dev` now starts infrastructure only
- [x] `make dci-api` / `dci-web` / `dci-worker` — one service per terminal via `up --attach`; Ctrl+C stops only that service
- [x] `make dciup-all` preserves the previous one-command behaviour for demos; `--profile apps` threaded through `logs` / `down` / `ps`
- [x] `make` with no arguments prints a target list — the Makefile was the real workflow and the README never mentioned it

### Named hostnames
- [x] `frontend.inkwell.ai` (app) · `backend.inkwell.ai` (Swagger/curl) · `storage.inkwell.ai` (presigned uploads)
- [x] New `.infra/nginx/dev.conf`, kept separate from the production `default.conf` the two compose files had been sharing
- [x] nginx published on `127.0.0.2:80` **and** `127.0.0.1:8080` — the legacy origin stays because Google rejects `http://` redirect URIs on any host but `localhost`, and `pnpm api:codegen` hardcodes it

> **The design decision worth defending:** the browser still calls `/api` and `/storage` on the frontend's *own* origin — the extra hostnames exist for tooling, not for the app. A true three-origin split would have exercised CORS paths production never sees, broken the `sendBeacon` analytics calls (a JSON `Blob` body is not a CORS-simple request and cannot be preflighted), and required a data migration, because the relative `/storage/<bucket>/<key>` strings are already persisted in `users.avatar_url`, article covers, and inside TipTap document bodies.

> **The subtle one:** an nginx `upstream` block resolves its host at *config load*. With the app services no longer auto-starting, nginx exited at boot with `host not found in upstream`. Fixed with `resolver 127.0.0.11` plus a variable in `proxy_pass`, which defers the lookup to request time — a stopped service is now a clean 502 instead of a dead proxy.

### Defects found and fixed
- [x] **Image upload had never worked.** `presignedPutObject` builds its URL from `MINIO_ENDPOINT:MINIO_PORT`, set to `minio:9000` — resolvable only inside Docker, while the entity performing the PUT is the browser. Compounded by the bucket being created with **no policy**, so it stayed private and every object answered 403 to an unauthenticated GET: the upload would have succeeded and then no image would ever have rendered. Buckets now get anonymous `s3:GetObject`, with `s3:ListBucket` deliberately withheld so contents cannot be enumerated.
- [x] **`useSSL` was hardcoded `false`** — correct locally, but in production the endpoint is a domain behind TLS, so every presigned URL came out as `http://host:443/...`. Now driven by `MINIO_USE_SSL`.
- [x] **CI's `NEXT_PUBLIC_*` build arg was silently discarded** — the frontend `Dockerfile` declared no matching `ARG`, so every published image shipped the localhost fallback baked into its bundle.
- [x] **Production CORS rejected the real site.** `FRONTEND_URL` and `CORS_ORIGINS` were never passed to `api`, so the allow-list fell back to the schema defaults — `localhost:3000` and `localhost:3847`.
- [x] **The production worker crashed at boot** — its `ConfigModule` validation requires `JWT_SECRET`, which the production compose never passed. No scheduled job would have had a consumer.
- [x] **nginx never listened on 443** despite the compose file publishing it and mounting certificates. Added TLS termination, an HTTP→HTTPS redirect that spares the ACME challenge path, and a storage vhost — presigned URLs address `/<bucket>/<key>`, and on the apex domain that path is claimed by the Next.js catch-all.
- [x] `GOOGLE_CALLBACK_URL` was never passed in either environment, so OAuth fell back to a port nothing publishes
- [x] Backend `Dockerfile` said `EXPOSE 3001`; the app listens on 3000, and the wrong number had already been copied into nginx and both compose files

### Pulled forward from Phase 6
- [x] MinIO bucket created + **public read policy** for article images *(Phase 6 line item, closed here)*
- [x] TLS via Let's Encrypt — nginx side configured and verified; only VPS provisioning remains
- [x] Production `.env` documented — a full production override block in `.env.example`
- [x] `docker.inkwell.ai/README.md` rewritten — it had told developers to run `docker compose up --build`, which fails because no root compose file exists

**Verification:** both compose files validate; nginx boots with the app services stopped and returns 502 rather than dying; all three vhosts route correctly; a presigned upload was driven end-to-end (`presign → PUT 200 → public GET 200 image/png`) with bucket listing still 403; SSE confirmed unbuffered (`text/event-stream`, chunked); the production config was run against the live containers on a spare loopback address with a self-signed certificate and served the redirect, both vhosts and the ACME path correctly; backend typecheck, lint and 27/27 tests pass.

> **Cost/benefit for the report:** ~1.5 days of S5. This is the second time a "configuration" task has turned up demo-stopping defects (see Phase Q), and the pattern is the same both times: values that were *present* but never *exercised*. Nothing here was caught by tests or CI, because every one of them lives in the gap between the container and the browser — the one boundary neither unit tests nor typechecking cross.

---

## Phase 3 — Social + Analytics
> Sprints S5–S6 · Jul 27 – Aug 23 *(re-dated from Jun 26–Jul 9; likes/comments/notifications land in S5, aggregation + dashboards in S6)*

### Social (Backend)
- [x] Likes module — POST /articles/:id/like, DELETE /articles/:id/like
- [x] Comments module — POST/GET/DELETE for threaded comments
- [x] Follows module — POST /users/:username/follow, DELETE unfollow *(stretch — first social cut under time pressure)*
- [x] Reposts module — POST /articles/:id/repost — *2026-08-10. The `reposts` table and its unique constraint had existed since Phase 1, and the aggregation worker had been counting it into `article_metrics.total_reposts` and `writer_quality_metrics.repost_rate` the whole time. Nothing ever wrote a row, which is why `repostRate` on the evaluation report was structurally 0. No aggregation change was needed — only a writer.*
- [x] Notifications module:
  - [x] Create notification on like / comment / follow events
  - [x] GET /notifications (paginated list)
  - [x] PATCH /notifications/:id/read
  - [x] SSE endpoint GET /notifications/stream — live delivery

### Analytics (Backend) — Aggregation + Dashboards
> Note: event ingestion endpoint and frontend capture moved to Phase 2 (early data accrual).
- [x] BullMQ worker `aggregate-article-metrics` (every 5 min) → `article_metrics`
- [x] BullMQ worker `aggregate-writer-audience` (every 15 min) → `writer_audience_metrics`
- [x] BullMQ worker `aggregate-writer-content` (every 15 min) → `writer_content_metrics`
- [x] BullMQ worker `aggregate-writer-quality` (every 15 min) → `writer_quality_metrics`
- [x] GET /articles/:id/analytics — writer-only endpoint (self-improvement)
- [x] GET /writers/:username/evaluation — magazine-only endpoint (decision support)

> **Deviation — 4 workers shipped as 2 scheduled jobs.** The three writer rollups must run as a unit and in order: quality reads `article_metrics`, so it has to follow the article rollup. Four independently scheduled crons would let quality compute against a stale snapshot whenever the schedules drifted. They run as `aggregate-article-metrics` (\*/5) and `aggregate-writer-metrics` (:02/:17/:32/:47, offset so it lands just after an article rollup). All four rollups exist and populate all four tables; only the scheduling is grouped.
>
> **Three metric columns are written NULL, permanently until capture changes:** `article_metrics.paragraph_dropoff`, `writer_audience_metrics.top_countries` and `.device_split`. No client-side source exists for any of them. They are NULL rather than zero so a magazine can tell "not measured" from "measured, and none".
>
> **Blocker found and fixed:** the worker container had never run `worker.ts` — `nest start --watch -- --entryFile worker` passes the flag to the app, not the CLI, so it booted a second copy of the API. No BullMQ worker had ever run in this stack. The same class of bug existed in the production compose (`node dist/worker`) and the Dockerfile (`node dist/main`), where nest emits to `dist/src/` — meaning **the production image could never have started**. All fixed.
  - Combines audience + content + quality rollups in one response
  - Returns 403 if requester is not a magazine

### Social (Frontend)
- [x] Like button with optimistic UI
- [x] Comment section under articles — threaded replies
- [x] Follow button on profile pages — one shared `<FollowButton>` (handles self / logged-out / pending), replacing three disabled `TODO(Phase 3)` stubs. Delivered early by the quality pass; see the Tier 0–2 note below.
- [x] Repost button — *2026-08-10; optimistic count, sharing `useOptimisticToggle` with the like button*
- [x] Notification bell — live SSE connection, unread count badge
- [x] Notification dropdown list

### Analytics (Frontend) — Dashboards
> Note: frontend event capture moved to Phase 2 (early data accrual).
- [x] Writer analytics dashboard (`/dashboard`) — master/detail: your articles (drafts included) with the selected article's report
  - [x] Views per article (chart) — 30-day daily area chart with crosshair + tooltip
  - [x] Avg read time
  - [ ] ~~Scroll depth heatmap (bar chart per paragraph)~~ — **not built as specified.** The client records one page-level max-scroll percentage on leave, not per-paragraph `IntersectionObserver` entries, so there is no per-paragraph signal to chart. A quartile **retention curve** ships instead (share of readers reaching 25/50/75/90%), which is what page-level scroll honestly supports. Restoring the heatmap needs a capture change first, and it cannot be backfilled.
  - [x] Top performing articles — **2026-08-10**. The list had no performance data at all to rank by: `findByAuthor` selected only authoring fields, and sorted by `updatedAt` hardcoded. `article_metrics` is now LEFT JOINed (a PK lookup per row, so no N+1) and `GET /articles/me` accepts `?sort=recent|views|engagement`. Ranking is server-side so it covers the whole body of work rather than reordering the current page.

### Analytics (Frontend) — Magazine-Facing
- [x] Writer evaluation page — built at **`/discover/writers/[username]`**, not `?as=magazine`. A query parameter would make one public URL render entirely different, access-controlled content depending on the viewer. `/discover` is now behind the auth middleware; the account-type check stays server-side.
  - [x] **Audience panel**: unique readers, returning rate — *geo distribution and device split render as explicit "not collected" notes; neither has a capture source*
  - [x] **Content panel**: topic distribution, consistency, avg length, top tags — *posting frequency is a scalar stat, not a sparkline: no per-period series is stored*
  - [x] **Quality panel**: engagement rate, completion rate, repost rate, comment depth, retention curve — *repost rate is structurally 0 until the Reposts module ships*
  - [x] **Portfolio Insights panel** — present as a **stated placeholder**, not the AI implementation. Phase 4 swaps in the cached result; it deliberately shows neither a spinner nor invented prose.
- [x] Magazine discover page (`/discover`) — browse writers with filters. **Built 2026-08-10**, together with its backing endpoint `GET /discover/writers` (pulled forward from Phase 5). Search across name/username/bio, topic filter, four sorts, and an eligibility toggle. It is the entrance to the evaluation report, which until now was reachable only by typing a URL.

### Exit criteria
- [x] Like/comment/follow/repost all work with correct notifications — **closed 2026-08-10** with the Reposts module; three POSTs produce exactly one row and exactly one notification
- [x] Live notification arrives via SSE without page refresh
- [x] Writer dashboard shows real engagement data — verified in a browser against the seeded corpus
- [x] Magazine can browse writers and view writer evaluation dashboard with real metrics — **closed 2026-08-10**. Endpoint verified end to end: magazine 200 / personal 403 / anonymous 401, all four sorts distinct, case-insensitive search, tag filter, and stable pagination (two 13-row pages → 26 distinct writers, none repeated or dropped)

---

## S5 Close-out — the trailing items
> Sprint S5 → S6 boundary · 2026-08-10 · **Completed** (recorded in the same spirit as Phases D, Q and I)

> **Why this exists:** S5 absorbed two unplanned sub-phases (Q, then I) and they consumed the slack. What was left over was not a coherent feature but six individually small items — and between them they held **four written exit criteria** open across Phases 2 and 3. They were closed in one pass on the first day of S6 so Phase 4 opens with nothing trailing.

| Item | Phase it closed |
|---|---|
| Magazine discover page + `GET /discover/writers` | Phase 3 exit criterion |
| Article cover image, and paste/drag upload | Phase 2 exit criterion |
| AI "Insert into article", inline Replace / Insert below / Cancel, token-quota state | Phase 2 |
| Top-performing ranking on the writer dashboard | Phase 3 |
| Reposts module + button | Phase 3 exit criterion |
| Sentry (API, worker, Next server, browser) | Phase 2 observability |

### Defects found while closing them

Same pattern as Phases Q and I: the surfaces looked finished, and the gaps were all in code paths nothing exercised.

- **The inline AI popup could edit the wrong text.** `handleAction` and `handleAccept` each read `editor.state.selection` independently, with a multi-second stream between them. Any click, blur or bubble-menu reposition in that window moved the selection, so "Replace" deleted a different range than the one the writer had selected — silently, and destructively. The range is now captured once.
- **The AI token balance never moved.** `qk.ai.tokens()` was invalidated by nothing, anywhere. The indicator showed whatever the balance was when the panel first mounted and held that number for the entire session no matter how many tokens were spent.
- **Paste and drag had never been implemented**, despite being ticked — see the Phase 2 note above.
- **The dashboard's article list carried no metrics at all**, so "Top performing articles" had nothing to rank.
- **`notification_type` had no `'repost'` value**, so the Reposts module needed the close-out's only schema change: `ALTER TYPE ... ADD VALUE`, additive and non-rewriting.
- **`.pnpm-store/` was root-owned in both app repos** — a survivor of the root-container era that Phase Q fixed for `dist/` and `.next/` but missed here. Since the containers switched to the host UID, `pnpm install` had been failing on every `api` start with an opaque SQLite "attempt to write a readonly database". It went unnoticed because `node_modules` was already populated in its named volume, so nothing broke until a new dependency was added — at which point the container could not install it.
- **A pnpm placeholder stopped the web container booting.** Installing `@sentry/nextjs` made pnpm write `'@sentry/cli': set this to true or false` into `pnpm-workspace.yaml`. pnpm exits **non-zero** on an unresolved entry, and the dev container runs `pnpm install && pnpm dev`, so the `&&` short-circuited and the dev server never started.

### Deliberate deviations, recorded rather than silently resolved

- **`/discover` is not subscription-gated.** Spec §4.5.3 requires an active magazine subscription; the subscription module is Phase 5, so the gate is account-type only for now.
- **The credit-balance pill** from `design/prompts/08-marketplace-browse.md` is not built — it reads `magazine_profiles.credit_balance`, which Phase 5 owns.
- **Eligibility defaults to on, with a toggle.** §4.5.3 says "browse all eligible writers", but `check-writer-eligibility` is a Phase 5 worker, so the flag is seed-only today and a strict filter renders an empty page on any database where the seed has not run.
- **The upgrade CTA is a disabled button.** `ROUTES` has no billing entry and the upgrade flow is Phase 5; a live button would be a dead link. Matches the article paywall, which made the same call.
- **Route naming drift is resolved toward `/discover`.** `9-design.md` and design prompt 08 called this page `/marketplace`; the code uses `/discover`, because the evaluation report already lives at `/discover/writers/[username]`. `/marketplace` is left to Phase 5's *article* browse (`GET /discover/marketplace`).

**Verification:** both repos typecheck clean under `strict: true` with zero lint errors; backend 27/27 tests pass on the host; both compose files validate; the full stack (api + web + worker + infra) runs. The repost chain was driven end to end — button → row → `aggregate-article-metrics` → `aggregate-writer-metrics` → `repostRate` on the evaluation report moving from a structural 0 to 0.0076 — and the Sentry filter ordering was checked to confirm it had not swallowed the database exception filter (400 / 400 / 404 / 401 / 403, no 500s).

---

## Phase 4 — RAG (Headline Differentiator)
> Sprint S6 · Aug 10 – Aug 23 *(re-dated from Jul 10–23)*

### RAG Pipeline (Backend)
- [x] Embedding SDK + pgvector Drizzle helpers — *2026-08-10; `@ai-sdk/google` (already installed) plus Drizzle's first-party `vector` column, `cosineDistance`, and an HNSW index*
- [x] Article chunking on publish:
  - [x] Split TipTap JSON into paragraph-level chunks — *`chunking.ts`, 120–1200 chars with heading prefixing and sentence-boundary splitting; 22 tests. Paragraph-level alone was too fine: single-sentence paragraphs embed to noise.*
  - [x] Each chunk embedded via Gemini `gemini-embedding-001` at 1536 dims — *provider substituted for OpenAI, see the S6 note*
  - [x] Stored in `article_chunks` with `embedding vector(1536)` + HNSW index
  - [x] BullMQ job: `embed-article` triggered on publish/update — *plus `remove-article-chunks` on unpublish/delete, which the checklist never named but the corpus is wrong without*
- [x] Retrieval service:
  - [x] `findSimilarChunks(authorId, queryEmbedding, topK)` — cosine similarity with pgvector `<=>` operator
  - [x] Filter by author for writer-facing RAG (writer's own corpus only)
  - [x] No author filter for cross-corpus search (Phase 4.4 search)
- [x] Prompt template update — inject top-K retrieved chunks as context — *labelled distinctly from the current draft, because conflating them made the model "continue" text the writer never wrote here*

### Writer-Facing RAG (Use Case #1)
- [x] POST /ai/chat — enhanced with RAG retrieval from the user's own articles — *article lookup is scoped by `authorId`; it was not, which let any writer pass another's `articleId` and read it*
- [x] GET /ai/retrieval-debug — returns chunks used in last request (for demo/transparency) — *scoped to the caller, since the response contains article text*

### Magazine-Facing RAG — Portfolio Insights (Use Case #2)
- [x] POST /ai/portfolio-insights/:username — *`:username`, not `:writerUsername`*
  - [x] Auth guard: only magazine accounts can call — *one `@UseGuards` in execution order; two decorators do not compose, and the second silently replaced the first*
  - [x] Retrieves representative chunks from writer's full corpus — *window function, capped per article so a prolific piece cannot dominate the sample*
  - [x] Builds structured prompt (voice / topics / consistency / fit / strengths-gaps)
  - [x] LLM call with Zod-validated structured output — *Groq `openai/gpt-oss-120b`; `llama-3.3-70b-versatile` rejects the `json_schema` response format*
  - [x] Caches result in `portfolio_insights` table for 24h
  - [x] Invalidation: cache deleted when writer publishes a new article — *in `embed-article.service.ts`, so the cache is dropped by the same job that re-indexes the corpus the report was based on*
- [x] GET /writers/:username/portfolio-insights — returns cached, never generates — *on `reports.controller.ts`. It deliberately does NOT trigger generation as the checklist proposed: a magazine opening an evaluation page would then silently spend a model call per writer browsed.*
- [x] Frontend: Portfolio Insights panel on writer evaluation page — **2026-08-11**, at `/discover/writers/[username]` (not `?as=magazine`; see the Phase 3 note on why that route was chosen)
  - [x] Loading state during async generation
  - [x] Cached result rendered with last-updated timestamp — *plus how many articles it read, so the basis of the assessment is visible*
  - [x] Generation is an explicit action, not a page-load side effect — *the report costs a model call, so browsing writers must not spend a magazine's budget*
  - [x] The score is labelled **voice consistency**, never "score" — *it measures how recognisable the writing is across pieces, not how good it is; a consistently plain writer scores high, and reading it as a quality mark would be exactly wrong*

### Search
- [x] Postgres full-text search — `tsvector` on `articles.title + content + excerpt` — *a GENERATED ALWAYS AS ... STORED column with weights A/B/C plus a GIN index, added 2026-08-10. A title match ranks ~4× a body mention of the same word.*
- [x] GET /search?q= — hybrid: full-text + semantic search — **2026-08-11**
  - [x] Lexical results via `ts_rank` on `tsvector` — *`websearch_to_tsquery`, not `to_tsquery`, which raises a syntax error on a stray operator and would turn a user's typo into a 500*
  - [x] Semantic results via pgvector cosine similarity (`<=>`) on query embedding — *grouped to the best-scoring chunk per article, so a long article cannot occupy the result list purely for having more chunks*
  - [x] **Reciprocal Rank Fusion (RRF)** to merge both result sets: `score = Σ 1/(k + rank_i)` with k=60 — *in `SearchService`, not SQL. RRF scores by POSITION in each ranking, which needs two independently ordered result sets; one query produces one ordering. `ts_rank` and cosine similarity are also unrelated scales, so ranks are the only common currency.*
- [x] Frontend: search bar in navbar → search results page — *the navbar box was inert (no state, no form, no handler) and `/search` was a 10-line stub*
- [x] **Writers included alongside articles** — *beyond `2-features.md` §2.7, which specifies articles only. Restricted to writers with at least one published public article, because this endpoint is public unlike the magazine-only `/discover`.*
- [x] `?tag=` browse — *fixes four links that had always pointed at `/search?tag=<slug>` from the sidebar, the mobile drawer and trending topics, and landed on the stub*

> **Fusion is measurably doing work**, which is the claim worth defending:
>
> ```
> "tackle"                               2 lexical + 3 semantic → 3 fused
> "how do I stop my ferments going bad"  0 lexical + 2 semantic → 2 fused
> "reading the water before you cast"    1 lexical + 3 semantic → 3 fused
> ```
>
> The middle line is the case that justifies the pipeline: **no article contains
> the searcher's words**, and the correct results still come back. The first line
> is the converse — an exact title match that pure semantic ranking would not
> reliably put first.
>
> **`ts_headline` highlighting was deliberately skipped.** It only helps the
> lexical half — a semantic match often shares no words with the query, so there
> is nothing to mark — and it would mean rendering database-derived HTML, which
> would be this codebase's first `dangerouslySetInnerHTML` and first XSS surface.
>
> **The semantic floor is 0.60, the same as chat's.** It was set to 0.55 first,
> reasoning that search tolerates looser matches than prompt injection. That was
> wrong: 0.55 sits inside the measured off-topic band (0.48–0.58), so searching a
> surname scored 0.586 against an unrelated article and ranked it first. There is
> no weaker-but-genuine zone below 0.60 for this model.

### Frontend
- [x] Search bar in navbar → search results page — *see the Search section above*
- [x] "Sources used" expandable section below AI responses — **2026-08-11**; grouped by article, not by chunk, because two passages from one piece are one source used twice. Shows each article's closest similarity and the passages themselves, so the RAG claim is checkable rather than asserted.
- [x] RAG demo notice in writer chat — **2026-08-11**, worded *"Drawing on N published articles of yours"*, **not** the specified *"AI trained on your X published articles"*. See the deviation note below.
- [x] Portfolio Insights panel renders structured report — *see the Portfolio Insights section above*

> **The notice does not say "trained", and the difference is not cosmetic.**
> Nothing here is trained: the articles are embedded and retrieved at query
> time, and the model's weights never change. Shipping "trained" would claim
> fine-tuning this project does not do — in front of an examiner who may well
> ask how the fine-tuning was done. Retrieval is also the better answer, because
> an article published a minute ago is usable immediately, which no training run
> would give you.
>
> **Sources are held per assistant message, not as one "latest" value.** The
> server keeps only the caller's most recent retrieval, so a single shared value
> would relabel every earlier reply in the conversation with the newest
> retrieval — evidence attached to the wrong answer, which is worse than no
> evidence at all.

### AI Memory (spec §9.3.1 — was in no phase checklist until 2026-08-11)
- [x] `extract-writer-memory` BullMQ job — *chained after `embed-article` rather than enqueued alongside it, because it reads the chunks that step writes; in parallel it would race and lose on a writer's first publish*
- [x] Structured tone / style / vocabulary / topics extracted via Zod-validated output into `user_ai_memory` — *a table that had existed since Phase 1 with nothing ever writing to it*
- [x] Injected into writer chat as a compact block — *complementary to RAG, not redundant: the profile is a stable persona that holds when retrieval finds nothing, the passages are evidence relevant to the current question*

### Exit criteria
> **All six verified 2026-08-15** against the running stack with real Gemini
> embeddings and Groq completions. Full record with figures:
> [`review-test/phase-4-exit-verification.md`](./review-test/phase-4-exit-verification.md).

- [x] Publish 5+ articles with distinct topics/vocabulary — *5 seed writers, 13 articles, non-overlapping vocabularies, all embedded. The planned `db:embed-backfill` turned out to be unnecessary: 0 published non-deleted articles lacked chunks; the apparent gap was a query that did not filter `deleted_at`.*
- [x] **Writer demo**: AI chat generates a new article that demonstrably uses retrieved vocabulary and style — *asked `imane-farouk` for an opening on parking minimums, a topic she has never written about; the reply re-applies her setback argument ("the edge of the street… empty expanses of asphalt") to it. The argument transferred, not just the keywords.*
- [x] **Magazine demo**: Magazine views a writer's profile → Portfolio Insights panel shows AI-generated voice/topics/score/fit — *this produced the **first `portfolio_insights` row the table has ever held**; generation is an explicit click by design, so the panel had never rendered a populated report since shipping on 2026-08-11. Voice, 5 topics, 85/100 consistency, 5 commission ideas, strengths-and-gaps all render. Now covered by `e2e/17-phase4-portfolio-insights.spec.ts`.*
- [x] `/ai/retrieval-debug` shows correct chunk IDs pulled from the user's articles — *5 chunks, top similarity 0.668; cross-checked by ID against the database: 5 of 5 exist, **0 belong to anyone else**.*
- [x] Search returns relevant results for both keyword and semantic queries — *the three recorded fusion cases reproduce exactly, including `0 lexical + 2 semantic` on a query whose words appear in no article.*
- [x] Cache invalidation works (publish a new article → next insights request regenerates) — *cache dropped and the new article re-indexed within 3s; the cached read returns `{"insights": null}` rather than stale data; regeneration went `basedOnArticles` 3 → 4 and its topics now include "curb cut design" from the article published seconds earlier.*

---

## Phase 5 — Marketplace + Premium + Moderation
> Sprint S7 · Aug 24 – Sep 6 *(re-dated from Jul 24–Aug 6; voice, email, AI eval harness and the mobile go/no-go moved to Post-MVP Descope)*
>
> **Built 2026-08-13/14.** Backend `819726f`, frontend `7be2873`, both merged to
> `main` with CI green. 479 backend tests pass. The whole phase was built against
> schema that has existed since Phase 1's marketplace pivot — `article_purchases`,
> `transactions`, `magazine_subscriptions`, `writer_eligibility_audit_log` and
> `reports` all existed with **zero write sites** — so this was services, routes
> and UI rather than migrations. The one schema change is noted below.

### Premium + Subscription
- [x] Backend subscription simulation:
  - [x] POST /subscriptions/upgrade — sets `user.plan = premium`
  - [x] POST /subscriptions/downgrade
  - [ ] Token top-up endpoint (simulated purchase) — **not built. Design decided 2026-08-15; deliberately not implemented.** `dailyAllowanceSql` rewrites `ai_tokens_remaining` to a fixed per-plan allowance every UTC day, so topped-up tokens would be erased at midnight. Magazine CREDIT top-up is built and is a different thing.

    > **The decision: a separate non-resetting column, not a change to the reset rule.**
    >
    > The two candidates were weighed against the three sites that write `ai_tokens_remaining` — the nightly `ResetTokensProcessor`, the lazy grant in `readQuotaGrantingIfDue`, and the spend in `ai.service.ts`.
    >
    > **Changing the reset rule cannot be made correct.** `SET remaining = GREATEST(remaining, allowance)` loses purchased tokens the moment the user spends below the allowance: buy 500 on top of 1,000, spend 1,200, and the 300 left is entirely purchased — the next reset replaces it with 1,000 rather than adding to it, and 300 paid-for tokens vanish. `SET remaining = remaining + allowance` is worse: unspent daily tokens accumulate without bound, so a premium account that never uses AI banks ~30,000 a month and "daily allowance" stops meaning anything.
    >
    > The reason is structural, not a matter of picking a better expression: **a single integer cannot distinguish "granted today, expires tonight" from "bought, never expires".** Any rule over one column has to guess which kind of token it is holding, and both guesses cost someone something — the first costs the user what they paid for, which is the exact failure this item was flagged for in the first place.
    >
    > **The shape to build**, when it is built: an `ai_tokens_purchased` column that no reset ever touches. The nightly job and the lazy grant keep writing `ai_tokens_remaining` and are left completely unchanged. The spend drains the expiring bucket first and the purchased reserve only on overflow — which is also the fair order, since it spends what expires before what does not:
    >
    > ```sql
    > SET ai_tokens_remaining = GREATEST(0, ai_tokens_remaining - :used),
    >     ai_tokens_purchased = GREATEST(0, ai_tokens_purchased - GREATEST(0, :used - ai_tokens_remaining))
    > ```
    >
    > Both right-hand sides see the pre-update row, so the overflow term reads the old `ai_tokens_remaining` — which is what makes this a single atomic statement rather than a read-then-write race. `getTokenCount` returns the sum, and `useAiQuota`'s `exhausted` becomes sum ≤ 0.
    >
    > **One product question to settle before building it:** a free account's allowance is 0 *by design*. If a free user can buy tokens, the top-up becomes a way to buy AI without buying premium, which quietly undoes the plan gate. The top-up should almost certainly be premium-only, but that is a pricing decision rather than an engineering one.
- [x] Frontend upgrade flow:
  - [x] Upgrade page — `/subscription`, one route serving both account types (magazine subscription + credits, or the personal plan switch)
  - [x] Plan comparison — *2026-08-15. A three-row table on `/subscription`, with the current plan's column marked. Deliberately three rows: exactly two things in the codebase branch on `plan === 'premium'` — the access gate in `article-access.ts` and `dailyAllowanceSql` — so anything further would be marketing copy dressed as a feature table. **Marketplace listing is explicitly called out as NOT included**, because it is gated on `isMarketplaceEligible` (earned through readership, granted by an admin) and a writer upgrading in order to sell would otherwise have bought the wrong thing. Note the stale comment in `types/index.ts` claiming premium is required to list; it is not.*
  - [x] Payment mock — a button that confirms, with the simulation stated on the page rather than implied
  - [x] Premium badge on profile — *2026-08-15. **This was not frontend-only, contrary to the earlier read of it:** `plan` was absent from `findByUsername`, the public profile query, and only present on `findById` (`/users/me`). Adding it means `GET /u/:username` — unauthenticated — now tells any anonymous caller whether a given person pays us. That is a billing fact about a person, published to strangers; it was a deliberate product decision, taken 2026-08-15, and `test/users/public-profile.spec.ts` pins the exposed field list so widening it later has to be done on purpose. Nothing else was added: not the renewal date, not `aiTokensRemaining`, not the email. The badge renders for premium only — a "Free" counterpart would label most of the platform with what they have not bought, on a page they do not control.*

### Marketplace — Subscription + Preview/Purchase Transactions
- [x] Backend subscription module:
  - [x] POST /subscriptions/magazine — activate magazine subscription (simulated payment, sets subscription_status + initial credit_balance)
  - [x] BullMQ cron job `renew-magazine-subscriptions` — monthly credit grant + renewal row insert
  - [x] POST /credits/topup — optional extra credits for magazines (simulated)
  - [x] Subscription guard middleware — 403 if magazine subscription inactive on marketplace endpoints
- [x] Backend marketplace module:
  - [x] Writer eligibility BullMQ worker `check-writer-eligibility` — runs on a 20-minute schedule, flips eligible writers
  - [x] GET /discover/writers — magazine-only writer browse with filters/sort — **pulled forward to 2026-08-10**. The subscription gate landed in Phase 5 as planned.
  - [x] GET /discover/marketplace — magazine-only browse of marketplace-listed articles
  - [x] POST /purchases/preview — preview unlock (atomic DB transaction):
    - [x] Validates `subscription_status = active` + `credit_balance >= preview_price`
    - [x] Debits magazine `credit_balance`
    - [x] Credits writer `earnings_balance` (preview_price - platform_fee)
    - [x] Inserts `article_purchases` row (`stage = preview_unlock`)
    - [x] Inserts transaction rows (preview_unlock + writer_payout + platform_fee — see deviations)
    - [x] Idempotency key prevents double-charge
  - [x] POST /purchases/buy — full purchase (atomic DB transaction):
    - [x] Looks up prior preview row for (article_id, magazine_id)
    - [x] Validates credit_balance >= remaining amount (price - preview_paid)
    - [x] Debits magazine, credits writer, inserts full_purchase row with parent_purchase_id
    - [x] Idempotency key
  - [x] GET /magazines/me/library — magazine's fully purchased articles
  - [x] GET /me/earnings — writer's earnings summary (preview payouts + purchase payouts)
  - [x] Admin: POST /admin/eligibility/:writerId — grant eligibility manually + audit log entry
- [x] Notifications:
  - [x] Writer notified when article previewed by a magazine
  - [x] Writer notified when article purchased by a magazine
  - [x] Writer notified when earnings credited
- [x] Frontend marketplace UI:
  - [x] Marketplace placement option + price input in publish flow (enabled per writer from the live eligibility check, with progress bars when locked)
  - [x] Magazine subscription screen (sign-up wall and settings)
  - [x] Magazine Discover page with writer cards + filters — **built 2026-08-10**; the subscription gate and credit-balance indicator landed in Phase 5
  - [x] Writer evaluation page: marketplace article list with "Preview" / "Purchase" buttons — *2026-08-15. An "Available to license" panel, full width below the metrics: the panels above are what the decision is made ON, this is where it is acted on. Frontend only — `GET /discover/marketplace?writer=` already existed for exactly this and nothing was calling it. Reuses `MarketplaceCard` and `PurchaseDialog` rather than reimplementing them, so the two screens cannot drift apart on what an article costs; every price still comes from the server. The empty state distinguishes "has not listed anything" from "not eligible to list", which look identical otherwise. Covered by `e2e/18-evaluation-marketplace-panel.spec.ts`.*
  - [x] Preview confirmation modal (shows 10% cost + credit balance)
  - [x] Purchase confirmation modal (shows remaining 90% + credit balance + preview-credit note)
  - [x] Magazine library page (fully purchased articles)
  - [x] Writer earnings dashboard (preview + purchase transactions itemized)
  - [x] Magazine credit balance display + top-up flow
  - [x] Writer eligibility progress bar on dashboard
  - [x] Admin: eligibility grant UI in admin panel — **built 2026-08-14.** Username lookup through `GET /u/:username`, which already returns the id and the current flag, then the grant. Sits above the report queue; refuses magazines and already-eligible writers before the click.

### Moderation
- [x] Reports module — POST /reports (article, user or comment), admin GET /admin/reports
- [x] Admin panel (`/admin`):
  - [x] Reports queue with target preview, status filters, and the report's own audit trail
  - [x] Actions: dismiss / delete article / ban user (soft delete)
  - [x] User management table with role/plan editing — *2026-08-15. New `GET /admin/users` (paginated, searchable on username/name/email, filterable by role and by active/banned) and `PATCH /admin/users/:id`. Banned accounts are visible on request: they are soft-deleted and so excluded from every other read path, but reviewing a ban after the fact is the part of moderation most worth being able to do.*

    > **The escalation boundary, decided 2026-08-15.** `admin` is **not an assignable role**, and an existing admin's role is **not editable**, in either direction. There is no super-admin tier in this system, and `banUser` already refuses outright with *"Administrators cannot be banned"* — so an admin able to grant `admin` means one compromised session can create an account with full rights that the product offers no way to remove. Promotion to admin stays a deliberate act against the database. Blocking demotion too is the same boundary crossed the other way: an admin who cannot be created through the UI must not be removable through it either.
    >
    > Three further refusals, all server-side: you cannot edit **your own** role or plan (demoting yourself locks you out of the page you are standing on, with no UI to undo it); you cannot edit a **banned** account (it cannot log in, so the edit changes nothing observable while implying it did); and you cannot give a **magazine** a role (`users.role` is NULL there by design — capability comes from `accountType`).
    >
    > Plan editing **is** allowed both ways, and is logged at warn alongside bans and eligibility grants. Payments are simulated in this release, so granting premium costs nothing — which is exactly why it should leave a trace.
    >
    > The UI declines to render controls for edits the API would refuse, rather than offering a dropdown that always errors. The server is the gate; `test/moderation/admin-users.spec.ts` (11 tests) pins every refusal above.
- [x] Content moderation on article publish: auto-flag violating content — **Groq, not OpenAI.** The chain prefers OpenAI's `/v1/moderations` when `OPENAI_API_KEY` is set and falls back to Groq; there is no OpenAI key on this project (no international card), so it runs on Groq in practice. A flag writes a `pending` report and the article publishes regardless.

### Exit criteria
- [x] Upgrade flow changes user plan and unlocks premium articles + AI features — *browser walkthrough run 2026-08-15 ([record](./review-test/phase-5-exit-verification.md)). **Premium articles** pass: a new free account is shown the paywall, and after upgrading and re-authenticating the same account receives the same article's body. The re-authentication is not a workaround — the plan is a claim inside the access token, and `/subscription` says so.*

    > **The AI half failed first, and was fixed rather than caveated.** A freshly-upgraded premium account had **no AI access at all** until midnight UTC. `AiQuotaGuard` granted the allowance on demand but ran only on `/ai/chat` and `/ai/inline`, while `GET /ai/tokens` was a plain `SELECT` of a column that defaults to 0. The client derives `exhausted` from that read and disables the composer — so the user could not issue the request that would have granted their tokens. Measured: `GET /ai/tokens` → 0, one `POST /ai/chat` → guard grants 1000 and spends 218, `GET /ai/tokens` → 782.
    >
    > This is precisely the 24-hour wait the guard's own comment says the lazy grant exists to eliminate; the protection had been applied to the paths that *spend* the quota but not to the one that *reports* it. The grant statement moved to `readQuotaGrantingIfDue` in `ai-token-allowance.ts` and both callers now share it. Verified on a fresh account: free → 0 (by design), premium with no prior AI request → **1000**.*
- [x] Reported content appears in admin queue — *browser walkthrough run 2026-08-15: `12-flow-moderation`, 5 steps green — report filed, reaches the queue, dismissed, article removed, author banned. The suspension message shows on login while the enumeration guard holds: the same banned account with a wrong password still returns a generic 401.*
- [x] **Marketplace end-to-end demo**: Admin grants eligibility to demo writer → Writer publishes article to marketplace → Magazine (with active subscription) browses → views writer evaluation + Portfolio Insights → previews article (credits debited 10%) → purchases full (credits debited remaining 90%) → article appears in magazine library → writer earnings reflect both the preview payout and the purchase payout — *verified end to end in a browser 2026-08-15. Steps 1,2,3,5,6,7,8 by `11-flow-marketplace` (6 tests); step 4 — the evaluation and Portfolio Insights view — by `22-phase5-marketplace-demo`, which also completes the purchase FROM the evaluation page, the first time credits have been spent through the licensing panel. Charged 445→435 (preview, 10% of 100) then 435→345 (remainder 90); ledger rows: preview 10 = 8 payout + 2 fee, purchase 90 = 72 payout + 18 fee. The note about step 1 needing the admin grant UI was stale — that UI already existed.*

> ### Deviations and findings, Phase 5
>
> **Three transaction rows per purchase, not two.** `6-database-schema.md`:572
> describes two. The `platform_fee` enum value exists and
> `ledger-invariants.ts`:107 already documents such a row's shape ("null on both
> user sides"), so the two-row reading leaves an enum member permanently dead and
> platform revenue unqueryable. The third row is invisible to both balance
> invariants, so it adds information without moving any balance.
>
> **Eligibility could not read the rollups.** §4.5.2 requires *lifetime* unique
> readers and reactions. `writer_audience_metrics.total_unique_readers` is a
> 30-day window (`aggregation.service.ts`:189), so a writer could cross the line
> and later fall back under it — contradicting "once reached, it stays unlocked
> permanently" — and no table holds a lifetime reaction count at all. Both are
> computed from `analytics_events` and the social tables instead. Consequence
> worth knowing: anonymous views carry `viewer_id IS NULL` and cannot count
> toward a DISTINCT tally of people, so the threshold is 5,000 *identified*
> readers. The seeded corpus reaches 11.
>
> **`GET /articles/:slug` was serving every article's body to anyone.** No
> authentication, no status check, no placement check. Marketplace articles were
> readable without paying, the Phase 3 premium paywall existed only in the
> browser, and unpublished drafts were readable by slug. The §7.4 matrix is now
> applied server-side and `content` arrives null when locked. **One row of that
> matrix is deliberately not implemented**: §7.4 also reads as requiring an
> account to see a free public article's body. That would change the reading
> experience of the whole product and contradicts the public feed and the Phase 6
> SEO work, so free public articles remain readable by guests.
>
> **A ban did not ban.** `deleted_at` was checked in exactly one place —
> `refresh()`. Neither `login()` nor the Google path looked at it, so a banned
> user could sign in again and a self-deleted account was never locked out.
> Fixed. A ban still takes effect at the next authentication rather than
> instantly: `JwtStrategy` does not re-read the database, so an issued access
> token stays valid for the rest of its 15 minutes.
>
> **`reports.reporter_id` widened to nullable** — the one schema change in this
> phase. It was NOT NULL, which made the automatic publish-time flag
> unrepresentable: a classifier is not a user, and naming the author or an
> arbitrary admin would have been false. NULL means the platform filed it. The
> queue's join on `users` had to become a LEFT join in the same change; an inner
> join silently dropped exactly the automatic flags nobody is watching for.
>
> **`magazine_profiles.subscription_status` is `varchar(20)`** while a real
> `subscription_status` pgEnum exists and is used by
> `magazine_subscriptions.status`. Two spellings of one concept. DTOs are typed
> to the enum's values so the application cannot write a third; converting the
> column deserves its own change.
>
> **The eligibility sweep was a performance defect as first written.** It
> examined every personal account — one query per registered user, every twenty
> minutes. A writer with no published public article is provably at zero on both
> counts, so excluding them changes no outcome; the test suite went from 22
> minutes to 15 seconds.
>
> **The seed had no admin account**, which made this phase's own exit criterion
> ("admin grants eligibility") impossible to demonstrate on a fresh database.
> Added, along with the audit rows behind the seeded grants — which previously
> claimed `admin_grant` with an empty audit log and no admin who could have made
> the decision.

**Verification:** 479 backend tests pass, including a price sweep over every
value from 1 to 300 (both stages and both splits reconcile exactly) and ledger
invariant checks after every money-moving spec. `tsc --noEmit` and
`eslint --max-warnings=0` clean in both repos; the frontend builds with **empty**
`NEXT_PUBLIC_*`. The full marketplace flow, the three scheduled jobs, the
moderation queue and the publish-time classifier were each driven against the
running stack — `reconcile-balances` reports the dev ledger consistent. **No
Phase 5 screen has been looked at in a browser.**

---

## Phase 6 — Polish, Deploy & Defense Prep
> Sprint S7 (parallel with Phase 5) · Aug 24 – defense · *(re-dated from Aug 7–end of August)*

### Quality
- [x] Playwright E2E tests — cover all critical flows: *all five verified 2026-08-15 against the existing suite, which stands at 155 passing.*
  - [x] Sign up → create → publish → read cycle — *`08-flow-register-publish-read`, 3 tests*
  - [x] AI chat interaction — *`09-flow-ai`, "the AI chat panel opens and answers"*
  - [x] Inline editing — *`09-flow-ai`, 2 tests: the popup appears on a selection, and an action returns a suggestion that can be applied*
  - [x] Like / comment / follow — *`10-flow-social`, 4 tests, including the notifications the actions produce*
  - [x] Premium gate — *`15-flow-premium-paywall`, 3 tests, plus `21-phase5-upgrade-flow` which drives the free→premium transition across the same article*
- [ ] Lighthouse audit — target score >90 on article pages (Performance, Accessibility, SEO)
- [ ] Accessibility pass — `axe-core` scan, fix critical issues
- [x] Fix all TypeScript strict errors — *2026-08-15: both repos already carry `"strict": true` and `tsc --noEmit` exits 0. Nothing to fix; the box was never ticked.*
- [ ] Input sanitization audit (XSS on article content, comments)

### SEO
- [ ] Dynamic OG images for articles (Next.js `ImageResponse`) *(stretch — zero demo value)*
- [ ] Sitemap (`/sitemap.xml`) — auto-generated from published articles
- [ ] Structured data (JSON-LD `Article` schema on article pages)
- [ ] `<meta>` description from article excerpt

### Demo & Seed Mode
- [ ] `DEMO_MODE=true` environment flag:
  - [ ] Lowered eligibility thresholds (e.g., 5 readers + 2 reactions)
  - [x] Seed script: pre-populate demo writers, 10+ substantive articles, analytics events, magazine account — *built in Phase Q: `pnpm db:seed` produces 5 writers, 12 published articles, a subscribed magazine, 3 readers, 12 one-off visitors, 8 tags and ~1,250 analytics events, with deliberately non-overlapping vocabularies*
  - [x] Demo scenario: writer crosses eligibility live → publishes to marketplace → magazine previews + purchases — *walked end to end 2026-08-15: `11-flow-marketplace` (6 tests) plus `22-phase5-marketplace-demo` (3), which adds the evaluation/Portfolio Insights step and completes the purchase from that page. **Note the live-crossing beat still needs the `DEMO_MODE` thresholds below** — the real bar is 5,000 identified readers and the seeded corpus reaches 11.*
- [ ] `reconcile-balances` background job — asserts snapshot == ledger sum, alerts on drift

### Production Deploy
> **DEFERRED — this whole section is the last thing that happens.** Decision of
> 2026-08-10: development continues **entirely locally** until the feature work is
> finished. Nothing in Phases 4–5 depends on any of it.
>
> *Updated later the same day:* the original reason for deferring was that a
> domain and a VPS both cost money the project could not spend. The GitHub
> Student Developer Pack supplies both at no cost, so this is now a **scheduling**
> decision rather than a hard block — features first, deploy last, but the deploy
> is genuinely reachable. That is a materially better position for the defense: a
> live production URL is worth real marks on a DevOps-heavy project.
>
> The configuration is already written and tested (see **Phase I**) — what remains
> is provisioning, then a single pass through the checklist below.

**Prerequisites — both are covered by the GitHub Student Developer Pack**
*(confirmed available 2026-08-10; no purchase and no international card needed,
which was the original blocker)*

- [x] **Claim a domain.** — **`inkwell-ai.me`, registered 2026-08-16** via
      Namecheap's pack offer.
      **Correction to the note this replaces:** it said `inkwell.ai` was a
      placeholder to be substituted "in all four places at once". That was wrong.
      `inkwell.ai` is also the *local dev hostname* — `/etc/hosts` maps
      `frontend.`/`backend.`/`storage.inkwell.ai` to `127.0.0.2`, and `dev.conf`,
      the Playwright suite and every review-test doc resolve through those names.
      A blanket replace would break local dev and all 22 E2E specs.
      Production barely uses the name: `default.conf` serves the app on
      `server_name _` (catch-all), so exactly **one** line hardcoded a domain.
      Substituted 2026-08-17 in the production-only places — the `.env.example`
      prod block, `default.conf`'s storage vhost and certbot line, and the
      README's production section. Dev names left untouched, deliberately.
- [ ] **Provision the VPS.** ~~DigitalOcean ($200 pack credit)~~ — **withdrawn.**
      DigitalOcean wound down its Student Pack participation and revoked *all*
      pack credits on 2026-08-01, including ones already redeemed.
      **Use Azure for Students** ($100, academic-email verification, no card —
      which is the binding constraint here). Size **B2s** (2 vCPU, 4 GiB, x86),
      ~$30–35/mo, so the credit covers ~3 months against the ~4 weeks needed.
      Nothing builds on the server — all three app containers pull prebuilt
      images from GHCR — so this is runtime footprint only.
      **Oracle Cloud's Always Free tier is not a drop-in replacement**: it is ARM
      Ampere, and neither CI workflow sets `platforms:` on
      `docker/build-push-action`, so the images are amd64-only. Going ARM means
      adding multi-arch builds and a 20–40 min QEMU cross-compile.
      **Fallback if Azure rejects the academic email:** Cloudflare Tunnel — free,
      no card, real certificate, stack running on the laptop. Not a true deploy
      and the report should say so, but it makes the live-URL demo performable.

> **Standing preference (2026-08-10):** when a Student Pack offer is the best
> available option for a piece of infrastructure, use it. It is why deployment is
> no longer blocked on spending money — the constraint that produced the deferral
> below has been removed, and what remains is sequencing, not capability.

**Then, in order:**

- [ ] Configure domain + Cloudflare DNS — **three A records**, all at the VPS and all resolving *before* certbot runs, since one certificate covers all three: `inkwell-ai.me`, `www.inkwell-ai.me`, and `storage.inkwell-ai.me` for presigned uploads (the apex path `/<bucket>/<key>` is claimed by the Next.js catch-all)
- [x] TLS via Let's Encrypt (Nginx + certbot) — **nginx side done 2026-08-06**: 443 listener, HTTP→HTTPS redirect sparing the ACME path, certbot webroot volume, storage vhost. Verified against live containers with a self-signed certificate. Issuing the real certificate needs the VPS.
- [ ] GitHub Actions deploy workflow in `docker.inkwell.ai`:
  - [ ] Trigger on push to `main` in backend/frontend repos (via `repository_dispatch`)
  - [ ] SSH to VPS → pull new images → `docker compose up -d`
- [x] Production `.env` configured — **template done 2026-08-06**: a full production override block in `.env.example`, including which values are runtime and which are build-time. Filling in real secrets needs the VPS.
- [ ] Database migration runs automatically on deploy — **note there is already one pending migration**: `notification_type` gained `'repost'` on 2026-08-10 (`ALTER TYPE ... ADD VALUE`, additive). It is applied to the dev and test databases; a production database has never existed, so it will be created with the value present.
- [x] MinIO bucket created + public read policy for article images — **done 2026-08-06**, in `UploadsService` on bucket creation, and applied to the existing dev bucket
- [ ] **Set the four GitHub repository variables** (Settings → Secrets and variables → **Variables**, not Secrets): `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_STORAGE_URL`, `NEXT_PUBLIC_SENTRY_DSN`. `next build` inlines them into the browser bundle, so a runtime value changes nothing the browser executes — and changing one requires **rebuilding** the frontend image, not restarting it. **Deliberately left unset while local-only** (see the note below).
- [ ] Create the Sentry project and set `SENTRY_DSN` (runtime, VPS `.env`) and `NEXT_PUBLIC_SENTRY_DSN` (build-time, repository variable). The SDK no-ops with no DSN, so this is a deploy-time task, not a blocker.
- [ ] Verify full stack running at production URL

> **Why the repository variables are intentionally empty right now.** They were
> set briefly on 2026-08-10 and immediately removed once it was confirmed no
> domain had been bought — pointing them at an unregistered `inkwell.ai` would
> bake a domain nobody controls into every published image. With them unset,
> `next build` receives empty strings and the code falls back to its localhost
> defaults, which is the correct behaviour for a local-only project. CI still
> builds and publishes images to GHCR on every push to `main`; those images are
> **not deployable** and are not meant to be — they exist to keep the pipeline
> exercised.
>
> This only works because of the `||`-vs-`??` fix committed the same day: an
> absent build arg arrives as the **empty string**, not as `undefined`, and the
> old `??` fallbacks kept it — which failed the first CI build on `main` outright
> (`new URL('')` in the root layout).

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

## Phase V — Vendored Sources & Dev Images
> Sprint S7 · 2026-08-19 · **Completed** (backfilled into the plan, in the same spirit as Phases D, Q and I)

> **Why this phase exists:** it started as a bug report — `make dciup-dev` followed by a 502 at `frontend.inkwell.ai`. The 502 was correct behaviour (that target starts infrastructure only, and the `web` container was not running), but the reason the app services could not be started at all was that the two app repos were **absent from the machine**. Tracing why that failed so opaquely surfaced three further defects, one of them live in production.

### Repo layout
- [x] `frontend.inkwell.ai` and `backend.inkwell.ai` vendored as **git submodules** under `docker.inkwell.ai/src/`, both pinned to `main`
- [x] Dev bind mounts retargeted from `../../../<repo>` — paths *outside* the repository, enforced by nothing but a README paragraph — to `../../src/<repo>`
- [x] `make check-submodules` guards `dci-api` / `dci-web` / `dci-worker` / `dciup-all`; `dciup-dev` deliberately unguarded, since it mounts no application source
- [x] `make git-spull` fast-forwards both submodules to the branch declared in `.gitmodules`
- [x] `make setup-hosts` adds the three dev hostnames idempotently; `check-hosts` warns before `dciup-dev` without failing or prompting for sudo

### Dev images
- [x] `.infra/dockerfiles/{web,api}.dev.dockerfile` — dependencies as a cached layer, source still bind-mounted, `api` and `worker` sharing one image
- [x] Container start no longer re-runs `pnpm install`: a cold container serves in ~5s
- [x] `dci-dev-build` is now cached (the common case after a dependency bump); `dci-dev-rebuild` keeps `--no-cache`

### Defects found while closing them

Same pattern as Phases Q and I: each had been latent for some time, and none was what the original bug report was about.

- **A missing repo failed silently and misleadingly.** Docker's response to a bind-mount source that does not exist is to *create* it, owned by root. The app container then died on a missing `package.json` with nothing pointing at the actual cause — a repository that had never been cloned. Submodules make the layout a property of the checkout rather than a convention.
- **The `node_modules` named volumes were seeded root-owned.** Docker seeds an empty named volume from the image, ownership included; nothing existed at `/app/node_modules` in the stock `node:22-alpine`, so the volume was created `root:root` while the container ran as the host UID. Every first start died on `EACCES: permission denied, mkdir '/app/node_modules/.pnpm'`. The dev images install as the runtime user, so the seed is correct. This is the same class of bug as the root-owned `.pnpm-store/` found in Phase 3's close-out, in a place that pass did not reach.
- **Datastore ports were published on `0.0.0.0`.** nginx had been carefully bound to `127.0.0.2` and `127.0.0.1`, while `db`, `redis` and `minio` used bare `"5433:5432"`-style mappings — offering Postgres, Redis and the object store to every host on whatever network the laptop had joined. All now bind `127.0.0.1`; verified from the machine's LAN address that each port refuses while loopback still connects.
- **Production published the MinIO admin console on `0.0.0.0:9001`.** That console authenticates with `MINIO_ROOT_USER`/`MINIO_ROOT_PASSWORD` — full access to every bucket — so the VPS was serving an internet-facing root login. Now `127.0.0.1:9001`, reached over an SSH tunnel. **This one was live**, and the fix only takes effect on the next production deploy.
- **`.gitignore` did not ignore the TLS private key.** The pattern `nginx/certs/` contains a non-trailing slash, so git anchored it to the repository root and it never matched `.infra/nginx/certs/`. Corrected and verified with `git check-ignore`.
- **A stale `DOCKER_UID` from an unrelated project broke every app container.** An old project exported `DOCKER_UID=oussama` from `~/.zshrc`, and Compose gives the shell environment precedence over `--env-file`, so `.env`'s `1000` was silently ignored and containers failed with `unable to find user oussama`. An environment-only defect, recorded because the precedence rule is not obvious and the symptom names no project.

**Verification:** both compose files validate; the submodule guard was negative-tested against an emptied submodule; the `node_modules` volumes were deleted and the stack brought up cold to confirm correct seeding; images build in 1m44s and a cached rebuild in under a second; `frontend.inkwell.ai` returns 200, `backend.inkwell.ai/api/docs` returns 200, `localhost:8080` returns 200, and the worker registers its BullMQ repeatable jobs.

**Not addressed, recorded rather than silently skipped:**
- **Dev still has no migration path.** The *production* half is done and recorded in S7 (automatic migrations on deploy, built 2026-08-17): a one-shot `migrate` service gated on `service_completed_successfully`. Locally, though, nothing creates the schema and no `make` target documents it, so a fresh clone gets an empty database. The same `drizzle-orm` migrator the deploy uses would serve.
- **Neither app repo declares `packageManager`** in `package.json`, so `corepack` resolves an unpinned pnpm version and two machines can silently differ. Belongs to the app repos, not the infra repo.

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

- **AI providers used:** Groq (LLM + Whisper, free tier), Gemini 2.0 Flash (LLM fallback) and `gemini-embedding-001` (embeddings) — all free tier, no payment method required
- **Shared types strategy:** Backend OpenAPI → auto-generated TS client in frontend CI + `@inkwell/shared` package for non-API types
- **Worker container** shares the backend image but runs `node dist/src/worker` — handles BullMQ jobs for embedding, analytics aggregation, email
- **RAG scope:** Only the writer's own articles (not platform-wide) — makes the demo story "it writes like *me*"
- **Mobile:** deferred post-MVP (resolved by the 2026-07-26 re-baseline — see Post-MVP Descope)

## Droppable Features (Priority Order)
> Mobile, voice, email, AI eval, cookie consent, and advanced moderation were already descoped in the 2026-07-26 re-baseline. If further time pressure builds, drop the remaining features in this order (top = first to cut):

1. ~~**Reposts**~~ — **built 2026-08-10**, so no longer available to cut. It was cheaper than it looked: the table, the constraint and the aggregation already existed and only a writer was missing, and it turns `repostRate` on the magazine evaluation report from a structural 0 into a real measurement.
2. **Follows / follower-growth chart** — vanity metrics
3. **Dynamic OG images** — SEO polish, not load-bearing
4. **BI trim** (last resort, per contingency rule) — magazine dashboard panels reduced to summary cards; eligibility pipeline untouched

**Never cut:** Editor, AI chat/inline, RAG (write-like-me + Portfolio Insights), Analytics (event capture + dashboards), Marketplace (preview/purchase + locked ledger), Likes + Comments (feed eligibility computation)
