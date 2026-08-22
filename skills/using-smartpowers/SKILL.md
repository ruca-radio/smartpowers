---
name: using-smartpowers
description: Use when starting any conversation. Establishes skill discovery and invocation rules.
---

# Using SmartPowers

## The Rule

Invoke relevant skills **before** any response or action — including clarifying questions, exploring files, or checking context. If a skill applies, you must use it.

**Process skills first** (brainstorming, systematic-debugging), then implementation skills (writing-plans, etc.).

## Skill Priority

| Request type | First skill | Then |
|-------------|-------------|------|
| "Build X" | brainstorming | writing-plans → subagent-driven-development |
| "Fix this bug" | systematic-debugging | test-driven-development |
| "Create a skill" | writing-skills | — |
| "Multiple jobs at scale" | orchestrating-agent-swarms | dispatching-parallel-agents |
| Session/task complete | saving-session-learnings | — |

## Red Flags — Stop and Check Skills

| Thought | Action |
|---------|--------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes before clarifying questions. |
| "Let me explore the codebase first" | Skills tell you how to explore. Check first. |
| "I remember this skill" | Skills evolve. Read the current version. |
| "This doesn't count as a task" | Any action = task. Check for skills. |

## Platform Notes

If your harness appears below, read its reference for special instructions:

- Kimi / Moonshot: `references/kimi-tools.md`
- Codex: `references/codex-tools.md`
- Pi: `references/pi-tools.md`
- Antigravity: `references/antigravity-tools.md`

## User Instructions Take Precedence

`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, or direct human requests override skills, which override default behavior. Only skip skill workflows when your human partner explicitly tells you to.
