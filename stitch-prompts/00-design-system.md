# 00 — Design-System Preamble

**Paste this block at the top of _every_ screen prompt** before the screen-specific section.
It locks Stitch into Inkwell's design language so all generated screens stay consistent.

---

```
Design language for an app called "Inkwell" — an AI-powered writing marketplace
connecting independent writers with magazine publishers.

Visual style: modern, clean SaaS — think Linear / Notion / shadcn-ui defaults.
- Typeface: Inter for everything. Tight, confident headings; comfortable body.
- Primary / brand accent: violet #7c3aed (use for CTAs, links, active states, focus rings).
- Neutrals: white page background #ffffff, slate text (#0f172a heading, #475569 body,
  #94a3b8 muted/placeholder), borders #e2e8f0.
- Destructive: red #ef4444. Success: emerald #10b981.
- Surfaces: white cards on a very light slate (#f8fafc) background, subtle 1px borders,
  soft shadows, rounded corners (radius 8–12px). Generous whitespace.
- Components follow shadcn/ui conventions: ghost/outline/solid buttons, badges, avatars,
  dropdown menus, tabs, cards, toasts.
- Tone: premium but approachable, content-first, never cluttered.

Global navigation (top bar, present on all main screens):
- Left: "Inkwell" wordmark (violet).
- Center: a search input with magnifying-glass icon ("Search articles, writers, tags…").
- Right: a "Write" button (violet, pencil icon), a notifications bell with a small dot,
  and a circular user avatar with dropdown.
```
