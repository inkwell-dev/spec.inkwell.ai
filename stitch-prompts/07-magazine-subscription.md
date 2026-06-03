# 07 — Magazine Subscription Wall

**Route:** `/m/subscribe` · **Role:** Magazine (no active subscription) · **Stitch mode:** Standard

This is the mandatory gate after magazine sign-up — no marketplace access until subscribed.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Magazine Subscription Wall, route "/m/subscribe".
This screen blocks all marketplace access until the magazine subscribes. It appears
immediately after magazine sign-up or when an unsubscribed magazine tries to access
any marketplace feature.

Layout: top navigation bar (minimal — only Inkwell wordmark + magazine avatar), then a
centered content area.

- A large heading: "Subscribe to access the marketplace".
- Subtext: "Browse writers, preview articles, and build your curated library."
- A single subscription plan card (MVP has one tier), prominently displayed:
  - Plan name (e.g., "Magazine Pro") with a violet accent bar on the left.
  - Price: "$XX/month" (large, bold).
  - Included benefits as a checklist with emerald check icons:
    - "500 credits/month to preview and purchase articles"
    - "Browse all marketplace-eligible writers"
    - "AI-powered Portfolio Insights on every writer"
    - "Writer evaluation dashboards (audience, content, quality)"
    - "Curated library with republish rights"
  - A violet "Subscribe now" button (full width of the card).
  - Small muted text: "Credits refresh monthly. Top up anytime if you need more."
- Below the card: a muted "How credits work" expandable section that explains:
  "Preview an article for 10% of its price to read the full content. Purchase for the
  remaining 90% to add it to your library with republish rights. Preview cost is always
  credited toward the full purchase."

Mobile (375px): same layout, card takes full width with comfortable padding.
```
