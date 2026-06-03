# 05 — Writer Analytics Dashboard

**Route:** `/dashboard/analytics` · **Role:** Writer · **Stitch mode:** Standard

Self-improvement analytics about the writer's own published articles.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Writer Analytics dashboard, route "/dashboard/analytics".
Self-improvement analytics for a writer about their own published articles.

Layout: top navigation bar, then a dashboard with a LEFT sidebar and a main content area.
- Left sidebar (writer dashboard nav): My Articles, Analytics (active, violet highlight),
  Earnings, Notifications, Settings.
- Main area:
  - Page header: "Analytics" title + a date-range dropdown ("Last 30 days") and an article
    selector dropdown ("All articles").
  - A row of 4 KPI stat cards: Total Views (with a small up-trend % and sparkline),
    Avg. Read Time ("4m 12s"), Engagement Rate ("62%"), Total Likes. Each card: muted label,
    big number, small trend indicator.
  - A large "Views over time" line/area chart card (violet line, soft gradient fill, x-axis
    dates, subtle gridlines).
  - Two cards side by side:
    LEFT — "Scroll depth & drop-off": a horizontal bar / funnel showing reader retention by
    paragraph (100% → declining), so you can see where readers drop off.
    RIGHT — "AI feedback": a card with a sparkle icon listing AI-detected weak sections as
    bullet points with small severity dots — e.g. "Intro is weak — consider a stronger hook",
    "Paragraph 4 is too long (210 words)", "Add a subheading before section 3".
  - A "Top articles" table: columns Title, Views, Avg read time, Engagement, Likes — 5 rows
    with a small thumbnail next to each title.

Use realistic but clearly placeholder numbers. Charts should look clean and modern, violet
accent, not cluttered.

Mobile (375px): sidebar collapses into the bottom tab bar; KPI cards become a 2×2 grid;
charts stack vertically full-width; the top-articles table becomes stacked cards.
```
