# Evaluation {#sec:ch7}

## Introduction {.unnumbered}

The release chapters showed what the platform does. This chapter measures how well it
does it. It evaluates the three components whose quality cannot be read off a screen
(the retrieval behind the assistant, the hybrid search and the moderation classifier),
then the performance and accessibility of the platform, and finally the delivery
itself: the velocity of the sprints against the plan, and a retrospective of each
release. Every measurement was taken on the workstation of @tbl:hardware, with the
full stack running in Docker, and every script and result is kept in the backend
repository (`eval/`) so that it can be repeated.

## Evaluation protocol {#sec:eval-protocol}

**Corpus.** Retrieval and search were evaluated on the demonstration corpus of
@sec:sprint6, restricted to six writers, one for each of the corpus's six subjects
(coastal craft, inference systems, cities, fermentation, orchestral music, analogue
photography): **56 published articles split into 1,202 embedded passages**. The
restriction is imposed by the embedding provider's free tier, which allows about a
thousand embeddings a day. It keeps the evaluation within one day's quota.

**Questions.** The evaluation set is a *known-item* set: 30 target passages chosen from
the corpus, five per subject, each asked twice: once with the passage's own
distinctive words (the *keyword* query) and once as a paraphrase that avoids them (the
*paraphrase* query). A passage or an article is relevant when it contains the target
passage. Three targets turned out to appear in none of their writer's embedded
articles and were dropped, leaving **27 targets and 54 queries**. Because the seeded
corpus reuses paragraphs across a writer's articles, a target appears on average in 5.9
articles. The queries were written before any result was seen.

**Metrics.** The standard measures of ranked retrieval were used
[@manning2008ir; @voorhees1999trec; @jarvelin2002ndcg]:

- **hit@k**: the share of queries for which at least one relevant item is among the
  first *k* results.
- **MRR** (mean reciprocal rank): the mean of 1/*r*, where *r* is the rank of the first
  relevant result (0 when there is none). A score of 1.00 means the first result
  is always relevant.
- **precision@5**: the share of relevant items among the passages returned.
- **recall@10**: the share of the relevant articles found in the first ten results.
- **nDCG@10**: a rank-weighted score that rewards relevant results placed higher.

The evaluation reuses the production code: queries are embedded by the platform's own
embedding service, and the rankings are the SQL of the retrieval and search services.
As a check, the production retrieval call was run on every query and returned the same
passages as the evaluation in 54 cases out of 54.

## Retrieval behind the assistant {#sec:eval-rag}

The assistant retrieves the five passages of the writer's own work closest to the
question, provided they score above a similarity floor (@sec:sprint4). Two questions
matter: does the right passage come back, and does the floor correctly return nothing
when the question is off-topic? The second was measured by asking every query to a
writer of *another* subject, for whom the correct answer is no passage at all.
@tbl:eval-rag gives the results for floors from 0.50 to 0.70.

| Floor | Hit@5, keyword | Hit@5, paraphrase | Hit@5, all | MRR | Precision@5 | Passages returned | Off-topic refused |
|:----:|:--------:|:--------:|:--------:|:------:|:--------:|:--------:|:--------:|
| 0.50 | 0.96 | 0.81 | 0.89 | 0.79 | 0.59 | 5.0 | 0% |
| 0.55 | 0.96 | 0.81 | 0.89 | 0.79 | 0.59 | 5.0 | 7% |
| **0.60** | **0.96** | **0.81** | **0.89** | **0.79** | **0.59** | **5.0** | **69%** |
| 0.65 | 0.96 | 0.81 | 0.89 | 0.79 | 0.60 | 4.9 | 98% |
| 0.70 | 0.93 | 0.74 | 0.83 | 0.75 | 0.64 | 4.1 | 100% |

: Retrieval of the writer's own passages, by similarity floor (54 queries) {#tbl:eval-rag}

At the floor used in production (0.60), a relevant passage is among the five returned
for 89% of the questions (96% when the question uses the passage's words, 81% when it
paraphrases them), and it is usually the first one (MRR 0.79). The floor is the reason
off-topic questions are refused: at 0.60, 69% of the questions asked to the wrong
writer retrieve nothing, where a floor of 0.50 would have fed five irrelevant passages
to the model every time.

The table also shows that 0.60 is not the best value. Raising the floor to **0.65**
keeps every hit and refuses 98% of off-topic questions. Only at 0.70 do relevant
passages start to be lost. The similarities explain why: the best relevant passage
scored between 0.66 and 0.84, and the best off-topic passage between 0.52 and 0.66, so
the two ranges barely touch at 0.65. The measurement therefore supports raising the
floor from 0.60 to 0.65, which is listed among the perspectives. Precision stays near
0.6 at every floor because a target appears in about six articles but only some of
them are among the five passages returned. It is not a sign of irrelevant results.

## Hybrid search {#sec:eval-search}

Search fuses a lexical ranking and a semantic ranking with reciprocal rank fusion
(@sec:sprint4). @tbl:eval-search compares the two rankings alone and fused, with the
production constant k = 60 and two other values, on the same 54 queries over the 56
articles.

| Ranking | Recall@10, keyword | Recall@10, paraphrase | MRR, keyword | MRR, paraphrase | nDCG@10, all |
|:---------------------|:--------:|:--------:|:--------:|:--------:|:--------:|
| Lexical only (`ts_rank`) | 0.95 | 0.06 | 0.93 | 0.07 | 0.50 |
| Semantic only (embeddings) | 1.00 | 1.00 | 0.94 | 0.90 | 0.94 |
| Hybrid, RRF k = 10 | 1.00 | 1.00 | 0.98 | 0.90 | 0.95 |
| **Hybrid, RRF k = 60** | **1.00** | **1.00** | **1.00** | **0.90** | **0.95** |
| Hybrid, RRF k = 100 | 1.00 | 1.00 | 1.00 | 0.90 | 0.95 |

: Lexical, semantic and hybrid search (54 queries, 56 articles) {#tbl:eval-search}

The table justifies the hybrid design. Keyword search is excellent when the searcher
uses the article's words (recall 0.95) and nearly useless when they do not (0.06): a
paraphrase defeats it. Semantic search finds every relevant article in both cases. The
fusion keeps the semantic recall and improves the ranking of keyword queries: with
k = 60 the first result is relevant for every keyword query (MRR 1.00 against 0.94 for
semantic search alone), because an article that matches both by words and by meaning
is ranked first. The value k = 60 recommended by the method's authors
[@cormack2009rrf] is confirmed: a smaller constant is slightly worse, a larger one
changes nothing.

The limits of this evaluation must be stated. The corpus is small and synthetic, built
by a seed that reuses paragraphs. The queries were written by the author, who knew the
corpus, and a known-item set rewards finding one passage, not judging the usefulness of
an answer. The results show that retrieval and fusion behave as designed on this
corpus, not how they would score on a public benchmark.

**Search latency.** On the same queries, the stages of a search took a median of
263 ms to embed the query, 7 ms for the lexical ranking and 9 ms for the semantic
ranking: about 0.3 s in total, dominated by the call to the embedding provider. One
behaviour was also measured that the design did not intend. When the provider's daily
quota is exhausted, each search spends about **6.3 s** retrying the embedding three
times before falling back to keyword search. The fallback works, since the results are still
returned, but the retries make it slow. Failing fast once the quota is known to be
exhausted, and caching the embeddings of frequent queries, are listed among the
perspectives.

## Moderation classifier {#sec:eval-moderation}

The classifier reviews every public article after publication and files a report when
it judges the content to violate one of six categories (@sec:sprint5). It was evaluated
on a labelled set of 33 texts written for the purpose: **13 violating texts** across the
six categories, and **20 safe texts**, of which twelve are *hard negatives* (war
reporting, crime news, an addiction memoir, thriller fiction, a suicide-prevention
message, instructions on overdose treatment) that a naive classifier would flag
because of their subject. The production service was called on each text three times.

| | Classified violating | Classified safe |
|:----------------------|:-:|:-:|
| **Violating (13)** | 13 (true positives) | 0 (false negatives) |
| **Safe (20)** | 1 (false positive) | 19 (true negatives) |

: Confusion matrix of the moderation classifier (identical in the three runs) {#tbl:eval-moderation}

The classifier reaches a **precision of 0.93** and a **recall of 1.00** (F1 0.96), and
named the right category for all 13 violating texts. The three runs gave identical
results. Its single false positive is instructive: instructions for killing a landed
fish quickly, classified as violence. It is a hard negative about hunting, the kind of text
the instruction to judge content rather than subject is meant to pass. The policy
chosen in @sec:sprint5 absorbs exactly this kind of error: a false positive files a
report that an administrator dismisses, and never blocks the article.

The median classification took 2.2 s, which is acceptable because it runs after the
publication has been answered. The evaluation also had a second outcome. Its first run
showed that the model initially configured for the classifier had been withdrawn by
the provider, so that every call failed and the service, which fails open by design,
passed every article without a word in the logs. The classifier was moved to
`gpt-oss-20b`, with an output budget large enough for a reasoning model, and the
results above are those of the corrected service. The lesson is that a fail-open
component needs a liveness check of its own. The daily model check of the worker now
exercises the classifier at the budget it is called with.

## Performance and accessibility {#sec:eval-perf}

**API latency.** @tbl:eval-latency gives the response time of the main read routes,
measured inside the Compose network with ten concurrent clients and 300 requests per
route, each client presenting its own address so that the per-address rate limit
applied as it would to distinct readers.

| Route | Median | 95th percentile | Throughput |
|:-------------------------------------------|:-:|:-:|:-:|
| Public feed (`GET /articles`, 20 cards) | 34 ms | 41 ms | 285 req/s |
| Article page (`GET /articles/:slug`) | 15 ms | 19 ms | 652 req/s |
| Writer evaluation (`GET /writers/:username/evaluation`) | 16 ms | 20 ms | 620 req/s |
| Writer dashboard (`GET /me/analytics`) | 12 ms | 17 ms | 774 req/s |
| Search (stages, one query at a time) | ≈ 0.3 s | n/a | bound by the provider quota |

: Latency of the main API routes under concurrent load {#tbl:eval-latency}

Every route that reads the database answers in under 50 ms at the 95th percentile on
a laptop, and the two routes backed by the rollups (the evaluation report and the
dashboard) are among the fastest, which is the effect NFR-15 was written for. Search
is the exception, for the reason given in @sec:eval-search: its cost is the call to the
embedding provider, not the database. The rate limit of NFR-05 was verified on the
same occasion: sixty requests from one address within a minute were served, and the
sixty-first was answered 429.

**Lighthouse and accessibility.** NFR-37 asks for a Lighthouse score above 90 and no
critical accessibility violation on article pages [@lighthousedocs]. A production build
of the frontend was audited behind nginx, with Lighthouse's mobile and desktop presets
(median of three runs) and with axe-core on the WCAG 2.x A and AA rules at the two
designed widths [@axecore; @wcag22]. @tbl:eval-lighthouse gives the results.

| Page | Performance (mobile / desktop) | Accessibility | SEO | Critical axe violations | Serious axe violations |
|:------------------------------|:-:|:-:|:-:|:-:|:-:|
| Article, free | 63 / 96 | 92 | 100 | 0 | 6 |
| Article, premium (paywalled) | 74 / 98 | 91 | 100 | 0 | 5 |
| Home feed | 71 / 98 | 91 | 100 | 0 | 19 |
| Search results | 75 / 93 | 94 | 63 | 0 | 4 |

: Lighthouse scores and axe-core violations of the public pages {#tbl:eval-lighthouse}

NFR-37 is **partly met**. No page has a critical accessibility violation, at either
width. Every page scores above 90 for accessibility, and between 93 and 98 for
performance on desktop. On the mobile preset, which simulates a slow device and
network, the pages score 63 to 75: their largest element is painted after about six
seconds, because the page loads its fonts, cover image and interactive controls before
the text settles. The serious violations are of two kinds only: text whose contrast
with its background is too low, and icon-only links without an accessible name (the
reaction and share buttons of the cards, which explains the higher count on the feed).
Both are fixes of the design tokens and of a few components, and they are listed with
the limitations.

The search page's SEO score of 63 is intended: result pages are marked `noindex`, so
that search engines index the articles rather than lists of them.

## Test coverage

@tbl:tests in @sec:sprint6 gave the test suites. Their coverage was interpreted there.
In short, the 796 backend tests execute 48.5% of the backend's lines, concentrated on
the rules that move money or remove content (moderation 92%, purchases 77%), while the
analytics aggregation is verified by the measurements above rather than by unit
tests.

## Delivery: velocity and retrospective {#sec:velocity}

**Definition of done.** A story counted as delivered when its code had been reviewed
against the specification, the type check and the linter passed with no warning, the
backend tests passed in the container, the feature had been demonstrated in a browser,
and the specification had been updated to match what was built.

**Velocity.** @tbl:velocity compares the points committed in each sprint with the
points delivered under that definition.

| Sprint | Committed | Delivered | Gap |
|:--|:-:|:-:|:-------------------------------------|
| Sprint 1 | {{S1PTS}} | {{S1PTS}} |  |
| Sprint 2 | {{S2PTS}} | {{S2PTS}} |  |
| Sprint 3 | {{S3PTS}} | {{S3PTS}} |  |
| Sprint 4 | {{S4PTS}} | {{S4PTS}} |  |
| Sprint 5 | {{S5PTS}} | {{S5PTS}} |  |
| Sprint 6 | {{S6PTS}} | 12 | US-55 (8 points): configuration ready, server not provisioned |
| Sprint 7 | {{S7PTS}} | {{S7PTS}} |  |
| Sprint 8 | {{S8PTS}} | {{S8PTS}} |  |
| Sprint 9 | {{S9PTS}} | {{S9PTS}} |  |
| **Total** | **{{POINTS}}** | **342** | 98% of the committed points |

: Committed and delivered points per sprint {#tbl:velocity}

The plan was followed sprint for sprint: 98% of the points were delivered, and the only
gap is the public hosting of US-55. The table shows, however, that the loads were
uneven, from 16 to 85 points for sprints of the same length. That spread is a
consequence of estimating alone: without a team to challenge a figure, the marketplace
of Sprint 5 was planned as one block because its stories share one ledger, and the
light sprints of Release 4 reflect stories that reused existing pipelines and a release
that ran alongside the writing of this report. A velocity averaged over the project
(about 38 points per sprint) would have been the better planning figure, and would have
split Sprint 5 in two.

**Retrospective.** @tbl:retro summarises what each release taught.

| Release | What worked | What to improve | Action taken |
|:------|:--------------------------------|:--------------------------------|:--------------------------------|
| R1 | The ledger checks and the one-command stack existed before any feature that needed them | The editor waited six weeks for the design track | Later releases built on the design system and needed no separate design track |
| R2 | Rollups kept dashboards fast as events accumulated | The embedding provider's quota limits backfills and search under load | Embed one writer at a time. A query-embedding cache listed as a perspective |
| R3 | Every money rule is tested, including tests designed to fail under sabotage | Sprint 5 was overloaded. The aggregation has no unit tests. Hosting was not done | Plan by measured velocity. Aggregation tests listed as the first perspective |
| R4 | Voice and documents reused the AI pipeline, so they were small | A provider withdrew a model and the fail-open classifier hid it | A daily check exercises every model as it is called |

: Retrospective by release {#tbl:retro}

The retrospective shows a pattern. The rules written down early (the ledger
invariants, the access decision, the definition of done) held for the whole project.
What went wrong came from outside the code: the quotas and model changes of the AI
providers, and the time an individual project leaves for hosting. Those are the points
the perspectives address.

## Conclusion {.unnumbered}

The evaluation confirmed the main design decisions with measurements: retrieval finds a
relevant passage for 89% of questions and its floor refuses most off-topic ones.
Hybrid search keeps all relevant articles even when the searcher's words differ from
the author's. The moderation classifier reaches a precision of 0.93 and a recall of
1.00. The API answers in tens of milliseconds, and 98% of the planned points were
delivered. It also found what remains to be done: a higher similarity floor, a faster
fallback when the embedding quota is exhausted, better mobile performance and contrast,
tests for the aggregation, and the public hosting of the platform.
