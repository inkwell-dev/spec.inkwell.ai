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
id                           UUID PK
account_type                 ENUM('personal', 'magazine')
email                        VARCHAR(255) UNIQUE NOT NULL
username                     VARCHAR(50)  UNIQUE NOT NULL          -- for /u/[username] URLs
password_hash                VARCHAR(255) NULL                     -- nullable for OAuth-only
provider                     ENUM('local', 'google')
role                         ENUM('reader', 'writer', 'admin')     -- personal accounts only
plan                         ENUM('free', 'premium')                -- personal accounts only
name                         VARCHAR(100)
bio                          TEXT
avatar_url                   VARCHAR(500)
earnings_balance             INTEGER NOT NULL DEFAULT 0            -- writer payouts (personal accounts only)
is_marketplace_eligible      BOOLEAN NOT NULL DEFAULT FALSE        -- personal writer accounts only
marketplace_eligible_at      TIMESTAMPTZ NULL                      -- when threshold was first crossed
marketplace_eligible_source  ENUM('threshold', 'admin_grant') NULL
ai_tokens_remaining          INTEGER NOT NULL DEFAULT 0            -- daily AI quota
ai_tokens_reset_at           TIMESTAMPTZ
last_login_at                TIMESTAMPTZ
created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
deleted_at                   TIMESTAMPTZ NULL                       -- soft delete
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
id                       UUID PK, FK → users.id ON DELETE CASCADE
display_name             VARCHAR(100) NOT NULL                     -- shown on profile
slug                     VARCHAR(100) UNIQUE NOT NULL              -- /m/[slug] URL
logo_url                 VARCHAR(500)
website_url              VARCHAR(500)
description              TEXT
contact_email            VARCHAR(255)
subscription_status      ENUM('active', 'past_due', 'cancelled') NOT NULL DEFAULT 'cancelled'
subscription_tier        VARCHAR(50) NULL                          -- plan name/slug (MVP: single tier)
subscription_started_at  TIMESTAMPTZ NULL
subscription_renewed_at  TIMESTAMPTZ NULL                          -- last successful renewal
subscription_expires_at  TIMESTAMPTZ NULL                          -- access end if not renewed
credit_balance           INTEGER NOT NULL DEFAULT 0               -- current spendable credits
monthly_credit_allowance INTEGER NOT NULL DEFAULT 500             -- credits granted per renewal cycle
created_at               TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at               TIMESTAMPTZ NOT NULL DEFAULT now()
```

Constraints:
- Marketplace access requires `subscription_status = 'active'`
- `credit_balance` is always updated through a transaction row (never directly)

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
status           ENUM('draft', 'published') NOT NULL DEFAULT 'draft'
placement        ENUM('public', 'marketplace') NOT NULL DEFAULT 'public'
visibility       ENUM('free', 'premium') NULL             -- only applies when placement = 'public'; NULL for marketplace articles
marketplace_price INTEGER NULL                            -- platform credits; required when placement = 'marketplace'
read_time       INTEGER                                    -- estimated minutes
word_count      INTEGER
created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
published_at    TIMESTAMPTZ NULL
deleted_at      TIMESTAMPTZ NULL
```

Constraints:
- If `placement = 'marketplace'` then `marketplace_price > 0` and `visibility IS NULL`
- If `placement = 'public'` then `visibility IS NOT NULL` and `marketplace_price IS NULL`
- Writer must have `is_marketplace_eligible = TRUE` to publish with `placement = 'marketplace'` or `visibility = 'premium'`
- `slug` auto-generated from title with collision suffix
- `placement` can change from `'marketplace'` → `'public'` (one-way; reverse is blocked by application layer)

Indexes:
- `author_id`
- `slug` (UNIQUE)
- `status`
- `placement`
- `visibility`
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

### 4.1 Article Purchases

Records each stage of a magazine's interaction with a marketplace article (preview unlock and/or full purchase).

```
id                UUID PK
article_id        UUID NOT NULL FK → articles.id
magazine_id       UUID NOT NULL FK → users.id        -- account_type = magazine
stage             ENUM('preview_unlock', 'full_purchase') NOT NULL
credits_paid      INTEGER NOT NULL                    -- credits deducted at this stage
platform_fee      INTEGER NOT NULL                    -- fee withheld from writer payout
writer_payout     INTEGER NOT NULL                    -- credits_paid - platform_fee
parent_purchase_id UUID NULL FK → article_purchases.id  -- for 'full_purchase' rows: points to the prior 'preview_unlock' row; NULL for direct purchases (no prior preview)
purchased_at      TIMESTAMPTZ NOT NULL DEFAULT now()
UNIQUE (article_id, magazine_id, stage)               -- each magazine pays for each stage once
```

Constraints:
- Writers cannot purchase their own articles (app-layer guard)
- Article must have `placement = 'marketplace'` and `status = 'published'` at time of purchase
- `full_purchase.credits_paid = article.marketplace_price − (preview_unlock.credits_paid if parent_purchase_id IS NOT NULL else 0)`
- `parent_purchase_id` must reference a row with `stage = 'preview_unlock'` for the same `(article_id, magazine_id)`

Indexes:
- `article_id`
- `magazine_id`
- `(article_id, magazine_id)` (for per-magazine article state lookup)
- `purchased_at DESC` (for recent purchases query)

---

### 4.2 Transactions

Atomic financial ledger. Every credit movement (debit or credit) creates one transaction row.

```
id               UUID PK
type             ENUM(
                   'subscription_charge',    -- magazine pays for subscription
                   'monthly_credit_grant',   -- monthly credits issued to magazine
                   'credit_topup',           -- magazine manually tops up credits
                   'preview_unlock',         -- magazine debited for article preview
                   'article_full_purchase',  -- magazine debited for full article purchase
                   'writer_payout',          -- writer credited for preview or purchase
                   'platform_fee',           -- platform fee withheld
                   'refund'
                 )
amount           INTEGER NOT NULL                 -- absolute value; direction determined by type
from_user_id     UUID NULL FK → users.id          -- nullable for subscription/grant originating externally
to_user_id       UUID NULL FK → users.id          -- nullable for platform-fee sinks
article_id       UUID NULL FK → articles.id       -- set for preview/purchase/payout transactions
purchase_id      UUID NULL FK → article_purchases.id  -- replaces license_id
idempotency_key  VARCHAR(100) UNIQUE              -- prevents double-charging on retry
status           ENUM('pending', 'completed', 'failed', 'refunded') NOT NULL
metadata         JSONB                             -- provider response, error details, etc.
created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `from_user_id, created_at DESC`
- `to_user_id, created_at DESC`
- `purchase_id`
- `idempotency_key` (UNIQUE)

---

### 4.3 Magazine Subscriptions

Renewal history and dunning audit trail. One row per billing cycle per magazine.

```
id              UUID PK
magazine_id     UUID NOT NULL FK → users.id ON DELETE CASCADE
status          ENUM('active', 'past_due', 'cancelled', 'refunded') NOT NULL
credits_granted INTEGER NOT NULL                  -- credits issued at start of this cycle
started_at      TIMESTAMPTZ NOT NULL
expires_at      TIMESTAMPTZ NOT NULL
renewed_from_id UUID NULL FK → magazine_subscriptions.id  -- previous cycle (NULL for first)
created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `magazine_id, started_at DESC`
- `expires_at` (for renewal cron job)

---

### 4.4 Writer Eligibility Audit Log

Records every eligibility state change — both auto-triggered (threshold crossed) and admin grants.

```
id           UUID PK
writer_id    UUID NOT NULL FK → users.id
source       ENUM('threshold', 'admin_grant') NOT NULL
granted_by   UUID NULL FK → users.id             -- admin user_id; NULL for threshold-based
reason       TEXT NULL                            -- optional admin note
readers_at   INTEGER NULL                         -- snapshot of unique reader count at grant time
reactions_at INTEGER NULL                         -- snapshot of reaction count at grant time
created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
```

Indexes:
- `writer_id`
- `created_at DESC`

---

## 5. AI-Related Entities

### 5.1 Article Chunks (RAG Embeddings)

Powers both writer-facing RAG and magazine-facing Portfolio Insights.

```
id            UUID PK
article_id    UUID NOT NULL FK → articles.id ON DELETE CASCADE
chunk_index   INTEGER NOT NULL                    -- order within article
content       TEXT NOT NULL                        -- raw text of the chunk (paragraph)
embedding     VECTOR(1536) NOT NULL                -- OpenAI text-embedding-3-small
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
UNIQUE (article_id, chunk_index)
```

Indexes:
- `article_id`
- HNSW vector index on `embedding` (for fast cosine similarity)

Lifecycle:
- Chunks are created only for **published** articles (not drafts)
- On article **update/re-publish**: all existing chunks for the article are **deleted** then re-created (the unique constraint on `(article_id, chunk_index)` requires this)
- On article **soft delete**: chunks cascade-delete via FK
- On chunk refresh: the writer's `portfolio_insights` cache is also invalidated (deleted)

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
type        ENUM('follow', 'like', 'comment', 'reply',
                 'article_previewed',    -- magazine previewed the writer's article
                 'article_purchased',    -- magazine fully purchased the writer's article
                 'earnings_credited',    -- writer earnings_balance increased
                 'subscription_renewed') -- magazine's own subscription renewed
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
- A user (magazine) extends users via `magazine_profiles`; magazine subscription state lives in `magazine_profiles` (snapshot) and `magazine_subscriptions` (history)
- Articles can be tagged (many-to-many) and chunked (one-to-many for RAG)
- Articles have `placement`: public articles are in the reader feed; marketplace articles are visible only to subscribed magazines
- Magazines interact with marketplace articles through `article_purchases` (up to 2 rows per magazine–article pair: `preview_unlock` then `full_purchase`)
- A `full_purchase` row links back to its `preview_unlock` via `parent_purchase_id`; direct purchases (no prior preview) have `parent_purchase_id = NULL`
- Each purchase stage generates 2 transaction rows (magazine debit + writer payout); platform fee is embedded in the payout calculation
- `earnings_balance` on personal users is the running sum of completed `writer_payout` transactions to that user
- `credit_balance` on magazine profiles is updated only through transaction rows (`monthly_credit_grant`, `credit_topup`, `preview_unlock` debit, `article_full_purchase` debit)
- Writer eligibility (`is_marketplace_eligible`) is set by the analytics aggregator when lifetime thresholds are crossed, or by an admin action recorded in `writer_eligibility_audit_log`
- Writers have one row each in the three metrics rollup tables (audience / content / quality)
- All deletes on `articles`, `comments`, `users` are soft (set `deleted_at`); hard cascades only on owned children (chunks, metrics)

---

## 10. Constraints and Integrity

- Foreign keys enforced everywhere
- Unique constraints on duplicate-sensitive relations (likes, follows, reposts, purchases per stage)
- `earnings_balance` and `credit_balance` updates always go through a transaction row (no direct UPDATE on balance columns)
- Preview unlock runs inside a database transaction: validate credit balance → debit magazine credits → credit writer earnings → insert purchase row → insert transaction rows
- Full purchase runs inside a database transaction: validate credit balance → look up prior preview row → compute remaining amount → debit magazine → credit writer → insert purchase row with `parent_purchase_id` → insert transaction rows
- Subscription activation runs inside a database transaction: insert `magazine_subscriptions` row → update `magazine_profiles` snapshot → insert `monthly_credit_grant` transaction → update `credit_balance`
- Idempotency keys on transactions prevent double-charging
- Application layer enforces `placement` one-way switch (marketplace → public only)

### 10.1 Ledger Integrity & Concurrency

`earnings_balance` (on `users`) and `credit_balance` (on `magazine_profiles`) are **denormalized snapshots** that must always equal the sum of their corresponding `transactions` ledger entries. This creates a dual-source-of-truth risk that must be managed explicitly.

#### Row Locking

All purchase and credit operations must use **`SELECT ... FOR UPDATE`** on the balance-owning row before reading the balance:

```
-- Inside the purchase transaction:
SELECT credit_balance FROM magazine_profiles WHERE id = $magazine_id FOR UPDATE;
-- Now safe to validate, debit, and insert transaction rows
```

Without row-level locking, two concurrent purchases by the same magazine can read the same `credit_balance` and both succeed — double-spending credits.

#### Invariants

The following invariants must always hold:

1. `users.earnings_balance == SUM(amount) FROM transactions WHERE to_user_id = user_id AND type = 'writer_payout' AND status = 'completed'`
2. `magazine_profiles.credit_balance == SUM(credits_in) - SUM(credits_out)` where:
   - credits_in = `monthly_credit_grant` + `credit_topup` transactions
   - credits_out = `preview_unlock` + `article_full_purchase` transactions

#### Reconciliation

A `reconcile-balances` background job (run nightly or on-demand) asserts these invariants for every user and magazine. Any drift is logged as a critical alert. This serves both as a safety net and as a defense-ready demonstration of engineering rigor.

#### Ledger Invariant Tests

Automated tests must verify these invariants after every purchase, preview, subscription grant, and topup operation. These are the first tests written in the project.

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
