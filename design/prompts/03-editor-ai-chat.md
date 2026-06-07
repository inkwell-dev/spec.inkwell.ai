# 03 — Article Editor + AI Chat Panel [GENERATED]

**Route:** `/editor/[id]` · **Role:** Writer (premium) · **Stitch mode:** Experimental

The core writing experience: a TipTap-style rich-text editor plus the AI chat side panel.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: The article editor with the AI chat assistant open, route "/editor/[id]".
This is the core writing experience — a rich-text editor plus an AI side panel.

Layout (desktop, full-width app — no marketing nav, a slim editor top bar instead):

EDITOR TOP BAR (white background, 1px Slate-200 bottom border, 48px height):
  Left: back chevron (Phosphor CaretLeft, Slate-400) + "Draft" label (text-sm Slate-500)
    + small auto-save indicator: Phosphor Cloud check icon (Emerald-500) + "Saved just now"
    (text-xs Slate-400 Geist Mono). The save indicator appears quietly — no toast.
  Right: token-quota chip (Slate-100 background, rounded-full, text-xs Geist Mono —
    Phosphor Lightning icon Violet-500 + "1,240 tokens left" Slate-600), 12px gap,
    "Preview" ghost button (text-sm Slate-600, no border, hover Slate-100), 8px gap,
    "Publish" primary button (Violet-600 fill, text-sm, rounded-lg).

MAIN AREA split into two columns:

LEFT (~60%) — the writing canvas:
  White background, generous padding (48px horizontal, 32px top).
  - Title input: borderless, text-3xl (30px) font-bold Slate-900, placeholder
    "Untitled article..." in Slate-300. No border, no background — just text.
  - Cover image upload strip below title (16px gap): dashed Slate-200 border area,
    rounded-lg, 64px height, centered text "Add a cover image" (text-sm Slate-400) +
    Phosphor Image icon. Hover: Slate-100 fill, border Slate-300.
  - Rich text body (24px below cover strip): a few paragraphs of realistic draft text
    about content strategy. Text-base, Slate-700, line-height 1.75.
  - Floating formatting toolbar above content (only visible when text is selected — but
    show it in the mockup for context): white card, 1px Slate-200 border, rounded-lg,
    subtle shadow. Horizontal row of icons: Bold, Italic, H1, H2, bullet list, quote,
    code, link, image. Each 32px tap target, Slate-500, hover Slate-900.
  - Bottom-left corner: a small circular Violet-600 button with Phosphor Sparkle icon
    (the "Ask AI" shortcut, 40px, subtle shadow) and a microphone button next to it
    (Slate-200 border, Slate-500 icon, 40px).

RIGHT (~40%) — the AI Chat panel:
  White background, 1px Slate-200 left border. Full height of viewport.
  
  Header: "AI Assistant" (text-sm font-medium Slate-900) with Phosphor Sparkle icon
    (Violet-500) on the left, and a close X button (Phosphor X, Slate-400, hover Slate-600)
    on the right. 1px Slate-200 bottom border. 48px height to match top bar.
  
  Scrollable conversation area (padding 16px):
    User message: right-aligned bubble, Slate-100 background, rounded-xl (bottom-right
    corner less rounded), text-sm Slate-700. Content: "Help me write an introduction
    about the evolving role of editors in AI-assisted publishing".
    
    AI response: left-aligned, no bubble background (just text on white). Phosphor Sparkle
    icon (Violet-500, 16px) next to "Inkwell AI" label (text-xs Slate-400 Geist Mono).
    Response text: text-sm Slate-700, a well-written 3-sentence introduction.
    Below the response, action buttons in a horizontal row: "Insert into article"
    (text-xs Violet-600 ghost button, Phosphor ArrowSquareOut icon),
    "Replace selection" (text-xs Slate-500 ghost), "Copy" (text-xs Slate-500 ghost),
    "Regenerate" (text-xs Slate-500 ghost, Phosphor ArrowClockwise icon).
  
  Quick-action chips below conversation: horizontal scrollable row of small chips —
    "Improve this paragraph", "Make it shorter", "Continue writing", "Suggest a title".
    Each chip: text-xs, Slate-200 border, rounded-full, Slate-600 text, hover Slate-100.
  
  Bottom input area (sticky, 1px Slate-200 top border, padding 12px):
    Text input with Phosphor PaperPlaneRight send button (Violet-600).
    Below input: "Uses ~200 tokens" hint (text-xs Slate-400 Geist Mono).

Mobile (375px): editor canvas full screen. The AI chat panel becomes a bottom sheet
that slides up covering 70% of the screen, with a small drag handle (Slate-300, 40px wide,
4px height, rounded-full, centered) at the top. Same conversation + input layout.
```
