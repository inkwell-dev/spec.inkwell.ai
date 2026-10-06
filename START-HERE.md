# START HERE — bringing a new Claude session up to speed on inkwell.ai

For the setup where the four repositories are **cloned and linked to a Claude
Project**. In that setup nothing loads automatically: `CLAUDE.md` auto-loading is
a Claude Code mechanism and a Project does not use it. So the context has to be
handed over deliberately, which is what §5's prompts do.

**How to use this file:** read §1–§4 yourself once, so you can tell whether the
model's answers are right. Then paste §5's prompts in order, grading the answer
to Prompt 4 against the key given there. Do not skip to the work — a session that
starts writing chapters without §4 will confidently reproduce figures that are
already known to be wrong.

---

## 1. The project in one page

**Inkwell.ai is an AI-powered writing marketplace** connecting independent
writers with magazine publishers. Three pillars (`1-product-overview.md` §1):

1. **AI-collaborative writing** — an assistant integrated as chat, voice input
   and inline editing, grounded in the writer's own published corpus and in
   reference documents they upload.
2. **Decision-support analytics** — every published article generates audience,
   content and quality signals that feed dashboards magazines use to evaluate
   talent.
3. **Article licensing marketplace** — magazines are a distinct account type.
   They browse writer profiles, read AI-generated portfolio insights, and license
   existing articles for republication at writer-set prices, paying in credits.

**Eight actors**, and they generalise rather than sitting side by side
(`10-requirements.md` §1): Visitor → Free reader → Premium reader; Writer →
Eligible writer; Magazine unsubscribed → Magazine subscribed; Administrator.
Role and plan are deliberately independent columns — a writer can be on the free
plan and write without AI.

**Stack.** Next.js 16 (App Router) · NestJS 11 · PostgreSQL 16 + pgvector ·
Redis/BullMQ · MinIO · nginx, all under Docker Compose. Groq and Gemini for
completions, embeddings, moderation and speech. Thirty tables, six worker queues.

**It is a PFE engineering report project as much as a product.** The report is
written in English and presents the work as fixed two-week Scrum sprints.

---

## 2. The four repositories

```
docker.inkwell.ai/        PRIVATE   superproject: Docker, nginx, deploy, the ticket skill
├── spec.inkwell.ai/      PUBLIC    submodule — specs, THE REPORT, diagrams, screenshots
└── src/
    ├── backend.inkwell.ai/   PRIVATE  submodule — NestJS API + worker
    └── frontend.inkwell.ai/  PRIVATE  submodule — Next.js app, and capture/
```

**The three inner repos are git submodules, committed as gitlinks (mode
`160000`).** The superproject stores a 40-character commit pointer for each, not
their files — so `docker.inkwell.ai` on its own contains none of the report and
none of the application code, and a clone without `--recurse-submodules` leaves
three empty directories while reporting no error.

Consequences that matter in a Project:

- **Link all four repositories individually.** There is no path from the
  superproject to a submodule's files; each has to be present as itself.
- **Name the repository in your prompts** (`spec.inkwell.ai/10-requirements.md`),
  or the model will search the wrong one of four.
- After pulling a submodule change, the superproject's pointer has to be bumped
  too, or a fresh recursive clone checks out the old commit.

---

## 3. Where to find what

| Looking for | Repo · path |
|---|---|
| the report's own state, decisions and open questions | `spec` · **`REPORT-CONTEXT.md`** |
| the per-figure verdict on all 33 diagrams and 37 screenshots | `spec` · **`FIGURES-AUDIT.md`** |
| requirements, user stories, release plan, the sprint map | `spec` · `10-requirements.md` |
| product overview · features · user flows | `spec` · `1-` · `2-` · `3-*.md` |
| architecture · AI design · database schema | `spec` · `4-` · `5-` · `6-*.md` |
| figure sources, house style, rendering | `spec` · `diagrams/` + its `README.md` |
| the 37 screen captures and what each is for | `spec` · `figures/screens/` + its `README.md` |
| how to run, test or verify anything | `docker` · `.claude/skills/inkwell-ticket/references/environment.md` |
| the product-change pipeline | `docker` · `.claude/skills/inkwell-ticket/SKILL.md` |
| repo map, branches, commits, PRs, code style | `docker` · `.claude/skills/inkwell-ticket/references/conventions.md` |
| tables, enums, services | `backend` · `src/database/schema/*.ts`, `src/*/` |
| routes, UI features, the screenshot harness | `frontend` · `src/app/`, `src/features/`, `capture/` |

The `inkwell-ticket` skill is the authority on process and environment. Prefer it
over any note, memory or summary that disagrees with it — it is versioned with
the code.

---

## 4. The report, in ten lines

- Chapters: **1** methodology · **2** global model · **3** architecture ·
  **4** Sprints 1–2 · **5** Sprints 3–4 · **6** Sprints 5–6 ·
  **7** Sprints 7–9 *(new, decided 2026-10-05, no figures exist yet)*.
- The authority for which sprint a feature belongs to is the **`Sprint` column of
  `10-requirements.md` §2** — not git dates. It attributes a requirement to the
  sprint whose feature it refines.
- The 33 diagrams froze **2026-08-19**, the 37 screenshots **2026-08-23**, the
  capture harness **2026-08-24**. Specs and code ran to **2026-09-21**.
- Audit verdict: **7 diagrams redraw · 12 amend · 14 verified clean**, and
  **all 37 screenshots need recapturing**.
- Chapter 7 additionally needs **9 new diagrams and 14 new captures** that have no
  source at all.
- `fig-4-5` states voice input was descoped and is future work. Voice shipped
  under FR-82/83. It is the one claim in the set a jury could falsify live.
- The capture harness is **broken, not merely stale**: it asserts an AI composer
  placeholder the frontend no longer renders.
- Three counts in `10-requirements.md` are stale: `:415` says *"54 stories, 8
  epics"* against **72 stories and 9 epics**; §5 says *"three releases, six
  sprints"* and stops at Sprint 6; and FR-78's supersession of FR-30 needs saying
  in both Ch.4 and Ch.7.
- Test counts in `fig-3-4` and `fig-6-7` must be re-measured by one real run in
  the container. Do not carry the "479" forward — see `FIGURES-AUDIT.md` §3.
- The two questions that blocked work were answered on 2026-10-06
  (`REPORT-CONTEXT.md` §6): the Gantt covers **2026-02-01 → 2026-07-31**, with no
  submission or defense milestone, and **Google sign-in is configured** for the
  captures.

---

## 5. The prompt ladder

Paste these in order. Each ends by telling the session to stop, so you get
something to check instead of an agent that has already started drawing.

### Prompt 1 — orient

```
Read these three files, in this order, and nothing else yet:

  1. spec.inkwell.ai/START-HERE.md
  2. spec.inkwell.ai/REPORT-CONTEXT.md
  3. spec.inkwell.ai/FIGURES-AUDIT.md

Four repositories are linked to this project: spec.inkwell.ai holds the report,
backend.inkwell.ai and frontend.inkwell.ai hold the code, docker.inkwell.ai is
the superproject. Always name the repository when you cite a file.

Do NOT read the numbered specs (0- through 10-) yet — they are 10,165 lines and
reading them cold wastes the context the writing needs.

Then tell me, in under 200 words: what this project is, where the report stands,
and what is blocking it. Then stop.
```

### Prompt 2 — the product

```
Now read, from spec.inkwell.ai:

  - 10-requirements.md sections 1, 2 and 4 (actors, functional requirements,
    product backlog)
  - 1-product-overview.md section 1

Build me a table of the eight actors and, for each, the two or three
requirements that matter most to them. Flag any requirement whose Sprint column
disagrees with what you would have guessed from its subject. Then stop.
```

### Prompt 3 — the report's shape

```
Now read, from spec.inkwell.ai:

  - diagrams/README.md
  - figures/screens/README.md
  - 10-requirements.md section 5 (the release plan)

Then produce the chapter-by-chapter figure inventory: for each of chapters 1-7,
which figures exist, which the audit marks redraw or amend, and which do not
exist yet. Mark every place where section 5's release plan contradicts the
Chapter 7 decision recorded in REPORT-CONTEXT.md. Then stop.
```

### Prompt 4 — the check

```
Answer from what you have read, without reading anything further:

  1. How many diagrams need a full redraw, and why is fig-5-4 not one of them?
  2. How many tables does the database have, and how many do the two global
     class diagrams account for?
  3. How many worker queues does fig-3-2 draw, and how many exist?
  4. What exactly is wrong with the screenshot capture harness?
  5. What two questions blocked the report, and how were they answered?
```

**Key — grade it against this.** If question 1 or 4 is wrong, the files did not
load properly; stop and fix that before going on.

1. **Seven.** `fig-5-4` is clean because the assistant rewrite it would seem to
   contradict is FR-78/79/80, which belong to **Sprint 8** — so `fig-5-4` remains
   the accurate record of the Sprint 4 chat turn, and Chapter 7 gets a new figure
   instead. (A per-sprint figure is judged only against its own sprint.)
2. **30 tables; the diagrams account for 24.** Missing: `comment_likes`,
   `blocks`, `saves`, `documents`, `document_chunks`, `article_documents` — plus
   `articles.publisher_id` on an existing class.
3. **Four drawn, six exist** — `embeddings`, `analytics`, `marketplace`,
   `ai-tokens`, plus `documents` and `ai-models`.
4. It asserts the AI composer by the placeholder
   `/ask the ai assistant|no ai tokens remaining/i`, but
   `frontend.inkwell.ai/src/features/ai/ai-assistant-host.tsx` now renders
   `'Ask, or say what to write…'`. The test fails its own guard and writes no
   file.
5. The Gantt dates — answered as **2026-02-01 → 2026-07-31**, with no
   submission or defense milestone on the chart; and whether Google sign-in is
   configured — **it is**, so the login and register captures show the button.

### Prompt 5 — begin

```
Good. Start on the cheap half, in the order FIGURES-AUDIT.md section 4 gives:

  1. Fix fig-4-5's voice note — reword it as a forward reference to Chapter 7
     rather than a claim that voice is future work.
  2. Then the remaining AMEND figures, which are all label and note edits.

Work one figure at a time. For each, show me the exact diff to the .puml or
generator source and the code path or requirement id that justifies it, and wait
for my go-ahead before the next one. Do not render anything — rendering needs
Docker and happens on the Linux machine.
```

---

## 6. Rules the session must respect

- **Never name an assistant.** No `Co-Authored-By`, and no mention of Claude,
  Copilot, ChatGPT or "AI-generated" in any commit message, PR title or body,
  changelog entry or code comment. The user is the sole author of every commit.
  In a Project there is no hook enforcing this, so it is held by hand.
- **Cite, do not recall.** Every claim about product behaviour in a chapter names
  the spec section or the code path it came from. Copies that drifted are this
  report's entire current problem.
- **Nothing verifies host-side.** `node_modules/` is an empty docker volume mount
  in both app repos, so a lint, typecheck or test run outside the container has
  silently not run and will report success anyway.
- **A figure is judged against the code, not the specs.** The specs are
  reconciled after the fact and carry their own drift.
- **Rendering and screenshots need Docker.** `make` in `diagrams/` renders SVG;
  the capture sitting needs the stack, the `full` seed and Playwright. Neither is
  possible from a Project — keep both on the machine that runs the stack.

---

## 7. If you are in Claude Code instead of a Project

Then most of this is automatic. Launch from `docker.inkwell.ai/` — not its
parent, or `.claude/skills/` is never discovered and the `inkwell-ticket` skill
and the five hookify rules beside it stay silent, including the one that blocks a
commit naming an assistant. `CLAUDE.md` then loads at the root, and
`spec.inkwell.ai/CLAUDE.md` imports `REPORT-CONTEXT.md` when you work in the spec
repo. You can still paste §5's ladder; Prompts 2–5 are useful either way.
