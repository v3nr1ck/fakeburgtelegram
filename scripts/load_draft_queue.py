#!/usr/bin/env python3
"""Load content/drafts into content/articles at 2 per day starting today (site TZ)."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "content" / "drafts"
ARTICLES = ROOT / "content" / "articles"
SKIP = {"README.md", "INDEX.md", "SCHEDULING.md"}


def today() -> date:
    if ZoneInfo:
        return datetime.now(ZoneInfo("America/New_York")).date()
    return date.today()


def parse_fm(text: str) -> tuple[dict, str]:
    """Tolerant frontmatter parse (excerpts often contain colons)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict = {}
    raw = parts[1]
    # Prefer YAML when it works; fall back to line parser
    if yaml:
        try:
            meta = yaml.safe_load(raw) or {}
            return meta, parts[2].lstrip("\n")
        except Exception:
            meta = {}
    for line in raw.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if v.lower() in ("true", "false"):
            meta[k] = v.lower() == "true"
        else:
            meta[k] = v
    return meta, parts[2].lstrip("\n")


def dump_fm(meta: dict) -> str:
    order = [
        "title",
        "slug",
        "date",
        "publish_date",
        "category",
        "author",
        "excerpt",
        "image",
        "image_caption",
        "top_story",
        "featured",
    ]
    lines = ["---"]
    seen = set()
    for k in order:
        if k not in meta:
            continue
        seen.add(k)
        v = meta[k]
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        else:
            s = str(v).replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{k}: "{s}"')
    for k, v in meta.items():
        if k in seen:
            continue
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def main():
    ARTICLES.mkdir(parents=True, exist_ok=True)
    drafts = sorted(p for p in DRAFTS.glob("*.md") if p.name not in SKIP)
    start = today()
    print(f"Loading {len(drafts)} drafts → articles, 2/day from {start.isoformat()}")

    for i, src in enumerate(drafts):
        day = start + timedelta(days=i // 2)
        day_s = day.isoformat()
        meta, body = parse_fm(src.read_text(encoding="utf-8"))
        slug = meta.get("slug") or src.stem
        meta["date"] = day_s
        meta["publish_date"] = day_s
        if isinstance(meta.get("category"), list):
            meta["category"] = ", ".join(str(c) for c in meta["category"])
        out = ARTICLES / f"{day_s}-{slug}.md"
        out.write_text(dump_fm(meta) + "\n" + body.strip() + "\n", encoding="utf-8")
        print(f"  {day_s}  {out.name}")

    print("Done. Original drafts left in content/drafts/.")


if __name__ == "__main__":
    main()
