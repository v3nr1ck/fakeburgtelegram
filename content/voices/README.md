# Champaign Voices

Local version of The Onion’s **American Voices**: a news-ish headline, one setup sentence ending in **“What do you think?”**, then **three** deadpan quotes from “regular people” with absurd job titles.

## CMS (preferred)

Use the same local dashboard as articles:

```powershell
python admin.py
```

Open **http://127.0.0.1:5050** → **Champaign Voices** → **New Voices** / **Edit**.  
**Publish** rebuilds articles and voices together.

## Format (Markdown on disk)

One Markdown file per piece. Everything lives in frontmatter:

```yaml
---
title: "Short newsy headline"
slug: optional-slug
date: 2026-07-20
publish_date: 2026-07-20   # optional; defaults to date
draft: false
lede: >
  One or two sentences summarizing the (satirical) news item,
  then ask: What do you think?
people:
  - portrait: old-white-man    # stock face id (see cast below)
    name: "Dale Evilsizor"
    title: "Adams Township Roadside Philosopher"
    quote: "Short, idiotic, or weirdly sharp reaction."
  - portrait: young-white-woman
    name: "..."
    title: "..."
    quote: "..."
  - portrait: black-man
    name: "..."
    title: "..."
    quote: "..."
---
```

Body below `---` is optional (ignored for now).

## Rules of the form

1. **Always exactly 3 people** (enforced by build + CMS).
2. **Portrait IDs** are the fixed stock cast below — same photos every time; **new name + job every piece**.
3. Jobs should be ridiculous and specific (`Carafe Refiller`, `Monologue Archivist` energy).
4. Quotes are short (one line, sometimes two).
5. **Topics should be big / national / world / existential news** — not stories *about* Champaign County.
   The **voices** are local small-town minds reacting. The **headline** is broader current events.
6. Batch generator for big runs: `python scripts/generate_voices_batch.py`
7. Scheduling: same as articles (`draft`, `publish_date` / `date` vs America/New_York).

## Stock cast (`assets/img/voices/`)

| `portrait:` id | File |
|----------------|------|
| `asian-man` | asian-man.jpg |
| `asian-woman` | asian-woman.jpg |
| `black-man` | black-man.jpg |
| `hispanic-man` | hispanic-man.jpg |
| `hispanic-woman` | hispanic-woman.jpg |
| `old-white-man` | old-white-man.jpg |
| `old-white-woman` | old-white-woman.jpg |
| `young-white-man` | young-white-man.jpg |
| `young-white-woman` | young-white-woman.jpg |

Defined in `voices_portraits.py` (shared by CMS + builder).
