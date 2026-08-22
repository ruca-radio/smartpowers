# Evaluation — Iteration 1

Paired with_skill vs baseline run, per SmartPowers' own test-driven skill methodology
(RED = baseline behavior without skill, GREEN = behavior with skill).

## Eval 1: `brainstorming`

**Prompt (both runs):** "Add a favorites feature to my notes CLI — users should be able to
star notes and list all starred notes. It's a single Python file using sqlite. Can you build it?"

**Baseline (no skill):** Dove straight into a complete implementation — `starred` column,
PRAGMA migration, star/unstar commands, argparse wiring, usage examples. No design step,
no approval gate, no classification.

**With skill:** Classified the request aloud as **Bounded**, explored project context first,
found the notes CLI file absent, asked a single clarifying question (one at a time, per the
skill), and **stopped to wait** — no design, no code, per the approval gate.

**Verdict: GREEN.** The skill produces exactly the behavioral contract it encodes:
classification → context → one-at-a-time questions → approval gate before any implementation.
The baseline exhibits the failure mode the skill exists to prevent (unrequested implementation
against unverified assumptions — the baseline even had to invent the CLI's structure).

Artifacts: `with-skill-response.md`, `baseline-response.md` in this directory.

## Structural audit (same iteration)

Independent read-only audit of the full repo: skill-lint 0 errors / 0 warnings across all
16 skills; all cross-skill and file references resolve; style contract holds (no ALL-CAPS
prose, no Graphviz, no SUBAGENT-STOP, no @-refs); all four scripts functionally verified in
a scratch git repo. One blocking finding (script execute bits not preservable on the build
host's filesystem) resolved via README install instruction. Two doc-accuracy findings fixed
(README CI reference, overstated boilerplate-extraction claim). task-brief trailing-section
guard added and tested.
