# Bugs

Findings from the UI sweep, newest first within each severity. See `README.md` for the
severity ladder and the filing format.

**IDs are never reused.** A finding that turns out to be invalid is marked `WITHDRAWN`
and left in place rather than renumbered — a stale reference to `BUG-007` should resolve
to something, even if that something says "this was wrong".

**No causes, no fixes.** This is a catalogue. Diagnosis is separate work.

| severity | count |
|---|---|
| Critical | 0 |
| High | 5 |
| Medium | 6 |
| Low | 2 |
| **active total** | **13** |
| *(withdrawn)* | *3* |

**All 13 active findings are fixed.** See `triage.md` for what each fix was.

---

## Critical

*None recorded.*

## High

### BUG-012 — the publish dialog's confirm button is unreachable at a 1280×720 window

- **Route:** `/editor/[id]` — the publish dialog
- **Persona:** any writer (found on a newly registered account, reproduced on the
  default Playwright viewport)
- **Expected:** the dialog's footer controls — "Publish", "Save as draft", "Close" — are
  reachable, by scrolling if the dialog is tall.
- **Actual:** at a 1280×**720** window the confirm button's box sits at **y = 754.5**,
  below the 720px fold, and **cannot be scrolled into view**. The dialog does not scroll
  internally and the page behind it does not move. The automation reports "element is
  outside of the viewport" after scrolling and the click never lands. Growing the window
  to 1280×1600 puts the button at y = 1194.5, where it works normally and publishes
  correctly.
- **Consequence:** on a laptop screen a writer can fill in the entire publish dialog and
  then have no way to press Publish, Save as draft, or even Close.
- **Screenshot:** `screenshots/publish-dialog-footer-720--e2e.png` (cut off),
  `screenshots/publish-dialog-footer-1600--e2e.png` (reachable),
  `screenshots/publish-dialog--e2e.png`
- **Console/network:** none captured — nothing fails, the control simply cannot be
  reached.

### BUG-011 — there is no way to publish a premium article

- **Route:** `/editor/[id]` — the publish dialog
- **Persona:** any writer, on any plan
- **Expected:** a writer can mark an article premium, since the product has a premium
  paywall for readers and the API's publish payload accepts a `visibility` field.
- **Actual:** the publish dialog offers **placement** only — "Public" and "Marketplace"
  — and no free/premium choice anywhere. The publish request never carries a
  `visibility` value, so every article published through the UI is free. The premium
  paywall shown to readers cannot be reached by any article created in the product.
- **Corroborating:** the dev database contains **zero** articles with premium
  visibility, across 23 articles.
- **Screenshot:** `screenshots/publish-dialog--e2e.png`
- **Console/network:** none captured.
- **Note:** checked against the known-gap rule before filing — the publish dialog
  carries no `NOT WIRED` or `TODO(` marker for visibility. Its `disabled` markers relate
  to marketplace eligibility, which is a different and correctly-working gate.

### BUG-004 — `/subscription` fails to load

- **Route:** `/subscription`
- **Persona:** all signed-in personas — magazine, writer, reader and admin
- **Expected:** the page shows the current plan and offers the subscribe / upgrade /
  cancel controls.
- **Actual:** two distinct failures on the same route.
  - **Magazine account** (`editors@longformreview.example.com`): the page renders the
    heading **"This page couldn't load"** with "Reload to try again, or go back." The
    subscription cannot be viewed, cancelled or renewed.
  - **Personal accounts** (reader, writer, admin): the page renders a "Your plan"
    heading, but throws an uncaught hydration exception and leaves a loading skeleton in
    place of the plan panel.
- **Screenshot:** `screenshots/subscription--magazine.png`,
  `screenshots/subscription--writer.png`, `screenshots/subscription--admin.png`,
  `screenshots/subscription--reader.png`
- **Console/network:**
  - `[pageerror] Error: Hydration failed because the server rendered HTML didn't match
    the client. As a result this tree will be regenerated on the client.` — the reported
    subtree is `SubscriptionPage → SubscriptionView → Skeleton`.
  - `[console] Encountered a script tag while rendering React component. Scripts inside
    React components are never executed when rendering on the client.`
- **Note:** this blocks the "magazine (lapsed)" persona column entirely — the sweep
  cancels a subscription via `/subscription`, and that control cannot be reached.

### BUG-005 — `/settings` contains no settings

- **Route:** `/settings`
- **Persona:** all signed-in personas (identical on reader, writer, magazine, admin)
- **Expected:** controls for account and preferences — the page's own subtitle promises
  "Manage your account and preferences."
- **Actual:** the page renders the heading "Settings" and that one subtitle line, and
  nothing else. Measured on the page: **0 inputs, 0 buttons, 0 tabs.** There is nothing
  on the screen a user can change.
- **Screenshot:** `screenshots/settings--writer-depth.png`, `screenshots/settings--reader.png`,
  `screenshots/settings--magazine.png`, `screenshots/settings--admin.png`
- **Console/network:** none captured.
- **Note:** checked against the known-gap rule before filing — the page carries **no**
  `NOT WIRED`, `TODO(` or `disabled` marker of any kind, so it is a finding rather than
  a documented non-implementation.

### BUG-006 — the marketplace and earnings notifications render as "New notification"

- **Route:** `/notifications`
- **Persona:** writer (`imane@example.com`) — any writer who has sold or been previewed
- **Expected:** each row describes what happened, e.g. "Your article was purchased" or
  "84 credits were credited to your balance".
- **Actual:** every notification of these three types renders the identical placeholder
  string **"New notification"** — no actor, no article title, no amount, no timestamp:
  - `earnings_credited`
  - `article_purchased`
  - `article_previewed`

  A writer is therefore never told that they were paid, or how much. Confirmed by count:
  the dev database holds exactly four notifications across these three types
  (`earnings_credited` ×2, `article_purchased` ×1, `article_previewed` ×1), and exactly
  four placeholder rows render.
- **Scope — the social notifications are fine.** Driven end to end in flow 4: a like, a
  comment, a repost and a follow against an `E2E:` article all produce correctly worded
  rows with actor, article title and relative timestamp, e.g. *"hakim-toure reposted
  your article "E2E: Publish and read 24136735" — 38s ago"*. Only the money-related
  types fall through to the placeholder.
- **Screenshot:** `screenshots/notifications--writer-depth.png`,
  `screenshots/notifications--writer.png` (placeholders);
  `screenshots/notifications--e2e-author.png` (the same screen rendering correctly)
- **Console/network:** none captured.
- **Note:** checked against the known-gap rule — no `NOT WIRED` or `TODO(` marker exists
  anywhere in the notifications feature, so this is a finding. Originally filed during
  session 1 as "every notification"; narrowed to the four marketplace/earnings types in
  session 2 after driving the social flow.

## Medium

### BUG-016 — publish-time auto-moderation flagged innocuous text as "hate"

- **Route:** the publish path; the result is visible in the `/admin` queue
- **Persona:** any writer publishing; seen by admin
- **Expected:** anodyne text is not flagged.
- **Actual:** an article whose entire body was *"Body for the remove moderation case."*
  was automatically reported at publish, and sits in the admin **Pending** queue with
  the reason:

  > Automatically flagged at publish by groq: hate. Published normally — this is a
  > review request, not a block.

  There is nothing resembling hate speech in the article.
- **Frequency:** 1 of the 6 identical, equally innocuous `E2E:` articles this sweep
  published was flagged; the other 5 were not. So it is intermittent rather than
  deterministic on this input.
- **Screenshot:** `screenshots/admin-queue-pending--admin.png`
- **Console/network:** none captured — publishing succeeded normally.
- **Note:** publishing is **not** blocked, so the consequence is a moderation queue
  filling with false positives rather than lost work. Recorded because an admin
  reviewing the queue has no way to tell this apart from a real report, and because a
  demo run that publishes an article may put a spurious "hate" flag on screen.

### BUG-014 — every dead content URL is a blank page for 7.5 seconds

> **Corrected in triage.** Filed as "no not-found state anywhere". That was wrong: the
> not-found state exists and is correctly worded — it just takes **~7.5 s** to appear,
> and the sweep only waited 3.5 s. Cause and fix in `triage.md` (Cause 1). The finding
> stands, re-scoped from "missing" to "unusably delayed"; severity unchanged.

- **Route:** `/articles/[slug]`, `/u/[username]`, `/m/[slug]`
- **Persona:** all, including guest
- **Expected:** a not-found state — "this article doesn't exist", a link back to the
  feed, something.
- **Actual:** the content region is **entirely empty (0 characters)** for the first
  ~7.5 seconds on every one of them — the sidebar, topic list and footer render as
  normal, wrapped around nothing, because the loading skeletons contain no text. A
  visitor cannot tell whether the link is dead, the page is still loading, or the app is
  broken. Measured: `/articles/<dead-slug>` paints "Article not found" after **7547 ms**.
- **Reproduced with:**
  - `/articles/this-slug-does-not-exist-at-all-12345` → `404 GET /api/articles/…`
  - `/u/no-such-user-98765` → `404 GET /api/u/…`
  - `/m/no-such-magazine-98765` → `404 GET /api/m/…`
  - and an article an admin has just **removed** through the moderation queue, which
    leaves every existing link to it blank rather than explaining it is gone.
- **Screenshot:** `screenshots/notfound-articles-this-slug-does-not-exist-a--guest.png`,
  `screenshots/notfound-u-no-such-user-98765--guest.png`,
  `screenshots/notfound-m-no-such-magazine-98765--guest.png`,
  `screenshots/removed-article-page--admin.png`
- **Console/network:** a clean `404` from the API in each case — nothing crashes, and
  the API behaves correctly. Only the UI has nothing to show.
- **Note:** this is the general case. `BUG-007` (a marketplace listing the viewer may
  not read) and `BUG-013` (a deleted article in the editor) are the same blank-page
  symptom reached by two other doors, kept separate because each has its own
  reproduction.

### BUG-013 — the editor opens an empty, editable document over a deleted article

> **Re-scoped in triage.** The blank period is the `BUG-014` delay (paints after
> **7966 ms**). What survives is worse than "blank" and is why this stays Medium: after
> the delay the editor renders working chrome — "Edit article / AI Assistant / Publish" —
> around an **empty but editable** body, with no not-found state, over an article that
> still exists in the database. See `triage.md`, Cause 1.

- **Route:** `/editor/[id]` where the article has been soft-deleted
- **Persona:** writer (the article's own author)
- **Expected:** a not-found or "this article was deleted" state.
- **Actual:** an entirely empty content region — 0 characters, no message, no way back.
  The author sees a blank screen.
- **Reproduced with:** `/editor/24652cce-a682-47ad-8a24-d8dac41e8ff3`
  (`gate-check-a-draft`, whose `deleted_at` is set).
- **Screenshot:** `screenshots/editor-deleted--writer.png`
- **Console/network:** `404 GET /api/articles/id/24652cce-a682-47ad-8a24-d8dac41e8ff3`
- **Note:** the 404 is **correct** — the article is deleted. Only the missing empty
  state is the finding. This is the salvaged, accurate part of the withdrawn `BUG-003`.
  The editor opens live articles and newly created drafts without any problem.

### BUG-007 — a marketplace article is blank for 7.7 s, then says it "doesn't exist"

> **Corrected in triage; recommend dropping to Low.** The blankness is the `BUG-014`
> delay, not a missing state — the page paints after **7750 ms**. What remains specific
> to this route is only the wording: a listing the viewer is *not entitled to* is
> described as one that "doesn't exist". See `triage.md`, Cause 1.

- **Route:** `/articles/[slug]` where the article's placement is `marketplace`
- **Persona:** guest, and the article's **own author** (writer)
- **Expected:** either the article, or a legible refusal — "this is a marketplace
  listing", a not-found state, or a prompt to sign in. Something.
- **Actual:** the page chrome renders (sidebar, topic list, footer) and the content
  region is **entirely empty** — no heading, no message, no explanation. The visitor is
  shown a page with a hole where the article should be.
- **Reproduced with:** `/articles/gate-check-unpaid-listing` as a guest, and as
  `imane@example.com`, who is the author of that listing.
- **Screenshot:** `screenshots/article-marketplace--guest.png`,
  `screenshots/articles-gate-check-unpaid-listing--writer.png`
- **Console/network:** `404 GET /api/articles/gate-check-unpaid-listing`
- **Note:** the access gate itself is **correct** — the article body is genuinely
  withheld, and the magazine that purchased a marketplace article *can* read it
  (verified separately against `verification-the-cost-of-a-preview`, which opens
  normally for the purchasing magazine and from the "Read" control in `/library`). What
  is wrong is that the refusal has no on-screen form, and that it also applies to the
  author of the article.

### BUG-001 — the "Upgrade to Premium" button in the AI quota notice is permanently disabled

- **Route:** `/editor/[id]` (the AI panel, when a free-plan writer's allowance is spent)
- **Persona:** writer on the free plan
- **Expected:** the button offers a route to upgrading, now that `/subscription` exists
  and can change a personal account's plan.
- **Actual:** rendered `disabled`. Pressing it does nothing, and the notice offers no
  other way forward.
- **Confirmed in the browser** (session 2), on the free-plan `E2E:` account created by
  flow 1 once its allowance reached zero:
  - the quota indicator reads **"No tokens remaining"**
  - the prompt box is locked out, placeholder **"No AI tokens remaining"**
  - the notice's only control reads **"Upgrade to Premium"** and reports
    `enabled = false`

  So a free writer who runs out of tokens is shown the way forward and cannot take it.
- **Screenshot:** `screenshots/ai-quota-notice--free-writer.png`
- **Console/network:** none captured.
- **Also worth noting:** the AI panel is article-scoped and does not exist at all on an
  unsaved `/editor/new` — the control only appears once an article has been saved. That
  looks deliberate rather than broken, and is recorded here only so the next session
  does not mistake it for a missing button.
- **Note:** filed as a bug rather than a known gap because its marker is **stale**. The
  comment reads `TODO(Phase 5): enable once the subscription upgrade flow exists` — and
  Phase 5 shipped that flow. This is the pattern to watch for: a `TODO(Phase 5)` whose
  blocker has since landed.

### BUG-002 — the "Subscribe to access" button on a magazine profile is permanently disabled

- **Route:** `/m/[slug]`
- **Persona:** any signed-in account viewing a magazine profile
- **Expected:** a route to subscribing, now that `POST /subscriptions/magazine` and the
  `/subscription` page both exist.
- **Actual:** rendered `disabled` beneath the text "From 500 credits/month", so the CTA
  states a price and then refuses to act on it.
- **Screenshot:** `screenshots/m-the-longform-review--reader.png`,
  `screenshots/m-the-longform-review--writer.png` — **confirmed in the browser this
  session.** The "Subscribe to access" copy is present on the rendered magazine profile
  for every signed-in persona.
- **Console/network:** none captured.
- **Note:** same stale-marker pattern as `BUG-001`. The comment reads
  `TODO(Phase 5): Wire to subscription/payment API`; that API now exists.

## Low

### BUG-009 — a broken thumbnail on the home feed

- **Route:** `/`
- **Persona:** all — guest, reader, writer, magazine and admin alike
- **Expected:** every feed card shows its thumbnail, or falls back cleanly to no image.
- **Actual:** one card's image fails to load on every visit to the home page. The
  underlying file is absent from object storage, so the image request 400s and the card
  renders with a gap where the picture should be.
- **Affected article:** `the-ethics-of-the-last-cast`, whose `thumbnail_url` is
  `/storage/inkwell/934073d1-3550-4fdb-bb3d-7fe576247a44.png`.
- **Screenshot:** `screenshots/home--guest.png`, `screenshots/home--reader.png`
- **Console/network:**
  `400 GET /_next/image?url=%2Fstorage%2Finkwell%2F934073d1-3550-4fdb-bb3d-7fe576247a44.png&w=256&q=75`
  and `[console] Failed to load resource: the server responded with a status of 400`.
  Requesting the file directly returns `404`.

### BUG-015 — a banned account is told its password is wrong

- **Route:** `/login`
- **Persona:** an account an admin has banned
- **Expected:** the sign-in attempt is refused with a reason — the account has been
  suspended, and here is who to contact.
- **Actual:** the form shows **"Invalid credentials"**, the same message a typo
  produces. A banned user is told they mistyped their password and will keep retrying;
  nobody is told the account was actioned.
- **Reproduced:** banned `e2e-mod-202645` through the moderation queue in flow 6, then
  attempted sign-in with the correct password.
- **Screenshot:** `screenshots/banned-account-login--e2e.png`
- **Console/network:** none captured — the refusal itself works correctly.
- **Note:** the ban is enforced properly; this is only what the user is told about it.

---

## Withdrawn

### BUG-003 — ~~a writer opening their own saved draft gets an empty editor~~ — **WITHDRAWN**

Filed Critical during session 1 on the claim that `/editor/[id]` could not open an
existing article at all. That claim was **wrong**, and the ID is retained rather than
reused.

The article it was reproduced against — `gate-check-a-draft` — is **soft-deleted**; its
`deleted_at` column is set. The API's 404 was therefore correct behaviour, not a defect.
The editor was subsequently confirmed to open both a live published article and a
freshly created draft with their content intact, and the full register → write →
publish → read flow completes successfully.

What survives is the blank page shown in place of a not-found state, re-filed accurately
as **`BUG-013`** at Medium.

### BUG-010 — ~~a hydration mismatch is logged on every page carrying the navbar~~ — **WITHDRAWN**

Filed Low against the navbar's search input, on a React hydration mismatch naming
`caret-color: transparent`. **The sweep's own screenshots were causing it.**

Playwright's `page.screenshot()` defaults to `caret: 'hide'`, which works by mutating
`caret-color` on the page. Doing that while React is hydrating makes React see an
attribute that was not in the server HTML, and report a mismatch. Measured on the exact
sequence: **1 such error with a screenshot in the middle of it, 0 without.** Supporting
evidence: `caret-color` appears nowhere in `src/`, nowhere in the server-rendered HTML,
and the computed caret at runtime is a normal `rgb(0, 0, 0)`.

The screenshot helper now passes `caret: 'initial'`, and the error is gone from the whole
suite. Nothing in the application was wrong.

### BUG-008 — ~~`/discover/writers/[username]` is a blank page for personal accounts~~ — **WITHDRAWN**

Filed Medium after the route rendered a 0-character content region for both the reader
and the writer persona. It does **not** reproduce. On re-testing, the route renders the
correct refusal for a personal account:

> Writer evaluation is for magazine accounts — These reports support licensing
> decisions, so they are limited to magazines with an active subscription. You can still
> read this writer's published work. **View public profile**

The blank observations came from the first cold visits, while the Next.js dev server was
still compiling the route; the empty region was an unpainted page rather than a missing
empty state. **Lesson for later sessions:** on a cold dev server, give a
first-ever-visited route more settle time than `probe()`'s 1200 ms before recording a
blank page — and re-visit once before filing one.
