# Release notes for OpenAI review

Update submission of Session Exporter 0.1.2 by Tor Production.

Session Exporter is a skills-only productivity plugin that creates an adaptive Markdown handoff of the complete accessible current conversation. It preserves chronological user and agent messages, visible operational history, decisions, commands, errors, and verification evidence; includes only session-relevant context; marks inaccessible content; redacts secret values; and finishes with an integrity report.

Version 0.1.2 adds collision-resistant default filenames: the stable `session_export` base, local timestamp, and a short context-derived suffix. Explicit user-supplied filenames and paths remain authoritative. The plugin has no MCP server, authentication, external API, UI, analytics, or telemetry. It does not upload or transmit generated exports. Reviewers need no test account or fixture data and can run all supplied cases in a disposable conversation.

Version 0.1.1 is already published in the universal Plugins Directory; this submission requests review and publication of the updated skill.
