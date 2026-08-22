---
name: verification-before-completion
description: Use before declaring any task, bugfix, or feature complete.
---

# Verification Before Completion

## Overview

Ensure it's actually fixed, actually working, actually complete — not just apparently so.

**Required:** Read `smartpowers:core-principles` and `smartpowers:discipline-template`.

## The Checklist

- [ ] **Test evidence:** Automated tests pass with pristine output (no warnings, no errors).
- [ ] **Coverage:** The change you made is exercised by a test that would fail if reverted.
- [ ] **Isolation:** Change doesn't break unrelated tests or features.
- [ ] **Edge cases:** Empty input, max input, error paths handled.
- [ ] **Manual spot-check:** If UI/UX changed, verify visually. If API changed, verify with a real request.
- [ ] **Documentation:** README, comments, or specs updated if behavior changed.
- [ ] **Cleanup:** No debug code, no console.logs, no temporary files left behind.

## When to Stop

If you cannot check every box, the task is not complete. Do not rationalize:
- "The warning is unrelated" → fix or explicitly document why it's acceptable
- "I'll clean up later" → later never comes
- "It's obvious it works" → verify anyway

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I already checked it works" | Checked how? Under what conditions? Can you reproduce that check? |
| "The test suite takes too long" | Run the relevant subset. Skipping verification is how regressions ship. |
| "It's just a small change" | Small changes in shared code have large blast radius. Verify. |
| "I'll verify after merge" | Verification before merge is the point. After merge is damage control. |
