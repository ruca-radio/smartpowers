# Antigravity Platform Notes

Orientation only — Antigravity evolves quickly; check your harness documentation.

## Skill Discovery

Antigravity supports agent-defined instructions and skills. Check your harness documentation for the current install location (workspace- or user-level skills/rules directories); place the `skills/` tree there or index it from the workspace rules file.

## Subagent Dispatch

Antigravity runs agents as managed tasks, including background and parallel work. Map "dispatch a subagent" to a fresh managed task with the crafted prompt as its complete instructions. Check your harness documentation for task isolation guarantees.

## Worktree / Isolation

Check whether your version gives each managed task its own workspace. If tasks share a checkout, use `smartpowers:using-git-worktrees` before running parallel or fix-loop work.

## Quirks

- Agents produce artifacts (plans, walkthroughs) per task — treat ledger and report files as the durable record instead.
- Browser/editor integrations are out of scope for skill prompts; keep dispatches text-only.
- Review artifacts for scope expansion before approving task completion.
