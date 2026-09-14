# OpenAI Plugins Directory listing

## Submission identity

- Submission type: Skills only
- Plugin name: Session Exporter
- Technical ID: `session-exporter`
- Publisher: Tor Production
- Category: Productivity
- Version: 0.1.1
- Authentication: None
- Remote MCP server: None
- External data destination: None

## Descriptions

Short description:

> Export a complete conversation to a Markdown handoff.

Long description:

> Create a faithful, chronological Markdown export of the accessible current conversation, decisions, commands, and end state for handoff or audit. Session Exporter adapts context to the actual session, omits irrelevant metadata, marks inaccessible history, redacts secret values, and includes an integrity report. It is a skills-only plugin with no server, sign-in, analytics, or external data transfer.

## Public URLs

- Website: <https://tor-production.github.io/session-exporter/>
- Support: <https://tor-production.github.io/session-exporter/support.html>
- Privacy policy: <https://tor-production.github.io/session-exporter/privacy.html>
- Terms of service: <https://tor-production.github.io/session-exporter/terms.html>
- Source repository: <https://github.com/Tor-Production/session-exporter>

## Brand assets

- Listing logo: `dist/session-exporter-logo.png`
- Source logo: `plugins/session-exporter/assets/logo.png`
- Brand color: `#635BFF`
- Screenshots: None; the plugin has no UI.

## Starter prompts

1. Export this entire conversation to `session_export.md`.
2. Create a complete Markdown handoff for this task.
3. Save this session with Git state, decisions, and every accessible message.

## Data handling summary

The skill processes only content available to the active agent in the current user-scoped conversation and, when relevant, read-only workspace or repository metadata. The generated file remains in the user's current environment. Tor Production receives and retains no conversation data. Secret values, hidden system or developer instructions, and private chain-of-thought are excluded.

## Availability

Select all countries and regions where the OpenAI Plugins Directory permits this general productivity plugin and where the publisher's public terms can be offered. No region-specific service, server, account, or regulated data feature is involved.
