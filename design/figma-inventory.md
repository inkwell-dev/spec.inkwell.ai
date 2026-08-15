# Figma File Inventory

**File:** [Web Prototype](https://www.figma.com/design/D5PDq6r8KbkAg34RECWfYQ/Web-Prototype)
**Pages:** Prototype (58 screens), Design System (63 components + variables)
**Last synced:** 2026-06-10

---

## Figma structure

| Page | Node ID | Contents |
|------|---------|----------|
| Prototype | 13:10 | 58 screens organized into 11 Figma Sections |
| Design System | 51:10 | 63 reusable components (15 foundation + 48 screen-extracted), typography scale, color swatches |

### Variables collection
- **Name:** Inkwell Design Tokens
- **Tokens:** 39 total (22 colors, 13 spacing, 4 border radii)

### Component instancing
- **148 component instances** (5 families) used across **35 screens** (60% of all screens)
- Buttons: ×62 — Primary, Secondary, Ghost, Destructive variants across auth, publish, marketplace, settings, article, earnings screens
- Badges: ×23 — Success (ELIGIBLE, PURCHASED), Warning (PREVIEWED), Accent (PREMIUM, topics), Neutral (categories)
- Inputs: ×20 — Default state inputs across all 6 auth screens (mobile + desktop)
- Navigation: Mobile Navbar ×6, Desktop Navbar ×3, Left Sidebar ×4, Bottom Tab Bar ×10
- Content: Article Feed Cards ×6, Stat Cards ×2, Charts ×2, Tables ×1, Widgets ×1, Dashboard Cards ×7
- Toggle: ×1 (Writer toggle on Personal Sign Up)
- All DS components use unified Geist font family (158 font nodes corrected)
- Edits to source components propagate to all instances automatically

---

## All screens (58 total)

### Mobile screens (390px wide) — 28 screens

| # | Figma ID | Name | Section | Maps to prompt |
|---|----------|------|---------|----------------|
| 1 | 13:11 | Write Editor | 04 — Editor | — (bonus) |
| 2 | 13:71 | Writer Dashboard | 08 — Writer Dashboard | — (bonus) |
| 3 | 13:219 | Marketplace Feed | 09 — Marketplace | — (bonus) |
| 4 | 13:343 | Discovery & Search | 05 — Search & Discovery | — (bonus) |
| 5 | 13:513 | Login | 01 — Auth | 06-auth.md |
| 6 | 13:568 | Magazine Sign Up | 01 — Auth | 06-auth.md |
| 7 | 13:637 | Personal Sign Up | 01 — Auth | 06-auth.md |
| 8 | 13:710 | Home Feed | 02 — Home Feed | 01-home-feed.md |
| 9 | 13:875 | Article: Premium Locked | 03 — Article Variants | 02-article.md |
| 10 | 13:965 | Article: Marketplace Previewed | 03 — Article Variants | 02-article.md |
| 11 | 13:1068 | Article: Marketplace Buy | 03 — Article Variants | 02-article.md |
| 12 | 13:1189 | Article: Free Read | 03 — Article Variants | 02-article.md |
| 13 | 13:1330 | Article: Marketplace Purchased | 03 — Article Variants | 02-article.md |
| 14 | 13:1489 | Article Editor & AI Assistant | 04 — Editor | 03-editor-ai-chat.md |
| 15 | 13:1620 | Article Editor: Inline AI Actions | 04 — Editor | 04-editor-inline-popup.md |
| 16 | 13:1674 | Writer Analytics | 08 — Writer Dashboard | 05-writer-analytics.md |
| 17 | 13:1927 | Magazine Subscription Wall | 09 — Marketplace | 07-magazine-subscription.md |
| 18 | 13:1986 | Marketplace Browse | 09 — Marketplace | 08-marketplace-browse.md |
| 19 | 13:2145 | Writer Profile: Evaluation Mode | 06 — Writer Profile | 09-writer-evaluation.md |
| 20 | 13:2546 | Magazine Library | 10 — Magazine Dashboard | 10-magazine-library.md |
| 21 | 13:2708 | Subscription & Credits Dashboard | 10 — Magazine Dashboard | 11-magazine-subscription-dashboard.md |
| 22 | 13:2900 | Writer Earnings Dashboard | 08 — Writer Dashboard | 12-writer-earnings.md |
| 23 | 13:3141 | Publish Modal: Eligible Writer | 11 — Common | 13-publish-flow.md |
| 24 | 13:3244 | Publish Modal: Not Yet Eligible | 11 — Common | 13-publish-flow.md |
| 25 | 27:2 | Writer Profile (public) | 06 — Writer Profile | 14-writer-profile.md |
| 26 | 27:475 | Magazine Profile (public) | 07 — Magazine Profile | 15-magazine-profile.md |
| 27 | 27:916 | Settings | 11 — Common | 16-settings.md |
| 28 | 27:1308 | Notifications | 11 — Common | 17-notifications.md |

### Desktop screens (1280px wide) — 30 screens

| # | Figma ID | Name | Section | Maps to prompt |
|---|----------|------|---------|----------------|
| 29 | 13:3354 | Article: Marketplace Buy (Desktop) | 03 — Article Variants | desktop-refinement.md §2 |
| 30 | 13:3439 | Article: Premium Locked (Desktop) | 03 — Article Variants | desktop-refinement.md §2 |
| 31 | 13:3520 | Article: Marketplace Previewed (Desktop) | 03 — Article Variants | desktop-refinement.md §2 |
| 32 | 13:3610 | Home Feed (Desktop) | 02 — Home Feed | desktop-refinement.md §1 |
| 33 | 13:3823 | Article: Free Read (Desktop) | 03 — Article Variants | desktop-refinement.md §2 |
| 34 | 13:3979 | Article: Marketplace Purchased (Desktop) | 03 — Article Variants | desktop-refinement.md §2 |
| 35 | 13:4138 | Writer Analytics (Desktop) | 08 — Writer Dashboard | desktop-refinement.md §5 |
| 36 | 13:4505 | Article Editor & AI Assistant (Desktop) | 04 — Editor | desktop-refinement.md §3 |
| 37 | 13:4658 | Article Editor: Inline AI Selection (Desktop) | 04 — Editor | desktop-refinement.md §4 |
| 38 | 13:4732 | Article Editor: Inline AI Result (Desktop) | 04 — Editor | desktop-refinement.md §4 |
| 39 | 13:4807 | Personal Sign Up (Desktop) | 01 — Auth | desktop-refinement.md §6 |
| 40 | 13:4869 | Login (Desktop) | 01 — Auth | desktop-refinement.md §6 |
| 41 | 13:4915 | Magazine Sign Up (Desktop) | 01 — Auth | desktop-refinement.md §6 |
| 42 | 13:4990 | Magazine Subscription Wall (Desktop) | 09 — Marketplace | desktop-refinement.md §7 |
| 43 | 13:5053 | Marketplace Browse (Desktop) | 09 — Marketplace | desktop-refinement.md §8 |
| 44 | 13:5367 | Magazine Library (Desktop) | 10 — Magazine Dashboard | desktop-refinement.md §10 |
| 45 | 13:5567 | Subscription: Top-up Modal (Desktop) | 10 — Magazine Dashboard | desktop-refinement.md §11 |
| 46 | 13:5750 | Subscription & Credits Dashboard (Desktop) | 10 — Magazine Dashboard | desktop-refinement.md §11 |
| 47 | 13:5911 | Writer Profile: Evaluation Mode (Desktop) | 06 — Writer Profile | desktop-refinement.md §9 |
| 48 | 13:6262 | Writer Earnings (Desktop) | 08 — Writer Dashboard | desktop-refinement.md §12 |
| 49 | 13:6613 | Publish Modal: Eligible (Desktop) | 11 — Common | desktop-refinement.md §13 |
| 50 | 13:6722 | Publish Modal: Not Eligible (Desktop) | 11 — Common | desktop-refinement.md §13 |
| 51 | 27:194 | Writer Profile (Desktop) | 06 — Writer Profile | desktop-refinement.md prompt E |
| 52 | 27:622 | Magazine Profile (Desktop) | 07 — Magazine Profile | desktop-refinement.md prompt F |
| 53 | 27:1075 | Settings (Desktop) | 11 — Common | desktop-refinement.md prompt G |
| 54 | 27:1434 | Notifications (Desktop) | 11 — Common | desktop-refinement.md prompt H |
| 55 | 27:1646 | Writer Dashboard (Desktop) | 08 — Writer Dashboard | desktop-refinement.md prompt B |
| 56 | 27:1891 | Marketplace Feed (Desktop) | 09 — Marketplace | desktop-refinement.md prompt C |
| 57 | 27:2193 | Discovery & Search (Desktop) | 05 — Search & Discovery | desktop-refinement.md prompt D |
| 58 | 27:2484 | Write Editor (Desktop) | 04 — Editor | desktop-refinement.md prompt A |

---

## Figma Sections (Prototype page)

| # | Section | Pairs | Contains |
|---|---------|-------|----------|
| 01 | Auth | 3 | Login, Personal Sign Up, Magazine Sign Up |
| 02 | Home Feed | 1 | Home Feed |
| 03 | Article Variants | 5 | Free Read, Premium Locked, Marketplace Previewed, Marketplace Buy, Marketplace Purchased |
| 04 | Editor | 4 | Write Editor, AI Assistant, Inline AI Selection, Inline AI Result |
| 05 | Search & Discovery | 1 | Discovery & Search |
| 06 | Writer Profile | 2 | Writer Profile (public), Writer Profile: Evaluation Mode |
| 07 | Magazine Profile | 1 | Magazine Profile (public) |
| 08 | Writer Dashboard | 3 | Writer Dashboard, Writer Analytics, Writer Earnings |
| 09 | Marketplace | 3 | Marketplace Feed, Marketplace Browse, Magazine Subscription Wall |
| 10 | Magazine Dashboard | 3 | Magazine Library, Subscription & Credits, Top-up Modal |
| 11 | Common | 4 | Notifications, Settings, Publish Modal: Eligible, Publish Modal: Not Eligible |

---

## Coverage

- **Mobile screens:** 28/28 (100%)
- **Desktop screens:** 30/30 (100%)
- **Total:** 58 screens — all designed, no gaps remaining
- **Design System:** 87 components (with variants) across 10 sections, unified Geist font
- **Component instances:** 148 instances (5 component families) in 35 screens (60% of all screens use DS components)
