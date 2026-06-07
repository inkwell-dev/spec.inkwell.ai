# 06 — Auth Screens [GENERATED]

**Routes:** `/login`, `/signup`, `/signup/magazine` · **Role:** Guest · **Stitch mode:** Standard

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen set: Authentication screens for Inkwell. Generate THREE variants.

VARIANT 1 — LOGIN ("/login"):
Full-page layout on #F8FAFC canvas. Centered card, max-width 400px.
  White card, 1px Slate-200 border, rounded-xl, padding 32px, ultra-diffuse shadow
  (0 1px 3px rgba(0,0,0,0.04)).
  - "Inkwell" wordmark at top center (Violet-600, text-xl font-bold, letter-spacing -0.02em).
  - 24px gap.
  - "Welcome back" (text-2xl font-semibold Slate-900, letter-spacing -0.02em).
  - "Sign in to your account" (text-sm Slate-500, 4px below heading).
  - 24px gap.
  - Email input: label "Email" (text-sm font-medium Slate-700), input with Slate-200 border,
    rounded-lg, placeholder "you@example.com" in Slate-400.
  - 16px gap.
  - Password input: label "Password", input with show/hide toggle (Phosphor Eye / EyeSlash
    icon, Slate-400). "Forgot password?" text link (text-xs Violet-600) right-aligned below.
  - 24px gap.
  - "Sign in" button: Violet-600 fill, white text, full width, rounded-lg, font-medium.
  - 16px gap.
  - Divider: horizontal line (Slate-200) with "or" text (text-xs Slate-400 on white background
    chip centered over the line).
  - 16px gap.
  - "Continue with Google" button: white fill, 1px Slate-200 border, full width, rounded-lg.
    Google "G" icon on the left (use the standard 4-color Google icon), "Continue with Google"
    text (text-sm font-medium Slate-700).
  - 24px gap.
  - "Don't have an account? Sign up" (text-sm Slate-500, "Sign up" in Violet-600).
  
  No decorative elements. No illustrations. No gradient. Just a clean, confident form.

VARIANT 2 — PERSONAL SIGN UP ("/signup"):
Same centered card layout, max-width 420px:
  - "Inkwell" wordmark (same as login).
  - "Create your account" (text-2xl font-semibold Slate-900).
  - "Start reading, start writing." (text-sm Slate-500).
  - Form fields (16px gaps between each):
    Name input ("Full name").
    Email input ("Email").
    Username input — with a real-time preview hint below: "/u/username" (text-xs Slate-400
    Geist Mono). Input has a "@" prefix indicator (Slate-400) or just a clean input.
    Password input (with show/hide toggle).
  - A toggle row: Phosphor PencilSimple icon + "I want to write" label (text-sm Slate-700)
    + a small switch toggle (Violet-600 when on, Slate-200 when off). Below the toggle
    when on: "You can always start writing later from settings." (text-xs Slate-400).
  - 24px gap.
  - "Create account" primary button (full width, Violet-600).
  - Divider + "Continue with Google" button (same as login).
  - "Already have an account? Sign in" link.
  - Bottom: "Are you a magazine? Sign up here" (text-xs Slate-400, "Sign up here" in
    Violet-600).

VARIANT 3 — MAGAZINE SIGN UP ("/signup/magazine"):
Wider layout, max-width 560px. Same white card on #F8FAFC:
  - "Inkwell" wordmark.
  - "Register your magazine" (text-2xl font-semibold Slate-900).
  - "Source exclusive content from independent writers." (text-sm Slate-500).
  - Two-column form on desktop (left column / right column, 16px gap):
    Left: Magazine name, slug input (with "/m/slug" preview in Geist Mono text-xs Slate-400),
    email, password.
    Right: website URL, description textarea (3 rows), logo upload area (dashed Slate-200
    border, rounded-lg, 80px height, centered Phosphor Image icon + "Upload logo" text-xs
    Slate-400, hover Slate-100).
  - Full-width below the form:
    "Create magazine account" primary button (Violet-600).
    Info note below button: Phosphor Info icon (Slate-400) + "A subscription is required
    to access the marketplace. You'll choose your plan on the next step." (text-xs Slate-400).
  - "Already have an account? Sign in" link.

Mobile (375px): all variants single column, card becomes full-width with 16px horizontal
padding, no border (card merges with canvas). Magazine signup stacks two columns vertically.
```
