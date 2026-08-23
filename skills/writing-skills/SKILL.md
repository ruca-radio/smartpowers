---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment.
---

# Writing Skills

## Overview

Writing skills is TDD applied to process documentation.

**Required:** Understand `smartpowers:test-driven-development` and `smartpowers:core-principles` first.

## What Is a Skill?

Reusable technique, pattern, or reference guide. Not a narrative about how you solved something once.

## Directory Structure

```
skills/
  skill-name/
    SKILL.md          # Main reference (required)
    supporting-file.* # Only if needed
```

Flat namespace. Separate files for: heavy reference (100+ lines), reusable tools/scripts.

## SKILL.md Structure

```yaml
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
---
```

**Frontmatter rules:**
- `name`: letters, numbers, hyphens only
- `description`: Third-person, "Use when..." format. **NEVER summarize workflow.** Describe the problem/situation only. Max 500 characters.

```yaml
# ❌ BAD: Summarizes workflow
description: Use for TDD - write test first, watch it fail, write minimal code

# ✅ GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

## Skill Discovery Optimization (SDO)

### Description Field

Agents read descriptions to decide which skills to load. Answer: "Should I read this skill right now?"

- Start with "Use when..."
- Concrete triggers, symptoms, situations
- Problem-focused, not technology-specific (unless skill is)
- Third person

### Keyword Coverage

Use words agents search for: error messages, symptoms ("flaky", "hanging"), synonyms, tool names.

### Naming

- Active voice, verb-first: `creating-skills`, `condition-based-waiting`
- Gerunds for processes: `debugging-with-logs`

### Token Efficiency

**Targets:**
- Bootstrap skills: <250 words
- Frequently-loaded: <400 words total
- Other skills: <800 words
- Keep high-churn skills ~5% under target — a field fix should land without a compression pass

**Techniques:**
- Move details to tool help (`--help`) instead of inline docs
- Cross-reference other skills by plain name, not `@` links (force-loads, burns context)
- One excellent example, not multi-language
- Eliminate redundancy — don't repeat cross-referenced skills

## Match the Form to the Failure

| Baseline failure | Right form | Wrong form |
|---|---|---|
| Skips rule under pressure | Prohibition + rationalization table + red flags | Soft guidance ("prefer...", "consider...") |
| Wrong output shape | Positive recipe: state what output IS, in order | Prohibition list ("don't restate") |
| Omits required element | Structural: REQUIRED field in template | Prose reminder near template |
| Behavior depends on condition | Conditional on observable predicate | Unconditional rule + exemption |

**Rules for whichever form:**
- No nuance clauses. "Don't X unless it matters" reopens negotiation.
- Exemption clauses don't scope. If part of output must be exempt, restructure so the rule can't reach it.

## Bulletproofing Against Rationalization

For discipline-enforcing skills, use the pattern in `smartpowers:discipline-template`:
1. State rule clearly
2. Close loopholes explicitly
3. Build rationalization table from baseline testing
4. Create red flags list

## RED-GREEN-REFACTOR for Skills

### RED: Baseline

Run pressure scenario WITHOUT skill. Document:
- What choices did they make?
- What rationalizations (verbatim)?
- Which pressures triggered violations?

### GREEN: Minimal Skill

Write skill addressing specific rationalizations. Don't add hypothetical content. Run same scenarios WITH skill. Verify compliance.

### REFACTOR: Close Loopholes

Find new rationalization → add explicit counter → re-test.

### Micro-Test Wording

Before full pressure scenarios, verify wording with 5+ one-shot samples per variant. Always include no-guidance control. Read every flagged match manually. Variance is a metric: five different interpretations means wording isn't binding.

## Skill Creation Checklist

Create a todo for each item.

**RED Phase:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run WITHOUT skill — document baseline behavior verbatim
- [ ] Identify rationalization/failure patterns

**GREEN Phase:**
- [ ] Name: letters, numbers, hyphens only
- [ ] YAML frontmatter with `name` and `description` (max 1024 chars total)
- [ ] Description: "Use when...", third person, triggers only, no workflow
- [ ] Keywords throughout
- [ ] Clear overview, core principle
- [ ] Address specific baseline failures
- [ ] Guidance form matches failure type
- [ ] Behavior-shaping guidance: micro-tested (5+ reps, manual review)
- [ ] One excellent example (not multi-language)
- [ ] Run WITH skill — verify compliance

**REFACTOR Phase:**
- [ ] New rationalizations from testing → explicit counters
- [ ] Rationalization table built from all iterations
- [ ] Red flags list created
- [ ] Re-test until bulletproof

**Quality:**
- [ ] Flowchart only if decision non-obvious (text-based, not Graphviz)
- [ ] Quick reference table
- [ ] Common mistakes section
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference
- [ ] Token count checked (`wc -w`)

**Deployment:**
- [ ] Run `scripts/skill-lint skills/` — fix every finding
- [ ] Commit and push
- [ ] Do NOT create multiple skills in batch without testing each
