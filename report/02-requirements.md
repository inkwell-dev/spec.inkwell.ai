# Chapter 2 — Requirements analysis and specification

## Introduction

This chapter specifies what the platform must do. It identifies the actors, states the
functional requirements per actor and the non-functional requirements, presents the
global use case diagram and the global class diagrams, and then organises the work as a
product backlog of user stories distributed over a release plan and a schedule.

## 2.1 Identification of the actors

The platform has eight actors. They are not independent: they generalise one another,
mirroring the three independent properties every account carries in the data model —
its **account type** (personal or magazine), its **role** (reader, writer or
administrator) and its **plan** (free or premium) — plus the writer's marketplace
eligibility. Table 2.1 lists them.

**Table 2.1 – Actors of the system**

| # | Actor | Data-model representation | Definition |
|---|---|---|---|
| A1 | Visitor | no account | Unauthenticated. Sees the public feed and free article bodies; cannot interact. |
| A2 | Free reader | personal account, free plan | Reads free public articles, interacts socially, has no AI allowance. |
| A3 | Premium reader | personal account, premium plan | Everything A2 has, plus premium articles and the daily AI allowance. |
| A4 | Writer | role writer | A2/A3 plus drafting, publishing and editing their own articles. |
| A5 | Eligible writer | marketplace-eligible writer | A4 plus the right to publish premium articles and to list on the marketplace. |
| A6 | Magazine (unsubscribed) | magazine account, no active subscription | Registered magazine stopped at the subscription wall. |
| A7 | Magazine (subscribed) | magazine account, active subscription | Browses writers, reads evaluation reports, spends credits to preview and purchase. |
| A8 | Administrator | role admin | Moderation queue, user management, manual eligibility grants. |

Three generalisations hold: the premium reader generalises the free reader, the
eligible writer generalises the writer, and the subscribed magazine generalises the
unsubscribed one. Role and plan are deliberately independent: a writer may stay on the
free plan and write without AI assistance. The administrator role cannot be obtained
through the interface; it is granted directly in the database.

## 2.2 Functional requirements

The functional requirements are stated per actor, each with a stable identifier, a
MoSCoW priority and the sprint that delivers it. Identifiers are stable rather than
sequential: a requirement added later keeps the next free number and is listed beside
the feature it belongs to.

### 2.2.1 Visitor (A1)

**Table 2.2 – Functional requirements of the visitor**

<!-- INCLUDE:fr-2.1 -->

Free public articles are deliberately readable without an account: gating them would
contradict the public feed and its search-engine visibility.

### 2.2.2 Free and premium reader (A2, A3)

**Table 2.3 – Functional requirements of the readers**

<!-- INCLUDE:fr-2.2 -->

### 2.2.3 Writer and eligible writer (A4, A5)

**Table 2.4 – Functional requirements of the writers**

<!-- INCLUDE:fr-2.3 -->

Voice in this product is the *voice prompt* of FR-82, which dictates a request to the
assistant; dictating a whole article is outside the scope of the project.

### 2.2.4 Magazine (A6, A7)

**Table 2.5 – Functional requirements of the magazines**

<!-- INCLUDE:fr-2.4 -->

Portfolio Insights generation is an explicit action rather than a side effect of
opening a page, because each generation costs a model call.

### 2.2.5 Administrator (A8)

**Table 2.6 – Functional requirements of the administrator**

<!-- INCLUDE:fr-2.5 -->

Several refusals are enforced server-side, each pinned by a test: the administrator
role cannot be assigned, an administrator's role cannot be edited, nobody can edit
their own role or plan, a banned account cannot be edited, and a magazine cannot be
given a role.

### 2.2.6 Cross-cutting requirements

**Table 2.7 – Cross-cutting functional requirements**

<!-- INCLUDE:fr-2.6 -->

## 2.3 Non-functional requirements

Each non-functional requirement is stated as a property together with the mechanism
that provides it, so that it can be verified rather than asserted. Table 2.8 groups
them by quality attribute.

**Table 2.8 – Non-functional requirements**

| ID | Requirement | Mechanism |
|---|---|---|
| **Security** | | |
| NFR-01 | Passwords stored as bcrypt hashes, cost factor 12 | authentication module |
| NFR-02 | Access tokens expire after 15 minutes, refresh tokens after 7 days | signed JWTs; the refresh token is stateless, so its lifetime is the bound on its validity |
| NFR-03 | Every protected route passes one composed guard stack | a single `@Auth()` decorator composing JWT, role, plan, account-type, subscription and AI-quota guards |
| NFR-04 | Authorisation is decided server-side; the client is told the verdict | the article access matrix evaluated by the API; locked content arrives as `null` |
| NFR-05 | Per-address rate limits on every endpoint, tighter on credential routes | 60 requests/min globally, 10/min on sign-in, 5/min on registration |
| NFR-06 | Financial operations are idempotent under retry | a unique idempotency key on every ledger transaction |
| NFR-07 | Uploads are presigned, time-limited and never routed through the API | 10-minute presigned PUT; the public bucket grants object reads only |
| NFR-08 | Datastore ports bind to the loopback interface only | Compose port bindings on `127.0.0.1` |
| NFR-09 | A ban takes effect at the next authentication | soft-deletion checked on sign-in, refresh and Google sign-in |
| NFR-10 | No stored HTML is ever rendered as markup | no raw-HTML rendering anywhere in the frontend |
| **Performance** | | |
| NFR-11 | Semantic retrieval stays sub-linear as the corpus grows | HNSW index on the embedding column (m = 16, ef_construction = 64) |
| NFR-12 | Full-text search is index-backed with weighted ranking | generated `tsvector` column with weights A/B/C and a GIN index |
| NFR-13 | Prompt context is bounded | at most 5 retrieved passages, a memory block under 200 tokens, about 2,000 tokens in total |
| NFR-15 | Dashboard totals and rates read pre-aggregated rows | four rollup tables refreshed by the worker |
| NFR-16 | Analytics aggregation is incremental and idempotent | each run reads only the events since the last one |
| NFR-17 | Expensive AI output is cached and invalidated by what changes it | portfolio insights cached 24 h and dropped when the writer publishes |
| NFR-18 | Streaming responses are never buffered end to end | nginx `proxy_buffering off` and a 300 s read timeout on streaming routes |
| **Reliability** | | |
| NFR-19 | Every denormalised balance equals the sum of its ledger rows | three invariants asserted after every money-moving test |
| NFR-20 | Concurrent purchases cannot double-spend | `SELECT … FOR UPDATE` on the balance-owning row inside the transaction |
| NFR-21 | Schema changes are versioned and applied before the application starts | a one-shot migration service the API and worker depend on |
| NFR-23 | Failed background jobs retry with exponential back-off | three attempts per job |
| NFR-24 | An AI provider outage degrades AI only | a model chain falling back from Groq to Gemini; the rest of the product is unaffected |
| NFR-25 | Every service reports liveness and readiness | `GET /health` and `GET /ready` |
| **Scalability** | | |
| NFR-26 | The API holds no session state | identity carried by JWT claims |
| NFR-27 | Long-running work never runs in the request path | six BullMQ queues consumed by a separate worker process |
| NFR-28 | API and worker scale horizontally behind the proxy | stateless containers, one Compose service each |
| **Maintainability** | | |
| NFR-29 | Both code bases compile in strict mode with zero lint warnings | `tsc --noEmit`, `eslint --max-warnings=0` in continuous integration |
| NFR-30 | The API contract is generated from OpenAPI | client types generated from the backend's OpenAPI document |
| NFR-31 | Business rules are tested, not asserted | 792 backend tests in 51 suites; 183 end-to-end tests in 25 files |
| NFR-32 | The build fails when schema and migrations disagree | a schema-drift check in continuous integration |
| NFR-33 | Errors are captured in every runtime without personal data | Sentry in API, worker, Next.js server and browser |
| **Usability** | | |
| NFR-34 | Two breakpoints are designed and implemented | 375 px and 1280–1440 px |
| NFR-35 | One design system, applied consistently | 39 design tokens and 87 components in Figma |
| NFR-36 | A complete dark mode | theme switch across every screen |
| NFR-37 | Lighthouse score above 90 and no critical accessibility violation on article pages | planned — see the general conclusion |

## 2.4 Global use case diagram

Figure 2.1 gives the global use case diagram. It is deliberately coarse: each use case
stands for a family of interactions refined in the per-sprint diagrams of Chapters 4
to 7. Every authenticated use case includes *Sign in*; *Sign in with Google* extends
it; listing on the marketplace extends publishing; unlocking a preview extends
acquiring an article; grounding answers in uploaded documents extends the use of the
assistant, which always includes retrieval from the writer's own corpus.

![Figure 2.1 – Global use case diagram](../diagrams/fig-2-1-use-case-global/fig-2-1-use-case-global.png){width=100%}

## 2.5 Global class diagram

The data model counts thirty persisted tables. Drawn in a single diagram they form an
unreadable strip, because the `User` class is related to most of the others, so the
global class diagram is split by domain into two figures. Attributes are shown with
domain types (`Json`, `Vector`, `Timestamp`); audit columns are omitted, and no
methods are shown because the model is relational and its behaviour lives in the
service layer.

**Core domain.** Figure 2.2 shows accounts, articles and their social layer: the
`User` and its optional `MagazineProfile`, the `Article` with its placement, visibility
and price, tags, threaded comments, likes, comment likes, reposts, saves, follows,
blocks, notifications and reports. `Article.publisherId` names the magazine that
published a licensed article and is empty for every other article.

![Figure 2.2 – Class diagram: core domain](../diagrams/fig-2-2-classes-core-domain/fig-2-2-classes-core-domain.png){width=100%}

**AI, marketplace and analytics.** Figure 2.3 shows the remaining sixteen tables: the
article chunks embedded for retrieval, the writer memory, the cached portfolio
insights and the AI interaction log; the private document library with its chunks and
article attachments; purchases, ledger transactions, magazine subscriptions and the
eligibility audit log; and the raw analytics events with the four metric rollups.

![Figure 2.3 – Class diagram: AI, marketplace and analytics](../diagrams/fig-2-3-classes-ai-marketplace-analytics/fig-2-3-classes-ai-marketplace-analytics.png){width=100%}

## 2.6 Product backlog

The product backlog expresses the requirements as user stories of the form *"As an
⟨actor⟩, I want ⟨goal⟩ so that ⟨benefit⟩"*. Stories are grouped into nine epics,
prioritised with MoSCoW and estimated in story points on a Fibonacci scale relative to
the simplest story (US-01). The backlog counts **72 stories for 345 points**. Table 2.9
summarises it by epic; the full backlog follows.

**Table 2.9 – Product backlog by epic**

<!-- INCLUDE:backlog-summary -->

<!-- INCLUDE:backlog -->

## 2.7 Release plan

The stories are delivered in four releases of two or three sprints each, every sprint
lasting two weeks. Table 2.10 gives the plan; the foundation week and the three-sprint
design track are not sprints, because they deliver no user-facing increment, and are
presented with the working environment in Chapter 3.

**Table 2.10 – Release plan**

| Release | Chapter | Sprint | Dates | Goal |
|---|---|---|---|---|
| **R1 — Functional foundation** | 4 | Sprint 1 | 09/02 – 20/02 | Schema, authentication, article core, ledger invariant harness |
| | | Sprint 2 | 06/04 – 17/04 | Editor, AI chat and inline actions, analytics event capture |
| **R2 — Social, analytics and AI** | 5 | Sprint 3 | 20/04 – 01/05 | Social interactions, notifications, aggregation, dashboards |
| | | Sprint 4 | 04/05 – 15/05 | Retrieval-augmented generation, portfolio insights, hybrid search, writer memory |
| **R3 — Marketplace, testing and deployment** | 6 | Sprint 5 | 18/05 – 29/05 | Marketplace, subscriptions, premium, moderation, administration |
| | | Sprint 6 | 01/06 – 12/06 | Tests, demo mode, deployment, CI/CD |
| **R4 — Social depth, assistant and documents** | 7 | Sprint 7 | 15/06 – 26/06 | Comment likes, follower lists, block, save, share |
| | | Sprint 8 | 29/06 – 10/07 | Live card controls, reposts tab, byline preview, assistant writing into the document, voice |
| | | Sprint 9 | 13/07 – 24/07 | Document library, ingestion, attachment, citations |

## 2.8 Schedule

Figure 2.4 places the work on the project window, from 2 February to 31 July 2026:
the foundation week and Sprint 1, the design track, Sprints 2 to 9 in four releases,
and the writing of this report alongside the last sprints.

![Figure 2.4 – Gantt chart of the project](../diagrams/fig-2-4-gantt/fig-2-4-gantt.png){width=100%}

## Conclusion

This chapter identified the eight actors of the platform, specified its functional and
non-functional requirements, presented the global use case and class diagrams, and
organised the work into a backlog of 72 user stories delivered by nine sprints in four
releases. The next chapter describes the environment in which the work was done and
the architecture of the system.

\newpage
