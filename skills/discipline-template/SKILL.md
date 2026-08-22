---
name: discipline-template
description: Use when writing a skill that enforces a rule agents skip under pressure. The shared enforcement pattern.
---

# Discipline Enforcement Pattern

Use this structure when a skill must enforce a rule agents tend to skip under pressure.

## 1. State the Rule Clearly

```
NO [ACTION] WITHOUT [PREREQUISITE] FIRST
```

## 2. Close Loopholes Explicitly

- Don't keep it as "reference"
- Don't "adapt" it while doing it right
- Don't look at it
- Delete means delete

## 3. Rationalization Table

Capture exact excuses from baseline testing:

| Excuse | Reality |
|--------|---------|
| "Too simple to need this" | Simple things break. The check takes 30 seconds. |
| "I'll do it after" | After proves nothing. You never watched the failure. |
| "This is different because..." | It isn't. Follow the rule. |

## 4. Red Flags — Stop and Restart

- [Action] before [prerequisite]
- "I already manually checked it"
- "[Prerequisite] after achieves the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing"

**All of these mean: Delete work. Start over with the rule.**
