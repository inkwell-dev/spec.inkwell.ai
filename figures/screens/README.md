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
| `writer-01…08`, `writer-12` | `nadia@example.com` | drafting, the editor, both AI surfaces, notifications |
| `writer-09…11` | `yusuf@example.com` | the two-stage sale, itemised |
| `magazine-` | `editors@longformreview.example.com` | subscribed, 953 credits, one article licensed |
| `admin-` | `admin@inkwell.ai` | the moderation console |

## The three that carry the most

- **`magazine-01-marketplace`** — the three listings in three different states at once:
  previewed (75 credits, 68 outstanding), untouched (preview 12 / buy 120), and already
  in the library. This is what §4.5.5 describes.
- **`writer-09-earnings`** — the split payment as the writer sees it: `PREVIEW +4`
  (4 paid, 0 fee) then `PURCHASE +29` (36 paid, 7 fee), summing to the 33 balance.
- **`admin-03-report-queue`** — reports across `PENDING` / `REVIEWED` / `DISMISSED`,
  including one with no reporter shown. That row is the platform's publish-time
  classifier (`reports.reporter_id IS NULL`, see `6-database-schema.md`), and it is in
  the seed specifically so the LEFT JOIN that path needs is visible in a figure.
