# Smartpowers 2.0 validation

Validated on 2026-09-28 against the v2 implementation based on upstream a21094a.

## Executable checks

- `python3 -m unittest discover -s tests -v`: 27 tests passed on Python 3.12.
- `python3 skills/writing-skills/scripts/skill-lint skills`: 27 skills, zero errors, zero warnings.
- `python3 -m smartpowers start examples/local-workflow.json`: both dependency-linked tasks completed once.
- Wheel build and isolated-environment installation with `pip install --no-build-isolation --no-deps .`: succeeded; installed console reports 2.0.0.
- `git diff --check`: passed.

The suite covers exclusive concurrent claims, capability/context routing, dependency cycles, safe/unsafe retry, stale completion rejection, finite leases, completion reservation, persistent mailboxes, resource serialization, approval/resumption, reconciliation, command cancellation, controller interruption, and helper/installer regressions.

Integration fixtures exercise two HTTP targets (429 followed by success), redirect rejection, and separate CLI processes for external claim, heartbeat, completion, and controller resumption. Repeated resume leaves completed tasks at one attempt. These are protocol fixtures, not live model-provider evaluations.

## Independent script review

An independent validation pass reproduced an external completion race and nonfinite leases, plus a supervised approval deadlock. All were repaired with regression coverage. A focused re-review found no remaining blocker in those fixes, repeated the original completion race 20 times without duplicate acceptance or artifact inconsistency, and checked expiry/cancellation of completion reservations.

## Workflow forward test

A fresh agent received only the revised skill location, an isolated fixture, and this user task:

> Fix normalize_label so it accepts None and returns an empty string, while preserving existing trimming behavior. Implement and verify the fix locally.

It loaded the relevant skills, reproduced the failing regression, implemented the fix, ran the two unit tests and boundary checks, and completed without requesting user input. It did not modify Smartpowers. This is one behavioral sample, not evidence of universal model compliance. The prior v1 evaluation remains under iteration-1 as historical evidence of the old approval-gate behavior.

## Limits

Only Python 3.12 was executed locally. CI declares Python 3.10, 3.12, and 3.13; its results must be checked separately. No paid/live provider credentials were used. Vendor-specific CLI integrations, distributed hosts, and production workloads were not certified. See docs/migration-v2.md for the implemented boundary.
