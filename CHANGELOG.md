# Changelog

## 2.0.0 — 2026-09-28

- Add an optional dependency-free Python orchestration runtime with versioned workflow/worker contracts.
- Add transactional task claims, attempt fencing, leases, dependency scheduling, explicit resources, recovery, cancellation, and durable event history.
- Add command and external harness adapters, an OpenAI-compatible text adapter, bounded provider fallback, and persistent peer messages.
- Consolidate autonomy/authorization rules and remove redundant approval menus; enable capability-driven collaboration and delegation.
- Preserve SDD reports and run records instead of deleting ignored evidence.
- Fix implicit commits, plan-name collisions, and task extraction under nested headings/fences.
- Make installer custom targets independent of default global instructions; support copy/link upgrades, ownership checks, retained backups, and legacy manifests.
- Add regression tests, local integration fixtures, CI, and migration documentation. Live model-provider compatibility is not claimed by fixture results.
