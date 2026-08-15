# Agent prompt — UI bug sweep

Paste everything below the line into a fresh agent session. It is written to be
self-contained: assume the agent knows nothing about this project.

---

You are running a **bug discovery sweep** on Inkwell.ai, a Next.js + NestJS publishing
platform with a credit-based article marketplace. Everything is built and merged;
almost none of it has ever been opened in a browser. Your job is to drive every screen
with Playwright, **record what is broken, and fix nothing**.

## The one rule

**Do not fix. Do not diagnose. Do not investigate causes.**

When something fails, capture it and move on. Resist the pull to open the source and
find out why — a complete catalogue of accurate symptoms is worth far more right now
than three well-understood bugs and twenty screens nobody looked at. Triage is the next
piece of work and it is not yours.

The one exception is the known-gap check below, which is a `grep`, not an investigation.

## Read first

`spec.inkwell.ai/review-test/progress.md` — the coverage matrix and session log. It is
the resume point. Earlier sessions may have covered most of this already; start where it
says to start, not at the beginning.

## The stack

Runs under Docker Compose from `docker.inkwell.ai`.

- App: **`http://frontend.inkwell.ai`** — plain HTTP. There is no TLS locally, and a
  browser that auto-upgrades to `https://` gets `ERR_CONNECTION_REFUSED`.
- API: `http://frontend.inkwell.ai/api` — `GET /api/health` returns `{"status":"ok"}`.
- Check with `docker ps`: you want `inkwell-web-1`, `inkwell-api-1`, `inkwell-nginx-1`,
  `inkwell-db-1`. The app services sit behind the compose `apps` profile, so if they are
  missing:

  ```
  cd docker.inkwell.ai
  docker compose -f .infra/compose/docker-compose.dev.yml --env-file .env \
    --profile apps up -d
  ```

If nothing resolves at all, check that no host nginx or apache is holding port 80 —
`docker port inkwell-nginx-1` should print two lines. This has happened before; it is
written up in `spec.inkwell.ai/HOW-IT-RUNS.md` §9.

## Step 1 — set Playwright up

**It is not installed.** No dependency, no config, no test directory.

```
cd frontend.inkwell.ai
pnpm add -D @playwright/test
npx playwright install chromium      # ~130 MB
```

**If that download fails because the sandbox has no network, stop and report it.** Do not
build a workaround, do not try another runner. It blocks the task and the user needs to
know rather than receive something improvised.

Then write these three fixtures **before any spec**:

**1. Auth per persona.** Log in through the real form and save `storageState`.
Authentication lives in **two** places — localStorage *and* an `access_token` cookie —
because the Edge middleware can only read the cookie. See
`src/lib/api/auth-storage.ts`, whose own comment records the bug that came from writing
only one. `storageState` captures both, so log in properly and save; **do not hand-inject
tokens**.

Access tokens expire after **15 minutes**. A long run crosses that boundary, and while
the app's refresh interceptor handles it in-page, a `storageState` saved once globally
will go stale. Re-authenticate per spec file.

**2. An error collector.** In `beforeEach`, subscribe to:

- `page.on('pageerror')` — uncaught exceptions
- `page.on('console')` filtered to `error`
- `page.on('response')` where `status() >= 400`

Accumulate per test and attach to the report. **This is the highest-value thing you will
write.** The user has already seen Next.js errors in the browser; this catches them, and
catches them on screens that look perfectly fine.

**3. A screenshot helper** writing `screenshots/<route>--<persona>.png` into
`spec.inkwell.ai/review-test/` for every screen visited.

The specs are **kept**. They become the project's Phase 6 E2E suite, so write real
assertions and commit them — this is not throwaway driving code.

## Accounts

Password `InkwellDemo123!` for every one.

| persona | account | notes |
|---|---|---|
| guest | — | signed out |
| reader | `hakim@example.com` | free plan, role `reader` |
| writer | `imane@example.com` | premium, marketplace-eligible, has published work |
| magazine | `editors@longformreview.example.com` | subscribed, ~1000 credits |
| magazine (lapsed) | same account | cancel via `/subscription`, test, then re-subscribe |
| admin | `admin@inkwell.ai` | role `admin` |

## Step 2 — coverage

Every route, for every persona that can reach it:

`/` · `/login` · `/register` · `/register/magazine` · `/articles/[slug]` ·
`/u/[username]` · `/m/[slug]` · `/editor/new` · `/editor/[id]` · `/dashboard` ·
`/notifications` · `/settings` · `/search` · `/discover` ·
`/discover/writers/[username]` · `/marketplace` · `/library` · `/earnings` ·
`/subscription` · `/admin`

Where a persona should be **refused**, assert the refusal rather than skipping the cell:

- a guest on `/dashboard` → redirected to `/login?redirect=…`
- a reader on `/admin` → a refusal state, not a crash and not the queue
- a personal account on `/marketplace` → told it is for magazines
- an unsubscribed magazine on `/marketplace` → told to subscribe

**The gates are the single most likely thing to be wrong.** A gate that silently lets the
wrong person through is Critical, and you will only find it by trying.

## Step 3 — flows

Screens in isolation miss the interesting failures. Drive these end to end:

1. **Register → publish → read.** New account, write an article, publish it public, read
   it back as another persona.
2. **The premium paywall.** A free reader on a premium article should see the body
   withheld and an upgrade route. A premium reader should see the body.
3. **AI.** Chat panel in the editor, inline editing actions, the token counter.
4. **Social.** Like, comment, reply, follow, repost — and the notifications they produce.
5. **The marketplace, whole.** Admin grants eligibility on `/admin` → writer publishes to
   the marketplace with a price → magazine browses `/marketplace` → previews (10% of
   price) → purchases (the remainder) → the article appears in `/library` → the writer's
   `/earnings` shows both payouts. **Check the arithmetic on screen**, not just that the
   buttons work.
6. **Moderation.** Report an article as a reader → it appears in `/admin` → dismiss it;
   then report another and remove the article; then ban an account you created.

## Mutations are allowed

You may spend credits, publish, purchase, ban and delete against the dev database. This
is expected and accepted.

Two constraints:

- **Prefix everything you create with `E2E:`** — article titles, usernames, magazine
  names. It has to be identifiable afterwards.
- **Prefer acting on what you created.** When a flow needs something banned or deleted,
  use your own `E2E:` content rather than a seeded account the demo depends on.

Record what you changed in `progress.md` as you go.

## Before filing anything: the known-gap check

Twelve frontend files document deliberate non-implementations — `NOT WIRED UP`,
`TODO(Phase N)`, `disabled so it can't 404`. **The "Continue with Google" button is one
of them**: `src/components/shared/google-oauth-button.tsx` states plainly that it has no
handler by design. Placeholder like/comment counts on article cards and the greyed
"Following" / "Analytics" nav entries are others. `known-gaps.md` already lists the ones
found so far.

So when a control does nothing:

1. `grep` the component for `NOT WIRED`, `TODO(`, `disabled`.
2. If a marker exists → `known-gaps.md`, with the comment quoted. **Not a bug.**
3. If none exists → it is a finding.

**One trap.** A `TODO(Phase 5)` marker may now be **stale**, because Phase 5 has shipped.
A control disabled pending something that now exists *is* a real finding. Two are already
filed this way as `BUG-001` and `BUG-002` — read them before you start so you recognise
the pattern.

Filing known gaps as bugs buries the real findings. Filing stale gaps as known gaps hides
them. Both matter.

## Recording

Everything goes in `spec.inkwell.ai/review-test/`.

Severity by **consequence**, not by appearance:

- **Critical** — data loss · money computed or moved wrongly · an access gate bypassed ·
  a core flow that cannot complete at all
- **High** — a core flow blocked for one persona, or a visibly wrong result
- **Medium** — misbehaves, but there is a workaround
- **Low** — cosmetic, copy, spacing, a missing empty state

Each finding, into `bugs.md` under its severity:

```markdown
### BUG-0NN — one-line summary

- **Route:** /marketplace
- **Persona:** magazine (subscribed)
- **Expected:** …
- **Actual:** …
- **Screenshot:** screenshots/marketplace--magazine.png
- **Console/network:** … or "none captured"
```

IDs are sequential and **never reused**, including for findings later found invalid —
mark those `WITHDRAWN` rather than renumbering. **No cause, no file references, no
proposed fix.**

## Resuming

This will not finish in one session. **Keep `progress.md` current as you go, not at the
end** — a session that dies mid-run should still leave an accurate resume point.

It carries the route × persona matrix, a session log (date, what was covered, where to
resume), and the dev-database state. Assume the next session starts completely cold with
only these files and no memory of yours.

## When the session ends

Report:

- cells covered / cells remaining
- counts by severity
- anything **Critical**, quoted in full
- whether the stack stayed healthy throughout

Give the counts and let the reader judge. Do not characterise the findings as "mostly
minor" or "nothing serious" — that is the reader's call, and a sweep that editorialises
its own results is less useful than one that just reports them.
