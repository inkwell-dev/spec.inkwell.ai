# Design — Inkwell.ai

All design assets, prompts, and audit documents for the Inkwell.ai platform.

---

## Structure

```
design/
├── README.md                    ← you are here
├── prompts/                     ← Stitch (Gemini) UI generation prompts
│   ├── 00-design-system.md      ← preamble — paste before every screen prompt
│   ├── 01-home-feed.md          ← individual screen prompts (mobile-first)
│   ├── ...
│   ├── 17-notifications.md
│   ├── DESKTOP-PROMPTS.md       ← desktop expansion for screens 01–13
│   ├── desktop-refinement.md    ← desktop for bonus screens + new screens 14–17
│   └── README.md                ← prompt usage guide
├── quality-review.md            ← Figma quality audit + manual checklists
└── figma-inventory.md           ← full screen inventory mapped to Figma node IDs
```

---

## Figma file

**[Web Prototype](https://www.figma.com/design/D5PDq6r8KbkAg34RECWfYQ/Web-Prototype)**

46 screens generated (24 mobile + 22 desktop). Target: 58 screens after remaining prompts.

---

## Screen coverage

| # | Screen | Mobile | Desktop | Prompt |
|---|--------|--------|---------|--------|
| 01 | Home Feed | ✅ | ✅ | `01-home-feed.md` |
| 02 | Article (5 variants) | ✅ | ✅ | `02-article.md` |
| 03 | Editor + AI Chat | ✅ | ✅ | `03-editor-ai-chat.md` |
| 04 | Editor Inline AI | ✅ | ✅ | `04-editor-inline-popup.md` |
| 05 | Writer Analytics | ✅ | ✅ | `05-writer-analytics.md` |
| 06 | Auth (3 screens) | ✅ | ✅ | `06-auth.md` |
| 07 | Subscription Wall | ✅ | ✅ | `07-magazine-subscription.md` |
| 08 | Marketplace Browse | ✅ | ✅ | `08-marketplace-browse.md` |
| 09 | Writer Evaluation | ✅ | ✅ | `09-writer-evaluation.md` |
| 10 | Magazine Library | ✅ | ✅ | `10-magazine-library.md` |
| 11 | Subscription Dashboard | ✅ | ✅ | `11-magazine-subscription-dashboard.md` |
| 12 | Writer Earnings | ✅ | ✅ | `12-writer-earnings.md` |
| 13 | Publish Flow (2 variants) | ✅ | ✅ | `13-publish-flow.md` |
| — | Write Editor | ✅ | ⬜ | `desktop-refinement.md` A |
| — | Writer Dashboard | ✅ | ⬜ | `desktop-refinement.md` B |
| — | Marketplace Feed | ✅ | ⬜ | `desktop-refinement.md` C |
| — | Discovery & Search | ✅ | ⬜ | `desktop-refinement.md` D |
| 14 | Writer Profile | ⬜ | ⬜ | `14-writer-profile.md` + refinement E |
| 15 | Magazine Profile | ⬜ | ⬜ | `15-magazine-profile.md` + refinement F |
| 16 | Settings | ⬜ | ⬜ | `16-settings.md` + refinement G |
| 17 | Notifications | ⬜ | ⬜ | `17-notifications.md` + refinement H |

---

## How to generate remaining screens

1. Open [stitch.withgoogle.com](https://stitch.withgoogle.com)
2. For new mobile screens (14–17): paste `00-design-system.md` + the screen prompt
3. For missing desktops: paste `00-design-system.md` + the relevant prompt from `desktop-refinement.md`
4. Export each batch to Figma
5. Use the reorganization prompt in `quality-review.md` to arrange mobile+desktop pairs

---

## Design system source

- Spec: [`../9-design.md`](../9-design.md)
- Design skills: emil-design-eng, minimalist-ui, stitch-design-taste, high-end-visual-design
- Brand: Violet #7C3AED accent, Geist Sans/Mono, Phosphor icons, #F8FAFC canvas
