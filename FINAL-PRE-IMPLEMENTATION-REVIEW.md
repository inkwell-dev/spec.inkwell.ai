# Inkwell — Final Pre-Implementation Review

> **Reviewer role:** Principal Software Architect  
> **Scope:** Final review of all updated Inkwell specifications (0–8) and the ARCHITECTURE-REVIEW.md document before implementation begins.  
> **Date:** 2026-05-29  
> **Context:** Final-year CS Engineering graduation project · single engineer · heavy AI agent usage · ~14-week timeline

---

# Part 1 — Review of the Architecture Review Recommendations

## R1 — Remove the Python AI service

**Assessment: Strongly Agree**

The review correctly identified that this was already done and only the docs needed updating. The docs are now consistent — the system architecture describes a modular monolith with AI orchestration in NestJS via the Vercel AI SDK. No remaining issues.

**Missing considerations:** None. This is resolved.

---

## R2 — Structured Memory + RAG

**Assessment: Agree — with one implementation concern the review's fix introduced**

The review correctly identified the underspecified memory extraction pipeline and the specs now include §9.3.1 with the extraction job. The architecture (stable persona via memory + contextual exemplars via RAG) is sound and well-reasoned.

**Missing consideration — extraction cost scaling:** The spec says the `extract-writer-memory` job "retrieves the writer's full published corpus (or a representative sample)." Sending 50 articles to an LLM on every publish is expensive and slow. The spec needs a practical bound: extract from the **most recent 10 articles** or from the **existing RAG chunks** (which are already paragraph-level summaries sitting in the database). Using chunks as input is elegant — the extraction job becomes a SQL query + a single LLM call, not a corpus retrieval + multi-document analysis.

**Missing consideration — memory staleness:** The extraction runs on publish, but what if a writer's style evolves? Memory extracted from articles 1–5 will dominate the profile even after articles 6–20 shift the voice. The "most recent N" sampling approach solves this implicitly; the "full corpus" approach doesn't.

---

## R3 — Embeddings only for published articles

**Assessment: Strongly Agree**

Already the design; the chunk lifecycle (delete-then-reinsert on update, cascade on soft delete, cache invalidation) is now well-specified in schema §5.1. The review's gap-closing was thorough.

**Missing consideration:** None.

---

## R4 — PostgreSQL + pgvector as sole layer

**Assessment: Strongly Agree**

This remains the single best architectural decision. The specs now define RRF for hybrid search with `score = Σ 1/(k + rank_i)` with k=60. Correct and sufficient.

**Missing consideration — RRF implementation detail:** The spec defines the formula but not the *query structure*. In practice, RRF over pgvector + tsvector requires two separate queries (one `ts_rank` ordered, one `<=>` ordered), merging results in application code. This is not a single SQL query — it's a service-layer merge. An AI agent will try to do it in one query and fail. A brief note that RRF runs in the `SearchService` (not in raw SQL) would prevent wasted time.

---

## R5 — Keep Drizzle over Prisma

**Assessment: Agree**

The reasoning is correct: Drizzle is the more honest fit for a schema with CHECK constraints, partial indexes, pgvector, and tsvector. The AI-familiarity mitigation (pin Drizzle docs via Context7) is practical.

**Missing consideration — Drizzle and pgvector interop is immature:** As of mid-2026, Drizzle's pgvector support is community-driven, not first-party. You'll need the `drizzle-orm/pg-core` `customType` helper to define `vector(1024)` columns, and the `<=>` cosine distance operator requires raw SQL in `where` clauses (`sql\`embedding <=> ${queryVector}\``). This is workable but AI agents won't know the pattern without an explicit example in the schema file. **Write a reference query in a comment block** at the top of the schema — this is one of the rare cases where a comment has permanent value.

---

## R6 — Prioritize analytics earlier

**Assessment: Strongly Agree with the review's modified version**

The review correctly rejected the original recommendation's ordering (which put Marketplace before Analytics and Social, inverting the eligibility dependency). The adopted approach — move event *capture* to Phase 2, keep aggregation + dashboards in Phase 3 — is correct and is now in the phase plan.

**Missing consideration:** None. This was well-handled.

---

## R7 — Simplify to scroll milestones (drop paragraph-level)

**Assessment: Agree with the review's decision to reject this**

The review is correct: 50k rows is nothing for Postgres, paragraph-level analytics is the demo differentiator ("the AI knows which paragraphs your readers skip"), and the spec already has both granularities in the right places (per-paragraph for `article_metrics.paragraph_dropoff`, quartiles for `writer_quality_metrics.retention_curve`).

**Missing consideration — client-side deduplication:** The review says "harden the capture" but doesn't specify *how*. The real risk with `IntersectionObserver` paragraph tracking is **duplicate scroll events** — a user scrolling up and down generates multiple intersection entries for the same paragraph. The frontend must **deduplicate per session**: track which paragraph indexes have already been reported, only send each once per page load. Without this, `paragraph_dropoff` will be inflated and the heatmap will be meaningless. This is a 5-line fix but easy for an agent to miss.

---

## R8 — MVP focus; postpone likes/follows/reposts

**Assessment: Agree with the review's modified cut list**

The review correctly identified that likes + comments are load-bearing (eligibility = 1,000 reactions) and cannot be cut. The revised droppable features list in the phase plan is realistic and correctly prioritized.

**Missing consideration — the droppable list should include the AI Eval Harness.** It's already marked "optional" in Phase 5, but it's not in the droppable features list. It should be — it's a nice-to-have that competes with must-ship marketplace work in weeks 10–11.

---

## R9 — Integration testing early

**Assessment: Strongly Agree**

Ledger invariant tests as the first tests in the project is the right call. This is now specified in the phase plan (Phase 1) and in the database schema (§10.1).

**Missing consideration — what test infrastructure?** The spec says "first tests in the project" but doesn't specify the test setup. NestJS testing with a real PostgreSQL database (not mocks — per the review's philosophy) requires a test database container. The `docker-compose.yml` should include a `db-test` service or the tests should connect to the `db` service with a separate database name. Define this early or the first test session will be spent on infrastructure instead of writing assertions.

---

## R10 — Deploy on Vercel + Render + Neon

**Assessment: Strongly Agree with the review's rejection**

The review is correct: the Docker/VPS stack is already built, more defensible for an engineering thesis, and avoids a three-vendor fragmentation. The concession to optionally lift only Postgres to managed is reasonable.

**Missing consideration:** None. Well-argued.

---

## R11 — Observability (/health, /ready, Sentry)

**Assessment: Strongly Agree**

Now mandatory in the specs. Health checks are defined for all Docker services. Sentry integrated in both backend and frontend.

**Missing consideration — Sentry DSN management.** Sentry requires a DSN (data source name) injected as an environment variable. This should be in the `.env.example`. Minor but easy to forget.

---

## Review of the six identified risks

### Risk 1: Ledger dual-source-of-truth + concurrency

**Assessment: Correctly identified and now well-addressed.**

The schema now specifies `SELECT ... FOR UPDATE`, the two invariants, the reconciliation job, and ledger invariant tests. This is the most important single fix from the review. The remaining concern is that Drizzle's transaction API must be used correctly — `db.transaction(async (tx) => { ... })` with the `FOR UPDATE` inside the transaction scope. Test this with a concurrent purchase test (two async operations on the same magazine) to verify the lock holds.

### Risk 2: Demo threshold impossible to reach organically

**Assessment: Correctly identified and now addressed.**

`DEMO_MODE=true` with configurable thresholds + a seed script. The remaining concern is that the seed script must generate *believable* analytics data — not just random numbers but time-series patterns that look organic on dashboards. This is polish, not architecture.

### Risk 3: Cohere free trial expiry

**Assessment: Correctly identified, partially addressed.**

The provider table now notes the trial risk and the OpenAI fallback. But the spec doesn't address **embedding compatibility**: if you switch from Cohere `embed-multilingual-v3.0` (1024 dimensions) to OpenAI `text-embedding-3-small` (1536 dimensions), you must **re-embed all existing chunks** — the vector dimensions don't match, so old and new embeddings can't be compared via cosine similarity. The `article_chunks.embedding` column is `VECTOR(1024)`.

**Alternative approach:** Use OpenAI `text-embedding-3-small` from the start. It's $0.02/1M tokens — at PFE scale (a few hundred chunks), the total cost is under $0.01. Eliminate the Cohere dependency entirely. Or if Cohere is kept, plan a re-embedding migration script and make the vector dimension a config value.

### Risk 4: RAG demo-fragile with thin corpus

**Assessment: Correctly identified, partially addressed.**

The seed script creates "10+ substantive articles" but the spec doesn't define *what kind* of articles. For convincing RAG, the demo writer needs articles with a **distinctive, consistent voice** — not generic lorem ipsum. Write 3–4 real articles in a specific style before the defense and use those as seed data. This is content work, not engineering, but it determines whether the headline feature lands.

### Risk 5: Free-tier RPM limits during live demo

**Assessment: Correctly identified, not sufficiently addressed.**

The spec mentions testing the fallback chain but doesn't specify a concrete mitigation. **Pre-warm the Portfolio Insights cache** for all demo writers before the defense starts. For AI chat, Groq's free tier allows ~30 requests/minute on Llama 3.3 70B — sufficient for a demo, but if multiple jury members are using the app simultaneously, you could hit it. Test with 3 concurrent users before the defense.

### Risk 6: Spec internal inconsistency

**Assessment: Now resolved.** All specs are consistent.

---

# Part 2 — Architecture Audit

## Strengths

### 1. Single data layer (PostgreSQL + pgvector + tsvector)
The decision to use one database for relational data, full-text search, and vector storage is unusually mature for a graduation project. It eliminates distributed-consistency bugs, reduces operational complexity, and is genuinely the right call at this scale. A jury member who has worked with microservices will recognize this as a deliberate, well-reasoned simplification — not laziness.

### 2. The locked financial ledger
The transactions table design — absolute amounts, directional types, idempotency keys, `SELECT ... FOR UPDATE`, invariant tests, reconciliation job — is production-grade. If implemented correctly, this is the single most impressive engineering artifact in the project. It demonstrates understanding of concurrent systems, financial correctness, and defensive programming.

### 3. Dual-purpose analytics (writer self-improvement + magazine decision support)
The insight that the same event pipeline serves both a writer's feedback loop and a magazine's purchase decision is strong product thinking. It gives analytics "economic gravity" — every metric has a downstream consequence, which is a compelling narrative for a defense.

### 4. RAG reuse (write-like-me + Portfolio Insights)
Using the same chunk infrastructure for two distinct use cases (writer-facing style matching and magazine-facing evaluation) is good architectural leverage. It means the RAG pipeline has double the justification and double the demo surface area.

### 5. The droppable features list
Explicitly ranking what to cut under time pressure — and distinguishing "never cut" items from optional polish — is unusual discipline for a student project. A jury will read this as project management maturity.

---

## Weaknesses

### 1. TipTap JSON → plain text extraction is completely unspecified

This is the biggest gap in the entire spec. The `articles` table stores content as `JSONB` (TipTap JSON), but three critical systems need plain text:

- **`content_search` (tsvector)** — must be populated from the article content for full-text search
- **Article chunking (RAG)** — must extract paragraph-level plain text for embedding
- **Word count / read time** — computed from text length

TipTap JSON is a nested ProseMirror document tree (`{ type: "doc", content: [{ type: "paragraph", content: [{ type: "text", text: "..." }] }] }`). Extracting plain text requires recursively walking this tree.

**What to specify:**
- A shared utility function `extractTextFromTipTap(json: TipTapDoc): string` that recursively extracts text
- A variant `extractParagraphs(json: TipTapDoc): string[]` that returns one string per paragraph node (for chunking)
- Whether `content_search` is populated by a PostgreSQL trigger or by the application layer on insert/update
- Recommendation: application-layer population via Drizzle — a trigger would need custom SQL migration and is harder to test

### 2. Aggregation query correctness is underspecified

The spec defines *what* metrics are computed (unique readers, returning reader rate, geographic distribution, device split, paragraph-level dropoff, coefficient of variation for posting consistency) but never defines *how*. These are complex SQL queries:

- **Returning reader rate:** `COUNT(DISTINCT viewer_id WHERE viewed_2_plus_articles) / COUNT(DISTINCT viewer_id)` — requires a subquery or CTE
- **Geographic distribution:** `GROUP BY metadata->>'viewer_country'` with percentage calculation — requires JSONB extraction
- **Posting consistency (coefficient of variation):** `STDDEV(inter_publication_days) / AVG(inter_publication_days)` — requires computing gaps between `published_at` timestamps
- **Paragraph-level dropoff:** `MAX(paragraph_index)` per view session, then percentage at each index — requires session grouping

An AI agent will write plausible-but-wrong versions of these. The aggregation worker is the system where **wrong numbers look right** — there's no invariant test that catches "returning reader rate is 0.45 but should be 0.38." Consider writing the critical aggregation queries in pseudocode in the spec, or at minimum defining test fixtures with known-correct expected outputs.

### 3. The `users` table's conditional nullability creates type-system friction

The `users` table uses single-table inheritance: `account_type` determines which fields are valid. For `account_type = 'magazine'`, `role` and `plan` are NULL (enforced by CHECK constraint); for `personal`, they're NOT NULL.

In Drizzle's TypeScript types, all nullable columns are `string | null`. This means every piece of code that handles a personal user must assert `role !== null` and `plan !== null` even though the CHECK constraint guarantees it. AI agents will generate code that either:
- Doesn't handle the null case (runtime crash on magazine accounts)
- Over-handles it with unnecessary null checks on personal accounts

**Mitigation:** Define discriminated union types at the application layer:
```typescript
type PersonalUser = { accountType: 'personal'; role: Role; plan: Plan; ... }
type MagazineUser = { accountType: 'magazine'; role: null; plan: null; ... }
type User = PersonalUser | MagazineUser
```
Map from the Drizzle row type to these unions in the repository layer. This is a pattern AI agents need to see explicitly.

### 4. Refresh token storage is not in the schema

The auth spec says "JWT access token (15 min) + refresh token (7 days)" but there's no `refresh_tokens` table and no mention of Redis storage for refresh tokens. Stateless refresh tokens (JWT) can't be revoked on logout or password change. Stored refresh tokens need a table or a Redis key structure.

**Recommendation:** Store refresh tokens in Redis with key `refresh:{userId}:{tokenId}` and TTL 7 days. On logout, delete the key. On password change, delete all keys for that user. This is a 30-line implementation but needs to be designed before Phase 1.

### 5. MinIO signed URL upload conflicts with the network topology

The spec says "Upload via signed POST URLs to avoid routing media through the backend" but MinIO runs inside the Docker network (`minio:9000`). The browser can't POST directly to an internal container. Either:
- MinIO must be exposed through Nginx (add a `/storage` proxy path), or
- Uploads must route through a backend endpoint that proxies to MinIO

The first option is simpler and preserves the signed-URL benefit. Add an Nginx location block for `/storage` → `minio:9000`.

### 6. SSE connection architecture is underspecified

The specs mention SSE for two purposes:
- AI streaming responses (per-request, short-lived)
- Live notifications (per-session, long-lived)

These are architecturally different:
- AI SSE: opened by the AI request, streams tokens, closes when the response is complete. This is well-handled by the Vercel AI SDK's `streamText`.
- Notification SSE: opened on page load, kept alive for the session duration, requires heartbeats to prevent proxy timeouts (Nginx default is 60s).

The spec doesn't address: heartbeat interval, reconnection strategy (EventSource auto-reconnects but loses events during downtime), or whether these are one or two SSE connections. In NestJS, each SSE connection holds an open HTTP response, consuming a connection slot. Define the heartbeat (30s `:\n\n` comment) and test that Nginx doesn't kill the connection.

---

## Top Technical Risks (ranked)

### 1. Analytics aggregation correctness (HIGH)
**Why:** Complex SQL queries operating on JSONB metadata fields, producing dashboard numbers that look plausible even when wrong. No invariant test catches incorrect engagement rates or geographic distributions. Silent failures. This is the subsystem most likely to produce bugs that are never detected until the defense, when a jury member asks "how is this number computed?"

### 2. Transaction concurrency and ledger integrity (HIGH, but well-mitigated)
**Why:** The spec now addresses this with `SELECT ... FOR UPDATE` and invariant tests. The risk is *implementation*, not *design* — an AI agent may not use Drizzle's transaction API correctly, or may forget the `FOR UPDATE` clause. Write the first purchase flow by hand, not by AI, and verify the lock with a concurrent test.

### 3. TipTap integration complexity (MEDIUM-HIGH)
**Why:** Rich text editors are historically the most time-consuming frontend integration. TipTap extensions, image upload via MinIO, auto-save with debouncing, and the inline editing popup (AI actions on selected text) create a dense interaction surface. The AI chat panel + inline popup are two custom UI components that must integrate with TipTap's selection and transaction APIs. Estimate 2x the time you think this will take.

### 4. AI provider reliability during live demo (MEDIUM)
**Why:** Free-tier rate limits on Groq/Gemini/Cohere. The fallback chain is designed but untested. Pre-warm caches, test with concurrent users, and have the backup demo video ready.

### 5. RAG quality with thin corpus (MEDIUM)
**Why:** 5–10 articles may not produce convincing "writes like me" results. The structured memory helps stabilize voice, but the demo needs articles with a real, distinctive style — not AI-generated placeholder content.

### 6. Drizzle + pgvector + tsvector interop (MEDIUM)
**Why:** Drizzle's pgvector support requires `customType`, raw SQL for vector operations, and manual tsvector population. These are non-standard patterns that AI agents haven't seen often. The first migration will surface compatibility issues.

### 7. Frontend dashboard complexity (MEDIUM)
**Why:** Four distinct dashboard surfaces (writer analytics, magazine evaluation, writer earnings, magazine library) each with charts, tables, and filters. Charting libraries (recharts, nivo, chart.js) add bundle size and API learning curves. The magazine evaluation page alone has four panels (audience, content, quality, portfolio insights).

### 8. Docker Compose + VPS deployment during demo (LOW-MEDIUM)
**Why:** You've already built the compose stack in Phase 0. The risk is operational: VPS disk space, OOM kills on a 4GB machine running 7 containers + Postgres + HNSW indexes. Monitor memory usage during load testing. The Hetzner CX22 at 4GB RAM is tight for 7 containers — consider the CX32 (8GB) if budget allows.

---

## Overengineering Check

### Overengineered for a solo engineer

1. **Three separate writer metrics rollup tables** (`writer_audience_metrics`, `writer_content_metrics`, `writer_quality_metrics`). These are aggregated at the same frequency (15 min) by the same worker. A single `writer_metrics` table with all columns would be simpler, require one aggregation job instead of three, and produce one dashboard query instead of three. The split would make sense if different teams owned different metrics — they don't. **Recommendation:** merge into one table. This cuts 2 BullMQ jobs and simplifies the aggregation worker.

2. **Magazine subscription renewal history** (`magazine_subscriptions` table with `renewed_from_id` chain). For a simulated-payment MVP, a simple `subscription_status` + `expires_at` on `magazine_profiles` is sufficient. The renewal history is future-proofing for Stripe integration that won't happen in 14 weeks. **Recommendation:** keep the table in the schema (it's already defined), but deprioritize the renewal cron job. Activate subscriptions with a simple API call that sets status + expiry directly.

3. **Writer eligibility audit log.** Nice for compliance, but in a PFE with ≤ 5 eligibility grants, a log entry in the application logs is sufficient. **Recommendation:** keep the table (it's cheap), but don't spend time building an admin UI for it.

4. **Platform fee as a stored field per transaction.** If the fee is always a fixed percentage (e.g., 10%), computing it on read is simpler than storing it on each row. **Recommendation:** define the fee percentage as a config constant, compute it in the purchase flow, store it on the transaction row for auditability. This is actually NOT overengineered — the stored field is correct for a financial ledger. Keep it.

### Low value relative to implementation effort

1. **AI Eval Harness** (Phase 5, optional) — LLM-as-judge scoring of AI actions. High implementation effort (define test cases, build evaluation pipeline, score parsing) for a feature that won't be shown in the defense. Drop it.

2. **Dynamic OG images** (Phase 6) — Next.js `ImageResponse` for social sharing. Zero demo value during a defense. Drop it.

3. **Cookie consent / analytics opt-out** (Phase 6) — GDPR compliance polish. Not needed for a PFE demo. Drop it.

4. **Content moderation via OpenAI Moderation API** — Interesting technically but not a differentiator. A basic report queue (already in the plan) is sufficient.

---

## Missing Architecture Decisions

These need to be resolved before implementation:

1. **TipTap JSON → plain text extraction:** define the utility function, decide trigger vs application-layer for tsvector population
2. **Refresh token storage:** Redis vs database, key structure, revocation strategy
3. **Platform fee structure:** percentage, configurable constant, where defined
4. **MinIO Nginx proxy:** add `/storage` location block to Nginx config
5. **SSE heartbeat and reconnection:** interval, Nginx timeout override, notification SSE lifecycle
6. **CORS configuration:** NestJS CORS settings for local development (without Nginx)
7. **Test database setup:** separate container? separate database name? connection string for tests?
8. **RRF implementation location:** service-layer merge in `SearchService`, not raw SQL
9. **Memory extraction input scope:** most recent N articles vs full corpus vs RAG chunks
10. **Vector dimension strategy:** commit to 1024 (Cohere) or switch to 1536 (OpenAI) before writing the schema

---

# Part 3 — Direct Answers

## 1. If you were the technical lead, what would you change before writing the first line of production code?

Five things, in order:

1. **Resolve the embedding provider now.** Either commit to Cohere with a concrete fallback plan (re-embedding script, dimension-agnostic column), or switch to OpenAI `text-embedding-3-small` from day 1. The Cohere trial expiry is a time bomb you can defuse for $0.01.

2. **Write the TipTap → plain text extraction utility spec.** Every AI agent session that touches tsvector, chunking, or word count will need this. Define it once, in one place, before anyone writes code.

3. **Merge the three writer metrics rollup tables into one.** This removes two aggregation jobs, simplifies the worker, and reduces the dashboard query surface from three tables to one.

4. **Define refresh token storage in Redis** with a clear key structure and revocation semantics. This is a security gap that will block the auth implementation.

5. **Prototype the Drizzle schema** — just the schema file, not the modules — and verify that pgvector `customType`, CHECK constraints, partial indexes, and tsvector all work in a single `drizzle-kit push`. This is a 2-hour investment that could save a week.

## 2. What implementation order would you recommend?

Keep the existing Phase 1–6 structure with these adjustments:

**Phase 1 (weeks 2–3):** Schema + Auth + Articles + Ledger tests  
- Drizzle schema (all tables, verified with `drizzle-kit push`)  
- Auth (email/password, JWT, refresh tokens in Redis — defer Google OAuth to Phase 3)  
- Articles CRUD (create, publish, feed, slug)  
- Ledger invariant tests (against manual transaction inserts)  
- TipTap → text extraction utility  

**Phase 2 (weeks 4–5):** Editor + AI + Event capture + Observability  
- TipTap editor (formatting, image upload, auto-save)  
- AI chat + inline editing (Vercel AI SDK, SSE streaming)  
- Analytics event capture (view, scroll, time-on-page) — data accrues from here  
- Health/ready endpoints + Sentry  

**Phase 3 (weeks 6–7):** Social + Aggregation + Dashboards  
- Likes + comments (load-bearing for eligibility)  
- Follows (if time; droppable)  
- Aggregation workers (article metrics, writer metrics)  
- Writer dashboard + magazine evaluation dashboard  

**Phase 4 (weeks 8–9):** RAG + Portfolio Insights + Search  
- Embedding pipeline (Cohere/OpenAI → pgvector)  
- Writer-facing RAG (chat enhanced with chunks)  
- Portfolio Insights (magazine-facing, Zod-validated)  
- Hybrid search (tsvector + pgvector + RRF)  
- Memory extraction pipeline  

**Phase 5 (weeks 10–11):** Marketplace + Transactions  
- Magazine subscription (simulated)  
- Preview unlock + full purchase (atomic transactions with row locking)  
- Writer eligibility gating  
- Earnings dashboard + magazine library  
- Voice-to-article (if time; first to cut)  

**Phase 6 (weeks 12–14):** Deploy + Polish + Defense  
- VPS deploy (compose stack already built)  
- Demo/seed mode  
- Playwright E2E (critical paths only)  
- Reconcile-balances job  
- Defense prep (docs, slides, demo script, backup video)  

The main change from the current plan: Google OAuth deferred from Phase 1 to Phase 3 (it's OAuth plumbing, not a differentiator), and the TipTap text extraction utility is explicitly called out as a Phase 1 deliverable.

## 3. What subsystem would you prototype first?

**The Drizzle schema with pgvector + tsvector + CHECK constraints.**

This is the single artifact most likely to surface problems early. Create a minimal `schema.ts` with:
- The `users` table (with CHECK constraint for account_type/role/plan)
- The `articles` table (with tsvector column and GIN index)
- The `article_chunks` table (with `vector(1024)` column and HNSW index)
- A partial index on `deleted_at IS NULL`

Run `drizzle-kit push` against a local Postgres with pgvector. If everything works, you have confidence. If Drizzle can't handle the `vector` type or the CHECK constraint, you know immediately and can write raw SQL migrations.

This is a 2-hour prototype that could save a week of debugging in Phase 1.

## 4. What subsystem would you be most worried about?

**Analytics aggregation correctness.**

This is the subsystem where:
- The queries are complex (unique readers across multiple articles, JSONB metadata extraction, coefficient of variation, paragraph-level dropoff curves)
- Wrong numbers look right (a dashboard showing 42% engagement rate when it should be 38% won't trigger any alarm)
- There are no automatic invariant tests (unlike the ledger, where snapshot == sum is testable)
- The data flows through a multi-step pipeline (events → raw table → aggregation worker → metrics table → API → dashboard), and a bug at any stage propagates silently
- AI agents will write plausible-but-wrong SQL (particularly for returning reader rate and posting consistency)

**Mitigation:** Write the critical aggregation queries by hand (not by AI), with test fixtures that have known-correct expected outputs. For example: seed 3 articles, 100 view events, 50 scroll events with known paragraph indexes, then assert the aggregated metrics match hand-calculated values.

## 5. What subsystem would most impress an engineering jury if implemented correctly?

**The locked financial ledger with invariant tests and reconciliation.**

This demonstrates:
- Understanding of concurrent systems (row-level locking with `SELECT ... FOR UPDATE`)
- Financial correctness (double-entry-style ledger, idempotency keys, atomic transactions)
- Defensive programming (invariant tests, reconciliation job, drift alerting)
- Real software engineering (not just feature building — infrastructure that prevents a class of bugs)

A jury member who has worked on production systems will immediately recognize this as unusually mature for a student project. It also creates a natural defense talking point: "I chose to implement balance-denormalization with row locking rather than computing from the ledger on every read, because..." — this is a genuine architectural trade-off discussion, not a rehearsed answer.

The RAG + Portfolio Insights pipeline is a close second (it's technically interesting and visually impressive), but it's more "tech demo" than "engineering discipline." The ledger is engineering; the RAG is product. Both matter, but the ledger is rarer in student projects.

## 6. What are the top 5 things most likely to cause schedule overruns?

1. **TipTap editor integration** — Rich text editors are historically the most time-consuming frontend integration. TipTap extensions, image upload (MinIO signed URLs through Nginx), auto-save with debouncing, the AI inline editing popup (intercepting text selection, positioning the popup, replacing content in the editor transaction) — this is dense, fiddly UI work. AI agents can scaffold the basics but the edge cases (cursor position after replacement, undo/redo with AI edits, image paste handling) consume days. **Budget 50% more time than estimated.**

2. **Analytics aggregation queries** — Writing correct SQL for unique readers, returning reader rate, geographic distribution from JSONB, posting consistency as coefficient of variation, and paragraph-level dropoff — each query takes 30–60 minutes to write and verify, with subtle gotchas (null viewer_id for guests, timezone handling in time-on-page, deduplicating scroll events). Four aggregation jobs × 5–8 metric computations each = 20–30 non-trivial SQL queries. **This is a full week of work, not a few hours.**

3. **The marketplace purchase flow** — The two-stage purchase (preview + buy) with atomic transactions, row locking, idempotency keys, credit validation, balance updates, parent_purchase_id linking, and transaction row insertion is the most complex single API endpoint in the system. Getting the Drizzle transaction API right, testing the row lock with concurrent requests, handling edge cases (insufficient credits mid-transaction, preview but never purchase, direct purchase without preview) — this is the hardest piece of backend code. **Write and test this by hand, not by AI agent.**

4. **Frontend dashboard UI** — Four distinct dashboard views (writer analytics, magazine evaluation, writer earnings, magazine library), each with charts (recharts or similar), data tables, filters, and responsive layouts. The magazine evaluation page alone has four panels plus the Portfolio Insights async-loaded section. Chart integration, loading states, error states, empty states, mobile responsiveness — this is a lot of UI work. **Consider using a dashboard template or component library (shadcn charts) to reduce custom code.**

5. **SSE streaming + Nginx configuration** — AI streaming via SSE requires Nginx to not buffer the response (`proxy_buffering off`), the NestJS response to flush correctly, and the frontend to handle partial token streams. Notification SSE requires long-lived connections with heartbeats that survive Nginx's proxy timeout. These are infrastructure concerns that produce "works locally, breaks in Docker" bugs. **Test through Nginx from the start, not just with direct API calls.**

---

# Final Assessment

The Inkwell specification, after two rounds of architecture review, is **unusually well-designed for a graduation project**. The core architectural decisions (single data layer, consolidated AI orchestration, dual-purpose analytics, locked financial ledger) are genuinely strong and defensible.

The primary remaining risks are not in the architecture — they're in the **implementation**: getting the aggregation SQL right, making TipTap + AI integration smooth, and shipping the marketplace transaction flow with correct concurrency handling.

The 14-week timeline is achievable if scope is managed aggressively. The droppable features list is realistic. The critical path is: **schema → auth → editor → AI → analytics → RAG → marketplace → deploy**. Everything else is polish.

The system you've designed would be impressive at a professional level, not just an academic one. The challenge now is building it.
