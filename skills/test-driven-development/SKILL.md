---
name: test-driven-development
description: Use when implementing behavior or fixing a bug that needs executable regression coverage.
---

# Test-Driven Development

Apply `smartpowers:core-principles`. Define the expected behavior, reproduce the failure, then implement the smallest correct change.

1. Write a test for the observable contract or bug. Prefer real interfaces over implementation-mirroring mocks.
2. Run it and confirm the intended failure, distinguishing an assertion failure from broken test setup.
3. Implement the fix. Run the focused test and affected integration checks.
4. Refactor only while preserving the verified behavior.

If valid implementation already exists, preserve it and add meaningful coverage; do not delete working code to recreate a test-first chronology. Describe what was actually tested.

Choose checks proportional to risk. Runtime concurrency, persistence, retries, and side effects need executable regression coverage. Prose, formatting, and simple reversible configuration changes may be better verified through inspection or the relevant validator.

Read `writing-good-tests.md` for test design. Exercise failure paths that affect the contract. Do not equate a mocked response with a live provider integration test.

When testing is difficult, simplify the interface or introduce explicit dependencies. Resolve ordinary setup issues autonomously within scope. Ask only when the expected behavior or necessary authority is genuinely missing.

Report exact commands, results, and untested boundaries. Never claim a test was observed failing when it was not run.
