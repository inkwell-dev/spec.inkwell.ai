# 11 — Magazine Subscription & Credits Dashboard [GENERATED]

**Route:** `/m/dashboard/subscription` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

Subscription management + credit balance + top-up + transaction history.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Magazine Subscription & Credits dashboard, route "/m/dashboard/subscription".

Layout: top navigation bar, then dashboard layout with sidebar + main on #F8FAFC canvas.

LEFT SIDEBAR (240px, magazine dashboard nav):
  Marketplace, Library, Subscription & Credits (active — Violet-50 bg, Violet-700 text),
  Notifications, Settings. Phosphor icons.

MAIN AREA:

  PAGE HEADER: "Subscription & Credits" (text-2xl font-semibold Slate-900).

  SECTION 1 — Subscription status (20px below header):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    3px Violet-600 left accent border.
    
    Top row: "Magazine Pro" (text-lg font-semibold Slate-900) + Emerald-50 badge
    "Active" (text-xs Emerald-700 Geist Mono).
    
    Info row (12px below, text-sm Slate-500 Geist Mono):
      "Renewed: May 1, 2026 · Expires: Jun 1, 2026 · Next renewal in 28 days"
    
    Button row (16px below):
      "Renew early" outline button (Slate-200 border, text-sm Slate-700).
      "Cancel subscription" ghost button (text-sm Slate-400, hover Red-500 text).
    Note below buttons: "Access continues until end of billing cycle." (text-xs Slate-400).

  SECTION 2 — Credit balance (20px below):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    
    Left side:
      "Credit Balance" label (text-xs uppercase tracking-wide Slate-400).
      Large number: "342" (text-4xl font-bold Slate-900 Geist Mono tabular-nums) +
      "/ 500 monthly" (text-base Slate-400 Geist Mono, baseline-aligned).
    
    Progress bar below number (12px gap):
      Full-width, 8px height, rounded-full.
      Track: Slate-100. Fill: Violet-600 at 68.4% width.
    
    Info line (8px below bar):
      "Monthly allowance: 500 credits · Resets on Jun 1, 2026" (text-xs Slate-400 Geist Mono).
    
    Right side (right-aligned):
      "Top up credits" primary button (Violet-600, text-sm, Phosphor Plus icon).

    TOP-UP MODAL (show as a second state overlaid on the page):
      Centered modal, max-width 400px, white fill, rounded-xl, shadow (0 8px 32px
      rgba(0,0,0,0.12)), 1px Slate-200 border.
      Subtle backdrop (rgba(0,0,0,0.3)).
      
      "Add credits" heading (text-lg font-medium Slate-900).
      Amount selector: 4 option cards in a 2x2 grid (each white, 1px Slate-200 border,
      rounded-lg, padding 12px, text-center):
        "100 credits" / "250 credits" / "500 credits" / "Custom".
        Selected: Violet-600 border, Violet-50 bg. Unselected: Slate-200 border.
        Each shows the credit amount in Geist Mono font-semibold.
      
      Price shown below grid: "Total: $25.00" (text-sm Slate-700 Geist Mono).
      "Confirm top-up" primary button (Violet-600, full width).
      "Cancel" ghost button below (text-sm Slate-400).
      Note: "Top-up credits don't expire and carry over." (text-xs Slate-400).

  SECTION 3 — Recent transactions (20px below):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Recent transactions" heading (text-base font-medium Slate-900).
    
    Table (no outer border, clean):
      Header: text-xs uppercase tracking-wide Slate-400.
      Columns: Date, Type, Article, Credits, Balance.
      
      Rows (text-sm, Geist Mono for numbers):
        May 28 | Preview unlock (Amber-50 badge) | "The Future of AI Writing" | -12 | 342
        May 25 | Full purchase (Violet-100 badge) | "Remote Work in 2026" | -108 | 354
        May 20 | Preview unlock (Amber-50 badge) | "Design Systems at Scale" | -15 | 462
        May 1  | Monthly grant (Emerald-50 badge) | — | +500 | 477
        Apr 28 | Credit top-up (Slate-100 badge) | — | +250 | 227
      
      Credit column: green text (Emerald-600) for positive, default Slate-700 for negative.
      Row hover: Slate-50 fill. Rows separated by 1px Slate-100 borders.
    
    "View all transactions" link at bottom (text-sm Violet-600).

Mobile (375px): sidebar collapses to bottom tab bar. Cards stack full-width.
Transaction table becomes stacked cards with key info (type + article + credits).
Top-up modal becomes a bottom sheet.
```
