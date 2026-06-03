# 13 — Article Publish Flow (Writer)

**Route:** `/editor/[id]` (publish modal) · **Role:** Writer · **Stitch mode:** Standard

The publish modal where writers choose placement (public vs marketplace) and set pricing.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Article Publish modal, triggered from the editor's "Publish" button.
This is a full-screen overlay or large centered modal on top of the editor.

Generate TWO variants:

VARIANT 1 — ELIGIBLE WRITER (marketplace-eligible):
Modal with a clean white background, max ~600px wide, centered:
- Heading: "Publish your article".
- A thumbnail preview of the article (title + excerpt + cover image) at the top.

- STEP 1 — Placement selection:
  Two large radio cards side by side:
  CARD A — "Public" (default selected, violet border):
    - Icon: globe.
    - "Visible in the public feed to all readers."
    - Sub-option (appears when Public is selected): visibility toggle —
      "Free access" (radio, default) or "Premium access" (radio).
      Premium has a small note: "Only premium-plan readers can read the full article."
  CARD B — "Marketplace":
    - Icon: shopping bag.
    - "Exclusive to magazine subscribers. Not visible in the public feed."
    - Sub-options (appear when Marketplace is selected):
      - Price input: "Set your price" with a number input in credits (min enforced).
      - Preview price shown automatically below: "Preview price: 12 credits (10%)" — read-only,
        auto-calculated.
      - A muted note: "Magazines pay 10% to preview, then the remaining 90% to purchase."

- Tags input: a multi-select tag input with suggested tags.
- Excerpt textarea: auto-generated, editable.
- A violet "Publish" button (full width) and a "Save as draft" ghost button.

VARIANT 2 — NOT YET ELIGIBLE WRITER:
Same modal, but:
- The "Marketplace" card is greyed out / disabled with a small lock icon.
- Inside the disabled card: "Unlock marketplace: 3,200 / 5,000 readers · 780 / 1,000 reactions"
  with a small progress bar.
- The "Premium access" sub-option under Public is also greyed out with the same eligibility note.
- Only "Public → Free access" is available.

Mobile (375px): modal becomes full-screen. Placement cards stack vertically.
Sub-options slide in below the selected card.
```
