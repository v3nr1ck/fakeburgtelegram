# How to schedule articles (one per day, free)

You **can** push 20 articles at once and have them appear on the live site day by day.

## How it works

1. Put stories in `content/articles/` with a **future** `date:` (or `publish_date:`).
2. The site builder **hides** anything not due yet (America/New_York calendar day).
3. GitHub Actions runs **every morning**, rebuilds the site, and only that day’s (and earlier) stories go live.

No WordPress. No paid scheduler.

## Frontmatter

### Option A — byline date = go-live date (simplest)

```yaml
---
title: "My story"
date: 2026-07-15
category: news
---
```

If today is July 14 in Ohio, this story is **not** on the site.  
After the daily job on July 15, it **is**.

### Option B — different byline vs go-live

```yaml
---
title: "My story"
date: 2026-07-01
publish_date: 2026-07-20
category: news
---
```

Shows “July 1, 2026” in the byline, but only appears on the site starting July 20.

### Never publish (keep in articles folder)

```yaml
draft: true
```

## Top stories cadence (homepage hero)

The homepage **Top Stories** hero only changes when a new article with `top_story: true` (or category `top-stories`) goes live.

**Target:** about **one new top story per day** when you have content scheduled (not every 1–2 weeks).

When bulk-scheduling:

```yaml
top_story: true
featured: true
category: news, top-stories   # or sports, community, etc. + top-stories
```

Or run after writing a batch:

```powershell
python scripts/ensure_top_story_cadence.py          # promote ~1/day on future dates
python scripts/ensure_top_story_cadence.py --every 2  # every other day
python scripts/ensure_top_story_cadence.py --dry-run
```

Daily GitHub Action still rebuilds once each morning; cadence is controlled by **which stories are flagged**, not by how often Actions runs.

## Bulk release plan

1. Copy 20 files from `content/drafts/` → `content/articles/`.
2. Set each file’s `date:` (or `publish_date:`) to consecutive days.
3. Mark top-story cadence (`top_story: true` on ~one story per day, or run `ensure_top_story_cadence.py`).
4. `git push`.
5. Done. One (or more) appear each day when the clock catches up.

## Local preview of future stories

```powershell
$env:BUILD_INCLUDE_SCHEDULED="1"
python build.py
```

Normal build (what GitHub uses):

```powershell
python build.py
```

## When does the daily job run?

See `.github/workflows/deploy.yml` — cron `0 11 * * *` UTC (~morning Eastern).  
You can also run **Actions → Deploy site → Run workflow** anytime to force a rebuild.

## CMS note

The local CMS still edits files in `content/articles/`. After you save future-dated stories, run **Publish** (or push) once; the daily Action handles the drip from there.
