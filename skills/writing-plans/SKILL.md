---
name: writing-plans
description: Use when authorized work has multiple tasks, dependencies, or interfaces requiring an execution plan.
---

# Writing Plans

Apply `smartpowers:core-principles`. Plan around deliverables and acceptance criteria, not arbitrary minute counts. Avoid writing the entire implementation twice.

Save a dated plan under docs/smartpowers/plans. Include goal, design/spec reference, global constraints, authorization scope, integration destination, and verification commands. State which providers may receive task context.

Use this task shape:

```markdown
### Task 1: Deliverable
**Files:** exact affected paths
**Dependencies:** task IDs and required interfaces
**Inputs:** task-local context and relevant decisions
**Output:** artifact paths and interface contract
**Acceptance:** observable conditions for success
**Verification:** exact commands or inspection criteria
**Execution:** role and capability needs; workspace ownership
**Retry:** safe to repeat, or side-effect reconciliation required
```

Include concrete code when it resolves a fragile interface, not as mandatory boilerplate. Every task must carry the global constraints it needs. Reject placeholders that hide decisions essential to execution.

Review coverage, dependency cycles, conflicting file ownership, resource limits, and mismatched interfaces before starting. Batch mechanical changes when they share one verification surface.

Choose native agents, runtime workers, or inline execution based on available capabilities and coordination cost. Record the choice and begin authorized work; do not end with a redundant execution menu.
