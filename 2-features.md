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

### 2.4 Article Visibility

Each article must have a visibility level:

- **Free Access** → Accessible by all authenticated users
- **Premium Access** → Accessible only by premium-plan users

> Note: Articles are always publicly listed in the feed, but full access requires authentication. Magazine accounts can access any article they have licensed regardless of visibility.

---

### 2.4.1 Article Licensing State

Independent of free/premium visibility, every published article carries a **licensing state**:

- `not_listed` (default) — article is read-only, not available for purchase
- `listed` — article is available for licensing at a fixed price set by the writer
- `licensed` — at least one magazine has licensed the article (writer retains the ability to keep it listed for additional licenses)

Writers can toggle listing state and price from their article management dashboard.

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

## 4.5 📦 Licensing Marketplace

The marketplace is Inkwell's defining commercial layer.

### 4.5.1 Magazine Accounts

- Self-signup, instant (no admin approval in MVP)
- Distinct `account_type` = `magazine`
- Profile fields: name, logo, website, description, contact email
- Maintains a **wallet balance** in platform credits (simulated currency)
- Wallets can be topped up via simulated payment

---

### 4.5.2 Article Listings

- Writers mark a published article as **available for licensing** with a fixed price (set in platform credits)
- Can be toggled on/off
- Price is editable
- An article can be licensed by multiple magazines (non-exclusive)

---

### 4.5.3 Magazine Discovery & Browsing

Magazines have a dedicated discovery interface:

- Browse all writers (paginated, filterable by topic/tag)
- Search writers by name, topic expertise, or keyword
- Sort by engagement, posting frequency, or topic relevance
- Click into any writer's profile → see full evaluation dashboard (section 4.2) and Portfolio Insights (section 3.6)
- View a writer's listed articles + prices

---

### 4.5.4 License Purchase Flow

1. Magazine views a writer's listed article
2. Clicks "License this article" → confirmation modal showing price
3. Magazine confirms → wallet balance debited (validated server-side)
4. License record created (`article_licenses` table)
5. Article appears in magazine's **curated library** with a "Licensed by [Magazine]" badge on the writer's original page
6. Writer's wallet credited with the price (minus platform fee, configurable)
7. Notification sent to writer

---

### 4.5.5 Magazine Library

- Each magazine has a public library page showing all articles they have licensed
- Library is the magazine's "portfolio" — analogous to a writer's profile
- Articles in library link back to the original writer (attribution preserved)

---

### 4.5.6 Writer Earnings

- Writers see a **Earnings** section in their dashboard:
  - Total earnings (lifetime)
  - Recent license transactions
  - Articles ranked by license revenue
  - Wallet balance + simulated withdraw button

---

### 4.5.7 Transaction Safety

- All purchases are atomic database transactions (debit + credit + license record in single tx)
- Insufficient balance → graceful rejection with clear UX
- All transactions logged with idempotency keys to prevent double-charging on retry

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

- Wallet-based access (not free/premium tier)
- Can read any article they have licensed
- Cannot create or publish original articles (magazines license, they do not write)

---

### 7.4 Content Access Rules

- **Guests**: feed only, no full articles
- **Free plan**: free articles
- **Premium plan**: all articles
- **Magazines**: licensed articles unconditionally; free articles like any reader; premium-marked articles only if licensed

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
