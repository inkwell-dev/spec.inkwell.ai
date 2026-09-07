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

#### Who can still see a listing

"Not listed ... on the writer's public profile" is honoured from 2026-09-07, and
it was not honoured before: the profile listed every marketplace article, and
`GET /articles/:slug` then answered 404 to the reader who clicked it. A card that
leads nowhere is worse than no card.

Two viewers are exempt, and only two:

- **The author**, always, on their own profile. A writer's profile is also how
  they check what they currently have out for sale.
- **An administrator**, for the same reason the read gate lets them see
  everything: moderation cannot moderate what it cannot list.

A subscribed **magazine** gets no exemption. Marketplace browsing has its own
surface with its own filters (§4.5.3), and a profile that quietly showed
different articles to different buyers would be a second, undocumented
marketplace.

One profile surface is **not** covered by this rule, deliberately: the
**Reposted** tab (§5.6) still lists a marketplace article that somebody reposted
before reposting one was refused, and that tab is public. The rule above is about
the writer's *own shelf* — what they published — and a repost is a different
claim: it says an account amplified something, and it stays true. Filtering the
reposted list to match this rule would delete rows with the count agreeing, which
§5.6 explains at length.

> **Not yet built.** Once a magazine *publishes* an article it has licensed, the
> article returns to the writer's profile carrying an *in [Magazine]*
> attribution. That needs `articles.publisher_id`, which does not exist yet — see
> `docs/superpowers/specs/2026-09-06-magazine-licensing-design.md`, decision D4.
> Until then a sold listing is simply absent like any other.

#### Engagement on a listing

A marketplace listing is a private commercial offer, not a published article with
a smaller audience. **Liking, commenting on and reposting one are refused** — a
public like count, a public comment thread and amplification into someone's
followers' feed are all forms of publication, and none of them belong on
something that is being sold. The refusal is uniform: the author and
administrators are refused too, so a listing cannot acquire a thread with one
possible participant.

**Saving is not refused**, and the contrast is deliberate — see §5.8. A save is
private to the saver, and shortlisting candidates is exactly what a magazine does
while evaluating.

All three switch on the moment the article becomes public.

Engagement recorded *before* this rule existed is **preserved, not purged**. What
stops is **rendering**: no surface in the product draws a listing's like count,
comment thread, comment strip or engagement controls any more.

The underlying reads are deliberately left alone, so be precise about what that
means. `GET /articles/:id/like` and `GET /articles/:id/repost` still answer with
the historical counts to anyone holding the article's id, and the thread endpoint
still serves the historical conversation to the viewers who can read the article
— its author, an administrator, and a subscribed magazine (§5.5). Nothing was
hidden retroactively; the surfaces that displayed it were removed.

It also remains **removable by whoever created it**: un-liking, un-reposting and
deleting one's own comment all still work. Closing those would strand engagement
made under the old rule, which is a worse outcome than its being unreachable.
See §5.4, §5.5, §5.6 and §5.8.

#### Placement Rules
- Placement is chosen at publish time and defaults to **public**.
- **Marketplace → Public** switch is allowed at any time **until the article is
  sold** (writer abandons the sale and makes the article public). Once a magazine
  holds a full purchase the switch is refused: the buyer paid for exclusivity, and
  a writer who could make the article free afterwards would be selling something
  they can take back. Deleting a sold article is refused for the same reason —
  see §2.5.
  *(Corrected 2026-09-07. This rule previously said "at any time" with no
  exception, which was true of the code and incompatible with the exclusivity
  US-41 and §4.5 both promise.)*
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

**Since 2026-09-07 this state is no longer purely per-pair.** Exclusivity makes
*being purchased* a property of the **article**, not of a magazine–article pair:
once any magazine reaches **Purchased**, every other magazine is frozen wherever
it stands and can go no further. A magazine that had reached **Previewed** keeps
what it paid for — permanent reading access — and is simply refused at the
purchase step; it is **not** refunded, because the preview fee bought the read
and it still has the read. A magazine at **Not previewed** can no longer preview
at all, since paying 10% to evaluate an article nobody can buy would be selling
something with no value.

A sold article also leaves the marketplace browse (§4.5.3) rather than sitting
there advertising a purchase that would be refused.

---

### 2.5 Soft Deletes

Articles, comments, and users use **soft deletes** (`deleted_at` timestamp). Deleted content is hidden from public views but retained for:
- Moderation audit trails
- Recovery on user request
- Linking integrity (e.g., licensed articles cannot be hard-deleted while licenses exist)

**A sold article cannot be soft-deleted either, as of 2026-09-07.** The line above
has always covered *hard* deletes, but soft delete is what `DELETE /articles/:id`
actually performs — so until now the rule protected nothing a writer could
actually do. A writer who deletes an article a magazine has paid for is taking
back what was sold, so the delete is refused while any full purchase exists.
Administrative removal through the moderation queue (§8.2) is deliberately
**not** blocked: moderation authority overrides the commercial guarantee, because
the alternative is content that cannot be taken down because somebody bought it.

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

> **Descoped to post-MVP** in the 2026-07-26 re-baseline (see [`0-phase-plan.md`](./0-phase-plan.md) — Post-MVP Descope). Design kept below as future-work reference.

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
- View a writer's marketplace-listed articles with titles, excerpts, and prices — **excluding any already purchased by another magazine**, which leave the browse entirely rather than sitting there advertising a purchase that would be refused (§2.4 Placement Rules, FR-72)
- See per-writer stats (per-article stats deferred to post-MVP)

> **As built (2026-08-10).** The page is `/discover`, not `/marketplace` — the
> writer evaluation report already lives at `/discover/writers/[username]`, so
> the browse surface sits above it. `/marketplace` is reserved for the Phase 5
> browse of marketplace-listed *articles*.
>
> One deliberate departure from the paragraph above:
>
> - **"All eligible writers" is the default, not the only option.** The page
>   ships an *Eligible only* toggle, on by default. A strict filter renders an
>   empty page on any database where the seed has not run, which is the wrong
>   first impression of the feature — and the toggle also lets a magazine see the
>   writers who are *close* to eligible, which is information the strict view
>   destroys.
>
> **Retired 2026-08-24 — the subscription-gating departure.** A second note here
> said access was gated on account type "not on an active subscription", because
> "there is no subscription state to check yet". Phase 5 built that state:
> `POST /subscriptions/magazine` is what made the gate meaningful, and both routes
> in `discover.controller.ts` (:56, :80) now carry `subscription: true`, appending
> `SubscriptionGuard` to the same `@UseGuards` as the account-type check. The
> paragraph above — "requires active subscription" — is now simply true, which is
> why the note is gone rather than amended. Both guards must sit in **one**
> `@UseGuards`: split across two decorators, the second runs before the first has
> attached the user, and the subscription lookup dereferences `undefined`.
>
> Sorting is by engagement, unique readers, posting frequency, or account age.
> "Topic relevance" is not implemented: it needs the Phase 4 embeddings to mean
> anything more than the tag filter already provides.

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
- **No badge appears on the writer's profile while the article sits in the
  library.** The listing is simply absent from that profile, per §2.4.

> **Resolved contradiction (2026-09-07).** This stage used to promise an
> *"In [Magazine]'s library" attribution badge on the writer's profile*, while
> §2.4 said a marketplace article is not on that profile at all. Both could not
> hold, and the code honoured neither. §2.4 is the one that stands: a purchase
> puts the article in the library **unpublished**, and nothing about the writer's
> profile changes. The attribution arrives only when the magazine *publishes* the
> article, which is not built yet — see
> `docs/superpowers/specs/2026-09-06-magazine-licensing-design.md`, decision D4.

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

**Profile tabs.** A personal profile carries `Articles | Saved | Reposted |
About`; a magazine profile the same set with `Published articles` first and
`Writers` last. Two of those four are conditional:

- **Saved** (§5.8) renders **only on your own profile**. A visitor does not see
  it disabled — they do not see it at all, and cannot learn it exists. The list
  behind it is private.
- **Reposted** renders on **every** profile and is **public** — it lists what
  that account has reposted, newest repost first, to anyone at all including a
  signed-out visitor. The contrast with **Saved** is the point: a saved shelf is
  private, so its tab is conditionally rendered; a repost is public
  amplification, so there is nothing to withhold and nothing to hide the tab
  from. The two are treated differently because the two lists *are* different,
  not by oversight.

---

### 5.3 Follow System

- Users can follow writers
- Notifications are triggered when:
  - A user gains a new follower
- A profile's follower and following counts are public, and each opens the
  corresponding **list** of accounts — on any profile, not only one's own
- From either list a viewer can follow or unfollow a listed account. An account
  that already follows the viewer offers **Follow back** rather than Follow —
  the same action, a truer label
- Unfollowing asks for confirmation; following does not. The rule is that the
  destructive direction stops to ask: a follow is trivially undone and instant
  feedback is the point of the control, whereas an accidental unfollow silently
  drops a writer out of the reader's feed with nothing on screen afterwards to
  explain what happened

**Banned accounts are excluded from both the lists and the counts.** A
soft-deleted account's profile 404s, so listing it produces a row nobody can
open. The counts follow the same rule so that a badge and the list it links to
can never disagree — they sit one click apart, which is exactly where a
discrepancy would be noticed.

---

### 5.4 Likes / Reactions

- Users can like articles — from the article page **and** directly from a feed
  card, which shows whether the signed-in reader has already liked it
- Users can like comments and replies (see §5.5)
- Like count is visible publicly
- Only article likes count toward marketplace eligibility — see §9.3 of the
  analytics model for why comment likes are excluded
- **A marketplace listing cannot be liked** (§2.4). Likes recorded before that
  rule existed are kept, are no longer drawn on any card or article page, and
  remain **un-likeable** — that is, removable — by whoever made them. The count
  itself is still returned by `GET /articles/:id/like` to anyone holding the
  article's id; what went away is every surface that displayed it

---

### 5.5 Comments System

#### Type:
- Threaded comments (nested replies)

#### Features:
- Add comment
- Reply to comment
- Delete own comment
- Like a comment or a reply, and un-like it — the count is public, and the
  comment's author is notified of a like that is not their own

#### Not on a marketplace listing

A listing has no comment section at all (§2.4) — not on the article page and not
on a feed card, where both the recent-comments strip and the composer are absent.

The **thread endpoint follows the article's own access verdict** and adds nothing
to it. Before 2026-09-07 it had no access check whatever, so a signed-out visitor
could read the conversation about an article the reader gate answered 404 for —
the body was withheld and the discussion of it was not. Drafts leaked the same
way, from the moment a slug exists.

*Locked* is not *hidden*: a public premium article a reader cannot yet read still
returns its thread, because the article itself is publicly acknowledged and its
title, excerpt and comment count already are.

#### On a feed card

A feed card carries a **small comment section** of its own, so a reader can join
a conversation without leaving the feed:

- The last hour's comments on that article, **newest first, at most three**,
  shown **without any click**. A card with nothing recent shows nothing at all.
- A **composer** that opens from the card's Comment control. **Enter** submits;
  **Shift+Enter** inserts a newline.
- **Top-level comments only**, both in what it shows and what it posts. A reply
  rendered with no parent above it reads as an answer to a question that is not
  on screen, and threading needs the room the article page has. Replies and
  comment likes stay there.
- Consequently a card's comment **count** and its comment **strip** can disagree
  — "12 comments" above one line is correct. The count is how much discussion
  the article has; the strip is what was said here in the last hour.

---

### 5.6 Repost System

Reposting is a **plain toggle** — repost, un-repost. There is no quote-repost
and no comment attached to a repost.

**The public list.** Every account's reposts are enumerable from the **Reposted**
tab on its profile (§5.9), newest repost first, readable by anyone including
signed-out visitors.

The list **excludes** an article that is unpublished, soft-deleted, or whose
author has been banned — and, for a signed-in viewer, anything by an account
either party has blocked. A block between the viewer and the profile owner 404s
the profile, and the tab with it, rather than showing an empty list.

It deliberately **does not exclude** marketplace or premium articles. A repost is
amplification of an article that exists; whether the *body* is readable is the
article route's own access gate (§7.4) and a separate question. Filtering them
here would silently delete rows with the count agreeing, which presents as data
loss rather than as a filter bug.

**Followers see it.** An article reposted by an account you follow appears in
your **following feed**, attributed as *"X reposted"*, positioned by the
**repost's** time rather than the article's publication date — otherwise an old
article amplified a minute ago would land pages deep and the amplification would
achieve nothing. It appears **exactly once** however many accounts you follow
were involved, and the name shown is the most recent of them. A repost by an
account that is later banned surfaces nothing.

Marketplace articles are the one thing a repost does not pull into the following
feed: that feed is publicly readable articles by definition, and the marketplace
has its own surfaces.

**A new repost of a marketplace listing is refused** (§2.4), while reposts made
before that rule remain in the list above. The two facts read as contradictory
until you separate the write from the read: the list is a record of what an
account amplified, and rewriting history to match a newer rule would delete rows
with the count agreeing — the exact failure the paragraph above exists to
prevent. The card for such a row renders without its Like, Comment and Repost
controls.

---

### 5.7 Blocking

A signed-in user can **block** another account from the three-dot menu at the
top right of that account's profile — the same menu that offers **Report**
(§8.1). Blocking asks for confirmation; unblocking does not, following the same
rule as unfollow in §5.3.

**A block is mutual in effect, even though one person pressed it.** Neither
party sees the other anywhere afterwards:

- the blocked account's profile returns 404 — **to the blocker as well**, not
  only to the person blocked
- their articles leave the home feed, the following feed and the article page
- their comments leave every thread
- they leave search results, both as articles and as writers, including the
  semantic ranking
- they leave follower, following and suggested-writer lists, and the counts
  those lists sit beside

**Blocking removes any follow between the two accounts, in both directions, and
unblocking does not bring it back.** This is the one consequence a person cannot
undo by unblocking, so the confirmation dialog states it before they commit.

**The blocked account is never told.** No notification, no marker on the
profile, no change it can observe directly. That is why the block list shows
only who *you* blocked and never who blocked you.

**Where blocking deliberately does not reach:**

- **Notification history.** Notifications are stored against their recipient
  with no actor column, so a like or follow received before the block stays in
  the list. New ones cannot arrive: the actions that produce them are all
  unreachable in both directions.
- **Marketplace and evaluation surfaces.** A magazine browsing listings, an
  evaluation report, and Portfolio Insights are commercial and analytical
  paths, not social ones, and they do not filter. Articles already purchased
  stay readable, and existing purchases are unaffected either way.
- **Admin surfaces.** The report queue and user administration must show every
  account regardless of who has blocked whom, or a block would become a way to
  hide from moderation. Reporting also keeps working in both directions, so
  blocking someone never costs you the ability to report them.
- **Anonymous visitors.** A block is a relationship between two accounts. With
  no viewer there is no relationship to apply, and signed-out readers see the
  site unchanged.

**The AI paths need no block filter, and this is worth stating.** Semantic
retrieval looks like an obvious way for a blocked writer's prose to reach
someone anyway, and it is not one: the writing assistant, writer memory and
Portfolio Insights all retrieve strictly within the requesting writer's *own*
corpus, and hybrid search — the one retrieval path that spans everyone — screens
its semantic candidates against the block **before** they are fused with the
lexical ranking, not after, so a blocked article cannot reach the results or the
result count. Recorded because the absence of a filter in the retrieval layer
reads as an oversight until you know where the filtering happens instead.

A person can review and lift their blocks from **Settings → Blocked accounts**,
which is the only surface in the product that names a block.

---

### 5.8 Saved Articles

A signed-in account of **either type** can save an article to come back to it
later — personal accounts and magazines alike. A magazine's saves are a
shortlist of pieces it is considering; they are not the same thing as **Your
Library** (§4), which holds articles it has actually licensed.

Saving is available from **two controls**: the bookmark on an article card in
the feed, and the bookmark in the action bar on the article page. Saving again
un-saves. A signed-out visitor who presses either one is sent to sign in and
returned to where they were.

**The author is notified, and the notification names the saver** — "*{user}
saved your article*" — like every other social notification. Saving your **own**
article is allowed and notifies nobody.

**The list is private to the person who made it.** There is no public save
count anywhere in the product: not on the card, not on the article page, not in
analytics. A save signals nothing to anyone except the author's single
notification, and the reader's shelf is theirs alone.

Two entrances lead to the same list:
- **Saved** in the sidebar
- the **Saved** tab on your own profile

**Saving is the one social action a marketplace listing keeps.** Liking,
commenting and reposting are all refused there (§2.4); saving is not, because a
save is private to the saver and shortlisting candidates is precisely what a
magazine does while deciding whether to license something. The three public
signals are publication; a save is a bookmark.

**A save is a pointer, not access.** Saving a marketplace or premium article
does not unlock it — the card carries its usual badge, and the access rules in
§7.4 still decide what the body shows on read. This is deliberate and is the one
rule most likely to be "simplified" away by mistake: filtering the saved list
the way the public feed is filtered would silently empty a magazine's shelf of
exactly the articles it was shortlisting.

**Blocking applies in both directions** (§5.7): a save is refused between two
accounts where either has blocked the other, and an article saved before a block
drops out of the list while the block stands.

**Articles that go away, go away quietly.** A deleted article or one whose author
is banned leaves the list, and the count leaves with it, so the number above the
list and the rows in it can never disagree.

---

### 5.9 Reposted

The **Reposted** tab on a profile lists what that account has reposted, newest
first, as ordinary feed cards. It renders on **every** profile, enabled, for
**every** viewer including signed-out ones — reposting is public amplification,
so unlike **Saved** (§5.8) there is nothing to withhold and no reason to
conditionally render it.

Paginated in the standard envelope, stepped a page at a time. The membership
rules are in §5.6.

A repost whose article is later deleted leaves the list quietly, and the count
leaves alongside it — the same behaviour §5.8 describes for saves.

---

### 5.10 Sharing

Articles and writer profiles carry a **Share** control that opens a small
anchored popover with four actions: **X**, **Facebook**, **LinkedIn**, and
**Copy link**. The three social targets are ordinary links to each network's
share intent, opened in a new tab; only X accepts a pre-filled subject, so the
article title is passed there and nowhere else. Facebook and LinkedIn both
dropped pre-filled captions years ago and read the page's Open Graph tags
instead, which the article and profile routes already emit.

Sharing needs **no account**. It is one of the few interactions available to a
signed-out visitor (§A1), because nothing about it writes a row: there is no
share count, no notification, and **no share tracking of any kind**. A shared
link is an ordinary public URL, and the product learns nothing when one is
created. That is a deliberate scope boundary rather than an oversight — adding
attribution later would mean a real endpoint and a real table.

Links are built from the site's canonical origin and the item's own path, never
from the reader's current address bar, so a share never carries someone's query
string or scroll fragment along with it.

**Copy link** works on a non-secure origin as well as an https one. This matters
more than it sounds: the Clipboard API and the native share sheet are both
gated on a secure context, so on a plain-http origin neither exists, and an
implementation that assumes either one silently does nothing at all. The copy
action falls back to a selection-based copy so the control behaves the same way
everywhere it is served.

---

### 5.11 Engagement counts

The like, comment and repost counts on a **feed card** are computed **live**,
from the underlying tables, not read from the `article_metrics` rollup.

That is not a preference. The rollup runs on a schedule and nothing writes to it
when a reader presses a button, so a card showing a rollup number under an
interactive control visibly *snaps back*: the optimistic toggle ticks 17 to 18,
the next refetch hands back 17, and nothing on screen explains it. No amount of
caching fixes reading a stale number.

`article_metrics` remains the source for the **writer dashboard** and the
**analytics reports**, which report on a period rather than on a button, and
which also sort by it. The distinction worth keeping: *a dashboard that reports
on a period reads the rollup; a card the reader is about to press reads the
table.* Merging the two back together re-introduces the snap-back.

The counts a card reads are also **seeded** into the per-article status caches
the controls render from, so a page of twenty cards costs no extra requests
rather than sixty.

### Loading a long list

Every list of articles continues loading as the reader scrolls. A sentinel below
the last row starts the next page roughly a viewport early, a skeleton stands in
while it is in flight, and the new rows append beneath the ones already read.

A **"Load more" button remains** below the sentinel throughout, and is not
decoration. Scrolling is not an interaction every reader can perform: a keyboard
or screen-reader user generates no intersection events near a one-pixel div, and
the observer may never fire at all in a browser that lacks it. The button is also
what makes the *end* of a list legible — when it disappears, the list is finished.
Auto-loading alone gives the reader no equivalent signal.

Two failure rules go with it:

- **A failed page never discards the pages already read.** The rows and the
  reader's scroll position stay exactly where they are; the failure is reported at
  the bottom of the list with a retry. Only a failure with *nothing* loaded
  replaces the surface with an error state.
- **A failed page stops the auto-loader.** Recovery is deliberately manual,
  because a sentinel that is still on screen would otherwise retry immediately and
  without pause, turning one failed request into a continuous stream of them.

This applies to the home feed, the following feed, a writer's profile articles,
the writer's own dashboard list, saved articles, the reposted list, the
marketplace, a magazine's library, discover and search.

> Lists page by **offset**, not by cursor — see the NFR-14 note in
> `10-requirements.md`. A reader scrolling while new articles are published may
> therefore see one article twice, since every later row shifts down as rows are
> inserted above them. Ordering is `(published_at DESC, id DESC)`, which makes the
> boundary deterministic against *ties* but cannot make it stable against
> *insertion*.

---

## 6. 🔔 Notifications System

Notifications include:

- New follower
- New like on article
- New like on one's own comment or reply
- New comment on article
- **Someone saved one's article** (§5.8) — names the saver, and is never sent for
  saving one's own work

No notification is ever sent for a block (§5.7): the blocked account is told
nothing.

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

**An article's comment thread follows the article's own verdict in this table.**
*Not visible* means the thread is not visible either — the endpoint answers 404,
byte-identical to the article route's refusal, rather than handing over the
conversation about something it will not acknowledge. *Blocked* does not: a
public premium article is acknowledged, so its thread stays readable and only the
body is withheld.

---

## 8. ⚠️ Moderation & Reporting

### 8.1 Reporting System

Users can:
- Report articles — from the article's action bar
- Report other users — from the three-dot menu on their profile, beside
  **Block** (§5.7)

A report is filed for the admin queue (§8.2) and **offers a reason without
requiring one** — an unexplained report is still a signal an admin can act on,
and demanding prose is a reliable way to stop people reporting at all. A second
report on the same target by the same reporter, while the first is still
pending, is refused as a duplicate rather than queued twice.

Reporting requires a signed-in account: an anonymous report cannot be
deduplicated, rate limited per person, or weighed against the reporter's
history. Blocking someone does not remove the ability to report them, in either
direction.

> **Known drift:** the `reports.target_type` enum, the admin queue and FR-59 all
> cover a third target — a **comment** — and no control anywhere in the product
> files one. The reporting API would accept it today; only the UI is missing.
> Recorded rather than quietly dropped from the requirement, because the data
> model and the moderation queue are both already built for it.

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
