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

### Auth
| Frame | Role | Route |
|-------|------|-------|
| Login | GUEST | `/login` |
| Sign Up — Personal | GUEST | `/signup` |
| Sign Up — Magazine | GUEST | `/signup/magazine` |

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
| Tag Browse | ANY AUTH | `/tag/[tag]` |

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
| Subscription Wall | MAGAZINE UNSUB | `/m/subscribe` | Mandatory before marketplace access |
| Marketplace Browse | MAGAZINE | `/marketplace` | Writer discovery, filterable grid |

### Writer Dashboard `/dashboard`
| Frame | Role | Route |
|-------|------|-------|
| My Articles | WRITER | `/dashboard/articles` |
| Analytics + Eligibility | WRITER | `/dashboard/analytics` |
| Earnings | WRITER | `/dashboard/earnings` |
| Notifications | ANY AUTH | `/dashboard/notifications` |
| Settings | ANY AUTH | `/dashboard/settings` |

### Magazine Dashboard `/m/dashboard`
| Frame | Role | Route |
|-------|------|-------|
| Library | MAGAZINE | `/m/dashboard/library` |
| Subscription & Credits | MAGAZINE | `/m/dashboard/subscription` |
| Credit Top-Up Modal | MAGAZINE | `/m/dashboard/subscription` (modal overlay) |
| Notifications | MAGAZINE | `/m/dashboard/notifications` |
| Settings | MAGAZINE | `/m/dashboard/settings` |

### Admin `/admin`
| Frame | Role | Route |
|-------|------|-------|
| Admin Panel | ADMIN | `/admin` |
| Reports Queue | ADMIN | `/admin/reports` |
| User Management | ADMIN | `/admin/users` |
| Article Management | ADMIN | `/admin/articles` |

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
