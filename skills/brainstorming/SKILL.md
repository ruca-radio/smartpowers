---
name: brainstorming
description: Use before any creative work — creating features, building components, adding functionality, or modifying behavior.
---

# Brainstorming Ideas Into Designs

Turn ideas into fully formed designs through collaborative dialogue. Get approval before implementation.

## Three Paths

Classify before your first question. Say the classification out loud so your human partner can override.

| Path | When | Output | Approval |
|------|------|--------|----------|
| **Spike** | "Can we...", "is it possible...", quick feasibility | Answer, not kept code | Nod |
| **Bounded** | Well-scoped change to existing code in this repo | Short design in chat | Explicit yes |
| **Architectural** | New projects, subsystems, interface changes | Written spec + plan | Spec review |

**Ratchet rule:** Hidden complexity upgrades the path mid-task. Stop, say so, step up. Nothing downgrades.

## Anti-Pattern: "Too Simple To Need Approval"

Every path ends with approval. A todo list, a single function, a config change — the design may be two sentences, but you must present it and get approval. What scales with simplicity is the artifact, never the gate.

## Checklist by Path

**Spike:**
1. Explore project context
2. Present question + probe plan (2-3 sentences)
3. Get approval
4. Investigate as cheaply as correctness allows
5. Report findings; label anything built as throwaway

**Bounded:**
1. Explore project context (files, docs, recent commits)
2. Ask clarifying questions — one at a time
3. Present short design in chat (approach, files, testing)
4. **Get approval — STOP and wait for explicit yes**
5. Implement via normal workflow (TDD applies; no plan document)

**Architectural:**
1. Explore project context
2. Ask clarifying questions — one at a time, understand purpose/constraints/success
3. Propose 2-3 approaches with trade-offs and recommendation
4. Present design in sections; get approval after each
5. Write design doc to `docs/smartpowers/specs/YYYY-MM-DD-<topic>-design.md`
6. Self-review: placeholder scan, consistency, scope, ambiguity
7. User reviews written spec
8. Invoke `writing-plans` skill

## Design Principles

- **Decompose first:** If the request describes multiple independent subsystems, flag immediately. Decompose into sub-projects, then brainstorm the first.
- **YAGNI ruthlessly:** Remove unnecessary features from every approach.
- **Design for isolation:** Each unit has one clear purpose, well-defined interface, testable independently. If you can't explain what it does without reading internals, the boundary needs work.
- **Follow existing patterns:** In existing codebases, match established style. Include targeted improvements only when they serve the current goal.

## Red Flags

| Thought | Reality |
|---------|---------|
| "This is too simple to need a design" | Simple means a short design, not no design. |
| "I'll call it bounded and skip the spec" | Reaching for a label to skip work IS the doubt — take the heavier path. |
| "It's bounded and the design is obvious — I'll start while they read it" | The gate is the approval, not the design's length. Present, then stop until yes. |
| "I understand this kind of app, so it's bounded" | Bounded measures the repo, not your familiarity. A new project has no existing flow — it is architectural. |
| "The spike works, so I'll keep the code" | A spike's output is an answer. Keeping the code is a new request — classify it. |

## Visual Companion (Optional)

Browser-based tool for mockups and diagrams. **Offer just-in-time only** — when a question would genuinely be clearer shown than told. Do not offer upfront.

> "This next part might be easier if I show you — mockups, diagrams, comparisons in a browser tab. Want me to?"

Wait for response. If accepted, read `visual-companion.md` before proceeding.
