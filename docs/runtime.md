# Runtime contracts and operations

## Contents

- Workflow contract
- Target adapters
- Worker request and result
- External workers and messaging
- Recovery, cancellation, and ownership
- Authorization and verification

## Workflow contract

Protocol version 1 is independent of package version 2.0.0. A workflow is JSON with:

| Field | Contract |
|---|---|
| `version` | `1` |
| `root` | Existing project directory; resolved at submission |
| `authorization.mode` | `autonomous` or `supervised` |
| `authorization.providers` | Explicit permitted provider identifiers |
| `authorization.capabilities` | Explicit permitted capability strings |
| `targets` | Nonempty array of execution targets |
| `tasks` | Nonempty acyclic graph of tasks |

Each target has `id`, `adapter`, `provider`, `model`, `capabilities`, optional integer `priority` (lower first; default 100), optional `context_tokens`, and `timeout` (seconds, default 300).

Each task has `id`, `prompt`, and optional:

- `role`: descriptive staffing role; separate from model/provider selection.
- `depends_on`: task IDs whose accepted outputs become inputs.
- `requires`: capability strings the target must satisfy.
- `targets`: eligible target IDs; empty means all compatible targets.
- `min_context_tokens`: declared context requirement; values above 1 require an explicit sufficient target capacity. This is a caller estimate, not a tokenizer.
- `workspace`: existing directory within the root, resolved to an absolute path.
- `resources`: exclusive resource names. Tasks with overlapping names cannot run concurrently **within a run**. Give same-checkout writers the same resource; use different worktrees for independent writers. Coordinate separate runs externally.
- `retry_safe`: false by default. True authorizes automatic replay after transient errors or expiry; the task must actually be idempotent or effects must use the stable idempotency key.
- `max_attempts`: positive attempt budget, default 3.
- `approved`: supervised-mode task authorization; false by default.
- `verify`: argv arrays of acceptance commands, run in the task workspace after a claimed successful result. Requires `shell` in authorization capabilities. Each command has a 300-second timeout.

An output claim alone is not proof of correctness. Encode executable acceptance checks when possible. For non-executable work, use a separate review task or review the evidence before integration.

## Target adapters

### Command harness

Supply `command` as an argv array; no shell expansion occurs. Use `input: "json"` and `output: "json"` for protocol workers. For an existing headless CLI, `input: "prompt"` sends the prompt plus serialized task context and `output: "text"` captures stdout. Configure vendor-specific model and permission flags explicitly in the argv; the `model` metadata does not inject vendor flags.

Commands inherit the controller environment and use the task workspace. Exit 75 means a temporary failure eligible for retry when the task is retry-safe. Other nonzero exits fail the task. Startup failure and timeout are transient classifications, but replay still requires retry-safe. Output is limited to 2 MiB. Raw stderr is not persisted because CLIs may echo credentials.

### External harness

Set `adapter: "external"`. The scheduler leaves the task available for an external harness worker. Use this for interactive agents, native delegation tools, or harnesses without compatible stdin/stdout modes. The worker uses its own tools and returns the same result contract.

### OpenAI-compatible text provider

Set `adapter: "openai-compatible"`, `url` to the full chat-completions endpoint, and optionally `api_key_env` to an environment variable name. `model` is sent as the request's model. This adapter only supports the `text` capability, sends a user message, and expects `choices[0].message.content` to be text. It has no tool loop, streaming, or vendor-specific reasoning options. Redirects are rejected rather than forwarding authorization to a different endpoint.

401/403/408/429 and 5xx responses permit bounded routing fallback only for retry-safe tasks and already-authorized providers. Error bodies and credential values are not stored. No live provider has been tested as part of this repository's fixture suite.

## Worker request and result

Command workers receive one JSON document on stdin:

```json
{
  "version": 1,
  "run_id": "stable-run-id",
  "attempt_id": "unique-attempt-id",
  "idempotency_key": "stable-run-id:task-id",
  "task": {"id": "task-id", "prompt": "Task", "workspace": "/project"},
  "dependencies": {},
  "authorization": {"mode": "autonomous", "providers": ["local"], "capabilities": ["text"]}
}
```

Fields omitted above for brevity remain present in validated tasks. Command requests also include selected target metadata. All workers return:

```json
{"version":1,"status":"completed","output":"Result or artifact references","evidence":["Observed evidence"]}
```

Statuses are `completed`, `failed`, or `blocked`. The controller runs configured verification before accepting completion. Runtime-generated result artifacts are per-attempt JSON files with paths relative to the database directory. Additional worker-created artifacts should be referenced in output/evidence and preserved by the worker.

## External workers and messaging

Commands below run from the checkout or installed runtime. Replace uppercase identifiers with actual IDs; use the same database in every harness.

```bash
smartpowers --db /project/.smartpowers/state.db claim RUN_ID --owner harness-a --target external-reviewer
smartpowers --db /project/.smartpowers/state.db heartbeat ATTEMPT_ID
smartpowers --db /project/.smartpowers/state.db complete ATTEMPT_ID result.json
smartpowers --db /project/.smartpowers/state.db resume RUN_ID
```

Claim returns a request or JSON null when no work is eligible. Persist it and renew the lease at least every 10 seconds during work (default lease: 30 seconds). `complete` verifies the result and configured acceptance commands, then fences the terminal transition against the active attempt. An expired attempt cannot submit accepted results.

```bash
smartpowers send RUN_ID --sender designer --recipient implementer --correlation interface-v1 --body 'Use the committed interface artifact.'
smartpowers inbox RUN_ID implementer
smartpowers ack RUN_ID implementer MESSAGE_ID
```

Delivery is persistent and at-least-once until acknowledged. Recipients deduplicate by message ID. The mailbox API is a local trusted-worker interface; names are addresses, not authenticated identities. Workers with database access can act with controller authority. Do not expose this CLI as an unauthenticated remote service.

## Recovery, cancellation, and ownership

State changes use SQLite transactions. Each attempt owns a lease; completion and heartbeat require the active, unexpired attempt. Resource claims are derived from running tasks and updated under the same transaction. Keep SQLite on a local filesystem; this is a single-host coordination runtime, not a distributed database.

`resume` recovers expired leases and schedules ready tasks. Completed tasks are not repeated. Retry-safe interrupted work returns to pending while attempt budget remains. Uncertain or exhausted work becomes blocked with retained evidence. Reconcile explicitly:

```bash
smartpowers reconcile RUN_ID TASK_ID --status completed --evidence 'Verified the earlier artifact and acceptance checks.'
smartpowers reconcile RUN_ID TASK_ID --status pending --evidence 'Confirmed no external effect occurred; retry is authorized.'
```

Reconciliation retains prior attempts. It cannot reset the attempt budget; a revised scoped run is required after exhaustion. Dependents blocked only by upstream failure become eligible again after upstream recovery.

`cancel` fences active results immediately. Local command process groups are killed when cancellation is observed on POSIX; Windows cleanup kills the direct process. An in-flight HTTP call can run until its configured timeout, but cannot publish an accepted result after cancellation. External workers must observe failed heartbeat and stop their own tools. There is no promise of exactly-once external effects: stable keys support service-side idempotency, and uncertain effects require reconciliation.

The controller returns durable status when only externally owned work remains. It does not pretend to be an always-on daemon. A supervisor can invoke `resume` when workers complete. CLI `start` and `resume` return 0 for complete, 2 for incomplete/failed/blocked/cancelled; invalid operations return 1. `start --no-run` also returns 2 for a newly pending run.

## Authorization and verification

Routing requires the provider and all declared target capabilities to be granted, plus the task's capabilities to be satisfied. The runtime does not sandbox subprocesses or inspect a harness's tools. Set real permissions in the harness or operating system, and keep target declarations accurate.

Supervised tasks require `approved: true` or an explicit `approve RUN_ID TASK_ID`. Autonomous tasks proceed within the workflow grant. Provider fallback never expands that grant. Workflow configuration is a trusted operator input; model output is a result, not authority to change it.

Use absolute `--db` paths across harnesses. Switching harnesses on the same host preserves root/workspace paths. Moving to another host requires copying the closed/checkpointed database plus artifacts and preserving those paths; automatic path relocation and cross-machine workers are not implemented. `export` is a readable diagnostic snapshot, not a database restore format.
