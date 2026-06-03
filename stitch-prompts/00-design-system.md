# 00 — Design System Preamble

**Paste this block at the top of _every_ screen prompt** before the screen-specific section.
It locks Stitch into Inkwell's design language so all generated screens stay consistent.

---

```
Design system for "Inkwell" — an AI-powered writing and magazine marketplace platform.

--- VISUAL ATMOSPHERE ---
The atmosphere is restrained, content-first, and quietly premium — like a well-lit
architecture studio crossed with a modern editorial tool. Think Linear, Notion, Raydiant —
not a marketing site. Density is balanced (not sparse, not cockpit-dense). Layouts use
confident asymmetric whitespace. Motion is fluid but invisible — present when purposeful,
absent when decorative.

--- COLOR PALETTE ---
Every color has a single functional role. Color is scarce — used for meaning, not decoration.

Canvas background:        #F8FAFC  (cool off-white, never pure white for page backgrounds)
Card / surface fill:      #FFFFFF  (pure white for elevated cards only)
Primary text:             #0F172A  (Slate-900, never pure #000000 — used for headings)
Body text:                #334155  (Slate-700, comfortable reading weight)
Muted / secondary text:   #64748B  (Slate-500, metadata, timestamps, placeholders)
Structural borders:       #E2E8F0  (Slate-200, 1px lines only — never thicker)
Hover surface:            #F1F5F9  (Slate-100, subtle row/card hover tint)

Brand accent (singular):  #7C3AED  (Violet-600 — CTAs, links, active states, focus rings.
                           This is the ONLY saturated accent. Saturation < 80%.)
Accent hover:             #6D28D9  (Violet-700, button hover)
Accent muted background:  #EDE9FE  (Violet-100, selected tag chips, light accent surfaces)

Semantic status colors (used sparingly, only for state indication):
  Success / eligible:     #10B981  (Emerald-500, badges only — never large fills)
  Warning / pending:      #F59E0B  (Amber-500, preview-stage badges)
  Destructive / error:    #EF4444  (Red-500, inline errors, destructive actions)

BANNED: purple neon glows, gradient text on large headers, oversaturated accent fills
on large areas, colored section backgrounds (no violet hero, no blue footer), pure black
#000000 anywhere.

--- TYPOGRAPHY ---
Primary typeface:  Geist Sans — clean geometric sans-serif with character. Used for
                   everything: headings, body, UI labels, buttons.
Monospace:         Geist Mono — for metadata, credit amounts, timestamps, token counts.

Heading hierarchy (weight-and-color driven, not just size):
  Page title:     text-3xl (30px), font-semibold, Slate-900, letter-spacing -0.025em
  Section heading: text-xl (20px), font-medium, Slate-900
  Card title:     text-lg (18px), font-medium, Slate-900
  Body:           text-base (16px), font-normal, Slate-700, line-height 1.6, max-width 65ch
  Small / meta:   text-sm (14px), font-normal, Slate-500
  Caption:        text-xs (12px), font-medium, uppercase, letter-spacing 0.05em, Slate-400

BANNED: Inter (too generic), Roboto, Arial, Open Sans, any generic serif (Times, Georgia).
No text larger than 36px in the app UI (this is a tool, not a landing page). No emoji
anywhere — use Phosphor icons (regular weight) or clean SVG primitives instead.

--- COMPONENT STYLING ---
Buttons:
  Primary: Violet-600 fill, white text, rounded-lg (8px), no shadow, no outer glow.
    Hover: Violet-700. Active: scale(0.97) press feedback + slight darken.
  Secondary: transparent background, Slate-200 border, Slate-700 text. Hover: Slate-50 fill.
  Ghost: no border, no background. Slate-500 text. Hover: Slate-100 fill.
  Destructive: Red-500 fill, white text. Used only for irreversible actions.

Cards:
  White fill on the #F8FAFC canvas. 1px Slate-200 border. Rounded-xl (12px).
  Ultra-diffuse shadow: 0 1px 3px rgba(0,0,0,0.04). Generous internal padding (20-24px).
  Hover: border shifts to Slate-300, shadow deepens to 0 2px 8px rgba(0,0,0,0.06).
  NO heavy drop shadows. NO gradient fills. NO colored card backgrounds.

Inputs:
  Label above (text-sm, font-medium, Slate-700). Input: white fill, 1px Slate-200 border,
  rounded-lg (8px). Focus: 2px Violet-600 ring. Error: Red-500 border + inline error text
  below. No floating labels.

Badges / Status pills:
  Small, rounded-full, text-xs, font-medium, uppercase tracking-wide.
  Use muted pastel backgrounds matching status:
    Violet-100 + Violet-700 text (default accent)
    Emerald-50 + Emerald-700 text (success / eligible / purchased)
    Amber-50 + Amber-700 text (warning / previewed / pending)
    Slate-100 + Slate-600 text (neutral / inactive)

Progress bars:
  Rounded-full track (Slate-100), Violet-600 fill, 8px height. Clean and flat.
  Label above or beside (never inside the bar).

Tables:
  No outer border. Header row: text-xs uppercase tracking-wide Slate-500, bottom Slate-200
  border. Data rows: text-sm Slate-700, separated by 1px Slate-100 borders. Row hover:
  Slate-50 fill. Numbers in Geist Mono with tabular-nums.

Loading states:
  Skeleton loaders matching exact layout dimensions — shimmer with Slate-100 to Slate-200
  gradient animation. No circular spinners. No bouncing dots.

Empty states:
  Centered icon (Slate-300, 48px) + heading + description + single CTA button.
  Never just "No data" text.

--- GLOBAL NAVIGATION (top bar, present on all main screens) ---
White background, 1px Slate-200 bottom border, sticky top.
Left: "Inkwell" wordmark in Violet-600, font-semibold.
Center: search input with magnifying-glass icon, Slate-200 border, rounded-lg,
  placeholder "Search articles, writers, tags..." in Slate-400.
Right: "Write" button (Violet-600 fill, small, pencil icon), notification bell with
  small red dot badge (only when unread), circular user avatar (32px) with dropdown.
No background color on the navbar — just white + bottom border.

--- SIDEBAR NAVIGATION (dashboard screens) ---
Left sidebar, 240px wide, white background, 1px Slate-200 right border.
Nav items: text-sm, Slate-600, horizontal padding 12px, vertical padding 8px, rounded-lg.
Active item: Violet-50 background, Violet-700 text, font-medium.
Hover: Slate-50 background.
Section labels: text-xs uppercase tracking-wide Slate-400, top margin.
Sidebar collapses to bottom tab bar on mobile (375px).

--- LAYOUT PRINCIPLES ---
Max content width: 1280px centered with auto margins.
Reading column (articles, editor): max-width 680px centered.
Dashboard grid: sidebar (240px) + main content area.
Feed card grid: single centered column (max 720px) with optional side rails on desktop.
Card grids: CSS Grid, never equal 3-column rows — use asymmetric spans or 2-column layouts.
Generous vertical spacing between sections: 32-48px gaps.
All multi-column layouts collapse to single column below 768px.
Horizontal overflow on mobile is a critical failure — never allow it.

--- MOTION PHILOSOPHY ---
Motion is invisible and purposeful. It exists to prevent jarring state changes, provide
feedback, and maintain spatial consistency — never for decoration.

Easing: always ease-out (cubic-bezier(0.23, 1, 0.32, 1)) for entering elements.
  Never ease-in for UI — it feels sluggish. Never linear except for progress bars.
Duration: UI animations under 250ms. Modals/drawers 200-350ms. Button press: 120ms.
Button active state: scale(0.97) on press — every clickable element must feel responsive.
List entry: stagger delay 40-60ms between items, translateY(8px) + opacity fade.
Page transitions: crossfade opacity only, 150ms.
Skeleton loaders: gentle shimmer animation, 1.5s duration, infinite.
Toasts: slide in from top-right with ease-out, auto-dismiss after 4s.
Reduced motion: respect prefers-reduced-motion — keep opacity transitions, remove movement.

BANNED: bounce animations, spring physics on standard UI (save for drag interactions only),
animations longer than 500ms in the app UI, custom mouse cursors, parallax scrolling,
scroll-jacking, "scroll to explore" text, bouncing chevrons, neon glow hover effects.

--- ANTI-PATTERNS (AI TELLS TO AVOID) ---
These make generated UI look cheap and templated. Avoid all of them:
- No emojis anywhere in the UI
- No generic placeholder names ("John Doe", "Acme Corp", "Lorem Ipsum")
- No fake round numbers (99.99%, 50%, 10,000) — use believable specifics (63.2%, 12,847)
- No AI copywriting clichés ("Elevate", "Seamless", "Unleash", "Next-Gen", "Supercharge")
- No 3-column equal card layouts — use 2-column or asymmetric grids
- No centered hero sections with massive text (this is a tool, not a landing page)
- No gradient backgrounds on any section
- No glassmorphism / frosted glass effects (except subtle navbar blur if needed)
- No decorative blob shapes or abstract SVG backgrounds
- No broken Unsplash links — use solid color placeholders or SVG avatar initials
- No overlapping elements — every element occupies its own clean spatial zone
- Use realistic article titles about writing, publishing, journalism, content strategy
- Use realistic writer names (diverse, international) — not "Jane Smith" or "John Writer"
- Use realistic magazine names ("The Atlantic Review", "Meridian Digital", "Prose & Pixel")
```
