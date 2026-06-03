# 11 — Magazine Subscription & Credits Dashboard

**Route:** `/m/dashboard/subscription` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

Replaces the old "Wallet" concept — subscription management + credit balance + top-up.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Magazine Subscription & Credits dashboard, route "/m/dashboard/subscription".

Layout: top navigation bar, then a dashboard layout with a left sidebar and main content.
- Left sidebar (magazine dashboard nav): Marketplace, Library,
  Subscription & Credits (active, violet highlight), Notifications, Settings.
- Main area:
  - Page header: "Subscription & Credits".

  SECTION 1 — Subscription status card (full width):
  - A card with a violet left accent bar.
  - Plan name: "Magazine Pro" with an emerald "Active" badge.
  - Stats row: "Renewed: May 1, 2026 · Expires: Jun 1, 2026 · Next renewal in 28 days".
  - Two buttons: "Renew early" (outline) and "Cancel subscription" (ghost, muted, destructive
    red on hover). A small note: "Access continues until end of billing cycle."

  SECTION 2 — Credit balance card:
  - Large number prominently displayed: "342 credits" with a small "/ 500 monthly" indicator.
  - A progress bar showing credits used vs remaining (violet fill on slate track).
  - Below: "Monthly allowance: 500 credits · Resets on Jun 1, 2026".
  - A violet "Top up credits" button that opens a modal (show the modal as a second state):
    Modal: "Add credits" heading, amount selector (100, 250, 500, custom), price shown,
    "Confirm top-up" violet button, "Cancel" ghost button.
    Note in modal: "Top-up credits don't expire and carry over between billing cycles."

  SECTION 3 — Recent transactions table:
  - Columns: Date, Type, Article, Credits, Balance after.
  - Example rows:
    - "May 28 · Preview unlock · 'The Future of AI Writing' · −12 · 342"
    - "May 25 · Full purchase · 'Remote Work in 2026' · −108 · 354"
    - "May 20 · Preview unlock · 'Design Systems at Scale' · −15 · 462"
    - "May 1 · Monthly credit grant · — · +500 · 477"
    - "Apr 28 · Credit top-up · — · +250 · −23 → 227"
  - Type column uses color-coded badges: green for grants/top-ups, red for debits.
  - Pagination for older transactions.

Mobile (375px): sidebar collapses into bottom tab bar. Cards stack vertically full-width.
Transaction table becomes stacked cards with key info.
```
