---
name: using-cli-agent-harnesses
description: Use when delegating to local CLI agents, external harnesses, or different model providers.
---

# Using CLI Agent Harnesses

Apply `smartpowers:core-principles`. Discover the installed executable's version and help before constructing argv. Do not assume vendor flags, model names, or permission switches.

## Adapters

- Native tools: use the harness's actual delegation and messaging API.
- Command worker: configure an argv array, working directory, timeout, and input/output modes. JSON workers read the versioned request on stdin and return a versioned result on stdout. Prompt/text mode supports simpler headless CLIs; the process exit code is not proof of task acceptance.
- External worker: claim a runtime task, renew its lease, execute using the current harness, then submit the result. Use mailboxes for peer coordination.
- Direct HTTP: the optional OpenAI-compatible adapter returns text only. Use a tool-capable command or external harness for tool execution.

The optional runtime's CLI help and docs/runtime.md in the repository define exact contracts. A skills-only installation does not require the runtime.

## Execution

Brief task, inputs, interfaces, authorization, done criteria, and artifact locations. Use an isolated worktree for writes or declare resource ownership. Never copy credentials into prompts or workflow files; use the harness's credential mechanism or environment-variable references.

Capture results and verify acceptance independently. Preserve output and reports as durable artifacts. Do not claim that a CLI permits resume, messaging, or a model override until discovered.

## Recovery

Auth or quota failure: select another compatible, authorized target if available. Transient errors: bounded retry with new attempt IDs. Invalid output or reasoning: revise context or target and re-verify. Unknown side effects: reconcile before replay. Cancelled or expired attempts cannot publish accepted results.

Use configured provider priorities and context requirements. Explicit user-selected models take precedence. Unsupported capabilities produce a clear blocked result, not an invented success.
