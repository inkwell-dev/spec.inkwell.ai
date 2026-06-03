# 04 — Editor: Inline AI Selection Popup

**Route:** `/editor/[id]` · **Role:** Writer (premium) · **Stitch mode:** Experimental

The core differentiating feature: select text → AI action popup (reformulate / shorten /
expand / simplify / improve engagement).

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: The article editor showing the INLINE AI EDITING POPUP — the core feature that
appears when a writer selects text. Route "/editor/[id]".

Same editor canvas as the previous screen (title, formatting toolbar, draft paragraphs) BUT:
- One sentence in a paragraph is shown SELECTED (highlighted in a light violet selection color).
- Directly above the selection, a compact floating popup card (shadcn-style, rounded, shadow):
  a horizontal row of AI action buttons, each with a small icon + label:
  "Reformulate", "Shorten", "Expand", "Simplify", "Improve engagement".
  A subtle divider, then a sparkle icon on the left of the row to signal these are AI actions.
- Show a SECOND state to the side: after an action is chosen, the popup expands into a
  result card showing the AI-rewritten version of the selected text in a bordered preview box,
  with three buttons below: "Replace" (violet), "Insert below" (outline), "Cancel" (ghost),
  and a tiny "~80 tokens" cost hint.

Keep the surrounding editor context visible so it's clear the popup is anchored to the text
selection. Token-quota chip still visible in the top bar.

Mobile (375px): the action popup appears as a horizontal scrollable toolbar pinned just above
the on-screen keyboard area; the result preview appears as a bottom sheet.
```
