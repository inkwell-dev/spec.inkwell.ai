# General conclusion and perspectives {.unnumbered}

This project set out to connect two groups the existing platforms leave apart:
independent writers, who lack an assistant that writes in their own voice and a direct
way to be paid for quality, and magazines, which lack objective evidence to judge a
writer before buying. Inkwell.ai answers both with one platform.

Over nine two-week sprints in four releases, the project delivered:

- a **writing environment**: a rich-text editor with automatic saving and images, and
  an AI assistant grounded in the writer's own published work through
  retrieval-augmented generation, which decides per request whether to answer or to
  write into the document, writes into a protected range the writer keeps or discards,
  shows its real pipeline as it runs, accepts dictated prompts, reads its replies
  aloud, and cites reference documents to the page;
- an **analytics pipeline**: reading events captured in the browser, aggregated
  incrementally into per-article and per-writer metrics, presented to writers as
  dashboards and to magazines as an evaluation report completed by AI portfolio
  insights;
- a **marketplace**: an eligibility gate, magazine subscriptions with monthly credits,
  a two-stage exclusive purchase and the magazine's own publication, with every credit
  movement written to a ledger inside one transaction and three balance invariants
  asserted after every money-moving test;
- a **social layer** (likes, threaded comments, comment likes, reposts, follows,
  saves, blocks, sharing and live notifications) and the **moderation** console;
- the **engineering around it**: a containerised stack started by one command, a
  continuous-integration pipeline with strict typing, zero lint warnings and a
  schema-drift check, 796 backend tests, a demonstration corpus and a production-ready
  stack.

The evaluation of Chapter 7 measured the result rather than asserting it: retrieval
returns a relevant passage for 89% of questions, hybrid search keeps every relevant
article for paraphrased queries that keyword search misses, the moderation classifier
reaches a precision of 0.93 and a recall of 1.00, the API answers in tens of
milliseconds, and 98% of the planned points were delivered.

Beyond the product, the project was an exercise in engineering discipline:
requirements stated per actor with stable identifiers, non-functional requirements tied
to the mechanism that provides them and to the way they are verified, business rules
proven by tests (including tests designed to fail when the code is sabotaged) and
claims checked by measurement, which in two cases corrected the project itself.

## Limitations {.unnumbered}

Some points remain open and are stated as such.

1. **Public hosting.** The production stack, its TLS configuration and its delivery
   pipeline are ready and the domain is registered, but no server was provisioned, so
   US-55 is only partly delivered.
2. **Background job retries.** No queue is configured with retries, so a job that fails
   (an embedding during a provider outage, for instance) is not attempted again
   (NFR-23).
3. **Pagination.** Lists are paginated by offset; a cursor-based scheme would stay
   stable when new rows are inserted while a reader scrolls (NFR-14).
4. **Readiness.** The readiness endpoint checks PostgreSQL but not Redis (NFR-25).
5. **Mobile performance and accessibility.** On the mobile preset the article pages
   score 63 to 74 for performance, and the public pages carry serious, though not
   critical, accessibility violations: insufficient contrast and icon-only links
   without a name (NFR-37).
6. **Session revocation.** Refresh tokens are stateless: a password change does not
   revoke one already issued, which stays valid until its seven days expire. A ban is
   enforced at the next refresh, within fifteen minutes.
7. **Test coverage of the analytics.** The aggregation queries have no unit tests; they
   are verified only end to end and by measurement.
8. **Search under quota exhaustion.** When the embedding provider's quota is exhausted,
   search falls back to keywords only after about six seconds of retries.

## Perspectives {.unnumbered}

- **Go live** on a provisioned server, then measure real traffic against the
  performance requirements.
- **Harden the background work**: retries with back-off on every queue, and a
  readiness check that includes Redis.
- **Tune retrieval and search with the measurements of Chapter 7**: raise the
  similarity floor to 0.65, cache the embeddings of frequent queries, and fail fast to
  keyword search once the provider's quota is known to be exhausted.
- **Fix the accessibility findings** (contrast tokens and accessible names on icon
  links) and improve the mobile loading of article pages.
- **Test the aggregation** with fixtures of known events and expected metrics.
- **Real payments** in place of the simulated ones, with the ledger already designed to
  record them, and **revocable sessions** by storing refresh tokens server-side.
- **Richer AI collaboration**: dictating whole articles, style learning beyond the
  current voice profile, and feedback on weak sections.
- **Wider audience**: multilingual publishing and a native mobile application on the
  existing 375 px designs.
