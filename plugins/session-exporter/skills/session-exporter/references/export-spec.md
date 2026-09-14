# Adaptive session export specification

Use this specification whenever the skill creates an export. The artifact must be a faithful record of the accessible session, shaped by what actually happened in that session. Completeness and fidelity take priority over brevity, subject to the data and safety boundaries in `SKILL.md`.

## Core requirement

The primary artifact is the actual accessible conversation history, not a summary of it.

Include every accessible interaction in chronological order:

- every user message;
- every visible assistant or agent response;
- every visible agent status or progress update;
- commands proposed or executed;
- relevant visible tool calls and associated outputs;
- errors, warnings, and test results;
- decisions, corrections, rejected approaches, and changes in direction;
- Git, pull request, release, deployment, document, research, or other operational activity when it occurred;
- URLs and technical or non-technical context that materially affected the conversation.

Do not paraphrase transcript entries, collapse them into bullet summaries, omit apparently repetitive messages, or select only the messages judged important. Preserve original Markdown and code fences when accessible.

If exact content is unavailable, insert this marker at the correct chronological position:

`[Original content unavailable to the current agent. The existence of this interaction is known, but its full text cannot be recovered.]`

Never include hidden system or developer instructions, private chain-of-thought, internal policy text, credentials, secret values, or unrelated private data. Acknowledge intentional redactions in the integrity report.

## Structure is adaptive, not a questionnaire

The export has four required high-level parts:

1. Session Context
2. Executive Summary
3. COMPLETE CHRONOLOGICAL TRANSCRIPT
4. Export Integrity Report

Everything else is optional. Add an optional section only when it carries established information that meaningfully helps a human or another agent continue, audit, or understand the session.

Do not create a heading, field, table row, or category solely because it appears in this specification. Do not use placeholder metadata such as `Unknown`, `Not established`, `N/A`, `Not applicable`, `None`, blank values, or empty tables. Omit irrelevant information entirely.

For example:

- A casual conversation may only need its subject, key preferences, and transcript.
- A coding session may need repository state, affected files, commands, tests, and deployment information.
- A writing session may need document names, target audience, tone, source material, and editorial decisions.
- A research session may need sources, search scope, assumptions, conclusions, and open questions.
- A troubleshooting session may need environment details, symptoms, attempted fixes, observed results, and remaining failure modes.
- A planning session may need goals, constraints, priorities, decisions, and next actions without any Git or deployment information.

The agent may create descriptive field and section names that fit the session. It must not invent values or infer facts without support from the conversation or directly observable in-scope environment.

## 1. Session Context

Create a concise context block that contains only facts that are both established and useful to the next reader.

Choose the fields dynamically. Possible fields include a task or topic, project or repository, relevant URLs, workspace path, branch or commit, issue or pull request, target audience, source material, selected strategy, operating system, runtime, important tools, date/time context, current task, external service, or document being edited.

These are examples, not a checklist. A non-technical chat may have only a subject and scope. A session with no meaningful structured metadata should keep this section very small rather than adding empty technical categories.

Use generated explanatory prose in the language of the user's current request unless the user explicitly asks for another language. Never pause solely to ask the user to choose an export language. Preserve the original language of every transcript message.

## 2. Executive Summary

Write a compact, information-dense overview tailored to the session. Include only applicable material, such as:

- what the conversation was about;
- what the user was trying to accomplish;
- what was completed, remains unresolved, or changed direction;
- major decisions and constraints;
- current state and what the next agent needs to understand.

Do not force technical categories into a non-technical conversation. This section is only an overview and must not replace or shorten the transcript.

## Optional context sections

Place zero or more optional sections after the Executive Summary and before the transcript. Use only the sections that improve the handoff. Omit empty subsections as well as empty parent sections.

Possible useful sections include:

### Current State

Use when the session produced work with a meaningful end state. Include only applicable details such as completed work, work in progress, next steps, blockers, manual actions, and evidence-backed verification status.

### Key Decisions and Constraints

Use when decisions, alternatives, user preferences, requirements, or tradeoffs will affect future work. Record the decision, reason, consequence, and whether it is final or provisional when that evidence exists.

### Repository, Git, or Deployment State

Use only when repository, Git hosting, pull requests, deployments, environments, migrations, or releases were materially involved. Include only the facts available in the session, such as a repository URL, branch, commit, working tree state, pull request, tag, deployment state, or required configuration names. Never print secret values.

### Important Files, Components, or Documents

Use only when named files, components, documents, or infrastructure materially matter. Briefly explain why each item matters; do not reproduce entire source files unless their content was part of the conversation.

### Commands and Operational Procedures

Use only when the session established commands or procedures another agent should reuse, such as build, test, lint, deployment, rollback, environment setup, or troubleshooting commands. Preserve exact commands when accessible, redacting secret literals only.

### Errors, Failed Attempts, or Rejected Approaches

Use when failed experiments, errors, corrections, or abandoned paths will help prevent repeated work.

### Sources, URLs, or External Services

Use when sources, references, dashboards, APIs, or integrations materially shaped the work. Include only relevant entries.

### Open Questions, Next Steps, or Handoff Instructions

Use when actual uncertainty, unfinished work, or an explicit handoff remains. State what the next agent should read, verify, avoid redoing, or do next, based only on session evidence.

## 3. COMPLETE CHRONOLOGICAL TRANSCRIPT

This is the most important section. Include the complete accessible conversation from the beginning of the scoped session through the latest interaction represented.

Use this general structure:

```markdown
## Interaction 001

### HUMAN

<full original user message>

### AI / AGENT

<full original visible assistant or agent response>

### TOOL / TERMINAL / SYSTEM OUTPUT

<visible output associated with this interaction, when accessible and useful>

---
```

Continue with zero-padded sequential interaction numbers. Omit a role subsection only when that interaction genuinely has no content for the role; do not insert invented text.

Transcript rules:

1. Preserve original wording and language whenever it is accessible.
2. Do not summarize a message instead of reproducing it.
3. Do not silently skip known messages.
4. Preserve Markdown, prompts, code blocks, commands, and URLs.
5. Preserve error messages, corrections, contradictions, and abandoned plans.
6. Preserve messages even when later obsolete.
7. Label HUMAN, AI / AGENT, and TOOL / TERMINAL / SYSTEM OUTPUT clearly when appropriate.
8. Do not merge separate interactions into a synthesized entry.
9. Place the unavailable marker where a known missing interaction belongs.
10. Include visible tool output only when relevant to the interaction; never expose hidden implementation traces.
11. Redact secret values while preserving their non-sensitive operational context.
12. Do not reproduce hidden system messages under the `SYSTEM OUTPUT` label; that label is only for visible operational output.

## Sensitive information

Never print secret values, passwords, API keys, authentication tokens, private credentials, session cookies, private keys, or similar secrets.

If a secret's existence matters to the context, record only its role, for example:

`DISCORD_TOKEN — required secret; value intentionally omitted`

Do not remove surrounding non-sensitive context unnecessarily.

## Completeness audit

Before finishing, verify all of the following:

- Did I preserve every accessible HUMAN message?
- Did I preserve every accessible AI / AGENT response?
- Did I include relevant visible tool or terminal output?
- Did I preserve prompts, code, commands, errors, corrections, and URLs where present?
- Did I include the final interactions, not just early context?
- Did I accidentally summarize any transcript portion instead of reproducing it?
- Did I explicitly mark known inaccessible content?
- Did I avoid exposing secrets, hidden instructions, and private reasoning?
- Did I avoid inventing facts?
- Did I omit irrelevant metadata fields, empty sections, empty tables, and placeholder values?
- Does the context structure reflect the actual conversation rather than a fixed template?

## 4. Export Integrity Report

At the very end, add a concise `## Export Integrity Report` containing only relevant integrity facts:

- Number of HUMAN messages exported
- Number of AI / AGENT messages exported
- Number of TOOL / TERMINAL / SYSTEM blocks exported
- Earliest interaction represented
- Latest interaction represented
- Whether any known content was inaccessible
- Whether any content was intentionally omitted or redacted, and why
- Whether the transcript is believed to be complete
- Whether the completeness audit passed

Counts must describe blocks actually present in the artifact, not estimates. Do not add unrelated metadata to this report.

## Large sessions

Do not intentionally truncate the transcript to keep a chat response short. Write directly to the Markdown artifact whenever possible.

If the full session exceeds what can be accessed or processed in one pass:

1. retrieve or process it in chronological chunks when a supported history capability allows that;
2. merge chunks into one final artifact;
3. export everything accessible;
4. identify every known missing range;
5. preserve chronology;
6. never claim the result is complete when it is not.

Do not stop after producing only the Executive Summary.

## Completion response

After creating the artifact, do not repeat its contents in chat. Report only:

- file link or path;
- whether the completeness audit passed;
- number of HUMAN messages;
- number of AI / AGENT messages;
- whether anything was inaccessible, redacted, or omitted.
