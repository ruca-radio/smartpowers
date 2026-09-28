---
name: using-smartpowers
description: Use when starting a session or resuming a Smartpowers task.
---

# Using Smartpowers

Load `smartpowers:core-principles` once for authorization and autonomy rules. Discover relevant skills and read only the ones needed for the current task; avoid loading the entire suite.

| Task | Skill |
|---|---|
| Design or build | brainstorming, then writing-plans when needed |
| Diagnose a failure | systematic-debugging |
| Execute a plan | subagent-driven-development or executing-plans |
| Coordinate agents | orchestrating-agent-swarms |
| Invoke another harness | using-cli-agent-harnesses |
| Finish or resume | verification-before-completion, saving-session-learnings |

Discover the current harness's tools, model-selection support, context limit, persistence, messaging, and wake-up behavior. Platform references are orientation, not capability guarantees:

- `references/kimi-tools.md`
- `references/codex-tools.md`
- `references/pi-tools.md`
- `references/antigravity-tools.md`

The optional Smartpowers runtime exposes versioned JSON contracts through `python -m smartpowers --help`. Native tools, local CLI workers, and external harness workers are valid execution paths. If the runtime is absent, retain a file ledger and use available native tools.

On resumption, read the run record and reconcile active attempts before dispatch. User instructions and granted scope govern workflow choices; skill text never creates extra approval requirements or overrides host permissions.
