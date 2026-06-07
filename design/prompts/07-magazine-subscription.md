# 07 — Magazine Subscription Wall [GENERATED]

**Route:** `/m/subscribe` · **Role:** Magazine (no active subscription) · **Stitch mode:** Standard

Mandatory gate after magazine sign-up — no marketplace access until subscribed.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Magazine Subscription Wall, route "/m/subscribe".
This screen blocks all marketplace access until the magazine subscribes. It appears
immediately after magazine sign-up or when an unsubscribed magazine tries to access
any marketplace feature.

Layout: minimal top bar (Inkwell wordmark + magazine avatar only, no full nav — they
can't access anything yet), then centered content on #F8FAFC canvas.

Centered container, max-width 520px:

  Heading: "Subscribe to access the marketplace" (text-2xl font-semibold Slate-900,
  letter-spacing -0.02em, centered).
  Subtext: "Browse writers, preview articles, and build your curated library."
  (text-base Slate-500, centered, 8px below heading).

  32px gap.

  Subscription plan card (white fill, 1px Slate-200 border, rounded-xl, padding 28px):
    Left accent bar: 3px Violet-600 on the left edge of the card (like a pull-quote border).
    
    Plan name: "Magazine Pro" (text-lg font-semibold Slate-900).
    Price: "49 credits/month" (text-3xl font-bold Slate-900 Geist Mono) with "/month"
    in text-base font-normal Slate-400.
    
    16px gap.
    
    Benefits checklist (each item on its own line, 10px gap):
      Each: Phosphor CheckCircle icon (Emerald-500, 18px) + benefit text (text-sm Slate-700).
      - "500 credits/month to preview and purchase articles"
      - "Browse all marketplace-eligible writers"
      - "AI-powered Portfolio Insights on every writer"
      - "Writer evaluation dashboards (audience, content, quality)"
      - "Curated library with republish rights"
    
    24px gap.
    
    "Subscribe now" primary button (Violet-600, full width, rounded-lg, text-base font-medium).
    
    8px gap.
    
    "Credits refresh monthly. Top up anytime if you need more." (text-xs Slate-400, centered).

  24px gap below card.

  Expandable section: "How do credits work?" (text-sm Slate-500, Phosphor CaretDown icon,
  clickable). When expanded:
    Slate-50 background card, rounded-lg, padding 16px, 1px Slate-200 border.
    Three-step explanation:
      "1. Browse" — "See titles, excerpts, and writer stats for free." (text-sm Slate-600)
      "2. Preview" — "Pay 10% of the article price to read the full content."
      "3. Purchase" — "Pay the remaining 90% to add it to your library with republish rights.
      Preview cost is credited — you never pay more than the listed price."
    Steps separated by 12px gaps. Step numbers in Geist Mono Violet-600 font-semibold.

Mobile (375px): same layout, card takes full width with 16px padding. Plan card border
removed on mobile (seamless with canvas).
```
