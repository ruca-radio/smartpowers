---
name: finishing-work
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work.
---

# Finishing Work

## Overview

Verify tests → detect environment → present options → execute choice → clean up.

## Step 1: Verify Tests

Run full test suite. If failures, report and stop — menu comes after green.

## Step 2: Detect Environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` | Standard 3 options | None |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 3 options | Provenance-based |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 2 options (no merge) | Leave in place |

## Step 3: Determine Base Branch

Usually named in plan or conversation. If unknown, ask: "This branch split from `<guess>` — correct?"

## Step 4: Present Options

**Normal repo / named branch:**
```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
```

**Detached HEAD:**
```
Implementation complete. Detached HEAD workspace.

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
```

Wait for answer. Discard only on explicit request.

## Step 5: Execute Choice

**Merge locally:**
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch>
git pull
git merge <feature-branch>
# Verify tests on merged result
```

If merged result fails: stop, leave worktree/branch, investigate.

If green: clean up worktree, delete branch: `git branch -d <feature-branch>`

**Push and PR:**
```bash
git push -u origin <feature-branch>
# Create PR against <base-branch>
```

Keep worktree for PR feedback.

**Keep as-is:** Report branch name and worktree path.

**Discard (explicit request only):**
Confirm: "Type 'discard' to permanently delete branch `<name>`, all commits, and worktree."
Wait for exact confirmation. Then clean up worktree and `git branch -D <feature-branch>`.

## Step 6: Cleanup

**If `GIT_DIR == GIT_COMMON`:** Normal repo, nothing to clean.

**If `WORKTREE_PATH` under `.smartpowers/worktrees/`:** We own cleanup:
```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune
```

**If removal refused** (uncommitted files): show `git status`, ask:
1. Commit them
2. Move to main repo
3. Delete them

Never `--force` on your own initiative.

**Otherwise:** Host environment owns workspace — leave in place.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier this session" | Run on the tree you're about to integrate. Green proves the tree it ran on. |
| "They obviously want it merged" | Integration is their decision. Present menu and wait. |
| "The PR is up, worktree is clutter" | PR feedback gets fixed there. It stays until work lands. |
| "Removal refused — `--force` is just cleanup" | Refusal means files exist only there. `--force` destroys them permanently. |
