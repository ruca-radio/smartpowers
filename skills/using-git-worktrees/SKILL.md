---
name: using-git-worktrees
description: Use when starting feature work that needs isolation or before executing implementation plans.
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer native tools. Fall back to git worktree only when no native tool exists.

**Announce:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Step 0: Detect Existing Isolation

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** Check `git rev-parse --show-superproject-working-tree`. If path returned, you're in a submodule — treat as normal repo.

**If `GIT_DIR != GIT_COMMON` (and not submodule):** Already in linked worktree. Skip to Step 2. Report: "Already in isolated workspace at `<path>` on branch `<name>`."

**If `GIT_DIR == GIT_COMMON`:** Normal repo. Ask for consent if no preference declared: "Set up isolated worktree? Protects current branch from changes."

## Step 1: Create Workspace

### 1a. Native Tools (preferred)

If you have a tool like `EnterWorktree`, `WorktreeCreate`, `/worktree`, or `--worktree` — use it. Skip to Step 2.

Native tools handle placement, branching, cleanup. Using `git worktree add` when native exists creates phantom state your harness can't manage.

### 1b. Git Fallback

Only if no native tool exists.

**Directory priority:**
1. User preference in instructions
2. Existing `.smartpowers/worktrees/` or `worktrees/`
3. Default: `.smartpowers/worktrees/`

**Verify ignored:**
```bash
git check-ignore -q .smartpowers/worktrees 2>/dev/null
```
If NOT ignored: add to `.gitignore`, commit, then proceed.

**Create:**
```bash
path="$LOCATION/$BRANCH_NAME"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Sandbox fallback:** If permission error, tell user sandbox blocked it. Work in current directory.

## Step 2: Project Setup

Auto-detect and run:
- `package.json` → `npm install`
- `Cargo.toml` → `cargo build`
- `requirements.txt` → `pip install -r requirements.txt`
- `pyproject.toml` → `poetry install`
- `go.mod` → `go mod download`

## Step 3: Verify Clean Baseline

Run tests. If fail: report, ask whether to proceed. If pass: report ready.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation |
| In submodule | Treat as normal repo |
| Native tool available | Use it |
| No native tool | Git fallback |
| `.smartpowers/worktrees/` exists | Use it (verify ignored) |
| Directory not ignored | Add to `.gitignore` + commit |
| Permission error | Sandbox fallback, work in place |
| Tests fail baseline | Report + ask |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Obviously not in a worktree — no need to check" | Run Step 0. Harness isolation and submodules fool eyeballing. |
| "`git worktree add` is quicker than hunting native tool" | Native tool owns placement, branching, cleanup. Bypassing it creates phantom state. |
| "Directory is surely ignored already" | Run `git check-ignore`. Unignored worktree commits the whole tree. |
| "Workspace is fresh — baseline tests can wait" | Dirty baseline makes every later failure ambiguous. |
