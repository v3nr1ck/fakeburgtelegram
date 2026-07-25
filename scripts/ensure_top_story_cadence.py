#!/usr/bin/env python3
"""
Ensure roughly one top-story go-live per calendar day (when content exists).

Homepage hero only rotates when a new top_story article becomes live.
This flags existing scheduled articles so the hero isn't stuck for weeks.

  python scripts/ensure_top_story_cadence.py
  python scripts/ensure_top_story_cadence.py --dry-run
  python scripts/ensure_top_story_cadence.py --every 1   # daily (default)
  python scripts/ensure_top_story_cadence.py --every 2   # every other day
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "content" / "articles"
SITE_TZ = ZoneInfo("America/New_York")


def parse_fm(text: str) -> tuple[dict, str, str]:
    if not text.startswith("---"):
        return {}, "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, "", text
    raw_fm, body = parts[1], parts[2]
    meta: dict = {}
    try:
        import yaml

        meta = yaml.safe_load(raw_fm) or {}
    except Exception:
        for line in raw_fm.splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, raw_fm, body


def dump_article(meta: dict, body: str) -> str:
    try:
        import yaml

        fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, default_flow_style=False)
        return f"---\n{fm}---{body if body.startswith(chr(10)) else chr(10) + body}"
    except Exception:
        lines = ["---"]
        for k, v in meta.items():
            if isinstance(v, bool):
                lines.append(f"{k}: {'true' if v else 'false'}")
            else:
                lines.append(f"{k}: {v}")
        lines.append("---")
        return "\n".join(lines) + (body if body.startswith("\n") else "\n" + body)


def go_live(meta: dict) -> date | None:
    raw = meta.get("publish_date") or meta.get("date")
    if not raw:
        return None
    s = str(raw)[:10]
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def cats_list(meta: dict) -> list[str]:
    c = meta.get("category") or ""
    if isinstance(c, list):
        return [str(x).strip() for x in c]
    return [x.strip() for x in str(c).split(",") if x.strip()]


def ensure_top(meta: dict) -> dict:
    meta = dict(meta)
    meta["top_story"] = True
    meta["featured"] = True
    cats = cats_list(meta)
    if "top-stories" not in cats:
        cats.append("top-stories")
    meta["category"] = ", ".join(cats)
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--every",
        type=int,
        default=1,
        help="Target max days between top-story go-lives (1 = daily when possible)",
    )
    ap.add_argument(
        "--from-date",
        default=None,
        help="Start date YYYY-MM-DD (default: tomorrow in America/New_York)",
    )
    args = ap.parse_args()

    today = datetime.now(SITE_TZ).date()
    start = (
        datetime.strptime(args.from_date, "%Y-%m-%d").date()
        if args.from_date
        else today + timedelta(days=1)
    )

    by_day: dict[date, list[Path]] = defaultdict(list)
    already_top: dict[date, list[Path]] = defaultdict(list)

    for path in sorted(ARTICLES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, _, _ = parse_fm(text)
        if meta.get("draft") is True:
            continue
        d = go_live(meta)
        if d is None or d < start:
            continue
        by_day[d].append(path)
        if meta.get("top_story") is True or "top-stories" in cats_list(meta):
            already_top[d].append(path)

    if not by_day:
        print("No future-dated articles found after", start.isoformat())
        return 0

    days = sorted(by_day.keys())
    end = days[-1]
    # Walk calendar; ensure a top at least every N days when content exists
    promoted: list[tuple[date, Path]] = []
    last_top: date | None = None
    # seed last_top from any tops on/before start-1
    for d in sorted(already_top.keys()):
        if d < start:
            last_top = d

    cursor = start
    while cursor <= end:
        if already_top.get(cursor):
            last_top = cursor
            cursor += timedelta(days=1)
            continue

        need = last_top is None or (cursor - last_top).days >= args.every
        if need and by_day.get(cursor):
            # promote first article of the day that isn't draft
            path = by_day[cursor][0]
            promoted.append((cursor, path))
            last_top = cursor
        cursor += timedelta(days=1)

    if not promoted:
        print(
            f"Already dense enough (every {args.every} day(s) from {start} through {end}). "
            f"No changes."
        )
        return 0

    print(f"Promoting {len(promoted)} article(s) to top_story (every {args.every} day(s)):")
    for d, path in promoted:
        print(f"  {d.isoformat()}  {path.name}")
        if args.dry_run:
            continue
        text = path.read_text(encoding="utf-8")
        meta, _, body = parse_fm(text)
        meta = ensure_top(meta)
        path.write_text(dump_article(meta, body), encoding="utf-8")

    if args.dry_run:
        print("(dry-run — no files written)")
    else:
        print("Done. Rebuild/publish when ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
