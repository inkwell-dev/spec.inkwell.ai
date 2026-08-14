# Triage

The sweep's job was to catalogue symptoms without diagnosing them. This is the other
half: what actually causes each finding, what they share, and the order worth fixing
them in.

**The 14 active findings come from 8 distinct causes.** Three of them collapse into a
single one-line configuration change, and two more are blocked behind a third — so the
list is considerably shorter to fix than it is to read.

**Status: steps 1–6 are done** — see "What was fixed" at the end. Steps 7–10 remain.

| | |
|---|---|
| Active findings | 14 |
| Distinct causes | 8 |
| Findings fixed by the single highest-value change | 3 |
| Findings whose severity triage changed | 3 |
| **Fixed so far** | **9 of 14** (steps 1–6) |

---

## Three findings were mis-described by the sweep

Diagnosis changed what these are. The symptom entries in `bugs.md` have been annotated;
the reasoning is here.

**`BUG-014` is not "no not-found state".** The not-found state exists, is correctly
worded, and renders — after **7.5 seconds**. Measured:

| route | paints after | with |
|---|---|---|
| `/articles/<dead-slug>` | 7547 ms | "Article not found — This article doesn't exist, was unpublished, or its link has changed." |
| `/articles/<marketplace listing>` (`BUG-007`) | 7750 ms | the same not-found state |
| `/editor/<deleted id>` (`BUG-013`) | 7966 ms | the editor chrome, body still empty |

So the sweep, which waited 1.2 s and then 3.5 s, was photographing a loading state and
calling it a missing one. That is the sweep's error, not the app's.

**`BUG-007` should drop to Low.** The gate is correct, the eventual copy is correct, and
the only residue is that a *gated* marketplace listing is described as one that "doesn't
exist" — misleading, but minor, and it is the generic not-found string doing its job.

**`BUG-013` stays Medium** but for a narrower reason than filed. After the delay the
editor does not show a not-found state at all: it shows working editor chrome — "Edit
article / AI Assistant / Publish" — wrapped around an **empty, editable** document, over
an article that still exists in the database. That is the overwrite risk, and it is real
independent of the timing.

---

## Cause 1 — 404 responses are retried, so every "not found" takes ~7.5 s

**Fixes `BUG-014`, `BUG-007`, and the timing half of `BUG-013`.**

TanStack Query's default `retry: 3` with exponential backoff is applied to 404s. A 404
will never succeed on retry, so the client spends ~7.5 s re-asking a question already
answered before it will render the answer. Two individual hooks already opt out — the
`discover` and `subscription` hooks set `retry: false` with a comment explaining that a
403 is a permission boundary rather than a transient failure — but the reasoning was
never generalised to the default.

It reads as a *blank* page rather than a slow one because the loading skeletons are
empty `div`s: they contain no text, so the content region measures 0 characters and
looks like nothing rendered at all.

- **Fix:** set a default `retry` predicate on the query client that does not retry 4xx.
  One place, and it corrects every route at once.
- **Effort:** small · **Risk:** low · **Blast radius:** every query in the app, which is
  the point.
- **Worth doing alongside:** give the skeletons a visually-hidden "Loading…" so a
  loading state is never indistinguishable from an empty one.

## Cause 2 — `SubscriptionView` branches its layout on a client-only loading flag

**Fixes `BUG-004`** (High — and unblocks the last 4 coverage cells).

The API is healthy: `GET /subscriptions/me` returns `200` with correct data for the
magazine, and a correct `403` for personal accounts. The failure is entirely client-side.

`SubscriptionView` chooses between a skeleton and the real panel on
`useCurrentUser().isLoading`. The server prerenders the *loaded* branch and the client's
first render produces the *loading* branch, so the two disagree on the very first
element. React's own diff names it exactly:

```
<SubscriptionView>
  <div
+   className="mx-auto max-w-2xl space-y-4 px-4 py-8"   ← client (skeleton branch)
-   className="mx-auto max-w-2xl px-4 py-8"             ← server (loaded branch)
```

Hydration fails, React discards and regenerates the tree, and the page settles on either
a stuck skeleton (personal accounts) or an error card (magazine).

- **Fix:** do not branch markup on `isLoading` across the hydration boundary — render one
  stable shell and swap only its contents, or gate the page on a mounted flag.
- **Effort:** small–medium · **Risk:** low.
- **Sequencing:** **do this before `BUG-001` and `BUG-002`** — both of those fixes send
  users to `/subscription`, and routing people to a page that does not load would turn
  two dead buttons into two working buttons to a broken screen.

## Cause 3 — the dialog has no maximum height and cannot scroll

**Fixes `BUG-012`** (High).

`components/ui/dialog.tsx` positions content as:

```
fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 …
```

with **no `max-h`** and **no `overflow-y-auto`**. A dialog taller than the viewport
therefore overflows equally above and below the fold, and because it is `fixed`, nothing
can scroll it into view — the page behind it does not move it. At 1280×720 the publish
dialog's footer sits at y ≈ 754, 34 px past the fold and unreachable.

- **Fix:** add a max height and internal scrolling to the dialog primitive, e.g.
  `max-h-[calc(100dvh-2rem)] overflow-y-auto`.
- **Effort:** small (one class list) · **Risk:** low · **Blast radius:** every dialog in
  the app, all of which currently share the defect. The publish dialog is simply the
  tallest and so the first to hit it.
- **Highest value-per-line change on this list**: it currently blocks publishing outright
  on a laptop screen.

## Cause 4 — three notification types have no message case

**Fixes `BUG-006`** (High).

`buildMessage()` in `features/notifications/notification-list.tsx` switches on
`notification.type` and handles `like`, `repost`, `comment`, `follow` and `system`.
The three marketplace/earnings types — `earnings_credited`, `article_purchased`,
`article_previewed` — hit the `default:` arm and return the literal string
`'New notification'`.

- **Fix:** add the three cases, reading the amount and article title out of
  `notification.data`.
- **Effort:** small · **Risk:** low.
- **Why it matters more than its size:** this is the only channel that tells a writer
  they have been paid.

## Cause 5 — features that were never built

Not broken; absent. Each needs building rather than repairing.

| finding | what is missing | effort |
|---|---|---|
| `BUG-011` (High) | The publish dialog has no free/premium control and never sends `visibility`, so no article published through the product can ever be premium — the reader-side paywall is unreachable. | medium |
| `BUG-005` (High) | `/settings` is a stub: a heading, one subtitle line, and **0 inputs, 0 buttons, 0 tabs**. | large |

Neither carries a `NOT WIRED` or `TODO(` marker, which is why both are findings rather
than known gaps. `BUG-011` is what blocks flow 2 of the sweep.

## Cause 6 — controls disabled behind a dependency that has since shipped

**`BUG-001`** (the AI quota notice's "Upgrade to Premium") and **`BUG-002`** (a magazine
profile's "Subscribe to access"). Both are `disabled` behind a `TODO(Phase 5)`, and Phase
5 shipped the subscription flow and the API they were waiting for.

- **Fix:** enable each and point it at `/subscription`.
- **Effort:** small each · **Risk:** low.
- **Blocked by Cause 2.** See the sequencing note there.

## Cause 7 — backend behaviour

| finding | cause | notes |
|---|---|---|
| `BUG-016` (Medium) | The publish-time `groq` moderation check flagged the text *"Body for the remove moderation case."* as **hate**. 1 of 6 identical innocuous articles, so it is intermittent rather than input-determined. | Publishing is not blocked, so the cost is a queue filling with false positives an admin cannot distinguish from real reports. Needs a threshold/prompt review on the API side. |
| `BUG-015` (Low) | A banned account is refused with the generic `Invalid credentials`, identical to a typo. | The ban itself is enforced correctly. Needs a distinct response for a suspended account, and login copy to match. |

## Cause 8 — one-offs

| finding | cause | fix |
|---|---|---|
| `BUG-009` (Low) | **Data, not code.** `the-ethics-of-the-last-cast` has a `thumbnail_url` pointing at an object that is not in storage; the file 404s and `_next/image` turns that into a 400. | Reseed, re-upload, or null the column. Nothing to change in the app. |
| `BUG-010` (Low) | A hydration mismatch on the navbar search input's `caret-color`. No `caret-color` rule exists anywhere in `src/`, so it originates in a base/vendor layer. | Cosmetic; console noise only. The caret is genuinely visible — computed `caret-color` is `rgb(0, 0, 0)` and typing shows a normal cursor. Lowest priority on this list. |

---

## Suggested order

Sequenced by value per unit of effort, and by what unblocks what.

| # | do | fixes | effort | why here |
|---|---|---|---|---|
| 1 | Dialog max-height + scroll | `BUG-012` | S | One class list. Publishing is currently impossible at 720p. |
| 2 | Stop retrying 4xx | `BUG-014`, `BUG-007`, half of `BUG-013` | S | One config change, three findings, every route improves. |
| 3 | Fix `SubscriptionView` hydration | `BUG-004` | S–M | Unblocks the last 4 coverage cells **and** items 4. |
| 4 | Enable the two dead CTAs | `BUG-001`, `BUG-002` | S | Cheap, but only safe after 3. |
| 5 | Add the 3 notification cases | `BUG-006` | S | Small fix, and it is how writers learn they were paid. |
| 6 | Editor not-found state | rest of `BUG-013` | S | Removes the overwrite risk over a deleted article. |
| 7 | Premium visibility in publish | `BUG-011` | M | Unblocks sweep flow 2 and the whole premium feature. |
| 8 | Build `/settings` | `BUG-005` | L | Largest, and nothing else depends on it. |
| 9 | Moderation threshold; banned-login copy | `BUG-016`, `BUG-015` | S–M | Backend work, independent of the above. |
| 10 | Thumbnail data; caret hydration noise | `BUG-009`, `BUG-010` | S | Cosmetic and data cleanup. |

Steps 1–6 are all small, and between them close **9 of the 14** findings.

## Verifying the fixes

The E2E suite already asserts the correct behaviour for most of this, so the specs are
the acceptance criteria — a fix is done when its spec goes green without being edited:

| step | spec that should turn green |
|---|---|
| 1 | `08-flow-register-publish-read` publishes without growing the viewport |
| 2 | `13-not-found` (3 tests), `03-writer` marketplace-article cell |
| 3 | `/subscription` cells in `02-reader`, `03-writer`, `04-magazine`, `05-admin` |
| 5 | add an assertion to `10-flow-social` for a purchase notification |
| 6 | `03-writer` "a deleted article gives a not-found state" |
| 7 | flow 2 becomes drivable for the first time |

After step 2, lower `probe()`'s 3500 ms settle time — it is padded to accommodate exactly
the retry backoff that step removes.


---

## What was fixed

Steps 1–6, on `fix/sweep-triage-steps-1-6` in `frontend.inkwell.ai`. Six commits, one per
step. The suite went from **100 passed / 10 failed** to **112 passed / 0 failed**, with
2 skipped (the AI specs, on an exhausted allowance).

| step | finding(s) | commit |
|---|---|---|
| 1 | `BUG-012` | `fix(ui): cap dialog height so tall dialogs stay reachable` |
| 2 | `BUG-014`, `BUG-007`, timing half of `BUG-013` | `fix(query): stop retrying 4xx responses` |
| 3 | `BUG-004` | `fix(subscription): make /subscription load for every account type` |
| 4 | `BUG-001`, `BUG-002` | `fix(subscription): enable the two CTAs that lead to /subscription` |
| 5 | `BUG-006` | `fix(notifications): render the marketplace and earnings types` |
| 6 | rest of `BUG-013` | `fix(editor): show a not-found state instead of an empty editable document` |

### One cause the triage missed

`BUG-004` turned out to have **two** independent causes, not one. The hydration mismatch
was real and is fixed, but it was not what produced the magazine's "This page couldn't
load" — that was a second, unrelated fault sitting behind it:

`MagazinePanel` computes its idempotency token with `crypto.randomUUID()`.
**That API is secure-context only.** It is `undefined` over plain HTTP, which is exactly
how this app is served locally — confirmed in the browser: `isSecureContext: false`,
`typeof crypto.randomUUID === "undefined"`. Calling it did not degrade, it threw, during
render, taking out the error boundary and the whole page with it.

It would have worked perfectly in any HTTPS environment, which is precisely why it
survived to be found by a browser sweep on an HTTP dev stack. Fixed with `randomId()`,
which prefers `crypto.randomUUID` and falls back to assembling a v4 UUID from
`crypto.getRandomValues` — not secure-context gated, so still cryptographically random.

**Worth carrying forward:** anything gated on a secure context is invisible in
development-over-HTTPS and fails only where there is no TLS. This deployment has no TLS
until the very end, so that class of fault will keep landing here first.

### Two spec changes, both deliberate

Neither weakens an assertion:

- **Flow 1** no longer grows the viewport to 1600px before publishing. That was a
  workaround for `BUG-012`; it now publishes at 1280×720 and asserts the footer is
  reachable after scrolling.
- **Flow 4** presses repost and follow only when they are not already in the desired
  state. They are toggles against a persistent database, so on a second run the spec was
  undoing the first run's work rather than repeating it.

### Still open

Steps 7–10, covering `BUG-011` (no way to publish a premium article — still blocks sweep
flow 2), `BUG-005` (`/settings` is a stub), `BUG-016`, `BUG-015`, `BUG-009` and
`BUG-010`.
