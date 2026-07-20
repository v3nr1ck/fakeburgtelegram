"""
Shared Champaign Voices cast — fixed stock headshots, rotating names/jobs.

Source stock (Downloads/onion, top level only):
  asian man/woman, black man, hispanic man/woman,
  old white man/woman, young white man/woman

Files live in assets/img/voices/{id}.jpg
"""

from __future__ import annotations

# Stable IDs used in Markdown frontmatter: portrait: asian-man
VOICE_CAST: list[dict[str, str]] = [
    {"id": "asian-man", "label": "Asian man", "file": "asian-man.jpg"},
    {"id": "asian-woman", "label": "Asian woman", "file": "asian-woman.jpg"},
    {"id": "black-man", "label": "Black man", "file": "black-man.jpg"},
    {"id": "hispanic-man", "label": "Hispanic man", "file": "hispanic-man.jpg"},
    {"id": "hispanic-woman", "label": "Hispanic woman", "file": "hispanic-woman.jpg"},
    {"id": "old-white-man", "label": "Old white man", "file": "old-white-man.jpg"},
    {"id": "old-white-woman", "label": "Old white woman", "file": "old-white-woman.jpg"},
    {"id": "young-white-man", "label": "Young white man", "file": "young-white-man.jpg"},
    {"id": "young-white-woman", "label": "Young white woman", "file": "young-white-woman.jpg"},
]

VOICE_IDS: list[str] = [c["id"] for c in VOICE_CAST]
VOICE_BY_ID: dict[str, dict[str, str]] = {c["id"]: c for c in VOICE_CAST}

# Legacy numeric portraits (old voice-1.svg … voice-5.svg) → stock IDs
_LEGACY_INT_MAP = {
    1: "young-white-man",
    2: "young-white-woman",
    3: "old-white-man",
    4: "asian-woman",
    5: "black-man",
    6: "hispanic-man",
    7: "hispanic-woman",
    8: "asian-man",
    9: "old-white-woman",
}

MIN_VOICE_PEOPLE = 3


def portrait_url(portrait_id: str) -> str:
    entry = VOICE_BY_ID.get(portrait_id) or VOICE_CAST[0]
    return f"/assets/img/voices/{entry['file']}"


def normalize_portrait_id(raw, fallback_index: int = 0) -> str:
    """Accept stock id string, legacy int 1–9, or junk → valid stock id."""
    if raw is None or raw == "":
        return VOICE_IDS[fallback_index % len(VOICE_IDS)]

    s = str(raw).strip().lower().replace(" ", "-").replace("_", "-")
    # bare filename
    if s.endswith(".jpg") or s.endswith(".jpeg") or s.endswith(".png") or s.endswith(".svg"):
        s = s.rsplit(".", 1)[0]
    if s.startswith("voice-"):
        # voice-3 → legacy int
        try:
            n = int(s.split("-", 1)[1])
            return _LEGACY_INT_MAP.get(n, VOICE_IDS[fallback_index % len(VOICE_IDS)])
        except ValueError:
            pass
    if s in VOICE_BY_ID:
        return s
    # try int
    try:
        n = int(s)
        if n in _LEGACY_INT_MAP:
            return _LEGACY_INT_MAP[n]
        if 1 <= n <= len(VOICE_IDS):
            return VOICE_IDS[n - 1]
    except ValueError:
        pass
    return VOICE_IDS[fallback_index % len(VOICE_IDS)]
