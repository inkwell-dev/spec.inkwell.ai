# Desktop Refinement Prompts

Desktop (1440px) expansion prompts for screens that exist only as mobile in the Figma file, plus new screens (14–17) that need both mobile and desktop generation.

> For each prompt below: open a **new Stitch chat**, paste the **`00-design-system.md` preamble** first, then paste the prompt.

---

## A — Write Editor (Desktop)

Stitch generated a mobile-only "Write Editor" (basic editor without AI panel). This prompt creates the desktop version.

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: Basic article editor — no AI panel open, just the writing surface.
Route "/editor/[id]", writer is in drafting mode before opening the AI assistant.

Top bar (full-width, white, 1px Slate-200 bottom border):
  Left: back arrow (Phosphor CaretLeft, Slate-400) + "Draft" label (text-sm Slate-500)
  + "Saved just now" (text-xs Slate-400 Geist Mono).
  Right: "Preview" ghost button (text-sm Slate-500) + "Publish" primary button
  (Violet-600, text-sm).

Main area: centered writing column (max-width 680px, auto margins on #F8FAFC canvas).
  Token counter pill: "1,240 tokens left" (text-xs, Violet-100 bg, Violet-700 text,
  Geist Mono, centered above title).
  Title: "The Architecture of Focused Digital Interfaces" (text-3xl font-semibold
  Slate-900, editable).
  Cover image placeholder: dashed Slate-200 border, rounded-lg, 680x200px,
  Phosphor Image icon centered + "Add a cover image" (text-sm Slate-400).
  Body text: 4 paragraphs of realistic content about writing craft and digital
  editing (text-base Slate-700, line-height 1.8).

Floating toolbar (appears below content, centered):
  Pill-shaped bar (white, 1px Slate-200 border, rounded-full, shadow-sm, padding 8px 16px).
  Icons: Phosphor TextBolder, TextItalic, Link, Quotes, ListBullets, separated by
  1px Slate-200 vertical divider, then Phosphor DotsThree for more options.
  Far left: sparkle icon (Violet-600) — AI trigger button.

Left margin (fixed, 64px from left edge):
  Phosphor Microphone icon button (ghost, Slate-400) — voice input.

No sidebar. No AI panel. Clean, distraction-free writing surface.
```

---

## B — Writer Dashboard (Desktop)

Mobile-only general dashboard overview. This prompt creates the desktop version.

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: Writer Dashboard overview — the landing page after a writer logs in.
Route "/dashboard".

LEFT SIDEBAR (240px, white, 1px Slate-200 right border):
  Inkwell wordmark (Violet-600) at top.
  Nav items: Dashboard (active — Violet-50 bg, Violet-700 text, Phosphor House icon),
  My Articles (Phosphor Article), Analytics (Phosphor ChartLine), Earnings
  (Phosphor Wallet), Notifications (Phosphor Bell, small red dot), Settings
  (Phosphor Gear). Text-sm Slate-600.
  Bottom: user avatar (32px) + "Amira Okafor" + "Writer" (text-xs Slate-400).

MAIN AREA (padding 32px, #F8FAFC canvas):

  Welcome row: "Welcome back, Amira" (text-2xl font-semibold Slate-900).
  "Here's what's happening with your articles." (text-sm Slate-500).

  KPI ROW (24px below, 4 cards, equal width, 16px gap):
    Card style: white, 1px Slate-200 border, rounded-xl, padding 20px.
    "Total articles" — "24" (text-2xl Geist Mono Slate-900) + Phosphor Article (Slate-400).
    "Total readers" — "12,847" (Geist Mono) + trend "+12.3%" (Emerald-600, text-xs).
    "Total reactions" — "1,934" (Geist Mono).
    "Earnings" — "2,453 credits" (Geist Mono) + Phosphor TrendUp Emerald-500.

  TWO-COLUMN GRID (24px below, 60/40 split):

    LEFT COLUMN — "Recent articles" (text-lg font-medium Slate-900):
      White card, rounded-xl, 1px Slate-200 border, padding 24px.
      Table: Article title, Status (badge: "Published" Emerald-50, "Draft" Slate-100),
      Views (Geist Mono), Date (Geist Mono text-xs Slate-400).
      5 rows. "View all articles" link (text-sm Violet-600).

    RIGHT COLUMN — "Quick actions" + "Eligibility":
      Quick actions card (white, rounded-xl, padding 20px):
        "Write new article" primary button (Violet-600, full-width, Phosphor PencilSimple).
        "View analytics" secondary button (full-width).
        "Import article" ghost button (full-width).

      Eligibility card (20px below, white, rounded-xl, padding 20px):
        "Marketplace eligibility" (text-base font-medium Slate-900).
        Two progress bars:
          "Readers: 3,247 / 5,000" (Geist Mono text-xs) — bar 64.9%.
          "Reactions: 783 / 1,000" (Geist Mono text-xs) — bar 78.3%.
        "Keep publishing to unlock." (text-xs Slate-400).

  RECENT ACTIVITY (24px below, full-width):
    White card, rounded-xl, 1px Slate-200 border, padding 24px.
    "Recent activity" heading. Compact list: icon + text + timestamp.
    4 items: new comment, new follower, article reached 1K views, preview purchase.
```

---

## C — Marketplace Feed (Desktop)

Mobile-only marketplace feed screen. This prompt creates the desktop version.

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: Marketplace Feed — a curated feed of marketplace-only articles available
to subscribed magazines. Route "/marketplace/feed".

TOP NAVBAR: standard Inkwell navbar. "240 Credits" shown next to avatar (Geist Mono,
text-sm Slate-500).

LEFT SIDEBAR (240px, magazine dashboard nav):
  Marketplace (contains sub-items: Browse Writers, Feed (active — Violet-50 bg)),
  Library, Subscription & Credits, Notifications, Settings.

MAIN AREA (padding 32px):

  PAGE HEADER: "Marketplace Feed" (text-2xl font-semibold Slate-900).
  Subtitle: "Latest articles from marketplace writers." (text-sm Slate-500).

  FILTER BAR (16px below):
    Topic pills: "All" (Violet-600 bg, white text), "Technology", "Culture", "Design",
    "Business", "Science" (Slate-200 border, Slate-600 text). Rounded-full, text-sm.
    Right-aligned: sort dropdown — "Newest first" (Slate-200 border, text-sm).

  ARTICLE FEED (20px below, single centered column, max-width 720px):
    Each card: white, 1px Slate-200 border, rounded-xl, padding 20px. 16px gap between.

    Card layout (horizontal):
      Left (flex-1):
        Writer row: avatar (24px) + "Luca Hernandez" (text-sm Slate-600) + "in"
        + "AI & Machine Learning" (text-sm Violet-600).
        Title: "Beyond LLMs: The Future of Cognitive Computing in Enterprise"
        (text-lg font-medium Slate-900).
        Excerpt: 2 lines (text-sm Slate-500).
        Meta: "Oct 10 · 14 min read" (text-xs Slate-400 Geist Mono).
        Bottom: Phosphor Heart 89 · price badge: "120 credits" (Violet-100 bg,
        Violet-700 text, Geist Mono text-xs).
      Right: thumbnail (160x100px, rounded-lg).

    Show 5 articles. "Load more" centered below.

  RIGHT SIDEBAR (280px, optional on wide screens):
    "Trending in marketplace" card (white, rounded-xl, padding 20px):
      5 trending article titles (text-sm Slate-700) with rank numbers (Geist Mono
      Violet-600). "1." "2." etc.
    "Top writers" card (20px below):
      3 writer rows: avatar + name + article count (text-xs Slate-400 Geist Mono).
```

---

## D — Discovery & Search (Desktop)

Mobile-only search and discovery screen. This prompt creates the desktop version.

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: Discovery & Search page — where readers explore topics, discover writers,
and search across all content. Route "/discover".

TOP NAVBAR: standard Inkwell navbar. Search input in navbar is focused/active
(2px Violet-600 focus ring) with query text "content strategy" typed in.

MAIN AREA (no sidebar — full-width layout, max-width 1120px centered):

  SEARCH RESULTS HEADER (32px below navbar):
    "Results for "content strategy"" (text-xl font-medium Slate-900).
    "127 articles · 8 writers · 3 topics" (text-sm Slate-500 Geist Mono).

  TABS (16px below):
    "Articles" (active — Violet-600 text, 2px bottom border), "Writers" (Slate-500),
    "Topics" (Slate-500).
    1px Slate-200 bottom border.

  TWO-COLUMN LAYOUT (24px below tabs):

    LEFT COLUMN (flex-1, max-width 720px) — Search results:
      Article result cards (16px gap):
        Each: white, 1px Slate-200 border, rounded-xl, padding 20px. Horizontal.
        Left (flex-1):
          Writer: avatar (24px) + "Priya Nair" (text-sm Slate-600) · "in The Startup"
          (text-sm Slate-500).
          Title with highlighted match: "The Evolution of <mark>Content Strategy</mark>
          in the Age of AI" (text-lg font-medium Slate-900, matched words get
          Violet-100 bg highlight).
          Excerpt: 2 lines (text-sm Slate-500).
          Meta: "May 15 · 9 min read" (text-xs Slate-400 Geist Mono) + placement badge.
        Right: thumbnail (140x90px, rounded-lg).

      Show 5 results. Pagination: "1 2 3 ... 13" (text-sm, active page: Violet-600 bg
      white text circle, others Slate-500).

    RIGHT COLUMN (280px) — Discovery sidebar:
      "Related topics" card (white, rounded-xl, padding 20px):
        Topic pills: "Content Marketing", "Editorial Design", "AI Writing",
        "Publishing Strategy" (Slate-100 bg, text-sm Slate-600, rounded-full).

      "Suggested writers" card (20px below, white, rounded-xl, padding 20px):
        3 writer rows: avatar (40px) + name + bio snippet (text-xs Slate-500, 1 line)
        + "Follow" small secondary button.

      "Trending articles" card (20px below, white, rounded-xl, padding 20px):
        3 articles: rank number (Geist Mono Violet-600) + title (text-sm Slate-700)
        + author (text-xs Slate-400).
```

---

## E — Writer Profile (Desktop) — NEW screen 14

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: Public Writer Profile, route "/u/[username]". Reader-facing.

TOP NAVBAR: standard Inkwell navbar.

MAIN AREA (no sidebar, full-width, max-width 960px centered):

  HERO SECTION (40px below navbar):
    Horizontal layout: avatar (96px, rounded-full, 1px Slate-200 border) left.
    Right of avatar (24px gap):
      Name: "Amira Okafor" (text-2xl font-semibold Slate-900).
      Bio: "Senior Editor at Meridian Digital. Exploring the intersection of
      generative linguistics and modern urbanism." (text-base Slate-600).
      Location: Phosphor MapPin + "Lagos, Nigeria" (text-sm Slate-500) ·
      Phosphor CalendarBlank + "Joined Mar 2024" (text-sm Slate-500).

    Stats row (16px below bio, inline):
      "247 articles" · "3.2K followers" · "18.4K lifetime readers"
      (numbers in Geist Mono font-semibold Slate-900, labels text-sm Slate-500).

    Action row (beside stats, right-aligned):
      "Follow" primary button (Violet-600, Phosphor UserPlus).
      Phosphor ShareNetwork ghost icon button.

  TABS (24px below hero):
    "Articles" (active), "About". Full-width 1px Slate-200 bottom border.

  TWO-COLUMN LAYOUT (24px below tabs):

    LEFT COLUMN (flex-1, max-width 640px) — Article list:
      Filter pills: "All" (active), "Public", "Premium", "Marketplace".

      Article cards (16px gap): horizontal layout.
        Left: title (text-lg font-medium) + excerpt (text-sm Slate-500, 2 lines)
        + meta row (date Geist Mono · reading time · placement badge) + reactions.
        Right: thumbnail (140x90px, rounded-lg).
      5 articles. "Load more" below.

    RIGHT COLUMN (280px) — Sticky sidebar:
      "About" card (white, rounded-xl, padding 20px):
        Short bio + topics as pills + website link (Violet-600).
      "Also writes in" card (20px below):
        Magazine names the writer has contributed to: "The Atlantic Review",
        "Prose & Pixel" (text-sm Slate-600, with small magazine icon).
```

---

## F — Magazine Profile (Desktop) — NEW screen 15

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: Public Magazine Profile, route "/m/[slug]". Visible to any reader.

TOP NAVBAR: standard Inkwell navbar.

MAIN AREA (no sidebar, full-width, max-width 1120px centered):

  HERO (40px below navbar):
    Magazine logo (72px, rounded-xl, 1px Slate-200 border) + text beside it.
    Name: "The Atlantic Review" (text-2xl font-semibold Slate-900).
    Tagline (text-base Slate-600).
    Category badges: "Technology" "Culture" "Design" (Slate-100, text-xs, rounded-full).
    Stats: "142 articles" · "23 writers" · "Since Jan 2025" (Geist Mono).
    Subscribe button (Violet-600) or "Subscribed" pill (Emerald-50).

  TABS (24px below): "Published articles" (active), "Writers", "About".

  THREE-COLUMN ARTICLE GRID (24px below tabs):
    2-column CSS Grid (not 3 — per design system anti-patterns), 20px gap.
    Each card: thumbnail (full-width, 180px height) + content below.
      Writer + title + meta + placement badge.
      Lock overlay if not subscribed.
    8 cards. "Load more" below.

  RIGHT SIDEBAR (280px, floated right on wide screens):
    "Featured writers" card: 4 writers with avatars + names.
    "Subscription" card: plan info + "Subscribe" CTA.
```

---

## G — Settings (Desktop) — NEW screen 16

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: User Settings, route "/settings".

LEFT SIDEBAR (240px, dashboard nav): Settings active (Violet-50 bg, Violet-700 text).

MAIN AREA (padding 32px):
  "Settings" page title (text-2xl font-semibold Slate-900).

  LEFT SUB-NAV (200px, inline with main content, acting as section anchors):
    "Profile" (active — Violet-600 text), "Account", "Notifications", "Danger zone"
    (text-sm Slate-500, vertical list, 8px gap, sticky top).

  RIGHT CONTENT (flex-1, max-width 560px):
    Sections laid out vertically with 32px gap:

    PROFILE section: avatar (80px) + change/remove buttons. Form fields (name, username
    with helper, bio textarea, location, website). Save + Cancel buttons.

    ACCOUNT section: email row (with verified badge + change link), password row,
    connected accounts (Google).

    NOTIFICATIONS section: toggle rows (new follower, comments, likes, weekly digest,
    marketplace purchases, announcements). Toggle switches (Violet-600 when on).

    DANGER ZONE section: Red-100 border card, "Delete account" with destructive button.
```

---

## H — Notifications (Desktop) — NEW screen 17

```
Generate the DESKTOP (1440 × 900 px minimum) version of this screen.

Screen: Notifications page, route "/notifications".

LEFT SIDEBAR (240px): Notifications active (Violet-50 bg, Violet-700 text, Phosphor Bell).

MAIN AREA (padding 32px, max-width 800px):
  Header row: "Notifications" (text-2xl font-semibold Slate-900) + "Mark all as read"
  ghost button (text-sm Slate-400).

  Filter pills (16px below): "All" (active Violet-600), "Unread", "Comments",
  "Purchases", "Followers". Rounded-full, text-sm.

  Notification list card (white, rounded-xl, 1px Slate-200 border):
    Date group headers: "Today" (text-xs uppercase Slate-400, Slate-50 bg).

    Unread rows: 4px Violet-600 left border, Slate-50 bg tint.
      Avatar (36px) + rich text (bold actor name + action + bold object) + preview
      snippet (text-xs Slate-500 italic) + timestamp (Geist Mono text-xs Slate-400).
      Right: type icon (ChatCircle / ShoppingCart / Heart / UserPlus, Slate-300).

    Read rows: no left border, white bg, slightly lighter text.

    "Yesterday" group + 3 read rows.
    "This week" group + 2 rows.

  Pagination: "Showing 8 of 34" (text-xs Slate-400 Geist Mono) + "Load more" button.
```
