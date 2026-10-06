# General conclusion and perspectives {.unnumbered}

This project set out to connect two groups the existing platforms leave apart:
independent writers, who lack an assistant that writes in their own voice and a direct
way to be paid for quality, and magazines, which lack objective evidence to judge a
writer before buying. Inkwell.ai answers both with one platform.

Over nine two-week sprints in four releases, the project delivered:

- a **writing environment** — a rich-text editor with automatic saving and images, and
  an AI assistant grounded in the writer's own published work through
  retrieval-augmented generation, which decides per request whether to answer or to
  write into the document, writes into a protected range the writer keeps or discards,
  shows its real pipeline as it runs, accepts dictated prompts, reads its replies
  aloud, and cites reference documents to the page;
- an **analytics pipeline** — reading events captured in the browser, aggregated
  incrementally into per-article and per-writer metrics, presented to writers as
  dashboards and to magazines as an evaluation report completed by AI portfolio
  insights;
- a **marketplace** — an eligibility gate, magazine subscriptions with monthly credits,
  a two-stage exclusive purchase and the magazine's own publication, with every credit
  movement written to a ledger inside one transaction and three balance invariants
  asserted after every money-moving test;
- a **social layer** — likes, threaded comments, comment likes, reposts, follows,
  saves, blocks, sharing and live notifications — and the **moderation** console;
- the **engineering around it** — a containerised stack started by one command, a
  continuous-integration pipeline with strict typing, zero lint warnings and a
  schema-drift check, 792 backend tests and 183 end-to-end tests, a demonstration
  corpus, and a production-ready deployment.

Beyond the product, the project was an exercise in engineering discipline: requirements
stated per actor with stable identifiers, non-functional requirements tied to the
mechanism that provides them, business rules proven by tests — including tests designed
to fail when the code is sabotaged — and design documents and diagrams kept as versioned
text beside the code.

## Limitations

Some points remain open and are stated as such:

- **Live hosting.** The production stack, its TLS configuration and its delivery
  pipeline are ready and the domain is registered, but the server has not yet been
  provisioned.
- **Refresh-token revocation.** Refresh tokens are stateless; their 7-day lifetime is
  the bound on their validity, and a password change or a ban does not revoke one
  already issued.
- **Pagination.** Lists are paginated by offset; a cursor-based scheme would stay stable
  when new rows are inserted while a reader scrolls.
- **Accessibility and performance audit.** A Lighthouse score above 90 and the absence of
  critical accessibility violations on article pages (NFR-37) remain to be measured.
- **Readiness.** The readiness endpoint checks PostgreSQL but not Redis.

## Perspectives

- **Go live** on a provisioned server, then measure real traffic against the
  performance requirements.
- **Real payments** in place of the simulated ones, with the ledger already designed to
  record them.
- **Revocable sessions**, by storing refresh tokens server-side.
- **Richer AI collaboration**: dictating whole articles, writer-specific style
  learning beyond the current voice profile, and feedback on weak sections.
- **Wider audience**: multilingual publishing and a native mobile application on the
  existing 375 px designs.
- **Deeper analytics**: geographic and device distribution collected with the reader's
  consent, and topic-relevance ordering when magazines browse writers.

\newpage

# References {.unnumbered}

1. Schwaber, K. and Sutherland, J. *The Scrum Guide*. scrumguides.org, 2020.
2. Object Management Group. *Unified Modeling Language (UML), version 2.5.1*. 2017.
3. Lewis, P. et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP
   Tasks". *Advances in Neural Information Processing Systems 33*, 2020.
4. Cormack, G. V., Clarke, C. L. A. and Büttcher, S. "Reciprocal Rank Fusion
   Outperforms Condorcet and Individual Rank Learning Methods". *Proceedings of SIGIR*,
   2009.
5. Malkov, Y. A. and Yashunin, D. A. "Efficient and Robust Approximate Nearest
   Neighbor Search Using Hierarchical Navigable Small World Graphs". *IEEE
   Transactions on Pattern Analysis and Machine Intelligence*, 2018.
6. Next.js documentation — nextjs.org/docs.
7. NestJS documentation — docs.nestjs.com.
8. PostgreSQL 16 documentation — postgresql.org/docs/16 (full-text search).
9. pgvector — github.com/pgvector/pgvector.
10. BullMQ documentation — docs.bullmq.io.
11. Drizzle ORM documentation — orm.drizzle.team.
12. Vercel AI SDK documentation — ai-sdk.dev.
13. TipTap documentation — tiptap.dev.
14. Docker Compose documentation — docs.docker.com/compose.
15. Playwright documentation — playwright.dev.
