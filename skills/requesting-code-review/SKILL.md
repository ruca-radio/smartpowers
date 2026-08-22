---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements.
---

# Requesting Code Review

## Overview

Dispatch a code reviewer subagent to catch issues before they cascade. Give precisely crafted context — never your session history.

**Core principle:** Review early, review often.

## When to Request

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

1. **Get git SHAs:**
   ```bash
   BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
   HEAD_SHA=$(git rev-parse HEAD)
   ```

2. **Dispatch reviewer** using template at `code-reviewer.md` with:
   - `{DESCRIPTION}` — brief summary
   - `{PLAN_OR_REQUIREMENTS}` — what it should do
   - `{BASE_SHA}` — starting commit
   - `{HEAD_SHA}` — ending commit

3. **Act on feedback:**
   - Critical: fix immediately
   - Important: fix before proceeding
   - Minor: note for later
   - Push back if wrong (with reasoning)

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll review the diff myself" | You're the coordinator — inline review burns context you need to drive work. Dispatch a reviewer: diff and evaluation live in its context, only findings come back. |
| "Reviewer needs my session history" | Hand precisely crafted context, never history. Keeps reviewer on work product, not your thought process. |

## Red Flags

- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback
