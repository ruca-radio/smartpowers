# Session learnings — 2026-08-23 — Turn discipline

## What happened

Field report: controller dispatched four parallel background agents, ended its
turn with "they'll report back," and the session sat idle forever. The ended
turn never resumed; the agents' completions had no one to reconcile them.

## Root cause

The orchestration skills mandated bounded *waiting* but never prohibited
*ending the turn* with agents in flight. In most harnesses, an ended turn does
not resume — so "waiting" advice was inert exactly where it mattered.

## Fix (shipped)

- `dispatching-parallel-agents`: new "Turn Discipline" section + rationalization row.
- `orchestrating-agent-swarms`: Stage 4 turn-discipline bullet + rationalization row.
- `subagent-driven-development`: Pacing bullet rewritten to waiting/turn-discipline form
  (absorbed within the 800-word budget via compensating trims).

The rule everywhere: never end the turn with agents in flight; block on the
harness wait primitive in bounded stretches; status notes go between waits,
never instead of them. Sole exception: the human explicitly asks for detached
background operation.

## What went well

- The word budget did its job: the SDD fix had to earn its words, which kept
  the added rule terse instead of bloating the file.

## What to improve

- **Budget headroom.** SDD sat at exactly 800/800 words, so a one-line fix
  cost ten trims. Keep high-churn skills ~5% under budget so field fixes land
  without a compression pass.
- **Test the harness assumption, not just the text.** This defect was invisible
  to skill-lint and to the paired eval — both check artifacts, not turn-level
  behavior across a real dispatch. Future evals for orchestration skills should
  include a live "dispatch two background agents" scenario and check whether
  the controller blocks to completion.
- **Watch for the class, not the instance.** Any skill that advises concurrency
  needs an explicit rule for what the controller does while it waits. Audit new
  orchestration skills for this at review time.

## Fed back into

- `smartpowers:writing-skills` (budget-headroom guidance above)
- `smartpowers:conducting-critical-review` (question bank: "what does the
  controller do while agents run?")
