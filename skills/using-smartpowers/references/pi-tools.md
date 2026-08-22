# Pi Platform Notes

Orientation only — Pi's capabilities vary by version and configuration; check your harness documentation.

## Skill Discovery

Check your harness documentation for how Pi loads instructions and skills. If there is no native skill mechanism, point Pi at the `skills/` tree from your project instructions file and read each `SKILL.md` explicitly before applying it.

## Subagent Dispatch

Check your harness documentation for subagent or background-task support. Absent one, emulate the dispatch pattern: run a separate Pi session per task, with the crafted prompt as that session's complete context.

## Worktree / Isolation

Assume no harness-managed isolation. Use `smartpowers:using-git-worktrees` so concurrent agents never share a checkout.

## Quirks

- Context is per session; nothing reaches a dispatched worker unless it is in the prompt.
- Verify file-write permissions before running unattended fix loops.
- Ledger and report files on disk are the only memory that survives across sessions.
