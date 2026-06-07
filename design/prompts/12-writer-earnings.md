# 12 — Writer Earnings Dashboard [GENERATED]

**Route:** `/dashboard/earnings` · **Role:** Writer · **Stitch mode:** Standard

Writer's marketplace earnings — preview payouts, purchase payouts, eligibility progress.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Writer Earnings dashboard, route "/dashboard/earnings".

Layout: top navigation bar, then dashboard layout with sidebar + main on #F8FAFC canvas.

LEFT SIDEBAR (240px, writer dashboard nav):
  My Articles, Analytics, Earnings (active — Violet-50 bg, Violet-700 text),
  Notifications, Settings. Phosphor icons.

MAIN AREA:

  PAGE HEADER: "Earnings" (text-2xl font-semibold Slate-900).

  ELIGIBILITY BANNER (20px below header, conditional):
    IF NOT ELIGIBLE: white card, 1px Violet-200 border, rounded-xl, padding 20px.
      Left: Phosphor Storefront icon (Violet-500, 24px).
      Center:
        "Unlock the marketplace" (text-base font-medium Slate-900).
        Two side-by-side progress indicators (same style as analytics dashboard):
          "Unique readers: 3,247 / 5,000" — progress bar 64.9% (Violet-600 on Slate-100).
          "Reactions: 783 / 1,000" — progress bar 78.3%.
        Numbers in Geist Mono tabular-nums.
        "Reach both thresholds to list articles on the marketplace and publish premium
        content." (text-xs Slate-400).
    
    IF ELIGIBLE: small inline badge:
      Emerald-50 pill: Phosphor CheckCircle (Emerald-600) + "Marketplace eligible since
      Mar 15, 2026" (text-sm Emerald-700 Geist Mono).
      Below: "You can list articles on the marketplace and publish premium content."
      (text-xs Slate-400).

  KPI ROW (24px below banner, 4 cards):
    Same card style as analytics (white, 1px Slate-200 border, rounded-xl, padding 20px).
    
    Total Earnings: "2,453 credits" (text-2xl Geist Mono Slate-900) + Phosphor TrendUp
    Emerald-500 + "+18.7%" (text-xs Emerald-600).
    Preview Payouts: "382 credits" (with lighter Violet-400 sparkline).
    Purchase Payouts: "2,071 credits" (with solid Violet-500 sparkline).
    Earnings Balance: "1,204 credits" (available to withdraw — this is the key number,
    give it a subtle Violet-50 background tint to distinguish it).

  EARNINGS CHART (24px below KPI):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Earnings over time" heading (text-base font-medium Slate-900).
    Legend top-right: two items — "Purchase payouts" (Violet-500 line swatch) +
    "Preview payouts" (Violet-300 dashed line swatch). Text-xs Slate-500.
    
    Line chart: two series overlaid.
      Purchase payouts: solid Violet-500 line, 2px.
      Preview payouts: dashed Violet-300 line, 1.5px.
    X-axis: weeks over last 3 months (Geist Mono text-xs Slate-400).
    Y-axis: credit amounts (Geist Mono text-xs Slate-400).
    Subtle Slate-100 horizontal gridlines only.

  TOP-EARNING ARTICLES TABLE (24px below chart):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Top-earning articles" heading (text-base font-medium Slate-900).
    
    Table columns: Article (with small 40x28px thumbnail), Preview Revenue, Purchase Revenue,
    Total Revenue, Magazines (number of unique magazines that purchased).
    5 rows with realistic data, sorted by total descending. Numbers in Geist Mono.
    Totals row at bottom: bold, 1px Slate-200 top border.
    Row hover: Slate-50 fill.

  RECENT TRANSACTIONS (24px below table):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Recent transactions" heading (text-base font-medium Slate-900).
    
    Transaction list (not a full table — more compact):
      Each row: date (text-xs Slate-400 Geist Mono) + type badge + article title
      (text-sm Slate-700) + amount (text-sm Geist Mono) + magazine name (text-xs Slate-400).
      
      Type badges:
        Preview payout: Amber-50 bg, Amber-700 text, "Preview payout".
        Purchase payout: Emerald-50 bg, Emerald-700 text, "Purchase payout".
      
      Amounts always positive (Emerald-600 text): "+11 credits", "+97 credits".
      
      Show 4 transactions. "View all transactions" link (text-sm Violet-600).

  WITHDRAW CARD (24px below transactions):
    White card, 1px Slate-200 border, rounded-xl, padding 20px. Horizontal layout.
    Left: "Available balance" (text-sm Slate-500) + "1,204 credits" (text-xl font-semibold
    Slate-900 Geist Mono).
    Right: "Withdraw" primary button (Violet-600, text-sm).
    Below button: "(Simulated payout in MVP)" (text-xs Slate-400).

Mobile (375px): sidebar collapses to bottom tab bar. KPI cards 2x2 grid. Chart and table
stack full-width. Transaction list becomes compact cards. Withdraw card full-width,
button stacks below balance.
```
