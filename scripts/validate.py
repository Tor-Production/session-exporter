#!/usr/bin/env python3
"""Validate the Session Exporter marketplace and plugin package."""

from __future__ import annotations

import re
import sys
import json
import struct
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
    require(portable.get("version") == compatibility.get("version"), "portable and compatibility manifests use different versions", errors)
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

    text_files = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".html", ".css", ".py", ".svg", ".xml", ".txt"}]
    unfinished_marker = "[" + "TODO:"
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        require(unfinished_marker not in text, f"Unfinished scaffold marker in {path.relative_to(ROOT)}", errors)

    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        require(skill_text.startswith("---\nname: session-exporter\n"), "SKILL.md: invalid frontmatter start", errors)
        require("description:" in skill_text.split("---", 2)[1], "SKILL.md: missing description", errors)
        require("references/export-spec.md" in skill_text, "SKILL.md: export reference is not linked", errors)
        require("Do not create empty headings" in skill_text, "SKILL.md: adaptive metadata boundary is missing", errors)

    if reference_path.is_file():
        reference_text = reference_path.read_text(encoding="utf-8")
        for phrase in (
            "The export has four required high-level parts:",
            "The default filename uses a context-derived suffix",
            "Omit irrelevant information entirely.",
            "Do not use placeholder metadata",
            "Never pause solely to ask the user to choose an export language.",
        ):
            require(phrase in reference_text, f"export specification: missing adaptive rule: {phrase}", errors)

    test_cases_path = ROOT / "submission" / "test-cases.md"
    if test_cases_path.is_file():
        test_cases = test_cases_path.read_text(encoding="utf-8")
        require("no irrelevant metadata headings, tables, or placeholder values" in test_cases, "submission tests: non-repository scenario is not adaptive", errors)
        require("all eleven required sections" not in test_cases, "submission tests: obsolete fixed structure remains", errors)

    for relative in (
        "README.md",
        "LICENSE",
        "SECURITY.md",
        "docs/index.html",
        "docs/privacy.html",
        "docs/terms.html",
        "docs/support.html",
        "docs/sitemap.xml",
        "docs/robots.txt",
        "docs/social-card.svg",
        "docs/social-card.png",
        "submission/listing.md",
        "submission/test-cases.md",
        "submission/release-notes.md",
        "plugins/session-exporter/assets/icon.png",
        "plugins/session-exporter/assets/logo.png",
    ):
        require((ROOT / relative).is_file(), f"Missing required file: {relative}", errors)

    seo_pages = {
        "docs/index.html": "https://tor-production.github.io/session-exporter/",
        "docs/privacy.html": "https://tor-production.github.io/session-exporter/privacy.html",
        "docs/terms.html": "https://tor-production.github.io/session-exporter/terms.html",
        "docs/support.html": "https://tor-production.github.io/session-exporter/support.html",
    }
    for relative, canonical_url in seo_pages.items():
        page_path = ROOT / relative
        if not page_path.is_file():
            continue
        page_text = page_path.read_text(encoding="utf-8")
        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', page_text, re.IGNORECASE)
        og_url_match = re.search(r'<meta\s+property="og:url"\s+content="([^"]+)"', page_text, re.IGNORECASE)
        require(canonical_match is not None and canonical_match.group(1) == canonical_url, f"{relative}: canonical URL is missing or incorrect", errors)
        require(og_url_match is not None and og_url_match.group(1) == canonical_url, f"{relative}: og:url is missing or incorrect", errors)
        require('property="og:image"' in page_text and "https://tor-production.github.io/session-exporter/social-card.png" in page_text, f"{relative}: og:image is missing or incorrect", errors)
        require('name="twitter:card" content="summary_large_image"' in page_text, f"{relative}: Twitter summary card metadata is missing", errors)

    sitemap_path = ROOT / "docs/sitemap.xml"
    if sitemap_path.is_file():
        sitemap_text = sitemap_path.read_text(encoding="utf-8")
        for canonical_url in seo_pages.values():
            require(f"<loc>{canonical_url}</loc>" in sitemap_text, f"sitemap.xml: missing {canonical_url}", errors)

    robots_path = ROOT / "docs/robots.txt"
    if robots_path.is_file():
        robots_text = robots_path.read_text(encoding="utf-8")
        require("User-agent: *" in robots_text and "Allow: /" in robots_text, "robots.txt: crawling rules are missing", errors)
        require("Sitemap: https://tor-production.github.io/session-exporter/sitemap.xml" in robots_text, "robots.txt: sitemap directive is missing", errors)

    social_card_path = ROOT / "docs/social-card.png"
    if social_card_path.is_file():
        png_data = social_card_path.read_bytes()
        require(png_data.startswith(b"\x89PNG\r\n\x1a\n"), "social-card.png: invalid PNG signature", errors)
        if len(png_data) >= 24 and png_data.startswith(b"\x89PNG\r\n\x1a\n"):
            width, height = struct.unpack(">II", png_data[16:24])
            require((width, height) == (1200, 627), "social-card.png: expected dimensions are 1200x627", errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed: marketplace, manifests, skill, assets, policies, and submission materials are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
