#!/usr/bin/env python3
"""Build the site and copy dist/ into the repo root for GitHub Pages."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

# Generated page folders (safe to wipe on each publish)
GENERATED_DIRS = [
    "about",
    "category",
    "classifieds",
    "contact",
    "letter-to-the-editor",
    "privacy-policy",
    "search",
    "submit-an-obituary",
    "submit-anniversary",
    "submit-birth",
    "submit-engagement",
    "submit-guest-column",
    "submit-news-tip",
    "submit-scores",
    "submit-wedding",
    "weather",
    "2026",
    "2025",
    "2027",
    "docs",
]
GENERATED_FILES = ["index.html", "robots.txt", "rss.xml"]


def publish() -> str:
    # Build
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "build.py failed")

    if not DIST.is_dir():
        raise RuntimeError("dist/ missing after build")

    # Remove previous generated trees
    for name in GENERATED_DIRS:
        p = ROOT / name
        if p.is_dir():
            shutil.rmtree(p)
    for name in GENERATED_FILES:
        p = ROOT / name
        if p.is_file():
            p.unlink()

    # Copy dist → root
    for item in DIST.iterdir():
        dest = ROOT / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    (ROOT / "CNAME").write_text("fakeburgtelegram.com", encoding="ascii", newline="\n")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    # Don't let README steal the homepage
    readme = ROOT / "README.md"
    if readme.exists():
        readme.rename(ROOT / "DEV-README.md")

    msg = (result.stdout or "").strip() or "Published."
    return msg


if __name__ == "__main__":
    print(publish())
