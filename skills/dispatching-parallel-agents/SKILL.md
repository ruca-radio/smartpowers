---
name: dispatching-parallel-agents
description: Use when you have multiple independent tasks that can be executed concurrently by subagents.
---

# Dispatching Parallel Agents

## Overview

Run independent tasks concurrently to reduce wall-clock time. Coordinate results, handle failures, merge outputs.

## When to Use

- Multiple independent files to modify (same pattern, different locations)
- Independent research or analysis tasks
- Parallel test runs across different configurations
- Batch processing where tasks don't share state

## When NOT to Use

- Tasks depend on each other's outputs
- Tasks modify the same files
- Sequential logic is required (task N needs task N-1 complete)
- You lack mechanism to merge results safely

## Process

1. **Decompose** — split work into truly independent units. Verify no shared files or dependencies.
2. **Prepare briefs** — each subagent gets: task description, input data, expected output format, constraints. No session history.
3. **Dispatch** — send all tasks simultaneously. Record agent identities.
4. **Monitor** — track which agents complete, which fail, which stall.
5. **Merge** — combine outputs. Resolve conflicts if any (shouldn't happen if decomposition was correct).
6. **Verify** — run integrated tests on merged result.

## Turn Discipline

**Never end the turn with agents in flight.** An ended turn does not resume in most harnesses — "they'll report back" means the session sits idle forever. Block on your harness's wait primitive (wait-for-message, task-output) in bounded stretches; on each wake, reconcile completed agents and continue. Post status notes between waits, never instead of them. Sole exception: your human partner explicitly asks for detached background operation.

## Failure Handling

| Scenario | Action |
|----------|--------|
| One agent fails | Retry that agent with more context or simpler task. Don't restart others. |
| Multiple agents fail | Likely decomposition error. Stop, re-analyze dependencies, redesign. |
| Results conflict | Should not happen. If it does, your independence assumption was wrong. Sequentialize conflicting tasks. |
| Agent stalls | After bounded wait (5-10 min), check status. If truly stuck, cancel and re-dispatch. |

## Coordination

- **Shared state:** Avoid. If unavoidable, use a ledger file all agents read/write, with clear locking convention.
- **Output format:** Specify exactly. Structured formats (JSON, markdown tables) merge easier than prose.
- **Idempotency:** Design tasks so re-running is safe. Agents may need retry.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "These are mostly independent" | "Mostly" means they're not. Sequentialize until truly independent. |
| "Parallel is always faster" | Coordination overhead, merge conflicts, and debugging complexity often erase gains for <3 tasks. |
| "I'll sort out conflicts after" | Designing for independence before dispatch is cheaper than resolving conflicts after. |
| "Completions arrive automatically — I'll hand back" | Handing back ends the turn; nothing wakes it. Block on the wait primitive until the wave is done. |
