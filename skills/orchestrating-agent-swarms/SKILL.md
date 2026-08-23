---
name: orchestrating-agent-swarms
description: Use when planning work that needs multiple AI agents — designing agent roles, sizing the swarm to the task, and running agents in parallel or stages.
---

# Orchestrating Agent Swarms

Plan, staff, and run a swarm of task-specific agents. Scale the swarm to the work — no bigger.

**Related:** `smartpowers:dispatching-parallel-agents` (dispatch mechanics) and `smartpowers:subagent-driven-development` (plan execution with per-task review). This skill decides the swarm's shape; those skills run it.

## Stage 1: Decompose

Break the job into atomic tasks. A task is atomic when one agent can hold it in context and finish it without another agent's in-flight output.

- Tasks independent → parallel wave.
- Task N needs task N-1's output → pipeline stage. Never parallelize across a dependency.
- Map dependencies on paper before staffing. A swarm run from an unmapped dependency graph fails mid-flight.

## Stage 2: Design Roles

One role per distinct capability, not per task. Agents of the same role are interchangeable instances.

Each role brief defines: mission (one sentence), inputs, output contract (exact format and file path), constraints, and what it must NOT do. No role receives your session history — craft exactly what it needs, nothing else.

## Stage 3: Size the Swarm

Scale by work, not enthusiasm:

| Workload | Swarm |
|----------|-------|
| 1-2 tasks | Do it yourself — dispatch overhead exceeds the gain |
| 3-8 independent tasks | One agent per task, single wave |
| 9+ tasks or staged work | Waves: stage gates between dependency layers, parallel within a stage |
| Continuous pipeline | Long-lived background agents, woken by message as work arrives |

**Cap: never run more parallel agents than you can review.** Unreviewed parallel output is unmerged risk compounding silently. Stay within your harness's live-agent limit.

Model per role: the least capable model that handles the task class (see the model table in `smartpowers:subagent-driven-development`).

## Stage 4: Run

- Dispatch a full wave simultaneously; record agent identities.
- **Stage gates:** validate a stage's merged outputs before dispatching the next stage. Parallel agents cannot see each other — route all shared context yourself.
- While agents run, do your own non-overlapping work (ledger, next briefs, review packaging). Never idle-poll.
- **Turn discipline:** never end the turn with agents in flight — an ended turn does not resume in most harnesses. Block on the harness wait primitive in bounded stretches until the wave completes. Status notes go between waits, never instead of them.
- Merge per `smartpowers:dispatching-parallel-agents`; run integrated verification on the merged result.

## Failure Handling

| Scenario | Action |
|----------|--------|
| One agent fails | Retry with more context or a narrower task |
| A whole wave fails | Decomposition error — stop, re-map dependencies, redesign |
| Agent stalls | Bounded wait, one status check, then cancel and re-dispatch |
| Same role fails repeatedly | The role design is wrong — rewrite the brief, don't just re-dispatch |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "More agents = faster" | Coordination and review costs scale superlinearly. Unreviewed output is not progress. |
| "They'll figure out the shared context" | Parallel agents see nothing of each other. Route it or it doesn't exist. |
| "This dependency is minor" | A minor dependency is still a dependency. Stage it. |
| "I'll review everything at the end" | End-of-swarm review finds structural problems after N agents have amplified them. Gate each stage. |
| "Completions arrive automatically" | In most harnesses an ended turn never resumes. Block on the wait primitive; don't hand back. |
