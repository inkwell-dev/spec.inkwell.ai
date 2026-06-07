# 09 — Writer Profile: Evaluation Mode (Magazine View) [GENERATED]

**Route:** `/u/[username]?as=magazine` · **Role:** Magazine (active subscription) · **Stitch mode:** Standard

The magazine's decision-support view of a writer — analytics + Portfolio Insights + marketplace articles.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Writer Profile in evaluation mode, seen by a subscribed magazine,
route "/u/[username]?as=magazine".

Layout: top navigation bar, then full-width content on #F8FAFC canvas. No sidebar —
this is a profile page, not a dashboard.

PROFILE HEADER (white background, 1px Slate-200 bottom border, padding 32px):
  Asymmetric layout — NOT a centered bio card.
  Left: large avatar (72px, rounded-full) with a thin 2px Violet-200 ring.
  Right of avatar (16px gap):
    Name: "Amira Okafor" (text-2xl font-semibold Slate-900, letter-spacing -0.02em).
    Bio: "Senior technology journalist covering AI, automation, and the future of digital
    publishing." (text-sm Slate-500, max 2 lines).
    Topic tags: 3 small pills (Slate-100 bg, Slate-600 text, text-xs, rounded-full):
    "AI & Technology", "Publishing", "Automation".
    Stats row (Geist Mono, text-sm Slate-500, 8px above tags):
      "12,437 readers · 3,218 reactions · 47 articles · Joined Jan 2025"
    Emerald-50 badge: Phosphor CheckCircle (Emerald-600) + "Marketplace eligible"
    (text-xs Emerald-700).
  Far right: credit balance pill (same as marketplace browse — "342 credits" Geist Mono).

HORIZONTAL TAB BAR (below header, 1px Slate-200 bottom border):
  Tabs: "Audience" (active — Violet-600 text, 2px Violet-600 bottom border),
  "Content", "Quality", "Portfolio Insights", "Articles for Sale".
  Inactive tabs: Slate-500 text, hover Slate-700. Text-sm font-medium.

TAB 1 — AUDIENCE (render fully):
  Main content area, padding 24px.
  
  KPI row (4 cards, same style as writer analytics):
    Total Readers: "12,437" / Avg Views/Article: "264" / Followers: "891" /
    Reader Retention: "34.2%".
    Each in Geist Mono, with subtle sparkline + trend indicator.

  "Reader growth" chart (24px below):
    White card, rounded-xl. Line chart: Violet-500 line on clean axes.
    X-axis: last 30 days (Geist Mono text-xs Slate-400). Subtle Slate-100 gridlines.

  Two-column below chart:
    LEFT — "Geographic distribution": horizontal bar chart. Top 5 countries
    (United States, United Kingdom, India, Germany, Canada) with Violet bars of
    varying lengths. Country names text-sm Slate-700, percentages in Geist Mono.
    RIGHT — "Reader engagement by article": compact table. Title, Views, Avg Read Time,
    Scroll Depth. 5 rows. Numbers in Geist Mono.

TAB 2 — CONTENT (describe but don't fully render):
  Posting frequency bar chart (articles per month), avg word count stat,
  topic distribution (horizontal stacked bar — not a pie chart, pie charts look generic),
  content consistency score as a large number with context.

TAB 3 — QUALITY (describe but don't fully render):
  Avg engagement rate, comment-to-view ratio, repost rate, readability score.
  Each as a card with large Geist Mono number + context label + trend.

TAB 4 — PORTFOLIO INSIGHTS (AI-generated):
  White card, rounded-xl, padding 24px.
  Header: Phosphor Sparkle icon (Violet-500, 20px) + "AI Portfolio Insights"
  (text-lg font-medium Slate-900).
  
  Loading state: skeleton loaders matching the structured output format (4 skeleton
  blocks of varying height + shimmer animation). "Generating insights..." text
  (text-sm Slate-400) with a subtle pulse animation.
  
  Loaded state (show this): structured sections with 20px gaps:
    "Voice & Tone" — short paragraph (text-sm Slate-700).
    "Expertise Areas" — tag pills (Violet-100 bg, Violet-700 text, rounded-full, text-xs).
    "Consistency" — score "8.4 / 10" (text-xl Geist Mono Slate-900) + one-line explanation.
    "Fit Assessment" — paragraph about how this writer's style matches the magazine's needs.
    "Strengths" — bullet list (Phosphor CheckCircle Emerald-500 + text-sm Slate-700).
    "Gaps" — bullet list (Phosphor Warning Amber-500 + text-sm Slate-700).
  
  Footer: "Generated from 47 published articles. Cached — last updated 2h ago."
  (text-xs Slate-400 Geist Mono).

TAB 5 — ARTICLES FOR SALE:
  List of marketplace articles. Each as a horizontal card row:
    Left: title (text-base font-medium Slate-900) + excerpt (text-sm Slate-500, 1 line).
    Center: topic tag pill.
    Right: price "120 credits" (text-sm font-semibold Slate-900 Geist Mono) +
    preview price "Preview: 12 credits" (text-xs Slate-400 Geist Mono).
    
    Status badge per article (for this magazine):
      Not previewed: Slate-100 bg, "Not previewed" (Slate-500 text).
      Previewed: Amber-50 bg, "Previewed" (Amber-700 text).
      Purchased: Emerald-50 bg, "In your library" (Emerald-700 text).
    
    Action buttons (contextual, right-aligned):
      Not previewed: "Preview — 12 cr" (Violet-600 small button) + "Buy — 120 cr" (outline).
      Previewed: "Purchase — 108 cr" (Violet-600 small button).
      Purchased: "Read in library" (ghost link, Violet-600 text).
    
    Show 4 articles with mixed states. Cards separated by 1px Slate-100 dividers.

Mobile (375px): profile header stacks vertically (avatar above name/bio). Tabs scroll
horizontally. KPI cards 2x2 grid. Charts full-width stacked. Article list becomes cards.
```
