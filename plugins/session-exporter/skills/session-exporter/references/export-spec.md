# Session export specification

Use this specification whenever the skill creates an export. Completeness and fidelity take priority over brevity, subject to the data and safety boundaries in `SKILL.md`.

## Core requirement

The primary artifact is the actual accessible conversation history, not a summary of it.

Include every accessible interaction in chronological order:

- every user message;
- every visible assistant or agent response;
- every visible agent status or progress update;
- commands proposed or executed;
- important visible tool calls and associated outputs;
- errors, warnings, and test results;
- Git, pull request, release, and deployment activity;
- URLs, decisions, corrections, and rejected or superseded instructions;
- failed approaches as well as successful ones.

Do not paraphrase transcript entries, collapse them into bullet summaries, omit apparently repetitive messages, or select only the messages judged important. Preserve original Markdown and code fences when accessible.

If exact content is unavailable, insert this marker at the correct chronological position:

`[Original content unavailable to the current agent. The existence of this interaction is known, but its full text cannot be recovered.]`

Never include hidden system or developer instructions, private chain-of-thought, internal policy text, credentials, secret values, or unrelated private data. Acknowledge intentional redactions in the integrity report.

## Required document structure

# Session Export

## 1. Export Metadata

Record the following when applicable:

- Export date and time, including timezone when known
- AI, agent, and product
- Project name
- Repository name and URL
- Local repository or workspace path
- Current branch
- Current HEAD commit SHA
- Relevant base or default branch
- Current pull request number and URL
- Production URL
- Staging URL
- Preview or development URLs
- Relevant API, service, dashboard, and documentation URLs
- Deployment platform or platforms
- Relevant runtime, language, and framework versions
- Current environment
- Current task, issue, or ticket
- Related issue and pull request URLs
- Important external services and integrations
- Other identifiers needed to continue the work

For an unknown field, write exactly:

`Unknown / not established in this session`

Never infer a value merely to fill the template.

## 2. Executive Summary

Write a compact, information-dense overview of:

- what the project is;
- what the session attempted;
- what was completed;
- what remains in progress, failed, or unresolved;
- important technical decisions and constraints;
- current repository and deployment state;
- what the next agent must understand before acting.

This section is an overview only and must not replace or shorten the transcript.

## 3. Current State

Use these subsections:

### Completed

Only work definitively finished.

### In Progress

Work started but not finished.

### Pending / Next Steps

Remaining actions in useful order.

### Blockers

Anything that currently prevents progress.

### Manual Actions Required

Anything only the user or another authorized person can perform.

### Verification Status

Distinguish clearly among:

- implemented;
- locally tested;
- remotely tested;
- staging verified;
- production verified;
- not yet verified.

Never call something verified without evidence from the session.

## 4. Key Decisions and Constraints

For each material decision, include when available:

- the decision;
- its reason or context;
- alternatives discussed;
- consequences;
- whether it is final or provisional.

Also preserve explicit user preferences and constraints that shaped the work.

## 5. Repository / Git / Deployment State

Capture all available continuation-relevant state:

- repository and remotes;
- branch and HEAD SHA;
- working tree state;
- commits created or pushed;
- branches created;
- pull requests created, updated, merged, or closed;
- tags and releases;
- deployment, staging, and production state;
- environment configuration changes and migrations;
- required secrets or configuration names.

Never print secret values, passwords, API keys, tokens, cookies, private credentials, or equivalent authentication data. Use a descriptive placeholder such as:

`DISCORD_TOKEN - required secret, value intentionally omitted`

## 6. Important Files and Components

List the files, directories, modules, scripts, configuration, documentation, and infrastructure components materially involved. Briefly state why each matters. Do not reproduce entire source files unless their content was explicitly part of the conversation.

## 7. Commands and Operational Procedures

Collect important commands and procedures used or established for:

- build, test, lint, and local development;
- deployment and rollback;
- database or migration work;
- Git and GitHub operations;
- environment setup.

Preserve exact commands when accessible. If a visible command contained a secret literal, redact only the secret value and disclose that redaction.

## 8. COMPLETE CHRONOLOGICAL TRANSCRIPT

This is the most important section. Include the complete accessible conversation from the beginning of the scoped session through the latest interaction represented.

Use this format:

```markdown
## Interaction 001

### HUMAN

<full original user message>

### AI / AGENT

<full original visible assistant or agent response>

### TOOL / TERMINAL / SYSTEM OUTPUT

<visible output associated with this interaction, when accessible and relevant>

---
```

Continue with zero-padded sequential interaction numbers. Omit a role subsection only when that interaction genuinely has no content for the role; do not insert invented text.

Transcript rules:

1. Preserve original wording whenever it is accessible.
2. Do not summarize a message instead of reproducing it.
3. Do not silently skip known messages.
4. Preserve Markdown, prompts, code blocks, commands, and URLs.
5. Preserve error messages, corrections, contradictions, and abandoned plans.
6. Preserve messages even when later obsolete.
7. Label HUMAN, AI / AGENT, and TOOL / TERMINAL / SYSTEM OUTPUT clearly.
8. Do not merge separate interactions into a synthesized entry.
9. Place unavailable markers where the missing content belongs.
10. Include tool output only when visible to the user and relevant to the interaction; never expose hidden implementation traces.
11. Redact secret values while preserving the fact and context that a secret was present.
12. Do not reproduce hidden system messages under the `SYSTEM OUTPUT` label; that label is only for visible operational output.

## 9. Timeline of Material Actions

After the raw transcript, provide a concise chronological index of material actions. Include requests, inspections, implementation, commits, pull requests, manual testing, failures, fixes, deployments, and unresolved operational steps. This timeline must not replace the transcript.

## 10. Open Questions / Uncertainties

List facts the next agent must not assume, including untested work, unverified URLs, possible external branch changes, unfinished manual steps, and conflicting requirements.

## 11. Handoff Instructions for the Next AI

Address the next AI or agent directly and state:

- what to read first;
- what state to assume;
- what to verify before changing anything;
- what not to redo unnecessarily;
- which unresolved work should probably happen next.

Base every instruction on session evidence.

## Completeness audit

Before finishing, verify all of the following:

- The executive summary is present.
- Project, repository, and deployment metadata are included or explicitly unknown.
- Current state and verification levels are distinguished.
- Key decisions and constraints are recorded.
- Git and deployment state are recorded.
- Every accessible HUMAN message is present.
- Every accessible AI / AGENT response is present.
- Accessible prompts, code, commands, URLs, failures, and corrections are preserved.
- Final interactions are present, not just early context.
- Transcript entries have not been replaced with summaries.
- Known inaccessible content is explicitly marked.
- Secret values and hidden instructions are absent.
- No metadata was invented.

At the very end, add:

## Export Integrity Report

Report:

- Number of HUMAN messages exported
- Number of AI / AGENT messages exported
- Number of TOOL / TERMINAL blocks exported
- Earliest interaction represented
- Latest interaction represented
- Whether any known content was inaccessible
- Whether any content was intentionally omitted or redacted, and why
- Whether the transcript is believed to be complete
- Whether the completeness audit passed

Counts must describe blocks actually present in the artifact, not estimates.

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
