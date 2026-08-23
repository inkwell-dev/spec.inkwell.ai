# Screen captures

The application screenshots the report uses. Unlike `diagrams/`, these are raster and
they are the source — there is no vector original to re-render them from, so they are
committed rather than ignored.

Captured on **2026-08-22** against the dev stack, all in one run so the set matches:
1280×800, ×2 device pixel ratio, light theme, Chromium, the Next.js dev overlay and the
React Query devtools button suppressed.

## Regenerating

They are produced by a Playwright runner in the frontend repo, not by hand:

```bash
cd docker.inkwell.ai/src/frontend.inkwell.ai
npx playwright test --config capture/playwright.capture.ts
mv capture/figures/*.png ../../../spec.inkwell.ai/figures/screens/
```

`capture/README.md` there carries the prerequisites — the stack has to be up, seeded and
embedded, and four of the figures cost either AI tokens or a dialog that must not be
confirmed. Read it before re-running.

## Naming

`<persona>-<nn>-<screen>.png`. The number orders the screens within a persona's journey;
it is **not** the report's figure number. Assign those when the chapters are written and
reference these files by name, the way `diagrams/README.md` does for the UML figures.

Six accounts across five personas, because the seed puts the only draft on one writer and
the only sales on another:

| Prefix | Account | What it is there to show |
|---|---|---|
| `guest-` | signed out | the public surface, both registration paths, the premium gate |
| `reader-` | `hakim@example.com` | free plan, so the paywall and upgrade prompt are real |
| `writer-01…08`, `writer-12`, `writer-13` | `nadia@example.com` | the dashboard overview, My articles, drafting, the editor, both AI surfaces, notifications |
| `writer-09…11` | `yusuf@example.com` | the two-stage sale, itemised |
| `magazine-` | `editors@longformreview.example.com` | subscribed, 953 credits, one article licensed |
| `admin-` | `admin@inkwell.ai` | the moderation console |

## Captured whole, 2026-08-23

All 37 figures come from one sitting against a freshly seeded database, which is what
this directory has always asked for and had not had.

Getting there took three things worth knowing, because each will recur:

**The seed could not re-run.** Its cleanup deleted `ai_interactions` but not
`user_ai_memory`, which carries the same foreign key to `users` — so the first reseed
after anyone used the AI chat failed on `user_ai_memory_user_id_users_id_fk` having
already deleted everything else. Fixed in the backend.

**Seven of nineteen published articles were E2E artefacts.** The suite prefixes what it
creates with `E2E:` precisely so it is identifiable as debris, but the seed only removes
users it owns, so E2E-created accounts and their articles survive every reseed. They were
appearing in the feed, search and profile figures. Removed before capturing.

**`magazine-03-purchase-confirm` had never captured.** Its test skips when the listing has
no `Preview ·` control, and every seeded marketplace article had been previewed or
purchased by earlier E2E runs. A reseed restores an untouched listing; the figure now
shows the dialog with real arithmetic — 12 credits against a 120-credit listing, balance
953 → 941.

A reseed regenerates article ids, so `e2e/fixtures/seed-data.ts` and the capture spec's
own `draftId` both need re-verifying afterwards. Everything else in both is addressed by
slug for exactly this reason.

## Recaptured in Phase 6

The writer's routes moved under `/dashboard` and two pages that §6 specified were built
for the first time. The left sidebar changed with them — it now carries the writer's
workspace as its own block — and the sidebar appears in every figure, so the WHOLE SET
was recaptured in one sitting rather than patched figure by figure. The table below is
what changed in substance; everything else changed only in its navigation column.

| Figure | What changed |
|---|---|
| `writer-01-dashboard` | now the designed overview — welcome row, four KPI cards, recent articles, eligibility — rather than the master/detail list it was |
| `writer-10-dashboard-analytics` | **had been a second photograph of `/dashboard`**, because no analytics page existed. It now shows the page it has been named after since the figure list was drawn up |
| `writer-13-my-articles` | new. The searchable, date-filterable article table. Appended rather than renumbered, because the report references figures by name |
| `writer-09-earnings` | moved to `/dashboard/earnings`, and gained the preview/purchase KPI split and the per-article revenue table that FR-37 asks for |
| `writer-12-notifications` | filter pills, date grouping, mark-all-as-read, and rows that link through to their subject |
| `writer-02-own-profile` | the Articles tab shows this writer's real work. It previously showed four invented articles, identical on every profile in the product |
| `reader-04-settings` | location and website fields |

## The three that carry the most

- **`magazine-01-marketplace`** — the three listings in three different states at once:
  previewed (75 credits, 68 outstanding), untouched (preview 12 / buy 120), and already
  in the library. This is what §4.5.5 describes.
- **`writer-09-earnings`** — the split payment as the writer sees it, now at both
  levels: the KPI row separates `4` preview payouts from `29` purchase payouts against
  a `33` lifetime total, the Revenue by article table attributes all of it to one piece
  bought by one magazine, and the payout history itemises `PREVIEW +4` (4 paid, 0 fee)
  then `PURCHASE +29` (36 paid, 7 fee).
- **`admin-03-report-queue`** — reports across `PENDING` / `REVIEWED` / `DISMISSED`,
  including one with no reporter shown. That row is the platform's publish-time
  classifier (`reports.reporter_id IS NULL`, see `6-database-schema.md`), and it is in
  the seed specifically so the LEFT JOIN that path needs is visible in a figure.
