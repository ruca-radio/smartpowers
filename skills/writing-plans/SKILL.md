---
name: writing-plans
description: Use when you have an approved spec or requirements for a multi-step task, before touching code.
---

# Writing Plans

Write implementation plans assuming the engineer has zero context, questionable taste, and an aversion to testing. Document everything: exact files, complete code, verification steps, test commands.

**Save to:** `docs/smartpowers/plans/YYYY-MM-DD-<feature-name>.md`

## Plan Header

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED: Use `smartpowers:subagent-driven-development` or `smartpowers:executing-plans`.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [Key technologies]

**Spec:** [path to design doc]
```

## Global Constraints

Copy project-wide requirements verbatim: version floors, dependency limits, naming rules, platform requirements. Every task implicitly includes this section.

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [exact signatures from earlier tasks]
- Produces: [exact names/types for later tasks]

- [ ] **Step 1: Write failing test**
  ```python
  def test_behavior():
      result = function(input)
      assert result == expected
  ```
  Run: `pytest tests/path/test.py::test_name -v`
  Expected: FAIL with "function not defined"

- [ ] **Step 2: Write minimal implementation**
  ```python
  def function(input):
      return expected
  ```

- [ ] **Step 3: Verify test passes**
  Run: `pytest tests/path/test.py::test_name -v`
  Expected: PASS

- [ ] **Step 4: Commit**
  ```bash
  git add tests/path/test.py src/path/file.py
  git commit -m "feat: add specific feature"
  ```
```

## Rules

- **Bite-sized:** Each task is one action, 2-5 minutes.
- **No placeholders:** No "TBD", "TODO", "implement later", "add appropriate error handling", "similar to Task N". Every step contains the actual content needed.
- **Self-contained:** An engineer reading one task in isolation has everything required.
- **Task right-sizing:** Fold setup/config/docs into the task whose deliverable needs them. Split only where a reviewer could reject one task while approving its neighbor.

## Self-Review

After writing the plan:
1. **Spec coverage:** Can you point to a task for every spec requirement? List gaps.
2. **Placeholder scan:** Search for red-flag patterns. Fix them.
3. **Type consistency:** Do signatures in later tasks match what earlier tasks define?

Fix inline. No need to re-review — fix and move on.

## Execution Handoff

"Plan complete and saved to `<path>`. Two options:

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks
2. **Inline Execution** — batch execution with checkpoints

Which approach?"
