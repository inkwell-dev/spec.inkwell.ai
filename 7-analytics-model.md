# 07 - Analytics Model

## 1. Overview

The analytics system serves two distinct audiences with two distinct surfaces over a single underlying event pipeline:

- **Writer-facing analytics** — self-improvement metrics (how is my article performing?)
- **Magazine-facing analytics** — buyer decision support (is this writer worth licensing from?)

This dual-purpose design is what gives analytics **economic gravity** on the platform: every metric collected has a direct downstream consequence in a marketplace transaction.

---

## 2. Analytics Objectives

The analytics system must:

- Track how users interact with articles at granular level (per-paragraph)
- Provide writers with self-improvement insights
- Provide magazines with objective signals to evaluate writer profiles before licensing
- Power AI-driven feedback for both writers (improve content) and magazines (Portfolio Insights)
- Maintain reader privacy while exposing aggregate trends

---

## 3. Event-Based Tracking Model

The system uses an **event-driven architecture**. Each user interaction generates an event that is stored raw, then processed by background aggregation jobs into metrics tables consumed by dashboards.

```
User Interaction
    ↓
Frontend captures event
    ↓
Batched POST → /analytics/events (backend)
    ↓
Stored in analytics_events table (raw)
    ↓
BullMQ worker aggregates (every 15 min)
    ↓
Writes to writer_audience_metrics
            writer_content_metrics
            writer_quality_metrics
    ↓
Dashboards read aggregated tables (fast)
```

---

## 4. Event Types

### 4.1 View Event
Triggered on article load.

Captured data:
- `article_id`
- `viewer_user_id` (nullable for guests)
- `viewer_country` (from IP, optional)
- `viewer_device` (mobile / desktop / tablet)
- `referrer` (nullable)
- `timestamp`

### 4.2 Scroll Event
Triggered as the user scrolls through paragraphs (`IntersectionObserver`).

Captured data:
- `article_id`
- `viewer_user_id` (nullable)
- `paragraph_index`
- `scroll_percentage`
- `timestamp`

### 4.3 Time-on-Page Event
Captured at unload via `visibilitychange` + `beforeunload`.

Captured data:
- `article_id`
- `viewer_user_id` (nullable)
- `engaged_seconds` (only time when tab was visible)
- `completed` (boolean — did they reach the end?)
- `timestamp`

### 4.4 Social Events
- `like` — article_id, user_id
- `comment` — article_id, user_id, comment_id
- `repost` — article_id, user_id
- `follow` — follower_id, following_id

### 4.5 Transaction Events (Marketplace)
- `article_published_marketplace` — article_id, price (writer publishes to marketplace)
- `article_preview_unlocked` — article_id, magazine_id, preview_price, purchase_id
- `article_purchased` — article_id, magazine_id, total_price, purchase_id
- Stored in a separate `transactions` table (not in `analytics_events`)
- These events also feed the **writer eligibility computation** (see section 9.3)

---

## 5. Data Storage Strategy

### 5.1 Raw Events Table

`analytics_events`:
- Full append-only history
- Used for ad-hoc analysis and re-aggregation
- Indexed on `(article_id, created_at)` and `(viewer_user_id, created_at)`
- Older events can be archived after aggregation (>90 days)

### 5.2 Aggregated Tables (Per-Writer)

Three writer-level rollup tables, refreshed by background jobs every 15 minutes:

- `writer_audience_metrics` — who is reading this writer
- `writer_content_metrics` — what they publish, when, how often
- `writer_quality_metrics` — engagement quality signals

### 5.3 Per-Article Aggregation

`article_metrics`:
- Total views
- Total likes / comments / reposts
- Average read time
- Completion rate
- Engagement rate
- Paragraph-level drop-off (JSON array)
- Updated by the same aggregation job

---

## 6. Writer-Facing Analytics (Self-Improvement Surface)

Writers see their own metrics on the **Writer Dashboard** at `/dashboard`.

### 6.1 Article-Level View
- Total views
- Average read time (minutes)
- Scroll depth heatmap (per paragraph)
- Engagement rate (% of viewers who scroll past 75%)
- Completion rate (% who reach the end)
- Likes / comments / reposts
- Drop-off points (paragraphs where ≥30% of viewers leave)

### 6.2 Profile-Level View
- Total lifetime views across all articles
- Top performing articles
- Follower count growth chart
- AI feedback summary ("Your intros could be stronger", etc.)

### 6.3 Earnings View (writers only)
- Total earnings (lifetime — preview payouts + purchase payouts combined)
- Per-article revenue (preview payouts + purchase payouts per article)
- Recent transactions (previews and full purchases separately itemized)
- Earnings balance + simulated withdraw
- **Eligibility progress** — if writer is not yet eligible: "X / 5,000 readers · Y / 1,000 reactions to unlock marketplace"

---

## 7. Magazine-Facing Analytics (Buyer Decision Support)

Magazines see writer evaluation dashboards on each writer's profile. **This is the system's defining differentiator.**

**Access requirement**: active magazine subscription. Unauthenticated visitors and non-subscribed magazine accounts cannot view writer evaluation dashboards or Portfolio Insights.

Magazines view: `/u/[writer-username]?as=magazine` → renders the evaluation view rather than the standard public profile.

### 7.1 Audience Analytics

Answers: *"Who reads this writer?"*

- **Total unique readers** (lifetime, last 30 days, last 7 days)
- **Returning vs new reader ratio** — % of readers who have read 2+ articles by this writer
- **Geographic distribution** — pie chart of top 5 countries
- **Device split** — mobile / desktop / tablet
- **Average engaged minutes per reader** — across all of the writer's articles

### 7.2 Content Analytics

Answers: *"What does this writer publish?"*

- **Topic distribution** — derived from tags + AI inference over content
- **Posting frequency** — articles per month, last 12 months as a sparkline
- **Posting consistency** — coefficient of variation in inter-publication intervals (lower = more consistent)
- **Average article length** — word count
- **Tags / categories breakdown** — top 10 tags

### 7.3 Quality Signals

Answers: *"How good is this writer's content?"*

- **Engagement rate** — % of viewers reading past 75% scroll
- **Completion rate** — % of viewers reaching the end
- **Repost rate** — reposts / total views
- **Comment depth** — average replies per article
- **Retention curve** — chart showing % of readers retained at each scroll quartile

### 7.4 AI Portfolio Insights

Generated by RAG over the writer's published corpus. See [`5-ai-design.md`](./5-ai-design.md) for the prompt and pipeline design.

Magazine sees a rendered report:
- **Voice summary** — 2-3 sentences describing tone
- **Topic expertise** — bullet list of domains
- **Style consistency score** — 0–100 with brief justification
- **Suggested use-cases** — what kind of magazine would fit
- **Notable strengths and gaps**

Cached per writer for 24 hours or invalidated on new publication.

---

## 8. Paragraph-Level Analytics

Each paragraph (TipTap node) is treated as a unit of analysis.

For each `(article_id, paragraph_index)`:
- Number of views
- Average time spent
- Drop-off rate (% who stopped at or before this paragraph)

Used by:
- Writer dashboard (drop-off detection, AI feedback on weak sections)
- AI editor ("the AI knows which paragraphs your readers skip")

---

## 9. Aggregation Strategy

### 9.0 Event Capture Timing

Analytics event capture (the `/analytics/events` endpoint + frontend instrumentation) should be implemented in **Phase 2** alongside the editor — not deferred to Phase 3. This ensures weeks of real engagement data accumulate before the September defense, making demo dashboards show genuine usage patterns rather than synthetic data.

The aggregation workers and dashboard UI remain in Phase 3; Phase 2 only adds the raw event ingestion pipeline.

### 9.1 Frequency

- **Real-time counters** (views, likes) — increment on event capture
- **Per-article aggregations** — every 5 minutes (BullMQ scheduled job)
- **Per-writer rollups** (audience, content, quality) — every 15 minutes
- **AI Portfolio Insights** — on-demand (first request) with 24-hour cache

### 9.2 Implementation

- BullMQ worker container (`worker` service in docker-compose) runs:
  - `aggregate-article-metrics` job
  - `aggregate-writer-audience` job
  - `aggregate-writer-content` job
  - `aggregate-writer-quality` job
- Each job is idempotent and resumable
- Aggregation reads incrementally (only events since `last_aggregated_at`)

### 9.3 Writer Eligibility Computation

A writer becomes marketplace-eligible when their **lifetime public article metrics** cross both thresholds simultaneously:
- ≥ 5,000 **unique readers** (distinct `viewer_user_id` across all published public articles, guests excluded)
- ≥ 1,000 **reactions** (likes + comments, counted from the `likes` and `comments` tables)

**Computation trigger**: after each aggregation run, the worker queries writers whose current metrics are above threshold but whose `is_marketplace_eligible` is still `FALSE`. For each match:
1. Sets `users.is_marketplace_eligible = TRUE`
2. Sets `users.marketplace_eligible_at = NOW()`
3. Sets `users.marketplace_eligible_source = 'threshold'`
4. Inserts a row into `writer_eligibility_audit_log` with metric snapshots

**Admin grant path**: Admin sets eligibility directly via the admin panel → same fields updated + `marketplace_eligible_source = 'admin_grant'` + `granted_by = admin_user_id` in audit log.

**Immutability**: once granted, eligibility is never automatically revoked (lifetime threshold, not rolling window). Manual revocation is possible only through an explicit admin action (not modeled in MVP).

### 9.4 Demo Threshold Configuration

The 5,000-reader / 1,000-reaction thresholds are impossible to reach organically during a PFE demo. To ensure the data-driven differentiator can be demonstrated live:

- A `DEMO_MODE=true` environment flag lowers thresholds to configurable values (e.g., 5 readers + 2 reactions)
- A seed script pre-populates demo writers, articles, and analytics events
- This allows a writer to *actually cross the eligibility line* during the defense, rather than relying solely on admin-grant bypass

---

## 10. Privacy & Compliance

- `viewer_user_id` is nullable for guests
- Geographic data is country-level only (no city/IP stored long-term)
- Magazines see **aggregate** data only — never individual reader identities
- Writers can request deletion of their own analytics (GDPR-compatible)
- Readers can opt out of analytics tracking (cookie consent in Phase 6)

---

## 11. Performance Considerations

- Events batched on the frontend (sent in bursts of 10 or every 5 seconds)
- Indexes on `(article_id, created_at)` and `(viewer_user_id, created_at)`
- Aggregated tables denormalized for fast dashboard queries (single-table reads)
- Old raw events (>90 days) can be archived to a cold storage table

---

## 12. AI Feedback Integration

### 12.1 Writer-Facing AI Feedback
Based on analytics:
- "Readers drop off at paragraph 3 — consider tightening your intro"
- "Your articles longer than 1500 words have 40% lower completion"
- "Reposts spike on articles tagged 'tutorials' — lean into that"

### 12.2 Magazine-Facing AI Feedback
Based on writer's analytics + corpus:
- Portfolio Insights (see section 7.4)
- "This writer's audience overlaps with your typical readership"
- "Recommended licensing budget: X credits/month based on output cadence"

---

## 13. Future Enhancements (Post-MVP)

- Real-time analytics dashboard with WebSockets
- Cohort analysis (readers grouped by signup date)
- A/B testing infrastructure for article titles
- Heatmap visualization of attention per paragraph
- Audience overlap analysis between writers (for magazines)
- Predictive license value (ML model on engagement features)

---

## Summary

The analytics system is no longer a vanity dashboard — it is the **decision support layer** that drives the licensing marketplace. Every event captured serves both a writer's self-improvement loop and a magazine's purchase decision, creating a tight feedback loop between content quality and economic outcomes.
