# Codex Harness Notes

Discover this installation's version, tool list, context limit, permissions, skill discovery path, model selection, messaging, and background wake-up support. These properties vary by release and surface; do not assume them from the harness name.

Use native delegation when available. Otherwise use the Smartpowers command adapter for a headless CLI, the external worker protocol for an interactive harness, or inline execution. Read the installed CLI help before choosing flags. Do not assume sessions share history or workspaces; pass explicit artifact and interface references.

Install skills into the path this harness actually reads. With a custom target, specify --instructions explicitly to install the preamble; otherwise add it manually. The runtime is optional and separately installed.

Checkpoint before handoff. Wait while workers run if this host cannot wake automatically. When resuming, inspect persisted attempts and reconcile uncertain effects before retrying.
