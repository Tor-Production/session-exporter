---
name: session-exporter
description: Export the complete accessible current conversation and end-of-session workspace state to a structured Markdown handoff. Use when the user asks to export, save, archive, transfer, audit, or hand off the current chat or task; do not use for an ordinary summary or for conversations the user has not placed in scope.
---

# Session Exporter

Create one faithful, adaptive Markdown artifact that another AI or human can use to continue, audit, or reconstruct the current conversation. The document must reflect the session that actually occurred, not a pre-filled questionnaire.

## Workflow

1. Read [references/export-spec.md](references/export-spec.md) completely before producing the export.
2. Resolve the scope as the current conversation or task only, unless the user explicitly names additional conversations.
3. Retrieve the fullest accessible history in chronological order. Prefer a first-party current-task history or export capability when available, paging back to the earliest turn. Supplement it with the conversation context already visible to you. Do not inspect unrelated tasks, private databases, browser storage, or undocumented application internals.
4. Gather current workspace and repository metadata with read-only inspection when those resources are in scope. Never mutate Git, deployments, issues, pull requests, or external services merely to create the export.
5. Build the document using the adaptive structure and transcript rules in the reference. Include only context fields and optional sections that are both established and useful for this session. Preserve exact visible wording, code blocks, commands, URLs, errors, corrections, and relevant visible tool output whenever accessible.
6. Run the completeness audit, count exported blocks, and add the Export Integrity Report. If any known range or item is unavailable, say so precisely; never claim completeness without evidence.
7. Unless the user specifies another filename or path, apply the context-derived naming rule in [references/export-spec.md](references/export-spec.md): use a short filesystem-safe context prefix followed by the local export timestamp and the `session_export.md` suffix, such as `session-exporter-plugin__20260916-1430__session_export.md`. Prefer the environment's designated user-facing output directory, then the current workspace. If filesystem output is unavailable, create a downloadable Markdown artifact using the product's supported artifact mechanism.
8. In the final response, report only the artifact link or path, audit result, HUMAN and AI/AGENT counts, and whether anything was inaccessible, redacted, or omitted.

## Data and safety boundaries

- Export only content that is normally visible or otherwise explicitly available to the user in the current conversation. Never expose system or developer prompts, hidden policies, private chain-of-thought, internal reasoning, authentication material, or unrelated account data.
- Secret values remain omitted even if they appear in visible logs. Replace them with a descriptive redaction such as `API_TOKEN - required secret, value intentionally omitted`, and record the redaction in the integrity report.
- Do not upload, email, publish, sync, or otherwise transmit the export unless the user separately asks for that destination.
- Do not fabricate unavailable history or metadata. Use the exact unavailable marker defined in the reference.
- Do not create empty headings, empty tables, or placeholder metadata such as `Unknown`, `Not established`, `N/A`, `Not applicable`, or `None`. Omit irrelevant repository, deployment, technical, or other context entirely.
- Write generated explanatory sections in the language of the user's current request unless the user asks for another language. Preserve the original language of each transcript message. Do not stop to ask a language-selection question.
- Honor an explicit narrower scope, output path, or filename. The user's current request overrides optional defaults in this skill.
- If the environment cannot create or return a file, explain that limitation and provide the most faithful supported alternative without pretending a file exists.
