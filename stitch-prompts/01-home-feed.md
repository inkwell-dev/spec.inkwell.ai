# 01 — Home Feed

**Route:** `/` · **Role:** Reader / Writer (logged in) · **Stitch mode:** Standard

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Home Feed (logged-in reader/writer view), route "/".

Layout: top navigation bar (as defined in design system), then a three-rail desktop layout.

LEFT RAIL (200px, sticky):
  Vertical nav with Phosphor icons (regular weight) + labels — Home (active, Violet-700
  text on Violet-50 background), Discover, Following, Your Library.
  Below a "Topics" section label (text-xs uppercase Slate-400), then a vertical list of
  topic tags as small ghost pills: Technology, Culture, Business, Science, Design, Politics.
  Each pill: text-sm, Slate-600, rounded-lg, hover Slate-100 fill. No colored backgrounds
  on topic pills.

CENTER COLUMN (max 680px, centered):
  At the top: a horizontal row of filter chips — "All" (selected: Violet-600 fill, white
  text), "Technology", "Culture", "Business"... Each unselected chip: Slate-200 border,
  Slate-600 text, rounded-full, text-sm. Chips scroll horizontally if they overflow.
  
  Below: an infinite article feed. Each feed card is a white card on the #F8FAFC canvas:
    - Top line: circular avatar (28px) + writer name (text-sm font-medium Slate-900,
      clickable) + "·" separator + "5 min read" (text-sm Slate-500) + relative date
      (text-sm Slate-400, e.g. "2d ago").
    - Title: text-lg font-semibold Slate-900, max 2 lines, letter-spacing -0.01em.
    - Excerpt: text-sm Slate-500, 2 lines max, line-clamp.
    - Thumbnail: right-aligned, 120x80px rounded-lg, 16:9 aspect ratio. Use solid
      placeholder colors (#E2E8F0, #DBEAFE, #F3E8FF) — no broken image links.
    - Bottom action row: heart icon + "142" (Slate-500), comment icon + "23", repost icon,
      bookmark icon far right. All icons Phosphor regular, 18px, Slate-400. Hover: Slate-600.
    - Cards separated by 1px Slate-100 divider, not stacked with gaps.
  
  One card has a small "Premium" badge (Violet-100 background, Violet-700 text, text-xs
  uppercase, rounded-full) next to its title.
  
  Vary the content: use realistic article titles about writing craft, journalism, content
  strategy, publishing. Use diverse writer names (e.g., "Amira Okafor", "Luca Hernandez",
  "Priya Nair"). Use different placeholder thumbnail tints. Make it feel like a real feed.

  Note: marketplace articles (placement = "marketplace") are NEVER shown in this feed.
  Only public articles (free or premium) appear here.

RIGHT RAIL (260px, sticky):
  "Writers to follow" card: white card, 1px Slate-200 border. 3 writers, each row:
  avatar (36px) + name (text-sm font-medium) + topic (text-xs Slate-500) + small outline
  "Follow" button (text-xs, Slate-200 border, rounded-lg). Rows separated by Slate-100
  divider.
  Below: "Trending topics" card: same card style, topics as small pills with subtle
  Slate-100 background.

Mobile (375px): single column, no side rails. Tag chips scroll horizontally under a sticky
top bar. Feed cards stack full-width with thumbnail spanning full width above the content.
Bottom tab bar: Home / Search / Write / Notifications / Profile — Phosphor icons, 24px,
Slate-400, active icon Violet-600. No labels on mobile tab bar.
```
