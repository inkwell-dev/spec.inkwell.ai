# Magazine licensing: what a purchase actually buys

**Date:** 2026-09-06
**Status:** approved — decomposed into four tickets, none yet built
**Scope:** the magazine side of the marketplace, from listing to publication

---

## 1. Why this exists

Four observations, made while walking the magazine side of the product:

1. Marketplace articles render a comments section, which makes no sense for a
   private commercial listing.
2. After a magazine buys an article, it is still listed on the writer's public
   profile.
3. It is unclear where a bought article *goes*. Should the magazine publish it?
   Does it appear on the magazine profile, or in the home feed?
4. A magazine's card and a writer's card are indistinguishable.

All four turn out to share one cause, and settling that cause settles all four.

---

## 2. What the code does today

Verified by reading the source and by querying the running database on
2026-09-06. File references are to the state of `main` on that date.

### 2.1 A purchase does not touch the article

`PurchasesService.buyStage` (`src/purchases/purchases.service.ts:124`) writes an
`article_purchases` row, two ledger rows and a notification. **The `articles`
row is never updated.** "Bought" is therefore a fact recorded *beside* the
article, invisible to every read surface that does not join `article_purchases`.

That single choice is the root of all four observations.

### 2.2 There is no exclusivity

The unique key on `article_purchases` is
`(article_id, magazine_id, stage)` — not `(article_id, stage)`. Any number of
magazines may fully purchase the same article, and `browseMarketplace`
(`src/discover/discover.service.ts:266`) keeps listing it afterwards, because
its predicate is `placement = 'marketplace' AND status = 'published'` and
nothing else.

This contradicts the specification twice: US-41 ("paid for exclusivity") and
`2-features.md` §4.5 ("sell exclusive content").

### 2.3 Marketplace articles are listed on the writer's profile, and 404

`UsersService.findArticlesByUsername` (`src/users/users.service.ts:178`) lists
every published article regardless of placement, and its "Premium" filter
deliberately *includes* `placement = 'marketplace'`. Its docblock defends this:
"A profile shows what someone has published; the feed shows what is freely
readable."

But `resolveArticleAccess` (`src/articles/article-access.ts:126`) throws 404 for
any reader on a marketplace article. **A reader sees the card, clicks it, and
lands on a not-found page.** This is live behaviour, not a hypothetical.

### 2.4 The specification contradicts itself here

- `2-features.md` §2.4 — marketplace articles are "Not listed in the public feed
  or on the writer's public profile."
- `2-features.md` §4.5.4 Stage 3 — "Article gets a 'In [Magazine]'s library'
  attribution badge **on the writer's profile**."

Both cannot hold. The code matches neither. Section 4.3 below resolves it.

### 2.5 Engagement has no placement gate at all

`CommentsController` accepts a comment from any authenticated user on any
article id, with no placement or access check. Its GET is `JwtOptionalGuard`, so
**an anonymous reader can fetch the comment thread of an article they receive a
404 for.** Likes have no gate either. Reposts and saves both carry deliberate
comments explaining that they preserve marketplace articles on purpose.

The reader page renders `<ArticleComments>` whenever `!isGated`, which is true
for the author, for admins, and for any magazine that has unlocked the article.

### 2.6 The magazine's purchases are private, and its public profile is fake

`GET /magazines/me/library` is guarded `accountTypes: ['magazine']` with
`subscription: true` — private to the buyer. `GET /m/:slug` returns profile
fields only; **there is no public magazine article endpoint anywhere in the
backend.**

The magazine profile's "Published articles" tab
(`src/features/profiles/magazine-articles-tab.tsx`) is six hardcoded placeholder
articles with invented authors, `slug: '#'`, and a `LoadMoreButton` wired to
nothing. Its comment reads "Phase 1 demo data (Phase 3 wires to real API)".
Phase 3 came and went.

### 2.7 There is no publisher concept in the frontend

`ArticleCard`'s byline is always `article.author`. Its badges are placement and
visibility only. Nothing renders "licensed by" or "published in". The phase
plan's claim that a "Licensed by badge" shipped on the reader page is stale —
the only badge there is a `MARKETPLACE` crown.

### 2.8 What the live database contains

Queried against the seeded dev database, 2026-09-06:

| | count |
|---|---|
| Published marketplace articles | 110 |
| ...already fully purchased | 47 |
| ...**purchased by more than one magazine** | **16** (one by four) |
| **Comments on marketplace articles** | **966** |

The seed corpus actively contradicts exclusivity. This is a migration and
reseeding problem, not only a code problem — see section 6.

---

## 3. Decisions

Settled during the 2026-09-06 brainstorm. These override anything in section 2
and close the questions they answer.

**D1 — A purchase puts the article in the library *unpublished*.**
The magazine then takes an explicit "Publish" action, and *that* action, not the
purchase, makes the article publicly readable under the magazine's brand.
Rationale: it gives magazines real editorial agency, makes "curated library"
mean curation, and prevents an accidental purchase becoming instantly public.

**D2 — Licensing is exclusive. The first full purchase takes the article.**
No second magazine may buy it. This makes US-41 and §4.5 true rather than
aspirational.

**D3 — A stranded previewer is not refunded, and keeps reading access.**
If Other Mag paid the 10% preview fee and Young Youth then buys outright, Other
Mag keeps the read forever and simply cannot buy. The preview fee is priced as
reading access, not as an option to buy. No ledger change: `resolveArticleAccess`
already grants the read on either stage. Refunding was rejected because the
writer has already been paid 80% of that fee, so a refund means clawing it back
from an earnings balance that can go negative, or the platform absorbing it —
either needs a new ledger invariant and its own tests.

**D4 — A marketplace listing is hidden from the writer's public profile, and
reappears once published.**
While unsold it is absent entirely (§2.4's rule, and it kills the dead link).
Once the magazine publishes it, it returns to the writer's profile carrying an
"in [Magazine]" attribution, linking to the now-readable article — which is what
§4.5.4 Stage 3 was reaching for. The author always sees their own listings on
their own profile.

**D5 — A published licensed article is public like any other article.**
Home feed, magazine profile, writer profile, search; free to read for everyone
including signed-out visitors. A magazine is paying for reach.

**D6 — On an unsold listing, likes, comments and reposts are off. Saves stay.**
Public social signals do not belong on a private commercial listing. Saves
remain because shortlisting during evaluation is a real magazine workflow, and
`saves.service.ts` already preserves marketplace articles deliberately. The
three switch on the moment the article becomes public; saves were never off. This is consistent with
eligibility, which already counts reactions only on `placement = 'public'`
(`src/marketplace/eligibility.service.ts:94`).

**D7 — Cards carry a dual byline.**
Author and publisher side by side in the existing byline slot: the writer's
avatar and name, then the magazine's logo and name, each linking independently
to `/u/<username>` and `/m/<slug>`. Preserves §4.5.5's "attribution preserved"
while making the publisher plain, and reuses the `Byline` component rather than
inventing a badge type.

---

## 4. The design

### 4.1 One new column

```
ALTER TABLE articles
  ADD COLUMN publisher_id uuid NULL REFERENCES users(id);
CREATE INDEX articles_publisher_id_idx ON articles (publisher_id);
```

Generated through `drizzle-kit generate`, never hand-written.

### 4.2 Three states, no extra columns

| State | `placement` | `publisher_id` | `full_purchase` row |
|---|---|---|---|
| **Listed** | `marketplace` | `NULL` | none |
| **Owned** | `marketplace` | `NULL` | exists |
| **Published** | `public` | the magazine | exists |

Publishing sets `placement = 'public'`, `visibility = 'free'`, `publisher_id`,
and **nulls `marketplace_price`** — i.e. exactly what `switchToPublic` already
does, plus the publisher.

Keeping the price was considered and rejected. The seed documents an invariant
twice (`src/database/seed/index.ts:1075` and `:1245`) — "public: `visibility` is
'free' or 'premium', `marketplace_price` null" — derived from what
`articles.service.ts` can actually produce, on the principle that "a seeded row
that broke them would be a row the product cannot produce". The test fixtures
mirror it (`test/marketplace/eligibility.service.spec.ts:36`). Keeping the price
would also break `seed/index.ts:825`, which identifies listings by
`marketplacePrice !== null` rather than by placement, so every published
licensed article would be re-counted as a live listing.

Nothing is lost: `article_purchases.credits_paid` is the better record anyway,
being what was actually paid rather than what was asked.

Rejected alternatives, with the reason:

- **A new `'licensed'` placement value.** Keeps a permanent marker on the article
  that it came from the marketplace, and the enum addition is safe on a live
  database. Rejected because it touches every one of the ~10 sites that test
  `placement = 'public'` (feed x4, discover, retrieval, eligibility, profile
  filter), and enum additions are a catalogued silent-breakage source here:
  exhaustive switches break loudly, `??` fallback chains do not.
- **A `magazine_publications` table with the article row untouched.** Fully
  non-destructive and supports multiple publishers. Rejected because every
  public read gains an `OR EXISTS`, which walks straight into the `countRows`
  drift trap — a predicate reaching into another table must be a self-contained
  `EXISTS` with the identical value passed to both the page query and the count.
  That has already bitten follows, blocks and saves.

### 4.3 Four guards

Three of these are new refusals on paths that currently succeed.

1. **`loadPurchasable` rejects a purchase when a `full_purchase` row exists for
   any magazine.** Exclusivity, enforced at the only place credits move
   (D2).
2. **`switchToPublic` rejects once a `full_purchase` row exists.** Today a writer
   can sell an article and then unilaterally make it free, and the buyer's
   exclusivity evaporates with no trace.
3. **`softDelete` rejects a purchased article.** §2.5 already says "licensed
   articles cannot be hard-deleted while licenses exist", but soft delete *is*
   this product's delete — it is what `DELETE /articles/:id` performs — so
   without this guard a writer can take back what a magazine paid for and the
   rule protects nothing.
4. **Publishing requires** a magazine account, a live subscription, and a
   `full_purchase` row owned by the caller.

### 4.4 Read surfaces

| Surface | Change |
|---|---|
| Home feed | none — `placement = 'public'` picks it up |
| Search | none — same predicate (`search.service.ts:462`) |
| Reader access gate | none — marketplace still 404s, public still reads |
| Marketplace browse | none — delisting is automatic |
| Writer's public profile | **new predicate**: hide `placement = 'marketplace'` from viewers who are not the author |
| Writer's profile "Premium" filter | drops marketplace from its `OR`; becomes `visibility = 'premium'` only |
| Magazine public profile | **new endpoint** `GET /m/:slug/articles` — `publisher_id = magazine`, published, not deleted |
| Every article payload | gains `publisher: AuthorRef \| null` |
| Likes / comments / reposts | 403 on write when `placement = 'marketplace'`; the comment GET must 404 rather than leak a thread |
| Saves | unchanged, deliberately (D6) |

**`AUTHOR_SELECTION` cannot be reused for the publisher.** It binds directly to
`schema.users` (`src/database/query-helpers.ts:42`), so a second join needs a
table alias. Reusing the constant produces a publisher that silently equals the
author.

### 4.5 The magazine-side flow

- `POST /magazines/me/library/:articleId/publish` — the new action.
- `/library` distinguishes **Unpublished** (with a Publish button) from
  **Published** (linking to the live article).
- `magazine-articles-tab.tsx` loses its six hardcoded fakes and its dead
  `LoadMoreButton`, and gets `useInfiniteQuery` page-stepping — the
  grow-the-limit pattern removed everywhere else on 2026-09-06 (FR-69).
- The writer is notified when their article is published. This needs a new
  `notification_type` enum value, **appended at the end** of the list for the
  reason the enum's own comments give three times: appending emits a plain
  `ALTER TYPE ... ADD VALUE`, while slotting it mid-list emits
  `ADD VALUE ... BEFORE`, a needless extra constraint bought for cosmetic
  ordering that nothing sorts by.

---

## 5. What this makes false in the specification

Reconciled per ticket, not in one sweep. The full list:

- `2-features.md` §2.4 — the placement table's "Not listed in the public feed or
  on the writer's public profile" becomes true for the first time, and needs the
  post-publication exception spelled out.
- `2-features.md` §2.4 Placement Rules — "Marketplace -> Public switch is allowed
  at any time" is now false; it is blocked once sold.
- `2-features.md` §2.4.1 — the per-pair state list gains a fourth state,
  published, and stops being purely per-pair: exclusivity makes ownership a
  property of the article.
- `2-features.md` §4.5.4 Stage 3 — the badge is on the writer's profile only
  after publication, and the stage does not end at the library.
- `2-features.md` §4.5.5 — the library is no longer purely private; it gains a
  publish action and a public counterpart.
- `2-features.md` §5.2 — the magazine profile's "Published articles" tab
  finally means something.
- `6-database-schema.md` — `articles.publisher_id`, and the exclusivity rule on
  `article_purchases`.
- `10-requirements.md` — new `FR-` rows for exclusivity, for publication, and
  for the public magazine library; a `US-` row for the magazine publishing what
  it bought. **Ids are append-only** — take the next number, never renumber.
- The phase plan's "Licensed by badge" claim on the article reader page is
  stale and should be corrected rather than quietly satisfied.

---

## 6. Migration and seed

- **16 articles have 2-4 owners.** A backfill must not delete the losing purchase
  rows: their `writer_payout` transactions are real and already summed into
  `earnings_balance`, so deleting them breaks the ledger invariants. **Keep the
  rows, keep the money, add the guard going forward, and reseed.** The historical
  multi-owner rows are an artifact of a pre-exclusivity era.
- **966 comments on marketplace articles** become unreachable. They are not
  deleted; they stop rendering and stop counting. The seed stops generating them.
- The seed must produce all three lifecycle states, or `/library` and the
  magazine profile have nothing to render.

---

## 7. Silent-breakage risks specific to this change

Drawn from the catalogue in the ticket skill's environment notes, filtered to
what this change actually invites:

- **`countRows` drift** — every new list here (the magazine's public articles,
  the split library) must pass the *identical* predicate to both the page query
  and the count.
- **`forbidNonWhitelisted`** — a `published`/`unpublished` filter on the library
  is a new query parameter and must be declared on the DTO, or it 400s.
- **`@Auth()` vs `JwtOptionalGuard`** — `GET /m/:slug/articles` is a public,
  auth-aware read. `@Auth()` would 401 signed-out visitors and break the page.
- **Exhaustiveness the compiler cannot see** — the new notification type breaks
  the exhaustive switches loudly and mis-renders in the `??` fallback chains
  silently. Grep for the other enum values to find every site.
- **Grow-the-limit pagination** — the magazine articles tab must step pages, not
  raise its limit.
- **Viewer-scoped cache keys** — library state is per-magazine and belongs in
  `VIEWER_SCOPED_KEYS`.
- **The frozen pagination envelope** — `{ items, page, limit, total, hasMore }`,
  exactly, for both new lists.

---

## 8. Tickets

Four, ordered so each ships something on its own.

### Ticket 1 — Marketplace listings stop leaking into public surfaces
*backend + frontend + spec. No schema change.*

Hide `placement = 'marketplace'` from the writer's public profile for everyone
but the author; drop marketplace from the profile's "Premium" filter; gate
likes, comments and reposts on placement (403 on write); make the comment GET
404 for anyone who cannot read the article; remove the comments section and the
like/repost controls from the reader page for a marketplace article. Reconcile
§2.4 against §4.5.4.

Independent of everything else, fixes two of the four observations, and kills a
live 404. Ships first.

### Ticket 2 — Exclusivity
*backend + spec. Small.*

The three new refusals: purchase blocked when another magazine owns it,
`switchToPublic` blocked once sold, `softDelete` blocked once sold. Record in
the spec that exclusivity is now enforced rather than merely promised.

### Ticket 3 — A magazine can publish what it bought
*backend + frontend + spec. Schema change. Seed rework rides here.*

`articles.publisher_id` and its migration; the publish endpoint and its guards;
`/library` split into unpublished and published; the writer notification and its
enum value; the seed producing all three states.

Demoable alone: buy, publish, and it is live.

### Ticket 4 — Licensed work becomes visible
*backend + frontend + spec. Depends on ticket 3's column.*

`GET /m/:slug/articles`; the magazine profile tab wired to it with the six fakes
deleted; `publisher` on every article payload via an aliased join; the dual
byline on `ArticleCard`; the attribution back on the writer's profile.

---

## 9. Explicitly out of scope

- Any refund mechanism (D3 settles this: there is none).
- Unpublishing — a magazine that publishes cannot currently un-publish. Not
  designed here; if it is wanted it needs its own decision about what happens to
  readers mid-article and to the article's feed position.
- Reselling a licensed article to a second magazine.
- Showing magazines how many rivals have previewed an article. Considered and
  set aside as a second feature riding along; it also exposes competitors'
  evaluation activity to each other.
- The 966 existing marketplace comments are left in place, not purged.
