# General introduction {.unnumbered}

Writing has never been easier to publish and never harder to be paid for. Blogging
platforms and newsletter services let anyone reach readers in minutes, and large
language models now help with drafting, rephrasing and editing. Yet the market that
pays writers is narrow: of the roughly 50 million people who create content for an
audience, only about 4% earn more than $100,000 a year,
and most of the income comes from brand deals rather than from the writing itself
[@goldman2023creator]. Publications that would pay for good work struggle to find it
and, once they find it, to judge it on anything firmer than a few samples and
intuition.

This end-of-studies project starts from that double gap. On one side, writers need an
assistant that helps them write *in their own voice*, not a generic text generator. On
the other, magazines need objective signals (who reads a writer, how far, how often
they come back) before they commit money. Between them, a market is missing: a
place where a magazine can browse, evaluate and license an existing article directly
from its author, with clear terms and a trustworthy record of who paid what.

**Inkwell.ai** is the platform built to fill that gap. It combines 3 pillars:

1. **AI-collaborative writing**: an assistant integrated into the editor as chat,
   inline actions and voice input, grounded in the writer's published corpus and in
   reference documents the writer uploads, able to write directly into the draft.
2. **Decision-support analytics**: every published article generates audience,
   content and quality signals that feed dashboards for the writer and an evaluation
   report for magazines, completed by AI-generated portfolio insights.
3. **An article licensing marketplace**: magazines are a distinct account type that
   subscribes, receives monthly credits, previews an article for 10% of its price
   and buys the rest for exclusive republication rights.

The work was carried out over 6 months, from February to July 2026, following the
Scrum framework in 9 fixed 2-week sprints grouped into 4 releases. This report
follows that structure:

- **Chapter 1** presents the context of the project, studies the existing solutions
  and justifies the development method. It then analyses and specifies the
  requirements (actors, functional and non-functional requirements, the global use
  case and class diagrams, the product backlog and the release plan) and describes the
  working environment, the technological choices, the main parameters of the system
  and its logical and physical architecture.
- **Chapters 2 to 5** present the 4 releases sprint by sprint (the sprint backlog,
  the analysis, the design and the realisation), from the functional foundation to
  the marketplace, testing and deployment, and finally to the reworked assistant and
  the document library.
- **Chapter 6** evaluates the result: the retrieval behind the assistant, the hybrid
  search, the moderation classifier, the performance and accessibility of the
  platform, the test coverage and the delivery itself.

A general conclusion summarises the results, states the limitations of the work and
opens perspectives for the platform. The 2 annexes give the full functional
requirements and the full product backlog.
