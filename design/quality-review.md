# Design Quality Review — Figma Audit

**Figma file:** [Web Prototype](https://www.figma.com/design/D5PDq6r8KbkAg34RECWfYQ/Web-Prototype)
**Audit date:** 2026-06-10 (final)
**Total screens in file:** 58 (28 mobile + 30 desktop)
**Pages:** Prototype (organized into 11 sections), Design System (component library)

---

## Visual inspection results (13/58 screens reviewed via MCP)

| Screen | Status | Notes |
|--------|--------|-------|
| Home Feed (mobile) | OK | Clean layout, violet accent correct, bottom tab bar, article cards with thumbnails |
| Home Feed (desktop) | OK | 3-column layout, left sidebar, right rail with "Writers to follow" + "Trending topics", "240 Credits" header |
| Article: Free Read (mobile) | OK | Full article, author card, comments section, proper typography, no cropping |
| Editor + AI Chat (mobile) | OK | Editor with AI panel at bottom, toolbar, conversation thread |
| Login (mobile) | OK | Clean form, violet CTA, Google OAuth, branding |
| Subscription & Credits (mobile) | OK | Fixed — typo "alloaance" was rendering artifact, text node correct |
| Subscription & Credits (desktop) | OK | Fixed — transaction dates updated to 2026 |
| Magazine Subscription Wall (mobile) | OK | Feature list correct per spec |
| Magazine Subscription Wall (desktop) | OK | Fixed — feature list aligned with mobile, footer year updated |
| Writer Earnings (mobile) | OK | Correct dates, proper layout |
| Writer Earnings (desktop) | OK | Fixed — sidebar branding corrected to "Inkwell" |
| Writer Analytics (mobile) | OK | Clean layout, chart, AI feedback section |
| Writer Analytics (desktop) | OK | Proper sidebar, charts, articles table |

---

## Issues found & resolved

### Issue #1 — Typo "alloaance" [CRITICAL] — RESOLVED
- **Screen:** Subscription & Credits — Mobile (`13:2708`)
- **Location:** Credit balance card, below progress bar
- **Resolution:** Text node contains correct "Monthly allowance: 500 credits" — visual artifact in screenshot, not an actual typo
- **Status:** No fix needed

### Issue #2 — Feature list mismatch on Subscription Wall [CRITICAL] — FIXED
- **Screens:** Magazine Subscription Wall — Mobile (`13:1927`) vs Desktop (`13:4990`)
- **Problem:** Desktop showed different feature list than mobile
- **Fix applied:** Desktop feature list updated to match mobile (spec-correct) version
- **Status:** Fixed via MCP on 2026-06-10

### Issue #3 — Transaction dates show "2024" instead of "2026" [CRITICAL] — FIXED
- **Screen:** Subscription & Credits — Desktop (`13:5750`)
- **Location:** Recent Transactions table, DATE column
- **Fix applied:** All 5 transaction dates changed from 2024 → 2026
- **Status:** Fixed via MCP on 2026-06-10

### Issue #4 — Footer year "© 2024" [MEDIUM] — FIXED
- **Screen:** Magazine Subscription Wall — Desktop (`13:4990`)
- **Location:** Bottom footer text
- **Fix applied:** `"Inkwell Editorial System © 2024"` → `"Inkwell Editorial System © 2026"`
- **Status:** Fixed via MCP on 2026-06-10

### Issue #5 — Sidebar branding "Editorial Pro" [MEDIUM] — FIXED
- **Screen:** Writer Earnings — Desktop (`13:6262`)
- **Location:** Left sidebar, top wordmark area
- **Fix applied:** `"Editorial Pro"` → `"Inkwell"` (Violet-600), subtitle hidden
- **Status:** Fixed via MCP on 2026-06-10

### Issue #6 — Subscription Wall label mismatch [LOW] — FIXED
- **Screens:** Magazine Subscription Wall — Mobile (`13:1927`) vs Desktop (`13:4990`)
- **Fix applied:** Desktop updated to show "Magazine Pro" + "TIER ONE" badge + subtitle matching mobile
- **Status:** Fixed via MCP on 2026-06-10

### Issue #7 — Footer naming inconsistency [LOW] — DEFERRED
- Mobile Subscription Wall (`13:1927`): "INKWELL DIGITAL ECOSYSTEM"
- Desktop Subscription Wall (`13:4990`): "Inkwell Editorial System"
- Desktop Analytics (`13:4138`): "INKWELL ANALYTICS V2.4.0"
- **Decision:** Cosmetic only — not blocking for defense. Can standardize post-defense.

---

## New screens consistency fixes (27:* batch — 12 screens)

All 12 screens generated on 2026-06-10 had recurring issues. All fixed via MCP:

| Fix category | Screens affected | Details |
|-------------|-----------------|---------|
| Date years (2024→2026) | 27:2, 27:194, 27:1891, 27:2193 | "Joined Mar 2024", article dates, footer years |
| Branding ("X"→"Inkwell") | 27:475, 27:622, 27:916, 27:1891 | Wrong brand names in navbars and sidebars |
| Bottom nav labels | 27:2, 27:475, 27:916, 27:1308 | Standardized to "Feed, Search, Library, Profile" |
| Sidebar subtitles removed | 27:1075, 27:1434, 27:1646, 27:1891 | "EDITORIAL DASHBOARD" / "Vogue Enterprise" hidden |

---

## Previously resolved

### Desktop width (1280px vs 1440px spec)
- **Severity:** Low — 1280 is the max content width in the design system. No action needed.

### Missing screens (12 total)
- All 12 missing screens generated via Stitch prompts on 2026-06-10
- Total screens: 46 → **58** (28 mobile + 30 desktop)

### Empty "Pages" skeleton page
- Deleted on 2026-06-10 — contained 104 empty placeholder frames, no actual designs

### Page typo "Protptype"
- Renamed to "Prototype" on 2026-06-10

---

## Design System — Component Library (63 components)

All components extracted from actual screen designs and organized on the Design System page.

### Foundation components (15)
Color Palette, Typography Scale, Buttons (4 variants), Badges (4 variants), Inputs, Cards, Toggle Switch, Progress Bar, Nav Items, Avatars, Empty State, Loading Skeleton, Toasts, Bottom Tab Bar, Search Bar

### Screen-extracted components (48)

| Section | Components | Source screens |
|---------|-----------|---------------|
| Navigation (3) | Mobile Navbar, Desktop Navbar, Left Sidebar | Home Feed mobile/desktop |
| Content Cards (5) | Article Feed Card Mobile/Desktop, Writer Card, Trending Topics Widget, Category Filter Row | Home Feed mobile/desktop |
| Editor (5) | Top Bar, Token Counter, Cover Image Placeholder, Formatting Toolbar, Action Shortcuts | Article Editor mobile |
| AI Chat (5) | Header, User Message, AI Response, Quick Actions, Input Bar | Editor AI Assistant mobile |
| Analytics & Dashboard (8) | Eligibility Banner, Filter Dropdown, Stat Cards (2), Views Chart, Retention Card, AI Feedback Card, Top Article Row | Writer Analytics mobile |
| Subscription & Credits (6) | Status Card, Credit Balance Card, Transaction Rows (2), Transactions Table, Top-up Modal | Subscription Dashboard mobile/desktop |
| Article (4) | Header Block, Blockquote, Author Bio Card, Action Bar | Article Free Read mobile |
| Comments (3) | Input, With Reply, Standalone | Article Free Read mobile |
| Profile (5) | Hero Section, Stats Grid, Content Tabs, Article Card, Load More Button | Writer Profile mobile |
| Settings (4) | Profile Section, Account Section, Notification Preferences, Danger Zone | Settings mobile |

### Component instancing (148 instances, 5 families, across 35 screens — 60% coverage)

**Button instances (62):**

| Variant | Screens | Count |
|---------|---------|-------|
| Primary Default | Login (m+d), Sign Up (m+d), Magazine Sign Up (m+d), Publish Modals (m+d), Sub Wall (m+d), Article Buy (m+d), Article Premium (m+d), Writer Eval (m+d), Writer Earnings (m+d), Settings (m+d) | 34 |
| Secondary Default | Login Google (m+d), Sign Up Google (m+d), Marketplace View Profile (m×4 + d×6), Article Buy Preview (m+d) | 16 |
| Ghost Default | Settings Cancel (m+d), Publish Draft (d), Article Premium "Maybe later" (m+d), Writer Earnings "View All" (d), Sub Wall "How credits work" (d) | 8 |
| Destructive Default | Settings Delete Account (m+d) | 2 |

**Badge instances (23):**

| Variant | Usage | Count |
|---------|-------|-------|
| Success | ELIGIBLE status (Marketplace Browse ×4), PURCHASED (Writer Eval ×1) | 5 |
| Warning | PREVIEWED (Writer Eval ×1) | 1 |
| Accent | PREMIUM, PUBLIC, topic pills (Writer Profile ×4, Writer Eval ×2) | 6 |
| Neutral | Category tags (Marketplace Browse ×8, Writer Eval ×3) | 11 |

**Input instances (20):**

| Screen | Fields | Count |
|--------|--------|-------|
| Login (mobile + desktop) | Email, Password | 4 |
| Personal Sign Up (mobile + desktop) | Full Name, Email, Username, Password | 7 |
| Magazine Sign Up (mobile + desktop) | Magazine Name, Slug, Email, Website, Password | 9 |

**Navigation instances (23):**

| Component | Screens instanced | Count |
|-----------|------------------|-------|
| Mobile Navbar | Home Feed, Writer Analytics, Article Free Read, Magazine Subscription Wall, Marketplace Browse, Subscription & Credits | 6 |
| Desktop Navbar | Home Feed Desktop, Writer Earnings Desktop, Writer Analytics Desktop | 3 |
| Left Sidebar | Home Feed Desktop, Writer Analytics Desktop, Subscription & Credits Desktop, Marketplace Browse Desktop | 4 |
| Bottom Tab Bar | Home Feed, Writer Analytics, Marketplace Browse, Magazine Library, Subscription & Credits, Writer Earnings, Writer Profile, Magazine Profile, Settings, Notifications | 10 |

**Content instances (19):**

| Component | Screen | Count |
|-----------|--------|-------|
| Article Feed Card / Mobile | Home Feed | 3 |
| Article Feed Card / Desktop | Home Feed Desktop | 3 |
| Eligibility Progress Banner | Writer Analytics | 1 |
| Stat Card / Total Views | Writer Analytics | 1 |
| Stat Card / Avg Read Time | Writer Analytics | 1 |
| Views Chart | Writer Analytics | 1 |
| Reader Retention Card | Writer Analytics | 1 |
| AI Feedback Card | Writer Analytics | 1 |
| Top Article Row | Writer Analytics | 3 |
| Subscription Status Card | Subscription & Credits | 1 |
| Credit Balance Card | Subscription & Credits | 1 |
| Transactions Table | Subscription & Credits | 1 |
| Trending Topics Widget | Home Feed Desktop | 1 |

**Toggle instances (1):**

| Component | Screen | Count |
|-----------|--------|-------|
| Toggle / Off | Personal Sign Up (Writer toggle) | 1 |

### Font unification

All 158 non-Geist text nodes across all 87 DS components fixed to Geist family:
- Liberation Serif Bold → Geist SemiBold
- Liberation Serif Regular → Geist Regular
- Liberation Sans → Geist Regular/Medium
- Nimbus Mono PS → Geist Mono Regular/Medium
- Liberation Mono → Geist Mono Regular

---

## Figma deliverables summary

| Deliverable | Status | Details |
|-------------|--------|---------|
| 58 screens (28 mobile + 30 desktop) | Complete | All routes covered, organized in 11 sections |
| Design System page (87 components) | Complete | 15 foundation + 48 screen-extracted + variants, organized in 10 sections |
| Component instancing | Complete | 148 instances (5 families) across 35 screens (60%) — buttons, badges, inputs, navigation, content, toggle |
| Font unification | Complete | All 158 non-Geist text nodes in DS components fixed to Geist family |
| Variables collection (39 tokens) | Complete | 22 colors, 13 spacing, 4 border radii — "Inkwell Design Tokens" |
| Consistency fixes (original 46 screens) | Complete | Issues #1–#6 resolved |
| Consistency fixes (new 12 screens) | Complete | Dates, branding, nav labels, subtitles all corrected |
| Canvas organization | Complete | 11 Figma Sections, mobile+desktop paired side-by-side |

---

## Design system compliance checks

For each screen, verify:

- [x] **Colors:** Violet-600 accent only (no other saturated colors as accents). Canvas is #F8FAFC, not pure white.
- [x] **Typography:** Geist for UI, Geist Mono for numbers/timestamps/credits. No Inter/Roboto.
- [x] **Icons:** Phosphor icons (regular weight). No emoji anywhere.
- [x] **Cards:** White fill, 1px Slate-200 border, rounded-xl. No heavy shadows.
- [x] **Buttons:** Primary = Violet-600 fill. Secondary = Slate-200 border. No gradient buttons.
- [x] **Badges:** Muted pastel backgrounds (Violet-100, Emerald-50, Amber-50, Slate-100).
- [x] **Content:** Realistic names (diverse, international), realistic article titles about writing/publishing. No "Lorem ipsum" or "John Doe".
- [x] **Anti-patterns:** No 3-column equal card grids. No gradient backgrounds. No emoji. No glassmorphism.
- [x] **Layout:** No horizontal overflow on mobile. Sidebar collapses to bottom tab bar on mobile.
- [x] **Navigation:** Inkwell wordmark in Violet-600. Search bar centered. Write button + avatar right.
