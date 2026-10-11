# Project context and requirements analysis {#sec:ch1}

## Introduction {.unnumbered}

This chapter sets out what the project is and what it must do. Its first part places
the project in its context: the host organisation, the observations that motivated
it, the existing solutions, the problem and the proposed solution, and the
development method adopted and how it was adapted. Its second part specifies the
requirements: the actors, the functional and non-functional requirements, the global
use case and class diagrams, and the organisation of the work as a product backlog
and a release plan.

## Project context {#sec:context}

### Host organisation

This project was carried out at **Intuitiv Group**, a company with a dual culture: at
once an IT services company (*Entreprise de Services du Numérique*, ESN) and an
interactive agency. It works with large national and international groups while
keeping a human-scale structure, and positions itself on reactivity, reliability and
quality of service. That dual culture suits Inkwell.ai, which is as much a software
engineering effort — architecture, data, security, delivery — as a product and
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
  reading in detail — Medium pays its writers according to members' reading time,
  read ratio and engagement [@medium2026partner] — yet these signals are shown to the
  writer or used to rank content, never presented to a buyer judging the writer.
- **Paid writing is a narrow market.** About four percent of creators earn more than
  a hundred thousand dollars a year, and most creator income comes from brand deals
  [@goldman2023creator]. None of the publishing platforms studied below offers a
  publication a way to license an article that already exists.

### Study of existing solutions {#sec:existing}

The solutions close to the project fall into five families. **Publishing platforms**
such as Medium pay writers from a pool of reader subscriptions
[@medium2026partner]. **Newsletter platforms** — Substack, Ghost and beehiiv — let a
writer charge readers directly [@substack2026; @ghost2026], and beehiiv adds an AI
writing assistant to its editor [@beehiiv2026]. **Freelance marketplaces** such as
Contently and Upwork connect clients with writers for *commissioned* work: the article
does not yet exist when it is bought, and the platform holds no engagement data on
the writer's published pieces [@contently2026; @upwork2026]. **AI writing
assistants** such as Grammarly and Notion AI improve or generate text inside a
document [@grammarly2026; @notionai2026]. Finally, **source-grounded assistants** —
NotebookLM, ChatGPT with uploaded files, Perplexity Spaces — answer from documents the
user uploads and cite the passages they used [@notebooklm2024; @chatgptfiles2026;
@perplexity2026].

@tbl:existing compares these families on the criteria the project targets. Each cell
records what the product's own documentation states; "partial" means the capability
exists in a restricted form, explained below the table.

| Criterion | Medium | Newsletter platforms¹ | Freelance markets² | Writing assistants³ | Grounded assistants⁴ | **Inkwell.ai** |
|:------------------------------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| Publishing and public reading | ✓ | ✓ | — | — | — | ✓ |
| AI assistance in the editor | — | partial | — | ✓ | — | ✓ |
| Assistant grounded in the writer's published work | — | — | — | — | partial | ✓ |
| Answers citing uploaded documents | — | — | — | — | ✓ | ✓ |
| Engagement analytics for the writer | ✓ | ✓ | — | — | — | ✓ |
| Analytics exposed to a buyer as evidence | — | — | — | — | — | ✓ |
| Licensing of existing articles to publications | — | — | — | — | — | ✓ |
| Traceable payments | ✓ | ✓ | ✓ | — | — | ✓ |

: Comparison of existing solutions, from each product's public documentation {#tbl:existing}

¹ Substack, Ghost, beehiiv. ² Contently, Upwork. ³ Grammarly, Notion AI. ⁴ NotebookLM, ChatGPT with files, Perplexity Spaces.

Two cells need a word. beehiiv is the only newsletter platform of the three with an
assistant in its editor, hence "partial" for that family. The source-grounded
assistants could be grounded in a writer's published work only if the writer
uploaded it by hand, and they are separate from any editor or publishing workflow.

The decisive cells are the last three rows. Citing uploaded documents, taken alone, is
**not** distinctive: the source-grounded assistants already do it, and Inkwell.ai
borrows the idea. What no family offers is the *combination* — an assistant grounded
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

A **sequential (waterfall) process** runs requirements, design, implementation, testing
and delivery once each, in order; its classic description already warned that testing
at the end exposes design errors when they are most expensive to correct
[@royce1970]. An **agile process** builds the product in short iterations, each
delivering working software that is reviewed before the next is planned, and values
responding to change over following a plan [@agilemanifesto2001; @sommerville2016].
@fig:waterfall-agile contrasts the two.

![Classic and agile approaches compared](../diagrams/fig-1-2-waterfall-vs-agile/fig-1-2-waterfall-vs-agile.png){#fig:waterfall-agile height=45%}

The figure makes the deciding difference visible: in the sequential process the first
working software appears in the last phase, while in the agile process it appears at
the end of the first iteration. Inkwell.ai is built in layers that each depend on the
one below — the marketplace evaluates writers on analytics, analytics need published
articles, articles need accounts and an editor — so a defect in a lower layer must be
found before the next is built on it. Short iterations that end in working, tested
software are what that layering requires.

### Scrum, and its adaptation to a one-person project {#sec:scrum}

Among agile frameworks, **Scrum** was chosen for its fixed-length sprints and its
explicit artefacts and events [@scrumguide2020], which give an individual project the
regular checkpoints a supervisor can follow. @fig:scrum shows the framework as it was
applied.

![The Scrum framework, as practised in this project](../diagrams/fig-1-1-scrum-framework/fig-1-1-scrum-framework.png){#fig:scrum height=45%}

The figure reads from left to right: the product backlog feeds sprint planning, the
sprint backlog is built during a fixed two-week sprint, and every sprint ends with an
increment checked against the definition of done, reviewed, and followed by a
retrospective whose actions return to the next planning. What it implies for this
project is that the unit of progress is the increment, not the document: each sprint
must leave the platform runnable and tested.

Scrum is designed for a team of ten or fewer people holding three accountabilities —
Product Owner, Scrum Master and Developers [@scrumguide2020] — and this project has one
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

With one person, the value of Scrum lies in the discipline it imposes — a fixed
cadence, a written goal per sprint, an increment that must work — rather than in
coordination.

### Prioritisation and estimation {#sec:estimation}

Requirements and user stories are prioritised with **MoSCoW** — Must, Should, Could,
Won't — the prioritisation technique of the DSDM agile framework, in which the Must
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
generated (draw.io) in the project repository, versioned beside the code they
describe.

## Identification of the actors {#sec:actors}

The platform has five actors. @tbl:actors lists them with the way each is represented
in the data model, because the actors are not invented for the analysis: they follow
from two properties every account carries — its **account type** (personal or
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
and a magazine's **subscription** (active or not). They are states of an account —
the same person moves between them by upgrading, by being read, or by subscribing — so
they are drawn in the use case diagrams as **conditions** on the use cases they unlock,
not as separate actors: *Read a premium article* extends *Read an article* when
`[plan = premium]`, *List on the marketplace* extends *Publish an article* when
`[writer is eligible]`, and every marketplace use case requires an active
subscription.

Two generalisations hold: the reader specialises the visitor, and the writer
specialises the reader. The other two actors specialise nobody. A **magazine** is a
different account type with no role and no plan — a database constraint enforces it —
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
expected for a platform whose three pillars depend on one another — dropping a Must
from one pillar would break another. The Should and Could requirements are the
comforts that make each feature pleasant rather than possible: search and browsing
by tag, live comment previews, voice, sharing. The writers carry the most
requirements (31), because the editor, the assistant, the analytics and the earnings
all belong to them; the administrator carries the fewest (5), all delivered in one
sprint. A requirement listed under two sprints is delivered in two steps, the
second sprint completing the rule the first one prepared; Chapters 3 to 6 say which
part each sprint delivers.

## Non-functional requirements {#sec:nfr}

Each non-functional requirement is stated as a property together with the mechanism
that provides it and the way it is verified: by an automated **test** of the backend
suite, by a **measurement** reported in Chapter 7, by **inspection** of the code or the
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
| NFR-14 | Feed pagination is cursor-based, stable under insertion | — | **not met**: pagination is by offset |
| NFR-15 | Dashboard totals and rates read pre-aggregated rows | four rollup tables refreshed by the worker | measurement |
| NFR-16 | Analytics aggregation is incremental and idempotent | each run reads only the events since the last one | inspection |
| NFR-17 | Expensive AI output is cached and invalidated by what changes it | insights cached 24 h, dropped when the writer publishes | inspection |
| NFR-18 | Streaming responses are never buffered end to end | nginx `proxy_buffering off`, 300 s read timeout | inspection |
| | **Reliability** | | |
| NFR-19 | Every denormalised balance equals the sum of its ledger rows | three invariants asserted after every money-moving test | test |
| NFR-20 | Concurrent purchases cannot double-spend | `SELECT … FOR UPDATE` on the balance-owning row | test |
| NFR-21 | Schema changes are versioned and applied before the application starts | a one-shot migration service | inspection |
| NFR-22 | The vector extension exists before any migration that needs it | the migration runner creates it first | inspection |
| NFR-23 | Failed background jobs retry with exponential back-off | — | **not met**: jobs run once |
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
measurement in Chapter 7; two are enforced by the continuous-integration pipeline.
The others rest on inspection — they are properties of configuration (port bindings,
nginx buffering, Compose dependencies) rather than of behaviour, and a test would only
restate the configuration. Five are not fully met and are stated as such: NFR-14
(offset pagination), NFR-23 (no queue is configured with retries, so a failed job is
not attempted again), NFR-25 (readiness ignores Redis), NFR-28 (horizontal scaling is
designed for but was never exercised) and NFR-37 (met on desktop and for critical
violations, not on mobile — see @sec:eval-perf). They return as limitations in the
general conclusion.

## Global use case diagrams {#sec:uc-global}

The global use cases are drawn in three diagrams, one per group of actors, so that
each use case is a single action and every label can be read at page width. The
use cases are those of the functional requirements; the per-sprint diagrams of
Chapters 3 to 6 then refine each sprint's share. In the three diagrams, every use case
of a signed-in actor includes *Sign in*, which is stated once in a note rather than
drawn twenty times.

**Visitor and reader.** @fig:uc-visitor-reader gives the use cases of the two actors
who read.

![Global use case diagram — visitor and reader](../diagrams/fig-1-3-use-case-visitor-reader/fig-1-3-use-case-visitor-reader.png){#fig:uc-visitor-reader}

The visitor browses the feed, reads free articles, searches, views profiles and
shares, and reaches registration from *Sign in*: *Create an account* and *Sign in with
Google* both extend it. The reader inherits all of this and adds the social use
cases — liking, commenting and replying, liking a comment, reposting, saving,
following, blocking, reporting — together with notifications, the profile and the
upgrade to premium. The premium plan does not make a new actor: *Read a premium
article* extends *Read an article* under the condition `[plan = premium]`. The
diagram shows that the reader's use cases are all small, independent interactions
with one article or one account, which is why each is delivered by a short story of
the backlog.

**Writer.** @fig:uc-writer gives the use cases of the writer.

![Global use case diagram — writer](../diagrams/fig-1-4-use-case-writer/fig-1-4-use-case-writer.png){#fig:uc-writer}

The writer inherits the reader's use cases and adds three groups: writing (drafting
with automatic saving, images, publishing with a placement and a visibility,
withdrawing a listing, deleting), the assistant (asking, inline actions, a write into
the draft that the writer keeps or discards, dictation, replies read aloud, documents
uploaded, attached and cited by page), and the writer's own figures (analytics,
eligibility progress, earnings). Eligibility appears as a condition, not an actor:
*Publish as premium* and *List on the marketplace* extend *Publish an article* when
`[writer is eligible]`. Every use of the assistant includes *Consume the AI
allowance*, which only the premium plan grants. The diagram shows where the
complexity of the platform lies: the writer has the most use cases, and most of the
inclusions and extensions sit around *Publish an article* and *Ask the assistant*.

**Magazine and administrator.** @fig:uc-magazine-admin gives the use cases of the two
actors that specialise nobody.

![Global use case diagram — magazine and administrator](../diagrams/fig-1-5-use-case-magazine-admin/fig-1-5-use-case-magazine-admin.png){#fig:uc-magazine-admin}

A magazine subscribes, tops up credits, cancels and follows its balance; with an
active subscription it browses writers, reads their evaluation (extended by the
generation of portfolio insights), browses the marketplace, purchases an article
(extended by a preview unlock), keeps it in its library and publishes it. The four
marketplace use cases include *Check the active subscription*: the subscription is
the gate, not a different actor. The administrator works the report queue — dismissing
a report, removing an article or banning its author — searches users, changes a plan
and grants eligibility. Drawing the two actors side by side without a generalisation
shows the answer to a question the single diagram left open: neither the magazine nor
the administrator is a kind of reader or writer.

## Global class diagram {#sec:classes-global}

The data model counts thirty persisted tables. Drawn in a single diagram they form an
unreadable strip, because `User` is related to most of the others, so the global class
diagram is split by domain into two figures. Attributes are shown with domain types
(`Json`, `Vector`, `Timestamp`); audit columns are omitted. Each class shows the main
**operations** it supports; they are implemented by the service of the same domain
(for instance `Article.publish()` by the articles service), because the classes are
persisted records and the behaviour lives in the service layer. Relationships that
carry nothing but a pair and a date — likes, comment likes, reposts, saves, follows,
blocks, tags — are drawn as many-to-many associations; each is stored as a join table
with a unique constraint on its pair. The operations that create them — `like()`, `repost()`, `save()`,
`follow()`, `block()`, `likeComment()` — belong to `User`, the class that acts.

**Core domain.** @fig:classes-core shows accounts, articles and their social layer: the
`User` and its optional `MagazineProfile`, the `Article` with its placement,
visibility and price, tags, threaded comments, notifications and reports.

![Class diagram: core domain](../diagrams/fig-2-2-classes-core-domain/fig-2-2-classes-core-domain.png){#fig:classes-core}

The diagram shows that the social layer adds no entity of its own: every interaction
is an association between a user and an article, a comment or another user. That is
what makes interactions cheap to count for analytics and impossible to duplicate,
since the unique pair constraint turns a repeated like into a no-op.
`Article.publisherId` names the magazine that published a licensed article and is
empty for every other article; it is the single attribute through which the
marketplace changes the core model.

**AI, marketplace and analytics.** @fig:classes-ai shows the remaining tables: the
article chunks embedded for retrieval, the writer memory, the cached portfolio
insights and the AI interaction log; the private document library and its chunks;
purchases, ledger transactions, magazine subscriptions and the eligibility audit log;
and the raw analytics events with the four metric rollups.

![Class diagram: AI, marketplace and analytics](../diagrams/fig-2-3-classes-ai-marketplace-analytics/fig-2-3-classes-ai-marketplace-analytics.png){#fig:classes-ai}

Two properties follow from this diagram. Money is never a single number: a
`Purchase` records two to three `Transaction` rows, and every balance can be
recomputed from them, which is what the ledger invariants of NFR-19 check. And the
analytics are layered: raw `AnalyticsEvent` rows are written once and never read by a
dashboard, which reads only the rollups, so a dashboard's cost does not grow with the
event log (NFR-15).

## Product backlog {#sec:backlog}

The product backlog expresses the requirements as user stories of the form *"As an
⟨actor⟩, I want ⟨goal⟩ so that ⟨benefit⟩"*, grouped into nine epics, prioritised with
MoSCoW and estimated in story points relative to the simplest story (US-01). The
backlog counts **{{STORIES}} stories for {{POINTS}} points**. @tbl:backlog-summary
summarises it by epic; the full backlog is given in Annex B.

<!-- INCLUDE:backlog-summary -->

The distribution of points shows where the effort lies. The AI assistance epic is the
heaviest (21% of the points) although it is not the largest in stories: its stories —
retrieval grounded in the writer's corpus, writing into the document, voice, the
document library — are few but each is large, because each joins a model call to the
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
environment in Chapter 2.

| Release | Sprint | Dates | Goal | Points |
|:----------------------------|:---|:----------|:--------------------------------------|:-:|
| **R1 — Functional foundation** | Sprint 1 | 09/02 – 20/02 | Schema, authentication, article core, ledger invariant harness | {{S1PTS}} |
| | Sprint 2 | 06/04 – 17/04 | Editor, AI chat and inline actions, analytics event capture | {{S2PTS}} |
| **R2 — Social, analytics and AI** | Sprint 3 | 20/04 – 01/05 | Social interactions, notifications, aggregation, dashboards | {{S3PTS}} |
| | Sprint 4 | 04/05 – 15/05 | Retrieval-augmented generation, portfolio insights, hybrid search, writer memory | {{S4PTS}} |
| **R3 — Marketplace, testing and deployment** | Sprint 5 | 18/05 – 29/05 | Marketplace, subscriptions, premium, moderation, administration | {{S5PTS}} |
| | Sprint 6 | 01/06 – 12/06 | Tests, demonstration corpus, deployment, CI/CD | {{S6PTS}} |
| **R4 — Social depth, assistant and documents** | Sprint 7 | 15/06 – 26/06 | Comment likes, follower lists, block, save, share | {{S7PTS}} |
| | Sprint 8 | 29/06 – 10/07 | Live card controls, reposts, byline preview, assistant writing into the document, voice | {{S8PTS}} |
| | Sprint 9 | 13/07 – 24/07 | Document library, ingestion, attachment, citations | {{S9PTS}} |

: Release plan {#tbl:release-plan}

The order of the releases follows the layering argued in @sec:method: each release
needs the data the previous one produces. The loads are uneven. Sprint 5 commits 85
points against an average near 40, because the marketplace stories — subscription,
credits, preview, purchase, publication, earnings — share one transaction model and
were planned together rather than split across two sprints. Sprints 6, 7 and 9 are
light, for two different reasons: Sprint 6's real work, the test suite that proves
the business rules, is not expressed as user stories, and Release 4 runs alongside
the writing of this report. How this plan compares with what was delivered is
measured in @sec:velocity.

@fig:gantt places the work on the project window, from 2 February to 31 July 2026: the
foundation week and Sprint 1, the design track, Sprints 2 to 9 in four releases, and
the writing of this report alongside the last sprints.

![Gantt chart of the project](../diagrams/fig-2-4-gantt/fig-2-4-gantt.png){#fig:gantt}

The chart shows the one break in the rhythm of the sprints: the six weeks of the design
track between Sprint 1 and Sprint 2. Placing them there was deliberate — the editor
and the social features of Sprint 2 onwards were built from finished screens rather
than designed while being coded — and it is the reason the first release spans two
months instead of one.

## Conclusion {.unnumbered}

This chapter situated the project, showed that no existing family of solutions
combines AI writing grounded in the writer's own work, buyer-facing analytics and a
licensing market, and justified the use of Scrum and its adaptation to a one-person
project. It then identified the five actors, specified {{FRS}} functional and 37
non-functional requirements with the way each is verified, presented the global use
case and class diagrams, and organised the work into a backlog of {{STORIES}} user
stories delivered by nine sprints in four releases. The next chapter describes the
environment in which the work was done, the technological choices and the
architecture of the system.
