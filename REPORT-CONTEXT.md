# The PFE report — context for a cold session

Read this before touching the report. It exists because the report's state lived
only in a conversation on one laptop, and conversations do not travel between
machines. This file does.

It is deliberately **pointers, not copies**. Where another committed file already
holds the truth, this one links to it rather than restating it, because two
copies of a fact are two facts that can disagree — which is the exact failure
this report is currently recovering from (see §4).

**Read order for a cold session**

1. this file, end to end — about ten minutes
2. `FIGURES-AUDIT.md` in this repo — the per-figure verdict
3. `diagrams/README.md` — the figure house style, and the two traps that cost real time
4. `figures/screens/README.md` — what each screenshot is for, and how the set is captured
5. only then the chapter you are writing, and only the specs it cites

Do **not** read all 18 specs up front. They are 10,165 lines and reading them
cold burns the context the writing needs. Pull them per chapter, per §3's map.

---

## 1. Setting up a machine

### The four repositories

```
docker.inkwell.ai/              ← clone this one; open Claude Code HERE
├── .claude/skills/inkwell-ticket/   the product-change pipeline (980 lines)
├── .tickets/                        9 worked tickets
├── docs/                            ARCHITECTURE · RAG · DEMO-SCRIPT + 4 design specs
├── Makefile                         every dev operation
├── spec.inkwell.ai/            submodule  ← THE REPORT LIVES HERE
└── src/
    ├── backend.inkwell.ai/     submodule  (.env and .env.test live here)
    └── frontend.inkwell.ai/    submodule  (the capture/ harness lives here)
```

**The three inner repos are git submodules, committed as gitlinks (mode
`160000`).** The superproject stores a 40-character commit pointer for each, not
their files. A clone or a GitHub integration that does not recurse gets three
*empty directories* where the spec, backend and frontend should be — and no
error, because a gitlink is a perfectly valid committed object. So
`docker.inkwell.ai` on its own contains none of the report and none of the code.

```bash
git clone --recurse-submodules <docker.inkwell.ai>
```

Already cloned flat? `make git-spull` populates the submodules and
`make check-submodules` verifies all three. See this repo's parent `README.md`
§Prerequisites.

### Open the session in `docker.inkwell.ai/`, not its parent

`.claude/skills/` is discovered relative to the working directory. The
`inkwell-ticket` skill sits one level down, so a session launched from a parent
folder never sees it: it will not appear in the skills list, will not trigger,
and the five committed hookify rules beside it stay silent — **including the one
that blocks a commit naming an assistant.** Launch from `docker.inkwell.ai/`, or
read `.claude/skills/inkwell-ticket/SKILL.md` plus all three `references/` files
by hand and hold the no-attribution rule yourself.

The hookify rules need the `hookify` plugin installed to fire at all. Without
it, nothing *enforces* them.

### Windows notes

- `origin` may be an SSH alias from one machine's `~/.ssh/config`. The
  submodules use **relative** URLs on purpose, so they inherit whatever identity
  works for the parent — fix the parent remote and all three follow. HTTPS is
  fine.
- Writing chapters needs **no Docker**. It needs this repo and a text editor.
- Re-capturing screenshots **does** need the full stack up, seeded and embedded,
  plus Playwright (§4). That is the one task better done on a machine that
  already runs the stack.
- Line endings: the repos are text-heavy and `.puml`/`.md` diff constantly. If
  git on Windows rewrites every line, nothing in `FIGURES-AUDIT.md` can be
  trusted against a diff. Prefer `git config core.autocrlf input`.

---

## 2. What the report is

A PFE engineering report, **written in English**. The two example reports that
supply its structure are French; they supply structure, not wording, and the
figures carry English labels for the same reason (`diagrams/README.md`).

The report presents the work as fixed two-week Scrum sprints. That numbering is
**the report's own**, and it is not the calendar sprint numbering in
`0-phase-plan.md`. The mapping is explicit in `10-requirements.md` §5 so nothing
is hidden. Always check which numbering a document means before citing a sprint.

---

## 3. Chapter ↔ sprint ↔ requirement map

The authority for "which sprint does this requirement belong to" is the
**`Sprint` column of `10-requirements.md` §2**. It attributes a requirement to
the sprint whose feature it refines, which is not always the sprint the code
shipped in. Use it; do not re-derive sprint membership from git dates.

| Chapter | Content | Figures |
|---|---|---|
| **Ch.1** | methodology — Scrum, waterfall vs agile | `fig-1-1`, `fig-1-2` |
| **Ch.2** | global model — use cases, the two global class diagrams, Gantt | `fig-2-1` … `fig-2-4` |
| **Ch.3** | working environment and architecture | `fig-3-1` … `fig-3-4` |
| **Ch.4** | Sprint 1 (schema, auth, article core) · Sprint 2 (editor, AI, event capture) | `fig-4-1` … `fig-4-6` |
| **Ch.5** | Sprint 3 (social, notifications, analytics) · Sprint 4 (RAG, insights, search) | `fig-5-1` … `fig-5-9` |
| **Ch.6** | Sprint 5 (marketplace, premium, moderation) · Sprint 6 (tests, demo, deploy) | `fig-6-1` … `fig-6-8` |
| **Ch.7** | **Sprint 7 · Sprint 8 · Sprint 9 — NEW, no figures exist yet** | `fig-7-*`, to be drawn |

Chapter 7's three sprints, per `10-requirements.md` §2:

| Sprint | Requirements | What shipped |
|---|---|---|
| **7** | FR-60…FR-65 (US-56, US-57, US-58) | like a comment, follower/following lists, block, save, share |
| **8** | FR-66…FR-68, FR-77…FR-83 (US-59…US-62, US-65…US-69) | live card controls, Reposted tab, recent comments, byline preview, assistant routing and in-document writes, status steps, docked panel, voice in, voice out |
| **9** | FR-84…FR-87 (US-70, US-71, US-72) | document library, ingestion, per-article attachment, citations |

**Three counts in `10-requirements.md` are stale and the report would quote them:**

- `:415` — *"54 stories, 8 epics, 259 points."* There are **72 US ids and 9
  epics** (E1–E9). Points never recomputed.
- **§5's release plan** — *"Three releases, six sprints"*, and its table stops at
  Sprint 6. Needs rows for Sprints 7, 8 and 9.
- **FR-78 supersedes FR-30** (recorded 2026-09-14). Chapter 4 must present
  FR-30's manual insert as what Sprint 2 built; Chapter 7 must say it was
  replaced. Do not silently drop FR-30 — the supersession is part of the story.

---

## 4. The figures and screenshots, and why they are behind

The visual assets were frozen earlier than the system they describe:

| Asset set | Frozen | Contents |
|---|---|---|
| `diagrams/` | **2026-08-19** | 25 `.puml` + 8 `.drawio` sources, 33 rendered SVG |
| `figures/screens/` | **2026-08-23** | 37 PNG, one sitting, one seed |
| `capture/` (frontend repo) | **2026-08-24** | the Playwright runner that produces them |
| the specs and the code | **2026-09-21** | 37 doc + 141 code commits after the diagram freeze |

**`FIGURES-AUDIT.md` is the per-figure verdict** — read it rather than re-deriving
it. Summary as of 2026-10-05:

- **Diagrams: 7 redraw · 12 amend · 14 verified clean.**
  The redraws are the global figures (`fig-2-2`, `fig-2-3`, `fig-2-4`,
  `fig-3-2`) plus Sprint 5's licensing figures (`fig-6-1`, `fig-6-2`,
  `fig-6-8`). A per-sprint figure is judged only against **its own** sprint's
  requirements — which is why `fig-5-4`, whose flow was rebuilt in Sprint 8,
  stays clean as the Sprint 4 record and Chapter 7 gets a new figure instead.
- **Screenshots: recapture all 37.** `components/layout/sidebar.tsx` gained a nav
  entry three times after the sitting (Following, Saved, Documents) and the
  sidebar is in every figure. This is the same trigger, and the same remedy, as
  the Phase 6 whole-set recapture already recorded in
  `figures/screens/README.md`.
- **The capture harness is broken, not merely stale.**
  `capture/report-figures.capture.spec.ts` asserts the AI composer by
  placeholder `/ask the ai assistant|no ai tokens remaining/i`;
  `features/ai/ai-assistant-host.tsx` now renders `'Ask, or say what to write…'`.
  The test fails its own guard. Repair it before booking a sitting.
- **Chapter 7 needs 9 new diagrams and 14 new captures**, itemised in the audit.

### Before drawing anything

`diagrams/README.md` holds the house style, matched to the example report:
black-and-white UML with no fills, colour reserved for the architecture figures,
one folder per figure, `!include ../_style.puml`, and the PlantUML-vs-draw.io
dividing line with the reasoning behind it. It also records three traps that each
cost real time — `skinparam padding` renders a warning banner *into* the image,
`<<include>>` silently vanishes in draw.io labels, and a parenthesis in an
attribute makes PlantUML treat it as a method and `hide methods` then deletes it.
Read it before writing a `.puml`.

Render with `make` in `diagrams/` — Docker is the only requirement. **Use the SVG
in the report**, not the PNG.

### Numbers no figure should assert without a fresh measurement

`fig-3-4` and `fig-6-7` carry hard test counts. Measured statically on
2026-10-05, the backend suite went from **17 spec files at the freeze to 51**,
e2e from **23 files to 25**, and the ledger harness reads **30** `it()` blocks
against the figure's claim of 27. The "479 backend tests" both figures state
happens to equal a static grep of today's tree, which is a coincidence and not
corroboration — a grep is not what jest reports. **Run each suite once, in the
container, and regenerate those figures from its output.** Tests do not run
host-side on this project at all; the skill's `references/environment.md`
§Tests has the exact commands and the two flags that are not optional.

---

## 5. Decisions already taken

- **Sprints 7–9 become Chapter 7**, rather than being folded back into Chapters
  4–6 by subject (decided 2026-10-05). Chapters 4–6 stay the historical record of
  what each sprint delivered. This is what keeps 14 figures clean instead of
  forcing them cumulative, and it gives the newest work — in-document AI writes,
  voice, document sources — its own chapter.
- **Figures are judged against the code, not against the specs.** A figure is
  called stale only when something in `src/` disagrees with it. The specs are
  themselves reconciled after the fact and have their own drift (§3).
- **Figure sources stay in git as text.** That is what made the audit a
  text-to-text diff — "four queues drawn, six in `src/`" is a `grep`, not an
  inspection by eye.

---

## 6. Open questions — these block work

1. **The Gantt dates.** `fig-2-4` says `[Report submission] happens at
   2026-08-31` and `[Defense] happens at 2026-09-07`. Both are in the past and
   neither happened. The figure also has no S8/S9 bars; the commit record
   suggests roughly Sep 7–14 and Sep 15–21, but the user's own tracking wins.
   `fig-2-4` cannot be regenerated until this is answered.
2. **Is `GOOGLE_CLIENT_ID` populated in the capture environment?** The sign-in
   button is gated on Google being *configured* (2026-08-24), so this decides
   whether `guest-02-login` and `guest-03-register` show it.

---

## 7. How to verify a claim before writing it

The audit's findings all came from the same four moves. Use them rather than
trusting a spec sentence:

| To check | Do |
|---|---|
| when a column, table or constant appeared | `git log -S '<symbol>' -- <path>` in the owning submodule |
| what a figure asserts | read its `.puml`/generator source, not the SVG |
| the real route surface | `grep -rE "@(Get\|Post\|Patch\|Put\|Delete)\(" src/**/*.controller.ts` |
| the real table and enum list | `src/database/schema/*.ts` |
| which sprint a feature belongs to | the `Sprint` column of `10-requirements.md` §2 |

Two habits that paid off: compare a figure against the code at the **freeze
commit as well as HEAD** (`git rev-list -1 --before=<date>`) so you can tell
drift from an error that was always there; and when a note says something is
impossible, re-test it cheaply before repeating the claim.

---

## 8. What not to do

- **Do not restate product behaviour here or in a chapter from memory.** Cite the
  spec section or the code path. This report's whole current problem is copies
  that drifted.
- **Do not reconstruct the product-change pipeline.** If the task turns into a
  code change, use the `inkwell-ticket` skill; prefer it over any note that
  disagrees with it, because it is versioned with the code.
- **Do not verify host-side.** `node_modules` on the host is an empty volume
  mount for both app repos, so a lint or test that appears to pass has silently
  not run. The skill's `references/environment.md` is the authority.
- **No assistant named in any commit, PR, changelog or comment**, ever. This is
  the user's standing rule and a hookify rule enforces it — but only when the
  session was launched from `docker.inkwell.ai/` with the plugin installed.
