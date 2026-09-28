---
name: orchestrating-agent-swarms
description: Use when work benefits from multiple agents, models, providers, or collaboration patterns.
---

# Orchestrating Agent Swarms

Apply `smartpowers:core-principles`. Define the work graph before staffing. Separate role, model, provider, and harness so any compatible target can fill a role.

## Choose a topology

| Work | Pattern |
|---|---|
| Independent deliverables | Parallel workers |
| Outputs consumed by later tasks | Dependency graph or pipeline |
| Ambiguous interface | Peer discussion, then record the agreed contract |
| Independent assessment | Implementer and reviewer |
| Large separable project | Hierarchical delegation within shared budgets |
| Ongoing work | Persistent workers only when wake-up and state storage exist |

Do small tasks directly. Size concurrency by work, provider quotas, available memory, and review capacity. A role brief defines mission, inputs, capabilities, outputs, acceptance criteria, resource ownership, and authorization.

## Capability discovery and routing

Discover native delegation, per-agent model selection, messaging, context limits, filesystem sharing, background support, and tool access. Use CLI or external worker adapters when native features are absent. Never simulate unavailable tools by claiming they ran.

Choose targets meeting capability and context requirements, then rank by task success, latency, cost, and availability. Preserve the authorized provider/data scope during fallback. The runtime implements explicit priorities and capability/context matching; empirical ranking requires caller-supplied priorities.

## Coordinate

Give tasks stable identities and attempts unique identities. Use durable artifacts rather than copying full histories. Peer messages need sender, recipient, correlation ID, and acknowledgement; route through the controller only when direct messaging is unavailable.

Use transactional claims or leases for shared resources. Parallel writers need isolated workspaces or explicit ownership. Verify producer artifacts before dependent tasks start. Review and integrate outputs continuously.

Persist decisions and status before handoff. If the harness lacks automatic wake-up, remain active and wait in bounded intervals. Detached work requires a real supervisor, not a promise that agents will report later.

## Recover

Distinguish authentication/quota, transient transport, task ambiguity, unavailable capability, and invalid output. Use authorized provider fallback where appropriate. Expired work may have produced side effects; replay only if retry-safe or reconciled. Fence old attempts so late results cannot overwrite current state.

Use `smartpowers:dispatching-parallel-agents` for execution mechanics and `smartpowers:subagent-driven-development` for implementation review.
