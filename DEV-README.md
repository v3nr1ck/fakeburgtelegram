# Fake Burg Telegram

Static local newspaper site for **fakeburgtelegram.com** — Mechanicsburg & Champaign County, Ohio.

## Local CMS (free “WordPress-like” editor)

Double-click **`launch-admin.bat`**, or:

```powershell
cd C:\Users\comfy\Pictures\projects\fakeburg-telegram
pip install -r requirements.txt
python admin.py
```

Open **http://127.0.0.1:5050**

| You can… | How |
|----------|-----|
| Add a new article | **New article** → headline, body, sections, photo |
| Edit existing copy | **Articles** → **Edit** |
| **Champaign Voices** | **Champaign Voices** → headline + lede + 3 quotes/faces |
| Add/replace photos | On the article edit screen → choose image file |
| Homepage hero | Check **Feature on homepage** |
| Go live | **Publish** → Build & git push (articles + voices) |

Runs **only on your PC** (not public). Hosting stays free on GitHub Pages.

---

## Why static (not WordPress)?

| | This site (static) | Free WordPress.com | Self-hosted WordPress |
|--|--|--|--|
| Cost | Free hosting (Cloudflare/GitHub Pages) | Free tier is limited | Hosting ~$5+/mo |
| Update flow | Edit a `.md` file → run build | Web admin (easier UI) | Web admin + updates/plugins |
| Looks like Urbana Citizen | Custom CSS we control | Themes limited on free | Possible with paid Newspaper theme |
| Your domain | Yes (CNAME included) | Yes (paid often) | Yes |

**Updating is easy:** open a text file, change the story, run one command. Same nav structure as a newspaper CMS.

---

## Quick start

```powershell
cd C:\Users\comfy\Pictures\projects\fakeburg-telegram
pip install pyyaml
python build.py
python -m http.server 8080 --directory dist
```

Open http://localhost:8080

---

## Writing satire (local authenticity)

Full LLM instruct + county reference brain (roads, lore, surnames, mascots, businesses, variety rules):

`references/CHAMPAIGN-COUNTY-INSTRUCT.md`

Shorter place/business cheat-sheet: `references/CHAMPAIGN-COUNTY-LOCAL-BIBLE.md`

### Champaign Voices (American Voices–style)

Short reaction packages: headline + lede ending “What do you think?” + **3** quotes from locals with **fixed portraits** (new name/job each time).

- Content: `content/voices/*.md` (see README there)
- Live index: `/champaign-voices/`
- Homepage block: after Top Stories

---

## How to add or replace an article

1. Create a file in `content/articles/` named like:
   `2026-07-08-my-headline-slug.md`
2. Use this frontmatter:

```markdown
---
title: "Your headline here"
slug: your-headline-slug
date: 2026-07-08
category: sports
author: Sports desk
excerpt: One-line teaser for cards and SEO.
top_story: false
featured: true
---

**MECHANICSBURG** — Your article body here.

Use **bold**, *italic*, and paragraphs normally.

## Subhead if you want

More text.
```

3. **Categories** (comma-separated ok):  
   `top-stories`, `news`, `sports`, `opinion`, `community`, `lifestyle`, `special-sections`, `fair`, `obituaries`
4. Run:

```powershell
python build.py
```

5. Your story appears on the homepage section, category page, and its own URL:
   `/2026/07/08/your-headline-slug/`

### Your sports article

There is a **placeholder** sports story:

`content/articles/2026-07-08-indians-summer-scrimmage-ends-in-honorable-confusion.md`

**Replace that file** (or add a new `.md` with `category: sports`) with your real piece, then rebuild.

---

## Project layout

```
fakeburg-telegram/
  content/articles/   ← your stories (edit these)
  content/pages/      ← About, Contact, Privacy
  assets/css/         ← look & feel
  assets/js/          ← mobile menu, forms
  site.yaml           ← site name, nav, weather demo data
  build.py            ← generates the website
  dist/               ← finished site (upload this)
```

---

## Deploy (GitHub Pages — recommended)

See **[HOW-TO-PUBLISH.md](HOW-TO-PUBLISH.md)** for full steps.

Short version: push this repo to GitHub → Settings → Pages → Source: **GitHub Actions** → attach domain `fakeburgtelegram.com`.

Everyday: add a Markdown file under `content/articles/` → `git push` → site rebuilds automatically.

---

## Forms (tips, scores, letters)

Submit pages work in the browser as **demo forms** (they don’t email yet). When you’re ready, connect free **Formspree** or **Netlify Forms** in about 10 minutes — ask and we can wire that up.

---

## Optional: PyYAML

`build.py` works without PyYAML (built-in defaults), but install it so `site.yaml` is fully read:

```powershell
pip install pyyaml
```

---

## Branding

Edit `site.yaml` for phone, address, emails, weather demo numbers, and nav labels.  
Logo is CSS text (“Fake Burg / Telegram”) — swap for an image in `assets/img/` later if you want.
