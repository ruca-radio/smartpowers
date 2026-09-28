---
name: using-git-worktrees
description: Use when concurrent agents or feature work need isolated Git workspaces.
---

# Using Git Worktrees

Apply `smartpowers:core-principles`. Inspect status, current branch, worktree list, and the actual upstream/base before changing anything.

Use an existing isolated task workspace when suitable. Otherwise create a uniquely named branch and worktree under .smartpowers/worktrees or an explicit user location. Keep the directory locally excluded from Git. Do not create incidental commits merely to configure workspace exclusions.

Capture base commit and worktree ownership in the run record. Assign one writer per worktree unless a shared resource lease serializes access. Shared Git metadata still requires coordinated integration.

Keep unrelated staged and unstaged changes intact. Stage only the task's paths. Never reset, clean, or force-remove user work as setup or cleanup.

Integrate according to existing authorization, verifying the combined tree. Record conflicts and their resolution. Retain worktrees needed for PR feedback or active workers; archive reports before cleanup.

If isolation is unavailable, use explicit exclusive resource ownership and serialize writers. An inability to create worktrees is a capability constraint, not a reason to stop all useful work.
