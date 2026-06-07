# 15 — Magazine Profile (Public)

**Route:** `/m/[slug]` · **Role:** Any reader · **Stitch mode:** Standard

The public-facing magazine profile — shows the magazine's identity, curated articles, and subscription info. Visible to anyone; articles behind the subscription gate show a lock.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Public Magazine Profile page, route "/m/[slug]".

Layout: top navigation bar, then full-width content on #F8FAFC canvas.

MAGAZINE HERO (below navbar):
  Full-width white card, 1px Slate-200 bottom border, padding 32px vertical.
  Centered layout (max-width 960px, auto margins).

  Top row: magazine logo (64px square, rounded-xl, 1px Slate-200 border, placeholder
  with first letter in Violet-600 on Violet-50 bg) + text block beside it.
    Magazine name: "The Atlantic Review" (text-2xl font-semibold Slate-900).
    Tagline: "Long-form journalism for the digital age. Curating the finest voices in
    technology, culture, and design." (text-base Slate-600).
    Category badges: "Technology" "Culture" "Design" (Slate-100 bg, Slate-600 text,
    text-xs, rounded-full).

  Stats row (16px below, horizontal, 32px spacing):
    "142 articles" (Geist Mono font-semibold Slate-900 + label Slate-500).
    "23 writers" (same style).
    "Since Jan 2025" (same style).

  Action row (16px below stats):
    IF NOT SUBSCRIBED: "Subscribe to access" primary button (Violet-600, Phosphor
    CrownSimple icon). Below: "From 500 credits/month" (text-xs Slate-400 Geist Mono).
    IF SUBSCRIBED: Emerald-50 pill: Phosphor CheckCircle + "Subscribed" (Emerald-700).
    + "Visit library" secondary button (Slate-200 border).

CONTENT TABS (24px below hero):
  Full-width tab bar (max-width 960px centered):
    "Published articles" (active — Violet-600 text, 2px bottom border).
    "About" (Slate-500).
    "Writers" (Slate-500).
  1px Slate-200 full-width border below.

PUBLISHED ARTICLES TAB (active, 24px below tabs):
  Grid (max-width 960px centered): 2-column CSS Grid, 20px gap.

  Each card: white, 1px Slate-200 border, rounded-xl, overflow hidden.
    Thumbnail: full-width, 160px height, Slate-200 bg placeholder.
    Content padding 16px:
      Writer: small avatar (24px) + "Luca Hernandez" (text-sm Slate-600).
      Title: "Beyond LLMs: The Future of Cognitive Computing" (text-base font-medium
      Slate-900, 2 lines max).
      Meta: "Oct 10 · 14 min read" (text-xs Slate-400 Geist Mono).
      Bottom row: Phosphor Heart 89 (text-xs Slate-400) + placement badge.

    IF SUBSCRIBED: badge "PURCHASED" (Emerald-50 bg, Emerald-700) or "AVAILABLE"
    (Violet-100 bg, Violet-700).
    IF NOT SUBSCRIBED: subtle Phosphor Lock overlay on thumbnail corner (Slate-500, 20px).

  Show 6 article cards. "Load more" ghost button centered below.

WRITERS TAB (describe alternate):
  Grid (max-width 960px): 3-column grid of writer cards.
  Each card: white, rounded-xl, 1px Slate-200 border, padding 20px, centered content.
    Avatar (56px), name (text-sm font-medium Slate-900), role/bio snippet (text-xs
    Slate-500, 1 line), "12 articles" (text-xs Slate-400 Geist Mono).
    "View profile" link (text-xs Violet-600).

ABOUT TAB (describe alternate):
  Centered column (max-width 720px), padding 24px.
  Long description text (text-base Slate-700).
  "Subscription plans" section: single card showing the plan details — name, monthly
  credits, price. "Subscribe" button.

Mobile (375px): magazine hero stacks vertically (logo above text). Article grid becomes
single column. Writer grid becomes 2-column. Stats wrap. Subscribe button full-width.
```
