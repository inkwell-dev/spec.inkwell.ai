# 12 — Writer Earnings Dashboard

**Route:** `/dashboard/earnings` · **Role:** Writer · **Stitch mode:** Standard

Writer's marketplace earnings — preview payouts, purchase payouts, eligibility progress.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Writer Earnings dashboard, route "/dashboard/earnings".

Layout: top navigation bar, then a dashboard layout with a left sidebar and main content.
- Left sidebar (writer dashboard nav): My Articles, Analytics,
  Earnings (active, violet highlight), Notifications, Settings.
- Main area:
  - Page header: "Earnings".

  SECTION 1 — Eligibility status (conditional):
  IF NOT ELIGIBLE: a full-width banner card with a violet accent:
    - "Unlock the marketplace" heading.
    - Two side-by-side progress bars:
      - "Unique readers: 3,200 / 5,000" (64% filled, violet).
      - "Reactions: 780 / 1,000" (78% filled, violet).
    - Muted text: "Reach both thresholds to list articles on the marketplace and publish
      premium articles."
  IF ELIGIBLE: a small emerald badge row: "✓ Marketplace eligible since Mar 15, 2026"
    with a muted "You can list articles on the marketplace and publish premium content."

  SECTION 2 — Earnings overview (4 KPI cards in a row):
  - Total Earnings (lifetime): "2,450 credits" with a small up-trend arrow.
  - Preview Payouts: "380 credits" (from article previews).
  - Purchase Payouts: "2,070 credits" (from full purchases).
  - Earnings Balance: "1,200 credits" (available to withdraw).

  SECTION 3 — Earnings over time chart:
  - A line/area chart (violet) showing earnings per week over the last 3 months.
  - Two overlaid series: "Preview payouts" (lighter violet, dashed) and "Purchase payouts"
    (solid violet). Legend at top right.

  SECTION 4 — Top-earning articles table:
  - Columns: Article Title, Preview Revenue, Purchase Revenue, Total Revenue, Magazines.
  - 5 rows with realistic data, sorted by total revenue descending.
  - Each row shows a small thumbnail next to the title.

  SECTION 5 — Recent transactions:
  - A list of recent earnings transactions:
    - "May 28 · Preview payout · 'The Future of AI Writing' · +11 credits · from TechMag"
    - "May 25 · Purchase payout · 'Remote Work in 2026' · +97 credits · from DesignWeekly"
    - Color-coded: amber for preview payouts, emerald for purchase payouts.
  - "View all transactions" link at the bottom.

  SECTION 6 — Withdraw button:
  - A card at the bottom: "Available balance: 1,200 credits" with a violet
    "Withdraw" button. Small note: "(Simulated payout in MVP)".

Mobile (375px): sidebar collapses into bottom tab bar. KPI cards become a 2×2 grid.
Chart and table stack vertically full-width. Transaction list becomes stacked cards.
```
