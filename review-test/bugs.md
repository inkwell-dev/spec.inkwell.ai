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
| Medium | 4 |
| Low | 2 |
| **active total** | **11** |
| *(withdrawn)* | *2* |

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

### BUG-006 — every notification renders as the literal text "New notification"

- **Route:** `/notifications`
- **Persona:** writer (`imane@example.com`, who has unread notifications — the navbar
  bell shows a count of 2)
- **Expected:** each row describes what happened and who did it, e.g. "X liked your
  article …", and links to the thing it refers to.
- **Actual:** all four rows render the identical placeholder string **"New
  notification"**, with no actor, no article title, no timestamp and no visible link
  target. The list is unusable — a reader cannot tell what any notification is about.
- **Screenshot:** `screenshots/notifications--writer-depth.png`,
  `screenshots/notifications--writer.png`
- **Console/network:** none captured.
- **Note:** checked against the known-gap rule — no `NOT WIRED` or `TODO(` marker exists
  anywhere in the notifications feature, so this is a finding.

## Medium

### BUG-013 — the editor renders a blank page for a deleted article

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

### BUG-007 — a marketplace article renders a completely blank page to anyone without access

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
- **Screenshot:** *not yet captured — found by code inspection while preparing this
  sweep; confirm in the browser and attach.*
- **Console/network:** none captured.
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

### BUG-010 — a hydration mismatch is logged on every page carrying the navbar

- **Route:** every route with the site header — `/`, `/articles/[slug]`, `/u/[username]`
  and the rest
- **Persona:** all, including guest
- **Expected:** a clean console.
- **Actual:** every page logs a React hydration-mismatch error naming the navbar's
  search input, on the `caret-color: transparent` style attribute. React states the
  mismatch "won't be patched up".
- **Screenshot:** `screenshots/home--guest.png`
- **Console/network:** `[console] A tree hydrated but some attributes of the server
  rendered HTML didn't match the client properties. … <input type="search"
  aria-label="Search articles and writers" -style={{caret-color:"transparent"}}>`
- **Note:** checked for a visible consequence and found none — the computed
  `caret-color` on the focused search input is `rgb(0, 0, 0)`, and typing into the box
  shows a normal cursor. Filed Low on the console noise alone. This is a **different**
  error from the uncaught hydration *failure* on `/subscription` recorded in `BUG-004`.

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
