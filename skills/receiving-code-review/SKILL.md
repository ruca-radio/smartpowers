---
name: receiving-code-review
description: Use when responding to feedback from a code review, whether from a subagent or human partner.
---

# Receiving Code Review

## Overview

Feedback is data, not attack. Extract value, fix real issues, push back on wrong ones.

## Process

1. **Read all feedback first** — don't start fixing while reading. Patterns emerge only when you see the whole picture.
2. **Categorize each finding:**
   - **Correct and important:** Fix immediately.
   - **Correct but minor:** Batch with other minors, fix in one pass.
   - **Wrong or misapplied:** Push back with technical reasoning. Show code/tests that prove it works. Request clarification if unclear.
   - **Out of scope:** Note for later. Don't expand the PR.
3. **Fix in order:** Critical first, then Important, then batched Minors.
4. **Verify after fixes:** Run full test suite. Ensure fixes didn't break anything.
5. **Respond to reviewer:** Address every point — fixed, deferred with reason, or contested with evidence. Silence on a point means you missed it.

## Red Flags

- "The reviewer doesn't understand the codebase" → maybe, but verify your explanation is clear
- "This is just style, ignore it" → consistent style matters for readability
- "Fixing this would require massive refactoring" → might indicate the finding is correct but the scope needs discussion
- "I'll fix the easy ones and ignore the hard ones" → hard findings are often the most valuable

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "They missed the context" | Did you provide it? If not, add context and re-ask. If yes, clarify the specific gap. |
| "This feedback is nitpicky" | Nits aggregate into readability. Batch and fix them efficiently. |
| "I don't have time to address all of this" | Untriaged feedback rots. Sort into fix/defer/contest, then act. |
