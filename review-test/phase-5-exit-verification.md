# Phase 5 — Exit Criteria Verification

**Date:** 2026-08-15 · **Result: 3 of 3 pass** (one after a fix)

Driven in a real browser against the running stack. The marketplace figures below
are the ones the app actually charged, read back from the ledger.

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Upgrade changes plan and unlocks premium articles **+ AI features** | **PASS** — after fixing the AI half |
| 2 | Reported content appears in the admin queue | **PASS** |
| 3 | Marketplace end-to-end demo | **PASS** |

---

## 1. Upgrade flow — PASS (the AI half needed a fix)

`15-flow-premium-paywall` already proved the paywall, but with two *different*
pre-existing accounts. That shows the gate works; it does not show that upgrading
moves an account across it, which is what the criterion asks. So
`e2e/21-phase5-upgrade-flow.spec.ts` drives one account through the transition.

**Premium articles — passes.** A newly registered free account is shown the
paywall on a seeded premium article; after upgrading on `/subscription` and
re-authenticating, the same account receives the same article's body.

The re-authentication is not a workaround. The plan is a claim inside the access
token, minted at login, and the API reads the claim rather than the database.
`/subscription` states this outright rather than leaving the reader to find a page
that still looks locked.

### AI features — did not hold, and was fixed

As first run, a freshly-upgraded premium account had **no AI access at all**
until the nightly reset at UTC midnight.

Measured directly against the API:

```
GET /ai/tokens   -> {"remaining":0}
POST /ai/chat    -> (guard grants 1000, the request spends 218)
GET /ai/tokens   -> {"remaining":782}
```

**Why.** `AiQuotaGuard` grants the daily allowance on demand, but it only runs on
`/ai/chat` and `/ai/inline`. `GET /ai/tokens` calls `AiService.getTokenCount`,
which is a plain `SELECT` of `users.ai_tokens_remaining` — a column that defaults
to 0 and that only the nightly job otherwise writes.

**Why it is a dead end rather than a cosmetic zero.** `useAiQuota` derives
`exhausted` from that read, and `ai-chat-panel.tsx` disables the textarea and the
send button and returns early from submit when `exhausted`. So the user cannot
issue the one request that would have granted their tokens.

**This is the defect the guard was written to prevent.** Its own comment names the
scenario — *"A user whose plan becomes premium at 00:05 UTC has 0 tokens until the
next night's run — roughly 24 hours of a paid feature not working"* — and states
the principle: *"Granting on read makes the entitlement self-healing."* The guard
applies that to the AI routes; the endpoint the UI actually gates on was left as a
plain read, so the protection does not reach the path that needs it.

**The fix.** The grant statement moved out of the guard into
`readQuotaGrantingIfDue` in `ai-token-allowance.ts`, beside the SQL fragments it
is built from, and both the guard and `AiService.getTokenCount` now call it. Any
path that reports the balance grants on the same terms as the paths that spend
it, or the two disagree about what the account is entitled to.

Verified afterwards on a fresh account that had never made an AI request:

```
as FREE                       -> {"remaining":0}      (0 by design)
as PREMIUM, no AI request yet -> {"remaining":1000}   (read 0 before the fix)
```

Spec 21 step 4 asserts this directly. It was briefly a `test.fail()` marker while
the defect stood; that came out with the fix.

## 2. Reported content reaches the admin queue — PASS

`12-flow-moderation`, 5 steps, all green:

1. A disposable author with three articles is set up
2. A reader reports an article
3. The report reaches the queue and can be dismissed
4. An admin removes a reported article
5. An admin bans the account behind a report

The ban's login refusal reads *"This account has been suspended. Contact support if
you think this is a mistake."* — and the enumeration guard holds: the same banned
account with a **wrong** password still returns a generic `401 Invalid credentials`,
so the suspension message cannot be used to test whether an address exists.

## 3. Marketplace end-to-end demo — PASS

Eight steps, split across two specs because step 4 only became possible on
2026-08-15.

**Steps 1, 2, 3, 5, 6, 7, 8** — `11-flow-marketplace`, 6 tests, green. Admin grants
eligibility → writer lists at 100 credits → magazine finds it at the right price →
previews → purchases → library → earnings.

**Step 4 — "views writer evaluation + Portfolio Insights"** — `22-phase5-marketplace-demo`,
3 tests, green. This step was previously unwalkable: the evaluation page carried no
listings, so the magazine had to leave for `/marketplace` and find the writer again
by search. The licensing panel merged earlier the same day closes it, and this spec
completes the purchase **from the evaluation page** — the first time credits have
been spent through that panel.

### The arithmetic, as charged

Magazine credit balance, read from the nav indicator:

```
445 -> 435   preview   (10, being 10% of the 100-credit price)
435 -> 345   purchase  (90, the remainder — the preview is credited, not re-charged)
```

The purchase dialog states *"Already paid at preview"* rather than quoting a bare
90 on a 100-credit article, which would read as an unexplained discount.

And the ledger rows the platform actually wrote:

| Stage | Magazine pays | Writer nets | Platform fee |
|-------|---------------|-------------|--------------|
| Preview | 10 | 8 | 2 |
| Purchase | 90 | 72 | 18 |
| **Total** | **100** | **80** | **20** |

Three rows per stage, not two — the deviation already recorded in the phase plan.
The 20% platform fee holds at both stages, and the writer's payouts landed against
the correct account.

---

## A spec fragility found by the full-suite run, and fixed

`22-phase5-marketplace-demo` passed in isolation but failed once in a full-suite
run, at step 4c, with the confirm button disabled.

**The app was right.** The magazine was down to 35 credits — `11-flow-marketplace`
spends 100 on the same account earlier in every run, and each previous run took
its own 100 — so a 90-credit purchase was genuinely unaffordable. The purchase
dialog predicted the shortfall and disabled the control, which is exactly §4.5.7's
"graceful rejection with clear UX and prompt to top up".

The spec was the fragile part: its result depended on how many times the suite had
been run before. Its setup now tops the magazine up when the balance is below
twice the price, alongside seeding its listing.

`11-flow-marketplace` has the same latent dependency and will eventually hit it
from the other side. Left alone here — it currently passes, and widening this pass
to rewrite it would have buried the finding.

## Dev DB drift from this pass

- One new premium article and one new marketplace listing, both `E2E:`-prefixed,
  authored by `imane-farouk`
- Two new `e2e-upgrade-*` accounts, one left on the premium plan
- The magazine's credit balance moved 445 → 435 across the walkthroughs, including one 500-credit top-up the spec issued when it ran low
- `12-flow-moderation` and `11-flow-marketplace` left their usual debris, already
  described in `progress.md`
