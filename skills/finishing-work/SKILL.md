---
name: finishing-work
description: Use when work is ready for final verification, integration, and handoff.
---

# Finishing Work

Apply `smartpowers:core-principles`. Determine the requested integration destination from the task, plan, and existing authorization.

Verify the final artifact or tree with the relevant checks. Investigate failures within scope; do not claim completion while acceptance criteria fail. Report unrelated baseline failures separately with evidence.

| Authorized destination | Action |
|---|---|
| Review only | Deliver findings; do not change the project |
| Implementation with branch/PR delivery | Commit scoped changes, push the branch, open/update the PR |
| Explicit merge or deployment | Complete the requested integration and verify the result |
| Local-only | Retain changes and report their location |
| Destination materially unclear | Prepare verified changes, then ask one focused question |

Never require an integration menu when the destination is already established. Do not infer main-branch merge or production deployment from a generic request to implement.

Capture the actual base branch from Git metadata or project configuration. Do not assume it is named main. Check for unrelated changes before staging; stage only the task's files.

Preserve the run record, attempts, review findings, reports, and verification evidence. Archive run data before deleting disposable workspaces. Keep PR worktrees available for feedback. Host-owned workspaces stay with the host.

Remove only worktrees created for this task after their contents are preserved and no active agent owns them. If uncommitted work remains, preserve it and resolve ownership; do not force deletion.

Report what changed, verification results, the branch/PR or artifact, and any unresolved limitations. Use `smartpowers:saving-session-learnings` for reusable findings.
