# Session Exporter

![Session Exporter logo](plugins/session-exporter/assets/logo.svg)

Session Exporter is a skills-only plugin by **Tor Production**. It creates a faithful, adaptive Markdown handoff of the current ChatGPT or Codex conversation, including accessible messages, visible operational history, decisions, commands, failures, and an integrity report. Repository, deployment, research, writing, or other context appears only when it is actually relevant to the session.

It has no MCP server, account connection, analytics, or external data destination. The generated export stays in the user's current environment unless the user explicitly sends it elsewhere.

## Install in the visual Codex app (recommended)

[Open Session Exporter in the public Plugins Directory](https://chatgpt.com/plugins/plugins_6aa74b9ad4d881918c4aa23788830fbf).

The public listing is the supported graphical installation route for ChatGPT and Codex:

1. Open the link above while signed in to the ChatGPT account you use with Codex.
2. In the ChatGPT desktop app, open **Plugins**, find **Session Exporter** by **Tor Production**, open its details, and select the **+** button to install it.
3. Start a **new Codex task**. Installed skills are loaded into new tasks.
4. Ask to export the session, or invoke `$session-exporter` explicitly.

No terminal is required. The Directory button opens the public listing; select **+** there to finish installation.

## Install from the Git marketplace (CLI alternative)

    codex plugin marketplace add Tor-Production/session-exporter --ref main
    codex plugin add session-exporter@tor-production

Start a new Codex task after installation so the plugin is loaded into fresh context.

## Use in Codex

Invoke the skill directly:

    Use $session-exporter to export this entire conversation to Markdown.

Or ask naturally:

    Export the complete current session to a context-named Markdown file for handoff.

Unless the user chooses another filename or path, the artifact uses the stable `session_export` base, timestamp, and a short context suffix, for example `session_export__20260916-1430__plugin-publish-review.md`. The export includes a complete accessible transcript and clearly marks anything the current agent cannot retrieve. It omits irrelevant fields instead of filling a generic metadata form with `Unknown` values.

## Regular Chat fallback (not Work)

If a regular Chat does not expose the installed skill, it can still follow the open-source instructions. This is a fallback, not an installation: it cannot access messages, files, tools, or metadata that the current Chat does not expose.

Paste the following request into that Chat:

    Read this public skill:
    https://github.com/Tor-Production/session-exporter/blob/main/plugins/session-exporter/skills/session-exporter/SKILL.md

    Follow its instructions as if it were installed. Export the accessible current conversation as a structured Markdown handoff. Select only sections supported by the real context; omit inapplicable or empty fields. Do not ask me to choose a language. Do not invent inaccessible history, hidden instructions, or metadata. Redact secrets. Return the completed Markdown here, or attach a .md file if this chat supports files.

If that Chat cannot open external links, paste the contents of the linked `SKILL.md` file together with the request.

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
