---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---

# Systematic Debugging

## Overview

Find root cause before attempting fixes. Symptom fixes are failure.

**Required:** Read `smartpowers:core-principles` and `smartpowers:discipline-template` before proceeding.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Any technical issue: test failures, bugs, unexpected behavior, performance problems, build failures, integration issues.

**Especially when:** under time pressure, "just one quick fix" seems obvious, you've already tried multiple fixes, or you don't fully understand the issue.

## The Four Phases

Complete each phase before the next.

### Phase 1: Root Cause Investigation

**Before any fix:**

1. **Read error messages carefully** — don't skip warnings. Stack traces often contain the exact solution.
2. **Reproduce consistently** — exact steps, frequency, conditions. If not reproducible, gather more data; don't guess.
3. **Check recent changes** — git diff, recent commits, new dependencies, config changes, environmental differences.
4. **Gather evidence in multi-component systems** — At each boundary, log what enters and exits. Run once to see WHERE it breaks, then investigate that component.
5. **Trace data flow** — Where does the bad value originate? Trace up until you find the source. Fix at source, not symptom.

### Phase 2: Pattern Analysis

1. **Find working examples** — similar working code in the same codebase.
2. **Read reference implementations completely** — don't skim. Understand the pattern fully before applying.
3. **Identify differences** — list every difference between working and broken, however small.
4. **Understand dependencies** — what components, settings, assumptions does this need?

### Phase 3: Hypothesis and Testing

1. **Form single hypothesis** — "I think X is the root cause because Y." Write it down. Be specific.
2. **Test minimally** — smallest possible change, one variable at a time.
3. **Verify** — worked? → Phase 4. Didn't? → new hypothesis. Don't add more fixes on top.
4. **Don't know?** Say "I don't understand X." Ask for help. Don't pretend.

### Phase 4: Implementation

1. **Create failing test** — simplest reproduction. Use `smartpowers:test-driven-development`.
2. **Implement single fix** — address root cause. ONE change. No "while I'm here" improvements.
3. **Verify fix** — test passes? No other tests broken? Issue actually resolved? Use `smartpowers:verification-before-completion`.
4. **If fix doesn't work:** STOP. Count attempts.
   - < 3: Return to Phase 1 with new information.
   - **≥ 3: STOP and question the architecture.** Each fix revealing new shared state/coupling indicates a structural problem. Discuss with your human partner before Fix #4.

## Red Flags — Stop and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "One more fix attempt" (when already tried 2+)
- Each fix reveals a new problem in a different place

**All of these mean: STOP. Return to Phase 1.**

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is faster than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |
