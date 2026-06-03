# 03 — Article Editor + AI Chat Panel

**Route:** `/editor/[id]` · **Role:** Writer (premium) · **Stitch mode:** Experimental

The core writing experience: a TipTap-style rich-text editor plus the AI chat side panel.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: The article editor with the AI chat assistant open, route "/editor/[id]".
This is the core writing experience — a rich-text editor (TipTap-style) plus an AI side panel.

Layout (desktop, full-width app — no marketing nav, a slim editor top bar instead):
- Editor top bar: back chevron + "Draft" label with a small "Saved" auto-save indicator
  (cloud check + "Saved just now"); on the right a token-quota chip ("1,240 tokens left"
  with a small lightning icon), a "Preview" ghost button, and a violet "Publish" button.
- Main area split into two columns:
  LEFT (~60%) — the writing canvas on white:
    - A large borderless Title input ("Untitled article…").
    - A thumbnail/cover upload strip ("Add a cover image").
    - The rich-text body with a floating formatting toolbar (bold, italic, H1/H2, bullet list,
      quote, code, link, image) shown above the content. A few paragraphs of draft text.
    - A small circular violet AI button floating bottom-left ("Ask AI") and a microphone
      button next to it (voice input).
  RIGHT (~40%) — the AI Chat panel (bordered, white):
    - Header: "AI Assistant" with a sparkle icon and a close X.
    - A scrollable conversation: a user message bubble ("Help me write an intro about remote
      work") and an AI response bubble with generated text, followed by action buttons under
      the AI message: "Insert into article", "Replace selection", "Copy", "Regenerate".
    - Quick-action suggestion chips ("Improve this", "Make it shorter", "Continue writing").
    - Bottom: a chat input with a send button and a small "Uses ~200 tokens" hint.

Mobile (375px): editor canvas full screen; the AI chat panel becomes a bottom sheet that
slides up over the content, with the same conversation + input.
```
