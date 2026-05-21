# 06 - Database Schema

## 1. Overview

This document defines the database schema for the Inkwell platform.

The system uses **PostgreSQL 16** with the **pgvector** extension for relational data, full-text search (`tsvector`), and vector storage (RAG embeddings).

The schema is designed to:
- Ensure data consistency and referential integrity
- Support the writer / magazine marketplace
- Enable efficient querying for both transactional and analytical workloads
- Power RAG retrieval (writer-facing AI + magazine-facing Portfolio Insights)
- Handle event-driven analytics aggregation

---

## 2. Design Principles

- Normalized structure for core entities
- Foreign keys enforced everywhere; cascade strategies documented per relation
- Indexes on every frequently-queried field
- **Soft deletes** (`deleted_at`) on user-facing tables for moderation + recovery
- Vector embeddings stored in the same database as relational data (pgvector)
- JSON columns only where flexibility is needed (TipTap content, analytics metadata)

---

## 3. Core Entities

### 3.1 Users

Represents all platform members. Account-type and role-plan are kept orthogonal.

```
id                  UUID PK
account_type        ENUM('personal', 'magazine')
email               VARCHAR(255) UNIQUE NOT NULL
username            VARCHAR(50)  UNIQUE NOT NULL          -- for /u/[username] URLs
password_hash       VARCHAR(255) NULL                     -- nullable for OAuth-only
provider            ENUM('local', 'google')
role                ENUM('reader', 'writer', 'admin')     -- personal accounts only
plan                ENUM('free', 'premium')                -- personal accounts only
name                VARCHAR(100)
bio                 TEXT
avatar_url          VARCHAR(500)
wallet_balance      INTEGER NOT NULL DEFAULT 0            -- platform credits
ai_tokens_remaining INTEGER NOT NULL DEFAULT 0            -- daily AI quota
ai_tokens_reset_at  TIMESTAMPTZ
last_login_at       TIMESTAMPTZ
created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
deleted_at          TIMESTAMPTZ NULL                       -- soft delete
```

Constraints:
- For `account_type = 'magazine'`, `role` and `plan` are NULL (enforced via CHECK constraint)
- For `account_type = 'personal'`, `role` and `plan` are NOT NULL

Indexes:
- `email` (UNIQUE)
- `username` (UNIQUE)
- `account_type`
- `deleted_at` (partial index `WHERE deleted_at IS NULL`)

---

### 3.2 Magazine Profiles

Extends `users` for magazine-specific fields. One-to-one with `users` where `account_type = 'magazine'`.

```
id              UUID PK, FK → users.id ON DELETE CASCADE
display_name    VARCHAR(100) NOT NULL                     -- shown on profile
slug            VARCHAR(100) UNIQUE NOT NULL              -- /m/[slug] URL
logo_url        VARCHAR(500)
website_url    VARCHAR(500)
description     TEXT
contact_email   VARCHAR(255)
created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `slug` (UNIQUE)

---

### 3.3 Articles

```
id              UUID PK
author_id       UUID NOT NULL FK → users.id
title           VARCHAR(255) NOT NULL
slug            VARCHAR(255) UNIQUE NOT NULL              -- /articles/[slug]
excerpt         TEXT
content         JSONB NOT NULL                            -- TipTap JSON
content_search  TSVECTOR                                  -- full-text search index
thumbnail_url   VARCHAR(500)
status          ENUM('draft', 'published') NOT NULL DEFAULT 'draft'
visibility      ENUM('free', 'premium') NOT NULL DEFAULT 'free'
licensable      BOOLEAN NOT NULL DEFAULT FALSE
license_price   INTEGER NULL                              -- platform credits, required if licensable
read_time       INTEGER                                    -- estimated minutes
word_count      INTEGER
created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
published_at    TIMESTAMPTZ NULL
deleted_at      TIMESTAMPTZ NULL
```

Constraints:
- If `licensable = TRUE` then `license_price > 0`
- `slug` auto-generated from title with collision suffix

Indexes:
- `author_id`
- `slug` (UNIQUE)
- `status`
- `visibility`
- `licensable`
- `published_at DESC` (for feed pagination)
- `content_search` (GIN index for full-text search)
- `deleted_at` (partial index `WHERE deleted_at IS NULL`)

---

### 3.4 Tags

```
id          UUID PK
name        VARCHAR(50) UNIQUE NOT NULL
slug        VARCHAR(50) UNIQUE NOT NULL
created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
```

### 3.4.1 Article Tags (Join)

```
article_id  UUID FK → articles.id ON DELETE CASCADE
tag_id      UUID FK → tags.id     ON DELETE CASCADE
PRIMARY KEY (article_id, tag_id)
```

Indexes:
- `tag_id` (for "articles tagged X" queries)

---

### 3.5 Comments

Threaded via self-referencing `parent_id`.

```
id          UUID PK
article_id  UUID NOT NULL FK → articles.id ON DELETE CASCADE
user_id     UUID NOT NULL FK → users.id
parent_id   UUID NULL FK → comments.id     ON DELETE CASCADE
content     TEXT NOT NULL
created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
deleted_at  TIMESTAMPTZ NULL
```

Indexes:
- `article_id`
- `parent_id`
- `user_id`

---

### 3.6 Likes

```
id          UUID PK
user_id     UUID NOT NULL FK → users.id
article_id  UUID NOT NULL FK → articles.id ON DELETE CASCADE
created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
UNIQUE (user_id, article_id)
```

Indexes:
- `article_id`

---

### 3.7 Follows

```
id            UUID PK
follower_id   UUID NOT NULL FK → users.id
following_id  UUID NOT NULL FK → users.id
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
UNIQUE (follower_id, following_id)
CHECK (follower_id != following_id)
```

Indexes:
- `follower_id`
- `following_id`

---

### 3.8 Reposts

```
id          UUID PK
user_id     UUID NOT NULL FK → users.id
article_id  UUID NOT NULL FK → articles.id ON DELETE CASCADE
created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
UNIQUE (user_id, article_id)
```

---

## 4. Marketplace Entities

### 4.1 Article Licenses

Records a magazine's right to feature an article in their library.

```
id              UUID PK
article_id      UUID NOT NULL FK → articles.id
magazine_id     UUID NOT NULL FK → users.id      -- account_type = magazine
price_paid      INTEGER NOT NULL                  -- platform credits at time of purchase
platform_fee    INTEGER NOT NULL                  -- fee withheld from writer payout
writer_payout   INTEGER NOT NULL                  -- price_paid - platform_fee
licensed_at     TIMESTAMPTZ NOT NULL DEFAULT now()
UNIQUE (article_id, magazine_id)                   -- can't double-license same article
```

Constraints:
- Writers cannot license their own articles (CHECK or app-layer guard)
- Article must be `licensable = TRUE` and `status = 'published'` at time of license

Indexes:
- `article_id`
- `magazine_id`
- `licensed_at DESC` (for recent licenses query)

---

### 4.2 Transactions

Atomic financial ledger. Every wallet movement creates one transaction row.

```
id               UUID PK
type             ENUM('license_purchase', 'wallet_topup', 'writer_payout', 'platform_fee', 'refund')
amount           INTEGER NOT NULL                 -- positive or negative depending on direction
from_user_id     UUID NULL FK → users.id          -- nullable for top-ups from external
to_user_id       UUID NULL FK → users.id          -- nullable for platform-fee sinks
article_id       UUID NULL FK → articles.id       -- nullable except for license transactions
license_id       UUID NULL FK → article_licenses.id
idempotency_key  VARCHAR(100) UNIQUE              -- prevents double-charging on retry
status           ENUM('pending', 'completed', 'failed', 'refunded') NOT NULL
metadata         JSONB                             -- provider response, error details, etc.
created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `from_user_id, created_at DESC`
- `to_user_id, created_at DESC`
- `license_id`
- `idempotency_key` (UNIQUE)

---

## 5. AI-Related Entities

### 5.1 Article Chunks (RAG Embeddings)

Powers both writer-facing RAG and magazine-facing Portfolio Insights.

```
id            UUID PK
article_id    UUID NOT NULL FK → articles.id ON DELETE CASCADE
chunk_index   INTEGER NOT NULL                    -- order within article
content       TEXT NOT NULL                        -- raw text of the chunk (paragraph)
embedding     VECTOR(1024) NOT NULL                -- Cohere embed-multilingual-v3.0
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
UNIQUE (article_id, chunk_index)
```

Indexes:
- `article_id`
- HNSW vector index on `embedding` (for fast cosine similarity)

---

### 5.2 AI Interactions

```
id           UUID PK
user_id      UUID NOT NULL FK → users.id
article_id   UUID NULL FK → articles.id
action_type  ENUM('chat', 'inline_reformulate', 'inline_shorten', 'inline_expand',
                  'inline_simplify', 'inline_improve', 'voice_transcribe',
                  'portfolio_insight')
input_text   TEXT
output_text  TEXT
tokens_used  INTEGER NOT NULL
model        VARCHAR(50)                           -- provider/model used
created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `user_id, created_at DESC`
- `article_id`

---

### 5.3 User AI Memory

Structured (not blob JSON) for queryability.

```
id                   UUID PK
user_id              UUID NOT NULL FK → users.id UNIQUE
tone_preferences     JSONB                        -- { formality, energy, persona }
style_examples       JSONB                        -- array of representative excerpts
vocabulary_patterns  JSONB                        -- common terms, phrasing patterns
topics               JSONB                        -- domains the writer covers
updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
```

---

### 5.4 Portfolio Insights Cache

```
id                  UUID PK
writer_id           UUID NOT NULL FK → users.id UNIQUE
voice_summary       TEXT
topic_expertise     JSONB                         -- ordered list
consistency_score   INTEGER                       -- 0-100
suggested_use_cases JSONB
strengths_gaps      TEXT
generated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
expires_at          TIMESTAMPTZ NOT NULL          -- generated_at + 24h
```

Indexes:
- `writer_id` (UNIQUE)
- `expires_at`

---

## 6. Analytics Entities

### 6.1 Analytics Events (Raw)

Append-only event log.

```
id            UUID PK
event_type    ENUM('view', 'scroll', 'time_on_page', 'like', 'comment', 'repost')
article_id    UUID NULL FK → articles.id
viewer_id     UUID NULL FK → users.id              -- nullable for guests
metadata      JSONB                                 -- event-specific fields
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `(article_id, created_at)`
- `(viewer_id, created_at)`
- `event_type`

Old events (>90 days) can be archived.

---

### 6.2 Article Metrics (Per-Article Aggregation)

```
article_id          UUID PK FK → articles.id ON DELETE CASCADE
total_views         INTEGER NOT NULL DEFAULT 0
total_unique_views  INTEGER NOT NULL DEFAULT 0
total_likes         INTEGER NOT NULL DEFAULT 0
total_comments      INTEGER NOT NULL DEFAULT 0
total_reposts       INTEGER NOT NULL DEFAULT 0
avg_read_time_sec   FLOAT
completion_rate     FLOAT                            -- % reaching the end
engagement_rate     FLOAT                            -- % scrolling past 75%
paragraph_dropoff   JSONB                            -- [{idx: 0, dropoff: 0.1}, ...]
last_aggregated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
```

---

### 6.3 Writer Audience Metrics (Per-Writer Rollup — Magazine-Facing)

```
writer_id              UUID PK FK → users.id ON DELETE CASCADE
total_unique_readers   INTEGER NOT NULL DEFAULT 0
returning_reader_rate  FLOAT
top_countries          JSONB                          -- [{country: "FR", pct: 0.35}, ...]
device_split           JSONB                          -- {mobile, desktop, tablet}
avg_engaged_minutes    FLOAT
window_days            INTEGER NOT NULL DEFAULT 30   -- rolling window
last_aggregated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
```

---

### 6.4 Writer Content Metrics (Per-Writer Rollup)

```
writer_id            UUID PK FK → users.id ON DELETE CASCADE
total_published      INTEGER NOT NULL DEFAULT 0
topic_distribution   JSONB                            -- [{topic, pct}]
posting_frequency    FLOAT                            -- articles per month
posting_consistency  FLOAT                            -- coefficient of variation (lower = more consistent)
avg_article_length   INTEGER                          -- word count
top_tags             JSONB                            -- [{tag, count}]
last_aggregated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
```

---

### 6.5 Writer Quality Metrics (Per-Writer Rollup)

```
writer_id          UUID PK FK → users.id ON DELETE CASCADE
engagement_rate    FLOAT
completion_rate    FLOAT
repost_rate        FLOAT
comment_depth      FLOAT                              -- avg replies per article
retention_curve    JSONB                              -- [25%, 50%, 75%, 100% retention values]
last_aggregated_at TIMESTAMPTZ NOT NULL DEFAULT now()
```

---

## 7. Notification System

```
id          UUID PK
user_id     UUID NOT NULL FK → users.id
type        ENUM('follow', 'like', 'comment', 'reply', 'article_licensed',
                 'license_earned', 'wallet_credited')
data        JSONB                                     -- type-specific payload (actor, target, etc.)
is_read     BOOLEAN NOT NULL DEFAULT FALSE
created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `(user_id, created_at DESC)`
- `(user_id, is_read) WHERE is_read = FALSE`

---

## 8. Moderation System

### 8.1 Reports

```
id            UUID PK
reporter_id   UUID NOT NULL FK → users.id
target_type   ENUM('article', 'user', 'comment')
target_id     UUID NOT NULL
reason        TEXT
status        ENUM('pending', 'reviewed', 'resolved', 'dismissed') NOT NULL DEFAULT 'pending'
admin_notes   TEXT
resolved_by   UUID NULL FK → users.id
resolved_at   TIMESTAMPTZ NULL
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `(target_type, target_id)`
- `(status, created_at)`

---

## 9. Relationships Summary

- A user (personal) can create many articles
- A user (magazine) extends users via `magazine_profiles`
- Articles can be tagged (many-to-many) and chunked (one-to-many for RAG)
- Magazines can license many articles (`article_licenses`); writers can have many licenses on many articles (non-exclusive)
- Each license generates 2-3 transaction rows (license_purchase, writer_payout, platform_fee)
- Wallet balance on users is the running sum of completed transactions to/from that user
- Writers have one row each in the three metrics rollup tables (audience / content / quality)
- All deletes on `articles`, `comments`, `users` are soft (set `deleted_at`); hard cascades only on owned children (chunks, metrics)

---

## 10. Constraints and Integrity

- Foreign keys enforced everywhere
- Unique constraints on duplicate-sensitive relations (likes, follows, reposts, licenses)
- Wallet balance updates always go through a transaction row (no direct UPDATE on `users.wallet_balance`)
- License purchases run inside a database transaction: validate balance → debit magazine → credit writer → record license → record transactions
- Idempotency keys on transactions prevent double-charging

---

## 11. Performance Considerations

- Index every FK + every WHERE-clause field
- Partial indexes on `deleted_at IS NULL` for soft-deleted tables
- HNSW vector index on `article_chunks.embedding`
- GIN index on `articles.content_search` for full-text search
- Aggregated metrics tables denormalized for fast dashboard reads (single-row lookups)
- Pagination via cursor (created_at DESC, id) on feed and notifications

---

## 12. Future Extensions

- Audit log table for sensitive admin actions
- Subscription history table (when premium becomes Stripe-integrated)
- Saved searches for magazines (alerts on new writers matching criteria)
- Reader bookmarks
- Writer collaborations (multi-author articles)

---

## Summary

The schema supports:

- Two-sided marketplace (personal users + magazines, with article licensing transactions)
- RAG-powered AI for both writers and magazines
- Decision-support analytics with per-writer rollups for fast magazine dashboards
- Strong consistency on financial movements (wallet + transactions ledger)
- Moderation, soft deletes, and audit-ready data integrity

It provides a foundation that can carry the platform from PFE demo to production without schema rewrites.
