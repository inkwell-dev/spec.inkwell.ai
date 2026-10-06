# Chapter 3 — Working environment and architecture

## Introduction

Before the release chapters, this chapter describes the environment the platform was
built in: the hardware and software used, the technological choices and their
justification, the work that preceded the feature sprints, and the architecture of the
system — its logical decomposition on the frontend and the backend, its physical
deployment and its delivery pipeline.

## 3.1 Working environment

### 3.1.1 Hardware environment

The project was developed on a single workstation, described in Table 3.1.

**Table 3.1 – Hardware environment**

| Component | Specification |
|---|---|
| Machine | Lenovo ThinkPad |
| Processor | Intel Core i7-1355U |
| Memory | 24 GB RAM |
| Graphics | NVIDIA GeForce MX550 |
| Storage | 512 GB NVMe SSD |
| Operating system | Ubuntu Linux |

### 3.1.2 Software environment

**Table 3.2 – Software tools**

| Tool | Use |
|---|---|
| JetBrains IDE | code editor |
| Git and GitHub | version control, pull requests, continuous integration (GitHub Actions) and container registry (GHCR) |
| Docker and Docker Compose | containers for every service, in development and in production |
| Figma | design system and screen design |
| PlantUML and draw.io | UML and architecture diagrams, kept as versioned sources |
| Swagger UI | exploring the REST API through the OpenAPI documentation the backend generates |
| Playwright | end-to-end tests and the capture of this report's screenshots |

### 3.1.3 Foundation and design track

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

### 3.1.4 Repository organisation

The source code lives in four Git repositories. `docker.inkwell.ai` is the
superproject: it holds the Compose files, the nginx configuration, the deployment
workflow and the developer Makefile, and it carries the three others as **Git
submodules** — `backend.inkwell.ai`, `frontend.inkwell.ai`, and `spec.inkwell.ai`, which
holds the specifications, the diagrams and this report's figures. A commit of the
superproject therefore identifies one exact, deployable revision of the whole system.

## 3.2 Technological choices

### 3.2.1 Frontend

**Table 3.3 – Frontend technologies**

| Technology | Role | Why it was chosen |
|---|---|---|
| **Next.js 16** (App Router) with **React 19** | web framework | server rendering for public articles and search engines, file-system routing, a request proxy for route protection |
| **TypeScript** (strict) | language | one typed language across frontend and backend |
| **Tailwind CSS 4** and accessible headless primitives | styling and components | implements the Figma design tokens directly; accessible dialogs, menus and tabs |
| **TipTap 3** | rich-text editor | ProseMirror-based, stores the document as JSON, extensible with the AI write range and inline actions |
| **TanStack Query 5** and **Zustand 5** | server state and client state | caching, optimistic updates and invalidation for API data; small stores for UI state |
| **Vercel AI SDK** (React bindings) | assistant client | consumes the typed UI-message stream of the assistant turn |
| **Axios** | HTTP client | interceptors implement the silent token refresh |

### 3.2.2 Backend

**Table 3.4 – Backend technologies**

| Technology | Role | Why it was chosen |
|---|---|---|
| **NestJS 11** | API and worker framework | modular structure, dependency injection, guards and interceptors, OpenAPI generation |
| **Drizzle ORM** | data access and migrations | type-safe SQL close to PostgreSQL, explicit migrations, no hidden queries |
| **PostgreSQL 16 + pgvector** | single data store | relational data, full-text search (`tsvector`) and vector search (HNSW) in one database and one transaction |
| **Redis 7 + BullMQ** | queues and scheduled jobs | retries with back-off, repeatable jobs, a separate worker process |
| **MinIO** | object storage (S3 API) | images and private documents, uploaded by the browser through presigned URLs |
| **Vercel AI SDK** | AI orchestration | one interface over several providers, streaming, tool calls and typed UI streams |
| **Passport (JWT, Google OAuth 2.0)** and **bcrypt** | authentication | standard strategies; password hashing with cost factor 12 |

### 3.2.3 Artificial-intelligence services

**Table 3.5 – AI models and their use**

| Use | Provider and model |
|---|---|
| Chat, writing, inline actions, portfolio insights, writer memory | Groq — `gpt-oss-120b`, falling back to `gpt-oss-20b`, then Google `gemini-3.5-flash` |
| Embeddings (articles, documents, queries) | Google `gemini-embedding-001`, 1,536 dimensions |
| Speech-to-text (voice prompt) | Groq — `whisper-large-v3-turbo` |
| Text-to-speech (replies read aloud) | Google `gemini-2.5-flash-preview-tts` |
| Content moderation at publish time | Groq classifier model |

The chain of chat models is what makes a provider outage degrade the assistant only:
the first chunk of a response is pulled before anything is sent to the browser, so a
refusal from one model can still be answered by the next.

### 3.2.4 Infrastructure and quality

**Docker Compose** runs eight services — nginx, web, api, worker, a one-shot migration
service, PostgreSQL, Redis and MinIO. **nginx** terminates TLS and routes traffic.
**GitHub Actions** runs the quality gates and builds the images; **GHCR** stores them.
**Jest** tests the backend against a real PostgreSQL database, **Playwright** drives a
real browser end to end, and **Sentry** captures errors in the four runtimes.

## 3.3 Logical architecture

### 3.3.1 Frontend

Figure 3.1 shows the logical architecture of the frontend. The **routes** (28 pages)
compose **feature modules** (18, among them the editor, the assistant, documents,
saves, reposts, the marketplace and the evaluation report). A **state and data** layer
holds the query cache, the client stores, the HTTP interceptors that refresh an expired
access token and retry the request, and the analytics tracker. A **request proxy**
protects private routes before a page renders. Two channels bypass the REST API: an
**SSE client** for live notifications, and **direct uploads** from the browser to
object storage through presigned URLs.

![Figure 3.1 – Logical frontend architecture](../diagrams/fig-3-1-architecture-frontend/fig-3-1-architecture-frontend.png){width=100%}

### 3.3.2 Backend

Figure 3.2 shows the backend. The **API** is a modular NestJS application: a global
rate-limiting guard runs on every route, then the guards composed once by the `@Auth()`
decorator — authentication, role, plan, account type, subscription and AI quota. The
feature modules cover authentication and users, articles, social interactions, AI,
analytics, the marketplace, search and discovery, moderation and uploads, and
documents. The **worker** runs from the same image with a second entry point and
consumes six queues: `embeddings` (chunking and embedding articles, extracting writer
memory), `analytics` (article and writer rollups), `marketplace` (eligibility and
subscription renewal), `ai-tokens` (the nightly allowance reset), `documents`
(extracting, chunking and embedding uploaded documents) and `ai-models` (a daily check
that every model still answers).

![Figure 3.2 – Logical backend architecture](../diagrams/fig-3-2-architecture-backend/fig-3-2-architecture-backend.png){width=100%}

## 3.4 Physical architecture

Figure 3.3 shows the deployment. All eight services run under Docker Compose on one
host. **nginx is the only service published**, on ports 80 and 443: it terminates TLS,
proxies `/` to the Next.js server and `/api` to the NestJS API, keeps server-sent
events unbuffered, and proxies the public image bucket at `/storage`. Private
documents are never served through that path; they are read through the API, which
checks ownership. The datastores are reachable only from inside the Compose network.

![Figure 3.3 – Physical architecture](../diagrams/fig-3-3-architecture-physical/fig-3-3-architecture-physical.png){width=100%}

## 3.5 Continuous integration and delivery

Figure 3.4 shows the pipeline. A push to `main` on either application repository runs
the quality gates — install, lint with zero warnings, type-check, the 792 backend
tests, a schema-drift check — then builds a multi-stage image and pushes it to GHCR,
tagged both `latest` and with the commit hash. A repository dispatch then triggers the
deployment workflow of the superproject, which pulls the images on the server, runs
the migrations (which must succeed before the API and worker start), restarts the
services, verifies the health and readiness endpoints and reloads nginx.

![Figure 3.4 – CI/CD pipeline](../diagrams/fig-3-4-architecture-cicd/fig-3-4-architecture-cicd.png){width=100%}

## Conclusion

This chapter presented the working environment, justified the technological choices
and described the logical and physical architecture of Inkwell.ai and its delivery
pipeline. The following chapters present the four releases, starting with the
functional foundation.

\newpage
