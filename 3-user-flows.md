# 📄 03 - User Flows

---

## 1. 🧠 Overview

This document defines the core user journeys within the platform.  
Each flow represents a sequence of actions performed by users to achieve a specific goal.

These flows are critical for:
- UI/UX design
- API design
- State management
- System behavior validation

---

## 2. 👤 Authentication Flow

### 2.1 Sign Up

User visits platform  
→ Clicks "Sign Up"  
→ Chooses method (Email/Password or Google OAuth)  
→ Submits credentials  
→ System validates data  
→ Account created  
→ User redirected to feed  

---

### 2.2 Login

User clicks "Login"  
→ Enters credentials or uses Google  
→ System authenticates  
→ JWT issued  
→ User redirected to feed  

---

## 3. 📰 Feed & Content Consumption Flow

### 3.1 Browse Feed (Guest)

User lands on homepage  
→ Sees article feed (titles, excerpts, thumbnails)  
→ Clicks on article  
→ System blocks full access  
→ Prompt: Login / Sign Up  

---

### 3.2 Read Article (Authenticated User)

User logs in  
→ Accesses feed  
→ Clicks article  

IF article is free:  
→ Full article displayed  

ELSE IF premium:  
→ Access restricted message  
→ Prompt to upgrade  

---

## 4. ✍️ Article Creation Flow

User clicks "Create Article"  
→ Editor opens  
→ User enters:
- Title  
- Thumbnail  
- Content  
- Excerpt  

→ System auto-saves draft continuously  

→ User chooses:
- Keep as draft  
- Publish  

IF publish:  
→ Select **placement**:
  - **Public** → select visibility (Free / Premium)
    - Premium option is only available if writer is marketplace-eligible (5K readers + 1K reactions)
    - Article appears in public feed
  - **Marketplace** → only available if writer is marketplace-eligible
    - Set article price (platform credits)
    - Preview price shown automatically (10% of price)
    - Article does NOT appear in public feed; visible only to subscribed magazines  

---

## 5. 🤖 AI Chat Assistant Flow

User opens AI chat panel  
→ User inputs prompt  
→ System sends:
- Article context  
- User preferences  

→ AI processes request  
→ Response returned  

→ User chooses:
- Insert into article  
- Ignore  

---

## 6. 🎙️ Voice-to-Article Flow

User clicks "Voice Input"  
→ Records speech  
→ Stops recording  
→ Audio sent to backend  

→ Speech-to-text processing  
→ AI generates structured content  

→ Draft inserted into editor  
→ User edits or refines content  

---

## 7. ✨ Inline Editing Flow (Core Feature)

User selects text in editor  
→ Popup appears near selection  

→ User selects action:
- Reformulate  
- Shorten  
- Expand  
- Simplify  
- Improve engagement  

→ System sends:
- Selected text  
- Article context  
- Action type  

→ AI processes request  
→ Result returned  

→ User chooses:
- Replace original text  
- Insert below  
- Cancel  

---

## 8. 📊 Analytics Flow

Reader opens article  
→ System tracks:
- View event  
- Time spent  
- Scroll behavior (per paragraph)  

→ Events sent to backend  
→ Stored in analytics system  
→ Aggregated into metrics  

→ Writer views dashboard:
- Views  
- Read time  
- Scroll depth  
- Engagement insights  

---

## 9. 💬 Social Interaction Flows

### 9.1 Like Article

User clicks "Like"  
→ System records like  
→ Like count updated  
→ Notification sent to author  

---

### 9.2 Comment on Article

User writes comment  
→ Submits comment  
→ Stored in database  
→ Displayed under article  
→ Author receives notification  

---

### 9.3 Reply to Comment (Threaded)

User clicks "Reply"  
→ Writes response  
→ System links to parent comment  
→ Nested display  

---

### 9.4 Follow Writer

User visits writer profile  
→ Clicks "Follow"  
→ System creates follow relationship  
→ Notification sent to writer  

---

### 9.5 Repost Article

User clicks "Repost"  
→ Article shared to user's profile/feed  
→ Visibility increased  

---

## 9.6 📦 Marketplace Flows

### 9.6.1 Magazine Sign-Up & Subscribe

Visitor clicks "Sign up as Magazine"
→ Form: email, password, magazine name, slug, website, description, logo
→ Submits
→ System validates and creates `users` row with `account_type = 'magazine'`
→ Creates `magazine_profiles` row
→ **Subscription wall**: redirected to subscription selection screen
  - Select plan (MVP: single tier, price TBD)
  - Simulated payment confirmation
  - `subscription_status` set to `active`
  - `credit_balance` initialized to monthly allowance (e.g. 500 credits)
→ Redirected to magazine dashboard / marketplace

If magazine account exists but subscription is inactive:
→ Any attempt to access marketplace → redirected to subscription screen

### 9.6.2 Publish to Marketplace (Writer)

Writer opens publish flow on a drafted article
→ System checks writer eligibility (`is_marketplace_eligible`)

IF not eligible:
→ Marketplace option is greyed out
→ Progress bar shown: "X / 5,000 readers · Y / 1,000 reactions to unlock marketplace"

IF eligible:
→ Writer selects placement: **Marketplace**
→ Enters article price (platform credits, min enforced)
→ Preview price shown automatically (10% of price, read-only)
→ Confirms → article published with `placement = 'marketplace'`
→ Article is invisible in the public feed
→ Article appears in marketplace browse for subscribed magazines

### 9.6.3 Magazine Browses Writers

Magazine logs in (active subscription required)
→ Opens "Marketplace" tab
→ Browses paginated list of marketplace-eligible writers
→ Filters by topic / tags / posting cadence / engagement rate
→ Sorts by relevance
→ Clicks into writer profile

### 9.6.4 Magazine Views Writer Profile

Magazine clicks a writer
→ Lands on writer profile in **evaluation mode**
→ Sees four panels:
  - Audience Analytics
  - Content Analytics
  - Quality Signals
  - AI Portfolio Insights (loaded async, cached if recent)
→ Sees writer's marketplace-listed articles with titles, excerpts, prices, and preview prices
→ Can initiate preview or purchase from this view

### 9.6.5 Preview Article (Stage 2)

Magazine clicks "Preview article" on a marketplace article
→ Confirmation modal shows:
  - Preview price (10% of article price)
  - Current credit balance and balance after deduction
→ Magazine confirms
→ Backend opens DB transaction:
  - Validates `credit_balance >= preview_price`
  - Debits `credit_balance` by preview price
  - Credits writer `earnings_balance` by `preview_price − platform_fee`
  - Inserts `article_purchases` row with `stage = 'preview_unlock'`
  - Inserts transaction rows (`preview_unlock`, `writer_payout`)
→ Commits transaction
→ Magazine can now read the full article
→ Notification to writer ("Your article was previewed by [Magazine]")

If credit balance insufficient:
→ Modal offers "Top up credits" option

### 9.6.6 Purchase Article (Stage 3)

Magazine has previewed the article and clicks "Purchase article"
→ Confirmation modal shows:
  - Remaining amount due (90% of price — preview credit already paid)
  - Total price paid across both stages = 100%
  - Current credit balance and balance after deduction
→ Magazine confirms
→ Backend opens DB transaction:
  - Looks up existing `article_purchases` preview row for `(article_id, magazine_id)`
  - Validates `credit_balance >= remaining_amount`
  - Debits `credit_balance` by remaining amount
  - Credits writer `earnings_balance` by `remaining_amount − platform_fee`
  - Inserts `article_purchases` row with `stage = 'full_purchase'` and `parent_purchase_id` pointing to preview row
  - Inserts transaction rows (`article_full_purchase`, `writer_payout`)
→ Commits transaction
→ Article appears in magazine's **curated library** with republish rights
→ Attribution badge "In [Magazine]'s library" appears on article
→ Notification to writer ("Your article was purchased by [Magazine]")

If magazine skips preview and purchases directly:
→ Same flow but `remaining_amount = 100%` (no prior preview credit to subtract)

### 9.6.7 Magazine Subscription Management

Magazine opens Settings → Subscription
→ Sees current plan, renewal date, credit balance, monthly allowance
→ Options:
  - Renew early
  - Cancel (access continues until end of billing cycle)
  - Top up credits (optional, simulated payment, adds to current balance)
→ Monthly renewal: cron job credits `monthly_credit_allowance` to `credit_balance` and inserts `monthly_credit_grant` transaction row

### 9.6.8 Writer Earnings Review

Writer opens Earnings dashboard
→ Sees:
  - Lifetime earnings (preview payouts + purchase payouts combined)
  - Recent transactions (previews and purchases separately itemized)
  - Articles ranked by total revenue
  - Earnings balance
→ Clicks "Withdraw" (simulated payout in MVP)
→ Writer sees progress toward marketplace eligibility if not yet unlocked

---

## 10. 🔔 Notification Flow

Trigger event occurs:
- New follower
- New like
- New comment / reply
- **Article licensed by magazine** (writer-facing)
- **Wallet credited** (writer-facing — license payout)

→ Notification created in DB
→ Stored in system
→ Delivered to active sessions via **Server-Sent Events (SSE)**
→ Persisted for offline retrieval (bell icon dropdown)  

---

## 11. ⚠️ Moderation Flow

### 11.1 Report Content

User clicks "Report"  
→ Selects reason  
→ Report submitted  
→ Stored in moderation system  

---

### 11.2 Admin Review

Admin accesses reports  
→ Reviews content or user  
→ Chooses action:
- Ignore  
- Delete content  
- Ban user  

---

## 12. 🔐 Access Control Flow

User requests article  
→ System checks:
- Authentication status  
- Subscription type  

IF not authenticated:  
→ Block access  
→ Prompt login  

ELSE IF premium content AND user is free:  
→ Block access  
→ Prompt upgrade  

ELSE:  
→ Grant access  

---

## 13. ⚠️ Edge Cases

- Network failure during AI request → show retry option  
- Large text selection → process in chunks  
- Unauthorized access → redirect to login  
- Token limit exceeded → block AI action and show warning  

---

## ✅ Summary

These user flows define all critical interactions in the system and ensure:

- Clear user journeys  
- Predictable system behavior  
- Strong foundation for UI and backend implementation  
