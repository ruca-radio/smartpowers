---
name: dispatching-parallel-agents
description: Use when independent or explicitly coordinated tasks can run concurrently.
---

# Dispatching Parallel Agents

Apply `smartpowers:core-principles` and use the topology from `smartpowers:orchestrating-agent-swarms`.

1. Define dependencies, acceptance criteria, provider scope, and output ownership.
2. Discover the harness's concurrency, messaging, model selection, and persistence capabilities.
3. Dispatch ready tasks with self-contained briefs and only relevant context.
4. Record each task, owner, target, attempt, workspace, and expected artifact.
5. Route questions through durable peer messages or the controller's mailbox.
6. Verify returned artifacts, integrate isolated changes, and run covering integration checks.

Shared files do not automatically prohibit parallel work: use separate worktrees with explicit integration, or serialize access with exclusive resource leases. Never allow uncoordinated writers in the same checkout.

For the optional runtime, declare dependencies and exclusive resource names in the workflow. External harnesses claim tasks, renew leases, submit results, and acknowledge messages through the CLI. The database handles competing claims transactionally.

Retry individual failures rather than restarting successful tasks. Preserve completed artifacts on resumption. Retry-safe tasks may restart after lease expiry; other tasks need evidence that earlier side effects are reconciled.

Wait while agents run if the host cannot resume automatically. Use background completion only when the host or supervisor actually supports it. Status updates should explain progress and blockers without replacing execution.
