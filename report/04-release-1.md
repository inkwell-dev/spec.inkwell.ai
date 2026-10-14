# Release 1: functional foundation {#sec:ch3}

## Introduction {.unnumbered}

The first release lays the foundation every later feature depends on. Sprint 1
delivers the data model, authentication and the core of article management; Sprint 2
delivers the rich-text editor, the first version of the AI assistant and the capture
of reading events that the analytics of Release 2 will aggregate. Each sprint is
presented in the same four steps: its backlog, the analysis, the design and the
realisation.

## Sprint 1: Schema, authentication and article core {#sec:sprint1}

### Sprint backlog

The goal of Sprint 1 is that a visitor can register and sign in, by password or with
Google; that a writer can create, edit, publish and delete articles, choosing their
placement and visibility; that a visitor can browse the public feed and read free
articles; and that the ledger invariant harness exists before any feature moves money.
@tbl:sprint-1 lists the stories committed.

<!-- INCLUDE:sprint-1 -->

The sprint commits {{S1PTS}} points, close to the average of the project. Almost a
fifth of them (US-49, US-50, US-51) produce nothing a user sees (the invariant harness,
the one-command stack and the quality gates) and were placed first on purpose: every
later sprint is built and verified with them.

### Analysis

**Use case diagram.** @fig:uc-s1 refines the global diagram for the scope of Sprint 1.

![Use case diagram, Sprint 1](../diagrams/fig-4-1-use-case-sprint-1/fig-4-1-use-case-sprint-1.png){#fig:uc-s1}

Registering specialises into a personal or a magazine account; managing one's
articles into drafting, editing, publishing and deleting, with publishing including a
placement and a visibility. From the first sprint, account type and placement, the
two properties the marketplace rests on, are already in place.

**Textual description.** @tbl:uc-publish details the central use case of the sprint.

+------------------------+--------------------------------------------------------------------+
| Item                   | Description                                                        |
+========================+====================================================================+
| Use case               | Publish an article                                                 |
+------------------------+--------------------------------------------------------------------+
| Actor                  | Writer (A3)                                                        |
+------------------------+--------------------------------------------------------------------+
| Pre-condition          | The writer is signed in and owns a draft                           |
+------------------------+--------------------------------------------------------------------+
| Post-condition         | The article is published with its placement, visibility, slug and  |
|                        | reading time                                                       |
+------------------------+--------------------------------------------------------------------+
| Main scenario          | 1\. The writer opens the publish dialog.                           |
|                        |                                                                    |
|                        | 2\. The writer chooses a placement (public or marketplace) and, for|
|                        |    a public article, a visibility (free or premium), and sets the  |
|                        |    cover, tags and excerpt.                                        |
|                        |                                                                    |
|                        | 3\. The system checks the choices.                                 |
|                        |                                                                    |
|                        | 4\. The system publishes the article and computes its word count   |
|                        |    and reading time.                                               |
|                        |                                                                    |
|                        | 5\. The article appears in the feed (public) or is kept for the    |
|                        |    marketplace (marketplace).                                      |
+------------------------+--------------------------------------------------------------------+
| Alternative scenario   | 3a. A marketplace placement without a price: the system refuses    |
|                        | and keeps the draft.                                               |
+------------------------+--------------------------------------------------------------------+

: Textual description of "Publish an article" {#tbl:uc-publish}

The description shows the scope of Sprint 1 for publishing: the placement and the
visibility are stored and validated, but nobody yet acts on them. From Sprint 5, the
premium visibility and the marketplace placement are reserved to eligible writers
(FR-35, FR-36), which adds a refusal at step 3; FR-23 and FR-24 are therefore
delivered in two steps, and the backlog records both sprints.

### Design

**Class diagram.** @fig:classes-s1 shows the classes of Sprint 1.

![Class diagram, Sprint 1](../diagrams/fig-4-2-classes-sprint-1/fig-4-2-classes-sprint-1.png){#fig:classes-s1}

The `User` carries its account type, provider, role and plan; the `MagazineProfile`
adds a magazine's name, slug and branding; the `Article` carries its status,
placement, visibility and search vector. One `User` class serves every kind of
account, the differences held in attributes, which is what lets one authentication
path serve every actor.

**Sequence diagram: sign in.** @fig:seq-auth shows signing in and the silent refresh
that keeps a session alive.

![Sequence diagram: sign in and silent refresh](../diagrams/fig-4-3-sequence-authentication/fig-4-3-sequence-authentication.png){#fig:seq-auth}

Sign-in is rate-limited (429 after ten attempts a minute) and returns a 15-minute
access token and a 7-day refresh token; an expired access token is refreshed and the
request retried transparently. A long writing session is never interrupted (US-04),
yet a revoked token lasts fifteen minutes at most (NFR-09).

**The ledger invariant harness.** Money appears in Sprint 5, but its rule is set
here: every balance must equal the sum of its ledger rows. Three invariants check it
after every test that moves credits, and the harness is itself tested by sabotage:
corrupting one column must fail the right invariant. No purchase code was ever
written without this check.

### Realisation

The realisation of Sprint 1 is what a visitor sees first. @fig:home shows the public
feed reached without an account.

![The public feed, as seen by a visitor](../figures/screens/guest-01-home.png){#fig:home}

The feed lists published public articles with their author, reading time, excerpt,
cover and reaction counts, filtered by topic along the top (FR-01). The header offers
only *Log in* and *Get started*: a visitor can read and browse but every interaction
leads to an account, which is the boundary between the visitor and the other actors.

@fig:login shows the sign-in page.

![Sign-in, with Google sign-in](../figures/screens/guest-02-login.png){#fig:login}

It offers the two authentication methods of FR-05 side by side (e-mail and password,
and *Continue with Google*) and the link to registration, *Create an account* in
@fig:uc-global. Google sign-in extends *Create an account* there, because a first
Google sign-in creates the account.

Registration differs by account type. @fig:register shows a personal account and
@fig:register-magazine a magazine account.

![Registering a personal account](../figures/screens/guest-03-register.png){#fig:register}

![Registering a magazine account](../figures/screens/guest-04-register-magazine.png){#fig:register-magazine}

The magazine form asks for what writers will see of the buyer (slug, name, website,
description and logo) and no personal fields. FR-04 and FR-39 give two kinds of
account from the first screen, which is why a magazine never inherits a reader's
capabilities.

@fig:article-free shows a free article opened by a visitor.

![A free article, readable without an account](../figures/screens/guest-05-article-free.png){#fig:article-free}

The full body is readable without an account (FR-02). This was a deliberate decision:
gating free articles would contradict the public feed and hide the content from search
engines, so the only articles a visitor cannot read are premium and marketplace ones,
for which Release 3 adds the paywall.

@fig:settings closes the sprint with the profile settings.

![Profile settings](../figures/screens/reader-04-settings.png){#fig:settings}

A signed-in user edits the display name, bio, location, website and profile picture
(FR-07); the picture is uploaded straight to object storage through a presigned URL
(NFR-07). *Save changes* stays disabled until something changes, so a click never sends
an empty update.

## Sprint 2: Editor, AI assistance and event capture {#sec:sprint2}

### Sprint backlog

The goal of Sprint 2 is that a writer drafts in a rich-text editor with automatic
saving and images; that a premium writer converses with an AI assistant and applies
inline AI actions to a selection, within a daily token allowance; and that every
article page records reading events. @tbl:sprint-2 lists the stories.

<!-- INCLUDE:sprint-2 -->

The sprint commits {{S2PTS}} points, and its single largest story, US-14 (13 points),
is split across two sprints: Sprint 2 delivers the conversation with the assistant,
Sprint 4 the retrieval that grounds it in the writer's corpus. The editor stories
(US-06 to US-09) come straight from the screens of the design track, which is why
they could be estimated with confidence.

### Analysis

@fig:uc-s2 gives the use cases of Sprint 2.

![Use case diagram, Sprint 2](../diagrams/fig-4-4-use-case-sprint-2/fig-4-4-use-case-sprint-2.png){#fig:uc-s2}

Writing specialises into formatting, inserting an image and setting a cover, and
includes the automatic save; using the assistant specialises into chatting and inline
actions and includes the daily allowance, so no path to a model goes uncounted.
Reading an article includes recording reading events. Upgrading from the interface
arrives in Sprint 5; here premium accounts come from the seed.

### Design

**Class diagram.** @fig:classes-s2 adds the classes of Sprint 2.

![Class diagram, Sprint 2](../diagrams/fig-4-5-classes-sprint-2/fig-4-5-classes-sprint-2.png){#fig:classes-s2}

Each AI call is logged as an `AiInteraction` with its action, tokens and model, and
reading is recorded as `AnalyticsEvent` rows; the user carries the remaining daily
allowance. Cost and reading are both append-only, so the allowance can be audited and
every metric of Release 2 is computed from events recorded from this sprint on.

**Sequence diagram: inline AI action.** @fig:seq-inline shows an inline action on a
selection.

![Sequence diagram: inline AI action](../diagrams/fig-4-6-sequence-inline-ai-edit/fig-4-6-sequence-inline-ai-edit.png){#fig:seq-inline}

The selection is fixed before streaming, so a click elsewhere cannot move it. The
allowance is checked once (403 when exhausted), then the suggestion is streamed and
its cost recorded. A writer is therefore never cut off mid-reply, at the price of a
small overrun on the day's last call.

**Event capture.** The article page sends batched reading events (scroll depth and
engaged time) to `POST /analytics/events`. The server, not the browser, attaches the
reader's identity from the access token, so no one can forge another reader's events.
Capture starts here so that real data accumulates before the dashboards of Release 2.

### Realisation

@fig:editor shows the editor, where a writer spends most of their time.

![The rich-text editor with the assistant panel](../figures/screens/writer-03-editor.png){#fig:editor}

The draft is edited as rich text (emphasis, headings, lists, quotes, code, images;
FR-18, FR-20) and saved automatically, as the *Saved* label shows (FR-19). The
assistant sits beside the text, not on another page: help arrives where the writing
happens.

@fig:publish-dialog shows the publish dialog designed in Sprint 1 and used here.

![The publish dialog: placement, visibility, tags and excerpt](../figures/screens/writer-04-publish-dialog.png){#fig:publish-dialog}

Every choice of @tbl:uc-publish is on one screen (placement, visibility, cover, tags
and excerpt; FR-21, FR-23, FR-24), so publishing is a single confirmed act and not a
sequence of settings pages.

The assistant is shown in two states. @fig:ai-panel shows the panel before a question
and @fig:ai-answer an answer.

![The AI assistant panel](../figures/screens/writer-05-ai-panel.png){#fig:ai-panel}

![An answer from the assistant](../figures/screens/writer-06-ai-answer.png){#fig:ai-answer}

The panel shows the remaining allowance (20,000 tokens at the start of the day)
before any question (FR-31), so a question's cost is never a surprise. The answer is
streamed and can be inserted at the cursor (FR-27, FR-30), a manual step Sprint 8
replaces.

The inline actions are the second way to use the assistant. @fig:inline-menu shows the
menu on a selection and @fig:inline-suggestion its result.

![The inline actions on a selection](../figures/screens/writer-07-inline-menu.png){#fig:inline-menu}

![An inline suggestion, ready to replace the selection](../figures/screens/writer-08-inline-suggestion.png){#fig:inline-suggestion}

Selecting text opens the five actions of FR-28: reformulate, shorten, expand,
simplify, improve. The suggestion appears in a popover over the highlighted original
rather than replacing it, with three choices: *Replace*, *Insert below* or *Cancel*.
The allowance in the panel has dropped accordingly. The assistant proposes and the
writer decides, which is the rule the whole assistant follows.

## Conclusion {.unnumbered}

Release 1 delivered the foundation: accounts of two types with rate-limited
authentication and a silent refresh, article management with placement and
visibility, a rich-text editor, the first AI assistant with inline actions under a
daily allowance, the capture of reading events, and the ledger harness that every
later money-moving feature is tested against. Release 2 builds the social layer and
the analytics on top of it.
