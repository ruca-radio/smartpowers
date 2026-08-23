---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session.
---

# Subagent-Driven Development

Execute plans with mostly independent tasks (tightly coupled → `smartpowers:executing-plans`): fresh implementer per task, task reviews, final review.

## Setup

- Isolate workspace — `smartpowers:using-git-worktrees` or verify isolation.
- `scripts/sdd-workspace PLAN_FILE` → git-ignored `<repo>/.smartpowers/sdd/<plan-basename>/` (git-ignores `.smartpowers/`, committing if needed).
- Ledger `<workspace>/progress.md`: names your plan → resume first incomplete task; else start fresh. First line: `# SDD ledger — plan: <plan file path>`.
- Read plan once (context, Global Constraints, spec path); todo per task.
- Pre-flight scan (conflicts, contradictions, type mismatches): ledger findings table; rule on each before Task 1.

## Model Selection

Least powerful model per role: fast/cheap for mechanical 1-2-file tasks; standard for multi-file work; most capable for architecture/final review.

**Always specify the model explicitly when dispatching** (default inherits yours). **Turn count beats token price** — cheap models take 2-3× turns; mid-tier floor for reviewers and prose implementers.

### 1. Dispatch

- **Brief:** `scripts/task-brief PLAN_FILE N` → task text in unique file.
- **Dispatch contains:** where-it-fits line; brief path as requirements source; earlier-task interfaces/decisions; ambiguity resolutions; report-file path.
- **Report file:** `task-N-brief.md` → `task-N-report.md`; full report lives there; return status, commits, test one-liner, concerns.
- **No history:** never paste prior-task summaries — subagent needs its task, interfaces, global constraints.
- **No subagents contract:** implementer never dispatches subagents; review comes from you.

### 2. Handle Report

- **DONE** → review package, task reviewer.
- **DONE_WITH_CONCERNS** → fix correctness/scope concerns before review; note observations, proceed.
- **NEEDS_CONTEXT** → provide context, re-dispatch.
- **BLOCKED** → context problem: re-dispatch same model; reasoning: stronger model; too large: break up; plan wrong: rule, ledger, re-dispatch with ruling.

### 3. Review

- Diff: `scripts/review-package PLAN_FILE BASE HEAD` (BASE = `git rev-parse HEAD` at dispatch, never `HEAD~1`).
- Reviewer gets: brief, report, review package paths; global constraints verbatim.
- **Reviewer verdicts:** spec compliance ✅/❌ AND quality approved/not approved — both required.
- **⚠️ items** (unchanged code or cross-task requirements): resolve yourself; real gap → failed spec review.

### 4. Fix Loop

Triggers: spec ❌, Critical/Important finding, or confirmed ⚠️ gap.

Ledger Minor findings (`Task <N>: minor (deferred): <one-liner>`) — never looped; rule on plan-mandated ones, ledger the ruling.

**Five rounds max.** 1-3: resume original implementer, open findings verbatim. 4-5: fresh implementer one tier above the stuck one — "you own it now; prior implementer failed [N] times; read the report file."

**Each round:** fix, re-run covering tests, append report (command, output); scoped re-review `scripts/review-package PLAN_FILE FIX_BASE HEAD` + `re-review-prompt.md`; ledger: `Task <N>: fix round <R>/5 (<X> addressed, <Y> open — <finding one-liners>; commits <a7>..<b7>)`

**Breaker (round 5 still open):** adjudicate each:
- Reviewer wrong/contestable → park: `Task <N>: parked — <finding> — Ruling: <why>`
- Real, nothing downstream depends on it → park same way
- Real and load-bearing → rule smallest unblocking change, ledger, carry into next dispatch

Adjudicate only at the cap; every ruling is a ledger entry — no silent discards.

Review clean or findings parked → ledger `Task <N>: complete (commits <base7>..<head7>, review clean)` or `Task <N>: complete (commits <base7>..<head7>, <K> parked)`; never advance with Critical/Important unfixed/unparked.

## Final Review

`scripts/review-package PLAN_FILE MERGE_BASE HEAD` (MERGE_BASE = `git merge-base main HEAD`), most capable model, `smartpowers:requesting-code-review`; reviewer sees ledger's deferred-minor/parked lines. Findings → ONE fix subagent with full list; one scoped re-review; adjudicate residuals; no second wave.

Finish: final message names every `Ruling:` ledger line under "Rulings I made," with cost if wrong — exhaustive. Delete workspace (`rm -rf <workspace>`) — git history is the record; use `smartpowers:finishing-work`.

## Pacing

- Narrate at most one short line between tool calls; never check in mid-task.
- **Rulings, not stalls:** decide conflicts, ambiguities, plan defects; record `Ruling: <what> — <why> — <cost if wrong>`.
- **Four things stop you:** irreversible/destructive operation; security-sensitive action; side effect outside worktree (merge, push); plan so broken every path is guesswork.
- **Batch same-shape work:** many small same-kind edits → ONE brief listing every file and change, one diff review; per-task dispatches only for work needing own judgment, tests, review surface.
- **Waiting / turn discipline:** never end the turn with agents in flight — ended turns do not resume. Do local work (ledger, next review package); idle → block on the harness wait primitive in 5-10 minute stretches; one status line per wake.

## Rationalizations

- "Close enough on spec" — gaps = not done; fix or adjudicate at cap.
- "I'll fix it myself" — controller fixes pollute context, skip review; resume implementer.
- "One more round will converge" — past cap = structural failure; adjudicate and route.
- "This finding is obviously wrong" — adjudicate only at cap; every ruling is a ledger entry.
- "The fix was small, skip re-review" — unreviewed fixes land regressions; re-review every round.
- "Ledger bookkeeping is overhead" — ledger survives compaction; without one you re-dispatch completed work.
