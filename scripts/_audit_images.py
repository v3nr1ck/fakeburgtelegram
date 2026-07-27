"""Audit article image front-matter vs git tracking and disk."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    tracked = set(
        subprocess.check_output(
            ["git", "ls-files", "assets/img"],
            cwd=ROOT,
            text=True,
        )
        .replace("\\", "/")
        .splitlines()
    )
    print(f"tracked images: {len(tracked)}")

    untracked_needed: list[str] = []
    missing_disk: list[tuple[str, str]] = []
    ok = 0

    for p in sorted((ROOT / "content" / "articles").glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'(?m)^image:\s*["\']?([^"\'\n]+)["\']?', text)
        if not m:
            continue
        img = m.group(1).strip()
        rel = img.lstrip("/").replace("\\", "/")
        disk = ROOT / rel
        if not disk.is_file():
            missing_disk.append((p.name, img))
            continue
        if rel not in tracked:
            untracked_needed.append(rel)
        else:
            ok += 1

    print(f"referenced images tracked+on-disk: {ok}")
    print(f"referenced images on-disk but untracked: {len(untracked_needed)}")
    for rel in untracked_needed:
        print(f"  ADD {rel}")
    print(f"referenced images missing on disk: {len(missing_disk)}")
    for name, img in missing_disk:
        print(f"  MISSING {name} -> {img}")

    # Also list all untracked jpgs under assets/img (alts/batch)
    all_untracked = []
    for f in (ROOT / "assets" / "img").rglob("*"):
        if not f.is_file():
            continue
        if f.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        rel = f.relative_to(ROOT).as_posix()
        if rel not in tracked:
            all_untracked.append(rel)
    print(f"all untracked image files under assets/img: {len(all_untracked)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
