# 09 — Implementation Guide

> Pre-implementation specification for every under-defined subsystem.
> Generated 2026-05-29 from a gap analysis of specs 0–8.
> This document does NOT revisit architecture decisions. It fills the "how" gaps that remain after the "what" is settled.

---

## 1. TipTap JSON Processing

### 1.1 Why this needs a spec

Three critical subsystems depend on extracting plain text from TipTap's ProseMirror JSON: `content_search` (tsvector), RAG chunking, and word count / read time. None of the existing specs define how this extraction works.

### 1.2 TipTap JSON structure

TipTap stores content as a nested ProseMirror document:

```json
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Hello " },
        { "type": "text", "marks": [{ "type": "bold" }], "text": "world" }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "Section Title" }
      ]
    },
    {
      "type": "image",
      "attrs": { "src": "https://...", "alt": "photo" }
    },
    {
      "type": "codeBlock",
      "content": [
        { "type": "text", "text": "const x = 1;" }
      ]
    }
  ]
}
```

### 1.3 Shared utility: `tiptap-utils.ts`

Located in the backend at `src/common/utils/tiptap-utils.ts`. Used by articles module, RAG pipeline, and analytics.

```typescript
interface TipTapNode {
  type: string;
  content?: TipTapNode[];
  text?: string;
  attrs?: Record<string, unknown>;
  marks?: { type: string }[];
}

// Recursively extract all text from a TipTap document
function extractFullText(doc: TipTapNode): string {
  if (doc.text) return doc.text;
  if (!doc.content) return '';
  return doc.content.map(extractFullText).join(
    doc.type === 'doc' || doc.type === 'paragraph' || doc.type === 'heading'
      ? '\n'
      : ''
  );
}

// Extract one string per paragraph/heading node (for RAG chunking)
function extractParagraphs(doc: TipTapNode): string[] {
  if (!doc.content) return [];
  return doc.content
    .filter(node => node.type === 'paragraph' || node.type === 'heading')
    .map(node => extractFullText(node).trim())
    .filter(text => text.length > 0);
}

// Word count from full text
function countWords(doc: TipTapNode): number {
  return extractFullText(doc).split(/\s+/).filter(Boolean).length;
}

// Estimated read time (250 wpm average)
function estimateReadTime(doc: TipTapNode): number {
  return Math.max(1, Math.ceil(countWords(doc) / 250));
}
```

### 1.4 tsvector population

**Strategy:** application-layer, not a database trigger.

On every article `INSERT` or `UPDATE` that changes `content`:

```typescript
const plainText = extractFullText(content);
const searchText = `${title} ${excerpt ?? ''} ${plainText}`;

await db.update(articles)
  .set({
    content_search: sql`to_tsvector('english', ${searchText})`,
    word_count: countWords(content),
    read_time: estimateReadTime(content),
  })
  .where(eq(articles.id, articleId));
```

This runs synchronously inside the article save/publish endpoint — not as a background job. The tsvector must be current for search to work.

### 1.5 RAG chunking rules

When the `embed-article` BullMQ job runs:

1. Call `extractParagraphs(article.content)` to get a `string[]`
2. Filter out paragraphs shorter than 20 characters (noise: blank lines, image captions)
3. If a paragraph exceeds 1000 characters, split at the nearest sentence boundary (`.` followed by space)
4. Each resulting string becomes one chunk with `chunk_index` = its position in the array
5. Delete all existing chunks for this article (`DELETE FROM article_chunks WHERE article_id = $1`)
6. Embed each chunk text via the embedding provider
7. Insert new chunk rows
8. Invalidate `portfolio_insights` cache for this writer (`DELETE FROM portfolio_insights WHERE writer_id = $author_id`)

Minimum corpus for RAG to function: 3 published articles with at least 5 paragraphs each.

---

## 2. Authentication & Token Management

### 2.1 Password hashing

Use `bcrypt` with cost factor 12:

```typescript
import * as bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
const isValid = await bcrypt.compare(password, hash);
```

### 2.2 JWT structure

**Access token** (15 min):
```json
{
  "sub": "uuid",
  "accountType": "personal" | "magazine",
  "role": "reader" | "writer" | "admin" | null,
  "plan": "free" | "premium" | null,
  "iat": 1234567890,
  "exp": 1234568790
}
```

**Refresh token** (7 days): opaque UUID stored in Redis. NOT a JWT — this allows revocation.

### 2.3 Refresh token storage (Redis)

```
Key:    refresh:{userId}:{tokenId}
Value:  { userAgent, createdAt }
TTL:    7 days (604800 seconds)
```

**Flows:**
- **Login:** generate UUID `tokenId`, store in Redis, return to client as `HttpOnly` cookie
- **Refresh:** client sends refresh token → lookup `refresh:{userId}:{tokenId}` → if exists, issue new access token + rotate refresh token (delete old, create new)
- **Logout:** delete `refresh:{userId}:{tokenId}`
- **Password change:** delete all keys matching `refresh:{userId}:*`
- **Soft delete / ban:** delete all keys matching `refresh:{userId}:*`

### 2.4 AI token quota

| Plan | Daily AI tokens | Reset time |
|------|----------------|------------|
| Free | 0 (no AI access) | — |
| Premium | 50,000 | Daily at midnight UTC |
| Magazine | 20,000 | Daily at midnight UTC |

One "AI token" = one LLM token consumed (input + output combined). The `ai_tokens_remaining` field on the `users` table is decremented after each AI response by the actual `tokens_used` value reported by the Vercel AI SDK.

The `reset-ai-tokens` BullMQ cron runs daily at 00:00 UTC:
```sql
UPDATE users
SET ai_tokens_remaining = CASE
  WHEN plan = 'premium' THEN 50000
  WHEN account_type = 'magazine' THEN 20000
  ELSE 0
END,
ai_tokens_reset_at = NOW()
WHERE deleted_at IS NULL;
```

---

## 3. MinIO Upload Flow

### 3.1 Network topology

MinIO runs inside the Docker network at `minio:9000`. Browsers cannot reach it directly. Two options:

**Option A (recommended): Proxy through Nginx**

Add to Nginx config:
```nginx
location /storage/ {
    proxy_pass http://minio:9000/;
    proxy_set_header Host $http_host;
    client_max_body_size 10M;
}
```

Presigned URLs generated by the backend point to `/storage/...` which Nginx proxies to MinIO internally.

**Option B: Upload through backend**

`POST /api/uploads` receives the file, streams it to MinIO server-side. Simpler but adds backend as a bottleneck.

### 3.2 Upload flow (Option A)

1. Frontend requests presigned URL: `POST /api/uploads/presign` with `{ filename, contentType }`
2. Backend generates presigned PUT URL using MinIO SDK:
   ```typescript
   const url = await minioClient.presignedPutObject(
     'inkwell-images',
     `${userId}/${uuid()}-${filename}`,
     3600 // 1 hour expiry
   );
   // Replace internal minio:9000 with the public /storage/ path
   return url.replace('http://minio:9000', '/storage');
   ```
3. Frontend uploads directly: `PUT /storage/inkwell-images/{key}` with the file body
4. Frontend receives the final URL: `/storage/inkwell-images/{key}` — this is what gets stored in the article content or as `thumbnail_url`

### 3.3 Buckets

| Bucket | Access | Contents |
|--------|--------|----------|
| `inkwell-images` | Public read, authenticated write | Article thumbnails, inline images, avatars, magazine logos |

Create bucket on first deploy:
```bash
mc alias set local http://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
mc mb local/inkwell-images
mc anonymous set download local/inkwell-images
```

---

## 4. SSE Architecture

### 4.1 Two distinct SSE connection types

| Type | Endpoint | Lifetime | Purpose |
|------|----------|----------|---------|
| AI streaming | `POST /api/ai/chat`, `POST /api/ai/inline` | Per-request (seconds) | Stream LLM tokens to the client |
| Notifications | `GET /api/notifications/stream` | Per-session (minutes–hours) | Push live notifications |

These are separate SSE connections. The AI endpoints use the Vercel AI SDK's `streamText` which returns an SSE response automatically. Notifications use NestJS's `@Sse()` decorator.

### 4.2 Notification SSE

```typescript
@Sse('stream')
@UseGuards(JwtAuthGuard)
stream(@Req() req): Observable<MessageEvent> {
  const userId = req.user.sub;
  return this.notificationsService.subscribe(userId);
}
```

Implementation notes:
- **Heartbeat:** emit a comment (`: heartbeat\n\n`) every 30 seconds to prevent Nginx proxy timeout (default 60s)
- **Reconnection:** `EventSource` auto-reconnects on disconnect; send `id:` field with each event so the client can resume via `Last-Event-ID` header
- **Cleanup:** on disconnect (observable unsubscribe), remove the subscriber from the in-memory map

### 4.3 Nginx SSE configuration

```nginx
location /api/ {
    proxy_pass http://api:3001/;
    proxy_http_version 1.1;
    proxy_set_header Connection '';
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 86400s;  # 24h for long-lived SSE
    add_header X-Accel-Buffering no;
}
```

### 4.4 CORS (development only)

When running without Nginx (frontend on `localhost:3000`, backend on `localhost:3001`):

```typescript
// main.ts
app.enableCors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true,
});
```

In production, Nginx proxies both services on the same origin, so CORS is not needed.

---

## 5. Marketplace Transaction Pseudocode

### 5.1 Platform fee

Platform fee is a **configurable percentage** defined as an environment variable:

```
PLATFORM_FEE_PERCENT=10
```

Fee calculation: `platformFee = Math.floor(creditsPaid * PLATFORM_FEE_PERCENT / 100)`

Writer payout: `writerPayout = creditsPaid - platformFee`

### 5.2 Preview unlock flow

```
POST /api/purchases/preview
Body: { articleId, idempotencyKey }

1. Validate JWT → extract magazineId
2. Validate magazine has account_type = 'magazine'
3. Validate magazine subscription_status = 'active'
4. Load article → validate placement = 'marketplace', status = 'published'
5. Validate article.author_id != magazineId (can't preview own articles)
6. Check no existing preview for (articleId, magazineId)

7. BEGIN TRANSACTION
   a. SELECT credit_balance FROM magazine_profiles
      WHERE id = magazineId FOR UPDATE
   b. previewPrice = Math.floor(article.marketplace_price * 0.10)
   c. IF credit_balance < previewPrice → ROLLBACK, return 402
   d. platformFee = Math.floor(previewPrice * PLATFORM_FEE_PERCENT / 100)
   e. writerPayout = previewPrice - platformFee
   f. UPDATE magazine_profiles
      SET credit_balance = credit_balance - previewPrice
      WHERE id = magazineId
   g. SELECT earnings_balance FROM users
      WHERE id = article.author_id FOR UPDATE
   h. UPDATE users
      SET earnings_balance = earnings_balance + writerPayout
      WHERE id = article.author_id
   i. INSERT INTO article_purchases (
        id, article_id, magazine_id, stage,
        credits_paid, platform_fee, writer_payout,
        parent_purchase_id
      ) VALUES (
        uuid(), articleId, magazineId, 'preview_unlock',
        previewPrice, platformFee, writerPayout,
        NULL
      )
   j. INSERT INTO transactions (
        id, type, amount, from_user_id, to_user_id,
        article_id, purchase_id, idempotency_key, status
      ) VALUES
      -- Magazine debit
      (uuid(), 'preview_unlock', previewPrice, magazineId, NULL,
       articleId, purchaseId, idempotencyKey + ':debit', 'completed'),
      -- Writer credit
      (uuid(), 'writer_payout', writerPayout, NULL, article.author_id,
       articleId, purchaseId, idempotencyKey + ':payout', 'completed')
8. COMMIT

9. Emit notification: article_previewed → writer
10. Return 201 { purchaseId, creditBalance: newBalance }
```

### 5.3 Full purchase flow

```
POST /api/purchases/buy
Body: { articleId, idempotencyKey }

1–6. Same validations as preview (but purchase stage)

7. Lookup existing preview:
   existingPreview = SELECT * FROM article_purchases
     WHERE article_id = articleId
       AND magazine_id = magazineId
       AND stage = 'preview_unlock'

8. Calculate remaining amount:
   IF existingPreview:
     remainingAmount = article.marketplace_price - existingPreview.credits_paid
     parentPurchaseId = existingPreview.id
   ELSE:
     remainingAmount = article.marketplace_price
     parentPurchaseId = NULL

9. BEGIN TRANSACTION
   a. SELECT credit_balance FROM magazine_profiles
      WHERE id = magazineId FOR UPDATE
   b. IF credit_balance < remainingAmount → ROLLBACK, return 402
   c. platformFee = Math.floor(remainingAmount * PLATFORM_FEE_PERCENT / 100)
   d. writerPayout = remainingAmount - platformFee
   e–j. Same pattern: debit magazine, credit writer,
        insert purchase row (stage='full_purchase', parent_purchase_id),
        insert transaction rows
10. COMMIT

11. Emit notification: article_purchased → writer
12. Return 201 { purchaseId, creditBalance: newBalance }
```

### 5.4 Idempotency key format

Generated client-side: `{magazineId}:{articleId}:{stage}:{timestamp}`

The `idempotency_key` UNIQUE constraint on `transactions` prevents double-charging if the client retries. On conflict, return the existing purchase result instead of inserting.

---

## 6. Analytics Aggregation Formulas

### 6.1 Article metrics (`aggregate-article-metrics`, every 5 min)

For each article with events since `last_aggregated_at`:

```sql
-- total_views
SELECT COUNT(*) FROM analytics_events
WHERE article_id = $1 AND event_type = 'view'

-- total_unique_views
SELECT COUNT(DISTINCT viewer_id) FROM analytics_events
WHERE article_id = $1 AND event_type = 'view' AND viewer_id IS NOT NULL

-- total_likes (from likes table, not events)
SELECT COUNT(*) FROM likes WHERE article_id = $1

-- total_comments
SELECT COUNT(*) FROM comments
WHERE article_id = $1 AND deleted_at IS NULL

-- total_reposts
SELECT COUNT(*) FROM reposts WHERE article_id = $1

-- avg_read_time_sec
SELECT AVG((metadata->>'engaged_seconds')::float)
FROM analytics_events
WHERE article_id = $1 AND event_type = 'time_on_page'

-- completion_rate
SELECT
  COUNT(*) FILTER (WHERE (metadata->>'completed')::boolean = true)::float
  / NULLIF(COUNT(*), 0)
FROM analytics_events
WHERE article_id = $1 AND event_type = 'time_on_page'

-- engagement_rate (% who scrolled past 75%)
WITH max_scroll AS (
  SELECT viewer_id, MAX((metadata->>'scroll_percentage')::float) AS max_pct
  FROM analytics_events
  WHERE article_id = $1 AND event_type = 'scroll' AND viewer_id IS NOT NULL
  GROUP BY viewer_id
)
SELECT
  COUNT(*) FILTER (WHERE max_pct >= 75)::float
  / NULLIF(COUNT(*), 0)
FROM max_scroll

-- paragraph_dropoff
-- For each paragraph_index, what % of viewers reached it
WITH viewer_max_para AS (
  SELECT viewer_id, MAX((metadata->>'paragraph_index')::int) AS max_para
  FROM analytics_events
  WHERE article_id = $1 AND event_type = 'scroll' AND viewer_id IS NOT NULL
  GROUP BY viewer_id
),
total_viewers AS (SELECT COUNT(*) AS cnt FROM viewer_max_para)
SELECT
  para_idx,
  COUNT(*) FILTER (WHERE max_para >= para_idx)::float / NULLIF(t.cnt, 0) AS retention
FROM viewer_max_para
CROSS JOIN total_viewers t
CROSS JOIN generate_series(0, (SELECT MAX(max_para) FROM viewer_max_para)) AS para_idx
GROUP BY para_idx, t.cnt
ORDER BY para_idx
```

Result stored as JSONB: `[{"idx": 0, "retention": 1.0}, {"idx": 1, "retention": 0.92}, ...]`

Dropoff = `1 - retention` at each index.

### 6.2 Writer audience metrics (`aggregate-writer-audience`, every 15 min)

```sql
-- total_unique_readers (lifetime, across all published articles)
SELECT COUNT(DISTINCT ae.viewer_id)
FROM analytics_events ae
JOIN articles a ON ae.article_id = a.id
WHERE a.author_id = $writer_id
  AND ae.event_type = 'view'
  AND ae.viewer_id IS NOT NULL
  AND a.status = 'published'
  AND a.deleted_at IS NULL

-- returning_reader_rate
-- Readers who viewed 2+ distinct articles by this writer
WITH reader_articles AS (
  SELECT ae.viewer_id, COUNT(DISTINCT ae.article_id) AS article_count
  FROM analytics_events ae
  JOIN articles a ON ae.article_id = a.id
  WHERE a.author_id = $writer_id
    AND ae.event_type = 'view'
    AND ae.viewer_id IS NOT NULL
  GROUP BY ae.viewer_id
)
SELECT
  COUNT(*) FILTER (WHERE article_count >= 2)::float
  / NULLIF(COUNT(*), 0)
FROM reader_articles

-- top_countries (top 5)
SELECT metadata->>'viewer_country' AS country,
       COUNT(*)::float / NULLIF(SUM(COUNT(*)) OVER(), 0) AS pct
FROM analytics_events ae
JOIN articles a ON ae.article_id = a.id
WHERE a.author_id = $writer_id AND ae.event_type = 'view'
  AND metadata->>'viewer_country' IS NOT NULL
GROUP BY country
ORDER BY COUNT(*) DESC
LIMIT 5

-- device_split
SELECT metadata->>'viewer_device' AS device,
       COUNT(*)::float / NULLIF(SUM(COUNT(*)) OVER(), 0) AS pct
FROM analytics_events ae
JOIN articles a ON ae.article_id = a.id
WHERE a.author_id = $writer_id AND ae.event_type = 'view'
GROUP BY device

-- avg_engaged_minutes
SELECT AVG((metadata->>'engaged_seconds')::float) / 60.0
FROM analytics_events ae
JOIN articles a ON ae.article_id = a.id
WHERE a.author_id = $writer_id AND ae.event_type = 'time_on_page'
```

### 6.3 Writer content metrics (`aggregate-writer-content`, every 15 min)

```sql
-- total_published
SELECT COUNT(*) FROM articles
WHERE author_id = $writer_id AND status = 'published' AND deleted_at IS NULL

-- posting_frequency (articles per month, last 12 months)
SELECT COUNT(*)::float / 12.0 FROM articles
WHERE author_id = $writer_id
  AND status = 'published'
  AND published_at >= NOW() - INTERVAL '12 months'

-- posting_consistency (coefficient of variation of inter-publication gaps)
WITH pub_dates AS (
  SELECT published_at,
    EXTRACT(EPOCH FROM published_at - LAG(published_at) OVER (ORDER BY published_at))
      / 86400.0 AS gap_days
  FROM articles
  WHERE author_id = $writer_id AND status = 'published' AND deleted_at IS NULL
  ORDER BY published_at
)
SELECT
  COALESCE(STDDEV(gap_days) / NULLIF(AVG(gap_days), 0), 0)
FROM pub_dates
WHERE gap_days IS NOT NULL

-- avg_article_length
SELECT AVG(word_count) FROM articles
WHERE author_id = $writer_id AND status = 'published' AND deleted_at IS NULL

-- top_tags
SELECT t.name, COUNT(*) AS cnt
FROM article_tags at
JOIN tags t ON at.tag_id = t.id
JOIN articles a ON at.article_id = a.id
WHERE a.author_id = $writer_id AND a.status = 'published'
GROUP BY t.name
ORDER BY cnt DESC
LIMIT 10

-- topic_distribution (percentage per tag)
-- Same as top_tags but with percentages
```

### 6.4 Writer quality metrics (`aggregate-writer-quality`, every 15 min)

```sql
-- engagement_rate (avg across all articles)
SELECT AVG(engagement_rate) FROM article_metrics am
JOIN articles a ON am.article_id = a.id
WHERE a.author_id = $writer_id

-- completion_rate (avg across all articles)
SELECT AVG(completion_rate) FROM article_metrics am
JOIN articles a ON am.article_id = a.id
WHERE a.author_id = $writer_id

-- repost_rate
SELECT SUM(total_reposts)::float / NULLIF(SUM(total_views), 0)
FROM article_metrics am
JOIN articles a ON am.article_id = a.id
WHERE a.author_id = $writer_id

-- comment_depth (avg comments per article)
SELECT AVG(total_comments)::float FROM article_metrics am
JOIN articles a ON am.article_id = a.id
WHERE a.author_id = $writer_id

-- retention_curve [25%, 50%, 75%, 100%]
-- Aggregated from paragraph_dropoff across all articles
-- For each quartile: avg retention at that % of article length
```

### 6.5 Eligibility computation

```sql
-- Run after aggregation, check all non-eligible writers
WITH writer_stats AS (
  SELECT
    a.author_id,
    (SELECT total_unique_readers FROM writer_audience_metrics
     WHERE writer_id = a.author_id) AS readers,
    (SELECT COUNT(*) FROM likes l
     JOIN articles a2 ON l.article_id = a2.id
     WHERE a2.author_id = a.author_id)
    +
    (SELECT COUNT(*) FROM comments c
     JOIN articles a3 ON c.article_id = a3.id
     WHERE a3.author_id = a.author_id AND c.deleted_at IS NULL)
    AS reactions
  FROM users u
  JOIN articles a ON a.author_id = u.id
  WHERE u.is_marketplace_eligible = FALSE
    AND u.account_type = 'personal'
    AND u.role = 'writer'
  GROUP BY a.author_id
)
SELECT author_id, readers, reactions
FROM writer_stats
WHERE readers >= $READER_THRESHOLD   -- 5000 or DEMO_MODE value
  AND reactions >= $REACTION_THRESHOLD -- 1000 or DEMO_MODE value
```

For each matching writer: update `is_marketplace_eligible`, `marketplace_eligible_at`, `marketplace_eligible_source`, insert audit log row.

---

## 7. Frontend Analytics Event Capture

### 7.1 Event batching

```typescript
class AnalyticsCollector {
  private buffer: AnalyticsEvent[] = [];
  private timer: ReturnType<typeof setTimeout> | null = null;

  track(event: AnalyticsEvent) {
    this.buffer.push(event);
    if (this.buffer.length >= 10) this.flush();
    else if (!this.timer) this.timer = setTimeout(() => this.flush(), 5000);
  }

  flush() {
    if (this.buffer.length === 0) return;
    const events = [...this.buffer];
    this.buffer = [];
    if (this.timer) { clearTimeout(this.timer); this.timer = null; }
    navigator.sendBeacon('/api/analytics/events', JSON.stringify({ events }));
  }
}
```

Use `sendBeacon` for reliability on page unload. Fall back to `fetch` with `keepalive: true`.

### 7.2 Scroll tracking with deduplication

```typescript
const reportedParagraphs = new Set<number>();

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const idx = Number(entry.target.dataset.paragraphIndex);
      if (!reportedParagraphs.has(idx)) {
        reportedParagraphs.add(idx);
        analytics.track({
          event_type: 'scroll',
          article_id: articleId,
          metadata: {
            paragraph_index: idx,
            scroll_percentage: Math.round((idx / totalParagraphs) * 100),
          }
        });
      }
    }
  });
}, { threshold: 0.5 });

// Observe each paragraph node
paragraphElements.forEach((el, i) => {
  el.dataset.paragraphIndex = String(i);
  observer.observe(el);
});
```

Each paragraph index is reported exactly once per page load. No duplicates on scroll-up/scroll-down.

### 7.3 Country and device detection

**Country:** extracted server-side from `X-Forwarded-For` or `CF-IPCountry` header (Cloudflare provides this). Stored as ISO 3166-1 alpha-2. Do not store raw IPs.

**Device:** parsed from `User-Agent` header server-side using a lightweight library (`ua-parser-js` or manual regex). Categorized as `mobile`, `desktop`, or `tablet`.

Both fields are injected into the `view` event metadata by the backend before storage, not by the frontend.

---

## 8. Hybrid Search (RRF)

### 8.1 Implementation location

RRF runs in `SearchService` (application layer), not as a single SQL query. Two queries are issued in parallel, then merged in TypeScript.

### 8.2 Pseudocode

```typescript
async search(query: string, limit = 20): Promise<SearchResult[]> {
  // 1. Embed the query
  const queryEmbedding = await this.embeddingService.embed(query);

  // 2. Run both searches in parallel
  const [lexicalResults, semanticResults] = await Promise.all([
    this.lexicalSearch(query, limit * 2),
    this.semanticSearch(queryEmbedding, limit * 2),
  ]);

  // 3. Reciprocal Rank Fusion
  const k = 60;
  const scores = new Map<string, number>(); // articleId → score

  lexicalResults.forEach((r, rank) => {
    const prev = scores.get(r.articleId) ?? 0;
    scores.set(r.articleId, prev + 1 / (k + rank + 1));
  });

  semanticResults.forEach((r, rank) => {
    const prev = scores.get(r.articleId) ?? 0;
    scores.set(r.articleId, prev + 1 / (k + rank + 1));
  });

  // 4. Sort by fused score, take top N
  const merged = [...scores.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit);

  // 5. Fetch full article data for the merged IDs
  return this.articlesRepo.findByIds(merged.map(([id]) => id));
}

private async lexicalSearch(query: string, limit: number) {
  return db.select()
    .from(articles)
    .where(sql`content_search @@ plainto_tsquery('english', ${query})`)
    .orderBy(sql`ts_rank(content_search, plainto_tsquery('english', ${query})) DESC`)
    .limit(limit);
}

private async semanticSearch(embedding: number[], limit: number) {
  return db.select()
    .from(articleChunks)
    .orderBy(sql`embedding <=> ${JSON.stringify(embedding)}::vector`)
    .limit(limit);
  // Note: deduplicate by article_id (multiple chunks per article)
}
```

---

## 9. Redis Key Conventions

```
Prefix               Example key                          TTL     Purpose
──────────────────────────────────────────────────────────────────────────
refresh:             refresh:{userId}:{tokenId}           7d      Refresh tokens
throttle:            throttle:{ip}:{endpoint}             per-window  Rate limiting (@nestjs/throttler)
bull:                bull:{queueName}:{jobId}             varies  BullMQ internal
cache:insights:      cache:insights:{writerId}            24h     Portfolio insights (optional Redis cache)
cache:metrics:       cache:metrics:{articleId}            5m      Article metrics (optional)
sse:heartbeat:       sse:heartbeat:{userId}               —       Not stored; heartbeat is in-process
```

BullMQ queue names:
```
embed-article
extract-writer-memory
aggregate-article-metrics
aggregate-writer-metrics
check-writer-eligibility
renew-magazine-subscriptions
reset-ai-tokens
send-email
```

---

## 10. Drizzle + pgvector Reference

### 10.1 Custom vector type

```typescript
import { customType } from 'drizzle-orm/pg-core';

const vector = customType<{ data: number[]; driverData: string }>({
  dataType() { return 'vector(1536)'; },
  toDriver(value: number[]) { return JSON.stringify(value); },
  fromDriver(value: string) {
    return value.replace(/[\[\]]/g, '').split(',').map(Number);
  },
});
```

### 10.2 Vector search query

```typescript
const results = await db
  .select({
    id: articleChunks.id,
    content: articleChunks.content,
    articleId: articleChunks.articleId,
  })
  .from(articleChunks)
  .where(
    sql`${articleChunks.articleId} IN (
      SELECT id FROM articles WHERE author_id = ${authorId}
    )`
  )
  .orderBy(sql`${articleChunks.embedding} <=> ${JSON.stringify(queryEmbedding)}::vector`)
  .limit(5);
```

### 10.3 HNSW index in migration

```sql
CREATE INDEX article_chunks_embedding_idx
ON article_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

This must be in a custom migration file since Drizzle Kit does not auto-generate HNSW indexes.

### 10.4 tsvector in Drizzle schema

```typescript
import { sql } from 'drizzle-orm';
import { customType, index } from 'drizzle-orm/pg-core';

const tsvector = customType<{ data: string; driverData: string }>({
  dataType() { return 'tsvector'; },
});

// In the articles table definition:
contentSearch: tsvector('content_search'),

// GIN index (custom migration):
// CREATE INDEX articles_content_search_idx ON articles USING gin(content_search);
```

---

## 11. Slug Generation

```typescript
import slugify from 'slugify';

async function generateUniqueSlug(title: string): Promise<string> {
  const base = slugify(title, { lower: true, strict: true }).slice(0, 200);
  let slug = base;
  let suffix = 0;

  while (await db.query.articles.findFirst({
    where: eq(articles.slug, slug)
  })) {
    suffix++;
    slug = `${base}-${suffix}`;
  }

  return slug;
}
```

Called in the article creation endpoint. The slug is immutable after creation (changing it would break URLs).

---

## 12. Rate Limiting Strategy

Using `@nestjs/throttler`:

```typescript
ThrottlerModule.forRoot([
  { name: 'short', ttl: 1000, limit: 3 },   // 3 req/sec per IP
  { name: 'medium', ttl: 60000, limit: 60 }, // 60 req/min per IP
  { name: 'long', ttl: 3600000, limit: 500 }, // 500 req/hour per IP
]);
```

Per-endpoint overrides:

| Endpoint | Limit | Reason |
|----------|-------|--------|
| `POST /auth/login` | 5/min | Brute-force protection |
| `POST /auth/register` | 3/min | Abuse prevention |
| `POST /ai/*` | 10/min | API cost control |
| `POST /analytics/events` | 30/min | High-frequency but bounded |
| `POST /purchases/*` | 5/min | Financial operations |

---

## 13. Environment Variable Catalog

```bash
# ── Database ──
DATABASE_URL=postgresql://user:pass@db:5432/inkwell
DATABASE_URL_TEST=postgresql://user:pass@db:5432/inkwell_test

# ── Redis ──
REDIS_URL=redis://redis:6379

# ── JWT ──
JWT_SECRET=<random-64-char>
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# ── MinIO ──
MINIO_ENDPOINT=minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=<key>
MINIO_SECRET_KEY=<secret>
MINIO_BUCKET=inkwell-images
MINIO_PUBLIC_URL=/storage  # URL prefix for public access via Nginx

# ── AI Providers ──
GROQ_API_KEY=<key>
GEMINI_API_KEY=<key>
COHERE_API_KEY=<key>
OPENAI_API_KEY=<key>           # fallback embeddings

# ── AI Config ──
LLM_PRIMARY_PROVIDER=groq      # groq | gemini
LLM_PRIMARY_MODEL=llama-3.3-70b-versatile
LLM_FALLBACK_PROVIDER=gemini
LLM_FALLBACK_MODEL=gemini-2.0-flash
EMBEDDING_PROVIDER=cohere       # cohere | openai
EMBEDDING_MODEL=embed-multilingual-v3.0

# ── Platform ──
PLATFORM_FEE_PERCENT=10
DAILY_AI_TOKENS_PREMIUM=50000
DAILY_AI_TOKENS_MAGAZINE=20000

# ── Eligibility (overridden in DEMO_MODE) ──
ELIGIBILITY_READER_THRESHOLD=5000
ELIGIBILITY_REACTION_THRESHOLD=1000

# ── Demo ──
DEMO_MODE=false

# ── Observability ──
SENTRY_DSN_BACKEND=<dsn>
SENTRY_DSN_FRONTEND=<dsn>

# ── Email ──
RESEND_API_KEY=<key>
RESEND_FROM_EMAIL=noreply@inkwell.ai

# ── Frontend ──
NEXT_PUBLIC_API_URL=/api
NEXT_PUBLIC_SENTRY_DSN=<dsn>

# ── Google OAuth ──
GOOGLE_CLIENT_ID=<id>
GOOGLE_CLIENT_SECRET=<secret>
GOOGLE_CALLBACK_URL=/api/auth/google/callback
```

---

## 14. Soft Delete Query Patterns

Every query on soft-deletable tables (`users`, `articles`, `comments`) must include the filter:

```typescript
// Standard pattern
.where(and(
  eq(articles.authorId, userId),
  isNull(articles.deletedAt),
))
```

For Drizzle, define a reusable helper:

```typescript
const notDeleted = <T extends { deletedAt: unknown }>(table: T) =>
  isNull(table.deletedAt);
```

Admin endpoints can bypass this filter to see deleted content.

---

## 15. BullMQ Job Design

### 15.1 Queue configuration

```typescript
const defaultJobOptions: JobsOptions = {
  attempts: 3,
  backoff: { type: 'exponential', delay: 1000 },
  removeOnComplete: { age: 86400 },  // keep completed jobs for 24h
  removeOnFail: { age: 604800 },     // keep failed jobs for 7 days
};
```

### 15.2 Scheduled jobs (repeatable)

```typescript
// In worker bootstrap:
await aggregateArticleMetricsQueue.add('run', {}, {
  repeat: { every: 5 * 60 * 1000 },  // 5 minutes
});
await aggregateWriterMetricsQueue.add('run', {}, {
  repeat: { every: 15 * 60 * 1000 }, // 15 minutes
});
await resetAiTokensQueue.add('run', {}, {
  repeat: { pattern: '0 0 * * *' },  // daily at midnight UTC
});
await renewSubscriptionsQueue.add('run', {}, {
  repeat: { pattern: '0 0 1 * *' },  // 1st of each month
});
```

### 15.3 Event-triggered jobs

```typescript
// In articles.service.ts, after publish:
await embedArticleQueue.add('embed', {
  articleId: article.id,
  authorId: article.authorId,
});
await extractWriterMemoryQueue.add('extract', {
  writerId: article.authorId,
});
```

### 15.4 Worker entrypoint

`src/worker.ts`:
```typescript
import { NestFactory } from '@nestjs/core';
import { WorkerModule } from './worker.module';

async function bootstrap() {
  const app = await NestFactory.createApplicationContext(WorkerModule);
  // BullMQ processors registered via module decorators
  // Keep process alive
}
bootstrap();
```

`WorkerModule` imports all processor modules but does NOT import HTTP controllers. It shares the same database and Redis connections as the API.

---

## 16. Testing Strategy

### 16.1 Test database

Use the same Docker PostgreSQL with a separate database:

```typescript
// test/setup.ts
beforeAll(async () => {
  testDb = drizzle(new Pool({
    connectionString: process.env.DATABASE_URL_TEST,
  }));
  await migrate(testDb, { migrationsFolder: './drizzle' });
});

afterEach(async () => {
  // Truncate all tables between tests
  await testDb.execute(sql`TRUNCATE users, articles, ... CASCADE`);
});
```

### 16.2 Ledger invariant test helper

```typescript
async function assertLedgerIntegrity(db: Database) {
  // Check every writer's earnings_balance
  const writers = await db.select().from(users)
    .where(eq(users.accountType, 'personal'));

  for (const writer of writers) {
    const sum = await db.select({
      total: sql<number>`COALESCE(SUM(amount), 0)`
    }).from(transactions)
      .where(and(
        eq(transactions.toUserId, writer.id),
        eq(transactions.type, 'writer_payout'),
        eq(transactions.status, 'completed'),
      ));
    expect(writer.earningsBalance).toBe(sum[0].total);
  }

  // Check every magazine's credit_balance
  const magazines = await db.select().from(magazineProfiles);
  for (const mag of magazines) {
    const creditsIn = await db.select({
      total: sql<number>`COALESCE(SUM(amount), 0)`
    }).from(transactions)
      .where(and(
        eq(transactions.toUserId, mag.id),
        inArray(transactions.type, ['monthly_credit_grant', 'credit_topup']),
        eq(transactions.status, 'completed'),
      ));

    const creditsOut = await db.select({
      total: sql<number>`COALESCE(SUM(amount), 0)`
    }).from(transactions)
      .where(and(
        eq(transactions.fromUserId, mag.id),
        inArray(transactions.type, ['preview_unlock', 'article_full_purchase']),
        eq(transactions.status, 'completed'),
      ));

    expect(mag.creditBalance).toBe(creditsIn[0].total - creditsOut[0].total);
  }
}
```

Call `assertLedgerIntegrity(db)` after every transaction-related test.

---

## 17. Memory Extraction — Input Scope Decision

**Decision:** extract from the **most recent 10 published articles** (or fewer if the writer has < 10).

Rationale:
- Full corpus is expensive for prolific writers (50+ articles → large LLM context)
- Using all articles weights early writing equally with current style
- Most recent 10 captures current voice while providing enough signal
- If the writer has < 10 articles, use all of them

Implementation in `extract-writer-memory` job:
```typescript
const recentArticles = await db.select()
  .from(articles)
  .where(and(
    eq(articles.authorId, writerId),
    eq(articles.status, 'published'),
    isNull(articles.deletedAt),
  ))
  .orderBy(desc(articles.publishedAt))
  .limit(10);

const corpusText = recentArticles
  .map(a => extractFullText(a.content))
  .join('\n\n---\n\n');

// LLM call with corpusText as input
// Zod schema for output validation
```

---

## 18. Embedding Provider — Final Decision

**Provider:** OpenAI `text-embedding-3-small` (1536 dimensions). This is now reflected in all specs.

- Costs $0.02 per million tokens — under $0.10 total at PFE scale
- No trial expiry risk (was the primary concern with Cohere)
- No fallback or provider-switching logic needed
- Schema uses `VECTOR(1536)` throughout

---

## 19. Reconciliation Job

`reconcile-balances` runs nightly (or on-demand via admin endpoint):

```typescript
async reconcile(): Promise<ReconciliationReport> {
  const drifts: Drift[] = [];

  // Writer earnings
  const writers = await db.execute(sql`
    SELECT u.id, u.earnings_balance AS snapshot,
      COALESCE(SUM(t.amount), 0) AS ledger_sum
    FROM users u
    LEFT JOIN transactions t
      ON t.to_user_id = u.id
      AND t.type = 'writer_payout'
      AND t.status = 'completed'
    WHERE u.account_type = 'personal'
    GROUP BY u.id
    HAVING u.earnings_balance != COALESCE(SUM(t.amount), 0)
  `);

  // Magazine credits
  const magazines = await db.execute(sql`
    SELECT mp.id, mp.credit_balance AS snapshot,
      COALESCE(credits_in.total, 0) - COALESCE(credits_out.total, 0) AS ledger_sum
    FROM magazine_profiles mp
    LEFT JOIN LATERAL (
      SELECT SUM(amount) AS total FROM transactions
      WHERE to_user_id = mp.id
        AND type IN ('monthly_credit_grant', 'credit_topup')
        AND status = 'completed'
    ) credits_in ON TRUE
    LEFT JOIN LATERAL (
      SELECT SUM(amount) AS total FROM transactions
      WHERE from_user_id = mp.id
        AND type IN ('preview_unlock', 'article_full_purchase')
        AND status = 'completed'
    ) credits_out ON TRUE
    HAVING mp.credit_balance != COALESCE(credits_in.total, 0) - COALESCE(credits_out.total, 0)
  `);

  if (writers.length > 0 || magazines.length > 0) {
    // Log critical alert to Sentry
    Sentry.captureMessage('LEDGER DRIFT DETECTED', {
      level: 'fatal',
      extra: { writers, magazines },
    });
  }

  return { drifts: [...writers, ...magazines], ok: writers.length === 0 && magazines.length === 0 };
}
```

---

## 20. Specification Gap Summary

| # | Gap | Risk if unspecified | Status |
|---|-----|--------------------|----|
| 1 | TipTap JSON → plain text extraction | **CRITICAL** — blocks tsvector, RAG, word count | Specified in §1 |
| 2 | tsvector population strategy | **CRITICAL** — search won't work | Specified in §1.4 |
| 3 | RAG chunking rules | **HIGH** — wrong chunks = bad RAG | Specified in §1.5 |
| 4 | Refresh token storage/revocation | **HIGH** — security gap | Specified in §2.3 |
| 5 | MinIO upload flow through Nginx | **HIGH** — uploads will fail in Docker | Specified in §3 |
| 6 | SSE architecture (two types) | **HIGH** — Nginx will kill notification connections | Specified in §4 |
| 7 | Purchase transaction pseudocode | **CRITICAL** — wrong ledger = data corruption | Specified in §5 |
| 8 | Platform fee definition | **HIGH** — undefined business rule | Specified in §5.1 |
| 9 | Idempotency key format | **MEDIUM** — double-charge risk without it | Specified in §5.4 |
| 10 | Analytics aggregation SQL | **HIGH** — wrong metrics look right | Specified in §6 |
| 11 | Eligibility computation SQL | **MEDIUM** — wrong threshold check | Specified in §6.5 |
| 12 | Frontend event capture + dedup | **MEDIUM** — inflated analytics | Specified in §7 |
| 13 | Country/device detection | **LOW** — metadata quality | Specified in §7.3 |
| 14 | RRF implementation | **MEDIUM** — agents will write wrong SQL | Specified in §8 |
| 15 | Redis key conventions | **LOW** — naming conflicts | Specified in §9 |
| 16 | Drizzle + pgvector custom type | **HIGH** — blocks schema definition | Specified in §10 |
| 17 | Slug generation | **LOW** — collision handling | Specified in §11 |
| 18 | Rate limiting strategy | **MEDIUM** — abuse risk | Specified in §12 |
| 19 | Environment variable catalog | **MEDIUM** — missing vars = broken deploy | Specified in §13 |
| 20 | Soft delete query patterns | **LOW** — data leaks if forgotten | Specified in §14 |
| 21 | BullMQ job design | **MEDIUM** — worker bootstrap | Specified in §15 |
| 22 | Testing infrastructure | **HIGH** — no tests = no confidence | Specified in §16 |
| 23 | Memory extraction scope | **MEDIUM** — cost/quality tradeoff | Specified in §17 |
| 24 | Embedding provider decision | **HIGH** — Cohere trial expiry risk | Specified in §18 |
| 25 | Reconciliation job | **MEDIUM** — drift detection | Specified in §19 |
| 26 | AI token quota values | **MEDIUM** — undefined limits | Specified in §2.4 |
| 27 | Password hashing | **LOW** — but must be specified | Specified in §2.1 |
| 28 | CORS for development | **LOW** — blocks local dev | Specified in §4.4 |
