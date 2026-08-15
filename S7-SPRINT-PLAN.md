# S7 — Sprint Plan

**Aug 24 – Sep 6** · the last sprint · Phase 6 only

> **Confirmed 2026-08-15.**
>
> - **Defense: week of Sep 7–13.** S7 closes Sep 6, so the defense lands days
>   after it. The schedule below works as drafted — but there is no recovery week
>   behind it, which is why the deploy moves to the front rather than the end.
> - **The report is tracked outside this plan** and is already underway. Phase 6
>   stays focused on the product; nothing here schedules writing it.
> - **Phase 5's token top-up:** design decided, deliberately not built. The
>   decision and the shape to build are recorded on the item itself in
>   `0-phase-plan.md`.
>
> **Still open:** whether the domain and VPS get bought in the pre-sprint window
> below, or wait for S7 to open. That is the one unanswered question in this plan,
> and it is the one with the most schedule risk attached.

---

## Phase 6 is smaller than it looks

The section carries 43 unchecked boxes. **Nine are already satisfied** — verified
against the code, not assumed:

| Item | Evidence |
|------|----------|
| Playwright E2E — all critical flows *(parent + 5 children)* | `08` register→publish→read · `09` chat + inline · `10` like/comment/follow · `15`+`21` premium gate |
| Fix all TypeScript strict errors | Both repos are `"strict": true` and `tsc --noEmit` exits 0 |
| Demo seed script | Phase Q built it: 5 writers, 12 articles, ~1,250 analytics events, a subscribed magazine |
| Demo scenario — eligibility → list → preview → purchase | `11-flow-marketplace` + `22-phase5-marketplace-demo`, both green |

Ticked 2026-08-15. Phase 6 now reads **34 open**, not 43.

## The one decision that has expired

`0-phase-plan.md` still carries the 2026-08-10 decision that **deployment is the
last work of the last sprint**, and the S7 row still describes the deploy block as
*"blocked on buying a domain and a VPS"*.

Both statements were written when feature work was unfinished, and the point was
that deploy must not steal time from features. **Features are now finished** —
Phases 1–5 are closed and verified. The rationale has lapsed, and the S7 row is
additionally stale on its own terms: the Phase 6 section already supersedes it,
noting the Student Pack supplies a free `.me` domain and $200 of DigitalOcean
credit, making it *"a scheduling decision rather than a hard block"*.

Holding deploy to the end **now** converts a de-risking decision into a risk.
Deployment is the only work in Phase 6 with dependencies this project does not
control: domain registration, DNS propagation, VPS provisioning, a first
production database, TLS issuance against a real hostname. Every one of those can
fail on someone else's timetable.

**Recommendation: move the deploy block to the front.** It is the critical path.

---

## Pre-sprint window — Aug 15–23 (9 unscheduled days)

Nothing is scheduled here. Spend it on the things with external latency, so S7
opens with the risk already retired.

- [ ] **Claim the `.me` domain** (Namecheap, Student Pack). Registration plus DNS
      propagation is wall-clock time nobody can compress.
- [ ] **Provision the VPS** (DigitalOcean, $200 pack credit).
- [ ] **Configure DNS** — two records, the apex and `storage.` for presigned
      uploads, per the note in the phase plan.
- [ ] **Create the Sentry project**, get both DSNs.
- [x] Tick the nine already-satisfied boxes above — *done 2026-08-15; Phase 6 now reads 34 open.*

If the domain and VPS exist before Aug 24, S7 has no external dependency left in
it at all.

## Week 1 — Aug 24–30 · get it live, then measure it

**Deploy (the critical path).**

- [ ] Set the four GitHub repository variables — deliberately empty today so
      images do not bake in a domain nobody owns; that reason is gone once the
      domain is real
- [ ] GitHub Actions deploy workflow: `repository_dispatch` trigger → SSH → pull
      → `docker compose up -d`
- [ ] Automatic migrations on deploy. The one pending migration is additive
      (`notification_type` gained `'repost'`) and production has never existed,
      so it lands with the value present — but the *mechanism* still needs to work
- [ ] Verify the full stack at the production URL

**Then quality, against the deployed instance where it matters:**

- [ ] Lighthouse >90 on article pages — run it against production, not localhost;
      the numbers differ and only one of them is the number
- [ ] `axe-core` scan, fix criticals
- [ ] XSS / input sanitization audit — narrow and worth doing properly. TipTap
      content is stored as JSON and rendered through the editor rather than
      `dangerouslySetInnerHTML`; the sweep's `ts_headline` note records that the
      codebase has **no** `dangerouslySetInnerHTML` today. The audit is to confirm
      that is still true and to check comment rendering

## Week 2 — Aug 31 – Sep 6 · the artefacts a defense is graded on

**SEO** (small, do it early in the week):

- [ ] `/sitemap.xml` from published articles
- [ ] JSON-LD `Article` on article pages
- [ ] `<meta>` description from excerpt
- [ ] ~~Dynamic OG images~~ — the plan itself marks this *"stretch — zero demo
      value"*. **Cut unless everything else is done.**

**Demo mode:**

- [ ] `DEMO_MODE=true` with lowered eligibility thresholds (5 readers + 2
      reactions) so a writer can cross the line live in front of an examiner. The
      real thresholds are 5,000 identified readers and 1,000 reactions — the
      seeded corpus reaches 11, so without this the demo's opening beat cannot be
      performed
- [ ] `reconcile-balances` job — asserts snapshot == ledger sum. Cheap, and it
      backs a claim worth making on a marketplace project

**Defense preparation** — the largest block, and the one that is graded:

- [ ] `docs/ARCHITECTURE.md` — a good part of it can be lifted from
      `HOW-IT-RUNS.md`, which already walks nginx, the containers, and the request
      path browser → Postgres
- [ ] `docs/RAG.md` — chunking → embedding → retrieval → prompt injection. The
      Phase 4 verification record already holds the measured fusion figures and
      the retrieval evidence
- [ ] `docs/AI-DESIGN.md` — reconcile the original spec with what was built
- [ ] `spec.inkwell.ai` — update the specs to match what shipped
- [ ] **Demo script**, 10 minutes
- [ ] **Slide deck**, 15–20: problem + solution · architecture diagram · RAG
      deep-dive · demo screenshots · stack rationale · metrics
- [ ] **Backup demo video** — record it the day the deploy is verified, while the
      environment is known-good
- [ ] **Rehearsal ×2**

---

## The demo script writes itself

Every beat of the intended demo is now a passing, recorded walkthrough. The script
is a matter of ordering evidence that already exists:

| Beat | Already proven by |
|------|-------------------|
| Register → write → publish → read | `08-flow-register-publish-read` |
| AI chat drawing on the writer's own corpus | Phase 4 record — the parking-minimums answer reusing her setback argument |
| "Sources used", with real chunk IDs | Phase 4 record — 5 chunks, top similarity 0.668, 0 belonging to anyone else |
| Hybrid search finding what shares no words with the query | Phase 4 record — `0 lexical + 2 semantic → 2 fused` |
| Admin grants eligibility → writer lists | `11-flow-marketplace` |
| Magazine reads the evaluation + Portfolio Insights | `22-phase5-marketplace-demo` |
| Preview 10% → purchase remainder → library → payouts | Ledger: 10 = 8+2, 90 = 72+18 |
| Moderation: report → queue → remove → ban | `12-flow-moderation` |

The strongest single moment is the semantic search case: **no article contains the
searcher's words and the right results still come back.** It is one line of typing
and it demonstrates the headline claim.

## Contingency

With the defense in the week of Sep 7–13 there is **no buffer week** after S7 —
whatever is unfinished on Sep 6 is unfinished at the defense. Cut in this order;
the first two cost nothing that is graded:

1. **Dynamic OG images** — the plan already calls this zero demo value
2. **`reconcile-balances`** — defensible as future work; the ledger invariants are
   already tested
3. **`docs/AI-DESIGN.md`** — fold the essentials into `docs/RAG.md`
4. **One rehearsal** — keep at least one, and keep the backup video

**Do not cut:** the deploy, `DEMO_MODE` thresholds, the demo script, or the backup
video. A live URL is worth real marks on a DevOps-heavy project; the thresholds
are what make the demo's first beat performable; and the video is the only
insurance against the live demo failing in the room.

Note the standing **BI-trim contingency** from the 2026-07-26 re-baseline is now
moot — it applied to S6, which closed early with everything shipped.

## Open question

**Domain and VPS: buy now, or wait for S7?** Everything else in this plan is
settled. This is the only external dependency left in the project, and with the
defense a few days after S7 closes there is no week in hand to absorb a
registration or propagation delay. The pre-sprint window exists precisely to
retire it early.
