# 02 — Article Read View [GENERATED]

**Route:** `/articles/[slug]` · **Role:** Reader / Magazine · **Stitch mode:** Standard

Includes five variants: free article, premium-locked, and three marketplace states.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Article reading page, route "/articles/[slug]".

Layout: top navigation bar, then a centered single reading column (max 680px) optimized
for long-form reading on the #F8FAFC canvas.

VARIANT 1 — FREE ARTICLE (default, generate this one fully):

Header block:
  - Title: text-3xl (30px) font-bold Slate-900, letter-spacing -0.025em, tight line-height
    (1.15). Title should be compelling: "The Quiet Art of Editing Your Own Voice".
  - Byline row below title (16px gap): circular avatar (40px) + writer name (text-sm
    font-medium Violet-600, clickable) + "Follow" outline button (text-xs, Slate-200 border,
    rounded-lg, Slate-600 text) + "·" + "Published May 28, 2026" (text-sm Slate-400) +
    "·" + "7 min read" (text-sm Slate-400).
  - 24px gap below byline.

Hero image: full-width of the reading column, rounded-xl, 16:9 aspect ratio. Use a
  solid placeholder tint (#DBEAFE light blue) — not a broken Unsplash link.

Article body (24px below hero):
  Realistic long-form content. Comfortable reading typography: text-base (16px), Slate-700,
  line-height 1.75, max-width 65ch within the column.
  Include: 3-4 paragraphs, one H2 subheading (text-xl font-semibold Slate-900, 32px top
  margin), a pull quote (left 3px Violet-500 border, italic, text-lg Slate-600, 24px
  left padding), and one inline image (rounded-lg, max-width 100%, with a text-xs Slate-400
  caption below).

Floating action bar (sticky, left of column on desktop, 48px offset):
  Vertical layout: heart icon + "247" count below, comment icon + "18", repost icon,
  bookmark icon. Each icon: Phosphor regular, 22px, Slate-400 default. Hover: Slate-600.
  Liked state: heart filled Violet-600.

Below article (48px gap):
  Author card: white card, 1px Slate-200 border, rounded-xl. Avatar (48px) + name
  (text-lg font-medium) + bio (text-sm Slate-500, 2 lines) + "1.2K followers" (text-xs
  Slate-400 Geist Mono) + "Follow" outline button. Horizontal layout on desktop.

  Comments section (32px below author card):
  "Responses" heading (text-lg font-medium Slate-900) + count badge.
  Comment input: avatar (32px) + input field ("Share your thoughts..." placeholder).
  Threaded comments: each with avatar (28px), name (text-sm font-medium), timestamp
  (text-xs Slate-400 Geist Mono), comment text (text-sm Slate-700), "Reply" link (text-xs
  Violet-600), heart icon + count (text-xs Slate-400). One nested reply indented 32px
  under a parent with a thin Slate-100 left border.

VARIANT 2 — PREMIUM-LOCKED state:
  Same header + hero. Article body visible for 2 paragraphs then fades to blur
  (backdrop-blur, gradient from transparent to white).
  Overlaid centered card (white, rounded-xl, shadow, 320px max-width):
    Phosphor Lock icon (24px, Slate-400) centered.
    "This is a premium article" (text-lg font-medium Slate-900).
    "Upgrade your plan to read the full story." (text-sm Slate-500).
    Violet-600 "Upgrade to Premium" button (full width of card).
    "Maybe later" ghost link below (text-sm Slate-400).

VARIANT 3 — MARKETPLACE ARTICLE (magazine viewer, not yet previewed):
  Shows title, byline with writer stats, and the excerpt only. The article body is
  completely hidden (not blurred — not rendered at all). Below the excerpt:
  A prominent action card (white, 1px Violet-200 border, rounded-xl):
    Article price in Geist Mono: "120 credits" (text-2xl font-semibold Slate-900).
    Preview price: "Preview: 12 credits (10%)" (text-sm Slate-500 Geist Mono).
    Two buttons side by side:
      "Preview article — 12 credits" (Violet-600 fill, primary).
      "Purchase directly — 120 credits" (outline, Slate-200 border).
    Info line: "Preview lets you read the full article. Preview cost credits toward
    purchase." (text-xs Slate-400, Phosphor Info icon).

VARIANT 4 — MARKETPLACE ARTICLE (previewed, not purchased):
  Full article body visible. Sticky banner at top of article (below navbar):
    Amber-50 background, 1px Amber-200 border, rounded-lg, padding 12px.
    "You've previewed this article" (text-sm Amber-700) +
    "Purchase — 108 credits remaining" Violet-600 button (text-sm) +
    "(preview credits applied)" (text-xs Slate-400 Geist Mono).
  Small "Previewed" badge (Amber-50 background, Amber-700 text) next to the title.

VARIANT 5 — MARKETPLACE ARTICLE (fully purchased):
  Full article body visible. Clean reading experience, no purchase CTAs.
  Small "In Meridian Digital's library" badge (Emerald-50 bg, Emerald-700 text) next to
  the title. A subtle "View in Library" text link (text-xs Violet-600) in the byline area.

Mobile (375px): single column, title text-2xl, action bar becomes a sticky bottom row
above the mobile tab bar. Premium lock card is full-width with 16px padding.
Marketplace CTAs stack vertically on mobile.
```
