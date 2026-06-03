# 02 — Article Read View

**Route:** `/articles/[slug]` · **Role:** Reader · **Stitch mode:** Standard

Includes a second **premium-locked** variant in the same prompt.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Article reading page, route "/articles/[slug]".

Layout: top navigation bar, then a centered single reading column (max ~680px) optimized
for long-form reading.
- Header block: article title (large, bold, text-4xl); below it a byline row — writer avatar,
  writer name (violet, clickable), "Follow" outline button, "· Published May 28 · 7 min read".
- Full-bleed hero thumbnail image (rounded) under the header.
- Article body: realistic long-form content — several paragraphs, one H2 subheading, a pull
  quote (left violet border, italic), and an inline image with a small caption. Comfortable
  line height, ~18px body text.
- A floating action bar that sticks to the left of the column on desktop (vertical) and to the
  bottom on mobile: Like (heart + count), Comment (count), Repost, Bookmark, Share.
- After the article: an author card (avatar, name, bio, follower count, Follow button), then a
  "Responses" / comments section showing threaded comments — each with avatar, name,
  timestamp, comment text, a Reply link, and like count; show one nested reply indented under
  a parent. A comment input box with the current user's avatar sits at the top of the section.

Also generate these additional variants of this screen:

VARIANT 2 — PREMIUM-LOCKED state: the article body is visible for the first 2 paragraphs
then fades to a blur, overlaid with a centered card: a small lock icon, "This is a premium
article", a line of subtext, and a violet "Upgrade to Premium" button plus a muted
"Maybe later" link.

VARIANT 3 — MARKETPLACE ARTICLE (magazine viewer, not yet previewed): the article shows
title, excerpt, writer name + stats, and the marketplace price prominently. The body is
completely hidden (not blurred — not visible at all). Two CTAs at the bottom of the header:
a violet "Preview article — 12 credits" button (10% of price) and a muted outline
"Purchase directly — 120 credits" button (full price). A small info line explains:
"Preview lets you read the full article. Preview cost is credited toward full purchase."

VARIANT 4 — MARKETPLACE ARTICLE (magazine viewer, previewed but not purchased): full article
body is visible (magazine has paid the preview fee). A sticky banner at the top:
"You've previewed this article" with a violet "Purchase — 108 credits remaining" button
and a note "(preview credits applied)". The article has a small "Previewed" badge next to
the title instead of "Premium".

VARIANT 5 — MARKETPLACE ARTICLE (magazine viewer, fully purchased): full article body
visible. A small "In [Magazine Name]'s library" attribution badge next to the title.
No purchase CTAs — just a clean reading experience with a "View in Library" link.

Mobile (375px): single column, title scales down, action bar becomes a sticky bottom row.
Marketplace CTAs stack vertically on mobile.
```
