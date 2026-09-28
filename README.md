# Smartpowers 2.0

Portable skills and an optional durable runtime for autonomous, multi-model agent workflows.

Smartpowers separates **roles**, **models**, **providers**, and **harnesses**. Use the Markdown skills with your existing agent, or install the runtime to coordinate workers, dependencies, provider fallback, persistent messages, and restart recovery.

## What ships

- 27 portable skills covering design, implementation, review, debugging, collaboration, and paid advertising.
- Scope-based autonomy: continue authorized work without repeated approval menus; supervised checkpoints remain available.
- Python runtime with no third-party runtime dependencies, SQLite task leases, attempt fencing, event history, dependency scheduling, and exclusive resource ownership.
- Command adapter for headless agents, external-worker protocol for other harnesses, and an OpenAI-compatible HTTP adapter for text tasks.
- Capability/context filtering and configurable target priorities; bounded fallback only for retry-safe tasks.
- Persistent reports and recipient-addressed mailboxes with explicit acknowledgements.
- Recoverable skill installation and standalone plan/review helpers.

## Install skills

Requires Python 3.10+, Bash, and a Unix-like system for installer/helper locking.

```bash
bash install.sh                         # Existing Kimi profile
bash install.sh --claude                # Existing Claude profile
bash install.sh --cursor                # Skills; preamble is manual
bash install.sh --target /path/to/skills --instructions /path/to/AGENTS.md
bash install.sh --target /path/to/skills --link
bash install.sh --target /path/to/skills --uninstall
```

Confirm the skill discovery path for your installed harness version. A custom `--target` does **not** modify a default harness's global instructions. Specify `--instructions` to bind a preamble, or add `preamble/AGENTS.snippet.md` yourself. Repeated installs remember an explicit instruction-file binding.

Upgrades preserve previous managed files under the target's `.smartpowers-backups/`. Unmanaged name collisions fail without overwriting the existing skill. The legacy line-based manifest is recognized. Uninstall preserves unrelated files and archives removed managed files.

## Install the optional runtime

```bash
python3 -m pip install .
smartpowers --version
smartpowers validate examples/local-workflow.json
smartpowers start examples/local-workflow.json
```

Alternatively, run `python3 -m smartpowers` from this checkout. Run the example from the repository root; it uses a deterministic local worker and makes no provider calls. `start` prints the run ID before execution. Workflows and CLI responses use protocol version **1**; the package release is **2.0.0**.

```bash
smartpowers status RUN_ID
smartpowers resume RUN_ID --workers 4
smartpowers events RUN_ID
smartpowers export RUN_ID
```

The default database is `.smartpowers/state.db`. Use `--db PATH` **before** the command to share state across harnesses. Results live beside it under `artifacts/`. Keep both; Git does not back up ignored runtime state.

## Execution targets

| Adapter | Integration | Evidence level |
|---|---|---|
| `command` | Headless executable; versioned JSON or prompt/text stdin/stdout | Tested with real local subprocesses |
| `external` | Any harness able to run the claim/heartbeat/complete CLI or Python API | Tested across separate controller/worker processes |
| `openai-compatible` | Configured chat-completions URL and environment-based credentials | Tested against a local HTTP fixture; no live provider certification |

A command worker can use its harness's tools. The direct HTTP adapter is text-only and does not implement a tool-calling loop. Native Codex, Claude, Kimi, OpenCode, Pi, and other agents can use the skills or external-worker protocol; there are no hard-coded vendor CLI flags. Configure and verify your installed CLI's headless/model flags before using the command adapter.

## Autonomy and capabilities

The skills default to proceeding within the user's requested scope. The runtime requires an explicit provider and capability grant in each workflow. `autonomous` executes eligible tasks; `supervised` requires task approval. These grants select workers; they are **not an operating-system sandbox**. Configure the actual harness/tool permissions separately.

Capability names are extensible strings. There is no vendor whitelist or fixed tool catalog. An adapter cannot grant unavailable tools, credentials, or model features. Use an authorized alternate target or surface a concrete blocked state.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 skills/writing-skills/scripts/skill-lint skills
```

See [runtime contracts and operations](docs/runtime.md), [migration and limitations](docs/migration-v2.md), and [release notes](CHANGELOG.md). The paid-advertising domain pack is retained from v1; its domain claims are not revalidated by the v2 runtime tests.

MIT — see [LICENSE](LICENSE).
