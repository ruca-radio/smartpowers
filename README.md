# SmartPowers

A lean, token-efficient agentic skills framework. Same rigor as Superpowers, half the context cost.

## Philosophy

- **Evidence over claims** — verify before declaring success
- **Systematic over ad-hoc** — process prevents thrashing
- **DRY applies to instructions** — say it once, reference it everywhere
- **Calm precision beats shouting** — agents comply with clarity, not volume

## How It Works

1. **using-smartpowers** — loads at session start. Checks for relevant skills before any action.
2. **brainstorming** — classifies work (spike / bounded / architectural), gets approval before implementation.
3. **writing-plans** — breaks approved designs into 2-5 minute tasks with exact file paths and code.
4. **subagent-driven-development** — dispatches fresh subagent per task, two-stage review, ledger-based recovery.
5. **test-driven-development** — RED-GREEN-REFACTOR. No production code without a failing test first.
6. **finishing-work** — verifies tests, presents merge/PR/keep options, cleans up.

## Installation

One command, global install (Kimi Code is the default target):

```bash
./install.sh              # Kimi / Moonshot harnesses -> ~/.agents/skills
./install.sh --claude     # Claude Code -> ~/.claude/skills
./install.sh --cursor     # Cursor -> ~/.cursor/skills
./install.sh --target DIR # any other harness
./install.sh --link       # dev mode: symlink instead of copy
./install.sh --uninstall  # remove everything it installed
```

The installer is idempotent: it runs `skill-lint` as a pre-flight, copies all skills, makes helper scripts executable, installs a managed session-start preamble block into the harness's global instructions file (the portable equivalent of a session-start hook), and verifies every skill landed. Manual install still works: copy `skills/` into your harness's skills path, then `find skills -path '*/scripts/*' -type f -exec chmod +x {} +`.

## Skills Library

### Core workflow

| Skill | When to Use |
|-------|-------------|
| `using-smartpowers` | Every session start |
| `core-principles` | When any skill references shared philosophy |
| `discipline-template` | When a skill needs to enforce a rule |
| `brainstorming` | Before any creative work |
| `writing-plans` | With an approved design, before code |
| `test-driven-development` | Before writing implementation code |
| `systematic-debugging` | When encountering any bug or failure |
| `subagent-driven-development` | Executing plans with independent tasks |
| `writing-skills` | Creating or editing skills |
| `finishing-work` | When implementation is complete |

### Supporting skills

| Skill | When to Use |
|-------|-------------|
| `verification-before-completion` | Before declaring any task complete |
| `using-git-worktrees` | Before feature work needing isolation |
| `executing-plans` | Executing a written plan inline (no subagents) |
| `requesting-code-review` | After tasks, before merges |
| `receiving-code-review` | When responding to review feedback |
| `dispatching-parallel-agents` | Multiple independent tasks, concurrently |
| `sensitive-rd-protocol` | Confidential, NDA-covered, or non-public R&D work |
| `orchestrating-agent-swarms` | Planning, sizing, and running multi-agent swarms |
| `conducting-critical-review` | Adversarial review of agent-built code, with rework authority |
| `saving-session-learnings` | End-of-session evaluation and knowledge persistence |
| `using-cli-agent-harnesses` | Delegating to local CLI agents (Codex, OpenCode, Antigravity) |

Word counts per skill are verified by `skills/writing-skills/scripts/skill-lint` — run it before committing.

After copying or cloning, make the helper scripts executable (git checkouts preserve the bit; archives may not):

```bash
find skills -path '*/scripts/*' -type f -exec chmod +x {} +
```

## What Changed vs. Superpowers

| Issue in Superpowers | SmartPowers Fix |
|---------------------|-----------------|
| Token bloat (~9,500 words loaded) | Shared patterns extracted into `core-principles` and `discipline-template` |
| Repeated "Iron Law" / "No exceptions" / Red Flags boilerplate | Compressed — shared enforcement pattern lives in `discipline-template`; skills keep only rule-specific rationalizations |
| ALL-CAPS brute-force compliance | Calm, precise language + rationalization tables (which actually work) |
| Graphviz flowcharts | Text-based state diagrams and tables (readable, token-efficient) |
| `<SUBAGENT-STOP>` hack | Removed — belongs in harness bootstrap, not skill content |
| Description fields summarizing workflow | All descriptions are trigger-only, per SDO research |
| No shared philosophy skill | Added `core-principles` — said once, referenced everywhere |
| Platform fragmentation | Harness-agnostic skills; platform notes in `using-smartpowers` only |
| No enforcement of token targets | `skill-lint` automates the checks |

## Contributing

Follow `writing-skills`. Every skill is test-driven: baseline scenario without the skill, then with. Run `skills/writing-skills/scripts/skill-lint` before committing.

## License

MIT — see [LICENSE](LICENSE).
