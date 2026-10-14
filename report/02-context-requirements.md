# Preliminary study and system design {#sec:ch1}

## Introduction {.unnumbered}

This chapter sets out what the project is, what it must do and how it is built. Its
first part places the project in its context: the host organisation, the observations
that motivated it, the existing solutions, the problem and the proposed solution, and
the development method adopted and how it was adapted. Its second part specifies the
requirements: the actors, the functional and non-functional requirements, the global
use case and class diagrams, and the organisation of the work as a product backlog
and a release plan. Its third part describes the environment the platform was built
in, the technological choices compared with their alternatives, the main parameters
of the system, and its logical and physical architecture and delivery pipeline.

## Project context {#sec:context}

### Host organisation

This project was carried out at **Intuitiv Group**, a company with a dual culture: at
once an IT services company (*Entreprise de Services du Numérique*, ESN) and an
interactive agency. It works with large national and international groups while
keeping a human-scale structure, and positions itself on reactivity, reliability and
quality of service. That dual culture suits Inkwell.ai, which is as much a software
engineering effort (architecture, data, security, delivery) as a product and
interface design effort.

### Context and motivation {#sec:motivation}

The project was proposed as an end-of-studies engineering project with a
product-shaped scope: not a prototype of one feature, but a complete two-sided
platform with real accounts, real data flows, an AI layer and money-like
transactions. Three observations motivated it.

- **Writing assistants are generic.** Mainstream assistants draft, shorten and change
  the tone of a text from a description of what is wanted [@grammarly2026;
  @notionai2026; @beehiiv2026]; none of those cited learns from what the writer has
  already published, so they write *for* the writer rather than *like* the writer.
- **Engagement data is collected, but not offered as evidence.** Platforms measure
  reading in detail: Medium pays its writers according to members' reading time,
  read ratio and engagement [@medium2026partner]. Yet these signals are shown to the
  writer or used to rank content, never presented to a buyer judging the writer.
- **Paid writing is a narrow market.** About four percent of creators earn more than
  a hundred thousand dollars a year, and most creator income comes from brand deals
  [@goldman2023creator]. None of the publishing platforms studied below offers a
  publication a way to license an article that already exists.

### Study of existing solutions {#sec:existing}

The solutions close to the project fall into five families. **Publishing platforms**
such as Medium pay writers from a pool of reader subscriptions
[@medium2026partner]. **Newsletter platforms** (Substack, Ghost and beehiiv) let a
writer charge readers directly [@substack2026; @ghost2026], and beehiiv adds an AI
writing assistant to its editor [@beehiiv2026]. **Freelance marketplaces** such as
Contently and Upwork connect clients with writers for *commissioned* work: the article
does not yet exist when it is bought, and the platform holds no engagement data on
the writer's published pieces [@contently2026; @upwork2026]. **AI writing
assistants** such as Grammarly and Notion AI improve or generate text inside a
document [@grammarly2026; @notionai2026]. Finally, **source-grounded assistants**
(NotebookLM, ChatGPT with uploaded files, Perplexity Spaces) answer from documents the
user uploads and cite the passages they used [@notebooklm2024; @chatgptfiles2026;
@perplexity2026].

@tbl:existing compares these families on the criteria the project targets. Each cell
records what the product's own documentation states; "partial" means the capability
exists in a restricted form, explained below the table.

| Criterion | Medium | Newsletter platforms¹ | Freelance markets² | Writing assistants³ | Grounded assistants⁴ | **Inkwell.ai** |
|:------------------------------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| Publishing and public reading | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ |
| AI assistance in the editor | ✗ | partial | ✗ | ✓ | ✗ | ✓ |
| Assistant grounded in the writer's published work | ✗ | ✗ | ✗ | ✗ | partial | ✓ |
| Answers citing uploaded documents | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Engagement analytics for the writer | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ |
| Analytics exposed to a buyer as evidence | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Licensing of existing articles to publications | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Traceable payments | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |

: Comparison of existing solutions, from each product's public documentation {#tbl:existing}

¹ Substack, Ghost, beehiiv. ² Contently, Upwork. ³ Grammarly, Notion AI. ⁴ NotebookLM, ChatGPT with files, Perplexity Spaces.

Two cells need a word. beehiiv is the only newsletter platform of the three with an
assistant in its editor, hence "partial" for that family. The source-grounded
assistants could be grounded in a writer's published work only if the writer
uploaded it by hand, and they are separate from any editor or publishing workflow.

The decisive cells are the last three rows. Citing uploaded documents, taken alone, is
**not** distinctive: the source-grounded assistants already do it, and Inkwell.ai
borrows the idea. What no family offers is the *combination*: an assistant grounded
in the writer's own published corpus inside the editor where the writing happens,
analytics presented to a buyer as evidence, and a market in which a publication
licenses an existing article. Each family covers one or two of these needs; the
platforms that pay writers do not give buyers evidence, and the tools that ground
answers in sources do not publish or pay.

### Problem statement and proposed solution

The study shows a problem on three levels. On the **supply side**, writers lack an
assistant that writes in their own voice from what they have published and the
material they are working from, and a direct path to be paid for quality. On the
**demand side**, magazines lack objective, comparable signals about a writer's
audience, consistency and quality. Between them, the **market** is missing: there is
no self-service place where a publication can discover, evaluate, preview and license
an existing article, with the money recorded in a way both parties can trust.

Inkwell.ai answers the three levels with one platform: an **editor with an AI
assistant** that retrieves passages from the writer's own articles and attached
documents, decides per request whether to answer or to write into the draft, and
cites its sources by page; an **analytics pipeline** that turns reading events into
per-article and per-writer metrics, presented to the writer and, as an evaluation
report with AI portfolio insights, to magazines; and a **marketplace** where
subscribed magazines preview an article for 10% of its price, buy the remaining 90%
for exclusive rights and publish it under their own masthead, every credit movement
being written to a ledger inside one database transaction.

## Development methodology {#sec:method}

### Sequential and agile approaches

A **sequential (waterfall) process** runs each phase once, in order, and its classic
description warned that late testing exposes design errors when they cost most
[@royce1970]. An **agile process** delivers working software in short, reviewed
iterations [@agilemanifesto2001; @sommerville2016]. @fig:waterfall-agile contrasts
the two.

![Classic and agile approaches compared](../diagrams/fig-1-2-waterfall-vs-agile/fig-1-2-waterfall-vs-agile.png){#fig:waterfall-agile height=45%}

Working software appears only in the last phase of the sequential process, but at
the end of every agile iteration. Inkwell.ai is built in layers (accounts, articles,
analytics, marketplace), each depending on the one below, so each must work before
the next is built on it.

### Scrum, and its adaptation to a one-person project {#sec:scrum}

Among agile frameworks, **Scrum** was chosen for its fixed-length sprints and its
explicit artefacts and events [@scrumguide2020], which give an individual project the
regular checkpoints a supervisor can follow. @fig:scrum shows the framework as it was
applied.

![The Scrum framework, as practised in this project](../diagrams/fig-1-1-scrum-framework/fig-1-1-scrum-framework.png){#fig:scrum height=45%}

The backlog feeds sprint planning; each two-week sprint ends with an increment checked
against the definition of done, a review and a retrospective whose actions return to
the next planning. For this project the unit of progress is therefore the increment:
every sprint leaves the platform runnable and tested.

Scrum is designed for a team of ten or fewer people holding three accountabilities
(Product Owner, Scrum Master and Developers) [@scrumguide2020], and this project has one
person. The adaptation, and its limits, were the following.

- **Roles.** The author held the Developer and Scrum Master accountabilities. The
  academic supervisor acted as Product Owner at sprint boundaries, accepting or
  returning each increment against the backlog. The limit is that one person both
  estimates and executes the work: there is no team discussion to correct an
  optimistic estimate, which shows in the uneven sprint loads discussed in
  @sec:velocity.
- **Events.** Sprint planning, the sprint review and the retrospective were kept; the
  daily scrum, which synchronises a team, has no purpose for one person and was
  replaced by a written log of what was done and what blocked. Its limit is the loss
  of a daily outside view.
- **Artefacts.** The product backlog, the sprint backlogs and the increment were kept
  unchanged, with a written **definition of done**, given with the evaluation in
  @sec:velocity: code reviewed against the specification, the type check and linter
  passing with no warning, the backend tests passing in the container, and the
  feature demonstrated in a browser.

With one person, the value of Scrum lies in the discipline it imposes (a fixed
cadence, a written goal per sprint, an increment that must work) rather than in
coordination.

### Prioritisation and estimation {#sec:estimation}

Requirements and user stories are prioritised with **MoSCoW** (Must, Should, Could,
Won't), the prioritisation technique of the DSDM agile framework, in which the Must
items form the minimum usable subset that the delivery guarantees [@dsdm2014]. Stories
are estimated in **story points** on a Fibonacci-like scale (1, 2, 3, 5, 8, 13),
relative to the simplest story: the gaps between values grow with size because
estimating larger work is less precise, which is the reason for the scale
[@cohn2005]. Points measure relative size, not hours; their sum per sprint gives the
velocity reported in @sec:velocity.

### Modelling language

Analysis and design use **UML 2.5** [@omg2017uml]: use case diagrams for the
functional scope of each sprint, class diagrams for the data model, sequence diagrams
for the main interactions, and activity and state diagrams where a decision or a
lifecycle is the subject. The diagrams are kept as text sources (PlantUML) or
as draw.io files, generated by a script or, for the global use case diagram, laid
out by hand, in the project repository, versioned beside the code they describe.

## Identification of the actors {#sec:actors}

The platform has five actors. @tbl:actors lists them with the way each is represented
in the data model, because the actors are not invented for the analysis: they follow
from two properties every account carries: its **account type** (personal or
magazine) and its **role** (reader, writer or administrator).

| # | Actor | Data-model representation | Definition |
|:--|:----------------|:-----------------------|:--------------------------------------------|
| A1 | Visitor | no account | Unauthenticated. Browses the public feed and reads free articles; cannot interact. |
| A2 | Reader | personal account | Reads and interacts: likes, comments, reposts, saves, follows, blocks, reports. On the premium plan, also reads premium articles and uses the AI assistant. |
| A3 | Writer | personal account, role writer | Everything a reader does, plus drafting, publishing and analysing their own articles. Once eligible, also publishes premium articles and lists on the marketplace. |
| A4 | Magazine | magazine account | Subscribes, then browses writers, reads evaluation reports, previews, buys and publishes licensed articles. |
| A5 | Administrator | personal account, role admin | Works the moderation queue, manages users and grants eligibility manually. |

: Actors of the system {#tbl:actors}

Three further properties change what an actor may do without making it a different
actor: a reader's **plan** (free or premium), a writer's **marketplace eligibility**,
and a magazine's **subscription** (active or not). They are states of an account:
the same person moves between them by upgrading, by being read, or by subscribing. So
they are drawn in the use case diagrams as **conditions** on the use cases they unlock,
not as separate actors: the assistant requires `[plan = premium]`, listing on the
marketplace requires `[writer is eligible]`, and every marketplace use case
requires `[subscription active]` (@fig:uc-s2, @fig:uc-s5).

Two generalisations hold: the reader specialises the visitor, and the writer
specialises the reader. The other two actors specialise nobody. A **magazine** is a
different account type with no role and no plan (a database constraint enforces it),
so it inherits nothing from the readers or writers; a person who runs a magazine and
also writes uses two accounts. The **administrator** holds a role that cannot be
obtained through the interface and is granted in the database; its capabilities are
moderation and management, not an extension of reading or writing, so it is not drawn
as a specialised reader either.

## Functional requirements {#sec:fr}

The functional requirements are stated per actor, each with a stable identifier, a
MoSCoW priority and the sprint that delivers it. Identifiers are stable rather than
sequential: a requirement added later keeps the next free number and is listed beside
the feature it belongs to. @tbl:fr-summary summarises them; the full statements are
given in Annex A.

<!-- INCLUDE:fr-summary -->

The platform counts {{FRS}} functional requirements, of which {{FR_MUST}} are Must:
four in five requirements belong to the minimum the delivery guarantees, which is
expected for a platform whose three pillars depend on one another: dropping a Must
from one pillar would break another. The Should and Could requirements are the
comforts that make each feature pleasant rather than possible: search and browsing
by tag, live comment previews, voice, sharing. The writers carry the most
requirements (31), because the editor, the assistant, the analytics and the earnings
all belong to them; the administrator carries the fewest (5), all delivered in one
sprint. A requirement listed under two sprints is delivered in two steps, the
second sprint completing the rule the first one prepared; Chapters 2 to 5 say which
part each sprint delivers.

## Non-functional requirements {#sec:nfr}

Each non-functional requirement is stated as a property together with the mechanism
that provides it and the way it is verified: by an automated **test** of the backend
suite, by a **measurement** reported in Chapter 6, by **inspection** of the code or the
configuration, or not at all when it is not met. @tbl:nfr groups them by quality
attribute. Identifiers are stable, as for the functional requirements.

| ID | Requirement | Mechanism | Verified by |
|:-------|:--------------------------------|:--------------------------------|:-----------|
| | **Security** | | |
| NFR-01 | Passwords stored as bcrypt hashes, cost factor 12 | authentication module, following [@owasppasswords] | inspection |
| NFR-02 | Access tokens expire after 15 minutes, refresh tokens after 7 days | signed JWTs [@rfc7519] | inspection |
| NFR-03 | Every protected route passes one composed guard stack | one `@Auth()` decorator composing six guards | inspection |
| NFR-04 | Authorisation is decided server-side; the client is told the verdict | the article access decision; locked content arrives as `null` | test |
| NFR-05 | Per-address rate limits, tighter on credential routes | 60 requests/min, 10/min on sign-in, 5/min on registration | measurement |
| NFR-06 | Financial operations are idempotent under retry | a unique idempotency key on every ledger transaction | test |
| NFR-07 | Uploads are presigned, time-limited and never routed through the API | 10-minute presigned upload URL | inspection |
| NFR-08 | Datastore ports bind to the loopback interface only | Compose port bindings on `127.0.0.1` | inspection |
| NFR-09 | A ban takes effect within 15 minutes at most | refused at sign-in, Google sign-in and refresh; an access token lasts 15 minutes | test |
| NFR-10 | No stored HTML is ever rendered as markup | no raw-HTML rendering in the frontend | inspection |
| | **Performance** | | |
| NFR-11 | Semantic retrieval stays sub-linear as the corpus grows | HNSW index (m = 16, ef_construction = 64) [@malkov2018hnsw] | measurement |
| NFR-12 | Full-text search is index-backed with weighted ranking | weighted `tsvector` column and GIN index [@postgres16fts] | measurement |
| NFR-13 | Prompt context is bounded | at most 5 passages, a memory block under 200 tokens | inspection |
| NFR-14 | Feed pagination is cursor-based, stable under insertion | none | **not met**: pagination is by offset |
| NFR-15 | Dashboard totals and rates read pre-aggregated rows | four rollup tables refreshed by the worker | measurement |
| NFR-16 | Analytics aggregation is incremental and idempotent | each run reads only the events since the last one | inspection |
| NFR-17 | Expensive AI output is cached and invalidated by what changes it | insights cached 24 h, dropped when the writer publishes | inspection |
| NFR-18 | Streaming responses are never buffered end to end | nginx `proxy_buffering off`, 300 s read timeout | inspection |
| | **Reliability** | | |
| NFR-19 | Every denormalised balance equals the sum of its ledger rows | three invariants asserted after every money-moving test | test |
| NFR-20 | Concurrent purchases cannot double-spend | `SELECT … FOR UPDATE` on the balance-owning row | test |
| NFR-21 | Schema changes are versioned and applied before the application starts | a one-shot migration service | inspection |
| NFR-22 | The vector extension exists before any migration that needs it | the migration runner creates it first | inspection |
| NFR-23 | Failed background jobs retry with exponential back-off | none | **not met**: jobs run once |
| NFR-24 | An AI provider outage degrades AI only | a model chain falling back from Groq to Gemini | test |
| NFR-25 | Every service reports liveness and readiness | `GET /health` and `GET /ready` | partly met: readiness checks PostgreSQL only |
| | **Scalability** | | |
| NFR-26 | The API holds no session state | identity carried by JWT claims | inspection |
| NFR-27 | Long-running work never runs in the request path | six BullMQ queues consumed by a separate worker | inspection |
| NFR-28 | API and worker scale horizontally behind the proxy | stateless containers, one Compose service each | not measured |
| | **Maintainability** | | |
| NFR-29 | Both code bases compile in strict mode with zero lint warnings | `tsc --noEmit`, `eslint --max-warnings=0` | continuous integration |
| NFR-30 | The API contract is generated from OpenAPI | client types generated from the backend's OpenAPI document | inspection |
| NFR-31 | Business rules are tested, not asserted | 796 backend tests | test |
| NFR-32 | The build fails when schema and migrations disagree | a schema-drift check | continuous integration |
| NFR-33 | Errors are captured in every runtime without personal data | Sentry in API, worker, Next.js server and browser | inspection |
| | **Usability** | | |
| NFR-34 | Two breakpoints are designed and implemented | 375 px and 1280–1440 px | measurement (accessibility at both) |
| NFR-35 | One design system, applied consistently | 39 design tokens and 87 components in Figma | inspection |
| NFR-36 | A complete dark mode | theme switch across every screen | inspection |
| NFR-37 | Lighthouse score above 90 and no critical accessibility violation on article pages | production build audited | measurement: partly met |

: Non-functional requirements and how each is verified {#tbl:nfr}

Of the 37 requirements, seven are verified by an automated test and six by a
measurement in Chapter 6; two are enforced by the continuous-integration pipeline.
The others rest on inspection: they are properties of configuration (port bindings,
nginx buffering, Compose dependencies) rather than of behaviour, and a test would only
restate the configuration. Five are not fully met and are stated as such: NFR-14
(offset pagination), NFR-23 (no queue is configured with retries, so a failed job is
not attempted again), NFR-25 (readiness ignores Redis), NFR-28 (horizontal scaling is
designed for but was never exercised) and NFR-37 (met on desktop and for critical
violations, not on mobile; see @sec:eval-perf). They return as limitations in the
general conclusion.

## Global use case diagram {#sec:uc-global}

@fig:uc-global gives the use cases of the five actors. At this size it is printed on
a fold-out page.

![Global use case diagram](../diagrams/fig-1-11-use-case-global/fig-1-11-use-case-global.png){#fig:uc-global .foldout height=88%}

Each actor's use cases hang below it, each base use case with its extensions
beside it, and the reader and the writer inherit the use cases of the actors to
their left. Every use case of a signed-in actor includes *Sign in*, and the figure
draws each of those «include» links rather than stating the rule once: signing in
is the boundary between the visitor and every other actor, and drawing it shows
how much of the platform lies behind it. The conditions that unlock a use case
(the premium plan, marketplace eligibility, an active subscription) are left to
the per-sprint diagrams of Chapters 2 to 5, which refine each sprint's share.

## Global class diagram {#sec:classes-global}

@fig:classes-global gives the data model: thirty persisted tables with domain types,
the main operations of each class, and the enumerations along the bottom; audit
columns are omitted. It is also printed on a fold-out page.

![Global class diagram](../diagrams/fig-1-12-classes-global/fig-1-12-classes-global.png){#fig:classes-global .foldout height=88%}

One `User` class serves every account, told apart by type, role and plan, and
`Article` is the other hub. Social interactions that carry data of their own (likes,
saves, reposts, comment likes, follows, blocks) are association classes on
many-to-many associations, stored as join tables with a unique pair; a
`Purchase` records two or three `Transaction` rows from which every balance can be
recomputed (NFR-19); and dashboards read the metric rollups, never raw events
(NFR-15). Each operation is implemented by the service of its domain.

## Product backlog {#sec:backlog}

The product backlog expresses the requirements as user stories of the form *"As an
⟨actor⟩, I want ⟨goal⟩ so that ⟨benefit⟩"*, grouped into nine epics, prioritised with
MoSCoW and estimated in story points relative to the simplest story (US-01). The
backlog counts **{{STORIES}} stories for {{POINTS}} points**. @tbl:backlog-summary
summarises it by epic; the full backlog is given in Annex B.

<!-- INCLUDE:backlog-summary -->

The distribution of points shows where the effort lies. The AI assistance epic is the
heaviest (21% of the points) although it is not the largest in stories: its stories
(retrieval grounded in the writer's corpus, writing into the document, voice, the
document library) are few but each is large, because each joins a model call to the
editor and to the data model. The marketplace comes next (18%), for the same reason
applied to money: a small number of stories, each guarded by transactions, locks and
ledger checks. The social epic has the most stories but small ones, and the technical
epic E9 (12%) is the price of a platform that runs, migrates and is tested with one
command. In short, the effort follows the product's ambition: two of its three
pillars, AI and the marketplace, take almost two fifths of the points.

## Release plan and schedule {#sec:release-plan}

The stories are delivered in four releases of two or three sprints each, every sprint
lasting two weeks. @tbl:release-plan gives the plan with the points committed per
sprint. The foundation week and the three-sprint design track are not sprints,
because they deliver no user-facing increment; they are presented with the working
environment in @sec:environment.

| Release | Sprint | Dates | Goal | Points |
|:----------------------------|:---|:----------|:--------------------------------------|:-:|
| **R1: Functional foundation** | Sprint 1 | 09/02 – 20/02 | Schema, authentication, article core, ledger invariant harness | {{S1PTS}} |
| | Sprint 2 | 06/04 – 17/04 | Editor, AI chat and inline actions, analytics event capture | {{S2PTS}} |
| **R2: Social, analytics and AI** | Sprint 3 | 20/04 – 01/05 | Social interactions, notifications, aggregation, dashboards | {{S3PTS}} |
| | Sprint 4 | 04/05 – 15/05 | Retrieval-augmented generation, portfolio insights, hybrid search, writer memory | {{S4PTS}} |
| **R3: Marketplace, testing and deployment** | Sprint 5 | 18/05 – 29/05 | Marketplace, subscriptions, premium, moderation, administration | {{S5PTS}} |
| | Sprint 6 | 01/06 – 12/06 | Tests, demonstration corpus, deployment, CI/CD | {{S6PTS}} |
| **R4: Social depth, assistant and documents** | Sprint 7 | 15/06 – 26/06 | Comment likes, follower lists, block, save, share | {{S7PTS}} |
| | Sprint 8 | 29/06 – 10/07 | Live card controls, reposts, byline preview, assistant writing into the document, voice | {{S8PTS}} |
| | Sprint 9 | 13/07 – 24/07 | Document library, ingestion, attachment, citations | {{S9PTS}} |

: Release plan {#tbl:release-plan}

The order of the releases follows the layering argued in @sec:method: each release
needs the data the previous one produces. The loads are uneven. Sprint 5 commits 85
points against an average near 40, because the marketplace stories (subscription,
credits, preview, purchase, publication, earnings) share one transaction model and
were planned together rather than split across two sprints. Sprints 6, 7 and 9 are
light, for two different reasons: Sprint 6's real work, the test suite that proves
the business rules, is not expressed as user stories, and Release 4 runs alongside
the writing of this report. How this plan compares with what was delivered is
measured in @sec:velocity.

@fig:gantt places the work on the project window, from 2 February to 31 July 2026: the
foundation week and Sprint 1, the design track, Sprints 2 to 9 in four releases, and
the writing of this report alongside the last sprints.

![Gantt chart of the project](../diagrams/fig-2-4-gantt/fig-2-4-gantt.png){#fig:gantt}

The chart shows one break in the rhythm: the six-week design track between Sprints 1
and 2. It was deliberate, since later features were built from finished screens rather
than designed while coded, and it is why the first release spans two months.

## Working environment {#sec:environment}

### Hardware environment

The project was developed and every measurement of Chapter 6 was taken on a single
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

The tools used outside the application code itself are presented below. They share a
principle: every artefact (code, diagrams, this report) is kept as text under
version control, and everything that runs, runs in a container.

::: {.tech logo="Logos/jetbrains_logo.png"}
**JetBrains IDE**

Code editor.
:::

::: {.tech logo="Logos/git_logo.png"}
**Git and GitHub**

Version control, pull requests, continuous integration (GitHub Actions) and container registry (GHCR).
:::

::: {.tech logo="Logos/docker_logo.png"}
**Docker and Docker Compose**

Containers for every service, in development and in production [@composedocs].
:::

::: {.tech logo="Logos/figma_logo.png"}
**Figma**

Design system and screen design.
:::

::: {.tech logo="Logos/plantuml_logo.png"}
**PlantUML and draw.io**

UML and architecture diagrams, kept as versioned sources.
:::

::: {.tech logo="Logos/swagger_logo.png"}
**Swagger UI**

Exploring the REST API through the OpenAPI document the backend generates.
:::

::: {.tech logo="Logos/playwright_logo.png"}
**Playwright**

End-to-end tests and the capture of this report's screenshots [@playwrightdocs].
:::

### Foundation and design track

Two blocks of work preceded the feature sprints and are presented here rather than as
sprints, because neither delivers a user-facing increment.

- **Foundation (one week).** The three repositories, their Docker images, the Compose
  stack, the reverse proxy and the continuous-integration pipeline were set up first,
  so that every later sprint started from a stack that builds, tests and runs with one
  command.
- **Design track (three sprints).** The user interface was designed in Figma before the
  editor and the social features were built: a design system of **39 tokens and 87
  components**, then the full screen set at two widths (**375 px for mobile and
  1280–1440 px for desktop**, 58 screens), then an audit of the screens against the
  specification. The release chapters implement these designs.

### Repository organisation

The source code lives in four Git repositories. `docker.inkwell.ai` is the
superproject: it holds the Compose files, the nginx configuration, the deployment
workflow and the developer Makefile, and it carries the three others as **Git
submodules**: `backend.inkwell.ai`, `frontend.inkwell.ai`, and `spec.inkwell.ai`, which
holds the specifications, the diagrams and this report. A commit of the superproject
therefore identifies one exact, deployable revision of the whole system.

## Technological choices {#sec:tech}

Each choice below is compared with the alternatives that were considered and the
criteria that decided between them, with a source for every claim that is not a
property of the project itself.

### Frontend

The frontend stack is presented below. Its central decision is the web framework:
the platform's public pages (the feed, articles, profiles) must be rendered on the
server so that search engines and link previews see their content, while the editor
and the assistant are interactive applications.

::: {.tech logo="Logos/nextjs_logo.png"}
**Next.js 16** (App Router) with **React 19**

*Alternatives considered:* Remix, Nuxt (Vue), a client-only React application.

Server rendering per route for public pages and a request proxy for protected routes, in the most used React framework [@nextjsdocs; @stateofjs2024]; a client-only application would serve empty HTML to search engines.
:::

::: {.tech logo="Logos/typescript_logo.png"}
**TypeScript** (strict)

*Alternatives considered:* JavaScript.

One typed language from the database schema to the browser; the API client types are generated from the backend (NFR-30).
:::

::: {.tech logo="Logos/tailwindcss_logo.png"}
**Tailwind CSS 4** with accessible headless primitives

*Alternatives considered:* CSS modules, a component library such as MUI.

The Figma tokens map directly to utility classes; headless primitives give accessible dialogs and menus without imposing a visual style.
:::

::: {.tech logo="Logos/tiptap_logo.png"}
**TipTap 3**

*Alternatives considered:* Lexical, Slate, Quill.

Built on ProseMirror, stores the document as JSON, and accepts custom extensions, which the protected range the assistant writes into needs [@tiptapdocs].
:::

::: {.tech logo="Logos/tanstack_logo.png"}
**TanStack Query 5** and **Zustand 5**

*Alternatives considered:* Redux Toolkit.

Server state (caching, invalidation, optimistic updates) and client state handled separately, with far less code than a single global store.
:::

::: {.tech logo="Logos/vercel_logo.png"}
**Vercel AI SDK** (React bindings)

*Alternatives considered:* hand-written stream parsing.

Consumes the assistant's typed stream of text, status and write parts [@aisdkdocs].
:::

### Backend

The backend stack is presented below. Its two structuring decisions are the
framework, which must host both an HTTP API and a background worker, and the data
store, which must hold relational data, full-text search and vector search.

::: {.tech logo="Logos/nestjs_logo.png"}
**NestJS 11**

*Alternatives considered:* Express or Fastify alone.

Modules, dependency injection, guards and OpenAPI generation built in [@nestjsdocs]; the same modules serve the API and the worker. Fastify is faster in raw benchmarks [@techempower2025], but the API's latency is dominated by the database and the model calls (@sec:eval-perf), not by the HTTP layer.
:::

::: {.tech logo="Logos/postegreSQL_logo.png"}
**PostgreSQL 16 + pgvector**

*Alternatives considered:* PostgreSQL with a separate vector database (Qdrant, Pinecone).

Relational data, full-text search and vector search in one database [@pgvector2026; @postgres16fts]: an article and its embeddings change in one transaction and are never out of sync, and there is one service less to run. HNSW, the index pgvector offers, is among the best recall-per-latency trade-offs in public benchmarks [@aumuller2020annbench].
:::

::: {.tech logo="Logos/drizzleorm_logo.png"}
**Drizzle ORM**

*Alternatives considered:* Prisma, TypeORM.

SQL-shaped, type-safe queries with explicit migrations [@drizzledocs]; the purchase transaction needs `SELECT … FOR UPDATE` and the search needs `ts_rank` and vector operators, which Drizzle writes directly.
:::

::: {.tech logo="Logos/redis_logo.png"}
**Redis 7 + BullMQ**

*Alternatives considered:* RabbitMQ, PostgreSQL-based queues.

Repeatable jobs, priorities and a separate worker process on one Redis instance [@bullmqdocs]; Redis also carries the notification fan-out.
:::

::: {.tech logo="Logos/minio_logo.png"}
**MinIO**

*Alternatives considered:* storing files in PostgreSQL, a cloud bucket.

The S3 API, so the same presigned-upload code runs against a cloud bucket in production; files never pass through the API.
:::

::: {.tech logo="Logos/padlock_logo.png"}
**Passport** (JWT, Google OAuth 2.0) and **bcrypt**

*Alternatives considered:* an external identity provider.

Standard strategies [@rfc7519; @rfc6749] with the session data kept in the platform's own database.
:::

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
the one choice settled by measurement rather than by documentation; Chapter 6 reports
the measurement.

### Infrastructure and quality

**Docker Compose** runs eight services: nginx, web, api, worker, a one-shot migration
service, PostgreSQL, Redis and MinIO. **nginx** terminates TLS and routes traffic.
**GitHub Actions** runs the quality gates and builds the images; **GHCR** stores them.
**Jest** tests the backend against a real PostgreSQL database, **Playwright** drives a
real browser end to end, and **Sentry** captures errors in the four runtimes.
Kubernetes was considered and rejected: a single host with Compose is enough for the
expected load, and the containers are already stateless (NFR-26) should the platform
ever need an orchestrator.

## Main parameters and their justification {#sec:parameters}

The behaviour of the platform depends on a few numbers. @tbl:parameters gives each,
with its value and the reason for it: a source, a measurement, or a product decision
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
measurement or by the literature, and Chapter 6 checks them. The security parameters
follow published guidance. The economic parameters (prices, fee, credits, thresholds)
are product decisions: they have no "correct" value, and they are named constants in
one place in the code precisely so that they can be changed as a decision rather than
discovered in a calculation.

## Logical architecture

### Frontend

@fig:arch-frontend shows the logical architecture of the frontend, organised in layers
from the routes down to the network.

![Logical frontend architecture](../diagrams/fig-3-1-architecture-frontend/fig-3-1-architecture-frontend.png){#fig:arch-frontend}

The **routes** (28 pages) compose **feature modules** (18) over a **state and data**
layer (query cache, stores, token-refresh interceptors, analytics tracker), and a
**request proxy** guards private routes. Only live notifications and direct uploads
bypass the API, so token refresh and error handling are written once.

### Backend

@fig:arch-backend shows the backend, which runs as two processes from the same image.

![Logical backend architecture](../diagrams/fig-3-2-architecture-backend/fig-3-2-architecture-backend.png){#fig:arch-backend}

The **API** passes every request through a rate limiter, then the guards composed by
`@Auth()`, into feature modules by domain. The **worker** runs from the same image and
consumes six queues: embeddings, analytics, marketplace, AI tokens, documents and
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

This chapter situated the project, showed that no existing family of solutions
combines AI writing grounded in the writer's own work, buyer-facing analytics and a
licensing market, and justified the use of Scrum and its adaptation to a one-person
project. It then identified the five actors, specified {{FRS}} functional and 37
non-functional requirements with the way each is verified, presented the global use
case and class diagrams, and organised the work into a backlog of {{STORIES}} user
stories delivered by nine sprints in four releases. Finally, it presented the working
environment, compared the technological choices with their alternatives, justified
the main parameters of the system, and described its logical and physical
architecture and its delivery pipeline. The following chapters present the four
releases, starting with the functional foundation.
