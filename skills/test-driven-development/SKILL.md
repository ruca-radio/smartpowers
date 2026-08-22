---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code.
---

# Test-Driven Development

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if the test is valid.

**Required:** Read `smartpowers:core-principles` and `smartpowers:discipline-template` before proceeding. This skill applies the discipline pattern to TDD.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

## RED → GREEN → REFACTOR

**RED:** Write one minimal test showing what should happen.
- One behavior per test
- Clear name describing behavior
- Real code (no mocks unless unavoidable)

**Verify RED (mandatory):** Run the test. Confirm it fails for the expected reason (feature missing, not typo). If it passes, fix the test. If it errors, fix the error first.

**GREEN:** Write the simplest code to pass the test. No extra features, no refactoring, no "improving" beyond the test.

**Verify GREEN (mandatory):** Run the test. Confirm it passes and other tests still pass. Output must be pristine (no errors, warnings).

**REFACTOR:** Clean up after green only. Remove duplication, improve names, extract helpers. Keep tests green. Don't add behavior.

**Repeat:** Next failing test for next feature.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| Minimal | One thing. "and" in name? Split it. | `test('validates email and domain')` |
| Clear | Name describes behavior | `test('test1')` |
| Intent | Demonstrates desired API | Obscures what code should do |

When writing any test, read `writing-good-tests.md` for rules that keep tests honest.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests-after answer "what does this do?" Tests-first answer "what should this do?" You never watched it fail, so you never proved it can catch the bug. |
| "Tests after achieve same goals" | Tests written after are biased by the code you already wrote. Coverage without proof the tests work. |
| "Already manually tested" | Manual testing is ad-hoc, unrepeatable, easy to forget cases under pressure. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping code you can't trust is the waste. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "TDD will slow me down" | TDD catches bugs before commit, prevents regressions, enables fearless refactoring. "Pragmatic" shortcuts mean debugging in production. |

## Red Flags — Stop and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "TDD is dogmatic, I'm being pragmatic"

**All of these mean: Delete code. Start over with TDD.**

## Verification Checklist

Before marking work complete:
- [ ] Every new function has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass
- [ ] All tests pass, output pristine
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression. Never fix bugs without a test.
