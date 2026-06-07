# 10 — Magazine Library [GENERATED]

**Route:** `/m/dashboard/library` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

The magazine's curated collection of fully purchased articles with republish rights.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Magazine Library, route "/m/dashboard/library".
Shows all articles the magazine has fully purchased (not previewed-only).

Layout: top navigation bar, then dashboard layout with sidebar + main on #F8FAFC canvas.

LEFT SIDEBAR (240px, magazine dashboard nav):
  Marketplace, Library (active — Violet-50 bg, Violet-700 text), Subscription & Credits,
  Notifications, Settings. Phosphor icons.

MAIN AREA:

  PAGE HEADER:
    "Your Library" (text-2xl font-semibold Slate-900) + small count badge next to it:
    "14 articles" (text-xs Slate-500 Geist Mono, Slate-100 bg, rounded-full, padding 4px 10px).
    Subtitle: "Articles you've purchased with republish rights." (text-sm Slate-500).
    Credit balance pill top-right (same as marketplace: "342 credits" Geist Mono).

  SEARCH + FILTER ROW (20px below):
    Search input: "Search your library..." with Phosphor MagnifyingGlass.
    Filter dropdown: "Filter by: All" (options: All, By writer, By topic).
    Sort dropdown: "Sort by: Recently purchased" (options: Recently purchased, Writer name,
    Price paid, Topic).

  ARTICLE LIST (24px below, NOT a grid — a list of horizontal cards):
    Each article card: white fill, 1px Slate-200 border, rounded-xl, padding 16px.
    Hover: border Slate-300, subtle shadow lift.
    
    Layout per card (horizontal, single row):
      LEFT: article thumbnail placeholder (80x56px, rounded-lg, solid color placeholder).
      CENTER (flex-1, 16px left margin):
        Title (text-base font-medium Slate-900, clickable) on first line.
        Writer: avatar (24px) + name (text-sm Violet-600) + "·" + topic tag pill
        (text-xs Slate-100 bg Slate-600 text).
        Excerpt: text-sm Slate-500, 1 line, truncated.
      RIGHT (text-right, min-width 160px):
        "120 credits" (text-sm Slate-700 Geist Mono) — price paid.
        "Purchased May 20, 2026" (text-xs Slate-400 Geist Mono).
        Emerald-50 badge: "Republish rights" (text-xs Emerald-700).
        "Read article" outline button (text-xs, Slate-200 border, rounded-lg, margin-top 8px).

    Show 5 articles with varied writers, topics, prices, dates. Use realistic titles:
      "The Quiet Art of Editing Your Own Voice" / "Remote Work Changed How We Write" /
      "Why Long-Form Journalism Still Matters in 2026" / "Design Systems for Content Teams" /
      "The Economics of Independent Publishing".

    Cards separated by 12px vertical gap (not dividers — use gap since these are cards).

  PREVIEWED SECTION (32px below purchased list):
    Collapsed by default. Header row:
      Phosphor CaretRight icon (rotates to CaretDown when expanded) + "Previewed but not
      purchased" (text-sm font-medium Slate-600) + count: "(3)" (text-sm Slate-400).
      1px Slate-200 top border above this section.

    When expanded: same card layout but with these differences:
      Badge: Amber-50 bg, "Previewed" (text-xs Amber-700) instead of Emerald.
      Instead of "Read article" button: "Purchase — 108 credits" small Violet-600 button.
      Cards have a very subtle Amber-50 left border (3px) to distinguish from purchased.

  PAGINATION (24px below):
    Simple: "1" (active), "2", "3", "Next". Same style as marketplace browse.

Mobile (375px): sidebar collapses to bottom tab bar. Article cards stack vertically —
thumbnail above content, right-column info below content. Previewed section is a
separate expandable accordion. Search bar full-width.
```
