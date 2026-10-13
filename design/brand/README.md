# Handoff: Inkwell logo (Nib Drop)

> **Archived 2026-10-13.** This is the design handoff as delivered, kept as the
> brand's source of truth. Two changes from the original: the SVGs had an embedded
> content-provenance `<metadata>` block (about 7.7 KB each) stripped, leaving the
> geometry untouched, and the presentation board moved into `board/`. The prompt
> that produced it is `design/prompts/18-logo.md`. The shipped implementation lives
> in the frontend at `src/components/brand/` and `src/app/` (icon, apple-icon,
> manifest).

## Overview
Brand identity for Inkwell, an AI-powered writing marketplace. The chosen direction, **Nib Drop**, is a single ink drop whose lower point splits into a pen nib (a vertical slit ending in a round breather hole). It stands for the moment writing starts, held by the writer. The mark is one flat shape in one color.

Deliverables: symbol, app icon (violet and light tiles), horizontal lockup, wordmark, and the five color variants.

## About the design files
`board/Inkwell Logo.dc.html` is a **design reference built in HTML**: a presentation board showing the concepts on the app's surfaces. It is not production code. Recreate the logo in the target codebase using its own patterns (React components, Next.js metadata icons, Tailwind, etc.). The production-ready vector sources are in `svg/`, and `reference/InkwellLogo.tsx` is a starting component.

Concept **1a** on the board is the chosen one. Ignore 1b–1d.

## Fidelity
**High fidelity.** Geometry, colors, and type values below are final. Use the exact path data; don't redraw.

## The mark
- Grid: 24 × 24 units. The drop spans x 6.31–17.69, y ≈ 2–21.5. Optical center sits slightly above center by design.
- **Standard cut** (use at ≥ 20 px):
  `M11 20.11L6.31 13.58A7 7 0 1 1 17.69 13.58L13 20.11V13.1A2.1 2.1 0 1 0 11 13.1Z`
  Slit 2 units wide (x 11–13), breather hole r = 2.1 centered at (12, 11.25).
- **Favicon cut** (use at ≤ 16 px): slit widened to 2.8 units (x 10.6–13.4), no hole, so the nib holds on the pixel grid.
  `M10.6 19.55L6.31 13.58A7 7 0 1 1 17.69 13.58L13.4 19.55V11H10.6Z`
- Single compound path, no masks, no strokes. Scales to any size.
- Rule: switch to the favicon cut whenever the rendered mark is ≤ 16 px (`InkwellMark` does this automatically).

## App icon
- 64-unit tile, `rx = 14` (≈ 22% corner radius; matches the UI's 12 px radius at sidebar sizes).
- **Violet tile**: fill #7C3AED, mark #FFFFFF. Default everywhere (favicon, sidebar, PWA, OS icons).
- **Light tile**: fill #F8FAFC, 2-unit #E2E8F0 inner border, mark #7C3AED. Use where a violet block is too heavy.
- Mark fill ratio of tile (optical sizing, already applied in `svg/app-icon-*`):
  - 16 px: 72% (favicon cut)
  - 32 px: 66%
  - ≥ 64 px / 512 px: 60%

## Lockup
- Mark + "Inkwell", vertically centered.
- Mark height = 1.2 × wordmark font-size. Gap = 0.32 × font-size.
- Sidebar: 32 px app icon + 17 px wordmark, 10 px gap (as shown on the board).
- Clear space: at least 0.5 × mark height on all sides. Minimum lockup height: 16 px.

## Wordmark
- Geist Sans, weight 600 (Semibold), letter-spacing −0.025em, title case "Inkwell".
- In the app, render as live text in Geist (already loaded). The `svg/lockup-*` and `svg/wordmark-*` files use a `<text>` element: **convert text to outlines** (Figma/Illustrator) before using them outside the app (email, press kit, social), where Geist isn't guaranteed. Widths in those viewBoxes are approximate until outlined.

## Color variants
| Variant | Mark | Wordmark | Background |
|---|---|---|---|
| Full color on light | #7C3AED | #0F172A | #F8FAFC or #FFFFFF |
| Full color on dark | #8257F0 | #F8FAFC | #0A0A0A |
| Single color violet | #7C3AED | #7C3AED | light |
| Single color Slate-900 | #0F172A | #0F172A | light |
| Reversed | #FFFFFF | #FFFFFF | #7C3AED |

Hover (if the logo is a link): mark #6D28D9 on light. No gradients, glows, shadows or opacity tricks.

## Implementation checklist
1. Add `svg/favicon.svg` as the SVG favicon; export 16/32/48 PNG + ICO and 180 px apple-touch-icon (from `app-icon-violet-512.svg`) for fallbacks.
2. Use `app-icon-violet-512.svg` for PWA manifest icons (192, 512). For maskable icons, use the symbol on a full-bleed #7C3AED square with 60% fill.
3. Sidebar header: `<InkwellAppIcon size={32} />` + `<InkwellWordmark size={17} />`; switch wordmark color with the theme (#0F172A light / #F8FAFC dark).
4. Marketing / auth pages: `<InkwellLogo size={24} theme=... />`.
5. Accessible name "Inkwell" on the logo link; the mark alone is `aria-hidden`.

## Design tokens
- Violet-600 #7C3AED (mark), Violet-700 #6D28D9 (hover), on-dark #8257F0
- Slate-900 #0F172A (ink), Slate-50 #F8FAFC (canvas / ink on dark), Slate-200 #E2E8F0 (light tile border)
- Card #FFFFFF, dark surface #0A0A0A
- Type: Geist Sans 600, −0.025em

## Files
- `svg/symbol-*.svg`: mark alone (violet, on-dark, Slate-900, white, favicon cut)
- `svg/app-icon-{violet,light}-{16,32,512}.svg`, `svg/favicon.svg`
- `svg/lockup-*.svg`: color-light, color-dark, violet, slate-900, reversed-on-violet
- `svg/wordmark-*.svg`
- `reference/InkwellLogo.tsx`: React reference components
- `board/Inkwell Logo.dc.html` (+ `board/support.js`): the presentation board; open in a browser
