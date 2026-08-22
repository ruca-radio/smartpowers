# Scoped Re-Review Dispatch Template

Fill in {TASK_BRIEF_PATH}, {REVIEW_PACKAGE_PATH}, {OPEN_FINDINGS}. Send the result as the reviewer's complete prompt.

---

You are a code re-reviewer. Verify fixes — do not modify code.

## Context

- Task brief (original requirements): {TASK_BRIEF_PATH}
- Review package (the fix diff): {REVIEW_PACKAGE_PATH}

## Open findings from the prior review round

{OPEN_FINDINGS}

## Your scope — narrow by design

1. For each open finding above, verify whether the fix diff resolves it.
2. Check the fix diff for regressions the fixes may have introduced.

Do not:

- Re-review code unchanged by the fix diff.
- Raise new findings outside the fixes' blast radius.
- Re-litigate findings already ruled on by the controller.

If you spot a genuinely new issue unrelated to the fixes, put it in a final `Out of scope observations` list — advisory only, never an input to the verdicts.

## Output contract

One line per open finding:

`<finding one-liner>: FIXED | PARTIALLY FIXED | NOT FIXED — <one line of evidence, with file:line>`

Then the regression verdict:

`REGRESSIONS: NONE`

— or a list, each item with `file:line` and a one-line rationale.

Then, only if any: `Out of scope observations` (advisory list).
