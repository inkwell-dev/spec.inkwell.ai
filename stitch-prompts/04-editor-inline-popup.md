# 04 — Editor: Inline AI Selection Popup

**Route:** `/editor/[id]` · **Role:** Writer (premium) · **Stitch mode:** Experimental

The core differentiating feature: select text, AI action popup appears.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: The article editor showing the INLINE AI EDITING POPUP — the core feature that
appears when a writer selects text. Route "/editor/[id]".

Same editor canvas as the previous screen (title, formatting toolbar, draft paragraphs)
but WITHOUT the AI chat panel open (full-width editor). Show these two states:

STATE 1 — ACTION SELECTION:
  One sentence in a paragraph is SELECTED (highlighted with a Violet-100 background
  selection color, not the browser default blue).
  Directly above the selection, a compact floating popup card:
    White background, 1px Slate-200 border, rounded-xl, shadow (0 4px 12px rgba(0,0,0,0.08)).
    A horizontal row of AI action buttons, each as a small ghost button with icon + label:
      Phosphor Sparkle icon (Violet-500, 14px) on the far left as a visual anchor.
      Then: "Reformulate" | "Shorten" | "Expand" | "Simplify" | "Improve"
      Each button: text-xs font-medium Slate-600, padding 8px 12px, rounded-lg,
      hover Slate-100 background. Separated by subtle Slate-100 dividers.
    The popup should feel light and precise — not heavy or modal-like.
    Transform-origin should be bottom-center (scaling from the selection toward the popup).

STATE 2 — RESULT PREVIEW (show this to the right of State 1):
  After an action is chosen (e.g., "Reformulate"), the popup expands downward into a
  result card:
    Same white card, 1px Slate-200 border, rounded-xl, wider than the action row.
    Header: "Reformulated" label (text-xs Slate-400 Geist Mono) + Phosphor Sparkle
    icon (Violet-500).
    The AI-rewritten text in a bordered preview box: Slate-50 background, 1px Slate-200
    border, rounded-lg, padding 12px. Text-sm Slate-700, the rewritten version of the
    selected sentence.
    Three buttons below the preview box:
      "Replace" (Violet-600 fill, text-xs, primary).
      "Insert below" (outline, Slate-200 border, text-xs).
      "Cancel" (ghost, text-xs Slate-400).
    Far right: "~80 tokens" cost hint (text-xs Slate-400 Geist Mono).
  
  The transition from State 1 to State 2 should feel like the card smoothly expands
  downward — not a jarring replacement.

Keep the surrounding editor context visible so it is clear the popup is anchored to the
text selection. Token-quota chip still visible in the top bar.

Mobile (375px): the action popup appears as a horizontal scrollable toolbar pinned just
above the on-screen keyboard area (not floating above text — mobile has limited space).
The result preview appears as a bottom sheet (same drag handle as the AI chat panel).
```
