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

// Estimated read time (200 wpm average)
function estimateReadTime(doc: TipTapNode): number {
  return Math.max(1, Math.ceil(countWords(doc) / WORDS_PER_MINUTE));
}
```

> **Corrected 2026-08-24.** This specified **250** wpm; the implementation uses
> **200** (`WORDS_PER_MINUTE` in `common/constants.ts:42`, applied in
> `tiptap-utils.ts:106`). 200 wpm is the conventional figure for reading prose on
> screen and is the more conservative of the two — it over-estimates rather than
> under-estimates the time a reader is asked for. The difference is not cosmetic:
> at 250 wpm a 2,000-word essay advertises 8 minutes, at 200 wpm it advertises 10.

### 1.4 tsvector population

> **Corrected 2026-08-24.** This described a single application-written `tsvector`
> column. What exists is a **split**: the application writes flattened *text*, and
> Postgres derives the vector from it as a `GENERATED ALWAYS ... STORED` column.
> The strategy below is half right — the flattening is application-layer, the
> vectorising is not, and it is not a trigger either.

**Strategy:** the application writes plain text; the database derives the vector.

On every article `INSERT` or `UPDATE` that changes `content`, the app flattens the
TipTap document and stores the result as **text**:

```typescript
await db.update(articles)
  .set({
    contentSearch: extractFullText(content),   // TEXT, not tsvector
    wordCount:     countWords(content),
    readTime:      estimateReadTime(content),
  })
  .where(eq(articles.id, articleId));
```

`articles.search_vector` is then maintained by Postgres itself:

```sql
search_vector tsvector GENERATED ALWAYS AS (
  setweight(to_tsvector('english', coalesce(title,          '')), 'A') ||
  setweight(to_tsvector('english', coalesce(excerpt,        '')), 'B') ||
  setweight(to_tsvector('english', coalesce(content_search, '')), 'C')
) STORED
```

**Why the split rather than one application-written column.** Extracting readable
text from a TipTap tree is a tree walk and belongs in application code. Turning
that text into a weighted vector is a pure function of the row, and a generated
column cannot drift from its inputs: there is no code path that can update the
title and forget the index. The weighting is the other half of the reason — a
title match outranks an excerpt match outranks a body match, which a single
`to_tsvector` over one concatenated string cannot express.

Still true from the original: this is synchronous inside the save/publish endpoint,
never a background job. The index must be current the moment the article is
searchable. See `6-database-schema.md` §3.3 for the full column pair, and note that
`'english'` is hard-coded because a generated column must be `IMMUTABLE`.

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

**Refresh token** (7 days): a **JWT**, signed with `JWT_REFRESH_SECRET`.

### 2.3 Refresh token storage — NOT IMPLEMENTED AS SPECIFIED

> **Corrected 2026-08-21.** This section specified opaque UUIDs in Redis,
> explicitly "NOT a JWT — this allows revocation". The built system does the
> opposite: `auth.service.ts` issues a second JWT and validates it with
> `this.jwt.verify(refreshToken, { secret: … })`. There is no `refresh_tokens`
> table, no Redis key, and nothing is stored server-side.
>
> **The consequence is the property this section was written to obtain: refresh
> tokens cannot be revoked.** Logout clears the client's copy only. Until it
> expires, a captured refresh token stays valid across a password change and a
> ban, and none of the four flows below exist:
>
> - ~~Login: store `tokenId` in Redis~~
> - ~~Refresh: look the token up, rotate it~~
> - ~~Logout: delete the key~~
> - ~~Password change / ban: delete all keys for that user~~
>
> Recorded rather than quietly dropped because it is a **security limitation the
> report should state**, not a detail. Closing it means either the Redis key
> structure originally specified here or a `refresh_tokens` table; the 7-day TTL
> bounds the exposure in the meantime.

The original design, kept for reference:

```
Key:    refresh:{userId}:{tokenId}
Value:  { userAgent, createdAt }
TTL:    7 days (604800 seconds)
```

### 2.4 AI token quota

> **Corrected 2026-08-24.** The allowances here were wrong by a factor of fifty,
> and the magazine row describes an entitlement that does not exist. Premium
> accounts receive **1,000** tokens a day (`PREMIUM_DAILY_AI_TOKENS` in
> `common/constants.ts:14`), not 50,000, and **magazine accounts are excluded from
> the AI quota entirely** — the grant is filtered on `account_type = 'personal'`
> (`ai/ai-token-allowance.ts`). The exclusion is a product rule, not an oversight:
> the AI assistant is a *writing* tool and a magazine account does not write.

| Plan | Daily AI tokens | Reset time |
|------|----------------|------------|
| Free (personal) | 0 — no AI access | — |
| Premium (personal) | 1,000 | Daily at 00:00 UTC |
| Magazine | none — excluded | — |

One "AI token" = one LLM token consumed (input + output combined). The
`ai_tokens_remaining` field on the `users` table is decremented after each AI
response by the actual `tokens_used` value reported by the Vercel AI SDK.

The allowance exists once, as a SQL fragment (`dailyAllowanceSql`), and has two
consumers: the nightly `reset-ai-tokens` cron and a lazy top-up on the read path.

```sql
-- dailyAllowanceSql
CASE WHEN plan = 'premium' THEN 1000 ELSE 0 END
```

```sql
-- the nightly reset, 00:00 UTC
UPDATE users
SET ai_tokens_remaining = <dailyAllowanceSql>,
    ai_tokens_reset_at  = now()
WHERE deleted_at IS NULL
  AND account_type = 'personal';
```

**Why a lazy top-up as well as a cron.** A nightly job alone means an account that
upgrades to premium at 09:00 sees a balance of 0 until midnight — and because the
client derives "exhausted" from that balance and disables the composer, the user
cannot make the request that would have granted their tokens. Every path that
*reports* the balance therefore also grants it if a grant is due
(`readQuotaGrantingIfDue`), in one atomic `UPDATE … WHERE <due>` so two concurrent
callers cannot both grant.

**Why free accounts are skipped rather than granted 0.** Writing "0" would stamp
`ai_tokens_reset_at` with today's date, consuming the only signal that says "this
account has never been granted" — so an upgrade an hour later would find the reset
no longer due and sit at 0 until midnight. The grant is guarded on
`(<dailyAllowanceSql>) > 0` so a free account's `reset_at` stays NULL and its first
read after upgrading pays out immediately.

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

> **Corrected 2026-08-24.** This section specified a **10%** fee read from an
> environment variable `PLATFORM_FEE_PERCENT`. Both halves are wrong: the rate is
> **20%**, and no such environment variable exists — the value is a compile-time
> constant. `PLATFORM_FEE_PERCENT` has been dropped from the §13 catalogue with
> this edit. Evidence: `common/constants.ts:119`, `purchases/pricing.ts:94`.
>
> Note this is **not** the 10% that appears throughout `2-features.md`,
> `3-user-flows.md` and `1-product-overview.md`. That is the *preview fraction* —
> what a magazine pays to unlock a preview — and it is correct at 10%. The two
> percentages are unrelated and only one of them drifted.

The platform fee is a **fixed rate expressed in basis points**, defined in code:

```ts
// common/constants.ts
export const PLATFORM_FEE_BPS = 2000;   // 20%
export const BPS_DENOMINATOR = 10_000;  // 100%
```

Fee calculation: `platformFee = Math.floor(creditsPaid * PLATFORM_FEE_BPS / BPS_DENOMINATOR)`

Writer payout: `writerPayout = creditsPaid - platformFee`

**Why basis points rather than a percentage or a float.** Credits are integers and
the ledger must reconcile exactly; `price * 0.2` is floating-point multiplication,
and `105 * 0.2` evaluates to `21.000000000000004`. Basis points keep the entire
calculation in integer arithmetic with a single floor at the end. The fee is
floored and the payout takes the remainder, so the writer absorbs no rounding loss
and the two always sum back to `creditsPaid` — which is what ledger invariant (c),
`credits_paid == platform_fee + writer_payout`, checks on every transaction.

**Why a constant rather than configuration.** Changing the rate changes what
writers earn, which is a product decision and not a deployment knob. It needs no
migration either way: each `article_purchases` row stores its own `platform_fee`
and `writer_payout`, so historical rows keep the split they were written with
rather than being recomputed from whatever the current rate happens to be.

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
   d. platformFee = Math.floor(previewPrice * PLATFORM_FEE_BPS / BPS_DENOMINATOR)
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
   c. platformFee = Math.floor(remainingAmount * PLATFORM_FEE_BPS / BPS_DENOMINATOR)
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

> **Corrected 2026-08-21.** Of the six prefixes originally listed here, exactly
> one is real. Redis holds BullMQ's queues and nothing else.

```
Prefix               Example key                          TTL     Purpose
──────────────────────────────────────────────────────────────────────────
bull:                bull:{queueName}:{jobId}             varies  BullMQ internal — the ONLY use of Redis
```

The five that were specified and never built, and where that state actually
lives instead:

| Prefix | Status |
|--------|--------|
| `refresh:` | Never built. Refresh tokens are JWTs — see §2.3. |
| `throttle:` | Never built. `@nestjs/throttler` is declared with no storage option, so it uses its in-memory store — per process, not shared. |
| `cache:insights:` | Built as a **Postgres table**, `portfolio_insights`, keyed by writer with an index on `expires_at`. Same 24h TTL, different substrate. |
| `cache:metrics:` | Never built. `article_metrics` is read straight from Postgres. |
| `sse:heartbeat:` | Correctly described as not stored; the heartbeat is in-process. |

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

> **Corrected 2026-08-24.** This catalogue was written before the backend existed
> and was never reconciled against it. Roughly half of what it listed does not
> exist: variable names that were never adopted (`JWT_ACCESS_EXPIRY`,
> `SENTRY_DSN_BACKEND`), knobs that turned out to be compile-time constants
> (`PLATFORM_FEE_PERCENT`, the AI token allowances, the eligibility thresholds),
> pluggability that was never built (`EMBEDDING_PROVIDER`, the four `LLM_*`
> variables), and a feature that was never started (`RESEND_*`, `DEMO_MODE`).
>
> The catalogue below is now generated from `config/env.validation.ts`, which is
> the single Zod schema every variable must pass at boot — a misspelled name is a
> startup failure, not a silent default. What was removed, and why, is tabulated
> after it.

```bash
# ── Runtime ──
NODE_ENV=development            # development | production | test
PORT=3000

# ── Database ──
DATABASE_URL=postgresql://user:pass@db:5432/inkwell

# ── Redis ──
REDIS_URL=redis://redis:6379

# ── JWT ──
JWT_SECRET=<min 32 chars>
JWT_EXPIRES_IN=15m
JWT_REFRESH_SECRET=<min 32 chars>       # distinct from JWT_SECRET
JWT_REFRESH_EXPIRES_IN=7d

# ── MinIO ──
MINIO_ENDPOINT=minio
MINIO_PORT=9000
MINIO_USE_SSL=false
MINIO_ACCESS_KEY=<key>
MINIO_SECRET_KEY=<secret>
MINIO_BUCKET=inkwell

# ── Origins ──
FRONTEND_URL=http://localhost:3000      # also the OAuth callback's return target
CORS_ORIGINS=                           # empty in production: FRONTEND_URL is the allow-list

# ── AI Providers ──
GROQ_API_KEY=<key>              # the LLM. Both chat models live here.
GEMINI_API_KEY=<key>            # LLM fallback AND all embeddings
OPENAI_API_KEY=<key>            # optional: moderation only, not embeddings

# ── Observability ──
SENTRY_DSN=<dsn>                # optional; the SDK no-ops without it

# ── Google OAuth ──
GOOGLE_CLIENT_ID=<id>
GOOGLE_CLIENT_SECRET=<secret>
GOOGLE_CALLBACK_URL=http://localhost:8080/api/auth/google/callback
```

Two more are **build-time** variables belonging to the web image, not to this
schema. Next.js inlines `NEXT_PUBLIC_*` into the browser bundle during
`next build`, so setting them at runtime configures nothing:

```bash
NEXT_PUBLIC_API_URL=/api
NEXT_PUBLIC_SITE_URL=https://inkwell.ai
NEXT_PUBLIC_SENTRY_DSN=<dsn>            # the browser DSN; distinct from SENTRY_DSN
NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED=false  # renders the "Continue with Google" button
```

`NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED` is separate from `GOOGLE_CLIENT_ID` because that
value is a server secret and never reaches the browser, and because
`GoogleStrategy` falls back to the literal client id `'not-configured'` rather than
failing at boot — so on a deployment with no credentials a rendered button would
send the user to Google's own `invalid_client` error page. The flag is the
deployment asserting that the server half is configured.

### What was removed, and why

| Removed | Why |
|---|---|
| `PLATFORM_FEE_PERCENT` | The fee is the compile-time constant `PLATFORM_FEE_BPS = 2000`. See §5.1. |
| `DAILY_AI_TOKENS_PREMIUM`, `DAILY_AI_TOKENS_MAGAZINE` | The allowance is `PREMIUM_DAILY_AI_TOKENS = 1000`, and magazines have no allowance at all. See §2.4. |
| `ELIGIBILITY_READER_THRESHOLD`, `ELIGIBILITY_REACTION_THRESHOLD` | Constants: `ELIGIBILITY_MIN_READERS = 5_000`, `ELIGIBILITY_MIN_REACTIONS = 1_000`. The values are right; their configurability was not. |
| `COHERE_API_KEY`, `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL` | Embeddings are not pluggable. `EmbeddingsService` names `gemini-embedding-001` directly and validates the returned vector against the column's 1536 dimensions — a provider swap is a migration, not an environment change. See §18. |
| `LLM_PRIMARY_PROVIDER`, `LLM_PRIMARY_MODEL`, `LLM_FALLBACK_PROVIDER`, `LLM_FALLBACK_MODEL` | The model list is the constant `LLM_MODELS = ['openai/gpt-oss-120b', 'openai/gpt-oss-20b']`, and failover runs *within* Groq. The specified Groq → Gemini chain was never built and cannot be — see NFR-24. |
| `DEMO_MODE` | Never implemented. No code reads it. |
| `RESEND_API_KEY`, `RESEND_FROM_EMAIL` | Transactional email was never built. Notifications are in-app only. |
| `MINIO_PUBLIC_URL` | Public object URLs are served by nginx at `/storage`, an nginx concern rather than an application one. |

One variable is **not removed but re-filed**: `DATABASE_URL_TEST` is real and
required, but it belongs to the *test harness*, not to the application. It is read
directly by `test/global-setup.ts` from `.env.test` and never passes through the
Zod schema, because the running API must never be able to reach the test database:

```bash
# .env.test — test harness only
DATABASE_URL_TEST=postgresql://user:pass@db:5432/inkwell_test
```

**Renamed** rather than removed: `JWT_ACCESS_EXPIRY` → `JWT_EXPIRES_IN`,
`JWT_REFRESH_EXPIRY` → `JWT_REFRESH_EXPIRES_IN`, `SENTRY_DSN_BACKEND` →
`SENTRY_DSN`, `SENTRY_DSN_FRONTEND` → `NEXT_PUBLIC_SENTRY_DSN`. `JWT_REFRESH_SECRET`
is **new** and mandatory: the refresh token is signed with its own secret, so a
leaked access-token secret cannot mint refresh tokens.

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

> **Superseded 2026-08-24.** The decision recorded below was taken before
> implementation and did not survive it. Embeddings are produced by **Gemini
> `gemini-embedding-001`**, not by OpenAI. The section is kept rather than
> rewritten, because the reasoning that led here — and the fact that it was
> overturned by something the reasoning could not have known — is part of the
> record. See "What actually shipped" beneath it.

### The decision as taken (superseded)

**Provider:** OpenAI `text-embedding-3-small` (1536 dimensions).

- Costs $0.02 per million tokens — under $0.10 total at PFE scale
- No trial expiry risk (was the primary concern with Cohere)
- No fallback or provider-switching logic needed
- Schema uses `VECTOR(1536)` throughout

### What actually shipped

**Provider:** Gemini `gemini-embedding-001`, requested at
`outputDimensionality: 1536` (`ai/embeddings.service.ts:35,128`).

The reasoning above holds on every point except the one that decided it: cost was
never the binding constraint, *having a working key* was. `GEMINI_API_KEY` was
already in the deployment for the LLM fallback, so embeddings could ship without
adding a second paid provider to a student project. `OPENAI_API_KEY` remains in the
schema but is optional and unrelated — when present it selects OpenAI's
`/v1/moderations` endpoint over the Groq classifier.

Three consequences worth stating, because they are what make this a decision
rather than a substitution:

1. **1536 dimensions was preserved deliberately.** `gemini-embedding-001` emits
   3072 by default; the service asks for 1536 so the existing `VECTOR(1536)` column
   and its ivfflat index stand unchanged. Every dimension count in the schema
   documents remains correct.
2. **The dimension is asserted, not assumed.** `EmbeddingsService` compares each
   returned vector's length against `EMBEDDING_DIMENSIONS` and throws on a
   mismatch. A provider silently changing its output width would otherwise write
   garbage into a typed column.
3. **The provider is not configurable, and that is the design.** The model name is
   a constant, not an environment variable. Swapping providers changes the vector
   space itself, which invalidates every stored embedding — it is a migration and a
   full re-index, not a redeploy. The `EMBEDDING_PROVIDER` / `EMBEDDING_MODEL`
   variables this document once listed have been removed from §13 for that reason.

One property of this model shapes the retrieval code and is documented at
`retrieval.service.ts:38`: `gemini-embedding-001` does not use the full [0,1]
similarity range, so the relevance threshold is tuned to the model rather than set
at an intuitive-looking round number.

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
