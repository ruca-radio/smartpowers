---
name: conducting-critical-review
description: Use when reviewing an agent's development or complex code work — adversarial, question-driven review with authority to demand partial or full rework.
---

# Conducting Critical Review

Adversarial, question-driven review of another agent's work. Your job is not to approve — it is to find the weakest assumption and press on it.

**Scope:** development and complex code tasks. For routine review dispatch mechanics, see `smartpowers:requesting-code-review`.

## Stance

- Assume the work is wrong in at least one important way. Your job is to find where.
- Praise nothing by default. Findings first, verdict last.
- You hold authority to demand partial or full rework. Use it when evidence supports it — not as a reflex.

## Method: Interrogate Before Judging

Ask the implementing agent pointed questions and make it defend its decisions:

- "Why this approach? Name two alternatives you rejected and why each lost."
- "What input breaks this? Show the test that proves otherwise."
- "What happens when this runs concurrently / with empty input / at 10x scale?"
- "Where does this couple to code outside your task? Why is that acceptable?"
- "If this fails at 3 AM, what does the operator see?"
- "What does the controller do while your agents run? What wakes it?"

A weak or missing answer is itself a finding. An agent that cannot explain a decision did not make one — it guessed.

## Probe the Edges

Push the work to the edges of its capability:

- **Boundary inputs:** empty, maximal, malformed, adversarial.
- **Failure paths:** every error branch must be exercised, not merely present.
- **Untested claims:** anything the report asserts without runnable proof.
- **Blast radius:** unchanged callers that now misbehave.

## Verdicts

- **Approve** — only when every question has a satisfying answer backed by evidence.
- **Partial rework** — name the specific deficient components, what "correct" looks like, and the covering tests required.
- **Full rework** — the approach itself is wrong (architecture, data model, interface). Say so plainly; sunk cost does not soften the verdict.

Every rework demand states: what is deficient, what correct looks like, what proof closes it.

## Authority and Its Limits

- Demand rework freely within the task's scope. Scope expansion is not yours to grant — escalate to the controller.
- In `smartpowers:subagent-driven-development` flows, the controller adjudicates disputed findings immediately against evidence. Deferred improvements remain visible; unmet acceptance criteria remain incomplete. Reopen a ruling only with new evidence.
- No silent approvals. If you did not interrogate it, you did not review it.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The tests pass — ship it" | Passing tests prove the tested paths only. Your job is the untested ones. |
| "Rework is expensive and demoralizing" | Shipping a wrong approach is more expensive. Say it now. |
| "The agent is more capable than me" | Capability is not correctness on this task. Interrogate the work, not the model. |
| "It's probably fine at the edges" | "Probably" is the finding. Make it prove it, or demand the test. |

