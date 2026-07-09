# Host on GitHub Pages + add articles

## Why GitHub Pages?

- Free HTTPS hosting for static sites  
- Your domain `fakeburgtelegram.com` works with a CNAME  
- You **don’t** touch WordPress  
- Workflow: edit a text file → push to GitHub → site updates in ~1 minute  

---

## One-time setup

### 1. Create a GitHub repo

1. Go to [github.com/new](https://github.com/new)  
2. Name it e.g. `fakeburg-telegram` (public is easiest for free Pages)  
3. **Don’t** add a README (we already have one)  
4. Create the repository  

### 2. Push this project

In PowerShell:

```powershell
cd C:\Users\comfy\Pictures\projects\fakeburg-telegram

git init
git add .
git commit -m "Initial Fake Burg Telegram site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fakeburg-telegram.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Turn on GitHub Pages

1. Repo → **Settings** → **Pages**  
2. **Source**: *GitHub Actions* (not “Deploy from a branch”)  
3. After the first push, open the **Actions** tab and wait for **Deploy to GitHub Pages** to finish green  

Temporary URL will look like:

`https://YOUR_USERNAME.github.io/fakeburg-telegram/`

> If the site is in a project repo (not `username.github.io`), links that start with `/assets/...` still work on a **custom domain**.  
> On the `github.io/repo-name/` URL only, you may need a base path later — use your real domain for production.

### 4. Attach fakeburgtelegram.com

1. In repo **Settings → Pages → Custom domain**, enter:  
   `fakeburgtelegram.com`  
2. At your domain registrar (Namecheap, Cloudflare, Google Domains, etc.), add DNS:

| Type  | Name | Value |
|-------|------|--------|
| `A`   | `@`  | `185.199.108.153` |
| `A`   | `@`  | `185.199.109.153` |
| `A`   | `@`  | `185.199.110.153` |
| `A`   | `@`  | `185.199.111.153` |
| `CNAME` | `www` | `YOUR_USERNAME.github.io` |

3. Wait for DNS (can take minutes to a few hours).  
4. Check **Enforce HTTPS** in Pages settings once DNS is green.

The build already puts a `CNAME` file in `dist/` for `fakeburgtelegram.com`.

---

## How you add more articles (everyday workflow)

### Option A — On your PC (recommended)

1. **Write the story** as a new Markdown file:

```
content/articles/2026-07-09-my-headline-slug.md
```

Example:

```markdown
---
title: "Village hall still closed on Fridays for 'reasons'"
slug: village-hall-still-closed-on-fridays
date: 2026-07-09
category: news
author: Staff report
excerpt: Short teaser that shows on the homepage cards.
top_story: true
featured: true
---

**MECHANICSBURG** — Body of the article goes here.

Second paragraph, etc.
```

2. **If you have a photo**, put it in `assets/img/` and set:

```yaml
image: /assets/img/my-photo.jpg
image_caption: Optional caption under the photo.
```

3. **Categories** (use one or more, comma-separated):

| Value | Where it shows |
|--------|----------------|
| `top-stories` | Homepage hero |
| `news` | News section |
| `sports` | Sports |
| `opinion` | Opinion |
| `community` | Life & Culture |
| `lifestyle` | Lifestyle |
| `special-sections` | Special sections grid |
| `fair` | Fair |
| `obituaries` | Obituaries |

4. **Preview locally** (optional but smart):

```powershell
cd C:\Users\comfy\Pictures\projects\fakeburg-telegram
python build.py
python -m http.server 8080 --directory dist
```

Open http://localhost:8080

5. **Publish**:

```powershell
git add content/articles assets/img
git commit -m "Add article: village hall closed Fridays"
git push
```

GitHub Actions rebuilds and deploys. In ~1–2 minutes the live site updates.

### Option B — Edit on GitHub.com (no PC tools)

1. Repo → `content/articles/` → **Add file** → **Create new file**  
2. Paste the Markdown (same format as above)  
3. Commit to `main`  
4. Wait for Actions to deploy  

Images: upload under `assets/img/` first, then reference them in the article.

---

## Checklist when something doesn’t show up

- [ ] File is under `content/articles/` and ends in `.md`  
- [ ] Frontmatter has `title`, `date`, `category`  
- [ ] You ran `git push` (or committed on GitHub)  
- [ ] Actions tab shows a green deploy  
- [ ] Hard-refresh the browser (Ctrl+F5)  

---

## Edit site settings (name, phone, weather demo)

Edit `site.yaml`, commit, push — same as articles.

---

## Summary

| Task | What you do |
|------|-------------|
| Add article | New `.md` in `content/articles/` → `git push` |
| Add photo | File in `assets/img/` + `image:` in frontmatter → push |
| Change About/Contact | Edit `content/pages/*.md` → push |
| Go live first time | Create repo, push, enable Pages (Actions), set domain |

You never need to open WordPress. The “CMS” is the `content/` folder.
