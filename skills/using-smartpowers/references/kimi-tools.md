# Kimi / Moonshot Harness Notes

Orientation only — behavior varies by harness version. Check your harness documentation when something here doesn't match what you observe.

## Skill Discovery

- Install target: `~/.agents/skills/<skill-name>/SKILL.md` (the default of `install.sh --kimi`).
- Discovery runs on frontmatter: `name` + `description`. Keep descriptions trigger-only per `smartpowers:writing-skills` — workflow summaries cause skipped loads.

## Subagents

- Kimi harnesses typically expose subagent dispatch (Task-style tools). If dispatch is unavailable in your configuration, fall back to `smartpowers:executing-plans` for inline plan execution with checkpoints.

## Workspace Isolation

- No native worktree tool is guaranteed — the git fallback in `smartpowers:using-git-worktrees` is the default path. The `.smartpowers/worktrees/` convention applies.

## Context Budget

- Moonshot models run long contexts, but the word budgets in `writing-skills` still bind: shorter skills load faster, cost less per session, and — per the framework's SDO findings — get read and followed more reliably than long ones.
