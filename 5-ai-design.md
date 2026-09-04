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

---

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

The voice system follows this pipeline:

- Audio Input  
- Speech-to-text processing  
- Cleaned transcription  
- Prompt construction  
- AI generation  
- Structured article output  

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
- Retrieved via cosine similarity for:
  - Writer-facing chat (top-K chunks from the writer's own articles, K ≤ 5)
  - Magazine-facing Portfolio Insights (representative chunks across writer's corpus)
- **Chunk lifecycle**: on article publish or update, existing chunks for that article are **deleted and re-created** (the `(article_id, chunk_index)` unique constraint requires delete-before-insert on updates)
- **Cache invalidation**: publishing or updating an article also invalidates the writer's `portfolio_insights` cache (if one exists)  

---

## 10. AI Usage Control

### 10.1 Token System

- Each AI request consumes tokens  
- Users have a daily token limit  

---

### 10.2 Limits

- Prevent excessive usage  
- Control operational cost  

---

### 10.3 Additional Tokens

- Users can acquire more tokens (simulated in MVP)  

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
  > Worth keeping as a lesson: this claim was load-bearing for four documents and
  > went stale in five weeks. Provider free-tier limits are not measured once.
- Return user-facing fallback message ("AI is temporarily unavailable")
- Log errors to Sentry for monitoring
- Non-AI features continue working during AI provider outages  

---

## 12. Performance Considerations

- Limit context size to reduce latency  
- Use asynchronous processing when needed  
- Cache repeated AI responses (optional)  

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
| Speech-to-text | — | — | **Never built.** *Recorded 2026-09-04:* no `whisper`, `speech` or transcription call exists anywhere in the backend. The `voice_transcribe` value survives in the `ai_action_type` enum (`database/schema/enums.ts`) and nothing ever writes it. The row previously read "**Groq Whisper-large-v3-turbo** / OpenAI Whisper API". |
| Embeddings (RAG) | **Gemini `gemini-embedding-001`** | — | Free tier, no payment method required. Emits **1536 dimensions** via `outputDimensionality`, matching the original OpenAI width so the schema is unaffected. |
| Content moderation | **Groq `groq/compound-mini`** | — | Free. *Updated 2026-09-04:* OpenAI has been **removed**, not merely left unconfigured — its `/v1/moderations` endpoint is free but gated behind a non-empty credit balance, so the key cannot work on a free-tier project and the code path could never run. The classifier was also `llama-3.1-8b-instant` until Groq retired it, which silently disabled moderation entirely (the chain fails open, so a dead provider and a clean verdict are indistinguishable). `npm run models:check` and a daily worker job now call every model id so a third retirement is visible. |
| Premium AI (optional) | — | — | **Never built.** *Recorded 2026-09-04:* no Anthropic dependency, key or call exists in the codebase, and there is no paid budget. Premium accounts differ by AI token allowance, not by model. The row previously read "**Anthropic Claude** — small paid budget for higher-quality premium actions". |

Provider abstraction is implemented via **Vercel AI SDK** in the NestJS backend, allowing one-line provider swaps.

---

## 14. Future Enhancements

- Real-time voice interaction  
- Advanced style learning  
- Multi-language generation  
- AI-driven article scoring  
- Context-aware semantic search  

---

## Summary

The AI system is designed as a context-aware, adaptive assistant that enhances the writing experience through:

- Structured interactions  
- Intelligent prompt design  
- User-specific personalization  
- Scalable architecture  

It transforms the platform from a traditional editor into an AI-powered content creation environment.
