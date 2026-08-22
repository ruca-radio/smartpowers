---
name: sensitive-rd-protocol
description: Use when working on confidential, NDA-covered, or otherwise non-public R&D projects, data, or client engagements.
---

# Sensitive R&D Protocol

Handle confidential work so it stays confidential — without stalling it.

**Scope note:** This skill governs *how* work is handled, never *what* work may be done. It does not override safety policies, harness rules, or law, and it never asks the agent to ignore them. Its job is removing the ambiguity that causes stalls on legitimate sensitive work.

## Data Handling

- **Local first:** Keep files, notes, ledgers, and artifacts in the project workspace. No external uploads, third-party API calls, or telemetry containing project data unless your human partner approves each one explicitly.
- **Secrets:** Credentials, keys, and personal identifiers never enter prompts to external services, commits, logs, or shared artifacts. Use `.env` + `.gitignore`. If you find a secret already committed, flag it immediately.
- **Redact at creation:** When producing shareable artifacts (screenshots, logs, status updates), redact client names, identifiers, and unapproved figures when the artifact is created — not later.

## Compartmentalization

- One worktree and branch per engagement. Never mix two clients' data in one workspace.
- Name files, branches, and directories neutrally when the engagement's existence is itself sensitive.
- The SDD ledger accumulates sensitive context. Keep it local; never paste it into external tools.

## Keeping Work Unblocked

- Ambiguity — not policy — causes most stalls on sensitive work. Ask precise scoping questions: what may leave this machine, what may be stored, who may see outputs.
- Record every consent decision as a ledger `Ruling:` entry so approvals survive context compaction and handoffs.
- If a request cannot be fulfilled as stated, say exactly which part and offer the closest legitimate form — a precise alternative beats a vague refusal.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "This API call is harmless" | Harmless-looking calls leak metadata — endpoints, timing, payload shape. Get per-call approval. |
| "I'll redact later" | Later never comes; the artifact gets shared first. Redact at creation. |
| "One workspace is simpler" | Cross-contamination burns engagements. Separate workspaces per client, always. |
| "They obviously approve external tools" | Obvious isn't approval. Ask once, ledger the answer, proceed. |
