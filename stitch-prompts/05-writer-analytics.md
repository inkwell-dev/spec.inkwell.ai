# 05 — Writer Analytics Dashboard

**Route:** `/dashboard/analytics` · **Role:** Writer · **Stitch mode:** Standard

Self-improvement analytics about the writer's own published articles.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Writer Analytics dashboard, route "/dashboard/analytics".
Self-improvement analytics for a writer about their own published articles.

Layout: top navigation bar, then a dashboard with sidebar + main content on #F8FAFC canvas.

LEFT SIDEBAR (240px, as defined in design system):
  Nav items: My Articles, Analytics (active — Violet-50 background, Violet-700 text),
  Earnings, Notifications, Settings. Each with a Phosphor icon (regular, 18px).

MAIN AREA:

  ELIGIBILITY PROGRESS BANNER (shown only if writer is NOT yet marketplace-eligible):
    Full-width card, white fill, 1px Violet-200 border (not Slate — Violet to draw
    attention), rounded-xl, padding 20px.
    Left side: Phosphor Storefront icon (Violet-500, 24px) + "Unlock the marketplace"
    heading (text-base font-medium Slate-900).
    Right side: two inline progress indicators:
      "3,247 / 5,000 readers" — Slate-700 label, progress bar below (Violet-600 fill,
      Slate-100 track, rounded-full, 6px height). Percentage: 64.9%.
      "783 / 1,000 reactions" — same style. Percentage: 78.3%.
    Below: "Reach both thresholds to list on the marketplace and publish premium content."
    (text-xs Slate-400).
    Numbers in Geist Mono with tabular-nums for clean alignment.

    IF ELIGIBLE: replace the banner with a small inline badge row:
    Emerald-50 background pill: Phosphor CheckCircle (Emerald-600) + "Marketplace eligible
    since Mar 15, 2026" (text-sm Emerald-700 Geist Mono).

  PAGE HEADER (24px below banner):
    "Analytics" (text-2xl font-semibold Slate-900) on the left.
    Right: date-range dropdown ("Last 30 days", Slate-200 border, rounded-lg, text-sm,
    Phosphor CalendarBlank icon) + article selector dropdown ("All articles", same style).

  KPI ROW (24px below header, 4 cards in a row):
    Each card: white fill, 1px Slate-200 border, rounded-xl, padding 20px.
      Label: text-xs uppercase tracking-wide Slate-400 (e.g., "Total Views").
      Value: text-2xl font-semibold Slate-900 Geist Mono tabular-nums (e.g., "12,847").
      Trend: small inline indicator — Phosphor TrendUp (Emerald-500) + "+12.3%" (text-xs
      Emerald-600 Geist Mono) or TrendDown (Red-500) for negative.
      Mini sparkline: 80px wide, 24px tall, Violet-500 stroke, no fill, no axes.
    Cards: Total Views, Avg. Read Time ("4m 12s"), Engagement Rate ("63.2%"), Total Likes.

  VIEWS CHART (24px below KPI row):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Views over time" heading (text-base font-medium Slate-900).
    Line/area chart: Violet-500 line (2px), soft Violet-100 gradient fill below,
    x-axis dates (text-xs Slate-400 Geist Mono), y-axis values (text-xs Slate-400
    Geist Mono), subtle Slate-100 horizontal gridlines only. No vertical gridlines.
    Clean, modern, minimal — no 3D effects, no decorative elements.

  TWO-COLUMN ROW (24px below chart):
    LEFT CARD — "Scroll depth":
      White card, rounded-xl. Horizontal bar chart / funnel:
      Paragraph labels on left (text-xs Slate-500: "Intro", "Para 2", "Para 3"...),
      horizontal bars showing reader retention percentage (Violet-500 to Violet-300
      gradient as bars get shorter, showing drop-off). Values on right in Geist Mono.
    RIGHT CARD — "AI feedback":
      White card, rounded-xl. Phosphor Sparkle icon (Violet-500) + "Writing feedback"
      heading. Bullet list of AI-detected insights:
        Each bullet: small colored dot (Amber-400, Emerald-400, or Slate-300 for severity)
        + insight text (text-sm Slate-700).
        E.g.: "Your introduction could use a stronger hook — consider opening with a
        specific anecdote." / "Paragraph 4 exceeds 210 words — consider splitting." /
        "Adding a subheading before the third section would improve scannability."

  TOP ARTICLES TABLE (24px below two-column row):
    White card, rounded-xl.
    "Top articles" heading (text-base font-medium Slate-900).
    Table: no outer border. Header: text-xs uppercase Slate-400. Columns: Title (with
    small 40x28px thumbnail placeholder), Views, Avg Read Time, Engagement, Likes.
    5 rows with realistic titles about writing/publishing. Numbers in Geist Mono.
    Row hover: Slate-50 fill.

Mobile (375px): sidebar collapses into bottom tab bar. KPI cards become a 2x2 grid.
Charts stack vertically full-width. Top-articles table becomes stacked cards (title +
key metrics per card). Eligibility banner stacks progress bars vertically.
```
