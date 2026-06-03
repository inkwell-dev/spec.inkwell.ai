# 06 — Auth Screens

**Routes:** `/login`, `/signup`, `/signup/magazine` · **Role:** Guest · **Stitch mode:** Standard

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen set: Authentication screens for Inkwell. Generate THREE variants.

VARIANT 1 — LOGIN ("/login"):
Centered card on a light slate background. Card has:
- "Inkwell" wordmark at top (violet).
- "Welcome back" heading.
- Email input field, password input field with show/hide toggle.
- Violet "Sign in" button (full width).
- A divider with "or" text.
- "Continue with Google" button (outline, Google icon).
- Below: "Don't have an account? Sign up" link, with "Sign up" in violet.

VARIANT 2 — PERSONAL SIGN UP ("/signup"):
Same centered card layout:
- "Inkwell" wordmark.
- "Create your account" heading.
- Name input, email input, username input (with a "/u/username" preview hint),
  password input, confirm password input.
- A toggle row: "I want to write" (writer role) — if toggled on, a small note:
  "You can always start writing later from settings."
- Violet "Create account" button (full width).
- Divider + "Continue with Google" button.
- Below: "Already have an account? Sign in" link.
- Small text: "Are you a magazine? Sign up here" linking to magazine signup.

VARIANT 3 — MAGAZINE SIGN UP ("/signup/magazine"):
Wider centered card (two-column on desktop):
- Left column: "Inkwell" wordmark, "Register your magazine" heading, a short pitch
  ("Source exclusive content from independent writers on Inkwell's marketplace").
- Right column: form fields — magazine name, slug (with "/m/slug" preview), email,
  password, website URL, description textarea, logo upload area (drag & drop).
- Violet "Create magazine account" button.
- Below the button: a note — "A subscription is required to access the marketplace.
  You'll choose your plan on the next step."
- Below: "Already have an account? Sign in" link.

Mobile (375px): all variants become single column, full-width cards with no side margins.
Magazine signup stacks the two columns vertically.
```
