# 01 — Home Feed

**Route:** `/` · **Role:** Reader / Writer (logged in) · **Stitch mode:** Standard

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Home Feed (logged-in reader/writer view), route "/".

Layout: top navigation bar, then a centered content column with a left/right rail on desktop.
- Left rail: a vertical nav with icons + labels — Home, Discover, Following, Your Library,
  and a "Tags" section listing popular tags as pills (Technology, Culture, Business,
  Science, Design, Politics).
- Center column (max ~720px): an infinite article feed.
  - At the very top: a horizontal row of tag filter chips (All, Technology, Culture, …),
    "All" selected in violet.
  - Each feed card shows: writer avatar + name + "· 5 min read" + relative date on one line;
    a bold article title (text-xl); a 2-line excerpt in muted slate; a thumbnail image on the
    right (16:9, rounded); and a bottom action row with like count (heart), comment count,
    repost icon, and a bookmark icon on the far right.
  - Show one card marked with a small violet "Premium" badge next to its title.
  - Vary the cards so it looks real (different titles, authors, thumbnails).
- Right rail: a "Suggested writers to follow" card (3 writers, each avatar + name + topic +
  small outline "Follow" button), and a "Trending tags" card.

Mobile (375px): single column, no side rails. Tag chips scroll horizontally under a sticky
top bar. Feed cards stack with the thumbnail on top, content below. Bottom tab bar with
Home / Search / Write / Notifications / Profile icons.
```
