# General introduction {.unnumbered}

Writing has never been easier to publish and never harder to be paid for. Blogging
platforms and newsletter services let anyone reach readers in minutes, and large
language models now help with drafting, rephrasing and editing. Yet an independent
writer who produces consistently good work still has few routes to income beyond
advertising or reader subscriptions, and the publications that would happily pay for
that work struggle to find it — and, once they find it, to judge it on anything firmer
than a few samples and intuition.

This end-of-studies project starts from that double gap. On one side, writers need an
assistant that helps them write *in their own voice*, not a generic text generator; on
the other, magazines need objective signals — who reads a writer, how far, how often
they come back — before they commit money. Between the two, a market is missing: a
place where a magazine can browse, evaluate and license an existing article directly
from its author, with clear terms and a trustworthy record of who paid what.

**Inkwell.ai** is the platform built to fill that gap. It combines three pillars:

1. **AI-collaborative writing** — an assistant integrated into the editor as chat,
   inline actions and voice input, grounded in the writer's published corpus and in
   reference documents the writer uploads, able to write directly into the draft;
2. **decision-support analytics** — every published article generates audience,
   content and quality signals that feed dashboards for the writer and an evaluation
   report for magazines, completed by AI-generated portfolio insights;
3. **an article licensing marketplace** — magazines are a distinct account type that
   subscribes, receives monthly credits, previews an article for a tenth of its price
   and buys the rest for exclusive republication rights.

The work was carried out over six months, from February to July 2026, following the
Scrum framework in nine fixed two-week sprints grouped into four releases. This report
follows that structure:

- **Chapter 1** presents the context of the project, studies existing solutions,
  states the problem and justifies the choice of Scrum as the development method.
- **Chapter 2** analyses and specifies the requirements: actors, functional and
  non-functional requirements, the global use case and class diagrams, the product
  backlog and the release plan.
- **Chapter 3** describes the working environment, the technological choices and the
  logical and physical architecture of the system.
- **Chapters 4 to 7** present the four releases sprint by sprint — the sprint backlog,
  the analysis and design (use case, class and sequence diagrams) and the
  realisation — from the functional foundation to the marketplace, testing and
  deployment, and finally to the reworked assistant and the document library.

A general conclusion summarises the results and opens perspectives for the platform.

\newpage

# Chapter 1 — Project context and methodology

## Introduction

This chapter situates the project. It presents the host organisation and the context
in which Inkwell.ai was conceived, studies the existing solutions on both sides of the
market, states the problem the project addresses and the solution it proposes, and
closes with the development methodology adopted and the reasons for choosing it.

## 1.1 Host organisation

This project was carried out at **Intuitiv Group**. Intuitiv describes itself as a
company with a dual culture: at once an innovative **ESN** (*Entreprise de Services du
Numérique*, an IT services company) and an **interactive agency**. It positions itself
on reactivity, innovation, reliability and quality of service, and works with large
national and international groups while deliberately keeping a human-scale structure.

That dual culture suits a project like Inkwell.ai, which is as much a software
engineering effort — architecture, data, security, delivery — as a product and
interface design effort, from the design system to the screens a writer works in
every day.

## 1.2 Project context

The project was proposed as an end-of-studies engineering project with an ambitious,
product-shaped scope: not a prototype of one feature, but a complete two-sided platform
with real accounts, real data flows, an AI layer and money-like transactions. Three
observations motivated it.

- **Generative AI has changed how text is produced**, but most writing assistants are
  generic: they write *for* the user rather than *like* the user, and they know nothing
  of what the writer has already published.
- **Engagement data is collected everywhere and used for very little.** Platforms
  measure views and reading time to rank content for readers, but none exposes those
  signals as evidence to a buyer evaluating a writer.
- **Content licensing between independent writers and publications is informal.** It
  happens by e-mail, on personal relationships, with no shared record of terms or
  payments.

## 1.3 Study of existing solutions

### 1.3.1 Publishing and newsletter platforms

**Medium** is an open publishing platform where readers subscribe to the platform and
writers in its partner programme are paid according to member reading time. It offers
good reading surfaces and audience statistics, but no AI assistance grounded in the
writer's corpus, and no way for a publication to license an article.

**Substack** lets writers run paid newsletters: readers subscribe to a writer directly.
It has made independent writing a viable business for some, but its economic model is
the reader subscription; there is no marketplace in which a publication buys an
existing piece.

### 1.3.2 Freelance content marketplaces

Content marketplaces such as **Contently** or general freelance platforms connect
brands with writers for *commissioned* work. Evaluation rests on portfolios, ratings
and interviews; the work does not yet exist when it is bought, and the platform holds
no engagement data about the writer's published pieces.

### 1.3.3 AI writing assistants

Tools such as **Grammarly** or **Notion AI** assist with grammar, tone and generation
inside a document. They are powerful editors, but they are not grounded in the
writer's own body of work, they do not cite the sources a passage came from, and they
are disconnected from any publishing or licensing workflow.

### 1.3.4 Comparative synthesis

Table 1.1 compares these families of solutions with the criteria the project targets.

**Table 1.1 – Comparison of existing solutions**

| Criterion | Medium | Substack | Content marketplaces | AI writing assistants | **Inkwell.ai** |
|---|:-:|:-:|:-:|:-:|:-:|
| Publishing and public reading | ✓ | ✓ | — | — | ✓ |
| AI assistance in the editor | — | — | — | ✓ | ✓ |
| Assistant grounded in the writer's own work | — | — | — | — | ✓ |
| Answers citing uploaded documents by page | — | — | — | partial | ✓ |
| Engagement analytics for the writer | ✓ | ✓ | — | — | ✓ |
| Analytics exposed to a buyer as evidence | — | — | — | — | ✓ |
| Licensing of existing articles to publications | — | — | — | — | ✓ |
| Traceable payments (ledger) | partial | ✓ | ✓ | — | ✓ |

## 1.4 Problem statement

The study shows that each existing family covers part of the need and that the parts do
not meet. The problem can be stated on three levels:

- **Supply side.** Writers lack an assistant that helps them write better *in their own
  voice*, grounded in what they have already published and in the material they are
  working from, and they lack a direct path to be paid for quality.
- **Demand side.** Magazines lack objective, comparable signals about a writer's
  audience, consistency and quality, and must evaluate by hand.
- **Market.** There is no self-service place where a publication can discover,
  evaluate, preview and license an existing article, with the money recorded in a way
  both parties can trust.

## 1.5 Proposed solution

Inkwell.ai answers these three levels with one platform:

- an **editor with an AI assistant** that retrieves passages from the writer's own
  published articles and attached reference documents, decides per request whether to
  answer in a panel or write into the document, streams what it writes into a
  protected range the writer keeps or discards, cites passages by page, and accepts
  spoken prompts;
- an **analytics pipeline** that turns reading events into per-article and per-writer
  metrics, presented to the writer for self-improvement and to magazines as an
  evaluation report with AI portfolio insights;
- a **marketplace** gated by an eligibility threshold, where magazines with an active
  subscription preview an article for 10% of its price, buy the remaining 90% for
  exclusive rights, and publish it under their own masthead — every credit movement
  being written to a ledger inside one database transaction.

## 1.6 Development methodology

### 1.6.1 Sequential and agile approaches

A **sequential (waterfall) process** runs requirements, design, implementation, testing
and delivery once each, in order; working software exists only at the end. An **agile
process** builds the product in short iterations, each delivering a working increment
that is reviewed before the next is planned. Figure 1.2 contrasts the two.

![Figure 1.2 – Classic and agile approaches compared](../diagrams/fig-1-2-waterfall-vs-agile/fig-1-2-waterfall-vs-agile.png){width=100%}

### 1.6.2 Choice of Scrum

Inkwell.ai is built in layers that each depend on the previous one: the marketplace
evaluates writers on analytics, analytics need published articles, and articles need
accounts and an editor. An iterative method fits that layering: each sprint delivers a
working layer that the next one builds on and that can be demonstrated on its own.
Among agile frameworks, **Scrum** was chosen for its fixed-length sprints, its explicit
artefacts — product backlog, sprint backlog, increment — and its events, which give an
individual project the regular checkpoints a supervisor can follow.

### 1.6.3 Scrum as practised in this project

Figure 1.1 shows the framework as it was applied.

![Figure 1.1 – The Scrum framework, as practised in this project](../diagrams/fig-1-1-scrum-framework/fig-1-1-scrum-framework.png){width=100%}

- **Roles.** The project is carried out by one person, who therefore holds the roles of
  Development Team and Scrum Master. The academic supervisor acts as Product Owner at
  sprint boundaries, reviewing each increment against the backlog.
- **Artefacts.** The product backlog holds 72 user stories in 9 epics, prioritised with
  MoSCoW and estimated in story points (Chapter 2). Each sprint has its own backlog and
  ends with a working increment.
- **Events.** Each two-week sprint starts with planning — pulling the highest-priority
  stories and setting a sprint goal — and ends with a review of the increment and a
  retrospective. Each phase of work carries written exit criteria, which is what lets
  every release chapter show evidence rather than assert completion.

### 1.6.4 Modelling language

Analysis and design use **UML 2**: use case diagrams for the functional scope of each
sprint, class diagrams for the data model, sequence diagrams for the main interactions,
and activity and state diagrams where a decision or a lifecycle is the subject. The
diagrams are kept as text sources (PlantUML) or generated (draw.io) in the project
repository, so they are versioned beside the code they describe.

## Conclusion

This chapter presented the context of the project, compared the existing solutions and
showed that none combines AI-assisted writing grounded in the writer's own work,
buyer-facing analytics and a licensing market. It stated the resulting problem and the
proposed solution, and justified the use of Scrum. The next chapter analyses and
specifies the requirements of the platform.

\newpage
