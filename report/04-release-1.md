# Chapter 4 — Release 1: functional foundation

## Introduction

The first release lays the foundation every later feature depends on. Sprint 1
delivers the data model, authentication and the core of article management; Sprint 2
delivers the rich-text editor, the first version of the AI assistant and the capture
of reading events that the analytics of Release 2 will aggregate. For each sprint this
chapter gives the sprint backlog, the analysis and design, and the realisation.

## 4.1 Sprint 1 — Schema, authentication and article core

### 4.1.1 Sprint goal and backlog

**Goal:** a visitor can register and sign in, by password or with Google; a writer can
create, edit, publish and delete articles, choosing their placement and visibility; a
visitor can browse the public feed and read free articles. The sprint also establishes
the ledger invariant harness that every later money-moving feature is tested against.

**Table 4.1 – Sprint 1 backlog**

<!-- INCLUDE:sprint-1 -->

### 4.1.2 Analysis

**Use case diagram.** Figure 4.1 refines the global diagram for Sprint 1. Registering
specialises into registering as a reader or as a magazine; managing one's own articles
specialises into creating a draft, editing, publishing and deleting; publishing
includes choosing a placement and a visibility.

![Figure 4.1 – Use case diagram, Sprint 1](../diagrams/fig-4-1-use-case-sprint-1/fig-4-1-use-case-sprint-1.png){width=100%}

**Textual description.** Table 4.2 details the central use case of the sprint.

**Table 4.2 – Textual description of "Publish an article"**

| Item | Description |
|---|---|
| Use case | Publish an article |
| Actor | Writer (A4); eligible writer (A5) for premium or marketplace placement |
| Pre-condition | The writer is signed in and owns a draft |
| Post-condition | The article is published with its placement, visibility, slug and reading time |
| Main scenario | 1. The writer opens the publish dialog. 2. The writer chooses a placement (public or marketplace) and, for a public article, a visibility (free or premium), and sets the cover, tags and excerpt. 3. The system checks that the writer may use the chosen placement and visibility. 4. The system publishes the article and computes its word count and reading time. 5. The article appears in the feed (public) or on the marketplace (marketplace). |
| Alternative scenario | 3a. The writer is not eligible and chose premium or marketplace: the system refuses and keeps the draft. 2a. Marketplace without a price: the system refuses. |

### 4.1.3 Design

**Class diagram.** Figure 4.2 shows the classes of Sprint 1: the `User` with its account
type, authentication provider, role and plan; the `MagazineProfile` that extends a
magazine account with its name, slug and branding; the `Article` with its status,
placement, visibility, price and generated search vector; tags through an association
table; and comments. Role and plan are empty for a magazine account, which a database
constraint enforces.

![Figure 4.2 – Class diagram, Sprint 1](../diagrams/fig-4-2-classes-sprint-1/fig-4-2-classes-sprint-1.png){width=100%}

**Sequence diagram — sign in.** Figure 4.3 shows signing in and the silent refresh that
keeps a session alive. Sign-in is rate-limited per address — ten attempts a minute,
five for registration, against sixty for other routes — and answers 429 before the
account is even read. On success the system issues a 15-minute access token and a
7-day refresh token; when a later request meets an expired access token, the client
refreshes it, rewrites both the client store and the cookie the route proxy reads, and
retries the original request transparently.

![Figure 4.3 – Sequence diagram: sign in and silent refresh](../diagrams/fig-4-3-sequence-authentication/fig-4-3-sequence-authentication.png){width=100%}

**The ledger invariant harness.** Money-like data appears from Sprint 5 onwards, but
its correctness rule is set here: every denormalised balance — a magazine's credit
balance, a writer's earnings — must equal the sum of its ledger rows. Three invariants
encode that rule and are asserted after every test that moves credits. The harness is
tested by sabotage: fixtures build a coherent purchase, then corrupt one column at a
time and check that the right invariant fails.

### 4.1.4 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/guest-01-home.png`

**Figure 4.4 – The public feed, as seen by a visitor**

> 📷 **Screenshot placeholder** — `figures/screens/guest-02-login.png`

**Figure 4.5 – Sign-in, with Google sign-in**

> 📷 **Screenshot placeholder** — `figures/screens/guest-03-register.png`

**Figure 4.6 – Registering a personal account**

> 📷 **Screenshot placeholder** — `figures/screens/guest-04-register-magazine.png`

**Figure 4.7 – Registering a magazine account**

> 📷 **Screenshot placeholder** — `figures/screens/guest-05-article-free.png`

**Figure 4.8 – A free article, readable without an account**

> 📷 **Screenshot placeholder** — `figures/screens/reader-04-settings.png`

**Figure 4.9 – Profile settings**

## 4.2 Sprint 2 — Editor, AI assistance and event capture

### 4.2.1 Sprint goal and backlog

**Goal:** a writer drafts in a rich-text editor with automatic saving and images; a
premium writer converses with an AI assistant and applies inline AI actions to a
selection, within a daily token allowance; every article page records reading events.

**Table 4.3 – Sprint 2 backlog**

<!-- INCLUDE:sprint-2 -->

### 4.2.2 Analysis

Figure 4.10 gives the use cases of Sprint 2. Writing in the editor specialises into
formatting, inserting an image and setting a cover image, and includes saving the
draft automatically. Using the assistant specialises into chatting and applying an
inline action, and includes consuming the daily allowance; inserting the answer into
the document extends the chat. Reading an article includes recording reading events.

![Figure 4.10 – Use case diagram, Sprint 2](../diagrams/fig-4-4-use-case-sprint-2/fig-4-4-use-case-sprint-2.png){width=100%}

### 4.2.3 Design

**Class diagram.** Figure 4.11 adds the classes of Sprint 2: each AI call is logged as
an `AiInteraction` with its action type, tokens used and model; reading is recorded as
`AnalyticsEvent` rows (view, scroll, time on page, like, comment, repost); and the
user carries the remaining daily token allowance and the time of its last reset. The
`voice_transcribe` action type is reserved in the enumeration and used from Sprint 8.

![Figure 4.11 – Class diagram, Sprint 2](../diagrams/fig-4-5-classes-sprint-2/fig-4-5-classes-sprint-2.png){width=100%}

**Sequence diagram — inline AI action.** Figure 4.12 shows an inline action on a
selection. The editor captures the selected range once, before anything is streamed,
so that a click elsewhere cannot move it. The system checks the daily allowance and
refuses with 403 and a plan-aware notice when it is exhausted; otherwise it builds the
prompt from the action, the selection and the surrounding article, streams the
suggestion to the editor as it is generated, and records the interaction and its cost.
The allowance is checked once, before the call: a reply may cost more than what
remained, and the balance then stops at zero.

![Figure 4.12 – Sequence diagram: inline AI action](../diagrams/fig-4-6-sequence-inline-ai-edit/fig-4-6-sequence-inline-ai-edit.png){width=100%}

**Event capture.** The article page observes scroll depth and engaged time and sends
batched events — every ten events, every five seconds, or when the page is left — to
`POST /analytics/events`. The server, not the client, attaches the reader's identity
from the access token, the country and the device. Capture starts in this sprint so
that real reading data accumulates before the dashboards of Release 2 aggregate it.

### 4.2.4 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/writer-03-editor.png`

**Figure 4.13 – The rich-text editor with the assistant panel**

> 📷 **Screenshot placeholder** — `figures/screens/writer-04-publish-dialog.png`

**Figure 4.14 – The publish dialog: placement, visibility, tags and excerpt**

> 📷 **Screenshot placeholder** — `figures/screens/writer-05-ai-panel.png`

**Figure 4.15 – The AI assistant panel**

> 📷 **Screenshot placeholder** — `figures/screens/writer-06-ai-answer.png`

**Figure 4.16 – An answer from the assistant**

> 📷 **Screenshot placeholder** — `figures/screens/writer-07-inline-menu.png`

**Figure 4.17 – The inline actions on a selection**

> 📷 **Screenshot placeholder** — `figures/screens/writer-08-inline-suggestion.png`

**Figure 4.18 – An inline suggestion, ready to replace the selection**

## Conclusion

Release 1 delivered the foundation: accounts and authentication with rate limiting and
a silent refresh, article management with placement and visibility, a rich-text editor,
the first AI assistant with inline actions under a daily allowance, and the capture of
reading events. Release 2 builds the social layer and the analytics on top of it.

\newpage
