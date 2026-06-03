# 10 — Magazine Library

**Route:** `/m/dashboard/library` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

The magazine's curated collection of fully purchased articles with republish rights.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Magazine Library, route "/m/dashboard/library".
Shows all articles the magazine has fully purchased (not previewed-only).

Layout: top navigation bar, then a dashboard layout with a left sidebar and main content.
- Left sidebar (magazine dashboard nav): Marketplace, Library (active, violet highlight),
  Subscription & Credits, Notifications, Settings.
- Main area:
  - Page header: "Your Library" title with a subtitle "Articles you've purchased with
    republish rights" and an article count badge ("14 articles").
  - A search bar: "Search your library…" with a filter dropdown (By writer, By topic, By date).
  - Sort dropdown: "Sort by: Recently purchased" with options: Recently purchased, Writer name,
    Price paid, Topic.
  - A list of purchased articles, each as a card:
    - Left: small article thumbnail (rounded, 16:9).
    - Center: article title (bold, clickable), writer avatar + name + violet link to writer
      profile, 2-line excerpt in muted text, topic tags as small pills.
    - Right: "120 credits" (price paid, muted), purchase date ("Purchased May 20, 2026"),
      an emerald "Republish rights" badge.
    - A small "Read article" outline button.
  - A "Previewed articles" section below (collapsed by default, expandable):
    - Header: "Previewed but not purchased (3)" with an expand chevron.
    - When expanded: same card layout but with an amber "Previewed" badge instead of emerald,
      and a violet "Purchase — X credits remaining" button on each card.
  - Pagination at the bottom.

Mobile (375px): sidebar collapses into bottom tab bar. Article cards stack vertically
with thumbnail on top. Previewed section is a separate expandable accordion.
```
