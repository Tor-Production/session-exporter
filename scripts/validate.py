#!/usr/bin/env python3
"""Validate the Session Exporter marketplace and plugin package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "session-exporter"
SKILL = PLUGIN / "skills" / "session-exporter"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
HTTPS = re.compile(r"^https://")


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing JSON file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"Expected an object in {path.relative_to(ROOT)}")
        return {}
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_manifest(manifest: dict[str, Any], label: str, errors: list[str]) -> dict[str, Any]:
    require(manifest.get("name") == "session-exporter", f"{label}: unexpected plugin name", errors)
    version = manifest.get("version")
    require(isinstance(version, str) and bool(SEMVER.fullmatch(version)), f"{label}: invalid semantic version", errors)
    require(isinstance(manifest.get("description"), str) and len(manifest["description"]) >= 30, f"{label}: description is too short", errors)
    author = manifest.get("author")
    require(isinstance(author, dict) and author.get("name") == "Tor Production", f"{label}: publisher must be Tor Production", errors)
    return manifest


def validate_interface(interface: dict[str, Any], label: str, errors: list[str]) -> None:
    required = (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "websiteURL",
        "privacyPolicyURL",
        "termsOfServiceURL",
        "defaultPrompt",
        "brandColor",
        "composerIcon",
        "logo",
    )
    for key in required:
        require(key in interface, f"{label}: missing interface.{key}", errors)

    require(interface.get("developerName") == "Tor Production", f"{label}: wrong developerName", errors)
    require(interface.get("category") == "Productivity", f"{label}: wrong category", errors)
    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        require(isinstance(interface.get(key), str) and bool(HTTPS.match(interface[key])), f"{label}: {key} must be HTTPS", errors)

    prompts = interface.get("defaultPrompt")
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, f"{label}: defaultPrompt must contain 1-3 prompts", errors)
    if isinstance(prompts, list):
        for index, prompt in enumerate(prompts, start=1):
            require(isinstance(prompt, str) and len(prompt) <= 128, f"{label}: defaultPrompt {index} exceeds 128 characters", errors)

    for key in ("composerIcon", "logo"):
        value = interface.get(key)
        require(isinstance(value, str) and value.startswith("./assets/"), f"{label}: {key} must be under ./assets/", errors)
        if isinstance(value, str) and value.startswith("./"):
            require((PLUGIN / value[2:]).is_file(), f"{label}: missing asset {value}", errors)


def main() -> int:
    errors: list[str] = []

    portable_path = PLUGIN / "plugin.json"
    compatibility_path = PLUGIN / ".codex-plugin" / "plugin.json"
    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"

    portable = validate_manifest(load_json(portable_path, errors), "portable manifest", errors)
    compatibility = validate_manifest(load_json(compatibility_path, errors), "compatibility manifest", errors)

    require(portable.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "portable manifest: wrong or missing schema", errors)
    require(portable.get("repository") == "https://github.com/Tor-Production/session-exporter", "portable manifest: wrong repository URL", errors)
    require(compatibility.get("skills") == "./skills/", "compatibility manifest: skills path must be ./skills/", errors)

    portable_interface = portable.get("extensions", {}).get("com.openai", {}).get("interface", {}) if isinstance(portable.get("extensions"), dict) else {}
    compatibility_interface = compatibility.get("interface", {})
    require(isinstance(portable_interface, dict), "portable manifest: missing OpenAI interface", errors)
    require(isinstance(compatibility_interface, dict), "compatibility manifest: missing interface", errors)
    if isinstance(portable_interface, dict):
        validate_interface(portable_interface, "portable manifest", errors)
    if isinstance(compatibility_interface, dict):
        validate_interface(compatibility_interface, "compatibility manifest", errors)
    require(portable_interface == compatibility_interface, "portable and compatibility interfaces differ", errors)

    marketplace = load_json(marketplace_path, errors)
    require(marketplace.get("name") == "tor-production", "marketplace: name must be tor-production", errors)
    plugins = marketplace.get("plugins")
    require(isinstance(plugins, list) and len(plugins) == 1, "marketplace: expected one plugin entry", errors)
    if isinstance(plugins, list) and plugins:
        entry = plugins[0]
        require(entry.get("name") == "session-exporter", "marketplace: wrong plugin name", errors)
        require(entry.get("source") == {"source": "local", "path": "./plugins/session-exporter"}, "marketplace: wrong local source", errors)
        require(entry.get("policy", {}).get("installation") == "AVAILABLE", "marketplace: installation must be AVAILABLE", errors)
        require(entry.get("policy", {}).get("authentication") == "ON_INSTALL", "marketplace: authentication must be ON_INSTALL", errors)
        require(entry.get("category") == "Productivity", "marketplace: wrong category", errors)

    skill_path = SKILL / "SKILL.md"
    reference_path = SKILL / "references" / "export-spec.md"
    agent_path = SKILL / "agents" / "openai.yaml"
    for path in (skill_path, reference_path, agent_path):
        require(path.is_file(), f"Missing skill file: {path.relative_to(ROOT)}", errors)

    text_files = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".html", ".css", ".py", ".svg"}]
    unfinished_marker = "[" + "TODO:"
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        require(unfinished_marker not in text, f"Unfinished scaffold marker in {path.relative_to(ROOT)}", errors)

    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        require(skill_text.startswith("---\nname: session-exporter\n"), "SKILL.md: invalid frontmatter start", errors)
        require("description:" in skill_text.split("---", 2)[1], "SKILL.md: missing description", errors)
        require("references/export-spec.md" in skill_text, "SKILL.md: export reference is not linked", errors)

    for relative in (
        "README.md",
        "LICENSE",
        "SECURITY.md",
        "docs/index.html",
        "docs/privacy.html",
        "docs/terms.html",
        "docs/support.html",
        "submission/listing.md",
        "submission/test-cases.md",
        "submission/release-notes.md",
        "plugins/session-exporter/assets/icon.png",
        "plugins/session-exporter/assets/logo.png",
    ):
        require((ROOT / relative).is_file(), f"Missing required file: {relative}", errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed: marketplace, manifests, skill, assets, policies, and submission materials are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
