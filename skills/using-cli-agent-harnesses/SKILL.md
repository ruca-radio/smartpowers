---
name: using-cli-agent-harnesses
description: Use when delegating work to locally installed CLI AI agents (Codex CLI, OpenCode CLI, Antigravity CLI) or orchestrating them from the shell.
---

# Using CLI Agent Harnesses

Drive local CLI coding agents — Codex CLI, OpenCode CLI, Antigravity CLI — as tools in your workflow. Their flags and capabilities change fast: verify, don't recall.

## Rule Zero: Discover, Don't Recall

Never invoke from memory. Before first use in a session:

```bash
<cli> --version
<cli> --help
```

Flags, subcommands, and headless modes differ by version. Two minutes of `--help` beats a failed automation run. Where this skill and `--help` disagree, `--help` wins.

## When to Delegate to a CLI Agent

- A second opinion from a different model family on a design or diff.
- Mechanical, well-scoped work (codemods, boilerplate) where its quota is cheaper than your context.
- Tasks in its documented strength area.
- Extra parallel capacity when your harness's subagent slots are full.

Do the work yourself when: the task needs your session's accumulated context, it involves secrets the CLI shouldn't see (`smartpowers:sensitive-rd-protocol`), or doing it is faster than briefing it.

## Invocation Pattern

1. **Headless only.** Find the non-interactive mode via `--help` (typically an `exec`/`run` subcommand or a print/prompt flag). Never start an interactive session you cannot drive.
2. **Self-contained brief.** The CLI agent has none of your context. Prompt = task + exact file paths + constraints + done-criteria — the same discipline as a subagent dispatch.
3. **Bound the blast radius.** Run it in an isolated worktree or scoped directory per `smartpowers:using-git-worktrees`. Learn its auto-apply/auto-edit behavior before pointing it at a dirty tree.
4. **Capture output to a file** in the workspace; parse the artifact rather than watching the stream.
5. **Verify its work yourself.** A CLI agent's "done" is a claim. Run the tests. For non-trivial output, apply `smartpowers:conducting-critical-review`.

## Failure Handling

| Symptom | Action |
|---------|--------|
| Hangs with no output | Likely waiting on interactive input or auth — kill it, re-check `--help` for headless and auth flags |
| Auth or quota error | Report it to your human partner; don't burn cycles retrying |
| Wrong-shaped output | Your brief was ambiguous — rewrite the brief, re-run |
| Confidently wrong code | Treat like any agent's work: interrogate, verify, demand rework if needed |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I remember the flags" | Versions drift. `--help` takes ten seconds. |
| "It's another AI — it'll figure it out" | It has zero session context. Brief it like a fresh subagent. |
| "Skip verification, it's a capable tool" | Capable tools are confidently wrong at the same rate as capable agents. Verify. |
