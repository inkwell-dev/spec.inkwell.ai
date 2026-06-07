# Desktop Prompts (1440px)

Paste each prompt into the **same Stitch chat** where you generated the mobile screens.
The design system preamble is already loaded — no need to re-paste it unless Stitch
has drifted (if it has, re-paste `00-design-system.md` before the first desktop prompt).

Each prompt references the mobile screen Stitch already generated and describes how
to expand it to the full desktop layout.

---

## 01 — Home Feed Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Home Feed screen.
The mobile version already exists — expand it to this desktop layout:

Three-rail layout on the #F8FAFC canvas:

LEFT RAIL (200px, sticky, left-aligned):
  Vertical nav with Phosphor icons + labels stacked vertically:
  Home (active — Violet-50 bg, Violet-700 text), Discover, Following, Your Library.
  Below a "Topics" section label (text-xs uppercase Slate-400), a vertical list of
  topic tag pills: Technology, Culture, Business, Science, Design, Politics.
  Each pill: text-sm, Slate-600, rounded-lg, no background, hover Slate-100 fill.

CENTER COLUMN (max 680px, centered between the two rails):
  Same content as the mobile feed — tag filter chips at top, then article cards.
  But cards now show the thumbnail RIGHT-ALIGNED (120x80px) beside the text content
  instead of stacked on top. The text (writer line, title, excerpt, action row) sits
  on the left, thumbnail on the right.
  Cards separated by 1px Slate-100 dividers, not gaps.
  The horizontal tag filter chips row is not scrollable — all visible at once.

RIGHT RAIL (260px, sticky, right-aligned):
  "Writers to follow" card: white card, 1px Slate-200 border, rounded-xl.
  3 writers: avatar (36px) + name (text-sm font-medium) + topic (text-xs Slate-500) +
  small outline "Follow" button. Rows separated by Slate-100 dividers.
  Below: "Trending topics" card: same style, topics as small Slate-100 bg pills.

Top navigation bar spans full width as defined in the design system.
No bottom tab bar on desktop — that is mobile only.
```

---

## 02 — Article Read View Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Article reading page.
The mobile version already exists — expand it to desktop layout:

Single centered reading column (max 680px) on #F8FAFC canvas. Top navbar full-width.

Everything from the mobile version stays the same (header, byline, hero image, body,
comments) but with these desktop-specific additions:

FLOATING ACTION BAR: a vertical bar fixed to the LEFT of the reading column, offset
48px from the column edge. Vertical stack of icons: heart + count, comment + count,
repost, bookmark. Each icon Phosphor regular 22px, Slate-400, hover Slate-600.
The bar stays sticky as the user scrolls. This replaces the mobile bottom action row.

The article body has more breathing room — generous padding, comfortable line-height
1.75 on 16px body text. Pull quotes have a 3px Violet-500 left border with 24px left
padding.

Author card below the article is horizontal layout: avatar (48px) on the left, name +
bio + follower count + Follow button on the right.

Comments show threaded replies indented 32px with a thin Slate-100 left border.

Also generate these additional desktop variants (can be separate frames or states):

VARIANT 2 — PREMIUM LOCKED: article fades to blur after 2 paragraphs, centered overlay
card (320px max-width) with lock icon + "Upgrade to Premium" Violet-600 button.

VARIANT 3 — MARKETPLACE (not previewed): title + excerpt only, no body. Price action
card below: "120 credits" in Geist Mono + "Preview — 12 credits" Violet button +
"Purchase directly — 120 credits" outline button.

VARIANT 4 — MARKETPLACE (previewed): full body visible, sticky Amber-50 banner at top
with "Purchase — 108 credits remaining" button.

VARIANT 5 — MARKETPLACE (purchased): full body, "In Meridian Digital's library"
Emerald-50 badge next to title.
```

---

## 03 — Editor + AI Chat Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Editor with AI Chat panel.
The mobile version already exists — expand to the full desktop split layout:

This is full-width, no marketing nav. A slim EDITOR TOP BAR instead:
  Left: back chevron + "Draft" + auto-save indicator ("Saved just now" Geist Mono).
  Right: token-quota chip ("1,240 tokens left" Geist Mono), "Preview" ghost button,
  "Publish" Violet-600 button.

MAIN AREA splits into two columns:

LEFT (~60%) — Writing canvas:
  White background, generous padding (48px horizontal).
  Borderless title input (text-3xl font-bold Slate-900, placeholder "Untitled article..."
  in Slate-300).
  Cover image upload strip (dashed Slate-200 border, "Add a cover image").
  Rich text body with a few paragraphs of draft content.
  Floating formatting toolbar shown above content (white card, border, icons: Bold, Italic,
  H1, H2, list, quote, code, link, image).
  Bottom-left: circular Violet-600 "Ask AI" button (Phosphor Sparkle) + mic button beside it.

RIGHT (~40%) — AI Chat panel:
  White background, 1px Slate-200 LEFT border, full viewport height.
  Header: "AI Assistant" + Sparkle icon + close X. 1px bottom border.
  Conversation: user bubble (Slate-100 bg, right-aligned) + AI response (no bg, left-aligned
  with Sparkle icon + "Inkwell AI" label). Action buttons below AI response: "Insert into
  article", "Replace selection", "Copy", "Regenerate".
  Quick-action chips: "Improve this paragraph", "Make it shorter", "Continue writing".
  Sticky bottom: chat input + send button + "Uses ~200 tokens" hint.

The two columns should have a clear visual boundary (the left border on the chat panel).
The editor canvas should feel spacious and focused — the chat panel is a tool, not the
main event.
```

---

## 04 — Editor Inline Popup Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Editor with inline AI selection popup.
The mobile version already exists — expand to desktop:

Full-width editor canvas (no AI chat panel — full width for writing). Same top bar as
the editor screen.

Show TWO states side by side (or as two frames):

STATE 1 — ACTION SELECTION:
  A sentence in the body text is highlighted (Violet-100 background selection).
  Floating popup ABOVE the selection: white card, 1px Slate-200 border, rounded-xl,
  subtle shadow. Horizontal row of buttons:
  Phosphor Sparkle (Violet-500) + "Reformulate" | "Shorten" | "Expand" | "Simplify" |
  "Improve". Each text-xs Slate-600, rounded-lg, hover Slate-100. Separated by Slate-100
  dividers. The popup is compact and precise — anchored to the selection.

STATE 2 — RESULT PREVIEW:
  The popup has expanded downward into a result card (wider than the action row).
  "Reformulated" label (text-xs Slate-400 Geist Mono) + Sparkle icon.
  Preview box: Slate-50 bg, 1px Slate-200 border, rounded-lg, the rewritten text inside.
  Three buttons: "Replace" (Violet-600), "Insert below" (outline), "Cancel" (ghost).
  "~80 tokens" hint (text-xs Slate-400 Geist Mono).

Surrounding editor content remains visible — the popup is clearly floating over the
editing canvas, not a modal. Token-quota chip visible in top bar.
```

---

## 05 — Writer Analytics Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Writer Analytics dashboard.
The mobile version already exists — expand to the sidebar + main desktop layout:

LEFT SIDEBAR (240px, white bg, 1px Slate-200 right border):
  Nav: My Articles, Analytics (active — Violet-50 bg, Violet-700 text), Earnings,
  Notifications, Settings. Phosphor icons.

MAIN AREA on #F8FAFC canvas:

  Eligibility progress banner (full-width card, only if not eligible):
    Violet-200 border. Phosphor Storefront icon + "Unlock the marketplace" heading.
    Two inline progress bars side by side: "3,247 / 5,000 readers" + "783 / 1,000 reactions".
    Geist Mono numbers. Or if eligible: small Emerald-50 badge.

  Page header: "Analytics" + date-range dropdown + article selector dropdown (right-aligned).

  4 KPI cards in a ROW (not 2x2 — full horizontal row on desktop):
    Total Views "12,847", Avg Read Time "4m 12s", Engagement Rate "63.2%",
    Total Likes "3,218". Each with sparkline + trend. Geist Mono tabular-nums.

  "Views over time" chart card: full width. Violet-500 line, Violet-100 gradient fill,
  clean axes in Geist Mono.

  Two-column row below chart:
    LEFT: "Scroll depth" horizontal bar chart (paragraph retention funnel).
    RIGHT: "AI feedback" card with Sparkle icon + bullet list of writing insights.

  "Top articles" table: 5 rows, columns: Title (with thumbnail), Views, Avg Read Time,
  Engagement, Likes. Geist Mono numbers. Row hover Slate-50.

  All cards white fill, 1px Slate-200 border, rounded-xl, generous padding.
```

---

## 06 — Auth Screens Desktop [GENERATED]

```
Generate the DESKTOP (1440px) versions of all three auth screens.
The mobile versions already exist — expand to centered desktop card layouts:

All three share: #F8FAFC canvas background, centered card with white fill, 1px Slate-200
border, rounded-xl, ultra-diffuse shadow (0 1px 3px rgba(0,0,0,0.04)).

VARIANT 1 — LOGIN (max-width 400px centered card):
  "Inkwell" wordmark (Violet-600) centered. "Welcome back" heading. Email input, password
  input with show/hide toggle. "Forgot password?" link right-aligned. "Sign in" Violet-600
  button full-width. "or" divider. "Continue with Google" outline button. "Don't have an
  account? Sign up" link below.

VARIANT 2 — PERSONAL SIGN UP (max-width 420px centered card):
  "Inkwell" wordmark. "Create your account" heading. Fields: name, email, username (with
  "/u/username" Geist Mono preview), password. "I want to write" toggle switch. "Create
  account" button. Google button. "Already have an account?" + "Are you a magazine?" links.

VARIANT 3 — MAGAZINE SIGN UP (max-width 560px centered card):
  "Inkwell" wordmark. "Register your magazine" heading. TWO-COLUMN form on desktop:
  Left column: magazine name, slug ("/m/slug" preview), email, password.
  Right column: website URL, description textarea, logo upload area (dashed border).
  Full-width below: "Create magazine account" button + subscription note.
  This is wider than the other auth cards because of the two-column layout.
```

---

## 07 — Magazine Subscription Wall Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Magazine Subscription Wall.
The mobile version already exists — expand to centered desktop layout:

Minimal top bar (Inkwell wordmark + avatar only). #F8FAFC canvas.

Centered container (max-width 520px):
  "Subscribe to access the marketplace" heading (text-2xl, centered).
  "Browse writers, preview articles, and build your curated library." subtext.

  Subscription plan card: white, 1px Slate-200 border, rounded-xl, 3px Violet-600 left
  accent bar. "Magazine Pro" plan name. "49 credits/month" large price in Geist Mono.
  Benefits checklist with Emerald-500 check icons (5 items).
  "Subscribe now" Violet-600 full-width button.

  Below card: expandable "How do credits work?" section — 3-step explanation in a Slate-50
  card when expanded. Step numbers in Geist Mono Violet-600.

  The card should feel prominent and confident on the wide desktop canvas — generous
  whitespace around it, not cramped.
```

---

## 08 — Marketplace Browse Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Marketplace Browse screen.
The mobile version already exists — expand to sidebar + main desktop layout:

LEFT SIDEBAR (240px): Marketplace (active), Library, Subscription & Credits,
Notifications, Settings.

MAIN AREA:
  Header: "Marketplace" title + "Discover writers and source content" subtitle.
  Credit balance pill top-right: "342 credits" Geist Mono on Slate-100 bg.

  Search bar (full width) + sort dropdown (right-aligned) on one row.
  Topic filter chips below: "All Topics" (Violet-600 selected), Technology, Culture, etc.

  WRITER GRID: 2-COLUMN grid (NOT 3-column — 2 wide cards per row). Each card: white,
  1px Slate-200 border, rounded-xl. Avatar (48px) + name + Emerald "Eligible" badge.
  Bio (1 line). Topic tag pills. Stats in Geist Mono ("12.4K readers · 3.2K reactions").
  "8 articles for sale" in Violet-600. "View profile" outline button full-width.
  
  Show 6 cards (3 rows of 2) with diverse writers: Amira Okafor, Luca Hernandez,
  Priya Nair, Tomoko Sato, Marcus Webb, Elif Aydin.

  Pagination at bottom.
```

---

## 09 — Writer Evaluation Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Writer Profile Evaluation screen.
The mobile version already exists — expand to full-width desktop layout:

No sidebar — this is a profile page. Top navbar full-width.

PROFILE HEADER (white bg, 1px Slate-200 bottom border, padding 32px):
  ASYMMETRIC layout (not centered):
  Left: large avatar (72px) with Violet-200 ring.
  Right of avatar: name "Amira Okafor" (text-2xl font-semibold), bio (text-sm Slate-500),
  topic pills, stats row in Geist Mono, Emerald "Marketplace eligible" badge.
  Far right: credit balance pill ("342 credits").

HORIZONTAL TAB BAR below header:
  "Audience" (active — Violet-600 text, 2px bottom border), "Content", "Quality",
  "Portfolio Insights", "Articles for Sale".

TAB 1 — AUDIENCE (generate fully):
  4 KPI cards in a horizontal row (not 2x2): Total Readers, Avg Views/Article, Followers,
  Reader Retention. Geist Mono + sparklines.
  "Reader growth" line chart (full-width card, Violet-500 line).
  Two-column: LEFT "Geographic distribution" bar chart, RIGHT "Engagement by article" table.

TAB 4 — PORTFOLIO INSIGHTS (generate fully):
  White card: Sparkle icon + "AI Portfolio Insights" heading.
  Structured sections: Voice & Tone (paragraph), Expertise Areas (Violet-100 tag pills),
  Consistency (8.4/10 in Geist Mono), Fit Assessment (paragraph), Strengths (emerald
  check bullets), Gaps (amber warning bullets).
  Footer: "Generated from 47 articles. Last updated 2h ago." Geist Mono.

TAB 5 — ARTICLES FOR SALE (generate fully):
  Horizontal card rows: title + excerpt | topic pill | price "120 credits" Geist Mono +
  preview price. Status badge per article (Not previewed / Previewed / Purchased).
  Action buttons: Preview, Purchase, or "Read in library" depending on state.
  Show 4 articles with mixed states.
```

---

## 10 — Magazine Library Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Magazine Library.
The mobile version already exists — expand to sidebar + main desktop layout:

LEFT SIDEBAR (240px): Marketplace, Library (active), Subscription & Credits,
Notifications, Settings.

MAIN AREA:
  Header: "Your Library" + "14 articles" count badge + subtitle + credit balance pill.
  Search + filter + sort row.

  Article list (NOT a grid — horizontal card rows):
  Each card: thumbnail (80x56px) LEFT | title + writer + excerpt CENTER | price + date +
  "Republish rights" Emerald badge + "Read article" button RIGHT.
  5 cards with realistic content, 12px vertical gaps between cards.

  "Previewed but not purchased (3)" collapsible section below: collapsed by default
  (Phosphor CaretRight icon). Same card style but Amber badges and "Purchase" buttons
  instead of "Read article". 3px Amber-50 left border on previewed cards.

  Pagination at bottom.
  
  The horizontal card layout should feel spacious with clear columns of information —
  thumbnail, content, and metadata are visually aligned across all cards.
```

---

## 11 — Subscription & Credits Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Magazine Subscription & Credits dashboard.
The mobile version already exists — expand to sidebar + main desktop layout:

LEFT SIDEBAR (240px): Marketplace, Library, Subscription & Credits (active),
Notifications, Settings.

MAIN AREA:
  Header: "Subscription & Credits".

  SECTION 1 — Subscription card (full width):
    White card, Violet-600 3px left accent bar. "Magazine Pro" + Emerald "Active" badge.
    "Renewed: May 1 · Expires: Jun 1 · Next renewal in 28 days" in Geist Mono.
    "Renew early" outline button + "Cancel subscription" ghost button.

  SECTION 2 — Credit balance card (full width):
    Large "342" in Geist Mono text-4xl + "/ 500 monthly" smaller.
    Full-width progress bar (Violet-600 fill at 68.4%, Slate-100 track).
    "Monthly allowance: 500 · Resets Jun 1" in Geist Mono.
    "Top up credits" Violet-600 button on the right side of the card.

  TOP-UP MODAL (show as overlay state):
    Centered modal (400px), white, rounded-xl, shadow. 2x2 grid of amount options
    (100 / 250 / 500 / Custom). Selected: Violet-600 border + Violet-50 bg.
    Price below. "Confirm top-up" button. Backdrop dimming.

  SECTION 3 — Transactions table (full width):
    Columns: Date, Type (badge), Article, Credits, Balance. 5 rows with realistic data.
    Color-coded: Emerald for positive (grants/top-ups), default for debits.
    Geist Mono for all numbers. Row hover Slate-50.
```

---

## 12 — Writer Earnings Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Writer Earnings dashboard.
The mobile version already exists — expand to sidebar + main desktop layout:

LEFT SIDEBAR (240px): My Articles, Analytics, Earnings (active), Notifications, Settings.

MAIN AREA:
  Header: "Earnings".

  Eligibility banner (conditional — same as analytics: Violet-200 border card with
  progress bars, or Emerald badge if eligible).

  4 KPI cards in a HORIZONTAL ROW: Total Earnings "2,453 credits", Preview Payouts
  "382 credits", Purchase Payouts "2,071 credits", Earnings Balance "1,204 credits"
  (this card gets Violet-50 bg tint). All in Geist Mono with sparklines + trends.

  "Earnings over time" chart: two-line chart — solid Violet-500 for purchase payouts,
  dashed Violet-300 for preview payouts. Legend top-right. Clean Geist Mono axes.

  "Top-earning articles" table: Title (with thumbnail), Preview Revenue, Purchase Revenue,
  Total Revenue, Magazines count. 5 rows. Totals row at bottom. Geist Mono numbers.

  "Recent transactions" compact list: date + type badge (Amber for preview, Emerald for
  purchase) + article title + amount (Emerald text) + magazine name. 4 items.

  Withdraw card: horizontal layout — "Available balance: 1,204 credits" left,
  "Withdraw" Violet-600 button right. "(Simulated in MVP)" note.
```

---

## 13 — Publish Flow Desktop [GENERATED]

```
Generate the DESKTOP (1440px) version of the Article Publish modal.
The mobile version already exists — expand to a centered desktop modal:

Editor canvas dimmed behind. Centered modal (max-width 520px), white, rounded-xl,
shadow, 1px Slate-200 border. Backdrop rgba(0,0,0,0.3).

TWO VARIANTS:

VARIANT 1 — ELIGIBLE WRITER:
  Header: "Publish your article" + close X.
  Compact article preview card (Slate-50 bg): thumbnail + title + excerpt.
  
  Placement selection: two radio cards SIDE BY SIDE (equal width):
    "Public" (Phosphor Globe, selected: Violet-600 border + Violet-50 bg):
      Sub-options when selected: "Free access" / "Premium access" radio choices.
    "Marketplace" (Phosphor Storefront):
      Sub-options when selected: price input (Geist Mono) + auto-calculated preview
      price + info note.
  
  Tags multi-select input. Excerpt textarea.
  Footer: "Save as draft" ghost + "Publish" Violet-600 button.

VARIANT 2 — NOT ELIGIBLE:
  "Marketplace" card greyed out (Slate-100 bg, opacity-60, Phosphor Lock icon).
  Inside: mini progress bars "3,247/5,000 readers" + "783/1,000 reactions".
  "Premium access" radio also greyed out with eligibility note.
  Only "Public > Free access" is selectable.
```
