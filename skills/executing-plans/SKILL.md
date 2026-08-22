---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints.
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce:** "I'm using the executing-plans skill to implement this plan."

**Note:** If subagents are available, use `smartpowers:subagent-driven-development` instead.

## Process

### Step 1: Load and Review
1. Ensure isolated workspace via `smartpowers:using-git-worktrees`
2. Read plan file
3. Review critically — identify questions or concerns
4. If concerns: raise with human partner before starting
5. If no concerns: create todos and proceed

### Step 2: Execute Tasks

For each task:
1. Mark in_progress
2. Follow each step exactly
3. Run verifications as specified
4. Mark completed

### Step 3: Complete

After all tasks:
- Announce: "I'm using `smartpowers:finishing-work` to complete this work."
- Follow that skill to verify tests, present options, execute choice

## Stop Conditions

Stop immediately when:
- Blocker (missing dependency, test fails, unclear instruction)
- Plan has critical gaps
- You don't understand an instruction
- Verification fails repeatedly

Ask for clarification. Don't guess.

## Revisit Earlier Steps

Return to review when:
- Partner updates plan based on your feedback
- Fundamental approach needs rethinking

Don't force through blockers.
