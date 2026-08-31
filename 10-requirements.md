# 10 — Requirements, Backlog & Release Plan

> **Why this document exists.** The report's Chapter 2 (*Requirements Analysis and
> Specification*) needs four things that exist nowhere else in this repository: a
> formal actor inventory, functional requirements stated per actor, non-functional
> requirements, and a product backlog written as user stories. `0-phase-plan.md` is
> an engineer's task checklist in the imperative — it records what was built, not
> what a user wanted. This document supplies the missing half.
>
> Created 2026-08-19, after reverse-engineering the structure of two example PFE
> reports supplied by the professor. Both organise Chapter 2 exactly this way, and
> Report B specifies functional needs **per actor**, which suits this project's
> eight-actor model better than grouping by feature domain.
>
> **Language.** English throughout — the report is written in English, unlike the
> two French example reports the professor supplied. Those examples give us the
> *structure*, not the wording, so nothing here needs translating at writing time.
> The user-story form is *"As a \<actor\>, I want \<goal\>, so that \<benefit\>"*.
>
> **Status.** Requirements and backlog are reconstructed from what was actually
> built (Phases 0–5 closed and verified). Where the built system deviates from the
> original intent, the requirement records reality and the deviation is noted, so
> the report never claims something the demo cannot show.

---

## 1. Actors

Eight actors. The set is not invented for the report — it is the role matrix the
design system already uses (`9-design.md` §5.3), which in turn mirrors the
`account_type` / `role` / `plan` columns and the `is_marketplace_eligible` flag.

| # | Actor | Data-model representation | One-line definition |
|---|-------|---------------------------|---------------------|
| A1 | Visitor | no row | Unauthenticated. Sees the public feed and free article bodies; cannot interact. |
| A2 | Free reader | `account_type='personal'`, `plan='free'` | Reads free public articles, interacts socially, no AI allowance. |
| A3 | Premium reader | `account_type='personal'`, `plan='premium'` | Everything A2 has, plus premium articles and the daily AI allowance. |
| A4 | Writer | `role='writer'` | A2/A3 plus drafting, publishing and editing their own articles. |
| A5 | Eligible writer | `is_marketplace_eligible=true` | A4 plus the right to publish premium articles and to list on the marketplace. |
| A6 | Magazine (unsubscribed) | `account_type='magazine'`, `subscription_status<>'active'` | Registered magazine with no active subscription. Blocked at the subscription wall. |
| A7 | Magazine (subscribed) | `account_type='magazine'`, `subscription_status='active'` | Browses writers, reads evaluation reports, spends credits to preview and purchase. |
| A8 | Administrator | `role='admin'` | Moderation queue, user management, manual eligibility grants. |

**Notes that matter for the use case diagram.**

- A3 generalises A2; A5 generalises A4; A7 generalises A6. Draw them as
  inheritance, not as separate unrelated actors.
- A4 is orthogonal to A2/A3: a writer can be on the free plan (they write without
  AI) or premium. Role and plan are deliberately independent columns.
- A6 exists as a distinct actor because it has exactly one meaningful capability —
  subscribing — and every other magazine capability is denied to it. Both example
  reports model their subscription wall the same way.
- A8 cannot be created through the UI. Promotion to `admin` is a deliberate act
  against the database (decided 2026-08-15), and an admin's role is not editable
  in either direction.

---

## 2. Functional requirements

IDs are stable; the report cites them. Priority uses MoSCoW. "Sprint" is the
report's sprint numbering (§5), not the calendar sprint.

### 2.1 A1 — Visitor

| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-01 | Browse the public feed, paginated, with title, excerpt, thumbnail and tags | Must | 1 |
| FR-02 | Read the full body of a **free public** article without an account | Must | 1 |
| FR-03 | Be blocked from premium and marketplace articles, with an explicit prompt to sign up | Must | 1 |
| FR-04 | Register as a personal account, or as a magazine account | Must | 1 |
| FR-05 | Authenticate by email/password or Google OAuth | Must | 1 |
| FR-06 | Search articles and writers, and browse by tag | Should | 4 |

> **Deviation recorded.** `2-features.md` §7.4 reads as requiring an account to see
> any article body. The built system leaves free public articles readable by
> guests, deliberately: gating them would contradict the public feed and the SEO
> work, and would change the product. The report states this as a decision.

### 2.2 A2 / A3 — Free and premium reader

> **FR ids are append-only.** FR-60 sits between FR-10 and FR-11 because the
> table groups by persona and by the feature it belongs beside, not by number.
> Requirement ids are referenced from the phase plan and from commit messages,
> so an existing one is never renumbered to close a gap or restore a sequence.

| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-07 | Manage a profile — display name, bio, avatar upload | Must | 1 |
| FR-08 | Like an article, and un-like it | Must | 3 |
| FR-09 | Comment on an article, and reply to a comment (threaded) | Must | 3 |
| FR-10 | Delete one's own comment | Must | 3 |
| FR-60 | Like a comment or a reply, and un-like it | Must | 7 |
| FR-11 | Repost an article | Could | 3 |
| FR-12 | Follow and unfollow a writer | Should | 3 |
| FR-61 | View any profile's followers and following lists, and follow or unfollow from them | Must | 7 |
| FR-13 | Receive notifications for follows, likes, comment likes, comments and replies, delivered live | Must | 3 |
| FR-14 | List past notifications and mark them read | Must | 3 |
| FR-15 | Upgrade to premium, and downgrade (simulated payment) | Must | 5 |
| FR-16 | *(A3 only)* Read premium-visibility articles | Must | 5 |
| FR-17 | *(A3 only)* Consume a daily AI token allowance | Must | 2 |

### 2.3 A4 / A5 — Writer

| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-18 | Create a draft and edit it in a rich-text editor (TipTap, stored as JSON) | Must | 2 |
| FR-19 | Have drafts saved automatically, debounced, without a save action | Must | 2 |
| FR-20 | Insert images by paste, drag or file picker, uploaded directly to object storage | Must | 2 |
| FR-21 | Set a cover image, excerpt and tags | Must | 2 |
| FR-22 | See live word count and estimated reading time | Should | 2 |
| FR-23 | Publish an article, choosing its placement: public or marketplace | Must | 1 |
| FR-24 | Choose a visibility for public articles: free or premium | Must | 1 |
| FR-25 | Update or soft-delete an own article | Must | 1 |
| FR-26 | Switch an article from marketplace to public (one-way; the reverse is refused) | Should | 5 |
| FR-27 | Converse with an AI assistant grounded in the writer's **own** published corpus | Must | 2, 4 |
| FR-28 | Apply an inline AI action to a text selection — reformulate, shorten, expand, simplify, improve | Must | 2 |
| FR-29 | See which passages the assistant retrieved, grouped by source article | Should | 4 |
| FR-30 | Insert an AI response into the document at the cursor | Must | 2 |
| FR-31 | See the remaining AI token balance, updated after each action | Must | 2 |
| FR-32 | View per-article analytics — views, unique readers, average read time, completion, engagement, retention curve | Must | 3 |
| FR-33 | Rank own articles by views or engagement, server-side across the whole body of work | Should | 3 |
| FR-34 | See progress toward marketplace eligibility | Must | 5 |
| FR-35 | *(A5 only)* Publish to the marketplace with a price in credits | Must | 5 |
| FR-36 | *(A5 only)* Publish premium-visibility articles | Must | 5 |
| FR-37 | View earnings — lifetime, per article, itemised by preview and purchase | Must | 5 |
| FR-38 | Be notified when a magazine previews or purchases an article, and when earnings are credited | Must | 5 |

> **Descoped, and the report says so:** voice-to-article (FR would have been "dictate
> an article"). Removed from the MVP in the 2026-07-26 re-baseline. The enum value
> `voice_transcribe` survives in `ai_action_type` with no implementation — mention
> it as future work rather than leaving an examiner to find it.

### 2.4 A6 / A7 — Magazine

| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-39 | Register with magazine fields — name, slug, logo, website, description | Must | 1 |
| FR-40 | *(A6)* Be stopped at a subscription wall before any marketplace surface | Must | 5 |
| FR-41 | Subscribe, receiving a monthly credit allowance (simulated payment) | Must | 5 |
| FR-42 | Top up credits outside the monthly grant | Should | 5 |
| FR-43 | See the credit balance, the renewal date and the transaction history | Must | 5 |
| FR-44 | Browse eligible writers, filtered by topic, searchable, with four sort orders | Must | 3 |
| FR-45 | Read a writer evaluation report — audience, content, quality panels | Must | 3 |
| FR-46 | Request AI Portfolio Insights for a writer, as an explicit action | Must | 4 |
| FR-47 | Browse a writer's marketplace-listed articles with prices | Must | 5 |
| FR-48 | Unlock a preview for 10% of the price, and read the full article | Must | 5 |
| FR-49 | Purchase the remainder (90%) and gain republish rights | Must | 5 |
| FR-50 | See the curated library of fully purchased articles | Must | 5 |

> **Deviations recorded.** Portfolio Insights generation is an explicit click,
> never a page-load side effect, because each generation costs a model call.
> "Topic relevance" sorting is not implemented.
>
> **Retired 2026-08-24 — the `/discover` gating deviation.** This note said
> `/discover` gates on account type rather than on an active subscription "until
> Sprint 5 lands the subscription state". Sprint 5 landed it: both routes on
> `discover.controller.ts` (:56, :80) carry `subscription: true`, which appends
> `SubscriptionGuard` to the same `@UseGuards` as the account-type check. The
> deviation described a state the system left months ago, and a stale deviation is
> worse than none — it invites a reader to distrust the ones that are still true.
> The deviation count in §6 drops from six to five.

### 2.5 A8 — Administrator

| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-51 | Review a queue of reports on articles, users and comments | Must | 5 |
| FR-52 | Dismiss a report, delete the reported article, or ban its author | Must | 5 |
| FR-53 | List and search users, filtered by role and by active/banned | Should | 5 |
| FR-54 | Edit a user's plan (both directions), logged | Should | 5 |
| FR-55 | Grant marketplace eligibility manually, with an audit-log entry | Must | 5 |

> **Refusals enforced server-side**, each with a test pinning it: `admin` is not an
> assignable role; an admin's role is not editable; you cannot edit your own role
> or plan; you cannot edit a banned account; a magazine cannot be given a role.

### 2.6 Cross-cutting

| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-56 | Every article body access decision is taken server-side against the §7.4 matrix; locked content arrives as null | Must | 5 |
| FR-57 | Content is classified at publish time; a flag files a pending report but never blocks publication | Should | 5 |
| FR-58 | Any credit movement writes ledger rows inside one transaction, under a row lock | Must | 5 |
| FR-59 | Report an article, a user or a comment | Must | 5 |

---

## 3. Non-functional requirements

Absent from every other spec document. Each is stated as a property with the
evidence that supports it, so the report can cite code rather than assert.

### 3.1 Security

| ID | Requirement | Evidence |
|----|-------------|----------|
| NFR-01 | Passwords stored as bcrypt hashes, cost factor 12 | `auth` module |
| NFR-02 | Access tokens expire in 15 minutes; refresh tokens in 7 days | `ACCESS_TOKEN_MAX_AGE = 900`. **Not revocable** — corrected 2026-08-21. `9-implementation-guide.md` §2.3 specified opaque UUIDs in Redis expressly to allow revocation; `auth.service.ts` issues a second JWT and verifies it against `JWT_REFRESH_SECRET`, storing nothing. Logout clears the client's copy only, so until it expires a captured refresh token survives a password change and a ban. The 7-day TTL is the whole of the bound. |
| NFR-03 | Every protected route passes a guard stack composed once via `@Auth()` | 6 guards: Jwt, Roles, Plans, AccountType, Subscription, AiQuota |
| NFR-04 | Authorisation is decided server-side; the client is told the verdict and never computes it | §7.4 matrix in `article-access.ts` |
| NFR-05 | Per-IP rate limits on every endpoint, tightened on the credential routes | `@nestjs/throttler`: 60/min globally, **10/min on `POST /auth/login` and 5/min on `POST /auth/register`**, 10 per 10s on analytics ingest. Keyed on the real client IP — `app.set('trust proxy', 1)` plus nginx's `X-Forwarded-For`, without which every request would share nginx's container IP and the limit would be global rather than per-IP. **Counters are in-process memory** — the module is configured with no `storage`, so limits are per API process and reset on restart. Corrected 2026-08-24: the auth tightening this row claimed was not implemented until that date, and "AI and purchase routes" was never true — AI spend is capped by the token quota, which is the more meaningful limit, and purchases by idempotency keys. |
| NFR-06 | Financial operations are idempotent under retry | `transactions.idempotency_key` UNIQUE |
| NFR-07 | Uploads are presigned, time-limited, and never routed through the API | 10-minute PUT TTL; bucket grants `s3:GetObject` only, never `s3:ListBucket` |
| NFR-08 | Datastore ports bind to loopback only, never `0.0.0.0` | Phase V fixed this in dev and production |
| NFR-09 | A ban takes effect at the next authentication; no session is silently immortal | `deleted_at` checked in `login()`, `refresh()` and the Google path |
| NFR-10 | No stored HTML is rendered as markup — no `dangerouslySetInnerHTML` anywhere | Confirmed by sweep; `ts_headline` deliberately not adopted |

### 3.2 Performance

| ID | Requirement | Evidence |
|----|-------------|----------|
| NFR-11 | Semantic retrieval stays sub-linear at corpus scale | HNSW index, `m=16`, `ef_construction=64`, `vector_cosine_ops` matching the query operator |
| NFR-12 | Full-text search is index-backed with weighted ranking | Generated `tsvector` column, weights A/B/C, GIN index |
| NFR-13 | Prompt context is bounded | top-K ≤ 5 chunks, memory block < 200 tokens, ≈2000 tokens total |
| NFR-14 | Feed pagination is cursor-based, stable under insertion | `(created_at DESC, id)` — see §6 on notifications |
| NFR-15 | Dashboard panels reporting totals and rates read pre-aggregated rows; time-series panels may query `analytics_events` directly, bounded and labelled | 4 rollup tables refreshed by the worker; `GET /me/analytics/timeseries` returns `source: 'events'` |
| NFR-16 | Analytics aggregation is incremental and idempotent | reads only events since `last_aggregated_at` |
| NFR-17 | Expensive AI output is cached and invalidated by the job that changes its basis | `portfolio_insights`, 24 h TTL, dropped by `embed-article` |
| NFR-18 | Streaming responses are not buffered end to end | `proxy_buffering off`, `X-Accel-Buffering: no`, 300 s read timeout |

### 3.3 Reliability and correctness

| ID | Requirement | Evidence |
|----|-------------|----------|
| NFR-19 | Denormalised balances always equal their ledger sum | three invariants in `database/ledger-invariants.ts`, asserted after every money-moving test |
| NFR-20 | Concurrent purchases cannot double-spend | `SELECT … FOR UPDATE` on the balance-owning row inside the transaction |
| NFR-21 | Schema changes are versioned and applied before the app starts | one-shot `migrate` service, gated `service_completed_successfully` |
| NFR-22 | The vector extension exists before any migration that needs it | runner issues `CREATE EXTENSION IF NOT EXISTS vector` first — measured failure otherwise |
| NFR-23 | Failed background jobs retry with exponential backoff, 3 attempts | BullMQ `defaultJobOptions` |
| NFR-24 | A single AI **model** failing degrades AI only; the rest of the product keeps working | Corrected 2026-08-21, **re-corrected 2026-08-24** — the first correction had itself gone stale. The specified Groq → Gemini chain was never implemented and **cannot be**: `portfolio-insights.service.ts` records that Gemini's free tier grants `generateContent` a quota of 0 for every model offered to new projects, which is why Insights runs on Groq. What exists is per-model failover *within* Groq. The chain is **`openai/gpt-oss-120b` → `openai/gpt-oss-20b`** (`LLM_MODELS`, `ai.service.ts:84`); the 2026-08-21 note named `llama-3.3-70b-versatile` as the primary, which had already been replaced — llama returns its reasoning inside `content` as a literal `<think>` block, so a writer asking for a rewrite would watch the model deliberate, while the gpt-oss pair put reasoning on a separate field the text stream does not carry. Failover works because the first chunk is pulled by hand: `streamText` defers the provider call until the stream is consumed, so a 401/429/unavailable surfaces while nothing has been written to the response and another model can still take over. 503 + "AI is temporarily unavailable" when both refuse. This survives one model's rate limit, **not** a total Groq outage. |
| NFR-25 | Every service reports liveness and readiness | `GET /health`, `GET /ready` — **Postgres only**. The Redis half was specified in three documents and never built (`health.controller.ts` returns `{ status, db }`). |

### 3.4 Scalability

| ID | Requirement | Evidence |
|----|-------------|----------|
| NFR-26 | The API holds no session state | JWT claims only |
| NFR-27 | Long work never runs in the request path | 4 queues, separate worker entrypoint from the same image |
| NFR-28 | API and worker scale horizontally behind the proxy | stateless containers, one compose service each |

### 3.5 Maintainability

| ID | Requirement | Evidence |
|----|-------------|----------|
| NFR-29 | Both repositories compile under `strict: true` with zero lint warnings | `tsc --noEmit`, `eslint --max-warnings=0` in CI |
| NFR-30 | The API contract is generated from OpenAPI and verified in CI against the committed types | `pnpm api:codegen`; hook signatures are hand-written against it — see §6 |
| NFR-31 | Business rules are tested, not asserted | 479 backend tests, 155 Playwright specs across 23 files |
| NFR-32 | CI fails when the schema and the migrations disagree | schema-drift check |
| NFR-33 | Errors are captured in four runtimes with no PII | Sentry in API, worker, Next server, browser; `sendDefaultPii: false`, traces 0.1 |

### 3.6 Usability and accessibility

| ID | Requirement | Evidence |
|----|-------------|----------|
| NFR-34 | Two breakpoints are designed and implemented: 375 px and 1280–1440 px | 58 Figma screens, both widths |
| NFR-35 | One design system, applied consistently | 39 tokens, 87 components, 148 instances across 60% of screens |
| NFR-36 | Dark mode is reachable and complete | Phase Q |
| NFR-37 | Lighthouse > 90 and no critical `axe-core` violations on article pages | **pending — Phase 6** |

> **NFR-37 is the only requirement in this document not yet satisfied.** State it as
> planned work, not as achieved.

---

## 4. Product backlog

The form is *"As a … I want … so that …"*. IDs are stable.
Points are Fibonacci, relative to US-01 = 1. "Sprint" refers to §5.

### E1 — Accounts and authentication

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-01 | Register with an email and a password so that I can have an identity on the platform | A1 | Must | 3 | 1 |
| US-02 | Sign in with Google so that I do not manage another password | A1 | Should | 3 | 1 |
| US-03 | Register as a magazine with my branding so that writers recognise my publication | A1 | Must | 5 | 1 |
| US-04 | Stay signed in across a long writing session so that I do not lose a draft | A4 | Must | 3 | 1 |
| US-05 | Edit my profile and avatar so that my public page represents me | A2 | Should | 3 | 1 |

### E2 — Writing and publishing

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-06 | Write in a rich editor so that structure and emphasis survive publication | A4 | Must | 8 | 2 |
| US-07 | Have my draft saved as I type so that I never lose work | A4 | Must | 3 | 2 |
| US-08 | Paste or drag an image into the article so that illustrating is not a detour | A4 | Must | 5 | 2 |
| US-09 | Set a cover image so that my article looks deliberate in the feed | A4 | Should | 3 | 2 |
| US-10 | Tag an article so that readers find it by topic | A4 | Should | 2 | 1 |
| US-11 | Choose at publish time whether an article is public or for sale | A4 | Must | 5 | 1 |
| US-12 | Restrict an article to premium readers so that my best work is worth a subscription | A5 | Should | 3 | 5 |
| US-13 | See word count and reading time so that I can judge length as I write | A4 | Could | 1 | 2 |

### E3 — AI assistance

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-14 | Ask an assistant that has read my published work so that suggestions sound like me | A4 | Must | 13 | 2, 4 |
| US-15 | Reformulate, shorten, expand, simplify or improve a selection so that editing is one click | A4 | Must | 8 | 2 |
| US-16 | Insert an answer into my document so that I do not copy by hand | A4 | Must | 2 | 2 |
| US-17 | See which of my passages the assistant used so that I can trust the answer | A4 | Should | 5 | 4 |
| US-18 | See my remaining allowance so that I can pace my usage | A3 | Must | 2 | 2 |
| US-19 | Have my voice profile extracted from my corpus so that the assistant stays consistent when retrieval finds nothing | A4 | Should | 8 | 4 |

### E4 — Discovery and search

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-20 | Search by keyword so that I find an article I half-remember | A1 | Must | 5 | 4 |
| US-21 | Find articles that match my meaning even when they share none of my words | A1 | Must | 8 | 4 |
| US-22 | Browse by tag so that I can follow a topic | A1 | Should | 2 | 4 |
| US-23 | Find writers, not only articles, so that I can follow a person | A1 | Should | 3 | 4 |

### E5 — Social interactions and notifications

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-24 | Like an article so that I can signal quality | A2 | Must | 2 | 3 |
| US-25 | Comment and reply in a thread so that discussion has structure | A2 | Must | 5 | 3 |
| US-26 | Follow a writer so that I keep up with them | A2 | Should | 3 | 3 |
| US-27 | Repost an article so that my followers see it | A2 | Could | 2 | 3 |
| US-28 | Be told the moment someone reacts to my work, without reloading | A4 | Must | 5 | 3 |
| US-29 | Review notifications I missed so that nothing is lost between sessions | A2 | Must | 3 | 3 |

### E6 — Analytics

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-30 | See how many people read an article and how far they got so that I can write better | A4 | Must | 8 | 3 |
| US-31 | Rank my articles by performance so that I learn what works | A4 | Should | 3 | 3 |
| US-32 | Evaluate a writer on audience, content and quality so that I can commission with evidence | A7 | Must | 13 | 3 |
| US-33 | Read an AI assessment of a writer's voice and range so that I can shortlist quickly | A7 | Must | 8 | 4 |

### E7 — Marketplace and subscriptions

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-34 | Upgrade to premium so that I can read everything and use the assistant | A2 | Must | 5 | 5 |
| US-35 | Subscribe as a magazine so that I can access the marketplace | A6 | Must | 8 | 5 |
| US-36 | Receive a monthly credit budget so that spending is predictable | A7 | Must | 5 | 5 |
| US-37 | Top up credits so that a good month is not capped | A7 | Should | 3 | 5 |
| US-38 | Pay 10% to read an article in full so that I can judge before buying | A7 | Must | 8 | 5 |
| US-39 | Pay the remainder to acquire republish rights so that I can publish it | A7 | Must | 8 | 5 |
| US-40 | Keep purchased articles in a library so that my acquisitions are in one place | A7 | Must | 3 | 5 |
| US-41 | List an article for sale at my own price so that I am paid for exclusivity | A5 | Must | 5 | 5 |
| US-42 | See my earnings itemised by preview and purchase so that I trust the accounting | A4 | Must | 5 | 5 |
| US-43 | See how far I am from eligibility so that the gate feels reachable | A4 | Should | 3 | 5 |

### E8 — Moderation and administration

| ID | User story | Actor | Pri | Pts | Sprint |
|----|-----------|-------|-----|-----|--------|
| US-44 | Report content so that abuse has a channel | A2 | Must | 3 | 5 |
| US-45 | Work a queue of reports so that moderation is systematic | A8 | Must | 5 | 5 |
| US-46 | Remove an article or ban an author so that decisions are enforceable | A8 | Must | 3 | 5 |
| US-47 | Grant eligibility manually so that a promising writer is not held back by a counter | A8 | Must | 3 | 5 |
| US-48 | Search and filter users so that I can act on the right account | A8 | Should | 5 | 5 |

### E9 — Quality and operations (technical stories)

| ID | Story | Pri | Pts | Sprint |
|----|-------|-----|-----|--------|
| US-49 | Prove that every balance equals its ledger sum, after every money-moving operation | Must | 8 | 1 |
| US-50 | Bring the whole stack up with one command, reproducibly | Must | 8 | 1 |
| US-51 | Fail the build on a lint error, a type error, a failing test or schema drift | Must | 5 | 1 |
| US-52 | Apply migrations automatically before the application starts | Must | 5 | 6 |
| US-53 | Seed a believable corpus so that the product can be demonstrated cold | Must | 5 | 6 |
| US-54 | Lower the eligibility thresholds under a flag so that the gate can be crossed live | Must | 2 | 6 |
| US-55 | Serve the product at a public URL over TLS | Must | 8 | 6 |

**54 stories, 8 epics, 259 points.**

---

## 5. Release plan

Three releases, six sprints. The report's sprint numbering differs from the
calendar sprints in `0-phase-plan.md`, which ran S0–S7 including a three-sprint
design track; the mapping is explicit so nothing is hidden.

| Release | Report chapter | Sprint | Calendar | Phase | Goal |
|---------|---------------|--------|----------|-------|------|
| **R1 — Functional foundation** | Ch.4 | Sprint 1 | S1 · 29/05–11/06 | Phase 1 | Schema, authentication, article core, ledger invariant harness |
| | | Sprint 2 | S5 · 27/07–09/08 | Phase 2 | Editor, AI chat and inline actions, analytics event capture |
| **R2 — Social, analytics and AI** | Ch.5 | Sprint 3 | S5–S6 · 27/07–23/08 | Phase 3 | Social interactions, notifications, aggregation, dashboards |
| | | Sprint 4 | S6 · 10/08–23/08 | Phase 4 | RAG, Portfolio Insights, hybrid search, memory extraction |
| **R3 — Marketplace, testing and deployment** | Ch.6 | Sprint 5 | 13–14/08 | Phase 5 | Marketplace, subscriptions, premium, moderation, admin |
| | | Sprint 6 | S7 · 24/08–06/09 | Phase 6 | Tests, demo mode, deployment, CI/CD |

**Work that is not a sprint.** Phase 0 (foundation), Phase D (design track,
S2–S4), Phase I (URL topology), Phase Q (quality pass) and Phase V (vendored
sources) are not user-facing increments. They belong to the report's Chapter 3,
*Working Environment* — neither example report has design-only or
tooling-only sprints, and inventing one would produce a sprint with no software in
it.

---

## 6. Traceability and open points

- Every functional requirement traces to a feature in `2-features.md` or a flow in
  `3-user-flows.md`; every non-functional requirement traces to code or config.
- Requirements record the **built** system. Five deviations from the original specs
  are noted inline (guest access to free articles, insights generation as an
  explicit action, absent topic-relevance sort, the three NULL analytics columns,
  voice descoped) — plus the §6 route topology, reconciled in Phase 6 and recorded
  below. It was six until 2026-08-24, when the `/discover` gating deviation was
  retired: Sprint 5 had closed it and the note outlived the drift it described.
  The report reports them; recorded deviations read as maturity, hidden ones read
  as luck.
- **Resolved 2026-08-21 — the three NULL analytics columns.** `total_unique_readers`,
  `returning_reader_rate` and `total_unique_views` were empty because
  `analytics_events.viewer_id` was NULL on every row ever written: the tracker sent
  events with `sendBeacon`, which cannot set headers and so never carried the access
  token, while the endpoint took the viewer from the request body. Fixed in two
  halves that do not work apart — backend `af73d47` takes the viewer from the token,
  frontend `e5bd528` sends one. Marketplace eligibility, which counts
  `DISTINCT viewer_id` against a 5,000-reader threshold, was unreachable organically
  until then. **This is no longer a deviation and should not be reported as one.**
- **Added 2026-08-21 — four Redis claims corrected across the specs.** Redis is
  BullMQ-only. It does not cache (Portfolio Insights is a Postgres table), does not
  back rate limiting (`@nestjs/throttler` is in-memory, therefore **per process**),
  does not store refresh tokens (see NFR-02), and `/ready` does not check it (NFR-25).
  Corrected in `4-system-architecture.md` §8, `8-devops.md`, and
  `9-implementation-guide.md` §2.3 and §9.
- **Spec-lags-code drift, still open.** One item found in the schema conformance
  pass and not yet reconciled: `articles.search_vector` (a generated `tsvector`
  column with a GIN index, backing NFR-12) is documented in no spec.

  The notification enum half of this is **resolved 2026-08-23**: the frontend's tenth
  value, `system`, was deleted. It existed in `types/index.ts` alone and no backend
  path could emit it, so the renderer carried a branch for a notification that could
  never arrive — which is what stopped its `switch` from being exhaustive in any useful
  sense. Spec and code now both hold the nine emittable values.
- **Amended 2026-08-23 — NFR-15 now distinguishes totals from series.** The original
  wording ("never raw events") was written when every dashboard figure came from a
  rollup, and the writer analytics page contradicted it: its 30-day chart reads
  `analytics_events` directly.

  It has to. All four rollup tables hold one row per entity, written with
  `ON CONFLICT DO UPDATE`, so each aggregation run OVERWRITES the previous values —
  there is no history in them to chart, and the raw event log is the only place a past
  day still exists. Adding a per-day rollup would be a schema change, a worker step and
  a new staleness story for a query that is already index-supported.

  The exemption is bounded rather than open: the window is a whitelist (7/30/90) so a
  query parameter cannot widen the scan, the join is scoped to one author, and the
  response carries `source: 'events'` with a generation timestamp so the client can
  tell a live figure from an aggregated one. Every other panel on that page — the KPI
  row, the retention curve, the content mix, the top-articles table — still reads
  rollups. The same exemption was already taken and documented for the per-article
  `dailyViews` series in `analytics-reports.service.ts`; this makes it a stated rule
  rather than a silent precedent.
- **Amended 2026-08-23 — NFR-30 describes verification, not consumption.** The
  contract IS generated (`pnpm api:codegen` → `src/types/api.generated.ts`), but the
  TanStack hooks hand-write their response types against it rather than importing
  from it, because the backend declares few `@ApiResponse` decorators and most
  generated response types come out as `never`. Claiming "never hand-copied" was
  therefore false of the response side. CI regenerates and fails on a diff, so the
  contract is verified even where it is not imported.
- **Amended 2026-08-23 — NFR-14 no longer claims cursor pagination on notifications.**
  Feed pagination is cursor-based as stated. Notifications are served by offset behind
  the `{ items, page, limit, total, hasMore }` envelope that `paginated-response.ts`
  calls a frozen contract with the frontend, and the list grows its limit rather than
  paging. Converting would change that envelope and every paginated hook with it.
  Recorded as knowingly unmet rather than quietly satisfied by a looser reading.
- **Delivered 2026-08-23 — the writer surfaces §6 specified and the build lacked.**
  `9-design.md` §6 has been reconciled with the application route by route; fifteen of
  its eighteen dashboard-area routes returned 404 before this pass. Three were built
  (`/dashboard/articles`, `/dashboard/analytics`, `/dashboard/earnings`), the rest were
  corrected in the spec to the flat, shared topology the application actually uses.

  Two requirements were only half-met until then and are now whole:
  **FR-33** ranked a writer's work but gave them no page listing it — `/dashboard/articles`
  adds search and a date range over `GET /articles/me`. **FR-37** says earnings are
  "lifetime, **per article**, itemised by preview and purchase"; the per-article half
  existed in neither API nor UI, and is now `GET /me/earnings/by-article` behind a
  revenue table.

  One frame in §6 was **removed rather than built**: an admin Article Management page at
  `/admin/articles`. Moderation is report-driven by design and FR-51–FR-55 never asked
  for a corpus browser. Recorded as future work rather than dropped silently.
- **NFR-37** (Lighthouse, `axe-core`) is the only unsatisfied requirement.
- **Open:** the AI token top-up (US absent by design — the decision and the column
  shape to build are recorded on the item in `0-phase-plan.md` Phase 5).
