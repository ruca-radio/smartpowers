---
name: subagent-driven-development
description: Use when executing an implementation plan through agents with per-task verification and recovery.
---

# Subagent-Driven Development

Apply `smartpowers:core-principles`. Use inline execution for tightly coupled or small tasks; delegate when it improves throughput or independent judgment.

## Persistent setup

Isolate writers with worktrees or explicit resource ownership. Run `scripts/sdd-workspace PLAN_FILE` to create or resume a persistent run. It prints an absolute path, changes no Git index, and creates no commit. Use --new for a separate run of an unchanged plan.

Keep progress, authorization, rulings, agent identities, attempts, and verification in that workspace. Changed plan content gets a new identity; reconcile reusable prior work explicitly. Never delete run evidence on completion. Git-ignored files are not backed up by commits.

When the optional runtime is present, use its task leases, event history, and mailboxes instead of concurrent writes to a Markdown ledger. Keep a readable summary alongside runtime state.

## Dispatch

Use `scripts/task-brief PLAN_FILE N` for task extraction. Add relevant global constraints, interfaces, decisions, provider permissions, acceptance criteria, and report destination. Supply minimum sufficient context; selectively include prior findings when the task needs them.

Select an eligible model/provider/harness for the role. Respect explicit model choices and host dispatch restrictions. Capability and context fit precede price; use observed task success to improve routing.

Nested delegation and peer messages are allowed when the harness supports them and the task's resource budget permits them. Keep one owner per output. Delegate scope, not additional authority.

## Results and review

Treat DONE as a claim until verified. NEEDS_CONTEXT means answer the missing question; BLOCKED means diagnose the actual cause. Separate provider failures, unavailable tools, ambiguous requirements, and reasoning failures.

Build the review package with `scripts/review-package PLAN_FILE BASE HEAD`; capture BASE at dispatch. Review against acceptance criteria, relevant interfaces, and integration behavior. Use independent review for substantial changes.

Adjudicate disputed findings immediately using evidence. Require correction for valid acceptance failures. Defer non-blocking improvements with a reason and owner; never relabel an unmet acceptance criterion as complete.

Retry only with new information, a narrower task, or a better-fitting target. Set a finite attempt budget. On exhaustion, revise the decomposition or report the concrete blocker. An arbitrary number of failed reviews is not a prerequisite to judgment.

## Coordination and completion

Use dependency gates before consumers run. For shared edits, isolate branches and review integration, or serialize through a resource lease. Persist mailbox messages and decisions that other agents need.

If the harness cannot wake after a turn ends, wait in bounded intervals while work runs. If durable background execution and wake-up are available, checkpoint and use them. Capability detection determines the policy.

Run integrated verification, archive reports, and follow `smartpowers:finishing-work` using existing authorization. State unresolved acceptance failures and consequential rulings clearly.
