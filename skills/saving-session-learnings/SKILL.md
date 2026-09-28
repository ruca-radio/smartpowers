---
name: saving-session-learnings
description: Use when a work session or major task completes — evaluate performance, extract reusable knowledge, and persist it to memory stores and project folders.
---

# Saving Session Learnings

Preserve run evidence and bank useful findings. Follow `smartpowers:core-principles` for authorization.

## When

- End of a work session.
- After a major milestone: plan executed, incident resolved, feature merged.

Keep it under five minutes. A learning ritual that slows work gets skipped.

## Step 1: Evaluate Performance

Three questions, answered with evidence from the session (ledger, rulings, test runs):

- **What worked?** Name the practice, not the feeling. ("Pre-flight scan caught two type mismatches before dispatch.")
- **What struggled?** Failures, rework rounds, stalls, wrong first guesses — verbatim from the ledger where possible.
- **What changes next time?** Each struggle maps to one concrete change: a rule, a check, a script, a skill edit. No change means it was an observation, not a learning.

## Step 2: Distill Key Knowledge

Separate session trivia from durable knowledge. Durable = useful in a future session without this one's context:

- Project facts: architecture decisions, environment quirks, where credentials live (never the secrets themselves).
- Rulings made and their reasoning (SDD ledger `Ruling:` lines).
- Failure signatures: symptom → root cause → fix.
- Your human partner's preferences and corrections.

## Step 3: Persist

Two stores, two purposes:

1. **Project folder:** `docs/smartpowers/learnings/YYYY-MM-DD-<topic>.md` — the full evaluation: performance answers, rulings, follow-ups. Commit it with the work.
2. **Memory store:** if your harness has persistent memory, save only the durable cross-session facts — one or two sentences each. Project-specific detail stays in the project; memory is for what travels.

Format for future-you: context line, the knowledge, the evidence. No narrative retelling of the session.

## Step 4: Feed the Loop

If a learning indicts a skill — a rule was unclear, a check was missing — record the proposed edit in the learnings file and apply it via `smartpowers:writing-skills` when authorized in the current scope; otherwise preserve it as a follow-up. Learnings that never change the system are trivia.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Nothing new happened this session" | Skip a separate learning artifact when there is no durable learning; retain the run evidence. |
| "I'll remember it" | You won't — context resets. The file remembers. |
| "Too busy wrapping up" | Five minutes now beats re-deriving it under pressure later. |

