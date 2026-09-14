#!/usr/bin/env python3
"""Create deterministic ZIP archives for release and OpenAI submission."""

from __future__ import annotations

import shutil
import zipfile
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "session-exporter"
SKILL = PLUGIN / "skills" / "session-exporter"
DIST = ROOT / "dist"
VERSION = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))["version"]
FIXED_TIMESTAMP = (2026, 9, 14, 0, 0, 0)


def write_archive(source: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(relative, FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> None:
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob("session-exporter-*.zip"):
        old.unlink()

    plugin_archive = DIST / f"session-exporter-plugin-{VERSION}.zip"
    skill_archive = DIST / f"session-exporter-skill-{VERSION}.zip"
    write_archive(PLUGIN, plugin_archive)
    write_archive(SKILL, skill_archive)

    shutil.copy2(PLUGIN / "assets" / "logo.png", DIST / "session-exporter-logo.png")
    print(plugin_archive)
    print(skill_archive)
    print(DIST / "session-exporter-logo.png")


if __name__ == "__main__":
    main()
