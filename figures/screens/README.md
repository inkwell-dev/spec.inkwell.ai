# Screen captures

The application screenshots the report uses. Unlike `diagrams/`, these are raster and
they are the source — there is no vector original to re-render them from, so they are
committed rather than ignored.

Captured against the dev stack **with its clock at 2026-07-31**, the last day of the
project window the report presents — so every date a figure shows falls inside it.
1280×800 at ×2 (the AI figures 1440×900), light theme, Chromium, the Next.js dev overlay
and the React Query devtools button suppressed.

## Regenerating

Driven from the superproject, not by hand — the clock is the reason:

```bash
cd docker.inkwell.ai
make dciup-capture      # the stack on the report's clock (2026-07-31)
make capture-seed       # fresh full seed, no date before 2026-02-01 — REPLACES dev data
make capture            # sitting 1: every figure that can show a date
make capture-real       # sitting 2: the AI and document figures (needs the embedding quota)
mv src/frontend.inkwell.ai/capture/figures/*.png spec.inkwell.ai/figures/screens/
make dciup-all          # back to the real clock
```

`.infra/compose/docker-compose.capture.yml` explains how the clock is moved and why the
database moves with it; `src/frontend.inkwell.ai/capture/README.md` carries what each
figure needs. Two sittings because the AI providers' TLS certificates postdate the
report's clock: the AI figures run with the api and worker on the real clock and
everything a screen shows — the database, the web app, the browser — still on the
report's.

## Naming

`<persona>-<nn>-<screen>.png`. The number orders the screens within a persona's journey;
it is **not** the report's figure number. Assign those when the chapters are written and
reference these files by name, the way `diagrams/README.md` does for the UML figures.

| Prefix | Account | What it is there to show |
|---|---|---|
| `guest-` | signed out | the public surface, both registration paths (with Google sign-in), the premium gate, a licensed article |
| `reader-` | `lena@example.com` | the free plan, so the paywall and upgrade prompt are real; Sprint 7's saved shelf, blocked accounts, following feed, follower search and Reposted tab |
| `writer-01…08`, `writer-12…19` | `nadia@example.com` | the dashboard, My articles, the editor, both AI surfaces, notifications, and Sprint 8–9's assistant, write, document library, sources, citations and voice |
| `writer-09…11` | `yusuf@example.com` | the two-stage sale, itemised |
| `magazine-` | `editors@longformreview.example.com` | subscribed, licensing; publishing from its library (Sprint 5) |
| `admin-` | `admin@inkwell.ai` | the moderation console |

## Added for Chapter 7, and for Sprint 5's licensing

| Figure | Shows | Requirement |
|---|---|---|
| `reader-05-saved` | the Saved shelf | FR-63/64 |
| `reader-06-blocked-accounts` | blocked accounts, from settings | FR-62 |
| `reader-07-following-feed` | the following feed | — |
| `reader-08-followers-search` | a follower list, searched | FR-61 |
| `reader-09-reposted-tab` | the Reposted tab of a profile | FR-67 |
| `guest-10-licensed-article` | a licensed article under the magazine's masthead | FR-76 |
| `magazine-09-publish-from-library` | publishing what the magazine bought | FR-73/74 |
| `writer-14-ai-keep-discard` | a write awaiting Keep or Discard | FR-79 |
| `writer-15-ai-rail-live-step` | the live step on the collapsed rail | FR-80/81 |
| `writer-16-document-library` | the library, one document refused with its reason | FR-84 |
| `writer-17-ai-sources-tab` | the Sources tab, a document attached | FR-85 |
| `writer-18-ai-cited-reply` | a reply citing `[Title, p. N]` | FR-86 |
| `writer-19-voice-recording` | recording a prompt | FR-82 |

**Still to take: sitting 2** — `writer-03`, `writer-05…08` and `writer-14…19`, which need
the embedding provider's daily quota. Until then `writer-03` and `writer-05…08` here are
the previous set's.

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

- **`magazine-01-marketplace`** — listings priced in credits, each with its preview
  price (10%) beside the full one: Preview · 14 / Buy · 147. This is what §4.5.5 describes.
- **`writer-09-earnings`** — the split payment as the writer sees it, at both levels: the
  KPI row separates `9` preview payouts from `85` purchase payouts against a `94`
  lifetime total, the Revenue by article table attributes them to two pieces each bought
  by one magazine, and the payout history itemises each stage — `PURCHASE +44` (54 paid,
  10 fee), `PREVIEW +4` (5 paid, 1 fee).
- **`admin-03-report-queue`** — reports across `PENDING` / `REVIEWED` / `DISMISSED`,
  including one with no reporter shown. That row is the platform's publish-time
  classifier (`reports.reporter_id IS NULL`, see `6-database-schema.md`), and it is in
  the seed specifically so the LEFT JOIN that path needs is visible in a figure.
