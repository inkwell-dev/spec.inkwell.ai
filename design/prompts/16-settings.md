# 16 — Settings

**Route:** `/settings` · **Role:** Any authenticated user · **Stitch mode:** Standard

User settings page — profile editing, account preferences, and notification controls. Same layout for writers and magazine accounts, with role-specific sections.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: User Settings page, route "/settings".

Layout: top navigation bar, then dashboard layout with sidebar + main on #F8FAFC canvas.

LEFT SIDEBAR (240px, same nav as the user's dashboard):
  For WRITER: My Articles, Analytics, Earnings, Notifications, Settings (active —
  Violet-50 bg, Violet-700 text). Phosphor icons.
  For MAGAZINE: Marketplace, Library, Subscription & Credits, Notifications, Settings
  (active). Phosphor icons.

MAIN AREA:

  PAGE HEADER: "Settings" (text-2xl font-semibold Slate-900).

  SECTION 1 — Profile (20px below header):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Profile" heading (text-lg font-medium Slate-900).

    Avatar row: circular avatar (80px) + "Change photo" secondary button (text-sm)
    + "Remove" ghost button (text-sm Slate-400).

    Form fields (16px gap between each, max-width 480px):
      "Display name" — text input, pre-filled "Amira Okafor".
      "Username" — text input with "@" prefix indicator, pre-filled "amiraokafor".
        Helper text: "inkwell.ai/u/amiraokafor" (text-xs Slate-400).
      "Bio" — textarea, 3 rows, pre-filled with short bio.
      "Location" — text input, pre-filled "Lagos, Nigeria".
      "Website" — text input, pre-filled with URL.

    "Save changes" primary button (Violet-600, right-aligned) + "Cancel" ghost button.

  SECTION 2 — Account (20px below):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Account" heading (text-lg font-medium Slate-900).

    "Email" row: "o.bejaoui.dev@gmail.com" (text-sm Slate-700) + "Change" link
    (text-sm Violet-600). Verification badge: Emerald-50 pill "Verified".

    "Password" row: "••••••••" (text-sm Slate-400) + "Update password" link
    (text-sm Violet-600).

    "Connected accounts" row: Google icon + "Google" (text-sm Slate-700) +
    "Connected" (text-xs Emerald-600). "Disconnect" ghost link (text-xs Slate-400).

  SECTION 3 — Notification preferences (20px below):
    White card, 1px Slate-200 border, rounded-xl, padding 24px.
    "Notifications" heading (text-lg font-medium Slate-900).

    Toggle rows (each: label left + toggle switch right, 1px Slate-100 bottom border,
    padding 12px 0):
      "New follower" — toggle ON (Violet-600 fill).
      "Comment on your article" — toggle ON.
      "Article liked" — toggle OFF (Slate-200 fill).
      "Weekly analytics digest" — toggle ON.
      "Marketplace purchase notification" — toggle ON.
      "Platform announcements" — toggle OFF.

    Each toggle: 40px wide, 22px tall, rounded-full. Knob: white, 18px circle.

  SECTION 4 — Danger zone (20px below):
    White card, 1px Red-100 border, rounded-xl, padding 24px.
    "Danger zone" heading (text-lg font-medium Red-600).

    "Delete account" row: "Permanently delete your account and all associated data."
    (text-sm Slate-500). "Delete account" destructive button (Red-500 fill, white text,
    text-sm, right-aligned).

Mobile (375px): sidebar collapses to bottom tab bar. All sections stack full-width.
Form fields full-width. Avatar row stacks vertically. Toggle rows full-width.
```
