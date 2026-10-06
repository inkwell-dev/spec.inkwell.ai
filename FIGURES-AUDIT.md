# Figure and screenshot audit — before the report is written

The report's visual assets were frozen earlier than the system they describe:

| Asset set | Last changed | Evidence |
|---|---|---|
| `diagrams/` — 33 UML/architecture figures | **2026-08-19** | `git log -- diagrams/` has exactly two commits, both that day |
| `figures/screens/` — 37 screen captures | **2026-08-23** | `chore(figures): capture all 37 in one sitting, against a clean seed` |
| `capture/` harness in the frontend repo | **2026-08-24** | `git log -- capture/` stops there |
| The specs | 2026-09-21 | 37 doc commits after the diagram freeze |
| The code | 2026-09-21 | 60 backend + 81 frontend commits after the diagram freeze |

Everything between those dates is candidate drift. This document is the per-figure
verdict, measured against the code rather than against the specs, so that a figure is
only called stale when something in `src/` actually disagrees with it.

**Structural decision taken:** Sprints 7, 8 and 9 become **Chapter 7**. Chapters 4–6 stay
the historical record of what each sprint delivered. That decision is what makes most of
this set cheap — see §1.

---

## 0. Where the post-freeze work belongs

`10-requirements.md` already attributes every requirement to a report sprint, and §2's
`Sprint` column is the authority used throughout this audit:

| Sprint | Requirements | What shipped | Chapter |
|---|---|---|---|
| **5** | FR-72, FR-73, FR-74 (US-63, US-64) | exclusive purchase; a magazine publishes what it bought under its own masthead | **Ch.6 — existing figures need work** |
| **7** | FR-60…FR-65 (US-56, US-57, US-58) | like a comment, follower/following lists, block, save, share | **Ch.7 — new** |
| **8** | FR-66…FR-68, FR-77…FR-83 (US-59…US-62, US-65…US-69) | live card controls, Reposted tab, recent comments, byline preview, assistant routing and in-document writes, status steps, docked panel, voice in, voice out | **Ch.7 — new** |
| **9** | FR-84…FR-87 (US-70, US-71, US-72) | document library, ingestion, attachment, citations | **Ch.7 — new** |

Three things in that file are themselves stale and the report would quote them:

- **`10-requirements.md:415`** — *"54 stories, 8 epics, 259 points."* There are **72 US
  ids and 9 epics** (E1–E9); the points total was never recomputed.
- **§5's release plan** — *"Three releases, six sprints"*, table stops at Sprint 6. Needs
  rows for Sprints 7, 8 and 9.
- **FR-78 supersedes FR-30** (recorded 2026-09-14). Chapter 4 must therefore present
  FR-30's manual insert as what Sprint 2 built, and Chapter 7 must say it was replaced.

---

## 1. Diagrams — verdict for all 33

**REDRAW** = the figure asserts something the code contradicts · **AMEND** = a label, note
or count is wrong, the structure holds · **OK** = verified unaffected.

A per-sprint figure is judged only against its own sprint's requirements. A global or
architectural figure is judged against the system as built.

### REDRAW — 7 figures

| Figure | Why |
|---|---|
| `fig-2-2-classes-core-domain` | Global, so all sprints count. Missing `CommentLike` (FR-60), `Block` (FR-62), `Save` (FR-63). `Article` is missing `publisherId` (FR-73) and the magazine's *publishes* association. The `NotificationType` box lists 9 values; the enum has **12** — `comment_like`, `save`, `article_published` were appended. |
| `fig-2-3-classes-ai-marketplace-analytics` | Missing `Document`, `DocumentChunk`, `ArticleDocument` (FR-84/85) and the `DocumentStatus` enumeration. The two global class diagrams split "24 persisted classes" between them; there are now **30 tables**. |
| `fig-2-4-gantt` | Captioned *"the eight sprints, as executed"* and stops at S7 (Aug 24 – Sep 6); three more sprints ran to Sep 21. `[Report writing] starts 2026-08-19 lasts 8 days`, `[Report submission] happens at 2026-08-31` and `[Defense] happens at 2026-09-07` are all in the past and none of them happened. **Blocked on the real dates.** |
| `fig-3-2-architecture-backend` | Four worker queues drawn; there are **six** — `embeddings`, `analytics`, `marketplace`, `ai-tokens`, plus `documents` (09-17) and `ai-models` (09-04). No `Documents` module box. The Social box reads *"likes · reposts · follows · notifications"* and omits saves, blocks and comment likes. The guards strip omits the global `ThrottlerGuard`. The provider box says *"LLM, embeddings, moderation"*; speech is a fourth use — Groq transcription, Gemini synthesis. |
| `fig-6-1-use-case-sprint-5` | Sprint 5 gained FR-73: the magazine's own act of publishing an article it bought (`POST /magazines/me/library/:articleId/publish`). FR-72 also makes purchase exclusive, which the `BUY` use case does not convey. |
| `fig-6-2-classes-sprint-5` | Licensing is this figure's subject and `Article.publisherId` — the one column that encodes §4.2's three states — is absent, with it the *publishes* association. |
| `fig-6-8-state-article-lifecycle` | Two states missing, and they are the whole of FR-73. `purchases.service.ts` gives three marketplace states where the figure has one: **Listed** (`marketplace`, no owner) → **Owned** (`marketplace`, a `full_purchase` row, still not public) → **Published** (`public`, `publisherId` set, `visibility` forced to `free`, `marketplacePrice` nulled, `publishedAt` deliberately untouched). The existing `Market → PubFree : abandon the sale` covers only the writer's own withdrawal. |

### AMEND — 12 figures

| Figure | Why |
|---|---|
| `fig-1-1-scrum-framework` | *"54 user stories in 8 epics"* → 72 stories, 9 epics; points to be recomputed. |
| `fig-2-1-use-case-global` | Global, so the coarse labels now understate: *"Interact (like, comment, follow, report)"* omits save, repost and block; nothing covers a magazine publishing licensed work, nor grounding the assistant in uploaded documents. |
| `fig-3-1-architecture-frontend` | The Features box reads *"editor — TipTap · ai-chat · inline actions · analytics capture · marketplace · notifications"*; `src/features/` now holds 18 folders including `documents`, `saves`, `reposts`, `evaluation`, and "ai-chat" is a docked tabbed panel with voice. The Routes box samples 8 of **28** routes and omits every post-freeze one. |
| `fig-3-3-architecture-physical` | The worker box says **"4 queues"** — six now. MinIO is drawn as *"S3 API proxied by nginx at /storage"*; there is a second, **private `documents` bucket** served through `GET /api/documents/:id/file`, deliberately not through `/storage` (FR-87). |
| `fig-3-4-architecture-cicd` | Step 4 asserts *"479 backend tests"*. Unverified — see §3. |
| `fig-4-3-sequence-authentication` | `POST /auth/login` is rate-limited at 10/min and `POST /auth/register` at 5/min (NFR-05, implemented 08-24). No throttle step, no 429 branch. Optional: the security section could carry this instead of the Chapter 4 figure. |
| `fig-4-5-classes-sprint-2` | Carries a note that is now **false**: *"voice_transcribe exists in the enumeration but has no implementation: voice input was descoped in the 2026-07-26 re-baseline and is reported as future work."* Voice shipped under FR-82/83. Reword as a forward reference to Chapter 7 — it becomes an asset rather than a contradiction. |
| `fig-4-6-sequence-inline-ai-edit` | `POST /ai/inline` still works as drawn. Two label fixes: the quota refusal is **403** (`AiQuotaGuard` throws `ForbiddenException`), not the 402 drawn — a pre-existing error, not drift; and the allowance is only checked at the start, so a reply may overdraw, which the note should say (overdraft rule, 09-13). |
| `fig-5-1-use-case-sprint-3` | Sprint 3 kept one new requirement: **FR-70** — liking, commenting on or reposting a marketplace listing is refused, while saving one stays available. Best carried as a note on the `INT` use case rather than a new ellipse. |
| `fig-5-3-sequence-analytics-aggregation` | Step 2 reads *"Attach the country and device server-side"*. Since 08-20 the **viewer identity comes from the access token, not the request body** — worth having in the figure, since it is the fix that made reader attribution real. |
| `fig-6-3-sequence-two-stage-purchase` | Arithmetic and ledger rows still hold. Missing FR-72's exclusivity refusal when another magazine already owns the article, and the **fourth stage**: the purchase now leaves the article *owned but unpublished*. The closing message *"Republish rights granted, article added to the library"* should stop at the library. |
| `fig-6-7-test-strategy` | Four hard numbers to re-measure — see §3. |

*(`fig-6-6-activity-article-access` is listed as OK below, with one branch to confirm.)*

### OK — 14 figures

| Figure | Verified against |
|---|---|
| `fig-1-2-waterfall-vs-agile` | Method only; no code claims. |
| `fig-4-1-use-case-sprint-1` | Google sign-in was already an `«extend»`; finishing it (08-24) changed no use case. |
| `fig-4-2-classes-sprint-1` | `users.location` / `website_url` arrived with the Sprint 6 writer surfaces, not Sprint 1, so their absence here is correct. |
| `fig-4-4-use-case-sprint-2` | An accurate record of Sprint 2. The `«extend»` *"Insert the answer into the document"* is FR-30, which FR-78 superseded in Sprint 8 — note the supersession in the Chapter 7 text, not in this figure. |
| `fig-5-2-classes-sprint-3` | `CommentLike`, `Save` and `Block` are Sprint 7 classes; its 5-value `NotificationType` box is correct for Sprint 3. |
| `fig-5-4-sequence-ai-chat-rag` | An accurate record of the Sprint 4 chat turn. The rewrite is FR-78/79/80 — Sprint 8 — and needs a **new** figure in Chapter 7, not a redraw of this one. |
| `fig-5-5-use-case-sprint-4` | Document sources are FR-84…87, Sprint 9 → Chapter 7. |
| `fig-5-6-classes-sprint-4` | Same. Its note *"Chunks exist only for published articles"* holds as a Sprint 4 statement; Chapter 7 introduces the second corpus. |
| `fig-5-7-sequence-hybrid-search` | No search commit after the freeze; scoped document retrieval is assistant-side, not public search. |
| `fig-5-8-sequence-publish-pipeline` | The writer's publish path is unchanged. Document ingestion is a **second** background pipeline needing its own Chapter 7 figure, drawn as a companion to this one. |
| `fig-5-9-sequence-notification-delivery` | Structurally unchanged; only enum values were appended. |
| `fig-6-4-activity-eligibility-gate` | Verified in `eligibility.service.ts`: reactions are still `likes + comments`; comment likes and saves are deliberately excluded. |
| `fig-6-5-sequence-moderation` | The `Classifier` participant names no model, so replacing the retired model and dropping the OpenAI path (both 09-04) leave it accurate. |
| `fig-6-6-activity-article-access` | A published licensed article is `placement = public, visibility = free` and falls correctly through the existing public branch. **One branch to confirm:** what a subscribed magazine is shown for a marketplace article another magazine already owns exclusively (FR-72). |

**Totals: 7 REDRAW · 12 AMEND · 14 OK.** Choosing Chapter 7 moved six figures out of
REDRAW and into OK: `fig-4-4`, `fig-5-1`, `fig-5-2`, `fig-5-4`, `fig-5-5`, `fig-5-6`.

### Figures Chapter 7 needs, which have no source at all

Following the set's existing convention of one use case and one class diagram per sprint:

| Proposed figure | Covers |
|---|---|
| `fig-7-1-use-case-sprint-7` | like a comment, follower/following lists, block, save, share (FR-60…65) |
| `fig-7-2-classes-sprint-7` | `CommentLike`, `Save`, `Block`, and the two new notification types |
| `fig-7-3-use-case-sprint-8` | card controls, Reposted tab, recent comments, byline preview, assistant writes, status, voice (FR-66…68, FR-77…83) |
| `fig-7-4-sequence-assistant-turn` | the routing tool on a typed stream, status steps, retrieval, the Markdown reply |
| `fig-7-5-sequence-in-document-write` | the protected range, block-by-block streaming, Keep or Discard as one undo step (FR-79) |
| `fig-7-6-sequence-voice-round-trip` | record ≤ 5 min → transcribe → reply → speak, billed at 200 tokens a minute (FR-82/83) |
| `fig-7-7-use-case-sprint-9` | upload, attach, cite (FR-84…87) |
| `fig-7-8-classes-sprint-9` | `Document`, `DocumentChunk`, `ArticleDocument`, `DocumentStatus` |
| `fig-7-9-sequence-document-ingestion` | upload → register → queue → extract → chunk → embed → ready/failed, with the retry path |

Nine figures. They collapse to six if Sprints 7–9 share one use case and one class diagram,
which is the call to make when the chapter is outlined.

---

## 2. Screenshots — the whole set of 37

**Verdict: recapture all 37, the same way and for the same reason as Phase 6.**

`figures/screens/README.md` already records the precedent: *"the sidebar appears in every
figure, so the WHOLE SET was recaptured in one sitting rather than patched figure by
figure."* That trigger has fired three more times since the 08-23 sitting —
`components/layout/sidebar.tsx` and `nav-items.tsx` gained a nav entry for **Following**
(08-27), **Saved** (09-05) and **Documents** (09-17). Every figure's navigation column is
wrong.

Two shared surfaces changed as well, so this is not only the navigation column:

- **`components/shared/article-card.tsx` changed six times** after the sitting — 08-27
  real counts, 09-05 bookmark, 09-06 live like/repost/comment controls, 09-07 no social
  surface on a listing, 09-08 publication beside the writer, 09-12 straightened card and
  byline preview. It renders in the feed, following feed, search, both profile types,
  saved, reposted and every article list, so `guest-01`, `guest-07`, `guest-08`,
  `guest-09`, `reader-01`, `writer-02` and `magazine-05` change in substance.
- **The assistant was rebuilt three times** — side sheet → floating dock (09-14) → docked
  tabbed panel with a collapsed rail (09-20). `writer-05-ai-panel` and
  `writer-06-ai-answer` photograph a UI that no longer exists, and `writer-03-editor` now
  has the panel docked beside the editor.

### The capture harness is broken, not merely stale

`capture/report-figures.capture.spec.ts` has not been touched since 2026-08-24. Its
`test('the chat panel')` asserts the composer by placeholder:

```ts
page.getByPlaceholder(/ask the ai assistant|no ai tokens remaining/i)
```

`features/ai/ai-assistant-host.tsx:290` now renders one of `'Keep or discard the AI text
first'`, `'No AI tokens remaining'` or **`'Ask, or say what to write…'`**. On a draft with
tokens the match fails and the test stops at its own guard, *"the AI panel opened without
a prompt box"*. Repair the harness before booking a sitting.

### Captures Chapter 7 needs, which the harness does not produce

| Proposed figure | Route / surface | Requirement |
|---|---|---|
| the assistant panel, Chat tab, docked | `/editor/:id` | FR-81 |
| a write awaiting Keep or Discard | `/editor/:id` | FR-79 |
| the live step on the collapsed rail | `/editor/:id` | FR-80/81 |
| the Sources tab with attachments | `/editor/:id` | FR-85 |
| a reply citing `[Title, p. N]` | `/editor/:id` | FR-86 |
| the document library, with one ingesting and one failed | `/dashboard/documents` | FR-84 |
| recording a prompt | `/editor/:id` | FR-82 |
| the saved shelf | `/saved` | FR-64 |
| blocked accounts | `/settings/blocked` | FR-62 |
| the following feed | `/following` | — |
| a follower list with search | `/u/:username/followers` | FR-61 |
| the Reposted tab | `/u/:username` | FR-67 |
| a magazine publishing from its library | `/library` | FR-73/74 |
| a licensed article under the magazine's masthead | `/m/:slug` | FR-76 |

### Prerequisites the sitting still has

The dev database must be the **`full` preset** — a bare `make dci-seed` shrinks it to a
tiny corpus. Embeddings must be backfilled, or the assistant figures show zero passages.
`magazine-03-purchase-confirm` needs an untouched listing, so it needs a fresh seed.
`/editor/:id` is the one figure addressed by id rather than slug, so `draftId` needs
re-reading after any reseed. One open question: whether `GOOGLE_CLIENT_ID` is populated in
the capture environment decides whether `guest-02-login` and `guest-03-register` show the
Google button, which is gated on being configured (08-24).

---

## 3. The hard numbers, and what is actually verified

Four figures assert counts. Measured statically from the trees — **not** from a run:

| Claim | Where | Measured now | At the 2026-08-19 freeze |
|---|---|---|---|
| "479 backend tests" | `fig-3-4`, `fig-6-7` | **51 spec files**, 479 `it(`/`test(` occurrences | **17 spec files**, 187 occurrences |
| "155 Playwright specs, 23 files" | `fig-6-7` | **25 files**, 100 `test(` blocks | — |
| "27 tests" (ledger harness) | `fig-6-7` | **30** `it(` blocks | — |
| "54 user stories in 8 epics" | `fig-1-1` | **72 stories, 9 epics** | — |

**Do not copy the 479 forward.** Today's static occurrence count happens to equal the
figure's number while the suite grew from 17 to 51 spec files — 30 of them added after the
freeze (documents ×4, voice ×4, exclusivity ×2, publish, blocks, comment likes, follow
lists, reposted list and more). A static grep is not what jest reports, so the two numbers
agreeing is coincidence, not corroboration. The report needs **one authoritative run** of
each suite, in the container, and the figures regenerated from its output.

Per the project's own notes: backend tests run inside the container against a `_test`
database, and the jest scripts carry `--experimental-vm-modules` for `pdf-parse`.

---

## 4. Order of work

1. **Settle the Gantt dates** — real submission and defense dates, and S8/S9 bars.
   `fig-2-4` cannot be regenerated without them.
2. **Fix `fig-4-5`'s voice note.** One line, and the only outright false claim in the set.
3. **Measure the suites once**, then regenerate the four counting figures (`fig-1-1`,
   `fig-3-4`, `fig-6-7`) and correct `10-requirements.md:415` and §5's release plan.
4. **Amend the 12 AMEND figures** — all text and label edits, no relayout.
5. **Redraw the 7 REDRAW figures.**
6. **Draw Chapter 7's 6–9 new figures.**
7. **Repair `capture/`**, add the 14 new captures, then recapture all 37 in one sitting
   against a freshly seeded `full` corpus.

Steps 1–5 are the cheap half and unblock Chapters 1–6. Steps 6–7 are Chapter 7's cost.
