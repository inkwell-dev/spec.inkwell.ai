# 📄 01 - Product Overview

---

## 1. 🧠 Executive Summary

Inkwell is an **AI-powered writing marketplace** that connects independent writers with magazine publishers.

The platform combines three pillars:

1. **AI-collaborative writing** — Writers produce high-quality content with the help of an AI assistant integrated via chat, voice input, and inline editing tools.
2. **Decision-support analytics** — Every published article generates rich engagement data (audience, content, quality signals) that feeds writer profile dashboards used by magazines to evaluate talent.
3. **Article licensing marketplace** — Magazines (a distinct account type) browse writer profiles, consume AI-generated portfolio insights, and **license existing articles** for republication at writer-set prices. Writers earn from licensing; magazines build curated libraries of vetted content.

This shifts Inkwell from a "blog with AI" to a **two-sided platform** where AI assists creation and analytics drives transactions.

---

## 2. 🎯 Problem Statement

The independent writing ecosystem suffers from disconnects on both supply and demand sides:

### 2.1 Writing Challenges (Supply Side)
- Independent writers struggle with structuring ideas, maintaining quality, and writing efficiently
- Existing platforms provide limited or no AI assistance during the writing process
- Writers have no clear path to monetize quality work beyond ad revenue or paid subscriptions

### 2.2 Discovery & Evaluation Gap (Demand Side)
- Magazines and publishers struggle to discover quality independent writers
- When they do find writers, they lack objective signals about audience, consistency, voice, and engagement quality
- Evaluation is currently a manual, time-consuming process (reading samples, requesting portfolios, intuition-based decisions)

### 2.3 Weak Feedback Loops
- Writers lack insight into how readers interact with their content and where engagement drops
- That same engagement data could power buyer decisions, but no platform exposes it for that purpose

### 2.4 No Native Licensing Market
- Existing platforms (Medium, Substack) are subscription-driven, not transactional
- There is no marketplace where magazines can browse, evaluate, and license articles from independent writers in a self-serve way

---

## 3. 💡 Proposed Solution

Inkwell is an **AI-native writing marketplace** with three coordinated layers:

### 3.1 Writers Collaborate with AI
- Generate content using a chat-based assistant, voice input, and inline editing tools
- Improve writing quality with contextual, RAG-powered suggestions trained on the writer's own past articles ("writes like me")

### 3.2 Intelligent Editing Experience
- Users can select any text and:
  - Reformulate
  - Simplify
  - Expand
  - Shorten
  - Improve engagement

### 3.3 Voice-Driven Content Creation
- Writers describe ideas verbally
- System transcribes (Groq Whisper) and structures speech into article drafts

### 3.4 Decision-Support Analytics
Two distinct analytics surfaces:
- **Writer-facing** — views, read time, scroll depth, drop-off points, engagement insights (self-improvement)
- **Magazine-facing** — writer evaluation dashboard exposing audience composition, content patterns, quality signals, and AI-generated portfolio insights (purchase decision support)

### 3.5 Article Licensing Marketplace
- Writers mark published articles as **available for licensing** at a fixed price
- Magazines browse, evaluate (with analytics + AI insights), and **license** articles to feature in their curated library
- Licensing is simulated payment in MVP; in production this is the platform's primary revenue mechanism (transaction fee)

### 3.6 Controlled Content Access
- Articles can be:
  - Free (visible to any authenticated user)
  - Premium (restricted to premium plan users)
- Licensing availability is orthogonal to free/premium — any published article can be marked licensable

---

## 4. 👥 Target Users

### 4.1 Independent Writers
- Solo creators, bloggers, journalists, domain experts producing original content
- Looking to grow audience and monetize quality work

### 4.2 Magazines & Publishers
- Editorial teams sourcing content for their publications
- Want to discover independent talent without going through agencies
- Need objective signals (analytics, AI portfolio insights) to make confident purchase decisions

### 4.3 Readers
- General audience consuming articles across topics
- Free readers access free articles; premium readers access all

---

## 5. 🧑‍💼 Account Model

Inkwell uses an **account type** + **role** + **plan** model to cleanly separate identity, capability, and entitlement.

### 5.1 Account Types

| Account Type | Description |
|--------------|-------------|
| **Personal** | Individual users — can be readers, writers, or both |
| **Magazine** | Organizations licensing content — branded profile, wallet, curated library |

### 5.2 Roles (Personal accounts)

| Role | Description |
|------|-------------|
| Reader | Default — can read articles, like, comment, follow |
| Writer | Reader + can create, edit, publish, list articles for licensing |
| Admin | Platform administration, moderation, reports |

Roles are additive — every writer is also a reader. Magazine accounts have their own capability set (browse writers, view evaluation analytics, license articles) and do not use the personal-account role enum.

### 5.3 Guest Access

Unauthenticated visitors can browse the public feed (titles, excerpts, thumbnails) but cannot access full article content. They are prompted to sign up to read.

---

## 6. 🔐 Access & Subscription Model

### 6.1 Plans (Personal accounts)

Plans are orthogonal to role — a user can be a `writer` with `free` plan or `premium` plan.

| Plan | Reading Access | Writing Capability |
|------|----------------|---------------------|
| **Free** | Free articles only | Can write, but no AI assistance |
| **Premium** | All articles (free + premium) | Full AI assistance with daily token quota |

### 6.2 Magazine Accounts

- Magazines do not use the personal free/premium plan
- They maintain a **wallet balance** denominated in platform credits (simulated currency)
- Wallet credits are spent on article licenses
- Magazines can read any article they have licensed regardless of free/premium status

---

### 6.2 AI Usage Model
- AI usage is limited by **daily token quota**
- Users can:
  - Consume tokens through AI actions
  - Purchase additional tokens (simulated in MVP)

---

## 7. 🌍 Platform Scope

### 7.1 Public Platform
- Articles are discoverable via a **feed system**
- Full access requires authentication

### 7.2 Content Visibility

Each article can be:
- Public (free users)
- Premium-only (restricted access)

---

## 8. 🧩 Core Functional Domains

The platform is divided into the following domains:

### 8.1 Content Creation
- TipTap-based rich text editor
- Auto-saving draft system
- Publishing workflow (status, visibility, tags, slug)

### 8.2 AI Assistance
- Chat assistant (RAG over writer's own corpus)
- Voice processing (Groq Whisper → structured draft)
- Inline editing actions (reformulate / shorten / expand / simplify / improve)
- Portfolio Insights for magazines (RAG-generated writer evaluation)

### 8.3 Social Interaction
- Likes / reactions
- Threaded comments
- Follow system
- Reposts

### 8.4 Analytics
Two surfaces, sharing the same underlying event pipeline:
- **Writer-facing** — self-improvement metrics
- **Magazine-facing** — writer evaluation (audience, content, quality, AI portfolio insights)

### 8.5 Licensing Marketplace
- Article listings (writer-set prices)
- Magazine browsing and search
- License purchase flow (simulated payment)
- Magazine curated library
- Writer wallet & earnings

### 8.6 Moderation
- Article and user reporting
- Admin queue, content moderation (OpenAI moderation API)
- Soft delete + audit trail

---

## 9. ⚙️ Key Functional Principles

### 9.1 AI as a First-Class Feature
AI is not an add-on; it is integrated into:
- Writing
- Editing
- Feedback

### 9.2 User-Centric Design
- Minimal friction in writing flow
- Fast interactions (especially AI)

### 9.3 Scalable Architecture
- Modular backend
- Separate AI service
- Event-driven analytics

### 9.4 Security & Access Control
- Role-based permissions
- Content access restrictions

---

## 10. ⚠️ Assumptions & Constraints

### 10.1 Assumptions
- Users are familiar with basic writing tools
- AI responses are probabilistic and may require user validation

### 10.2 Constraints
- AI usage limited by cost → token system required
- Voice processing is **non-real-time** in MVP
- Advanced analytics may be simplified initially

---

## 11. 🧪 Success Criteria

### Product Metrics
- Users can:
  - Create and publish articles
  - Use AI assistance effectively

### Technical Metrics
- System is stable and scalable
- AI responses are integrated smoothly

### User Experience
- Writing workflow is intuitive
- AI interactions feel natural and helpful

---

## 12. 🚀 Future Vision

Beyond MVP, the platform can evolve into:

- AI style learning (personalized writing assistant)
- Advanced engagement analytics
- Collaborative writing environments
- Multilingual publishing

---

## ✅ Summary

This platform aims to redefine content creation by combining:
- **AI-assisted writing**
- **Rich user interaction**
- **Data-driven insights**

into a single, scalable system.
