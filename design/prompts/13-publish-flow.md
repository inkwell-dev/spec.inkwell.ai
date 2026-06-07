# 13 — Article Publish Flow (Writer) [GENERATED]

**Route:** `/editor/[id]` (publish modal) · **Role:** Writer · **Stitch mode:** Standard

The publish modal where writers choose placement (public vs marketplace) and set pricing.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Article Publish modal, triggered from the editor's "Publish" button.
This is a centered modal overlay on top of the editor (editor dimmed behind).

Modal: max-width 520px, white fill, rounded-xl, shadow (0 8px 32px rgba(0,0,0,0.12)),
1px Slate-200 border. Backdrop: rgba(0,0,0,0.3).

Generate TWO variants:

VARIANT 1 — ELIGIBLE WRITER (marketplace-eligible):

  Modal header (padding 24px, 1px Slate-200 bottom border):
    "Publish your article" (text-xl font-semibold Slate-900).
    Close button: Phosphor X (Slate-400, hover Slate-600) top-right.

  Article preview (padding 20px horizontal):
    A compact preview card (Slate-50 bg, rounded-lg, padding 12px):
    Title: "The Quiet Art of Editing Your Own Voice" (text-sm font-medium Slate-900).
    Excerpt: first line of the article (text-xs Slate-500, 1 line truncated).
    Thumbnail placeholder (40x28px, rounded, Slate-200 bg) left-aligned.

  PLACEMENT SELECTION (24px below preview, padding 20px horizontal):
    "Where should this article appear?" (text-sm font-medium Slate-700).
    12px gap.
    Two radio cards side by side (equal width, 12px gap between):

    CARD A — "Public" (default selected):
      When selected: Violet-600 2px border, Violet-50 bg tint.
      When unselected: Slate-200 1px border, white bg.
      Card: rounded-xl, padding 16px.
      Phosphor Globe icon (20px, Violet-600 when selected, Slate-400 when not).
      "Public" (text-sm font-semibold Slate-900).
      "Visible in the public feed to all readers." (text-xs Slate-500).
      
      Sub-option (slides in below when Public is selected, 12px top margin):
        "Access level" label (text-xs Slate-400).
        Two small radio options (text-sm):
          "Free access" (radio selected, Slate-700) — "Any authenticated reader."
          "Premium access" (radio, Slate-700) — "Premium-plan readers only."
          Premium has a small Violet-100 badge: "Requires eligibility" text-xs.

    CARD B — "Marketplace":
      When selected: Violet-600 2px border, Violet-50 bg tint.
      When unselected: Slate-200 1px border, white bg.
      Phosphor Storefront icon (20px).
      "Marketplace" (text-sm font-semibold Slate-900).
      "Exclusive to magazine subscribers. Hidden from public feed." (text-xs Slate-500).
      
      Sub-options (slide in when Marketplace is selected):
        "Set your price" label (text-xs Slate-400) + number input (Geist Mono, Slate-200
        border, rounded-lg, 80px width). "credits" suffix text (text-xs Slate-400).
        Below input: "Preview price: 12 credits (10%)" (text-xs Slate-400 Geist Mono,
        auto-calculated, read-only — updates as the writer types a price).
        Info note: Phosphor Info icon + "Magazines pay 10% to preview, then 90% to purchase."
        (text-xs Slate-400).

  TAGS INPUT (20px below placement):
    "Tags" label (text-sm font-medium Slate-700).
    Multi-select tag input: pills inside the input (Violet-100 bg, Violet-700 text,
    text-xs, rounded-full, with X to remove). Placeholder: "Add topics..."
    Suggestion dropdown: 3-4 suggested tags below (text-sm Slate-600).

  EXCERPT (16px below tags):
    "Excerpt" label (text-sm font-medium Slate-700) + "(auto-generated, editable)"
    (text-xs Slate-400).
    Textarea: 2 rows, Slate-200 border, rounded-lg, pre-filled with article excerpt.

  FOOTER (24px top margin, padding 20px, 1px Slate-200 top border):
    "Publish" primary button (Violet-600, right-aligned).
    "Save as draft" ghost button (text-sm Slate-400, left of Publish).

VARIANT 2 — NOT YET ELIGIBLE WRITER:
  Same modal, but:
  
  The "Marketplace" card is visually disabled:
    Slate-100 bg (not white), Slate-300 border, opacity-60.
    Phosphor Lock icon (Slate-400) overlaid top-right corner of the card.
    Inside the disabled card, replacing the sub-options:
      Two mini progress bars (inline, compact):
        "3,247 / 5,000 readers" (text-xs Slate-400 Geist Mono) + thin progress bar.
        "783 / 1,000 reactions" (text-xs Slate-400 Geist Mono) + thin progress bar.
      "Keep publishing to unlock." (text-xs Slate-400).
  
  The "Premium access" radio under Public is also greyed out:
    Disabled state, Slate-300 text, with the same eligibility note as a small inline hint.
  
  Only "Public > Free access" is available and selected.

Mobile (375px): modal becomes a full-screen bottom sheet (slides up from bottom with
drag handle). Placement cards stack vertically. Tags and excerpt full-width.
Footer buttons stack vertically (Publish above Save as draft).
```
