# 17 — Notifications

**Route:** `/notifications` · **Role:** Any authenticated user · **Stitch mode:** Standard

Full-page notification center — grouped by date, with read/unread states and action links.

> Paste [`00-design-system.md`](./00-design-system.md) first, then the block below.

---

```
Screen: Notifications page, route "/notifications".

Layout: top navigation bar (notification bell in navbar should show NO dot since
user is viewing this page), then dashboard layout with sidebar + main on #F8FAFC canvas.

LEFT SIDEBAR (240px):
  Same dashboard nav for the user's role.
  Notifications item is active (Violet-50 bg, Violet-700 text, Phosphor Bell icon).

MAIN AREA:

  PAGE HEADER ROW:
    Left: "Notifications" (text-2xl font-semibold Slate-900).
    Right: "Mark all as read" ghost button (text-sm Slate-400, Phosphor Checks icon).

  FILTER PILLS (16px below header):
    "All" (active — Violet-600 bg, white text), "Unread" (Slate-200 border, Slate-600 text),
    "Comments" (same), "Purchases" (same), "Followers" (same).
    Rounded-full, text-sm, padding 6px 16px, 8px gap.

  NOTIFICATION LIST (20px below filters):
    White card, 1px Slate-200 border, rounded-xl, no internal padding (list fills card).

    DATE GROUP HEADER: "Today" (text-xs uppercase tracking-wide Slate-400, padding 12px 20px,
    Slate-50 bg, 1px Slate-100 bottom border).

    NOTIFICATION ROW (unread state):
      4px Violet-600 left border accent. Slate-50 background (unread tint).
      Padding 16px 20px. 1px Slate-100 bottom border.
      Left: avatar (32px) of the actor.
      Center:
        Text: "<strong>Marcus Chen</strong> commented on your article
        <strong>The Quiet Art of Editing</strong>" (text-sm Slate-700).
        Preview: "The point about 'druid-clearing' paragraphs hit home..." (text-xs
        Slate-500, 1 line truncated, italic).
        Timestamp: "2 hours ago" (text-xs Slate-400 Geist Mono).
      Right: Phosphor ChatCircle icon (Slate-300, 16px) indicating type.

    NOTIFICATION ROW (unread):
      4px Violet-600 left border.
      Avatar (32px) + "<strong>The Atlantic Review</strong> purchased your article
      <strong>Remote Work in 2026</strong> for <strong>120 credits</strong>"
      (text-sm Slate-700). Amount in Geist Mono.
      Timestamp: "5 hours ago". Type icon: Phosphor ShoppingCart (Slate-300).

    NOTIFICATION ROW (read state):
      No left border accent. White background (not Slate-50).
      Avatar + "<strong>Sarah Okafor</strong> started following you" (text-sm Slate-600,
      slightly lighter than unread).
      Timestamp: "1 day ago". Type icon: Phosphor UserPlus (Slate-300).

    DATE GROUP HEADER: "Yesterday" (same style as "Today").

    3 more read notification rows:
      - A "liked your article" notification (Phosphor Heart icon).
      - A "preview unlocked" notification (Phosphor Eye icon, Amber-50 type tint).
      - A "new follower" notification (Phosphor UserPlus icon).

    DATE GROUP HEADER: "This week".
    2 more read rows.

  PAGINATION (16px below list card):
    "Showing 8 of 34 notifications" (text-xs Slate-400 Geist Mono, centered).
    "Load more" ghost button (text-sm Slate-500, centered).

Mobile (375px): sidebar collapses to bottom tab bar. Filter pills scroll horizontally.
Notification rows: avatar + text stack, timestamp below text. Full-width card,
no horizontal padding reduction. Left border accent stays.
```
