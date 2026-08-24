# Progress

**Read this first.** It is the resume point — a session starts from here, not from the
beginning.

Keep it current **as you go**, not at the end. A session that dies mid-run should still
leave an accurate picture of what was covered.

---

## Status

| | |
|---|---|
| Sessions run | 2 |
| Cells covered | 62 / 66 · **flows 5 of 6** |
| Playwright installed | **yes** — see "The suite" below |
| Findings so far | 16 filed, 3 withdrawn → 13 active · **all 13 fixed** |
| **Resume at** | **nothing** — sweep, triage and all ten fix steps are complete |

---

## The suite

Playwright is installed and the fixtures are written. It lives in
`frontend.inkwell.ai/e2e/` and is run from `frontend.inkwell.ai`:

```
npx playwright test              # everything
npx playwright test 03-writer    # one spec
```

| file | what it is |
|---|---|
| `playwright.config.ts` | baseURL `http://frontend.inkwell.ai`, serial (`workers: 1`), no `webServer` — the stack must already be up |
| `e2e/fixtures/personas.ts` | the persona table and the shared demo password |
| `e2e/fixtures/auth.ts` | real-form login + `storageState`; asserts the `access_token` cookie is present |
| `e2e/fixtures/test.ts` | the **error collector** and the **screenshot helper**, plus `usePersona()` |
| `e2e/fixtures/probe.ts` | one route visit reduced to rendered / refused / blank / crashed |
| `e2e/fixtures/column.ts` | generates a persona's allowed + refused coverage cells |
| `e2e/fixtures/seed-data.ts` | the concrete slugs, usernames and ids read out of the dev database |

Flow specs, added in session 2: `08` register→publish→read, `09` AI, `10` social,
`11` marketplace (the whole chain, with the arithmetic asserted), `12` moderation,
`13` not-found states, `14` the free-plan AI quota notice.

Notes for whoever picks this up:

- **Tokens expire after 15 minutes.** `usePersona()` re-authenticates in a `beforeAll`,
  so each spec file starts with a fresh session. Do not hand-inject tokens — auth lives
  in localStorage *and* an `access_token` cookie and both must be set.
- The error collector subscribes to `pageerror`, `console` (errors only) and any
  response `>= 400`, and attaches what it caught to the HTML report **even on a pass**.
  It is what found `BUG-004`, `BUG-009` and `BUG-010`.
- Screenshots are written to `review-test/screenshots/` automatically.
- **Some specs fail on purpose.** They assert correct behaviour, and the behaviour is
  currently wrong. Every failure maps to a filed finding — 4 × `/subscription`
  (`BUG-004`), the marketplace article page (`BUG-007`), the deleted-article editor
  (`BUG-013`), 3 × not-found (`BUG-014`) and the AI quota notice (`BUG-001`). Do not
  "fix" the specs to make them green.
- **The AI specs skip when the allowance is exhausted.** That budget is real, finite and
  shared, and this sweep spent it. A skip there is an environment condition, not a pass.

## Seed-data facts worth knowing

- **There is no premium-visibility article in the seed** and no `magazines` table
  (magazine data lives in `magazine_profiles`). The premium paywall flow has to create
  its own article.
- **`hakim@example.com` is on the `premium` plan**, not free as the brief states. For a
  genuinely free reader use **`joon@example.com`** (`joon-park`) — same demo password.
- Two marketplace listings exist, both by `imane-farouk`: `gate-check-unpaid-listing`
  (80 credits, unsold) and `verification-the-cost-of-a-preview` (105 credits, already
  purchased by the magazine).
- DB access: `docker exec inkwell-db-1 psql -U inkwell -d inkwell`.

---

## Coverage matrix

`·` not attempted · `✓` covered, nothing found · `✗` covered, finding filed ·
`n/a` persona cannot reach this route · `→` should redirect/refuse (assert it)

| route | guest | reader | writer | magazine | mag. lapsed | admin |
|---|---|---|---|---|---|---|
| `/` | ✗ | ✗ | ✗ | ✗ | · | ✗ |
| `/login` | ✓ | → | → | → | → | → |
| `/register` | ✓ | → | → | → | → | → |
| `/register/magazine` | ✓ | → | → | → | → | → |
| `/articles/[slug]` (free) | ✓ | ✓ | ✓ | ✓ | · | ✓ |
| `/articles/[slug]` (premium) | → | → | · | · | · | · |
| `/articles/[slug]` (marketplace) | ✗ | → | ✗ | ✓ | → | · |
| `/u/[username]` | ✓ | ✓ | ✓ | ✓ | · | ✓ |
| `/m/[slug]` | ✓ | ✗ | ✗ | ✗ | · | ✗ |
| `/editor/new` | ✓→ | ✓ | ✓ | ✓ | n/a | · |
| `/editor/[id]` | ✓→ | · | **✗** | n/a | n/a | · |
| `/dashboard` | ✓→ | ✓ | ✓ | ✓→ | · | ✓ |
| `/dashboard/articles` | ✓→ | · | ✓ | ✓→ | · | · |
| `/dashboard/analytics` | ✓→ | · | ✓ | ✓→ | · | · |
| `/notifications` | ✓→ | ✓ | ✗ | ✓ | · | ✓ |
| `/settings` | ✓→ | ✗ | ✗ | ✗ | · | ✗ |
| `/search` | ✓ | ✓ | ✓ | ✓ | · | ✓ |
| `/discover` | ✓→ | ✓→ | ✓→ | ✓ | → | ✓→ |
| `/discover/writers/[username]` | ✓→ | ✓→ | ✓→ | ✓ | → | · |
| `/marketplace` | ✓→ | ✓→ | ✓→ | ✓ | → | ✓→ |
| `/library` | ✓→ | ✓→ | ✓→ | ✓ | → | ✓→ |
| `/dashboard/earnings` | ✓→ | ✓ | ✓ | ✓→ | · | · |
| `/subscription` | ✓→ | ✗ | ✗ | ✗ | · | ✗ |
| `/admin` | ✓→ | ✓→ | ✓→ | ✓→ | → | ✓ |

> **Rows changed 2026-08-23.** The writer's workspace nests under `/dashboard`, so
> `/dashboard/articles` and `/dashboard/analytics` join the matrix and `/earnings`
> becomes `/dashboard/earnings`. The legacy path still redirects and that redirect is
> asserted in `23-writer-dashboard.spec.ts` rather than assumed.
>
> The magazine column on all four writer rows moved from `✓` to `✓→`: those routes are
> personal-account territory — every endpoint behind them answers a magazine with 403 —
> so `proxy.ts` now sends a magazine to `/marketplace` instead of rendering four empty
> states. Previously this cell was recorded rather than asserted, on the grounds that the
> expected behaviour was unclear. It is no longer unclear.
>
> `·` on reader and admin for the two new rows is honest rather than lazy: both are
> personal accounts and both routes render for them, but no spec asserts it yet.

**Remaining cells (4):** the whole `mag. lapsed` column, which is blocked — cancelling a
subscription requires `/subscription`, and that page does not load for a magazine
account (`BUG-004`). Also not yet reached: `/articles/[slug]` (premium) for any persona,
because no premium article exists to visit until the paywall flow creates one.

## Flows

| flow | status |
|---|---|
| Register → publish → read | **✓ passes** — `08-flow-register-publish-read.spec.ts` |
| Premium paywall (free reader vs premium reader) | **blocked** — `BUG-011`: there is no UI to publish a premium article, and the seed has none |
| AI chat + inline editing + token counter | **✓ passes** — `09-flow-ai.spec.ts`, no findings |
| Like / comment / reply / follow / repost + notifications | **✓ passes** — `10-flow-social.spec.ts`; narrowed `BUG-006` |
| Marketplace: grant → list → subscribe → browse → preview → purchase → library → earnings | **✓ passes in full** — `11-flow-marketplace.spec.ts`, arithmetic verified |
| Moderation: report → queue → dismiss / remove article / ban | **✓ passes in full** — `12-flow-moderation.spec.ts` |

**Flow 1 passes** (`e2e/08-flow-register-publish-read.spec.ts`), with one obstacle found
on the way: a brand-new account registers and is signed in, writes in the TipTap editor,
saves a draft, publishes it Public, and the seeded reader then finds it via `/search`
and reads the full body back. The obstacle is `BUG-012` — the spec has to grow the
viewport to 1600px tall before it can press the dialog's Publish button.

**Flow 2 cannot be driven as written.** The brief asks for a free reader to be shown a
withheld body on a premium article. No premium article exists and none can be created
through the product (`BUG-011`). To test the reader-side paywall next session, set
`visibility = 'premium'` on an `E2E:` article directly in the database and drive the
reader half only — and record that mutation here.

**Flow 3 (AI) passes, no findings.** The chat panel opens, the prompt is echoed, a reply
streams back, and the counter moves — 1,000 → 226 on a single short question. All five
inline actions (Reformulate, Shorten, Expand, Simplify, Improve) appear on a selection,
and Shorten returned a suggestion with Replace enabled. Two notes: the token indicator
lives in the AI panel **header**, so it does not exist until the panel is opened; and the
AI panel is **article-scoped** — there is no AI control on an unsaved `/editor/new`.

**Flow 4 (social) passes.** Like, comment, reply, repost and follow all work against the
`E2E:` article, and all four produced correctly worded notifications for its author. This
is what **narrowed `BUG-006`** from "every notification" to the marketplace/earnings
types only.

**Flow 5 (marketplace) passes in full, and the arithmetic on screen is correct.** Driven
end to end at a listing price of 100 credits:

| step | on screen | correct |
|---|---|---|
| admin grants eligibility | Marketplace placement became selectable | ✓ |
| writer lists at 100 | card reads `100 credits` | ✓ |
| preview quoted | `Preview · 10` → `Confirm · 10 credits` | ✓ 10% of 100 |
| preview charged | balance 1045 → 1035 | ✓ exactly 10 |
| buy quoted after preview | `Buy · 90` → `Confirm · 90 credits` | ✓ the remainder, not the full price |
| purchase charged | balance 1035 → 945 | ✓ exactly 90 |
| total spent | 10 + 90 | ✓ = the 100 listing price |
| library | article present, `90 credits`, purchase date | ✓ |
| writer earnings | `90 paid − 18 platform fee → +72`, `10 paid − 2 platform fee → +8` | ✓ every row adds up |

The platform fee runs at 20%, and the writer's balance of 160 is exactly 2 × (72 + 8)
for the two listings this sweep sold.

**Flow 6 (moderation) passes in full.** A reader's report reaches the admin pending
queue, dismissing it moves it out of Pending and into Dismissed, "Remove article" (two
step, via "Confirm removal") makes the article unreadable, and "Ban author" (also two
step) blocks the account from signing back in. Two things were recorded on the way:
`BUG-014` (the removed article's URL becomes a blank page) and `BUG-015` (the banned
account is told "Invalid credentials").

---

## Session log

Newest first. Each entry: what was covered, what was found, where to resume, and what
was changed in the dev database.

### 2026-08-24 — Google sign-in wired; the spec reconciled with the code

Not a sweep. Two code changes and the specification corrections they belong with —
the remainder of the drift table opened after Phase 6.

- **Google OAuth (`SYNC-01`).** The known gap said "only the click handler is
  missing". It was not: `auth.controller.ts` redirects to
  `${FRONTEND_URL}/auth/callback`, and **that page did not exist**. The backend half
  had been complete and unreachable since it was written — a click handler alone
  would have delivered users to a 404 with their tokens in the URL. Built the
  callback route (server shell + client adopter), pointed the button at
  `/api/auth/google`, and gated the entry point on
  `NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED` because `GoogleStrategy` falls back to a
  literal `'not-configured'` client id rather than failing at boot — an
  unconfigured deployment would otherwise send users to Google's own error page.
  New spec: `e2e/24-google-oauth.spec.ts`, 6 tests. The round trip past Google's
  consent screen stays untestable here; `known-gaps.md` says why.
- **Auth rate limits (`SYNC-04`).** `POST /auth/login` at 10/min and
  `POST /auth/register` at 5/min, per IP. The global 60/min was a sane browsing
  ceiling and a useless password-guess ceiling. Counters are in-process memory, so
  the limit is per API process — NFR-05 now says so rather than implying a
  cluster-wide guarantee.
- **Twelve specification corrections.** The fee is 20% and not configurable; the AI
  quota is 1,000/day for premium personal accounts and magazines are excluded
  entirely; embeddings are Gemini, not OpenAI; there are eight services, not seven;
  Next.js 16, not 15; 200 wpm, not 250; `/discover` really is subscription-gated and
  the deviation saying otherwise was retired; the magazine NULL rule is
  application-enforced, not a CHECK constraint; `search_vector` documented for the
  first time; `'repost'` added to the notification enum; NFR-24 re-corrected because
  its own 2026-08-21 correction had gone stale.

Two things found that the drift table itself had wrong, and one it need not have
worried about:

- **The §13 environment catalogue was half fiction** — ten variables listed that no
  code reads, including four `LLM_*` knobs, three embedding knobs and the two
  eligibility thresholds (real values, but constants). Rewritten from
  `config/env.validation.ts`, which is the schema every variable must pass at boot.
- **All fourteen "10%" mentions across the spec are the *preview fraction*, which is
  correct.** The platform fee drift lived in one document. A find-and-replace on
  "10%" — the obvious way to execute that item — would have broken a rule that was
  right.
- **`fig-3-3-architecture-physical` needed no regeneration.** It already showed
  eight services with `migrate` named. The diagram was ahead of the prose.

**Four defects in the suite itself, all found by running it.** None were in the app.

1. **The suite depended on debris from its own past runs.** `seed-data.ts` carried
   three literals built from the timestamp `24136735` — the account and article that
   one run of flow 1 created in August 2026. Flow 1 mints a fresh stamp every run, so
   those constants never described the current run; they described rows left in the
   dev database, and four spec files consumed them. Removing that debris — which was
   done to get it out of the report's screenshots — broke five specs at once, each
   reporting something other than the cause: "no Like control on the article page"
   for an article that no longer existed, three login timeouts for a deleted account.
   Replaced with `e2e/fixtures/run-state.ts`: flow 1 writes what it created to
   `e2e/.auth/e2e-content.json`, the consumers read it, and reading before flow 1 has
   run raises an error that says it is an ordering problem.
2. **The base URL was written out four times** — `playwright.config.ts`, the auth
   fixture's hand-built context, three specs' `backend.inkwell.ai`, and the capture
   config. They only had to agree while nothing overrode them. Pointing the suite at
   an alternate port left logins going to the old one and **23 specs failed**, with
   the API calls reporting `SyntaxError: Unexpected token '<'` — the HTML of whatever
   was answering on port 80. Now one definition, `e2e/fixtures/base-url.ts`,
   overridable via `E2E_BASE_URL`.
3. **A search test that never waited.** `23-writer-dashboard` asserted
   `toHaveCount(await rows.count())` — the count equals itself, which passes instantly
   and waits for nothing. It then compared the pre-search row count against itself. It
   passed for months because the list happened to refresh before the next line ran; it
   started failing when the corpus shrank and the timing changed. Now it waits on the
   property that defines the result: no row survives that does not match the query.
4. **A fixture asserting an absence pointed at the wrong account.** "A free writer
   carries no badge" named `nadia-belhaj`, who is premium in the current seed. A spec
   that asserts an absence cannot fail loudly when its subject is wrong — it reports
   "a badge was found" and sends you looking at the badge component. Now
   `SEED.freeWriterUsername`, with a comment explaining why this one belongs in the
   fixture file rather than inline.

**One finding filed rather than fixed:** button-styled links announce as
`role="button"` — see `known-gaps.md`, Accessibility. It is one prop on a shared
primitive and wants its own pass.

### Session 2 — 2026-08-14 — flows 3–6 driven

- **Covered:** flows 3, 4, 5 and 6, all passing. Coverage cells unchanged at 62/66 — the
  4 that remain are the `mag. lapsed` column and are blocked on `BUG-004`.
- **Found:** 3 new findings — `BUG-014` (no not-found state on any content route),
  `BUG-015` (a banned account is told "Invalid credentials") and `BUG-016` (publish-time
  auto-moderation flagged an innocuous `E2E:` article as "hate"). `BUG-001` was **confirmed
  in the browser** for the first time and its screenshot attached; `BUG-006` was
  **narrowed** from "every notification" to the four marketplace/earnings types after the
  social flow showed like/comment/repost/follow rendering correctly.
- **The money path is correct.** Flow 5's arithmetic was checked at every step and every
  figure on screen is right — preview at 10% of price, purchase at the remainder, a 20%
  platform fee, and an earnings ledger whose rows add up. See the table above.
- **Two spec-quality fixes, not product changes.** `probe()` waited 1200 ms for a route
  to paint; the `/discover/writers` refusal takes ~1587 ms, which is what produced the
  withdrawn `BUG-008` and made that cell flake. The wait is now 3500 ms. Separately, the
  AI specs now **skip** when the account's allowance is exhausted rather than failing —
  the budget is real, finite and shared, and this sweep spent it.
- **Database changed:** substantially — see "Dev database state" below.
- **Stack health:** healthy throughout. No restarts, no port conflicts, `/api/health`
  green at the end of the session.
- **Suite state at end of session 2:** `100 passed, 10 failed, 2 skipped` on the
  non-mutating specs (the four flow specs that write to the database are run
  deliberately, not as part of a regression pass). Every failure maps to a filed
  finding: 4 × `/subscription` (`BUG-004`), the marketplace article page (`BUG-007`),
  the deleted-article editor (`BUG-013`), 3 × not-found (`BUG-014`) and the AI quota
  notice (`BUG-001`). The 2 skips are the AI tests on an exhausted allowance. The
  `/discover/writers` cell that flaked in session 1 is now stable.
- **Triaged (2026-08-14).** The 14 findings resolve to 8 causes; see `triage.md`. Three
  entries were corrected by diagnosis — `BUG-014`, `BUG-007` and `BUG-013` were all the
  same 7.5-second retry-on-404 delay being photographed as a missing state, which is a
  sweep error rather than an app one. The single highest-value change closes 3 findings.
- **Resume at:** nothing is left that is not blocked. `BUG-004` gates the last 4 cells
  (cancel a subscription to make the magazine lapse) and `BUG-011` gates flow 2. If
  either is fixed, those are the next things to drive. Otherwise the sweep is complete
  and the next piece of work is triage.

### Session 1 — 2026-08-14 — Playwright set up, all six persona columns swept

- **Covered:** 62 of 66 cells. Every route for guest, reader, writer, magazine and
  admin, including every refusal. Flow 1 driven end to end and passing; flow 2 blocked;
  flows 3–6 not started.
- **Set up:** Playwright installed (`@playwright/test` 1.62.1 + chromium), config and
  all three required fixtures written, plus a route probe and a column generator. Eight
  spec files, all committed as the beginnings of the Phase 6 suite.
- **Found:** 11 new findings, `BUG-003` … `BUG-013`, of which **two were withdrawn**
  after verification (`BUG-003`, `BUG-008`) — leaving 11 active overall. `BUG-002` was
  additionally confirmed in the browser and its screenshot attached.
- **One withdrawal worth reading.** `BUG-003` was filed Critical on the belief that a
  writer could not reopen their own draft. The article it was tested against turned out
  to be **soft-deleted**, so the 404 was correct. The editor opens live articles and new
  drafts fine, and flow 1 publishes successfully. Only the blank page in place of a
  not-found state survived, re-filed as `BUG-013` at Medium. Check `deleted_at` before
  trusting a 404.
- **A second withdrawal, `BUG-008`.** A route recorded as blank turned out to be an
  unpainted page on a cold dev server, not a missing empty state — it renders the
  correct refusal once warm. Re-visit a route before filing it as blank.
- **Suite state at end of session:** `98 passed, 6 failed`. Every failure is a filed
  finding, not a broken spec — 4 × `/subscription` (`BUG-004`), the marketplace article
  page (`BUG-007`), and the deleted-article editor (`BUG-013`).
- **The gates are sound.** This was the thing most likely to be wrong and it is not:
  every magazine-only route (`/discover`, `/marketplace`, `/library`) correctly refuses
  readers, writers *and* admins, `/admin` correctly refuses everyone but the admin, all
  ten middleware-protected routes bounce a guest to `/login` with a `?redirect`, and a
  marketplace article's body is withheld from everyone except the magazine that bought
  it. No gate let the wrong persona through. Two gates refuse without saying anything
  (`BUG-007`, `BUG-008`), but they do refuse.
- **Flows:** flow 1 (register → publish → read) driven and **passing**. Flow 2 blocked by
  `BUG-011`. Flows 3–6 not started.
- **Database changed:** 5 `E2E:` accounts and 5 `E2E:` articles created (one published,
  four drafts). No credits spent, nothing purchased, nobody banned, nothing deleted. See
  "Dev database state" below.
- **Stack health:** healthy throughout. All seven containers up for the whole session,
  `/api/health` returned `{"status":"ok"}`, no restarts, no port conflicts.
- **Resume at:** flow 3 (AI chat + inline editing + token counter), then flows 4–6.
  Before driving anything through the publish dialog, set a tall viewport — `BUG-012`
  makes its footer unreachable at 720px. `BUG-004` blocks the lapsed-magazine column
  outright, so those 4 cells stay open until it is fixed.

### Session 0 — 2026-08-14 — scaffolding only

Not a sweep. Prepared the directory and pre-populated `known-gaps.md` from a grep of the
frontend source so the agent does not rediscover twelve documented non-implementations
and file them as bugs.

- **Covered:** nothing in a browser.
- **Found:** `BUG-001` and `BUG-002` by code inspection — two controls disabled behind a
  `TODO(Phase 5)` whose blocker has since shipped. Both need browser confirmation and a
  screenshot.
- **Database changed:** nothing.
- **Resume at:** install Playwright, write the three fixtures, then start on the guest
  column.

---

## Dev database state

Sessions mutate the dev database — this is accepted. Record drift here so a later session
knows what it is looking at, and so the demo can be judged before a defence run.

### Current — after session 2

| | |
|---|---|
| Magazine credits | **945** — was 1145. Session 2 spent 200 buying two `E2E:` listings (10 + 90, twice) |
| `E2E:` accounts | **8** |
| `E2E:` articles | **14**, of which 2 marketplace listings (both sold) and 1 removed |
| Accounts banned | **1** — `e2e-mod-202645`, banned through the moderation queue |
| Articles removed | **1** — `E2E: Moderation remove 202645` |
| Reports | 2 dismissed, 2 resolved, **1 pending** |

Detail worth carrying forward:

- **`e2e-author-24136735` was granted marketplace eligibility** by an admin in flow 5.
  It is a free-plan personal account with `is_marketplace_eligible = true` and an
  earnings balance of **160** from the two sales — a useful fixture, and a state no
  seeded account is in.
- **AI allowances are spent.** `imane-farouk` is at **0** tokens (from 1,000) and
  `e2e-author-24136735` is at 0. The AI specs skip rather than fail while this is true;
  they exercise properly again once the allowance resets.
- **One pending report is left in the queue** — the auto-moderation false positive
  recorded as `BUG-016`, against `E2E: Moderation remove 120956`. Debris from an aborted
  first run of flow 6. Dismiss it before a demo, or keep it as that finding's
  reproduction.
- **Debris from aborted runs:** three `e2e-mod-*` accounts exist though only one was
  banned, and four `E2E: Publish and read` drafts from session 1 were never published.

### What session 1 created

All from the register→publish flow, all prefixed `E2E:`:

- **5 accounts** — `e2e-author-23787802`, `-23930922`, `-23996554`, `-24057797`,
  `-24136735` (`e2e-author-<stamp>@example.com`, demo password). Four are debris from
  runs that failed at `BUG-012` before the viewport workaround; only the last completed.
- **5 articles** — `e2e-publish-and-read-<stamp>`. Four left as **drafts**, one
  **published public**: `e2e-publish-and-read-24136735`.

Session 1 purchased nothing, banned nobody and deleted nothing; all of that came in
session 2.

**Restoring:** `pnpm db:seed` resets the seeded accounts and content, but also wipes
article embeddings — `pnpm db:embed-backfill` afterwards (real Gemini calls) before the
AI and search screens look right again.
