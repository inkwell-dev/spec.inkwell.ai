# 18 — Logo (Claude Design prompt)

Copy-paste prompt for generating the Inkwell logo in **Claude Design**.

Built from `1-product-overview.md`, `design/prompts/00-design-system.md` and the live
tokens in the frontend's `src/app/globals.css`. Today the brand is only a text wordmark
(`Inkwell` in Geist Bold, Violet-600, in `src/app/(auth)/layout.tsx`); this prompt asks
for a proper mark that sits beside it.

---

```
Design a logo for "Inkwell", an AI-powered writing marketplace.

--- WHAT THE PRODUCT IS ---
Inkwell is a two-sided platform:
- Independent writers draft articles with an AI assistant: chat, inline editing (rewrite,
  simplify, expand, shorten), and suggestions drawn from their own past articles, so the
  AI writes in their voice.
- Magazines and publishers browse those writers, judge them with engagement analytics
  and AI-generated portfolio insights, then license their articles for their own
  publications.
Its key idea is that the same AI understanding is used twice: once to help the writer
create ("AI writes like me") and once to help the magazine decide ("AI tells me what this
writer is great at"). It turns a writer's craft into something publishers can find, judge
and license.

--- WHAT THE LOGO SHOULD SAY ---
- Craft and authorship first, technology second. This is a tool for serious writers,
  not a gimmicky AI toy.
- The name is a metaphor: the inkwell is where every piece of writing starts. A modern
  take on the inkwell, an ink drop, or a pen nib works, as long as it is not literal or
  clip-art.
- Optional second idea, kept subtle: a link between two sides (writer ↔ publisher), or
  ink that flows out and becomes something larger (a page, a spark, a signal).
- Tone: restrained, content-first, quietly premium, like Linear, Notion or Vercel.
  Editorial-tech, not a marketing site.

--- DELIVERABLES ---
1. Symbol / app icon: a standalone mark that reads clearly at 16×16 (favicon) and
   32×32 (sidebar), and also works at 512×512.
2. Horizontal lockup: symbol + "Inkwell" wordmark.
3. Wordmark only.
4. Variants: full color on light, full color on dark, single-color violet, single-color
   Slate-900, and reversed (white on violet).
Show each one on the real app surfaces: canvas #F8FAFC, white card #FFFFFF, and the dark
background (~#0A0A0A).

--- COLOR PALETTE (use these exact values) ---
Brand accent (the ONLY saturated color):  #7C3AED  Violet-600
Accent hover / deeper shade:              #6D28D9  Violet-700
Accent on dark backgrounds:               #8257F0  (tested for contrast on near-black)
Light accent tint:                        #EDE9FE  Violet-100
Lightest accent tint:                     #F5F3FF  Violet-50
Primary ink / text:                       #0F172A  Slate-900 (never pure #000000)
Body text:                                #334155  Slate-700
Muted:                                    #64748B  Slate-500
Borders:                                  #E2E8F0  Slate-200
Page canvas:                              #F8FAFC  Slate-50
Card surface:                             #FFFFFF
Success (do not use in logo):             #10B981  Emerald-500
Warning (do not use in logo):             #F59E0B  Amber-500

Color rules: at most two colors in the mark, violet plus Slate-900 ink. The main version
must also work as a single flat color. No gradients, no neon or glow, no purple-to-blue
AI gradients.

--- TYPOGRAPHY ---
The app uses Geist Sans for everything (Geist Mono for numbers and metadata). The wordmark
should be Geist Sans Semibold or Bold with slightly tight tracking (about -0.025em), or a
custom geometric sans close to it, so the logo sits naturally beside the UI.
Do NOT use Inter, Roboto, Arial, Open Sans, or generic serifs (Times, Georgia).
"Inkwell" in title case. Small optical tweaks are welcome (for example, a custom dot on the
"i" that echoes an ink drop, or a "w" that hints at a nib) as long as it stays legible.

--- STYLE CONSTRAINTS ---
- Flat vector, geometric, built on a clear grid. Clean strokes, consistent stroke weight
  if lines are used.
- Corner softness that matches the UI: small rounding (the UI uses 8px and 12px radii),
  not bubbly.
- App-icon container, if used: rounded square, violet #7C3AED fill with a white mark, or
  a white/#F8FAFC fill with a violet mark.
- Must hold up as a monochrome stamp and a tiny favicon. No fine detail that disappears
  at small sizes.

--- AVOID ---
Robots, brains, circuit boards, sparkle/✨ "AI" icons, chat bubbles, quill-and-scroll
clichés, 3D, glossy effects, drop shadows, gradient text, emoji, more than two colors,
anything that looks like a stock "pen" icon.

--- OUTPUT ---
Give 3–4 distinct concepts. For each: a one-line rationale tied to the story above, the
deliverables listed, and SVG source for the chosen direction.
```
