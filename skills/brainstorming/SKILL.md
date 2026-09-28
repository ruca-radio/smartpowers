---
name: brainstorming
description: Use when a request needs design choices before implementing features, components, or behavior changes.
---

# Design Before Implementation

Apply `smartpowers:core-principles` for authorization. Design to resolve uncertainty, then continue with authorized implementation.

| Scope | Design artifact |
|---|---|
| Feasibility question | Evidence-backed answer; exploratory work if needed |
| Bounded change | Short approach with affected interfaces and verification |
| Architecture or subsystem | Written design, contracts, alternatives, acceptance criteria |

Inspect the existing project and relevant requirements. Ask a focused question only when the answer would materially change the implementation and cannot be inferred. Otherwise record a reasonable assumption and proceed.

For architectural work, compare plausible approaches, choose one, and record the tradeoff. Save the design under docs/smartpowers/specs with a dated filename. Break work along independently verifiable interfaces. Preserve the user's full objective when decomposing a large request.

Use `smartpowers:writing-plans` when dependencies or scale warrant a plan. A user who asked you to implement does not need to approve the same work again. Stop for a design review only when requested, when authorization is missing, or when an essential decision is unresolved.

If scope grows, explain the discovery and continue within authorization; ask only for the additional scope that needs a decision. Do not mechanically force a larger process for a small change.

For visual design questions, use a supported preview when it makes the choice clearer. See `visual-companion.md` for an optional browser approach; it does not impose an approval gate.
