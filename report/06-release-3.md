# Chapter 6 — Release 3: marketplace, testing and deployment

## Introduction

The third release delivers the reason the analytics exist: the marketplace. Sprint 5
adds the premium plan, magazine subscriptions and credits, the eligibility gate, the
two-stage purchase with exclusive rights and the magazine's own act of publishing, and
the moderation console. Sprint 6 hardens the whole: the test strategy, a demonstration
corpus, and a production-ready deployment with its continuous-delivery pipeline.

## 6.1 Sprint 5 — Marketplace, subscriptions, premium and moderation

### 6.1.1 Sprint goal and backlog

**Goal:** readers upgrade to premium; magazines subscribe and receive monthly credits;
eligible writers list articles; magazines preview, buy and publish them under their own
masthead, every credit movement recorded in a ledger; writers see their earnings;
administrators moderate.

**Table 6.1 – Sprint 5 backlog**

<!-- INCLUDE:sprint-5 -->

### 6.1.2 Business rules

**Table 6.2 – Marketplace rules**

| Rule | Value |
|---|---|
| Eligibility to list or publish premium | 5,000 identified unique readers **and** 1,000 reactions (likes and comments) across the writer's public articles, lifetime; or a manual grant by an administrator. Never revoked automatically. |
| Magazine subscription | monthly; grants 500 credits a month; unspent credits roll over |
| Preview unlock | 10% of the article's price, credited towards the purchase |
| Full purchase | the remaining 90%; exclusive — no other magazine can preview or buy the article afterwards |
| Platform fee | 20% of each stage, rounded down; the writer receives the rest |
| Publication | a separate, deliberate act of the owning magazine: the article becomes public and free, its price is cleared and the magazine is recorded as publisher |

### 6.1.3 Analysis

**Use case diagram.** Figure 6.1 gives the use cases of Sprint 5. An unsubscribed
magazine can only subscribe; a subscribed magazine browses the marketplace, purchases
an article exclusively — unlocking a preview extends the purchase — tops up credits,
views its library and publishes a purchased article from it. Every credit movement
includes moving credits in one transaction. An eligible writer lists an article,
which includes setting a price and classifying the content at publish time; the
administrator reviews the report queue, grants eligibility and manages users.

![Figure 6.1 – Use case diagram, Sprint 5](../diagrams/fig-6-1-use-case-sprint-5/fig-6-1-use-case-sprint-5.png){width=100%}

### 6.1.4 Design

**Class diagram.** Figure 6.2 shows licensing and the ledger. A `Purchase` records a
stage — preview unlock or full purchase — with the credits paid, the platform fee and
the writer's payout, and a full purchase links to the preview that preceded it. Each
stage writes three `Transaction` rows: the magazine's debit, the writer's payout and
the platform fee; amounts are always positive and their direction comes from the type,
enforced by a constraint. `Article.publisherId` is what tells the three states of a
marketplace article apart: listed (no full purchase), owned (a full purchase, not yet
public) and published (public and free, with the magazine as publisher).

![Figure 6.2 – Class diagram, Sprint 5](../diagrams/fig-6-2-classes-sprint-5/fig-6-2-classes-sprint-5.png){width=100%}

**Sequence diagram — the purchase.** Figure 6.3 shows the three calls of a licence.
Each purchase stage opens one database transaction: it locks the article row and reads
its owner, refusing with 409 if another magazine already owns it — before any
arithmetic, so a refusal rolls back an empty unit of work — then locks the magazine's
credit balance, refuses with 402 when it is insufficient, debits the magazine, credits
the writer, and writes the purchase and its three ledger rows. The full purchase
charges only what the preview has not already paid. It leaves the article in the
magazine's library, owned and unpublished; publishing is a third call. Every request
carries an idempotency key, so a retried request cannot charge twice, and the row lock
stops two concurrent purchases from spending the same credits.

![Figure 6.3 – Sequence diagram: preview, purchase and publication](../diagrams/fig-6-3-sequence-two-stage-purchase/fig-6-3-sequence-two-stage-purchase.png){width=100%}

**Activity diagram — the eligibility gate.** Figure 6.4 shows eligibility: after each
aggregation the worker checks writers above both thresholds who are not yet eligible,
marks them eligible and writes an audit-log entry with the metric snapshot; an
administrator can grant eligibility directly, with the same audit trail. Comment likes
and reposts are deliberately not counted as reactions, so that other people's activity
cannot move a writer's threshold.

![Figure 6.4 – Activity diagram: the marketplace eligibility gate](../diagrams/fig-6-4-activity-eligibility-gate/fig-6-4-activity-eligibility-gate.png){width=100%}

**Sequence diagram — moderation.** Figure 6.5 shows the two sources of reports. At
publish time a classifier model reviews the article; a flag files a pending report with
no reporter but never blocks publication. Readers report articles, users or comments.
The administrator works the queue: dismiss the report, remove the article or ban the
author — a ban taking effect at the next authentication.

![Figure 6.5 – Sequence diagram: reporting and moderation](../diagrams/fig-6-5-sequence-moderation/fig-6-5-sequence-moderation.png){width=100%}

**Activity diagram — the article access decision.** Figure 6.6 shows the decision taken
server-side for every article body. The author and administrators always read. A
marketplace article is visible only to a magazine with an active subscription, and its
body only once that magazine has previewed or bought it — otherwise it receives the
title, excerpt and price with the content set to `null`. A premium public article
requires the premium plan or a subscribed magazine. A free public article is readable
by everyone, visitors included. The client is told the verdict; it never computes it.

![Figure 6.6 – Activity diagram: the article access decision](../diagrams/fig-6-6-activity-article-access/fig-6-6-activity-article-access.png){width=100%}

**State diagram — the article lifecycle.** Figure 6.7 shows the states an article goes
through and the only transitions the API permits. A draft is published as free,
premium or listed on the marketplace. A listed article can be withdrawn to public —
never the reverse, because an article the public has read has no exclusivity left to
sell — or deleted, as long as no magazine owns it. Its first full purchase makes it
*owned*, after which the writer can neither withdraw nor delete it; the magazine's
publication makes it *published by a magazine*, public and free.

![Figure 6.7 – State diagram: the article lifecycle](../diagrams/fig-6-8-state-article-lifecycle/fig-6-8-state-article-lifecycle.png){width=100%}

### 6.1.5 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/guest-06-article-premium-paywall.png`

**Figure 6.8 – A premium article behind the paywall**

> 📷 **Screenshot placeholder** — `figures/screens/reader-03-subscription-plans.png`

**Figure 6.9 – The plans: free and premium**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-06-subscription-credits.png`

**Figure 6.10 – A magazine's subscription and credits**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-01-marketplace.png`

**Figure 6.11 – The marketplace, with preview and purchase prices**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-02-listing-detail.png`

**Figure 6.12 – A listing before preview**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-03-purchase-confirm.png`

**Figure 6.13 – Confirming a preview unlock: price and balance after**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-04-library.png`

**Figure 6.14 – The magazine's library: unpublished and published**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-09-publish-from-library.png`

**Figure 6.15 – Publishing a purchased article under the magazine's masthead**

> 📷 **Screenshot placeholder** — `figures/screens/guest-10-licensed-article.png`

**Figure 6.16 – A licensed article naming both the writer and the magazine**

> 📷 **Screenshot placeholder** — `figures/screens/guest-08-magazine-profile.png`

**Figure 6.17 – A magazine's public profile and its published articles**

> 📷 **Screenshot placeholder** — `figures/screens/writer-09-earnings.png`

**Figure 6.18 – A writer's earnings, itemised by preview and purchase**

> 📷 **Screenshot placeholder** — `figures/screens/writer-11-sold-article.png`

**Figure 6.19 – A sold article, as its author sees it**

> 📷 **Screenshot placeholder** — `figures/screens/admin-01-eligibility-grant.png`

**Figure 6.20 – Administration: manual eligibility grant**

> 📷 **Screenshot placeholder** — `figures/screens/admin-02-user-table.png`

**Figure 6.21 – Administration: user management**

> 📷 **Screenshot placeholder** — `figures/screens/admin-03-report-queue.png`

**Figure 6.22 – Administration: the report queue**

## 6.2 Sprint 6 — Tests, demonstration and deployment

### 6.2.1 Sprint goal and backlog

**Goal:** prove the business rules with tests, make the product demonstrable on a
realistic corpus, and make it deployable with one command and an automated pipeline.

**Table 6.3 – Sprint 6 backlog**

<!-- INCLUDE:sprint-6 -->

### 6.2.2 Test strategy

Figure 6.23 shows the strategy. The base is the **unit and service tests** of the
backend, which run against a real PostgreSQL database rather than mocks, so that
constraints, transactions and row locks are exercised for real. Above them,
**integration tests** go through the API — authentication, publishing, purchasing —
and verify the ledger afterwards. At the top, **end-to-end tests** drive a real browser
over a seeded corpus. Two families protect the money: the **ledger invariant harness**,
whose tests are mostly negative — a fixture builds a coherent purchase, corrupts one
column and checks that the right invariant fires — and a **price sweep** that checks
every price from 1 to 300 credits, both stages and both splits, reconciling exactly.
The harness was validated by sabotage: removing a filter from the earnings query or a
stage from the debit list fails exactly the tests that should fail, an exercise that
found one coverage gap which was then closed.

![Figure 6.23 – Test strategy](../diagrams/fig-6-7-test-strategy/fig-6-7-test-strategy.png){width=100%}

**Table 6.4 – Test results**

| Suite | Scope | Result |
|---|---|---|
| Backend (Jest) | 51 suites — services, controllers, ledger, purchases, documents, voice, AI pipeline | **792 tests, all passing** |
| Ledger invariant harness | balance and ledger invariants, seed ledger | 34 tests, included above |
| Price sweep | prices 1–300, both stages, both splits | included above |
| End-to-end (Playwright) | 25 spec files over the seeded corpus | 183 tests |
| Static gates | `tsc --noEmit` and `eslint --max-warnings=0`, both repositories | pass |

### 6.2.3 Demonstration corpus

A seed command builds a believable dataset in seconds and can rebuild it from scratch:
its full preset creates **100 writers and 989 articles**, **50 magazines** (30 with a
live subscription), **150 readers**, 110 marketplace listings with real purchases and
ledger rows, and more than 15,000 likes, 2,700 reposts and 8,000 comments, with
generated cover art and avatars uploaded to object storage. A fixed cast of named
accounts makes every demonstration path reproducible, and a flag lowers the
eligibility thresholds so that the gate can be crossed live during a demonstration.
Every seeded date is relative to the seed's clock and can be bounded below, so the
corpus never predates the platform.

### 6.2.4 Deployment

The production stack is ready to run on a single server:

- **multi-stage images** for the API and worker (one image, two entry points) and for
  the Next.js server in standalone mode;
- a **production Compose file** in which only nginx is published, on ports 80 and 443,
  with TLS certificates from Let's Encrypt renewed through certbot;
- a **one-shot migration service** that must succeed before the API and worker start;
- **health and readiness endpoints** checked by Compose and by the deployment workflow;
- the **continuous-delivery workflow** of Chapter 3, from the quality gates to the
  image registry and the server.

The domain `inkwell-ai.me` is registered. The remaining step — provisioning the
server and pointing the domain at it — is listed with the perspectives.

## Conclusion

Release 3 delivered the marketplace end to end — subscriptions and credits, the
eligibility gate, the exclusive two-stage purchase, the magazine's own publication and
the writer's itemised earnings, all on a ledger whose invariants are tested after every
operation — together with moderation, a test suite of 792 backend tests, a
demonstration corpus and a production-ready deployment. The last release deepens the
social layer and reworks the assistant.

\newpage
