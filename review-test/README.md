# Review & test — the UI bug sweep

Phase 5 shipped code-complete and CI-green, but almost none of it had been opened in a
browser. Everything was verified over the API, which structurally cannot catch a dead
button, a crashed render, or a gate that looks right and is not.

This directory is the record of driving every screen with Playwright and writing down
what is broken.

## The rule

**Find and record. Do not fix, and do not investigate causes.**

When something fails: capture it, file it, move on. Opening the source to work out *why*
feels productive and is the main way this sweep fails — it turns a complete catalogue
into three well-understood bugs and twenty unexamined screens. Triage is separate work,
done afterwards, against a finished list.

## Files

| file | what it holds |
|---|---|
| `AGENT-PROMPT.md` | The prompt to hand an agent for a sweep session. Paste it verbatim. |
| `progress.md` | The coverage matrix and session log. **The resume point** — read it first. |
| `bugs.md` | Every finding, grouped by severity. IDs are stable and never reused. |
| `known-gaps.md` | Documented deliberate non-implementations. **Not bugs.** |
| `screenshots/` | One per screen per persona, `<route>--<persona>.png`. |

## Severity

Judged by **consequence**, not by how broken it looks. A silent wrong number outranks a
loud crash on a page nobody needs.

| | |
|---|---|
| **Critical** | Data loss · money computed or moved wrongly · an access gate bypassed · a core flow that cannot complete at all |
| **High** | A core flow blocked for one persona, or producing a visibly wrong result |
| **Medium** | Misbehaves, but there is a workaround. A gate that refuses the right person for the wrong reason. |
| **Low** | Cosmetic, copy, spacing, a missing empty state |

## Before filing anything

**Check it is not a known gap.** Twelve files in the frontend carry documented deliberate
non-implementations — `NOT WIRED UP`, `TODO(Phase N)`, `disabled so it can't 404`. The
"Continue with Google" button is one of them, by design.

So when a control does nothing, grep the component for a marker first. If one exists it
belongs in `known-gaps.md` with the comment quoted — not in `bugs.md`. Filing known gaps
as bugs buries the real findings among noise, which is the second way this sweep fails.

One caveat, and it has already bitten: **a `TODO(Phase 5)` marker may now be stale**,
because Phase 5 shipped. A control disabled pending something that now exists is a real
finding. Two are already filed as `BUG-001` and `BUG-002`.

## Filing a finding

Stable id, then: route · persona · expected · actual · screenshot · any console or network
error captured. **No cause, no file references, no proposed fix.**

## Running a session

The stack must be up — `docker ps` should show `inkwell-web-1` and `inkwell-api-1`. App
services sit behind the compose `apps` profile and need `--profile apps` to start.

The app is at **`http://frontend.inkwell.ai`**. Plain HTTP: there is no TLS locally and a
browser that auto-upgrades to https gets `ERR_CONNECTION_REFUSED`.

Sessions mutate the dev database — credits get spent, articles published, accounts
possibly banned. That is accepted. `progress.md` records what each session changed.
