# 08 — Marketplace Browse (Magazine View)

**Route:** `/marketplace` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

The dedicated discovery interface for subscribed magazines to find eligible writers.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Marketplace Browse for magazines, route "/marketplace".
Only accessible to magazines with an active subscription.

Layout: top navigation bar, then a dashboard layout with a left sidebar and main content.
- Left sidebar (magazine dashboard nav): Marketplace (active, violet highlight), Library,
  Subscription & Credits, Notifications, Settings.
- Main area:
  - Page header: "Marketplace" title with a subtitle "Discover writers and source content".
  - A search bar: "Search writers by name, topic, or keyword…" with a magnifying-glass icon.
  - A horizontal row of filter chips: All Topics, Technology, Culture, Business, Science,
    Design, Politics — "All Topics" selected in violet.
  - Sort dropdown on the right: "Sort by: Engagement" with options: Engagement, Posting
    frequency, Topic relevance, Newest.
  - A grid of writer cards (3 columns on desktop):
    Each writer card shows:
    - Writer avatar (circular, medium) + name (bold) + a violet "View profile" link.
    - A short bio line (1 line, truncated).
    - Topic tags as small pills (e.g., "Technology", "AI", "Culture").
    - Stats row: "12.4K readers · 3.2K reactions · 47 articles".
    - Number of marketplace-listed articles: "8 articles for sale" in muted text.
    - A small emerald "Eligible" badge (all writers here are eligible by definition).
  - Vary the cards with different writers, topics, stats to look realistic.
  - Pagination at the bottom (1, 2, 3, … Next).

Mobile (375px): sidebar collapses into bottom tab bar. Writer cards become a single-column
list. Filter chips scroll horizontally. Search bar is full-width under a sticky top bar.
```
