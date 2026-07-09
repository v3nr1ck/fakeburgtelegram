#!/usr/bin/env python3
"""
Fake Burg Telegram — local CMS dashboard (free, runs on your PC only).

  pip install -r requirements.txt
  python admin.py

Open http://127.0.0.1:5050
"""

from __future__ import annotations

import re
import secrets
import subprocess
from datetime import date, datetime
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    request,
    send_from_directory,
    url_for,
)
from jinja2 import BaseLoader, Environment, TemplateNotFound, select_autoescape
from werkzeug.utils import secure_filename

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent
ARTICLES = ROOT / "content" / "articles"
IMG_DIR = ROOT / "assets" / "img"
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

CATEGORIES = [
    ("top-stories", "Top Stories (homepage hero)"),
    ("news", "News"),
    ("sports", "Sports"),
    ("opinion", "Opinion"),
    ("community", "Life & Culture / Community"),
    ("lifestyle", "Lifestyle"),
    ("special-sections", "Special Sections"),
    ("fair", "Fair"),
    ("obituaries", "Obituaries"),
]

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-") or "article"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = {}
            if yaml:
                meta = yaml.safe_load(parts[1]) or {}
            else:
                for line in parts[1].splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip()] = v.strip().strip('"').strip("'")
            return meta, parts[2].lstrip("\n")
    return {}, text


def dump_frontmatter(meta: dict) -> str:
    lines = ["---"]
    order = [
        "title",
        "slug",
        "date",
        "category",
        "author",
        "excerpt",
        "image",
        "image_caption",
        "top_story",
        "featured",
    ]
    seen = set()
    for key in order:
        if key not in meta:
            continue
        seen.add(key)
        val = meta[key]
        if isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        else:
            escaped = str(val).replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{key}: "{escaped}"')
    for key, val in meta.items():
        if key in seen:
            continue
        lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def list_articles() -> list[dict]:
    ARTICLES.mkdir(parents=True, exist_ok=True)
    items = []
    for path in ARTICLES.glob("*.md"):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        cats = meta.get("category") or meta.get("categories") or ""
        if isinstance(cats, list):
            cats = ", ".join(str(c) for c in cats)
        cats = str(cats)
        image = str(meta.get("image") or "").strip()
        has_photo = False
        if image.startswith("/"):
            has_photo = (ROOT / image.lstrip("/")).is_file()
        items.append(
            {
                "filename": path.name,
                "title": meta.get("title") or path.stem,
                "slug": meta.get("slug") or path.stem,
                "date": str(meta.get("date") or "")[:10],
                "category": cats,
                "author": meta.get("author") or "",
                "excerpt": meta.get("excerpt") or "",
                "image": image,
                "has_photo": has_photo,
                "top_story": bool(meta.get("top_story")),
                "featured": bool(meta.get("featured")),
                "body": body,
                "meta": meta,
            }
        )

    def sort_key(a):
        try:
            return datetime.strptime(a["date"], "%Y-%m-%d")
        except Exception:
            return datetime.min

    items.sort(key=sort_key, reverse=True)
    return items


def load_article(filename: str) -> dict | None:
    safe = Path(filename).name
    for a in list_articles():
        if a["filename"] == safe:
            return a
    return None


def save_image(file_storage, slug: str) -> str | None:
    if not file_storage or not file_storage.filename:
        return None
    name = secure_filename(file_storage.filename)
    ext = Path(name).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise ValueError(f"Unsupported image type: {ext}. Use jpg, png, gif, or webp.")
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_name = f"{slugify(slug)}-{stamp}{ext}"
    file_storage.save(IMG_DIR / out_name)
    return f"/assets/img/{out_name}"


def write_article(
    *,
    title: str,
    slug: str,
    date_str: str,
    categories: list[str],
    author: str,
    excerpt: str,
    body: str,
    image: str,
    image_caption: str,
    top_story: bool,
    featured: bool,
    old_filename: str | None = None,
) -> Path:
    ARTICLES.mkdir(parents=True, exist_ok=True)
    slug = slugify(slug or title)
    date_str = date_str or date.today().isoformat()
    cat_str = ", ".join(categories) if categories else "news"
    if top_story and "top-stories" not in [c.strip() for c in cat_str.split(",")]:
        cat_str = f"{cat_str}, top-stories"

    meta = {
        "title": title.strip(),
        "slug": slug,
        "date": date_str,
        "category": cat_str,
        "author": (author or "Staff report").strip(),
        "excerpt": excerpt.strip(),
        "top_story": top_story,
        "featured": featured,
    }
    if image:
        meta["image"] = image
    if image_caption:
        meta["image_caption"] = image_caption.strip()

    new_name = f"{date_str}-{slug}.md"
    new_path = ARTICLES / new_name
    new_path.write_text(dump_frontmatter(meta) + "\n" + body.strip() + "\n", encoding="utf-8")

    if old_filename and old_filename != new_name:
        old = ARTICLES / Path(old_filename).name
        if old.is_file() and old.resolve() != new_path.resolve():
            old.unlink()
    return new_path


def run_publish() -> str:
    from publish import publish

    return publish()


BASE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Dashboard{% endblock %} · Fake Burg CMS</title>
  <style>
    :root {
      --brand: #3372a5; --brand-dark: #285d88; --bg: #f4f6f8; --card: #fff;
      --border: #e2e8f0; --text: #1a202c; --muted: #718096;
      --danger: #c53030; --ok: #276749;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; }
    header.app {
      background: #111; color: #fff; padding: 0.85rem 1.25rem;
      display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
    }
    header.app a { color: #9fd4f5; text-decoration: none; font-weight: 600; }
    header.app a:hover { color: #fff; }
    header.app .logo { font-weight: 800; letter-spacing: 0.04em; text-transform: uppercase; color: #fff; }
    header.app .logo span { color: #4db2ec; font-size: 0.75em; display: block; letter-spacing: 0.15em; }
    .wrap { max-width: 1100px; margin: 0 auto; padding: 1.25rem; }
    .flash { padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 1rem; background: #e6fffa; border: 1px solid #81e6d9; color: var(--ok); white-space: pre-wrap; }
    .flash.error { background: #fff5f5; border-color: #feb2b2; color: var(--danger); }
    .toolbar { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1.25rem; align-items: center; }
    .btn {
      display: inline-block; background: var(--brand); color: #fff !important; border: 0;
      padding: 0.55rem 1rem; border-radius: 6px; font-weight: 700; font-size: 14px;
      cursor: pointer; text-decoration: none; font-family: inherit;
    }
    .btn:hover { background: var(--brand-dark); }
    .btn.ghost { background: #fff; color: var(--brand) !important; border: 1px solid var(--border); }
    .btn.danger { background: var(--danger); }
    .btn.ok { background: var(--ok); }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; margin-bottom: 1rem; }
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th, td { padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border); vertical-align: middle; }
    th { background: #f7fafc; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
    tr:last-child td { border-bottom: 0; }
    .thumb {
      width: 72px; height: 52px; border-radius: 4px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      background-size: cover; background-position: center; position: relative;
    }
    .thumb.missing::after {
      content: "no photo"; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
      font-size: 10px; color: #fff; font-weight: 700; background: rgba(0,0,0,0.25);
    }
    .badge {
      display: inline-block; font-size: 11px; font-weight: 700; padding: 0.15rem 0.45rem;
      border-radius: 999px; background: #edf2f7; color: #4a5568; margin-right: 0.25rem;
    }
    .badge.hero { background: #bee3f8; color: #2a4365; }
    .badge.photo { background: #c6f6d5; color: #22543d; }
    .badge.nophoto { background: #feebc8; color: #7b341e; }
    form.edit label { display: block; font-weight: 700; font-size: 13px; margin: 1rem 0 0.35rem; }
    form.edit input[type=text], form.edit input[type=date], form.edit input[type=file],
    form.edit textarea, form.edit select {
      width: 100%; padding: 0.55rem 0.7rem; border: 1px solid #cbd5e0; border-radius: 6px; font: inherit;
    }
    form.edit textarea.body { min-height: 280px; font-family: ui-monospace, Consolas, monospace; font-size: 13px; }
    form.edit .row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    @media (max-width: 700px) { form.edit .row { grid-template-columns: 1fr; } }
    .checks { display: flex; flex-wrap: wrap; gap: 0.75rem 1.25rem; margin-top: 0.5rem; }
    .checks label { font-weight: 600; display: flex; align-items: center; gap: 0.4rem; margin: 0; }
    .cats { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.35rem 1rem; margin-top: 0.35rem; }
    .cats label { font-weight: 500; margin: 0; display: flex; gap: 0.4rem; align-items: center; }
    .preview-img { max-width: 280px; max-height: 180px; border-radius: 6px; border: 1px solid var(--border); margin-top: 0.5rem; object-fit: cover; }
    .help { font-size: 13px; color: var(--muted); margin: 0.25rem 0 0; }
    .form-actions { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border); }
    .muted { color: var(--muted); font-size: 13px; }
    h1 { font-size: 1.4rem; margin: 0 0 0.25rem; }
    .sub { color: var(--muted); margin: 0 0 1.25rem; font-size: 14px; }
  </style>
</head>
<body>
  <header class="app">
    <div class="logo">Fake Burg<span>CMS · local only</span></div>
    <nav>
      <a href="{{ url_for('dashboard') }}">All articles</a>
      &nbsp;·&nbsp;
      <a href="{{ url_for('new_article') }}">New article</a>
      &nbsp;·&nbsp;
      <a href="{{ url_for('publish_site') }}">Publish</a>
      &nbsp;·&nbsp;
      <a href="https://fakeburgtelegram.com/" target="_blank" rel="noopener">Live site ↗</a>
    </nav>
  </header>
  <div class="wrap">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% for cat, msg in messages %}
        <div class="flash {% if cat == 'error' %}error{% endif %}">{{ msg }}</div>
      {% endfor %}
    {% endwith %}
    {% block body %}{% endblock %}
  </div>
</body>
</html>
"""

DASHBOARD = """
{% extends "base" %}
{% block title %}Articles{% endblock %}
{% block body %}
  <h1>Articles</h1>
  <p class="sub">{{ articles|length }} stories · edit photos &amp; copy here, then Publish for the live site.</p>
  <div class="toolbar">
    <a class="btn" href="{{ url_for('new_article') }}">+ New article</a>
    <a class="btn ok" href="{{ url_for('publish_site') }}">Publish to site</a>
    <span class="muted">Orange badge = still using a gradient (no photo).</span>
  </div>
  <div class="card">
    <table>
      <thead>
        <tr><th>Photo</th><th>Story</th><th>Section</th><th></th></tr>
      </thead>
      <tbody>
        {% for a in articles %}
        <tr>
          <td>
            <div class="thumb {% if not a.has_photo %}missing{% endif %}"
              {% if a.has_photo %}style="background-image:url('{{ url_for('media', filename=a.image.split('/')[-1]) }}')"{% endif %}
            ></div>
          </td>
          <td>
            <strong>{{ a.title }}</strong><br>
            <span class="muted">{{ a.date }} · {{ a.author }}</span>
            {% if a.top_story %}<span class="badge hero">homepage hero</span>{% endif %}
            {% if a.has_photo %}<span class="badge photo">has photo</span>{% else %}<span class="badge nophoto">needs photo</span>{% endif %}
          </td>
          <td><span class="muted">{{ a.category }}</span></td>
          <td style="white-space:nowrap">
            <a class="btn ghost" href="{{ url_for('edit_article', filename=a.filename) }}">Edit</a>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="4" class="muted">No articles yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
{% endblock %}
"""

EDIT = """
{% extends "base" %}
{% block title %}{{ 'Edit' if article else 'New' }} article{% endblock %}
{% block body %}
  <h1>{{ 'Edit article' if article else 'New article' }}</h1>
  <p class="sub">Headline, sections, body text, and photo — like a simple WordPress editor, free and local.</p>

  <div class="card" style="padding:1rem 1.25rem 1.5rem">
  <form class="edit" method="post" enctype="multipart/form-data"
        action="{{ url_for('edit_article', filename=article.filename) if article else url_for('new_article') }}">
    <label>Headline *</label>
    <input type="text" name="title" required value="{{ article.title if article else '' }}">

    <div class="row">
      <div>
        <label>Date</label>
        <input type="date" name="date" value="{{ article.date if article and article.date else today }}">
      </div>
      <div>
        <label>Author / byline</label>
        <input type="text" name="author" value="{{ article.author if article else 'Staff report' }}">
      </div>
    </div>

    <label>URL slug <span class="muted">(optional — auto from headline)</span></label>
    <input type="text" name="slug" value="{{ article.slug if article else '' }}" placeholder="my-story-slug">

    <label>Excerpt / teaser</label>
    <input type="text" name="excerpt" value="{{ article.excerpt if article else '' }}" placeholder="One-line summary for cards">

    <label>Sections *</label>
    <div class="cats">
      {% for key, label in categories %}
      <label>
        <input type="checkbox" name="category" value="{{ key }}"
          {% if article and key in article.category %}checked{% endif %}
          {% if not article and key == 'news' %}checked{% endif %}>
        {{ label }}
      </label>
      {% endfor %}
    </div>

    <div class="checks">
      <label>
        <input type="checkbox" name="top_story" value="1" {% if article and article.top_story %}checked{% endif %}>
        Feature on homepage (Top Stories hero area)
      </label>
      <label>
        <input type="checkbox" name="featured" value="1"
          {% if article and article.featured %}checked{% endif %}
          {% if not article %}checked{% endif %}>
        Featured card in its section
      </label>
    </div>

    <label>Article body *</label>
    <p class="help">Paragraphs = blank lines. Optional Markdown: **bold**, *italic*, ## subhead.</p>
    <textarea class="body" name="body" required>{{ article.body if article else '' }}</textarea>

    <label>Photo</label>
    {% if article and article.has_photo %}
      <div>
        <img class="preview-img" src="{{ url_for('media', filename=article.image.split('/')[-1]) }}" alt="Current">
        <p class="help">Current: {{ article.image }}</p>
      </div>
    {% elif article %}
      <p class="help">No photo yet — readers see a color gradient until you upload one.</p>
    {% endif %}
    <input type="file" name="image" accept=".jpg,.jpeg,.png,.gif,.webp,image/*">
    <p class="help">Choose a file to add or replace the photo.</p>

    <label>Photo caption <span class="muted">(optional)</span></label>
    <input type="text" name="image_caption" value="{{ article.meta.get('image_caption','') if article else '' }}">

    {% if article and article.image %}
    <div class="checks">
      <label><input type="checkbox" name="remove_image" value="1"> Remove photo (use gradient again)</label>
    </div>
    {% endif %}

    <div class="form-actions">
      <button class="btn" type="submit" name="action" value="save">Save article</button>
      <button class="btn ok" type="submit" name="action" value="save_publish">Save &amp; rebuild site</button>
      <a class="btn ghost" href="{{ url_for('dashboard') }}">Cancel</a>
      {% if article %}
      <button class="btn danger" type="submit" name="action" value="delete"
              onclick="return confirm('Delete this article permanently?')">Delete</button>
      {% endif %}
    </div>
  </form>
  </div>
{% endblock %}
"""

PUBLISH_PAGE = """
{% extends "base" %}
{% block title %}Publish{% endblock %}
{% block body %}
  <h1>Publish to live site</h1>
  <p class="sub">Rebuild HTML from your articles, then push to GitHub so fakeburgtelegram.com updates (still free).</p>
  <div class="card" style="padding:1.25rem">
    <form method="post">
      <ol>
        <li><strong>Build</strong> — updates files on this PC</li>
        <li><strong>Push</strong> — sends them to GitHub Pages (~1–2 min live)</li>
      </ol>
      <div class="form-actions">
        <button class="btn ok" type="submit" name="action" value="build">Build only</button>
        <button class="btn" type="submit" name="action" value="build_push">Build &amp; git push</button>
        <a class="btn ghost" href="{{ url_for('dashboard') }}">Back</a>
      </div>
    </form>
    {% if log %}
    <pre style="margin-top:1rem;background:#1a202c;color:#e2e8f0;padding:1rem;border-radius:8px;overflow:auto;font-size:12px">{{ log }}</pre>
    {% endif %}
  </div>
{% endblock %}
"""

TEMPLATES = {
    "base": BASE,
    "dashboard": DASHBOARD,
    "edit": EDIT,
    "publish": PUBLISH_PAGE,
}


def render(page: str, **ctx):
    class DictLoader(BaseLoader):
        def get_source(self, environment, template):
            if template not in TEMPLATES:
                raise TemplateNotFound(template)
            return TEMPLATES[template], template, lambda: True

    def _flashes(with_categories=False):
        from flask import get_flashed_messages as gfm

        return gfm(with_categories=with_categories)

    env = Environment(loader=DictLoader(), autoescape=select_autoescape(["html", "xml"]))
    env.globals["url_for"] = url_for
    env.globals["get_flashed_messages"] = _flashes
    return env.get_template(page).render(**ctx)


@app.route("/")
def dashboard():
    return render("dashboard", articles=list_articles())


@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(IMG_DIR, filename)


@app.route("/new", methods=["GET", "POST"])
def new_article():
    if request.method == "GET":
        return render("edit", article=None, categories=CATEGORIES, today=date.today().isoformat())
    return _save_from_form(old_filename=None)


@app.route("/edit/<path:filename>", methods=["GET", "POST"])
def edit_article(filename):
    article = load_article(filename)
    if not article:
        flash("Article not found.", "error")
        return redirect(url_for("dashboard"))
    if request.method == "GET":
        return render("edit", article=article, categories=CATEGORIES, today=date.today().isoformat())

    action = request.form.get("action") or "save"
    if action == "delete":
        path = ARTICLES / Path(filename).name
        if path.is_file():
            path.unlink()
        flash("Article deleted. Publish to update the live site.", "ok")
        return redirect(url_for("dashboard"))
    return _save_from_form(old_filename=filename)


def _save_from_form(old_filename: str | None):
    title = (request.form.get("title") or "").strip()
    if not title:
        flash("Headline is required.", "error")
        return redirect(request.url)

    slug = (request.form.get("slug") or "").strip() or slugify(title)
    date_str = (request.form.get("date") or date.today().isoformat()).strip()
    author = request.form.get("author") or "Staff report"
    excerpt = request.form.get("excerpt") or ""
    body = request.form.get("body") or ""
    image_caption = request.form.get("image_caption") or ""
    categories = request.form.getlist("category")
    top_story = request.form.get("top_story") == "1"
    featured = request.form.get("featured") == "1"
    remove_image = request.form.get("remove_image") == "1"

    image = ""
    if old_filename:
        existing = load_article(old_filename)
        if existing:
            image = existing.get("image") or ""
    if remove_image:
        image = ""

    try:
        uploaded = request.files.get("image")
        if uploaded and uploaded.filename:
            image = save_image(uploaded, slug) or image
    except ValueError as e:
        flash(str(e), "error")
        return redirect(request.url)

    path = write_article(
        title=title,
        slug=slug,
        date_str=date_str,
        categories=categories,
        author=author,
        excerpt=excerpt,
        body=body,
        image=image,
        image_caption=image_caption,
        top_story=top_story,
        featured=featured,
        old_filename=old_filename,
    )

    action = request.form.get("action") or "save"
    if action == "save_publish":
        try:
            log = run_publish()
            flash(f"Saved {path.name} and rebuilt the site locally.", "ok")
            flash(log[:500] if log else "OK", "ok")
        except Exception as e:
            flash(f"Saved {path.name}, but rebuild failed: {e}", "error")
    else:
        flash(f"Saved {path.name}. Use Publish when you want the live site updated.", "ok")

    return redirect(url_for("edit_article", filename=path.name))


@app.route("/publish", methods=["GET", "POST"])
def publish_site():
    log = None
    if request.method == "POST":
        action = request.form.get("action") or "build"
        try:
            log = run_publish()
            flash("Site rebuilt on this PC.", "ok")
            if action == "build_push":
                env = dict(**{k: v for k, v in __import__("os").environ.items()})
                # Prefer git on PATH with Git usr\bin for ssh if needed
                subprocess.run(["git", "add", "-A"], cwd=ROOT, capture_output=True, text=True)
                st = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
                if st.stdout.strip():
                    subprocess.run(
                        ["git", "commit", "-m", "Publish site updates from CMS"],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                    )
                    r3 = subprocess.run(
                        ["git", "push", "origin", "main"],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                    )
                    log = (log or "") + "\n\n--- git push ---\n" + (r3.stdout or "") + (r3.stderr or "")
                    if r3.returncode == 0:
                        flash("Pushed to GitHub. Live site updates in ~1–2 minutes.", "ok")
                    else:
                        flash("Git push failed — see log below, or push manually in a terminal.", "error")
                else:
                    flash("Nothing new to commit.", "ok")
        except Exception as e:
            flash(str(e), "error")
            log = str(e)
    return render("publish", log=log)


def main():
    ARTICLES.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    print("\n  Fake Burg CMS  →  http://127.0.0.1:5050\n  (local only — not on the public internet)\n")
    app.run(host="127.0.0.1", port=5050, debug=False)


if __name__ == "__main__":
    main()
