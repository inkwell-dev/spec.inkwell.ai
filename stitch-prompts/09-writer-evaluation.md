# 09 — Writer Profile: Evaluation Mode (Magazine View)

**Route:** `/u/[username]?as=magazine` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

The magazine's decision-support view of a writer — analytics + Portfolio Insights + marketplace articles.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Writer Profile in evaluation mode, seen by a subscribed magazine,
route "/u/[username]?as=magazine".

Layout: top navigation bar, then a full-width profile header + tabbed content below.

Profile header:
- Large writer avatar on the left, name (bold, text-3xl), bio (2 lines), topic tags as pills.
- Stats row: "12,400 unique readers · 3,200 reactions · 47 published articles · Joined Jan 2025".
- An emerald "Marketplace eligible" badge.
- No follow button (magazines don't follow writers — they purchase content).

Below the header, a horizontal tab bar with four tabs:
  "Audience" (active) · "Content" · "Quality" · "Portfolio Insights" · "Marketplace Articles"

TAB 1 — AUDIENCE (shown as active):
- 4 KPI cards in a row: Total Readers, Avg. Views/Article, Follower Count, Reader Retention Rate.
- A "Reader growth" line chart (violet, 30 days).
- A "Geographic distribution" horizontal bar chart (top 5 countries).
- A "Reader engagement by article" table: Title, Views, Avg Read Time, Scroll Depth — 5 rows.

TAB 2 — CONTENT (describe layout but don't render fully):
- Posting frequency chart, avg word count, topic distribution pie chart, content consistency score.

TAB 3 — QUALITY (describe layout but don't render fully):
- Avg engagement rate, comment-to-view ratio, repost rate, readability score.

TAB 4 — PORTFOLIO INSIGHTS (AI-generated):
- A card with a sparkle icon header: "AI Portfolio Insights".
- A loading state hint: "Generating insights…" with a spinner (these load async).
- When loaded: structured sections — "Voice & Tone" (short paragraph), "Expertise Areas"
  (tag pills), "Consistency" (score + explanation), "Fit Assessment" (paragraph about
  how this writer's style matches magazine content needs), "Strengths" (bullet list),
  "Gaps" (bullet list).
- A muted note: "Generated from the writer's full published corpus. Cached for 24 hours."

TAB 5 — MARKETPLACE ARTICLES:
- A list of the writer's marketplace-listed articles, each showing:
  - Title (bold), excerpt (2 lines, muted), price in credits (e.g., "120 credits"),
    preview price (e.g., "Preview: 12 credits").
  - Status badge per article for this magazine: "Not previewed" (gray), or
    "Previewed" (amber), or "Purchased" (emerald + "In your library").
  - Two action buttons per article (contextual):
    - Not previewed: "Preview — 12 credits" (violet) + "Purchase directly — 120 credits" (outline)
    - Previewed: "Purchase — 108 credits remaining" (violet)
    - Purchased: "Read in library" (outline link)

Mobile (375px): profile header stacks vertically, tabs become a horizontal scrollable row,
KPI cards become a 2×2 grid, charts stack full-width, article list becomes stacked cards.
```
