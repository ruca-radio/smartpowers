# Codex Platform Notes

Orientation only — behavior varies by version and surface; check your harness documentation.

## Skill Discovery

Codex reads repo-level instructions from `AGENTS.md`. Skills are not necessarily auto-discovered; list the `skills/` tree (or the specific `SKILL.md` paths) in `AGENTS.md` and read each skill explicitly before applying it.

## Subagent Dispatch

Delegation mechanics differ between the CLI and cloud surfaces. If no explicit subagent tool exists, emulate the dispatch pattern: start a fresh session per task with the crafted prompt as its complete context. Check your harness documentation for current subagent support.

## Worktree / Isolation

CLI: use `smartpowers:using-git-worktrees` directly. Cloud: each task already runs in an isolated environment; worktrees matter only when agents share a checkout.

## Quirks

- Sandbox and approval settings can block writes outside the workspace — configure before subagent-driven development.
- Sessions share no history; every dispatch prompt must be fully self-contained.
