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
→ Select visibility (Free / Premium)  
→ Article appears in feed  

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

## 10. 🔔 Notification Flow

Trigger event occurs:
- New follower  
- New like  
- New comment  

→ Notification created  
→ Stored in system  
→ Delivered to user interface  

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
