# Chapter 7 — Release 4: social depth, the reworked assistant and documents

## Introduction

The last release deepens what the platform already did. Sprint 7 completes the social
layer with comment likes, follower lists, blocking, saving and sharing. Sprint 8
reworks the assistant: it now decides on each request whether to answer or to write
into the document, shows its real pipeline as it runs, and accepts and speaks voice;
the feed card becomes interactive. Sprint 9 gives the writer a private library of
reference documents that the assistant can draw on and cite by page.

## 7.1 Sprint 7 — Comment likes, lists, block, save and share

### 7.1.1 Sprint goal and backlog

**Goal:** readers like comments, browse and act on follower lists, block accounts,
keep articles for later and share them outside the platform.

**Table 7.1 – Sprint 7 backlog**

<!-- INCLUDE:sprint-7 -->

### 7.1.2 Analysis

Figure 7.1 gives the use cases of Sprint 7. Sharing and the follower lists need no
account; following from a list extends viewing it. Liking a comment and saving an
article include notifying the recipient. A block hides the two accounts from each
other — profiles, articles and comments — and the only place to lift it is the
blocker's settings. Saves are private: the author is notified, but nobody else can
see what a reader keeps.

![Figure 7.1 – Use case diagram, Sprint 7](../diagrams/fig-7-1-use-case-sprint-7/fig-7-1-use-case-sprint-7.png){width=100%}

### 7.1.3 Design

Figure 7.2 shows the three new tables — `CommentLike`, `Block` and `Save` — and the two
notification types they emit. Each carries a unique constraint on its pair, so a
repeated request is a no-op, and a notification is emitted only when a row was actually
inserted; a check constraint forbids blocking oneself. A block row is directional, but
every read treats it both ways. Comment likes are kept in their own table rather than
among article likes, so that by construction they can never count towards a writer's
eligibility.

![Figure 7.2 – Class diagram, Sprint 7](../diagrams/fig-7-2-classes-sprint-7/fig-7-2-classes-sprint-7.png){width=100%}

### 7.1.4 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/reader-05-saved.png`

**Figure 7.3 – The Saved shelf**

> 📷 **Screenshot placeholder** — `figures/screens/reader-06-blocked-accounts.png`

**Figure 7.4 – Blocked accounts, in settings**

> 📷 **Screenshot placeholder** — `figures/screens/reader-07-following-feed.png`

**Figure 7.5 – The following feed**

> 📷 **Screenshot placeholder** — `figures/screens/reader-08-followers-search.png`

**Figure 7.6 – A follower list, searched**

## 7.2 Sprint 8 — Live cards, the assistant that writes, and voice

### 7.2.1 Sprint goal and backlog

**Goal:** readers react, repost and comment from the feed card, see recent comments
and preview any byline; the assistant decides whether to answer or to write into the
document, writes into a protected range the writer keeps or discards, shows its steps
as they run, sits in a panel docked beside the editor, accepts dictated prompts and
reads its replies aloud.

**Table 7.2 – Sprint 8 backlog**

<!-- INCLUDE:sprint-8 -->

### 7.2.2 Analysis

Figure 7.7 gives the use cases of Sprint 8. Briefing the assistant specialises into
receiving an answer in the panel and having text written into the document, and
includes following the live pipeline steps and consuming the allowance; keeping or
discarding the written text includes the write. Dictating extends the brief and is
billed; hearing the reply extends the answer. The choice between answering and writing
is the assistant's, made per message; it supersedes the manual "insert the answer into
the document" of Sprint 2 (FR-30, superseded by FR-78).

![Figure 7.7 – Use case diagram, Sprint 8](../diagrams/fig-7-3-use-case-sprint-8/fig-7-3-use-case-sprint-8.png){width=100%}

### 7.2.3 Design

**Sequence diagram — one assistant turn.** Figure 7.8 shows a turn. The request
carries the conversation, the article and any selection. The system reads the draft,
the writer's voice profile and — when documents are attached — passages from them,
reporting each stage to the panel as it completes. A single routing call to the model
then either answers in the panel, streamed as Markdown, or calls the
`write_to_article` tool with a placement (at the cursor or over the selection) and a
one-line brief; the write is described in Figure 7.9, after which the model adds a
one-line recap. The tokens of both calls are settled once, at the end; a stopped turn
still bills an estimate of what was produced. The response is a typed stream: status
parts for each stage, text parts for the answer, and article parts for the write.

![Figure 7.8 – Sequence diagram: one assistant turn](../diagrams/fig-7-4-sequence-assistant-turn/fig-7-4-sequence-assistant-turn.png){width=100%}

**Sequence diagram — writing into the document.** Figure 7.9 shows the write. The
system retrieves passages from the writer's other published articles and streams the
article text from a second model call. The panel opens a range in the editor at a block
boundary — after the block holding the cursor, or over the selected blocks — tints it
and refuses the writer's own edits inside it; each Markdown block is inserted as soon
as it is complete, outside the undo history. When the stream ends, the writer keeps the
text, which becomes one undo step, or discards it, which restores exactly what was
there. Opening the range at a block boundary is what makes that restoration exact:
every node the writer owns stays untouched.

![Figure 7.9 – Sequence diagram: writing into the document](../diagrams/fig-7-5-sequence-in-document-write/fig-7-5-sequence-in-document-write.png){width=100%}

**Sequence diagram — voice.** Figure 7.10 shows the voice round trip. A recording of
at most five minutes is sent with its length; the system checks the allowance, the
format and the size, transcribes it with Whisper, settles the duration — the
provider's when it reports one, otherwise the larger of the client's figure and a floor
derived from the file size — and bills 200 tokens per started minute. The transcript
lands in the composer, editable. Reading a reply aloud is free to the writer and
limited per account instead, to 20 replies a minute and 300 a day; the control exists
only when speech synthesis is available, and the mute choice persists in the browser.

![Figure 7.10 – Sequence diagram: the voice round trip](../diagrams/fig-7-6-sequence-voice-round-trip/fig-7-6-sequence-voice-round-trip.png){width=100%}

### 7.2.4 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/reader-09-reposted-tab.png`

**Figure 7.11 – The Reposted tab of a profile**

> 📷 **Screenshot placeholder** — `figures/screens/writer-14-ai-keep-discard.png`

**Figure 7.12 – A write awaiting Keep or Discard**

> 📷 **Screenshot placeholder** — `figures/screens/writer-15-ai-rail-live-step.png`

**Figure 7.13 – The live step on the collapsed panel**

## 7.3 Sprint 9 — Document library and citations

### 7.3.1 Sprint goal and backlog

**Goal:** a writer uploads reference documents into a private library, attaches them to
an article, and the assistant draws on them for answers and writes, citing each
passage by document and page.

**Table 7.3 – Sprint 9 backlog**

<!-- INCLUDE:sprint-9 -->

### 7.3.2 Analysis

Figure 7.14 gives the use cases of Sprint 9. Managing the library specialises into
uploading, retrying a failed document and deleting; uploading and retrying include
extracting, chunking and embedding the text. Attaching documents to an article is
extended by detaching one. Asking the assistant is extended by citing passages as
*[Title, p. N]*, itself extended by opening a cited passage at its page. Documents are
PDF, DOCX, TXT or Markdown files under 10 MB and 200 pages, at most 20 per writer. A
document is the writer's alone: it never feeds the voice profile, portfolio insights
or search, and no other account can read, attach or discover it.

![Figure 7.14 – Use case diagram, Sprint 9](../diagrams/fig-7-7-use-case-sprint-9/fig-7-7-use-case-sprint-9.png){width=100%}

### 7.3.3 Design

**Class diagram.** Figure 7.15 shows the library: a `Document` with its status, page and
chunk counts and a readable error; its `DocumentChunk`s, each keeping the page it came
from, which is what a citation points to; and the `ArticleDocument` attachments. The
status moves from pending to extracting to ready, or to failed with a reason the writer
can act on; the only backward move is a retry.

![Figure 7.15 – Class diagram, Sprint 9](../diagrams/fig-7-8-classes-sprint-9/fig-7-8-classes-sprint-9.png){width=100%}

**Sequence diagram — ingestion.** Figure 7.16 shows a document's path, the companion of
the publishing pipeline of Chapter 5. The browser asks for a presigned URL and uploads
the file straight to a private bucket — the file never passes through the API. The
registration checks that the object exists and is under 10 MB, counts the writer's
documents under a per-writer lock and queues ingestion. The worker extracts the text
page by page, refuses a document over 200 pages or without a text layer with a readable
reason, then chunks it, embeds the chunks and marks it ready in one transaction. The
file is served back only to its owner, through the API, as a short-lived URL.

![Figure 7.16 – Sequence diagram: document upload and ingestion](../diagrams/fig-7-9-sequence-document-ingestion/fig-7-9-sequence-document-ingestion.png){width=100%}

### 7.3.4 Realisation

> 📷 **Screenshot placeholder** — `figures/screens/writer-16-document-library.png`

**Figure 7.17 – The document library, one document refused with its reason**

> 📷 **Screenshot placeholder** — `figures/screens/writer-17-ai-sources-tab.png`

**Figure 7.18 – Attaching a document from the Sources tab**

> 📷 **Screenshot placeholder** — `figures/screens/writer-18-ai-cited-reply.png`

**Figure 7.19 – A reply citing its source as [Title, p. N]**

## Conclusion

Release 4 completed the social layer, turned the assistant from a chat beside the
editor into a collaborator that writes into the document under the writer's control,
added voice in both directions, and gave the writer a private library of sources the
assistant can cite to the page.

\newpage
