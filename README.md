# Session Exporter

![Session Exporter logo](plugins/session-exporter/assets/logo.svg)

Session Exporter is a skills-only plugin by **Tor Production**. It creates a faithful, adaptive Markdown handoff of the current ChatGPT or Codex conversation, including accessible messages, visible operational history, decisions, commands, failures, and an integrity report. Repository, deployment, research, writing, or other context appears only when it is actually relevant to the session.

It has no MCP server, account connection, analytics, or external data destination. The generated export stays in the user's current environment unless the user explicitly sends it elsewhere.

## Install from the Tor Production marketplace

```powershell
codex plugin marketplace add Tor-Production/session-exporter --ref main
codex plugin add session-exporter@tor-production
```

Start a new Codex task after installation so the plugin is loaded into fresh context.

The plugin is also being prepared for the universal Plugins Directory shared by ChatGPT and Codex. Directory publication requires OpenAI review and approval.

## Use

Invoke the skill directly:

```text
Use $session-exporter to export this entire conversation to Markdown.
```

Or ask naturally:

```text
Export the complete current session to session_export.md for handoff.
```

The default artifact is `session_export.md`. The user can choose another filename or path. The export includes a complete accessible transcript and clearly marks anything the current agent cannot retrieve. It omits irrelevant fields instead of filling a generic metadata form with `Unknown` values.

## Privacy by design

- No remote server, authentication, tracking, or telemetry.
- No automatic upload, publication, email, or synchronization.
- Hidden system instructions and private chain-of-thought are never exported.
- Secret values are redacted even if they occur in visible logs.
- The user controls the generated file and its retention.

Read the full [Privacy Policy](https://tor-production.github.io/session-exporter/privacy.html) and [Terms](https://tor-production.github.io/session-exporter/terms.html).

## Repository layout

```text
.agents/plugins/marketplace.json       Git marketplace catalog
plugins/session-exporter/plugin.json  Portable Agent Plugins manifest
plugins/session-exporter/.codex-plugin/plugin.json
plugins/session-exporter/skills/session-exporter/
docs/                                  Public website and policies
submission/                            OpenAI review materials
scripts/                               Validation and packaging helpers
```

## Validate and package

```powershell
python scripts/validate.py
python scripts/package.py
```

Packaging creates deterministic plugin and skill archives in `dist/` for releases and submission.

## Support

Use [GitHub Issues](https://github.com/Tor-Production/session-exporter/issues) for bugs and feature requests. Security-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) © 2026 Tor Production.
