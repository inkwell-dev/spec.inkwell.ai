# 08 — Marketplace Browse (Magazine View)

**Route:** `/marketplace` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

Dedicated discovery interface for subscribed magazines to find eligible writers.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Marketplace Browse for magazines, route "/marketplace".
Only accessible to magazines with an active subscription.

Layout: top navigation bar, then dashboard layout with sidebar + main on #F8FAFC canvas.

LEFT SIDEBAR (240px, magazine dashboard nav):
  Nav items with Phosphor icons: Marketplace (active — Violet-50 bg, Violet-700 text),
  Library, Subscription & Credits, Notifications, Settings.

MAIN AREA:

  PAGE HEADER:
    "Marketplace" (text-2xl font-semibold Slate-900) + "Discover writers and source content"
    (text-sm Slate-500, 4px below).
    Credit balance indicator in the header row, right-aligned: Phosphor Coins icon
    (Violet-500) + "342 credits" (text-sm font-medium Slate-700 Geist Mono). Small
    pill-shaped display, Slate-100 background, rounded-full. This gives the magazine
    constant awareness of their budget.

  SEARCH + FILTERS ROW (20px below header):
    Search input (flex-1): Phosphor MagnifyingGlass icon, "Search writers by name, topic,
    or keyword..." placeholder, Slate-200 border, rounded-lg.
    Sort dropdown (right, 160px): "Sort by: Engagement" (Slate-200 border, rounded-lg,
    text-sm, Phosphor SortAscending icon).

  TOPIC FILTER CHIPS (12px below search):
    Horizontal row: "All Topics" (selected — Violet-600 fill, white text), "Technology",
    "Culture", "Business", "Science", "Design", "Politics".
    Unselected: Slate-200 border, Slate-600 text, rounded-full, text-sm.

  WRITER GRID (24px below filters, 2-column grid on desktop, NOT 3-column):
    Each writer card: white fill, 1px Slate-200 border, rounded-xl, padding 20px.
    Hover: border Slate-300, shadow 0 2px 8px rgba(0,0,0,0.06).
    
    Card contents:
      Top: circular avatar (48px) + name (text-base font-semibold Slate-900) + small
      Emerald-50 "Eligible" badge (text-xs Emerald-700) on the same line.
      Bio: text-sm Slate-500, 1 line, truncated with ellipsis.
      Topic tags: 2-3 small pills (text-xs, Slate-100 background, Slate-600 text, rounded-full).
      12px gap.
      Stats row (Geist Mono, text-xs Slate-500, tabular-nums):
        "12.4K readers · 3.2K reactions · 47 articles"
      Marketplace line: "8 articles for sale" (text-xs Violet-600).
      16px gap.
      "View profile" button: outline, Slate-200 border, text-sm Slate-700, rounded-lg,
      full width. Hover: Slate-100 fill.

    Use 6 cards (3 rows of 2) with diverse, realistic writers:
      "Amira Okafor" — AI & Technology / "Luca Hernandez" — Narrative Journalism /
      "Priya Nair" — Digital Culture / "Tomoko Sato" — Science Communication /
      "Marcus Webb" — Business Strategy / "Elif Aydin" — Design & Craft.
    Different avatar placeholder colors. Different stat numbers (not round).

  PAGINATION (32px below grid):
    "1" (Violet-600 fill, white text, 32px square, rounded-lg), "2", "3", "..." , "Next"
    (Slate-600 text). Simple, understated.

Mobile (375px): sidebar collapses to bottom tab bar. Writer cards single column, full-width.
Search bar full-width under sticky top bar. Filter chips scroll horizontally. Credit
balance moves into the top bar next to the avatar.
```
