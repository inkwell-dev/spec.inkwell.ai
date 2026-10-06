# Chapter 5 — Release 2: social interactions, analytics and AI

## Introduction

The second release turns a publishing tool into a platform. Sprint 3 adds the social
layer — likes, threaded comments, reposts, follows, reports — with live notifications,
and aggregates the reading events captured since Release 1 into the metrics behind the
writer's dashboards and the magazine's evaluation report. Sprint 4 adds the platform's
retrieval layer: published articles are embedded, the assistant answers from the
writer's own passages and voice profile, magazines can request AI portfolio insights,
and search combines keywords with meaning.

## 5.1 Sprint 3 — Social interactions, notifications and analytics

### 5.1.1 Sprint goal and backlog

**Goal:** readers interact with articles and writers, and the author is told live;
writers see how their articles are read; subscribed magazines browse eligible writers
and read an evaluation report built on audience, content and quality metrics.

**Table 5.1 – Sprint 3 backlog**

<!-- INCLUDE:sprint-3 -->

### 5.1.2 Analysis

Figure 5.1 gives the use cases of Sprint 3. Interacting with an article specialises
into liking, commenting, replying, reposting, following and reporting, and includes
notifying the recipient. On a marketplace listing, liking, commenting and reposting
are refused while saving stays available, because a listing is a private commercial
offer rather than a publication. Viewing article analytics and reading a writer
evaluation both include the aggregation of raw events into metrics — a scheduled job
rather than a user action, drawn because no metric exists without it.

![Figure 5.1 – Use case diagram, Sprint 3](../diagrams/fig-5-1-use-case-sprint-3/fig-5-1-use-case-sprint-3.png){width=100%}

### 5.1.3 Design

**Class diagram.** Figure 5.2 adds likes, comments, reposts, follows and notifications,
and the four rollup tables: `ArticleMetrics` per article, and `WriterAudienceMetrics`,
`WriterContentMetrics` and `WriterQualityMetrics` per writer.

![Figure 5.2 – Class diagram, Sprint 3](../diagrams/fig-5-2-classes-sprint-3/fig-5-2-classes-sprint-3.png){width=100%}

**Sequence diagram — from reading events to metrics.** Figure 5.3 follows a reading
event to the dashboard. The browser batches events; the API takes the reader's
identity from the access token when one is sent — never from the request body — and
attaches the country and device server-side before appending the event. Every five
minutes the worker reads only the events since the last run and upserts the
per-article metrics (views, unique views, reading time, completion and engagement);
just after, it computes the three per-writer rollups and rechecks marketplace
eligibility. Dashboards read the rollups, never the raw events, so they stay fast as
the event log grows.

![Figure 5.3 – Sequence diagram: analytics aggregation](../diagrams/fig-5-3-sequence-analytics-aggregation/fig-5-3-sequence-analytics-aggregation.png){width=100%}

**Table 5.2 – Main metrics of the evaluation report**

| Panel | Metric | Definition |
|---|---|---|
| Audience | Unique readers | distinct identified readers across the writer's articles |
| Audience | Returning-reader rate | share of readers who read two or more of the writer's articles |
| Content | Posting frequency and consistency | articles per week; variation of the intervals between publications |
| Content | Topics | distribution of the writer's articles over tags |
| Quality | Engagement rate | share of views that read past 75% of the article |
| Quality | Completion rate | share of views that reach the end |
| Quality | Repost rate, comment depth | reposts per view; replies per comment |
| Quality | Retention curve | share of readers still reading at each quarter of the article |

**Sequence diagram — live notifications.** Figure 5.4 shows how a notification reaches
its recipient. The client keeps a server-sent-events stream open; when a reader likes
an article, the like and the notification row are written first, and only after the
commit is the event pushed to the recipient's open streams. If the connection drops,
the client reconnects with the identifier of the last event received and the server
replays what was missed. Delivery is best-effort; the database is the record.

![Figure 5.4 – Sequence diagram: live notification delivery](../diagrams/fig-5-9-sequence-notification-delivery/fig-5-9-sequence-notification-delivery.png){width=100%}

### 5.1.4 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/reader-01-feed.png`

**Figure 5.5 – The feed of a signed-in reader, with live card controls**

> 📷 **Screenshot placeholder** — `figures/screens/writer-12-notifications.png`

**Figure 5.6 – Notifications, filtered and grouped by day**

> 📷 **Screenshot placeholder** — `figures/screens/writer-01-dashboard.png`

**Figure 5.7 – The writer's dashboard**

> 📷 **Screenshot placeholder** — `figures/screens/writer-13-my-articles.png`

**Figure 5.8 – "My articles": every article, sortable by performance**

> 📷 **Screenshot placeholder** — `figures/screens/writer-10-dashboard-analytics.png`

**Figure 5.9 – The writer's analytics: views over the last 30 days**

> 📷 **Screenshot placeholder** — `figures/screens/guest-07-writer-profile.png`

**Figure 5.10 – A writer's public profile**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-07-discover-writers.png`

**Figure 5.11 – A magazine browsing eligible writers**

## 5.2 Sprint 4 — Retrieval, portfolio insights and hybrid search

### 5.2.1 Sprint goal and backlog

**Goal:** published articles become a retrievable corpus; the assistant answers from
the writer's own passages and shows them; each writer gets an automatically extracted
voice profile; magazines request AI portfolio insights; search finds articles by
meaning as well as by keyword.

**Table 5.3 – Sprint 4 backlog**

<!-- INCLUDE:sprint-4 -->

### 5.2.2 Analysis

Figure 5.12 gives the use cases of Sprint 4. Searching specialises into searching by
keyword and by meaning and includes merging the two result sets; using the assistant
includes retrieving passages from the writer's own corpus and showing the sources
used; publishing includes embedding the article, extracting the writer's voice profile
and invalidating the insights cache; reading a writer evaluation is extended by
generating portfolio insights.

![Figure 5.12 – Use case diagram, Sprint 4](../diagrams/fig-5-5-use-case-sprint-4/fig-5-5-use-case-sprint-4.png){width=100%}

### 5.2.3 Design

**Class diagram.** Figure 5.13 adds the retrieval corpus — `ArticleChunk`, a passage of
a published article with its 1,536-dimension embedding — the `WriterMemory` (tone,
style examples, vocabulary, topics), the cached `PortfolioInsight` and the
`AiInteraction` log. Chunks exist only for published articles.

![Figure 5.13 – Class diagram, Sprint 4](../diagrams/fig-5-6-classes-sprint-4/fig-5-6-classes-sprint-4.png){width=100%}

**Sequence diagram — what publishing sets in motion.** Figure 5.14 shows the background
pipeline a publication starts. The API writes the article and enqueues an embedding
job. The worker deletes the article's previous chunks, splits it into passages of 120
to 1,200 characters — each prefixed with its nearest heading, so that a short paragraph
embeds near its subject — embeds them, stores the vectors and drops the writer's
cached insights. It then chains the extraction of the writer's voice profile: the ten
most recent articles are sent to the model, which returns tone, style, vocabulary and
topics as a schema-validated object.

![Figure 5.14 – Sequence diagram: the publishing pipeline](../diagrams/fig-5-8-sequence-publish-pipeline/fig-5-8-sequence-publish-pipeline.png){width=100%}

**Sequence diagram — a chat turn grounded in the writer's corpus.** Figure 5.15 shows
retrieval-augmented generation as delivered in this sprint. The question is embedded;
the five passages of the writer's own work closest to it by cosine similarity are
retrieved, provided they score at least 0.60; the voice profile is read; the prompt is
assembled from role, memory, passages and question, bounded at about 2,000 tokens; the
answer is streamed, and the passages used are shown as sources. The similarity floor
was measured rather than chosen: with this embedding model, on-topic passages scored
0.63–0.73 and off-topic ones 0.48–0.58, so a floor of 0.60 lets retrieval return
nothing rather than five irrelevant passages.

![Figure 5.15 – Sequence diagram: AI chat with retrieval](../diagrams/fig-5-4-sequence-ai-chat-rag/fig-5-4-sequence-ai-chat-rag.png){width=100%}

**Sequence diagram — hybrid search.** Figure 5.16 shows search. The query is ranked
lexically with `ts_rank` over the article's weighted search vector, and semantically by
cosine distance, keeping the best chunk per article. Because the two scores are on
unrelated scales, the rankings are fused by position with reciprocal rank fusion —
each article scores Σ 1/(60 + rank) — so an article that never uses the searcher's
words can still be found by meaning.

![Figure 5.16 – Sequence diagram: hybrid search with reciprocal rank fusion](../diagrams/fig-5-7-sequence-hybrid-search/fig-5-7-sequence-hybrid-search.png){width=100%}

### 5.2.4 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/guest-09-search-results.png`

**Figure 5.17 – Search results**

> 📷 **Screenshot placeholder** — `figures/screens/magazine-08-writer-evaluation.png`

**Figure 5.18 – A writer evaluation report with portfolio insights**

## Conclusion

Release 2 made Inkwell.ai social and measurable: interactions with live notifications,
reading events aggregated into per-article and per-writer metrics, an evaluation
report for magazines, and a retrieval layer that grounds the assistant in the writer's
own work, produces portfolio insights and powers hybrid search. Release 3 builds the
marketplace those signals were designed for.

\newpage
