# Working environment and architecture {#sec:ch2}

## Introduction {.unnumbered}

Before the release chapters, this chapter describes the environment the platform was
built in: the hardware and software used, the work that preceded the feature sprints,
the technological choices compared with their alternatives, the main parameters of
the system and their justification, and the architecture of the system — its logical
decomposition on the frontend and the backend, its physical deployment and its
delivery pipeline.

## Working environment

### Hardware environment

The project was developed and every measurement of Chapter 7 was taken on a single
workstation, described in @tbl:hardware. A mid-range laptop is a deliberate baseline:
the whole stack of eight containers runs on it, so the performance figures reported
later are those of commodity hardware, not of a server.

| Component | Specification |
|:--------------------|:----------------------------------|
| Machine | Lenovo ThinkPad |
| Processor | Intel Core i7-1355U |
| Memory | 24 GB RAM |
| Graphics | NVIDIA GeForce MX550 |
| Storage | 512 GB NVMe SSD |
| Operating system | Ubuntu Linux |

: Hardware environment {#tbl:hardware}

### Software environment

@tbl:software lists the tools used outside the application code itself. They share a
principle: every artefact — code, diagrams, this report — is kept as text under
version control, and everything that runs, runs in a container.

| Tool | Use |
|:----------------------------|:----------------------------------------------------|
| JetBrains IDE | code editor |
| Git and GitHub | version control, pull requests, continuous integration (GitHub Actions) and container registry (GHCR) |
| Docker and Docker Compose | containers for every service, in development and in production [@composedocs] |
| Figma | design system and screen design |
| PlantUML and draw.io | UML and architecture diagrams, kept as versioned sources |
| Swagger UI | exploring the REST API through the OpenAPI document the backend generates |
| Playwright | end-to-end tests and the capture of this report's screenshots [@playwrightdocs] |
| Pandoc and LuaLaTeX | assembling and typesetting this report from its Markdown sources |

: Software tools {#tbl:software}

### Foundation and design track

Two blocks of work preceded the feature sprints and are presented here rather than as
sprints, because neither delivers a user-facing increment.

- **Foundation (one week).** The three repositories, their Docker images, the Compose
  stack, the reverse proxy and the continuous-integration pipeline were set up first,
  so that every later sprint started from a stack that builds, tests and runs with one
  command.
- **Design track (three sprints).** The user interface was designed in Figma before the
  editor and the social features were built: a design system of **39 tokens and 87
  components**, then the full screen set at two widths — **375 px for mobile and
  1280–1440 px for desktop**, 58 screens — then an audit of the screens against the
  specification. The release chapters implement these designs.

### Repository organisation

The source code lives in four Git repositories. `docker.inkwell.ai` is the
superproject: it holds the Compose files, the nginx configuration, the deployment
workflow and the developer Makefile, and it carries the three others as **Git
submodules** — `backend.inkwell.ai`, `frontend.inkwell.ai`, and `spec.inkwell.ai`, which
holds the specifications, the diagrams and this report. A commit of the superproject
therefore identifies one exact, deployable revision of the whole system.

## Technological choices {#sec:tech}

Each choice below is compared with the alternatives that were considered and the
criteria that decided between them, with a source for every claim that is not a
property of the project itself.

### Frontend

@tbl:tech-frontend gives the frontend stack. Its central decision is the web framework:
the platform's public pages — the feed, articles, profiles — must be rendered on the
server so that search engines and link previews see their content, while the editor
and the assistant are interactive applications.

| Choice | Alternatives considered | Deciding criteria |
|:-------------------------|:----------------------|:------------------------------------------|
| **Next.js 16** (App Router) with **React 19** | Remix, Nuxt (Vue), a client-only React application | server rendering per route for public pages and a request proxy for protected routes, in the most used React framework [@nextjsdocs; @stateofjs2024]; a client-only application would serve empty HTML to search engines |
| **TypeScript** (strict) | JavaScript | one typed language from the database schema to the browser; the API client types are generated from the backend (NFR-30) |
| **Tailwind CSS 4** with accessible headless primitives | CSS modules, a component library such as MUI | the Figma tokens map directly to utility classes; headless primitives give accessible dialogs and menus without imposing a visual style |
| **TipTap 3** | Lexical, Slate, Quill | built on ProseMirror, stores the document as JSON, and accepts custom extensions — the protected range the assistant writes into needs one [@tiptapdocs] |
| **TanStack Query 5** and **Zustand 5** | Redux Toolkit | server state (caching, invalidation, optimistic updates) and client state handled separately, with far less code than a single global store |
| **Vercel AI SDK** (React bindings) | hand-written stream parsing | consumes the assistant's typed stream of text, status and write parts [@aisdkdocs] |

: Frontend technologies compared with their alternatives {#tbl:tech-frontend}

### Backend

@tbl:tech-backend gives the backend stack. Its two structuring decisions are the
framework, which must host both an HTTP API and a background worker, and the data
store, which must hold relational data, full-text search and vector search.

| Choice | Alternatives considered | Deciding criteria |
|:-------------------------|:----------------------|:------------------------------------------|
| **NestJS 11** | Express or Fastify alone | modules, dependency injection, guards and OpenAPI generation built in [@nestjsdocs]; the same modules serve the API and the worker. Fastify is faster in raw benchmarks [@techempower2025], but the API's latency is dominated by the database and the model calls (@sec:eval-perf), not by the HTTP layer |
| **PostgreSQL 16 + pgvector** | PostgreSQL with a separate vector database (Qdrant, Pinecone) | relational data, full-text search and vector search in one database [@pgvector2026; @postgres16fts]: an article and its embeddings change in one transaction and are never out of sync, and there is one service less to run. HNSW, the index pgvector offers, is among the best recall-per-latency trade-offs in public benchmarks [@aumuller2020annbench] |
| **Drizzle ORM** | Prisma, TypeORM | SQL-shaped, type-safe queries with explicit migrations [@drizzledocs]; the purchase transaction needs `SELECT … FOR UPDATE` and the search needs `ts_rank` and vector operators, which Drizzle writes directly |
| **Redis 7 + BullMQ** | RabbitMQ, PostgreSQL-based queues | repeatable jobs, priorities and a separate worker process on one Redis instance [@bullmqdocs]; Redis also carries the notification fan-out |
| **MinIO** | storing files in PostgreSQL, a cloud bucket | the S3 API, so the same presigned-upload code runs against a cloud bucket in production; files never pass through the API |
| **Passport** (JWT, Google OAuth 2.0) and **bcrypt** | an external identity provider | standard strategies [@rfc7519; @rfc6749] with the session data kept in the platform's own database |

: Backend technologies compared with their alternatives {#tbl:tech-backend}

### Artificial-intelligence services

@tbl:tech-ai lists the models and why each was chosen. Two constraints shaped all of
them: the project runs on providers' free tiers, and a model that is slow to *start*
answering makes the assistant feel broken, whatever its quality.

| Use | Model | Alternatives considered | Deciding criteria |
|:--------------------|:-----------------------|:--------------------|:-----------------------------------|
| Chat, writing, inline actions, insights, writer memory | Groq `gpt-oss-120b`, then `gpt-oss-20b`, then Google `gemini-3.5-flash` | OpenAI API, a single provider | Groq serves open-weight models on dedicated inference hardware with a generous free tier [@groqdocs]; a second provider makes an outage degrade the assistant only (NFR-24) |
| Embeddings | Google `gemini-embedding-001`, 1,536 dimensions | OpenAI embeddings, a local model | separate task types for queries and documents [@geminiembeddings]; its free tier covered the corpus |
| Speech-to-text | Groq `whisper-large-v3-turbo` | browser speech recognition | same provider as the chat; multilingual; works in every browser |
| Text-to-speech | Google `gemini-2.5-flash-preview-tts` | browser speech synthesis | a natural voice, identical in every browser |
| Moderation at publish | Groq `gpt-oss-20b` | a dedicated safety model (`gpt-oss-safeguard-20b`) | measured: precision 0.93 and recall 1.00 on a labelled set, while the dedicated model exceeded the time budget (@sec:eval-moderation) |

: AI models, their alternatives and the reasons for the choice {#tbl:tech-ai}

The chain of chat models is what makes a provider outage degrade the assistant only:
the first chunk of a response is pulled before anything is sent to the browser, so a
refusal from one model can still be answered by the next. The moderation classifier is
the one choice settled by measurement rather than by documentation; Chapter 7 reports
the measurement.

### Infrastructure and quality

**Docker Compose** runs eight services — nginx, web, api, worker, a one-shot migration
service, PostgreSQL, Redis and MinIO. **nginx** terminates TLS and routes traffic.
**GitHub Actions** runs the quality gates and builds the images; **GHCR** stores them.
**Jest** tests the backend against a real PostgreSQL database, **Playwright** drives a
real browser end to end, and **Sentry** captures errors in the four runtimes.
Kubernetes was considered and rejected: a single host with Compose is enough for the
expected load, and the containers are already stateless (NFR-26) should the platform
ever need an orchestrator.

## Main parameters and their justification {#sec:parameters}

The behaviour of the platform depends on a few numbers. @tbl:parameters gives each,
with its value and the reason for it — a source, a measurement, or a product decision
stated as such.

| Parameter | Value | Justification |
|:----------------------|:--------------------|:--------------------------------------------|
| Passages retrieved per question | 5 | enough context for an answer while keeping the prompt near 2,000 tokens (NFR-13) |
| Similarity floor for retrieval and search | 0.60 | measured: relevant passages score 0.66–0.84 and off-topic ones 0.52–0.66 (@sec:eval-rag) |
| Chunk length | 120 – 1,200 characters, prefixed by the nearest heading | a paragraph is the unit of meaning; shorter fragments embed poorly, longer ones mix topics |
| Fusion constant of RRF | k = 60 | the value recommended by the method's authors [@cormack2009rrf]; confirmed in @sec:eval-search |
| HNSW index | m = 16, ef_construction = 64 | pgvector's defaults, a balanced recall–build-time setting [@pgvector2026; @malkov2018hnsw] |
| Embedding width | 1,536 | supported output width of the model [@geminiembeddings]; fixed by the schema |
| Premium AI allowance | 20,000 tokens a day | product decision: about twenty long replies or sixty inline edits, a working day |
| Voice billing | 200 tokens per started minute, at most 5 minutes | product decision, so that dictation consumes the same allowance as typing |
| Preview price | 10% of the article's price | product decision, credited towards the purchase |
| Platform fee | 20% of each stage, rounded down | product decision; computed in integer basis points so that no amount is ever a float |
| Monthly credits | 500 per subscription | product decision; unspent credits roll over |
| Eligibility thresholds | 5,000 unique readers and 1,000 reactions | product decision: high enough that eligibility signals a real audience |
| Token lifetimes | 15 minutes (access), 7 days (refresh) | a short access token bounds how long a ban or a stolen token stays valid (NFR-09) |
| Rate limits | 60/min, 10/min on sign-in, 5/min on registration | enough for a reader, too few for password guessing |
| Password hashing | bcrypt, cost 12 | about 250 ms per hash: slow enough to make an offline attack expensive [@owasppasswords] |
| Presigned upload lifetime | 10 minutes | long enough for a slow mobile upload, short enough that a leaked URL is stale |
| Document limits | 10 MB, 200 pages, 20 per writer | bound the cost of ingestion and the size of the library |

: Main parameters of the system and their justification {#tbl:parameters}

The table shows three kinds of justification. The retrieval parameters are set by
measurement or by the literature, and Chapter 7 checks them. The security parameters
follow published guidance. The economic parameters — prices, fee, credits, thresholds
— are product decisions: they have no "correct" value, and they are named constants in
one place in the code precisely so that they can be changed as a decision rather than
discovered in a calculation.

## Logical architecture

### Frontend

@fig:arch-frontend shows the logical architecture of the frontend, organised in layers
from the routes down to the network.

![Logical frontend architecture](../diagrams/fig-3-1-architecture-frontend/fig-3-1-architecture-frontend.png){#fig:arch-frontend}

The **routes** (28 pages) compose **feature modules** (18) over a **state and data**
layer — query cache, stores, token-refresh interceptors, analytics tracker — and a
**request proxy** guards private routes. Only live notifications and direct uploads
bypass the API, so token refresh and error handling are written once.

### Backend

@fig:arch-backend shows the backend, which runs as two processes from the same image.

![Logical backend architecture](../diagrams/fig-3-2-architecture-backend/fig-3-2-architecture-backend.png){#fig:arch-backend}

The **API** passes every request through a rate limiter, then the guards composed by
`@Auth()`, into feature modules by domain. The **worker** runs from the same image and
consumes six queues — embeddings, analytics, marketplace, AI tokens, documents and
model checks. Everything slow or scheduled lives in the worker, so no API response
waits for background work (NFR-27).

## Physical architecture

@fig:arch-physical shows the deployment of the eight services on one host.

![Physical architecture](../diagrams/fig-3-3-architecture-physical/fig-3-3-architecture-physical.png){#fig:arch-physical}

**nginx is the only service published** (ports 80 and 443): it terminates TLS and
routes to Next.js, the API and the public image bucket. Private documents go through
the API, which checks ownership, and the datastores stay inside the Compose network:
one attack surface and one place to configure TLS and timeouts.

## Continuous integration and delivery

@fig:arch-cicd shows the pipeline from a push to a running service.

![CI/CD pipeline](../diagrams/fig-3-4-architecture-cicd/fig-3-4-architecture-cicd.png){#fig:arch-cicd}

A push to `main` runs the quality gates, then builds an image tagged `latest` and with
the commit hash; the deployment workflow pulls it, migrates, restarts the services
and checks their health. No image skips the gates, and every deployed version can be
traced to its commit.

## Conclusion {.unnumbered}

This chapter presented the working environment, compared the technological choices
with their alternatives, justified the main parameters of the system, and described
its logical and physical architecture and its delivery pipeline. The following
chapters present the four releases, starting with the functional foundation.
