# 05 - AI Design

## 1. Overview

This document defines the architecture, behavior, and integration of AI within Inkwell.

The AI system serves **two distinct audiences** with overlapping infrastructure:

1. **Writer-facing AI** — co-writer, editor, and assistant integrated into the creation workflow
2. **Magazine-facing AI** — generates Portfolio Insights reports that help magazines evaluate writers before licensing

Both surfaces share the same RAG pipeline over each writer's published corpus — this is the technical leverage point that makes the AI investment justify itself twice.

AI is not a bolt-on feature; it is a core system layer that enhances:
- Writing
- Editing
- Structuring
- Feedback
- Writer evaluation (for the marketplace)

---

## 2. AI System Objectives

The AI system must:

- Assist users in writing high-quality articles  
- Reduce time required to produce content  
- Adapt to user writing style over time  
- Provide contextual and relevant suggestions  
- Maintain consistency within articles  

---

## 3. AI Roles

The AI operates in multiple roles depending on the context:

### 3.1 Writer
- Generates content from prompts or voice input
- Produces structured articles (sections, paragraphs)

### 3.2 Editor
- Improves existing content
- Rewrites, shortens, expands, or simplifies text

### 3.3 Assistant
- Answers user questions
- Suggests ideas or improvements
- Helps with structure and flow

### 3.4 Coach (Basic in MVP)
- Provides feedback on writing quality
- Detects weak sections (e.g., long paragraphs, weak introduction)

### 3.5 Evaluator (Magazine-Facing) — *New role*
- Analyzes a writer's full corpus on demand
- Produces a structured Portfolio Insights report (voice, expertise, consistency, fit, strengths/gaps)
- Drives magazine preview and purchase decisions  

---

## 4. AI Interaction Types

### 4.1 Chat-Based Interaction

- User interacts with AI via a chat panel  
- AI receives full article context  
- Used for:
  - Content generation  
  - Questions  
  - Suggestions  

---

### 4.2 Inline Editing

Triggered when user selects text.

Actions include:
- Reformulate  
- Shorten  
- Expand  
- Simplify  
- Improve engagement  

---

### 4.3 Voice-to-Article

> **Descoped to post-MVP** (2026-07-26 re-baseline — see [`0-phase-plan.md`](./0-phase-plan.md)). Pipeline design retained for future work.
>
> *2026-09-15:* what shipped instead is the **voice prompt** — the writer
> dictates a request to the assistant, not an article (§5.2). The transcription
> engine is the one named below; the "LLM structures the transcript into
> sections" step is still not built.

Flow:
- User records speech
- Speech is transcribed via **Groq Whisper-large-v3-turbo** (free tier, fast)
- LLM structures the transcript into article sections
- Result inserted into the TipTap editor

---

### 4.4 Portfolio Insights (Magazine-Facing) — *New*

**Access requirement**: active magazine subscription. The endpoint returns 403 for non-subscribed or unauthenticated requests.

Triggered when a subscribed magazine opens a writer's evaluation page.

Flow:
- Backend retrieves the writer's `article_chunks` (RAG)
- Constructs a structured prompt requesting voice / topics / consistency / fit / strengths-gaps
- LLM generates a typed report (Zod-validated structure)
- Report cached for 24 hours (`portfolio_insights` table) or invalidated on new publication

Output format (structured):
- `voice_summary` (string)
- `topic_expertise` (string[])
- `consistency_score` (0-100)
- `suggested_use_cases` (string[])
- `strengths_gaps` (string)  

---

## 5. AI Request Lifecycle

All AI orchestration runs inside the NestJS backend — there is no separate AI service. The Vercel AI SDK provides a unified TypeScript interface for all providers.

Each AI request follows this pipeline:

1. User action (chat, selection, voice)  
2. Frontend sends request to backend  
3. Backend enriches request with:
   - Article context (current content)
   - Structured memory (tone, style, vocabulary, topics from `user_ai_memory`)
   - RAG retrieval (top-K relevant chunks from writer's published articles, capped at 5)
4. Backend builds prompt (ROLE + CONTEXT + TASK + INPUT)
5. Vercel AI SDK calls external provider (Groq primary, Gemini fallback)
6. Response streamed back to frontend via SSE (`streamText`)

   *Corrected 2026-09-14.* For the editor assistant (`POST /ai/chat`) the
   response is no longer a plain text stream. It is an AI SDK **UI-message
   stream** carrying typed parts — status for each stage, the text of an
   answer or recap, and the article being written — and step 3's RAG
   retrieval runs only when the model has decided to write. See §5.1. The
   inline actions (`POST /ai/inline`) still stream plain text.

### 5.1 The assistant turn (2026-09-14)

One request, one typed stream. The model **decides** whether a reply belongs in
the document or in the panel, through a single tool:

```
write_to_article({ placement: 'cursor' | 'replace_selection', brief: string })
```

The outer call carries a lean prompt (guidelines, the current article, the
style profile) and the tool. A question is answered as text — one call, no
retrieval. A request to produce or change article text makes the model call the
tool; the tool's `execute` runs the full generation path (article, style
profile, **retrieved passages** for the brief) as an inner call and forwards
every chunk to the client; it returns word and heading counts, and the outer
model continues with a one-line **recap** grounded in them.

**Parts on the stream** (`data-*` parts are transient — delivered to the client,
never persisted into the message history):

| Part | Payload |
|---|---|
| `data-status` | `{ step, state, detail?, chunks? }` — `step ∈ draft \| profile \| documents \| thinking \| retrieval \| writing \| done`, `state ∈ active \| done \| failed`; retrieval's `done` carries the passages. *`documents` added 2026-09-17 (§9.5) — emitted only when the article has attached, `ready` documents.* |
| `text` | the answer, or the recap after a write |
| `tool-write_to_article` | the decision (`placement`, `brief`) |
| `data-article-start` | `{ id, placement, brief }` — the client opens its insertion range |
| `data-article-delta` | `{ id, text }` — plain-text chunk of the article |
| `data-article-done` | `{ id, words, headings }` — written even when the inner stream fails, so the client can always close the range |

**Step order is the order the work happens**: draft → profile →
*(documents)* → thinking → *(retrieval → writing, only for a write)* → done.
Retrieval sits after thinking because the embedding search is the slowest
stage and only a write needs it. `documents` sits earlier, between `profile`
and `thinking`, and runs for both a question and a write *(2026-09-17, §9.5)*
— it is emitted only when the article has attached, `ready` documents, and it
has to come before routing because a question about the material needs it
just as much as a write does, unlike the voice-corpus `retrieval` step below,
which only a write reaches. No "web research" step exists because no web
research exists.

**Thinking** is the span from sending the outer request to the first visible
token or tool call. gpt-oss's reasoning parts are not forwarded to the client.

**Failure** is an `error` part on the open stream carrying "AI is temporarily
unavailable" when no model in the chain answers, and a `failed` status on the
stage that broke otherwise. The old 503-before-first-byte cannot survive here:
the pre-model stages are streamed live, so the response is open before a model
is chosen.

**Billing** sums both calls' total tokens into one `ai_interactions` row whose
`output_text` is the article when a write happened, else the answer. A Stop
mid-write bills an estimate — inner prompt plus text produced so far, at ~4
characters per token — because `onFinish` does not fire on abort and a Stop one
sentence before the end must not make the article free.

**Request body** gains `selection?: { text }` (≤ 6,000 characters) — the text of
the whole top-level block(s) the selection touches, since a rewrite always
replaces whole blocks; the inner prompt bounds the output to that passage.
Document positions never leave the client.

---

### 5.2 Voice in, voice out (2026-09-15)

Two small routes beside the assistant turn; the chat stream is untouched.

**`POST /ai/transcribe`** — the recorded prompt. Multipart `audio` (what
`MediaRecorder` produces: WebM/Opus, Ogg, MP4/AAC, WAV) plus a required
`seconds` field. Guards: JWT and the AI quota guard. Limits: **5 minutes** and
**10 MB**, either → `413` "Recording too long (max 5 minutes)" (multer's own
size rejection is rewritten to the same sentence by a route-scoped filter).
Whisper (`whisper-large-v3-turbo`, Groq) returns the text; the response is
`{ text, seconds, tokensUsed }`. Provider failure → `503` "Couldn't transcribe
— try again". A transcript of silence is `""` — and still billed, since the
call happened.

*Billing.* A minute of audio costs **200 tokens**, rounded up, never below one
minute. Groq reports no duration, so the figure billed is
`max(clientSeconds, bytes / 32 000)` — the client's claim, floored by what the
file size proves at 256 kbps, above anything a browser recorder emits (Chrome's
Opus default is 128 kbps plus container overhead, which is why 128 was not
enough of a ceiling). Logged as
`voice_transcribe` with `input_text = "[voice] <seconds>s"` and the transcript
as `output_text`.

**`POST /ai/speak`** — `{ text }` (≤ 1,000 characters, Markdown already
stripped by the client) → `audio/wav`, `Cache-Control: no-store`. Gemini TTS
(`gemini-2.5-flash-preview-tts`, voice *Kore*). JWT only, **free to the
writer**, limited **per user** to 20 a minute and 300 a day (in-process,
sliding windows — the route's IP throttle alone would let one office NAT
exhaust it for everyone), so a loop cannot spend the key's daily allowance.
Not logged. Any failure → `503`, and the client is silent
about it.

**`GET /ai/speech-availability`** → `{ available }`: true when the Gemini key
is configured **and** a one-time probe (speaking the word "ready") succeeded.
Both outcomes are memoised for the life of the process. This flag alone
decides whether the mute button exists; there is no browser-voice fallback.

**In the dock.** A microphone beside the input records; a check mark sends the
audio and the transcript lands in the input, editable — nothing is sent until
Enter. The mic is refused below one minute's worth of tokens and while the
input is disabled for any other reason. Every settled assistant reply is read
aloud unless the writer has muted it (a button left of the minimize control,
remembered per browser, default unmuted); a stopped or failed reply is never
spoken.

## 6. Context Management

AI responses depend heavily on context.

### 6.1 Context Sources

- Full article content  
- Selected text (if applicable)  
- User writing history  
- Action type (rewrite, expand, etc.)  

---

### 6.2 Context Strategy

- Include only relevant sections to avoid token overflow  
- Prioritize:
  - Current section  
  - Recent edits  

---

## 7. Prompt Engineering

### 7.1 Structure

Each prompt follows a structured format:

- ROLE: Defines AI behavior  
- CONTEXT: Article + user data  
- TASK: Specific instruction  
- INPUT: User text  

---

### 7.2 Example

- ROLE: Professional editor  
- CONTEXT:
  - Article topic: Surfcasting  
  - Style: Informative  
- TASK:
  - Rewrite the paragraph to be more engaging  
- INPUT:
  - "Original paragraph text..."  

---

### 7.3 Prompt Optimization

- Keep prompts concise  
- Avoid unnecessary context  
- Use clear instructions  
- Enforce output structure  

---

## 8. Voice Processing Pipeline

*Corrected 2026-09-15.* The pipeline that ships is the voice **prompt** (§5.2):

- Audio input (`MediaRecorder`, ≤ 5 minutes)
- Speech-to-text (Groq Whisper)
- Transcript into the assistant's input box, editable
- The writer sends it — the assistant turn (§5.1) does the rest
- The reply is read aloud (Gemini TTS) unless muted

The structured-article generation the pipeline used to end with (transcript →
sections → draft) remains descoped.

---

## 9. AI Memory System

### 9.1 Scope
- Memory is stored per user with a **structured schema** (not a JSON blob)

### 9.2 Stored Fields
See [`6-database-schema.md`](./6-database-schema.md) section 5.3 — `user_ai_memory`:
- `tone_preferences` (formality, energy, persona)
- `style_examples` (array of representative excerpts from the writer's articles)
- `vocabulary_patterns` (common terms, phrasing patterns)
- `topics` (domains the writer covers)

### 9.3 Usage
- Injected into prompts for writer-facing AI calls as a compact system-prompt block
- Used as input to Portfolio Insights generation
- Refreshed by a background job when the writer publishes a new article

### 9.3.1 Memory Extraction Pipeline

Structured memory is **not user-entered** — it is extracted automatically by an LLM job:

1. Writer publishes or updates an article
2. BullMQ triggers `extract-writer-memory` job
3. Job retrieves the writer's full published corpus (or a representative sample)
4. LLM call with a structured prompt requesting tone/style/vocabulary/topics analysis
5. Response validated via Zod schema matching `user_ai_memory` fields
6. Upsert into `user_ai_memory` table (creates on first publish, updates on subsequent)

The extraction runs asynchronously — it does not block the publish flow. If the LLM call fails, the existing memory (or empty memory for first-time writers) is used until the next successful extraction.

### 9.3.2 Prompt Size Management

To avoid token overflow from double-injecting memory and RAG chunks:
- Structured memory is injected as a **compact system-prompt block** (< 200 tokens)
- RAG retrieval is capped at **top-K ≤ 5 chunks**
- Total injected context (memory + chunks) should not exceed ~2000 tokens

### 9.4 RAG Layer (Article Chunks)
- Articles are split into paragraph-level chunks on publish
- Each chunk embedded with **Gemini `gemini-embedding-001`** at **1536 dimensions**
  (`outputDimensionality: 1536`). *Substituted for OpenAI `text-embedding-3-small`
  on 2026-08-10 — see the provider table in §13.5 for why. The width is
  deliberately unchanged, so the schema and the HNSW index were untouched.*
- Stored in `article_chunks` with HNSW vector index in pgvector
- **Chunk bounds, and why they are not the model's.** A block below **120
  characters** is merged forward into the next rather than embedded — "Yes."
  produces an embedding dominated by two tokens and matches almost nothing, and
  discarding it would lose prose that is often the punchline of the paragraph
  before. A block above **1200 characters** is split. That ceiling is *not* a
  model limit (the embedding endpoint accepts 8191 tokens); it is a retrieval
  ceiling, because one vector has to represent the whole chunk and a long chunk
  averages several ideas into a point that matches none of them sharply.
- **Each chunk is prefixed with its nearest preceding heading**, and the prefix
  is stored in `content` rather than merely used for the vector. A paragraph
  reading "It rarely works below 8°C" is nearly meaningless alone; prefixed with
  its heading it embeds near the subject it is about — and the model benefits
  from the same context the vector did.
- Retrieved via cosine similarity for:
  - Writer-facing chat (top-K chunks from the writer's own articles, K ≤ 5)
  - Magazine-facing Portfolio Insights (representative chunks across writer's corpus)
- **A similarity floor of `0.60`, measured rather than chosen** *(added
  2026-09-10; the value has been in the code since 2026-08-10 and was never
  written down here).* Vector search always returns its K nearest neighbours —
  there is no "no results" — so without a floor, asking a fermentation writer
  about tides returns five fermentation chunks and the model treats them as
  relevant background. That is worse than no retrieval, because it misleads.

  > The floor started at `0.35` and filtered nothing, because
  > `gemini-embedding-001` does not use the full [0,1] range: two texts on
  > entirely unrelated subjects still score around 0.5. Measured against this
  > corpus on 2026-08-10 — **on-topic 0.63–0.73, off-topic 0.48–0.58** — so 0.60
  > sits in the gap. Verified by asking a fermentation writer a surfcasting
  > question: at 0.35 it injected five irrelevant chunks scoring 0.52–0.55; at
  > 0.60 it correctly injects nothing.
  >
  > **The number belongs to the model, not to similarity in general.** A
  > threshold tuned for one embedding model is meaningless for another, so a
  > model change requires re-measuring. `retrieval.service.ts` says the same at
  > the constant.
- **Chunk lifecycle**: on article publish or update, existing chunks for that article are **deleted and re-created** (the `(article_id, chunk_index)` unique constraint requires delete-before-insert on updates)
- **Cache invalidation**: publishing or updating an article also invalidates the writer's `portfolio_insights` cache (if one exists)  

---

### 9.5 Document sources (2026-09-17)

A **second, independent corpus**, sitting beside the article-chunks RAG above
and never mixing with it. §9.4 answers "does this sound like the writer" from
the writer's own published work; this corpus answers "what does the material
the writer attached actually say" from documents they chose to upload. It is
**reference material**, not voice — the opposite instruction from the block
above — but it reuses the chunker, the embedder and the query pattern
verbatim.

**Tables** (full column definitions in `6-database-schema.md` §5.5–5.7):
`documents` — one row per upload, `status` enum `document_status` stepping
`pending` → `extracting` → `ready` | `failed`; `document_chunks` — the same
shape as `article_chunks` (`chunk_index`, `page`, `content`, `embedding
vector(1536)`), so `findSimilarDocumentChunks` reuses the pgvector query
pattern of the writer-corpus lookup; `article_documents` — the attach join,
one row per article–document pair, "attached to this article."

**Storage.** A private MinIO bucket, `documents`, created at boot like the
images bucket but **without** the anonymous-read policy. Upload is a
presigned PUT; download is `GET /documents/:id/file`, which returns a
presigned GET valid **600 seconds**, owner-only. No public URL for a document
ever exists.

**Ingestion** runs as `ingest-document` on its own BullMQ queue, `documents`
— separate from article embedding so a slow PDF never delays it. The worker
steps `pending` → `extracting` → extract by type (**PDF** via `pdf-parse`,
per page; **DOCX** via `mammoth`, one page throughout — DOCX has no fixed
pages to derive one from; **TXT/MD** as UTF-8) → chunk with the same rules as
§9.4 (120–1,200 characters, thin blocks merged forward) through a new
`chunkText`, which keeps the page a chunk starts on → embed
(`gemini-embedding-001`, `RETRIEVAL_DOCUMENT` — unchanged from §9.4, see
§13.5) → `ready`, with `page_count` and `chunk_count` set. Caps: **20
documents per writer**, **10 MB**, **200 pages**. Writer-readable failure
sentences:

- Under a **50-character** text floor after extraction: "This PDF has no
  text layer — export it with selectable text."
- Over **200 pages**: "Documents are limited to 200 pages".
- Any other extraction or embedding failure: "Couldn't process this document
  — try again."
- A 21st document: `409` "You already have 20 documents".

A delete soft-deletes the row — retrieval stops at once — then enqueues
`purge-document`, which removes the MinIO object and hard-deletes the row,
cascading chunks and attachments.

**Retrieval.** `RetrievalService.findSimilarDocumentChunks(query, { ownerId,
documentIds, topK = 5, minSimilarity = 0.60 })` embeds the writer's message as
`RETRIEVAL_QUERY`, exactly like the voice lookup, and scopes the `<=>` query
to `owner_id = caller`, `id IN attached`, `status = 'ready'`,
`deleted_at IS NULL`. It runs **before the routing call**, for **both**
questions and writes — a question about the material needs it as much as a
write does, unlike the voice passages above, which stay write-only. The
`0.60` floor is carried over from §9.4 rather than re-derived, and the plan's
spike measured it on this corpus rather than assumed it transfers: **on-topic
0.606–0.738, off-topic 0.436–0.488**, measured 2026-09-17 on uploaded
reference text — the same gap shape as the article corpus, so the floor holds
unchanged. An attached document still `extracting` at send time is skipped
for that turn.

**Prompt block**, distinct from the voice block and carrying the opposite
instruction:

> Reference material the writer attached. Use it for facts and structure; do
> not imitate its style. When you use a passage, cite it inline as [Title,
> p. N].

Each passage is prefixed `[Title, p. N]` (or `[Title]` for DOCX/text).

**Status step.** `documents` is a new step in `CHAT_STEPS`, on both the
backend and the frontend copies, inserted **between `profile` and
`thinking`** — earlier than the write-only `retrieval` step in §5.1, because
a question never reaches that step and needs the material just as much as a
write does. Emitted only when the article has attached, `ready` documents.
The run card gains a row **"Reading your documents — N passages from M
documents"**, expandable to the passages used; each passage is a link that
calls `GET /documents/:id/file` on click and opens the returned presigned URL
with `#page=N` appended in a new tab (a plain `href` cannot carry a URL that
expires in 600 seconds).

**Citations.** The model's inline citation stays in the text: `[Title, p. N]`
for PDFs, `[Title]` for DOCX and TXT/MD, which have no page to cite.

**Cost.** ≤ 5 passages ≈ 1,500 prompt tokens, billed in the turn like the
voice passages above — free to upload, not free to use.

**Scope.** Every route filters on `owner_id`; a mismatch is `404`, never
`403`, so a document's existence is not observable from outside its owner.
Documents never feed **writer memory** (§9.1–9.3), **Portfolio Insights**
(§4.4), or **search** — they are the writer's material, not the writer's
work, and none of the three treats an uploaded document as if it were.

---

## 10. AI Usage Control

### 10.1 Token System

- Each AI request consumes tokens
- Users have a daily token limit, granted per plan

*Pinned to the implementation 2026-09-10 — this section described the mechanism
without ever naming a number, which made it unfalsifiable:*

| Plan | Daily AI tokens |
|------|-----------------|
| Free | **0 — no AI access at all** |
| Premium | **20,000** |

> **Raised 2026-09-12, from 1,000.** A token here is a *total* token — input and
> output combined (see `9-implementation-guide.md` §2.4) — and a chat turn's
> input carries the system prompt, up to ~1,500 tokens of the current article,
> the retrieved passages, the style profile and the whole conversation replay.
> One article-length reply therefore cost the entire 1,000, and the first
> premium writer to try the assistant found it "very low" after a single
> answer. 20,000 is about twenty long replies or sixty inline edits — a
> working day. Billing stays on total tokens deliberately, so the cost of prompt
> context remains visible rather than hidden by counting output alone.
>
> *2026-09-15:* a **recorded prompt** draws on the same allowance at **200
> tokens per minute of audio**, rounded up and never below one minute (§5.2).
> Spoken replies are free to the writer.

The free-plan zero is a product decision rather than a missing constant: AI
access *is* the premium tier. There is deliberately no constant for it, because
the absence of an allowance is the rule and not a tunable number.

---

### 10.2 Limits

- Prevent excessive usage
- Control operational cost

**The allowance is rewritten, not incremented.** A nightly worker job sets
`users.ai_tokens_remaining` to the plan's figure; it does not add to whatever was
left. Unspent tokens therefore do not accumulate, which is what keeps the daily
cap a cap.

The quota is checked by a guard that runs **before** the model call, so an
exhausted account costs nothing.

**A low balance can be overdrawn, by design.** The guard only asks whether the
balance is above zero; the reply then runs to completion and the decrement
clamps at zero (`GREATEST(0, remaining − used)`). So a writer with 50 tokens
left gets a whole answer, not 50 tokens of one, and ends the day at 0. The
alternatives — capping the reply at the remaining balance, or refusing to send
below a reserve — both trade a complete answer for bookkeeping neatness, and a
reply that stops mid-sentence is worse than a balance that reads 0 a little
early. What the writer *is* owed is to be told: the chat panel shows a notice
inside the conversation, under the reply that spent the balance, saying so and
naming the reset time. *(Recorded 2026-09-12; the behaviour predates the note.)*

---

### 10.3 Additional Tokens

> **Corrected 2026-09-10. This section said "Users can acquire more tokens
> (simulated in MVP)". No such thing exists, and it was deliberately not built.**
>
> The daily reset rewrites `ai_tokens_remaining` to a fixed per-plan allowance
> rather than adding to it, so tokens bought at noon would be erased at midnight.
> Shipping a purchase that silently expires within hours is worse than not
> offering one. Making it work needs a second column the reset does not touch —
> a design decision, not an implementation gap, and one nothing has asked for.
>
> **Magazine *credit* top-up is a different thing and does work** (§4.5.1). Credits
> are a ledger balance and never rewritten, which is precisely why top-up is
> coherent there and not here.

---

## 11. Error Handling and Reliability

### 11.1 Failure Cases

- External AI provider unavailable or rate-limited
- Timeout from external API  
- Invalid or malformed LLM responses (fails Zod validation)
- Embedding provider quota exhausted or key absent

---

### 11.2 Handling Strategy

- Retry failed requests (Vercel AI SDK built-in retry)
- **Provider failover**: `openai/gpt-oss-120b` → `openai/gpt-oss-20b` →
  `gemini-3.5-flash`. The first two are Groq, so a single model being rate-limited
  is absorbed without leaving the provider; Gemini is reached only when Groq as a
  whole refuses. Gemini `gemini-embedding-001` remains the sole embedding
  provider (free tier, no card required), with no fallback of its own.

  > **Corrected 2026-08-24, restored 2026-09-03.** The 2026-08-24 note recorded
  > that the specified Groq → Gemini chain was never implemented and **could not
  > be**, because Gemini's free tier granted `generateContent` a quota of 0 on
  > every model offered to new projects. That was accurate when measured. It is no
  > longer: re-measured 2026-09-03 against the project's current key,
  > `generateContent` answers 200, and the chain is now built — see `llm-chain.ts`
  > for the ordering rule and NFR-24 for the evidence.
  >
  > Two things survive the reversal. The model id here is **not** the
  > `gemini-2.0-flash` of §13.5, which now 404s. And provider-level resilience
  > stops at *one* provider being down: Groq and Gemini failing together still
  > yields 503, and no free-tier arrangement changes that.
  >
  > *2026-09-14:* for `POST /ai/chat` the total outage is now an `error` part on
  > an already-open stream, with the same copy — see §5.1. `POST /ai/inline`
  > still returns the 503.
  >
  > Worth keeping as a lesson: this claim was load-bearing for four documents and
  > went stale in five weeks. Provider free-tier limits are not measured once.
- Return user-facing fallback message ("AI is temporarily unavailable")
- Log errors to Sentry for monitoring
- Non-AI features continue working during AI provider outages  

---

## 12. Performance Considerations

- Limit context size to reduce latency
- Use asynchronous processing when needed — embedding runs on a queue, so
  publishing never waits for an embedding API
- Cache repeated AI responses *(partially: **Portfolio Insights** are cached in
  their own table with an expiry, and invalidated when the writer publishes or
  edits. Chat and inline edits are **not** cached — they are conversational and a
  cache hit would be a wrong answer to a different question.)*

---

## 13. Security and Safety

- Validate all user inputs  
- Prevent prompt injection  
- Filter harmful or inappropriate outputs  

---

## 13.5 AI Providers (Free-Tier First)

| Capability | Primary Provider | Fallback | Notes |
|------------|------------------|----------|-------|
| LLM (chat, inline edit, Portfolio Insights) | **Groq** (`openai/gpt-oss-120b`, then `openai/gpt-oss-20b`) | **`gemini-3.5-flash`** | Both free tiers. *Updated 2026-09-03: Llama 3.3 70B and Gemini 2.0 Flash are both retired — the ids here are the ones verified by invocation. Portfolio Insights does **not** use this chain; it pins `openai/gpt-oss-120b` for `json_schema` support.* |
| Speech-to-text | **Groq `whisper-large-v3-turbo`** | — | *Built 2026-09-15* (§5.2), for the voice prompt. `voice_transcribe` is now written by `POST /ai/transcribe`. The 2026-09-04 note recorded that nothing existed then. |
| Text-to-speech | **Gemini `gemini-2.5-flash-preview-tts`** (voice *Kore*) | — | *Built 2026-09-15* (§5.2). Free tier; availability probed once per process and the feature hidden when the key cannot speak. No browser-voice fallback by decision. |
| Embeddings (RAG) | **Gemini `gemini-embedding-001`** | — | Free tier, no payment method required. Emits **1536 dimensions** via `outputDimensionality`, matching the original OpenAI width so the schema is unaffected. *Unchanged for document sources (§9.5, 2026-09-17)* — the same model and width also embed `document_chunks`; no separate provider or dimension for the second corpus. |
| Content moderation | **Groq `groq/compound-mini`** | — | Free. *Updated 2026-09-04:* OpenAI has been **removed**, not merely left unconfigured — its `/v1/moderations` endpoint is free but gated behind a non-empty credit balance, so the key cannot work on a free-tier project and the code path could never run. The classifier was also `llama-3.1-8b-instant` until Groq retired it, which silently disabled moderation entirely (the chain fails open, so a dead provider and a clean verdict are indistinguishable). `npm run models:check` and a daily worker job now call every model id so a third retirement is visible. |
| Premium AI (optional) | — | — | **Never built.** *Recorded 2026-09-04:* no Anthropic dependency, key or call exists in the codebase, and there is no paid budget. Premium accounts differ by AI token allowance, not by model. The row previously read "**Anthropic Claude** — small paid budget for higher-quality premium actions". |

Provider abstraction is implemented via **Vercel AI SDK** in the NestJS backend, allowing one-line provider swaps.

---

## 14. Future Enhancements

- Real-time voice interaction
- Advanced style learning
- Multi-language generation
- AI-driven article scoring
- ~~Context-aware semantic search~~ — **shipped.** Search runs a lexical
  ranking and the vector retrieval above concurrently and fuses them by
  reciprocal rank fusion on *position*, because `ts_rank` and cosine similarity
  are incomparable scales. Moved out of this list 2026-09-10; it had been sitting
  here as an aspiration while the feature was live.

---

## Summary

The AI system is designed as a context-aware, adaptive assistant that enhances the writing experience through:

- Structured interactions  
- Intelligent prompt design  
- User-specific personalization  
- Scalable architecture  

It transforms the platform from a traditional editor into an AI-powered content creation environment.
