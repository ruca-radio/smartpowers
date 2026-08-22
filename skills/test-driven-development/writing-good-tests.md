# Writing Good Tests

Rules that keep tests honest.

## Naming

Name the behavior and expected outcome: `test_rejects_empty_email`. Never name the implementation: `test_regex_branch_3`. A reader should know what broke from the failure line alone.

## One Behavior Per Test

One test, one behavior. The "and" heuristic: an "and" in the name means split it. Otherwise the first failing assertion hides everything after it.

## Real Code Over Mocks

Mock only at true system boundaries: network, clock, filesystem, randomness. Everything in between runs for real. A test that mocks its own unit proves nothing about that unit.

Mock-heavy test files are a design signal: the code is too coupled. Fix the design — dependency injection, narrower interfaces — not the test.

## Independence

No test depends on another's order, output, or leftover state. Each arranges its own fixtures. If a test fails when run alone, the suite was lying about coverage.

## Edge Cases Worth Testing

- Empty, zero, and maximum input
- Error paths — the exact error, not "some exception"
- Boundary values — one below, at, and above the limit

## Anti-Patterns

| Habit | Why it lies |
|-------|-------------|
| Asserting on mock calls | Proves wiring, not behavior — refactors break the test while behavior stays correct |
| Overly broad assertions (`assert result is not None`) | Passes on regressions and says nothing when it fails |
| `sleep(2)` to wait for async work | Flaky under load, slow always — poll a condition with a timeout instead |
| Copy-pasted setup across tests | Fixtures drift; a fix in one test silently never reaches the others |
| Testing through private methods | Locks tests to implementation; every refactor becomes a test rewrite |
| One giant end-to-end test | Failures give no location; most behaviors never get isolated coverage |
