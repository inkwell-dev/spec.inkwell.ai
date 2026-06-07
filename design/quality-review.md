# Design Quality Review — Figma Audit

**Figma file:** [Web Prototype](https://www.figma.com/design/D5PDq6r8KbkAg34RECWfYQ/Web-Prototype)
**Audit date:** 2026-06-07
**Total screens in file:** 46 (24 mobile + 22 desktop)

---

## Visual inspection results (5/46 screens reviewed via MCP)

| Screen | Status | Notes |
|--------|--------|-------|
| Home Feed (mobile) | OK | Clean layout, violet accent correct, bottom tab bar, article cards with thumbnails |
| Home Feed (desktop) | OK | 3-column layout, left sidebar, right rail with "Writers to follow" + "Trending topics", "240 Credits" header |
| Article: Free Read (mobile) | OK | Full article, author card, comments section, proper typography, no cropping |
| Editor + AI Chat (mobile) | OK | Editor with AI panel at bottom, toolbar, conversation thread |
| Login (mobile) | OK | Clean form, violet CTA, Google OAuth, branding |

**Remaining 41 screens need manual visual inspection** — Figma MCP rate limit (Starter plan) blocked further automated review.

---

## Issues found

### 1. Desktop width discrepancy
- **Expected:** 1440px (per design system prompts and `DESKTOP-PROMPTS.md`)
- **Actual:** 1280px in all desktop frames
- **Severity:** Low — 1280 is the max content width specified in the design system, so layouts are correct. The extra 160px would just be canvas margins. No action required for implementation.

### 2. Missing desktop counterparts for 4 mobile screens
These mobile screens were generated but have no desktop version in the Figma file:

| Mobile screen | Figma ID | Action |
|---------------|----------|--------|
| Write Editor | 13:11 | Generate desktop via `desktop-refinement.md` prompt A |
| Writer Dashboard | 13:71 | Generate desktop via `desktop-refinement.md` prompt B |
| Marketplace Feed | 13:219 | Generate desktop via `desktop-refinement.md` prompt C |
| Discovery & Search | 13:343 | Generate desktop via `desktop-refinement.md` prompt D |

### 3. Missing screens entirely (no mobile or desktop)
These screens are in the spec but have no Figma representation:

| Screen | Route | Priority | Action |
|--------|-------|----------|--------|
| Writer Profile (public) | `/u/[username]` | High | New prompt `14-writer-profile.md` created |
| Magazine Profile (public) | `/m/[slug]` | High | New prompt `15-magazine-profile.md` created |
| Settings | `/settings` | Medium | New prompt `16-settings.md` created |
| Notifications | `/notifications` | Medium | New prompt `17-notifications.md` created |
| Admin moderation | `/admin/*` | Low (post-MVP) | Not yet prompted |

---

## Manual checklist — verify in Figma

Go through each screen in the Figma file and check for these issues. Mark each cell Y/N.

### Mobile screens (390px)

| # | Screen | Not cropped | Bottom nav visible | Text readable | Violet accent correct | Scrollable content complete |
|---|--------|-------------|--------------------|--------------|-----------------------|-----------------------------|
| 1 | Write Editor | | | | | |
| 2 | Writer Dashboard | | | | | |
| 3 | Marketplace Feed | | | | | |
| 4 | Discovery & Search | | | | | |
| 5 | Login | Y | N/A | Y | Y | Y |
| 6 | Magazine Sign Up | | | | | |
| 7 | Personal Sign Up | | | | | |
| 8 | Home Feed | Y | Y | Y | Y | Y |
| 9 | Article: Premium Locked | | | | | |
| 10 | Article: Marketplace Previewed | | | | | |
| 11 | Article: Marketplace Buy | | | | | |
| 12 | Article: Free Read | Y | Y | Y | Y | Y |
| 13 | Article: Marketplace Purchased | | | | | |
| 14 | Editor + AI Assistant | Y | N/A | Y | Y | Y |
| 15 | Editor: Inline AI Actions | | | | | |
| 16 | Writer Analytics | | | | | |
| 17 | Magazine Subscription Wall | | | | | |
| 18 | Marketplace Browse | | | | | |
| 19 | Writer Profile: Evaluation | | | | | |
| 20 | Magazine Library | | | | | |
| 21 | Subscription & Credits | | | | | |
| 22 | Writer Earnings | | | | | |
| 23 | Publish Modal: Eligible | | | | | |
| 24 | Publish Modal: Not Eligible | | | | | |

### Desktop screens (1280px)

| # | Screen | Not cropped | Sidebar present | Content centered | Right rail if needed | Responsive grid |
|---|--------|-------------|-----------------|-----------------|---------------------|-----------------|
| 25 | Article: Marketplace Buy | | | | | |
| 26 | Article: Premium Locked | | | | | |
| 27 | Article: Marketplace Previewed | | | | | |
| 28 | Home Feed | Y | Y | Y | Y | Y |
| 29 | Article: Free Read | | | | | |
| 30 | Article: Marketplace Purchased | | | | | |
| 31 | Writer Analytics | | | | | |
| 32 | Editor + AI Assistant | | | | | |
| 33 | Editor: Inline AI Selection | | | | | |
| 34 | Editor: Inline AI Result | | | | | |
| 35 | Personal Sign Up | | | | | |
| 36 | Login | | | | | |
| 37 | Magazine Sign Up | | | | | |
| 38 | Magazine Subscription Wall | | | | | |
| 39 | Marketplace Browse | | | | | |
| 40 | Magazine Library | | | | | |
| 41 | Subscription: Top-up Modal | | | | | |
| 42 | Subscription & Credits | | | | | |
| 43 | Writer Profile: Evaluation | | | | | |
| 44 | Writer Earnings | | | | | |
| 45 | Publish Modal: Eligible | | | | | |
| 46 | Publish Modal: Not Eligible | | | | | |

---

## Design system compliance checks

For each screen, verify:

- [ ] **Colors:** Violet-600 accent only (no other saturated colors as accents). Canvas is #F8FAFC, not pure white.
- [ ] **Typography:** Geist Sans for UI, Geist Mono for numbers/timestamps/credits. No Inter/Roboto.
- [ ] **Icons:** Phosphor icons (regular weight). No emoji anywhere.
- [ ] **Cards:** White fill, 1px Slate-200 border, rounded-xl. No heavy shadows.
- [ ] **Buttons:** Primary = Violet-600 fill. Secondary = Slate-200 border. No gradient buttons.
- [ ] **Badges:** Muted pastel backgrounds (Violet-100, Emerald-50, Amber-50, Slate-100).
- [ ] **Content:** Realistic names (diverse, international), realistic article titles about writing/publishing. No "Lorem ipsum" or "John Doe".
- [ ] **Anti-patterns:** No 3-column equal card grids. No gradient backgrounds. No emoji. No glassmorphism.
- [ ] **Layout:** No horizontal overflow on mobile. Sidebar collapses to bottom tab bar on mobile.
- [ ] **Navigation:** Inkwell wordmark in Violet-600. Search bar centered. Write button + avatar right.

---

## Figma organization prompt

After all screens are generated, paste this into Stitch or arrange manually in Figma:

> Reorganize the Figma canvas so each page has its mobile (390px) and desktop (1280px) 
> version placed side by side, with 80px horizontal gap. Group each pair under a labeled 
> Figma Section with the screen name. Order sections top-to-bottom matching the prompt 
> numbering (01 Home Feed, 02 Article variants, 03 Editor AI Chat, etc.). Place article 
> variants as sub-groups within the "02 Article" section.
