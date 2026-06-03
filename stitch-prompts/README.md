# 🎨 Stitch Prototype Prompts — Inkwell

Copy-paste prompts for generating the Inkwell UI prototype in
**[Google Stitch](https://stitch.withgoogle.com)** (Gemini-powered UI design tool).

Stitch generates **one screen per prompt**, so the prompts are split into a shared
**design-system preamble** plus **one file per screen**. Paste the preamble at the top of
every screen prompt to keep the design language consistent.

---

## ⚙️ Configuration applied

| Setting | Value |
|---------|-------|
| Visual direction | Modern SaaS clean (Linear / Notion / shadcn defaults) |
| Primary / brand color | Violet `#7c3aed` |
| Typeface | Inter |
| Form factors | Desktop (1440px) + Mobile (375px) |
| Scope | Full platform — writer, reader, magazine, and marketplace flows |

---

## 📂 Files

| File | Screen | Suggested Stitch mode |
|------|--------|-----------------------|
| [`00-design-system.md`](./00-design-system.md) | Shared preamble — paste at top of every prompt | — |
| [`01-home-feed.md`](./01-home-feed.md) | Home Feed (`/`) | Standard |
| [`02-article.md`](./02-article.md) | Article read view + premium-lock + marketplace variants (`/articles/[slug]`) | Standard |
| [`03-editor-ai-chat.md`](./03-editor-ai-chat.md) | Editor + AI Chat panel (`/editor/[id]`) | Experimental |
| [`04-editor-inline-popup.md`](./04-editor-inline-popup.md) | Editor + inline AI selection popup (`/editor/[id]`) | Experimental |
| [`05-writer-analytics.md`](./05-writer-analytics.md) | Writer Analytics dashboard + eligibility progress (`/dashboard/analytics`) | Standard |
| [`06-auth.md`](./06-auth.md) | Login, Personal Sign Up, Magazine Sign Up (`/login`, `/signup`, `/signup/magazine`) | Standard |
| [`07-magazine-subscription.md`](./07-magazine-subscription.md) | Magazine Subscription Wall — mandatory before marketplace access (`/m/subscribe`) | Standard |
| [`08-marketplace-browse.md`](./08-marketplace-browse.md) | Marketplace writer discovery for magazines (`/marketplace`) | Standard |
| [`09-writer-evaluation.md`](./09-writer-evaluation.md) | Writer Profile in evaluation mode — analytics + Portfolio Insights + articles (`/u/[username]?as=magazine`) | Standard |
| [`10-magazine-library.md`](./10-magazine-library.md) | Magazine's curated library of purchased articles (`/m/dashboard/library`) | Standard |
| [`11-magazine-subscription-dashboard.md`](./11-magazine-subscription-dashboard.md) | Subscription management + credit balance + transactions (`/m/dashboard/subscription`) | Standard |
| [`12-writer-earnings.md`](./12-writer-earnings.md) | Writer Earnings dashboard — payouts + eligibility progress (`/dashboard/earnings`) | Standard |
| [`13-publish-flow.md`](./13-publish-flow.md) | Article Publish modal — placement choice + pricing (`/editor/[id]` overlay) | Standard |

---

## 🚀 How to run these in Stitch

1. Go to **stitch.withgoogle.com** → create a new project.
2. For each screen: paste the **`00-design-system.md` preamble + that screen's prompt** as a
   single message, then generate.
3. **Both form factors:** each prompt already describes its mobile variant, but Stitch renders
   one viewport at a time. Generate the **desktop** version first, then send a short follow-up:
   *"Now generate the mobile (375px) version of this same screen, following the mobile notes."*
   Stitch keeps the design language consistent within a project.
4. Use **Experimental mode** for the editor screens (03 & 04) — they're the most layout-dense.
   **Standard mode** is fine for all other screens.
5. Iterate with small deltas (*"make the AI panel narrower"*, *"add a premium badge"*) rather
   than re-describing the whole screen.

---

## ⚠️ Notes & limitations

- **Stitch produces static high-fidelity screens** (+ exportable HTML/CSS and a Figma export),
  not clickable multi-screen prototypes. For clickable flow-linking, export to Figma and wire
  the prototype there — this matches the Figma-primary plan in [`../9-design.md`](../9-design.md).
- Not yet generated (ask to add):
  - **Admin** — moderation queue, user/article management.
  - **Magazine Profile** (public page showing purchased articles).

---

## 🔗 Source spec

These prompts are derived from:
- [`../1-product-overview.md`](../1-product-overview.md) — vision, account model, subscription + credits
- [`../2-features.md`](../2-features.md) — editor, AI features, marketplace, eligibility gate
- [`../3-user-flows.md`](../3-user-flows.md) — user journeys, 3-stage purchase flow
- [`../9-design.md`](../9-design.md) — design system, page inventory, breakpoints
