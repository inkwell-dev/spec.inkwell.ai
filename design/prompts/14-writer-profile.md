# 14 — Writer Profile (Public)

**Route:** `/u/[username]` · **Role:** Any reader · **Stitch mode:** Standard

The public-facing writer profile — what readers see when they click a writer's name from an article or the feed. This is NOT the magazine evaluation view (prompt 09); this is the reader-friendly version.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Public Writer Profile page, route "/u/[username]".

Layout: top navigation bar (Inkwell wordmark + search + Write button + avatar),
then full-width content on #F8FAFC canvas.

HERO SECTION (below navbar):
  Full-width white card, 1px Slate-200 bottom border, padding 32px vertical.
  Centered layout (max-width 720px, auto margins):

  Top row: circular avatar (80px, 1px Slate-200 border) + text block beside it.
    Name: "Amira Okafor" (text-2xl font-semibold Slate-900).
    Bio: "Senior Editor at Meridian Digital. Exploring the intersection of generative
    linguistics and modern urbanism. Currently working on a book about digital semiotics."
    (text-base Slate-600, max 2 lines).
    Location + joined date row: Phosphor MapPin icon (Slate-400) + "Lagos, Nigeria"
    (text-sm Slate-500) · Phosphor CalendarBlank icon + "Joined Mar 2024" (text-sm Slate-500).

  Stats row (16px below bio, horizontal, spaced 32px apart):
    "247 articles" (text-sm, number in Geist Mono font-semibold Slate-900, label Slate-500).
    "3.2K followers" (same style).
    "18.4K lifetime readers" (same style).
    Numbers use Geist Mono tabular-nums.

  Action row (16px below stats):
    "Follow" primary button (Violet-600, text-sm, Phosphor UserPlus icon).
    Phosphor ShareNetwork icon button (ghost, Slate-400).

CONTENT TABS (24px below hero):
  Centered tab bar (max-width 720px):
    "Articles" (active — Violet-600 text, 2px Violet-600 bottom border).
    "About" (Slate-500, hover Slate-700).
  1px Slate-200 full-width bottom border under tabs.

ARTICLES TAB (active, 24px below tabs):
  Centered column (max-width 720px).

  Filter row: "All" pill (Violet-600 bg, white text), "Public" pill (Slate-200 border,
  Slate-600 text), "Premium" pill (Slate-200 border). Text-sm, rounded-full, padding 6px 16px.

  Article list (16px below filters, 16px gap between cards):
    Each card: white, 1px Slate-200 border, rounded-xl, padding 20px. Horizontal layout.
    Left (flex-1):
      Title: "The Quiet Art of Editing Your Own Voice" (text-lg font-medium Slate-900).
      Excerpt: first line (text-sm Slate-500, 2 lines max, truncated).
      Meta row: "May 28, 2026" (text-xs Slate-400 Geist Mono) · "7 min read"
      · badge — "PUBLIC" (Slate-100 bg, Slate-600 text) or "PREMIUM" (Violet-100 bg,
      Violet-700 text) or "MARKETPLACE" (Amber-50 bg, Amber-700 text).
      Stats: Phosphor Heart 142 · Phosphor ChatCircle 23 (text-xs Slate-400).
    Right: thumbnail (120x80px, rounded-lg, Slate-200 bg placeholder).

  Show 4 articles. "Load more" ghost button centered below (text-sm Slate-500).

ABOUT TAB (hidden, describe for alternate state):
  Centered column (max-width 720px), padding 24px.
  "About" heading (text-lg font-medium Slate-900).
  Long-form bio text (text-base Slate-700, line-height 1.7).
  "Topics" section: tag pills (Slate-100 bg, text-xs Slate-600) —
  "Digital Semiotics", "Generative Writing", "Content Architecture", "Editorial Design".
  "Links" section: Phosphor Globe + website link (Violet-600), Phosphor TwitterLogo + handle.

Mobile (375px): avatar 64px, stats wrap to 2x2 grid, article cards stack vertically
with thumbnail above text (full-width). Tabs full-width. Action buttons full-width.
```
