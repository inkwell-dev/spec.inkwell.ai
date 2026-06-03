# 📄 02 - Features Specification

---

## 1. 🧠 Overview

This document defines all functional features of the Inkwell platform, including:

- Content creation and management
- AI-assisted writing capabilities
- Social interactions
- Analytics (writer-facing + magazine-facing)
- Licensing marketplace (magazine accounts, listings, transactions)
- Access control and monetization

Features are categorized into:
- **MVP (Minimum Viable Product)**
- **Post-MVP (Future Enhancements)**

---

## 2. ✍️ Content Creation & Management

### 2.1 Article Editor

The platform uses **TipTap (ProseMirror)** as the rich text editor. Article content is stored as **TipTap JSON** to enable paragraph-level AI manipulation and analytics.

#### Fields:
- Title
- Slug (auto-generated from title, unique, indexed — used for SEO-friendly URLs `/articles/[slug]`)
- Thumbnail (image upload)
- Excerpt (short summary)
- Content (TipTap JSON)
- Tags (multi-select, MVP feature — used for discovery and filtering)

#### Features:
- Text formatting (bold, italic, headings, lists, quotes, code blocks)
- Image embedding within content (uploaded to MinIO/S3)
- Structured content blocks (each paragraph is a node — enables paragraph-level analytics and selection-based AI editing)

---

### 2.2 Draft System

- Articles are automatically saved as drafts during editing
- No manual save required
- Drafts persist across sessions

---

### 2.3 Publishing Workflow

Users can:
- Publish articles immediately
- Keep articles as drafts
- Update already published articles

---

### 2.4 Article Placement & Visibility

When publishing, a writer first chooses a **placement**:

| Placement | Audience | Description |
|-----------|----------|-------------|
| **Public** | Free/premium readers | Appears in the public feed. Subject to free/premium visibility rules below. |
| **Marketplace** | Magazine subscribers only | Not listed in the public feed or on the writer's public profile. Accessible only to magazines with an active subscription. |

For **public** articles, a visibility level further restricts access:

- **Free Access** → Accessible by all authenticated users
- **Premium Access** → Accessible only by premium-plan users (requires writer eligibility — see section 4.5.2)

> Articles are always publicly listed in the feed by title/excerpt, but full access requires authentication. Magazine accounts can access any article they have fully purchased regardless of its original visibility.

#### Placement Rules
- Placement is chosen at publish time and defaults to **public**.
- **Marketplace → Public** switch is allowed at any time (writer abandons the sale and makes the article public).
- **Public → Marketplace** switch is **blocked** (an article that has already been read by the public audience has no marketplace exclusivity value).

---

### 2.4.1 Marketplace Article State

For articles with `placement = marketplace`, the following state applies:

- `price` — writer-set price in platform credits (required)
- `preview_price` — derived automatically as 10% of price (platform constant, not editable)
- No free/premium subdivision — marketplace articles have a single access path through the magazine purchase flow

State per magazine–article pair:
- **Not previewed** — magazine has not unlocked this article yet
- **Previewed** — magazine paid the preview fee (10%) and can read the full article; credits are held toward the purchase
- **Purchased** — magazine paid the remaining 90%; article is in their library with republish rights

---

### 2.5 Soft Deletes

Articles, comments, and users use **soft deletes** (`deleted_at` timestamp). Deleted content is hidden from public views but retained for:
- Moderation audit trails
- Recovery on user request
- Linking integrity (e.g., licensed articles cannot be hard-deleted while licenses exist)

---

### 2.6 Media Handling

- Users can upload images from their device
- Images are stored in **MinIO** (S3-compatible object storage)
- Images can be used as:
  - Thumbnail
  - Inline content within the editor
- Uploaded via signed POST URLs to avoid routing media through the backend

---

### 2.7 Discovery: Tags & Search

- **Tags** — multi-select, MVP feature. Articles can have multiple tags. Feed supports tag filtering.
- **Search** — MVP feature combining:
  - Postgres full-text search (`tsvector`) over title + excerpt + content
  - Semantic search via pgvector (queries embedded, matched against article chunks)
  - **Reciprocal Rank Fusion (RRF)** merges lexical and semantic result sets: `score = Σ 1/(k + rank_i)` with k=60
  - Hybrid ranking returns relevant results for both keyword and conceptual queries

---

## 3. 🤖 AI-Assisted Writing

### 3.1 AI Chat Assistant

A contextual AI assistant integrated into the editor.

#### Capabilities:
- Generate content based on prompts
- Answer questions related to the article
- Suggest improvements

#### Behavior:
- Adaptive tone based on user style
- Can ask clarifying questions depending on confidence level

---

### 3.2 Voice-to-Article Generation

#### Flow:
1. User records voice input
2. Audio is transcribed to text
3. AI processes the text
4. A structured article draft is generated

#### Notes:
- Non-real-time processing (MVP)
- Output includes:
  - Title suggestions
  - Sectioned content

---

### 3.3 Inline Editing Popup (Core Feature)

Triggered when a user selects text inside the editor.

#### Available Actions:
- Reformulate
- Shorten
- Expand
- Simplify
- Improve engagement

#### Behavior:
- AI processes selected text with article context
- Returns a refined version
- User can:
  - Replace original text
  - Insert result below

---

### 3.4 AI Usage Limits

- AI usage is controlled via **token-based limits**
- Each user has:
  - Daily token quota
- Tokens are consumed per AI action
- Users can purchase additional tokens (simulated)

---

### 3.5 AI Memory

- AI stores user-specific writing preferences with a structured schema:
  - `tone_preferences` — preferred voice (formal, casual, etc.)
  - `style_examples` — extracted style patterns from the writer's articles
  - `vocabulary_patterns` — recurring terms and phrasing
  - `topics` — domains the writer covers
- Memory is applied across all articles of the user
- Built incrementally from the user's published corpus (RAG ingestion in Phase 4)

---

### 3.6 Portfolio Insights for Magazines (Second RAG Use Case)

When a magazine views a writer's profile, AI generates a structured evaluation report:

- **Voice summary** — short description of the writer's tone and style
- **Topic expertise** — primary domains based on published content
- **Style consistency** — quantitative score (0–100) across articles
- **Suggested use-cases** — what kind of magazine the writer would fit
- **Notable strengths and gaps**

Powered by RAG over the writer's published corpus (same pgvector chunks already used for writer-facing AI). Results are cached per writer and refreshed on each new publication.

---

## 4. 📊 Analytics System

Analytics serves two distinct audiences with two distinct surfaces.

### 4.1 Writer-Facing Analytics (Self-Improvement)

Writers can access metrics about their own content:

- Total views per article
- Average read time
- Scroll depth distribution (paragraph-level drop-off)
- Engagement rate (deep readers / total views)
- Likes, comments, reposts
- AI feedback on weak sections (long paragraphs, weak introductions, etc.)

---

### 4.2 Magazine-Facing Analytics (Buyer Decision Support)

When a magazine views a writer's profile, they see a **writer evaluation dashboard** with four categories:

#### Audience Analytics
- Total unique readers
- Returning vs new reader ratio
- Geographic distribution (country-level)
- Average engaged minutes per reader

#### Content Analytics
- Topic distribution (from tags + AI inference)
- Posting frequency / consistency over time
- Average article length
- Publication cadence (articles per month)

#### Quality Signals
- Engagement rate per view (% who scroll past 75%)
- Repost rate
- Comment depth (avg replies per article)
- Completion rate (% who reach the end)
- Retention curve (read-completion by paragraph)

#### AI Portfolio Insights
- See section 3.6 — AI-generated qualitative report

All metrics are computed by background aggregation jobs (see [`7-analytics-model.md`](./7-analytics-model.md)) and cached for fast dashboard load.

---

### 4.3 Event Capture

Both surfaces share the same event pipeline:

- View event on article load
- Scroll events via `IntersectionObserver` (per paragraph)
- Time-on-page via `visibilitychange` + `beforeunload`
- Like / repost / comment events
- License purchase events (transactional, separate pipeline)

---

## 4.5 📦 Marketplace

The marketplace is Inkwell's defining commercial layer — a gated space where eligible writers sell exclusive content to magazine subscribers.

### 4.5.1 Magazine Subscription

- Self-signup, instant (no admin approval in MVP)
- Distinct `account_type` = `magazine`
- **A subscription is mandatory** before any marketplace access is granted — no free magazine tier
- Subscription includes a **monthly credit budget** (e.g. 500 credits/month, platform-configurable)
- Profile fields: name, logo, website, description, contact email
- Magazines can top up credits manually if the monthly budget is exhausted (simulated payment)

---

### 4.5.2 Writer Eligibility Gate

Before a writer can list articles on the marketplace or create premium articles, they must reach:

- **5,000 lifetime unique readers** across all their published public articles
- **1,000 lifetime reactions** (likes + comments) across all their published public articles

Rules:
- The threshold is computed as a **lifetime sum** — once reached, it stays unlocked permanently
- Only **public** articles contribute to the count (marketplace articles are magazine-only and do not generate reader/reaction events from the public)
- **Admin bypass** — admins can manually grant marketplace eligibility for demo seeding or promotional purposes
- Writers can see their progress toward the threshold on their dashboard (e.g. "3,200 / 5,000 readers · 780 / 1,000 reactions")

---

### 4.5.3 Marketplace Browsing (Magazine Side)

Magazines have a dedicated discovery interface (requires active subscription):

- Browse all eligible writers (paginated, filterable by topic/tag)
- Search writers by name, topic expertise, or keyword
- Sort by engagement, posting frequency, or topic relevance
- Click into any writer's profile → see full evaluation dashboard (section 4.2) and Portfolio Insights (section 3.6)
- View a writer's marketplace-listed articles with titles, excerpts, and prices
- See per-writer stats (per-article stats deferred to post-MVP)

---

### 4.5.4 Three-Stage Article Flow (Magazine Side)

Magazines interact with marketplace articles through three stages:

#### Stage 1 — Free Browse
- Visible without spending credits
- What magazines see: title, excerpt, writer profile stats, price

#### Stage 2 — Preview Unlock (10% of price)
- Magazine clicks "Preview article" → confirmation modal shows preview price (10%)
- Credits debited from magazine credit balance (validated server-side)
- Magazine can now read the full article
- Writer receives payout: `preview_credits − platform_fee`
- **One-time per magazine**: once unlocked, the magazine can re-read the article anytime without paying again
- Preview is tracked per `(article_id, magazine_id)` pair

#### Stage 3 — Full Purchase (remaining 90%)
- After previewing, magazine clicks "Purchase article" → confirmation modal shows remaining amount (90% of original price)
- Credits debited for the remaining amount (total paid = 100% of price across both stages)
- Article added to magazine's **curated library** with republish rights
- Writer receives payout: `purchase_credits − platform_fee`
- Article gets a "In [Magazine]'s library" attribution badge on the writer's profile

If a magazine skips preview and goes straight to purchase, they pay 100% in one step (no credit for a prior preview).

---

### 4.5.5 Magazine Library

- Each magazine has a library page showing all articles they have **fully purchased**
- Library is the magazine's content portfolio — analogous to a writer's profile for readers
- Articles in library link back to the original writer (attribution preserved)
- Previewed-only articles are not in the library

---

### 4.5.6 Writer Earnings

- Writers see an **Earnings** section in their dashboard:
  - Total earnings (lifetime, including preview payouts + purchase payouts)
  - Recent transactions (previews and purchases separately itemized)
  - Articles ranked by total revenue
  - Earnings balance + simulated withdraw button

---

### 4.5.7 Transaction Safety

- All credit movements are atomic database transactions (debit magazine + credit writer + record purchase in single tx)
- Insufficient credit balance → graceful rejection with clear UX and prompt to top up
- All transactions logged with idempotency keys to prevent double-charging on retry
- Preview fees are tracked and subtracted from final purchase cost at purchase time (server-computed, never trusted from client)

---

## 5. 👤 User & Social Features

### 5.1 Account Model

See [`1-product-overview.md`](./1-product-overview.md) section 5 for the full account model. Summary:

- **account_type**: `personal` | `magazine`
- **role** (personal only): `reader` | `writer` | `admin`
- **plan** (personal only): `free` | `premium`

---

### 5.2 Profile System

Each **personal** user profile contains:
- `username` (unique, used in profile URL `/u/[username]`)
- Display name, bio, avatar
- Published articles (paginated)
- Aggregate stats (total views, likes, followers)
- Earnings section (for writers — visible only to themselves)

Each **magazine** profile contains:
- Magazine name, logo, website, description
- Curated library of licensed articles
- Wallet balance (visible only to the magazine itself)

---

### 5.3 Follow System

- Users can follow writers
- Notifications are triggered when:
  - A user gains a new follower

---

### 5.4 Likes / Reactions

- Users can like articles
- Like count is visible publicly

---

### 5.5 Comments System

#### Type:
- Threaded comments (nested replies)

#### Features:
- Add comment
- Reply to comment
- Delete own comment

---

### 5.6 Repost System

- Users can repost articles to their profile or feed
- Reposts increase article visibility

---

## 6. 🔔 Notifications System

Notifications include:

- New follower
- New like on article
- New comment on article

---

## 7. 🔐 Access Control & Membership

### 7.1 Authentication

- Email/password login
- Google OAuth login

---

### 7.2 Plans (Personal accounts only)

| Plan | Reading | Writing |
|------|---------|---------|
| Free | Free articles only | Can write, no AI |
| Premium | All articles | Full AI with token quota |

Plan is orthogonal to role. A free-plan user can be a writer (just without AI). A premium-plan user can choose not to write.

---

### 7.3 Magazine Accounts

- Subscription-based access (no free magazine tier)
- Subscription unlocks: marketplace browsing, writer evaluation dashboards, Portfolio Insights, and the ability to preview/purchase marketplace articles
- Can read any marketplace article they have **previewed** (preview unlock) or **purchased** (full purchase)
- Cannot create or publish original articles (magazines source content, they do not write)

---

### 7.4 Content Access Rules

| Actor | Public free articles | Public premium articles | Marketplace articles |
|-------|---------------------|------------------------|----------------------|
| Guest | Title/excerpt only | Title/excerpt only | Not visible |
| Free reader | Full access | Blocked (upgrade prompt) | Not visible |
| Premium reader | Full access | Full access | Not visible |
| Magazine (no sub) | No marketplace access at all | No marketplace access at all | Not visible |
| Magazine (active sub) | Full access | Full access | Browse free; preview unlock with credits; full content after purchase |

---

## 8. ⚠️ Moderation & Reporting

### 8.1 Reporting System

Users can:
- Report articles
- Report other users

---

### 8.2 Admin Capabilities

Admins can:
- Delete articles
- Ban users
- Review reports

---

## 9. 🚀 Post-MVP Features

The following features are planned for future iterations:

### 9.1 Advanced AI Features
- Style learning and personalization
- Multi-language content generation

---

### 9.2 Collaboration
- Multiple writers per article
- Shared editing

---

### 9.3 Version Control
- Article history tracking
- Restore previous versions

---

### 9.4 Advanced Analytics
- Heatmaps (visual engagement)
- Drop-off visualization
- AI-driven optimization suggestions

---

## ✅ Summary

The feature set combines:
- A powerful writing system
- Deep AI integration
- Social and engagement features
- Data-driven analytics

to create a complete, modern content platform.
