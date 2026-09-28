# Migrating from v1 to v2

1. Update the repository and rerun the installer against the existing target. Existing line-based manifests are accepted; unmanaged skill-name collisions require manual resolution.
2. For a custom target, explicitly pass the instruction-file path. v2 does not infer a Kimi instruction destination from a custom skills directory. If v1 installed a stray preamble elsewhere, remove that marked block after checking its target.
3. Keep v1 SDD workspaces. v2 keys runs by canonical plan path and content hash with a unique run ID. It does not silently import basename-based ledgers, because they may contain collisions. Review earlier evidence and record adopted results explicitly.
4. Invoke the standalone helper scripts directly or with Python, not with Bash. They require Python 3.10+ and Unix file locking. Git executable bits are included.
5. Read the new core-principles skill. Repeated design and integration menus are removed for already-authorized work. Scope, supervised checkpoints, host permissions, and verification still apply.
6. Install the runtime only if durable cross-harness coordination is needed. Existing skills-only use remains supported.

## What changed

The runtime is new in v2. Roles are distinct from targets; targets specify provider/model/harness capabilities. Task graphs, leases, fenced attempts, persistent mailboxes, provider fallback, and result artifacts are executable features rather than prompt conventions.

Runtime protocol and database schema versions start at 1. Unknown schema versions are rejected. Package version is 2.0.0.

## Deliberate limits

- No vendor-specific CLI flags or live provider certification. Test the actual installed CLI and credentials before production use.
- Direct HTTP is text-only. Tool-using agent work runs through command/external harnesses.
- Target ranking uses declared capabilities, context capacity, and configured priorities. There is no automatic quality/cost-learning optimizer yet.
- SQLite coordination is single-host. Resource locks apply within one run; use separate worktrees or external locking across runs.
- No autonomous daemon, remote authentication server, web dashboard, built-in MCP client, or provider billing meter.
- Runtime authorization is dispatch policy, not a sandbox or a replacement for host permissions.
- External side effects are not exactly-once. Retry-safe declarations and reconciliation are part of the task contract.
- Installation uses per-target locking and rollback on handled failures. Abrupt machine failure during a multi-file upgrade may require restoring the retained backup; there is no filesystem-wide transaction.

These boundaries are explicit so a new harness can integrate against a small, stable contract without relying on unsupported behavior.
