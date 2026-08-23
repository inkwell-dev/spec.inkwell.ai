# 📄 09 - Design Specification

---

## 1. 🧠 Overview

This document covers the design system, tooling, and UI/UX structure for the Inkwell platform.

It defines:
- Design tooling and file structure
- Component library and design system
- Breakpoints and responsive strategy
- Sitemap and frame organization
- Role-based view variants

---

## 2. 🛠️ Design Tooling

| Tool | Purpose |
|------|---------|
| **Figma** | Primary UI design tool — wireframes, mockups, prototypes |
| **Google Stitch** | Rapid AI-generated high-fidelity screens (exported to Figma for prototyping) |
| **shadcn/ui Figma Kit** | Community component library (maps 1:1 to code components) |
| **Inter** | Primary typeface (matches shadcn/ui defaults) |

---

## 3. 🎨 Design System

### 3.1 Component Library

The Inkwell UI is built on **shadcn/ui**, which provides:
- Unstyled, accessible primitives via **Radix UI**
- Styled with **Tailwind CSS**
- Copy-paste components (no external dependency)
- Full TypeScript support

In Figma, the **shadcn/ui community kit** is used as the base component library. Brand tokens (colors, radius, spacing) are remapped on top of the kit's variables.

### 3.2 Color Tokens

| Token | Usage |
|-------|-------|
| `--background` | Page backgrounds |
| `--foreground` | Primary text |
| `--primary` | Brand accent — violet `#7c3aed` (CTAs, links) |
| `--secondary` | Secondary actions |
| `--muted` | Subtle text, placeholders |
| `--destructive` | Errors, delete actions — red `#ef4444` |
| `--success` | Positive states — emerald `#10b981` |
| `--border` | Dividers, input borders |
| `--ring` | Focus rings |

### 3.3 Typography Scale

| Level | Size | Usage |
|-------|------|-------|
| `text-4xl` | 36px | Page titles |
| `text-3xl` | 30px | Section headings |
| `text-2xl` | 24px | Card titles |
| `text-xl` | 20px | Sub-headings |
| `text-base` | 16px | Body text |
| `text-sm` | 14px | Secondary text, labels |
| `text-xs` | 12px | Captions, metadata |

---

## 4. 📐 Breakpoints

Two breakpoints are designed and implemented:

| Breakpoint | Width | Frame size in Figma |
|-----------|-------|---------------------|
| **Desktop** | 1440px | 1440 × 960 |
| **Mobile** | 375px | 375 × 812 |

> Tablet (768px) is intentionally excluded from the MVP scope to meet the September 2026 timeline.

---

## 5. 🗺️ Sitemap & Frame Structure

### 5.1 Figma File Organization

All frames live on a **single Figma page**, organized into 11 sections flowing top to bottom:

```
01 — Auth
02 — Home Feed
03 — Article
04 — Search & Discovery
05 — Writer Profile
06 — Magazine Profile
07 — Article Editor
08 — Marketplace (Magazine)
09 — Writer Dashboard
10 — Magazine Dashboard
11 — Admin
```

Each section contains frames for **both breakpoints** side by side:
- Desktop frames (4 columns, 1440px wide) on the left
- Mobile frames (6 columns, 375px wide) on the right

### 5.2 Frame Naming Convention

```
[ROLE] Page Name — Breakpoint
```

Examples:
- `[GUEST] Login — Desktop`
- `[READER FREE] Article — Premium Locked — Mobile`
- `[MAGAZINE] Writer Profile — Evaluation — Desktop`
- `[MAGAZINE] Marketplace Browse — Desktop`
- `[WRITER] Publish Modal — Eligible — Desktop`

### 5.3 Roles

| Role tag | Color | Description |
|----------|-------|-------------|
| `[GUEST]` | Gray | Unauthenticated visitor |
| `[READER FREE]` | Violet | Authenticated, free plan |
| `[READER PREMIUM]` | Deep violet | Authenticated, premium plan |
| `[WRITER]` | Emerald | Personal account with writer role |
| `[WRITER ELIGIBLE]` | Emerald + gold | Writer who has crossed marketplace eligibility threshold |
| `[MAGAZINE]` | Amber | Magazine account (active subscription) |
| `[MAGAZINE UNSUB]` | Amber (muted) | Magazine account (no active subscription) |
| `[ADMIN]` | Red | Platform administrator |
| `[ANY AUTH]` | Blue | Any authenticated user |

### 5.4 Total Frame Count

| Breakpoints | Variants | Total frames |
|-------------|----------|-------------|
| Desktop + Mobile | 52 role/page variants | **104 frames** |

---

## 6. 📋 Page Inventory

> **Reconciled with the build, 2026-08-23 (Phase 6).**
>
> This section was written before implementation and described a URL tree that was
> never built. Fifteen of its eighteen dashboard-area routes returned 404. It has been
> corrected against the running application, route by route; the notes below record
> which way each discrepancy was resolved and why, rather than silently replacing the
> old paths.
>
> **The one structural decision worth stating up front.** The writer's workspace nests
> under `/dashboard`, as originally designed — `/dashboard/articles`,
> `/dashboard/analytics`, `/dashboard/earnings` were built in Phase 6 to close that
> gap. Everything serving BOTH account types stays flat and shared: one
> `/notifications`, one `/settings`, one `/subscription`. The original scheme gave
> magazines a parallel `/m/dashboard/*` tree, which would have meant two URLs rendering
> the same settings page — and `design/prompts/16-settings.md` is explicit that there is
> one settings page for both account types, with role-specific sections inside it.
> Account type is resolved server-side from the token, not encoded in the path.

### Auth
| Frame | Role | Route |
|-------|------|-------|
| Login | GUEST | `/login` |
| Sign Up — Personal | GUEST | `/register` |
| Sign Up — Magazine | GUEST | `/register/magazine` |

> `/register`, not `/signup`. The route has been `/register` since Phase 1 — it matches
> the API's `POST /auth/register`, so the page and the endpoint it posts to share a
> name.

### Home Feed
| Frame | Role | Route | Notes |
|-------|------|-------|-------|
| Home Feed | GUEST | `/` | Excerpts only, click to login gate |
| Home Feed | READER FREE | `/` | Full feed, free articles (public only — no marketplace articles) |
| Home Feed | READER PREMIUM | `/` | Full feed, all public articles |
| Home Feed | WRITER | `/` | + Create Article CTA |
| Home Feed | MAGAZINE | `/` | + Marketplace CTA |

### Article `/articles/[slug]`
| Frame | Role | Notes |
|-------|------|-------|
| Article | GUEST | Preview, login gate |
| Article — Free | READER FREE | Full content |
| Article — Premium Locked | READER FREE | Locked, upgrade gate |
| Article — Free | READER PREMIUM | Full content |
| Article — Premium | READER PREMIUM | Full content |
| Article (own) | WRITER | Full content + edit button |
| Article (others) | WRITER | Access by plan |
| Marketplace Article — Not Previewed | MAGAZINE | Title + excerpt + price, preview CTA (10%), purchase CTA (100%) |
| Marketplace Article — Previewed | MAGAZINE | Full content + "Purchase remaining 90%" CTA |
| Marketplace Article — Purchased | MAGAZINE | Full content + "In library" badge |
| Article | ADMIN | Full content + moderate controls |

### Search & Discovery
| Frame | Role | Route |
|-------|------|-------|
| Search | GUEST | `/search` |
| Search | ANY AUTH | `/search` |
| Tag Browse | ANY AUTH | `/search?tag=[slug]` |

> Tag browse is a parameter on search, not a route of its own. It renders the same
> results list with the same controls, differing only in which filter arrives
> pre-applied — a separate `/tag/[tag]` page would have been a second copy of `/search`
> maintained in parallel. The "Topics" links in the sidebar, the mobile drawer and the
> trending-topics widget all point at this form.

### Writer Profile `/u/[username]`
| Frame | Role | Notes |
|-------|------|-------|
| Writer Profile | GUEST | Articles + stats, follow gate |
| Writer Profile | READER FREE | + Follow button |
| Writer Profile | READER PREMIUM | + Follow button |
| Writer Profile (own) | WRITER | + Edit profile + eligibility progress |
| Writer Profile (others) | WRITER | + Follow button |
| Writer Profile — Evaluation | MAGAZINE | Audience, Content, Quality, AI Portfolio Insights + marketplace articles with preview/purchase CTAs |
| Writer Profile | ADMIN | + Ban / moderate controls |

### Magazine Profile `/m/[slug]`
| Frame | Role | Notes |
|-------|------|-------|
| Magazine Profile (Library) | GUEST | Purchased articles, read-only |
| Magazine Profile (Library) | READER FREE | + Follow |
| Magazine Profile (Library) | READER PREMIUM | + Follow |
| Magazine Profile (own) | MAGAZINE | + Manage library |
| Magazine Profile | ADMIN | + Moderate controls |

### Article Editor `/editor/[id]`
| Frame | Role | Notes |
|-------|------|-------|
| Editor | WRITER | Base editor |
| Editor + AI Chat | WRITER | AI chat panel overlay (premium) |
| Editor + Inline Popup | WRITER | Inline editing popup on text select (premium) |
| Editor + Voice Input | WRITER | Voice-to-article overlay (premium) |
| Publish Modal — Eligible | WRITER ELIGIBLE | Placement choice (public/marketplace) + pricing |
| Publish Modal — Not Eligible | WRITER | Public only, marketplace greyed out + progress |

### Marketplace (Magazine)
| Frame | Role | Route | Notes |
|-------|------|-------|-------|
| Subscription Wall | MAGAZINE UNSUB | in-page state on `/marketplace` and `/discover` | Mandatory before marketplace access |
| Marketplace Browse | MAGAZINE | `/discover` | Writer discovery, filterable grid. **Built at `/discover`, not `/marketplace`** (2026-08-10): the writer evaluation report already lives at `/discover/writers/[username]`, so the browse surface sits directly above it. `/marketplace` stays reserved for Phase 5's browse of marketplace-listed *articles*. |

### Writer Dashboard `/dashboard`
| Frame | Role | Route |
|-------|------|-------|
| Overview | WRITER | `/dashboard` |
| My Articles | WRITER | `/dashboard/articles` |
| Analytics + Eligibility | WRITER | `/dashboard/analytics` |
| Earnings | WRITER | `/dashboard/earnings` |

> **Personal accounts only.** Every endpoint behind these four answers a magazine with
> 403 (`accountTypes: ['personal']` on `/me/analytics`, `/me/earnings`,
> `/me/eligibility`), so `src/proxy.ts` redirects a magazine off `/dashboard` to
> `/marketplace` rather than rendering four empty states.
>
> **Overview** is the root of the tree rather than a redirect to My Articles. It answers
> a question the deeper pages cannot — "is anything happening" — with four figures on one
> line, and is the layout specified in `design/prompts/desktop-refinement.md` §B.
>
> **`/dashboard/earnings` moved here from `/earnings`** in Phase 6. The old path still
> redirects: it is five phases old, appears in the E2E matrix, and is the subject of a
> committed report figure.
>
> **Notifications and Settings have moved out of this table** — see Shared Surfaces
> below. Both serve every account type from one page, so filing them under a writer
> prefix would have been wrong twice over.

### Magazine Surfaces
| Frame | Role | Route |
|-------|------|-------|
| Library | MAGAZINE | `/library` |
| Subscription & Credits | MAGAZINE | `/subscription` |
| Credit Top-Up Modal | MAGAZINE | `/subscription` (modal overlay) |

> There is no `/m/dashboard/*` tree. It was specified as a mirror of the writer's, but
> three of its five frames were pages every account type shares, and the two that are
> genuinely magazine-only need no prefix to say so — the API refuses a personal account
> on both. `/subscription` in particular is deliberately shared: it is the magazine's
> subscription AND the personal plan switch, which is why the two use one route.

### Shared Surfaces
| Frame | Role | Route |
|-------|------|-------|
| Notifications | ANY AUTH | `/notifications` |
| Settings | ANY AUTH | `/settings` |

> One page each, for every account type, with role-specific sections inside — stated
> outright in `design/prompts/16-settings.md`, and the reason Figma files both under
> "11 — Common" rather than under either dashboard. Settings shows a Magazine profile
> section to magazine accounts and a Password section only to accounts that have a
> password (an OAuth account has none).

### Admin `/admin`
| Frame | Role | Route |
|-------|------|-------|
| Admin Panel | ADMIN | `/admin` |
| Reports Queue | ADMIN | `/admin` (section) |
| User Management | ADMIN | `/admin` (section) |
| Grant Eligibility | ADMIN | `/admin` (section) |

> `/admin` is one scrolling page with stacked sections, not a set of sub-routes. The
> moderation surface is small enough that splitting it across three URLs would add
> navigation without adding capability, and an admin working a queue wants the user
> table on the same screen.
>
> **Article Management is not here.** It was specified as `/admin/articles` and never
> built. Article removal is report-driven: an admin removes an article from the row of
> the report that flagged it, backed by `DELETE /admin/articles/:id`. There is no
> browse-all-articles surface and no `GET /admin/articles` endpoint behind one.
>
> This is a deliberate product position rather than an omission — you moderate what
> someone flags, not the whole corpus — and `10-requirements.md` agrees: FR-51 to FR-55
> cover the report queue, dismissal, deletion, user search, plan editing and eligibility
> grants, and none of them asks for a corpus browser. Recorded as future work in the
> report's perspectives section rather than dropped silently.

---

## 7. 🔧 Figma Plugin

A one-time Figma plugin script (`inkwell-sitemap-plugin.js`) auto-generates all 104 empty frames with:
- Role-colored top accent bars
- Frame names following the `[ROLE] Page Name — Breakpoint` convention
- Section labels and route annotations

**To run:** Plugins > Development > New Plugin > paste script into `code.js` > Run.

---

## 8. 🚀 Next Steps

1. Import **shadcn/ui community Figma kit** into the project
2. Remap color variables to Inkwell brand tokens
3. Design shared layout components (Navbar, Footer, Sidebar, Magazine sidebar)
4. Work through sections in order: Auth > Feed > Article > Profiles > Editor > Marketplace > Dashboards > Admin
5. Use Stitch prompts (`stitch-prompts/`) for rapid screen generation, then export to Figma for prototyping
6. Hand off to frontend once a section is complete (Figma to Next.js)
