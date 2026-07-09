#!/usr/bin/env python3
"""
Fake Burg Telegram static site builder.

Edit Markdown under content/, then run:
    python build.py

Output goes to dist/ — open dist/index.html or serve with:
    python -m http.server 8080 --directory dist
"""

from __future__ import annotations

import html
import re
import shutil
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
ARTICLES = CONTENT / "articles"
PAGES = CONTENT / "pages"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
SITE_YAML = ROOT / "site.yaml"


def load_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text)
    return _simple_yaml(text)


def _simple_yaml(text: str) -> dict:
    """Minimal fallback for top-level scalars if PyYAML missing."""
    data = {}
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#") or line.startswith(" ") or line.startswith("-"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip().strip('"').strip("'")
            if v:
                data[k.strip()] = v
    # Defaults if no PyYAML
    data.setdefault("name", "Fake Burg Telegram")
    data.setdefault("tagline", "Informing Mechanicsburg & Champaign County")
    data.setdefault("domain", "fakeburgtelegram.com")
    data.setdefault("phone", "(937) 555-0183")
    data.setdefault("address", "1 Telegram Square, Mechanicsburg, OH 43044")
    data.setdefault("copyright_year", 2026)
    data.setdefault(
        "parody_notice",
        "This is a satirical / parody publication. Not a real newspaper.",
    )
    data["nav"] = [
        {"label": "News", "children": [
            {"label": "Latest News", "href": "/category/news/"},
            {"label": "Top Stories", "href": "/category/top-stories/"},
            {"label": "Special Sections", "href": "/category/special-sections/"},
            {"label": "Submit News Tip", "href": "/submit-news-tip/"},
        ]},
        {"label": "Fair", "href": "/category/fair/"},
        {"label": "Sports", "children": [
            {"label": "Latest Sports", "href": "/category/sports/"},
            {"label": "Submit Scores", "href": "/submit-scores/"},
        ]},
        {"label": "Obituaries", "children": [
            {"label": "Latest Obituaries", "href": "/category/obituaries/"},
            {"label": "Submit an Obituary", "href": "/submit-an-obituary/"},
        ]},
        {"label": "Opinion", "children": [
            {"label": "Latest Opinion", "href": "/category/opinion/"},
            {"label": "Letter to the Editor", "href": "/letter-to-the-editor/"},
            {"label": "Submit Guest Column", "href": "/submit-guest-column/"},
        ]},
        {"label": "Life & Community", "children": [
            {"label": "Lifestyle", "href": "/category/lifestyle/"},
            {"label": "Community", "href": "/category/community/"},
            {"label": "Submit Anniversary", "href": "/submit-anniversary/"},
            {"label": "Submit Birth", "href": "/submit-birth/"},
            {"label": "Submit Engagement", "href": "/submit-engagement/"},
            {"label": "Submit Wedding", "href": "/submit-wedding/"},
        ]},
        {"label": "Classifieds", "href": "/classifieds/"},
        {"label": "Connect with Us", "children": [
            {"label": "About Us", "href": "/about/"},
            {"label": "Contact Us", "href": "/contact/"},
            {"label": "Privacy Policy", "href": "/privacy-policy/"},
        ]},
    ]
    data["home_sections"] = [
        {"title": "Top Stories", "category": "top-stories", "layout": "hero", "limit": 5},
        {"title": "News", "category": "news", "layout": "featured-list", "limit": 8},
        {"title": "Sports", "category": "sports", "layout": "featured-list", "limit": 8},
        {"title": "Life & Culture", "category": "community", "layout": "featured-list", "limit": 8},
        {"title": "Opinion", "category": "opinion", "layout": "featured-list", "limit": 8},
        {"title": "Special Sections", "category": "special-sections", "layout": "grid", "limit": 6},
    ]
    data["categories"] = {
        "top-stories": {"name": "Top Stories", "description": "The biggest stories in Champaign County."},
        "news": {"name": "News", "description": "Local news from Mechanicsburg and Champaign County."},
        "sports": {"name": "Sports", "description": "High school, rec leagues, and regional sports."},
        "opinion": {"name": "Opinion", "description": "Editorials, columns, and letters."},
        "community": {"name": "Life & Culture", "description": "Community life around Fake Burg."},
        "lifestyle": {"name": "Lifestyle", "description": "Living, dining, and local culture."},
        "special-sections": {"name": "Special Sections", "description": "Features and special coverage."},
        "fair": {"name": "Fair", "description": "Champaign County Fair and related coverage."},
        "obituaries": {"name": "Obituaries", "description": "Remembrances and notices."},
    }
    data["weather"] = {
        "city": "Mechanicsburg",
        "condition": "Partly cloudy",
        "temp_f": 78,
        "high": 84,
        "low": 64,
        "humidity": 62,
        "wind_mph": 7,
        "forecast": [
            {"day": "Thu", "high": 86},
            {"day": "Fri", "high": 82},
            {"day": "Sat", "high": 79},
            {"day": "Sun", "high": 81},
            {"day": "Mon", "high": 77},
        ],
    }
    return data


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta_raw = parts[1]
            body = parts[2].lstrip("\n")
            meta = {}
            if yaml:
                meta = yaml.safe_load(meta_raw) or {}
            else:
                for line in meta_raw.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip()] = v.strip().strip('"').strip("'")
            return meta, body
    return {}, text


def md_to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    para = []
    in_ul = False

    def flush_para():
        nonlocal para
        if para:
            text = " ".join(para)
            out.append(f"<p>{inline_md(text)}</p>")
            para = []

    def flush_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    for line in lines:
        if not line.strip():
            flush_para()
            flush_ul()
            continue
        if line.startswith("### "):
            flush_para()
            flush_ul()
            out.append(f"<h3>{inline_md(line[4:].strip())}</h3>")
        elif line.startswith("## "):
            flush_para()
            flush_ul()
            out.append(f"<h2>{inline_md(line[3:].strip())}</h2>")
        elif line.startswith("# "):
            flush_para()
            flush_ul()
            out.append(f"<h2>{inline_md(line[2:].strip())}</h2>")
        elif line.startswith("> "):
            flush_para()
            flush_ul()
            out.append(f"<blockquote><p>{inline_md(line[2:].strip())}</p></blockquote>")
        elif line.startswith("- "):
            flush_para()
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(line[2:].strip())}</li>")
        else:
            flush_ul()
            para.append(line.strip())
    flush_para()
    flush_ul()
    return "\n".join(out)


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def parse_date(d) -> datetime:
    if isinstance(d, datetime):
        return d
    if not d:
        return datetime.now()
    s = str(d)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return datetime.now()


def load_articles() -> list[dict]:
    items = []
    if not ARTICLES.exists():
        return items
    for path in sorted(ARTICLES.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        title = meta.get("title") or path.stem
        date = parse_date(meta.get("date"))
        slug = meta.get("slug") or slugify(title)
        cats = meta.get("categories") or meta.get("category") or "news"
        if isinstance(cats, str):
            cats = [c.strip() for c in cats.split(",")]
        cats = [c.lower().replace(" ", "-") for c in cats]
        item = {
            "title": title,
            "slug": slug,
            "date": date,
            "date_str": date.strftime("%B %d, %Y"),
            "date_iso": date.strftime("%Y-%m-%d"),
            "categories": cats,
            "primary_category": cats[0],
            "author": meta.get("author") or "Staff report",
            "excerpt": meta.get("excerpt") or first_sentence(body),
            "image": meta.get("image") or placeholder_image(title),
            "image_caption": meta.get("image_caption") or "",
            "featured": bool(meta.get("featured", False)),
            "top_story": bool(meta.get("top_story", False)) or ("top-stories" in cats),
            "body_md": body,
            "body_html": md_to_html(body),
            "url": f"/{date.strftime('%Y/%m/%d')}/{slug}/",
            "path": path,
        }
        items.append(item)
    items.sort(key=lambda a: a["date"], reverse=True)
    return items


def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"^#+\s*", "", text)
    m = re.match(r"(.{40,180}?[.!?])\s", text + " ")
    return (m.group(1) if m else text[:160]).strip()


def placeholder_image(title: str) -> str:
    # Deterministic gradient placeholder via CSS class; empty URL uses letter thumb
    return ""


def by_category(articles: list[dict], cat: str) -> list[dict]:
    cat = cat.lower()
    return [a for a in articles if cat in a["categories"] or (cat == "top-stories" and a["top_story"])]


def cat_name(site: dict, cat: str) -> str:
    info = (site.get("categories") or {}).get(cat) or {}
    return info.get("name") or cat.replace("-", " ").title()


def cat_desc(site: dict, cat: str) -> str:
    info = (site.get("categories") or {}).get(cat) or {}
    return info.get("description") or ""


# ——— HTML helpers ———

def thumb_style(article: dict) -> str:
    if article.get("image"):
        return f'style="background-image:url(\'{html.escape(article["image"])}\')"'
    # color from title hash
    h = abs(hash(article["title"])) % 360
    return f'style="background:linear-gradient(135deg,hsl({h},45%,42%),hsl({(h+40)%360},40%,28%))"'


def story_title_html(a: dict, level: str = "h3") -> str:
    return f'<{level} class="story-title"><a href="{a["url"]}">{html.escape(a["title"])}</a></{level}>'


def story_meta_html(a: dict) -> str:
    return (
        f'<div class="story-meta">'
        f'<a href="/category/{a["primary_category"]}/">{html.escape(cat_name_static(a["primary_category"]))}</a>'
        f' · {html.escape(a["author"])} — {a["date_str"]}'
        f"</div>"
    )


_CAT_LABELS = {
    "top-stories": "Top Stories",
    "news": "News",
    "sports": "Sports",
    "opinion": "Opinion",
    "community": "Life & Culture",
    "lifestyle": "Lifestyle",
    "special-sections": "Special Sections",
    "fair": "Fair",
    "obituaries": "Obituaries",
}


def cat_name_static(cat: str) -> str:
    return _CAT_LABELS.get(cat, cat.replace("-", " ").title())


def render_nav(site: dict) -> str:
    parts = ['<nav class="main-nav"><div class="container">']
    parts.append('<button class="nav-toggle" type="button" aria-label="Menu">Menu</button>')
    parts.append('<div class="nav-row">')
    for item in site.get("nav") or []:
        label = html.escape(item["label"])
        children = item.get("children")
        href = item.get("href")
        if children:
            parts.append('<div class="nav-item">')
            parts.append(f'<button type="button">{label}</button>')
            parts.append('<div class="dropdown">')
            for c in children:
                parts.append(f'<a href="{html.escape(c["href"])}">{html.escape(c["label"])}</a>')
            parts.append("</div></div>")
        else:
            parts.append(
                f'<div class="nav-item"><a href="{html.escape(href or "#")}">{label}</a></div>'
            )
    parts.append("</div></div></nav>")
    return "\n".join(parts)


def render_header(site: dict) -> str:
    name = html.escape(site["name"])
    return f"""
<header class="site-header">
  <div class="utility-bar">
    <div class="container inner">
      <a href="/">Home</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/classifieds/">Classifieds</a>
      <a href="mailto:{html.escape(site.get('email_news') or 'news@fakeburgtelegram.com')}">Newsletter</a>
    </div>
  </div>
  <div class="container header-main">
    <div class="logo-wrap">
      <a class="logo" href="/" aria-label="{name}">
        <div class="logo-mark">Fake Burg<span>Telegram</span></div>
      </a>
    </div>
    <div class="header-actions">
      <a class="btn-subscribe" href="/contact/">Contact</a>
    </div>
  </div>
</header>
{render_nav(site)}
"""


def render_footer(site: dict) -> str:
    return f"""
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <div class="footer-logo">Fake Burg<span>Telegram</span></div>
    </div>
    <div>
      <p>{html.escape(site.get("phone", ""))}<br>
      {html.escape(site.get("address", ""))}</p>
      <p><a href="mailto:{html.escape(site.get("email_news", ""))}">Newsroom</a> ·
         <a href="mailto:{html.escape(site.get("email_sports", ""))}">Sports</a> ·
         <a href="/contact/">Contact</a></p>
    </div>
    <div>
      <p>{html.escape(site.get("tagline", ""))}</p>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© {site.get("copyright_year", 2026)} {html.escape(site["name"])}. {html.escape(site.get("parody_notice", ""))}</p>
  </div>
</footer>
"""


def render_sidebar(site: dict, articles: list[dict], exclude_slug: str | None = None) -> str:
    w = site.get("weather") or {}
    forecast = "".join(
        f'<div><span>{html.escape(str(d.get("day","")))}</span>{d.get("high","")}°</div>'
        for d in (w.get("forecast") or [])
    )
    recent = [a for a in articles if a["slug"] != exclude_slug][:6]
    recent_html = "".join(
        f'<div class="side-story">{story_title_html(a, "h4")}{story_meta_html(a)}</div>'
        for a in recent
    )
    return f"""
<aside class="sidebar">
  <div class="widget">
    <h3>Search</h3>
    <form class="search-form" action="/search/" method="get">
      <input type="search" name="q" placeholder="Search…" aria-label="Search">
      <button type="submit">Go</button>
    </form>
  </div>
  <div class="widget weather-widget">
    <h3><a href="/weather/">Weather</a></h3>
    <div class="temp">{w.get("temp_f", "—")}° F</div>
    <div class="cond">{html.escape(str(w.get("city","")))} · {html.escape(str(w.get("condition","")))}</div>
    <div class="weather-stats">
      <div>High {w.get("high","—")}°</div>
      <div>Low {w.get("low","—")}°</div>
      <div>Humidity {w.get("humidity","—")}%</div>
      <div>Wind {w.get("wind_mph","—")} mph</div>
    </div>
    <div class="weather-forecast">{forecast}</div>
  </div>
  <div class="widget parody-box">
    <strong>Parody notice</strong><br>
    {html.escape(site.get("parody_notice",""))}
  </div>
  <div class="widget">
    <h3>Latest</h3>
    {recent_html or '<p class="empty-state">No stories yet.</p>'}
  </div>
</aside>
"""


def absolute_url(site: dict, path: str) -> str:
    """Build https://domain/path for Open Graph / canonical (Facebook requires absolute URLs)."""
    domain = (site.get("domain") or "fakeburgtelegram.com").strip().rstrip("/")
    if not path:
        path = "/"
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"https://{domain}{path}"


def shell(
    site: dict,
    title: str,
    body: str,
    description: str = "",
    *,
    path: str = "/",
    image: str = "",
    og_type: str = "website",
) -> str:
    site_name = site["name"]
    full_title = f"{title} — {site_name}" if title != site_name else site_name
    desc = description or site.get("tagline") or site_name
    # Facebook scrapes og:* tags; relative image URLs fail — always absolute
    img = image or "/assets/img/og-default.png"
    if img and not (img.startswith("http://") or img.startswith("https://")):
        if not img.startswith("/"):
            img = "/" + img
    canonical = absolute_url(site, path)
    og_image = absolute_url(site, img)
    return f"""<!DOCTYPE html>
<html lang="en" prefix="og: https://ogp.me/ns#">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{html.escape(canonical)}">
  <!-- Open Graph (Facebook, iMessage, LinkedIn, etc.) -->
  <meta property="og:site_name" content="{html.escape(site_name)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:type" content="{html.escape(og_type)}">
  <meta property="og:url" content="{html.escape(canonical)}">
  <meta property="og:image" content="{html.escape(og_image)}">
  <meta property="og:image:secure_url" content="{html.escape(og_image)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">
  <!-- Twitter / X card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(desc)}">
  <meta name="twitter:image" content="{html.escape(og_image)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Open+Sans:wght@400;600;700&family=Roboto:wght@400;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
{render_header(site)}
<main class="page-wrap">
  <div class="container">
{body}
  </div>
</main>
{render_footer(site)}
<script src="/assets/js/site.js"></script>
</body>
</html>
"""


def hero_section(title: str, cat: str, items: list[dict]) -> str:
    if not items:
        return f'<section class="section"><h2 class="block-title"><a href="/category/{cat}/">{html.escape(title)}</a></h2><p class="empty-state">No stories yet.</p></section>'
    lead, rest = items[0], items[1:5]
    stack = "".join(
        f"""
        <article class="stack-item">
          <a href="{a['url']}" class="thumb" {thumb_style(a)} aria-hidden="true"></a>
          <div>
            <div class="story-cat">{html.escape(cat_name_static(a['primary_category']))}</div>
            {story_title_html(a)}
            {story_meta_html(a)}
          </div>
        </article>
        """
        for a in rest
    )
    return f"""
<section class="section">
  <h2 class="block-title"><a href="/category/{cat}/">{html.escape(title)}</a></h2>
  <div class="hero-grid">
    <article class="hero-feature">
      <a href="{lead['url']}" class="thumb" {thumb_style(lead)}></a>
      <div class="hero-body">
        <div class="story-cat">{html.escape(cat_name_static(lead['primary_category']))}</div>
        {story_title_html(lead, 'h3')}
        {story_meta_html(lead)}
      </div>
    </article>
    <div class="hero-stack">{stack}</div>
  </div>
</section>
"""


def featured_list_section(title: str, cat: str, items: list[dict]) -> str:
    if not items:
        return f'<section class="section"><h2 class="block-title"><a href="/category/{cat}/">{html.escape(title)}</a></h2><p class="empty-state">No stories yet.</p></section>'
    feat = items[0]
    rest = items[1:]
    list_html = "".join(
        f"""
        <article class="list-item">
          {story_title_html(a)}
          <div class="story-meta">{a['date_str']}</div>
        </article>
        """
        for a in rest
    )
    return f"""
<section class="section">
  <h2 class="block-title"><a href="/category/{cat}/">{html.escape(title)}</a></h2>
  <div class="featured-list">
    <article class="featured-card">
      <a href="{feat['url']}" class="thumb" {thumb_style(feat)}></a>
      {story_title_html(feat)}
      {story_meta_html(feat)}
      <p class="story-excerpt">{html.escape(feat['excerpt'])}</p>
    </article>
    <div class="list-col">{list_html}</div>
  </div>
</section>
"""


def grid_section(title: str, cat: str, items: list[dict]) -> str:
    if not items:
        return f'<section class="section"><h2 class="block-title"><a href="/category/{cat}/">{html.escape(title)}</a></h2><p class="empty-state">No stories yet.</p></section>'
    cards = "".join(
        f"""
        <article class="grid-card">
          <a href="{a['url']}" class="thumb" {thumb_style(a)}></a>
          {story_title_html(a)}
        </article>
        """
        for a in items
    )
    return f"""
<section class="section">
  <h2 class="block-title"><a href="/category/{cat}/">{html.escape(title)}</a></h2>
  <div class="grid-cards">{cards}</div>
</section>
"""


def write_file(rel: str, content: str):
    path = DIST / rel.lstrip("/").replace("/", "\\") if False else DIST / Path(rel.lstrip("/"))
    # ensure index.html for directory URLs
    if rel.endswith("/"):
        path = DIST / rel.strip("/") / "index.html"
    elif not rel.endswith(".html") and not rel.endswith(".xml") and not rel.endswith(".txt"):
        path = DIST / rel / "index.html" if not Path(rel).suffix else DIST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def build_home(site: dict, articles: list[dict]):
    sections_html = []
    for sec in site.get("home_sections") or []:
        cat = sec["category"]
        items = by_category(articles, cat)[: int(sec.get("limit") or 8)]
        # also show top_story articles in top-stories
        if cat == "top-stories" and not items:
            items = [a for a in articles if a.get("top_story")][:5] or articles[:5]
        layout = sec.get("layout") or "featured-list"
        if layout == "hero":
            sections_html.append(hero_section(sec["title"], cat, items))
        elif layout == "grid":
            sections_html.append(grid_section(sec["title"], cat, items))
        else:
            sections_html.append(featured_list_section(sec["title"], cat, items))

    body = f"""
<div class="layout-main">
  <div class="content-col">
    {''.join(sections_html)}
  </div>
  {render_sidebar(site, articles)}
</div>
"""
    write_file(
        "index.html",
        shell(
            site,
            site["name"],
            body,
            site.get("tagline", ""),
            path="/",
            image="/assets/img/og-default.png",
            og_type="website",
        ),
    )


def build_article(site: dict, articles: list[dict], a: dict):
    crumbs = (
        f'<nav class="breadcrumb"><a href="/">Home</a> › '
        f'<a href="/category/{a["primary_category"]}/">{html.escape(cat_name(site, a["primary_category"]))}</a> › '
        f'{html.escape(a["title"])}</nav>'
    )
    caption = (
        f'<p class="story-meta">{html.escape(a["image_caption"])}</p>'
        if a.get("image_caption")
        else ""
    )
    if a.get("image"):
        hero = (
            f'<div class="article-hero">'
            f'<img src="{html.escape(a["image"])}" alt="{html.escape(a["title"])}">'
            f"{caption}</div>"
        )
    else:
        hero = f'<div class="article-hero"><div class="thumb" {thumb_style(a)}></div>{caption}</div>'
    body = f"""
<div class="layout-main">
  <article class="content-col">
    {crumbs}
    <div class="story-cat">{html.escape(cat_name(site, a["primary_category"]))}</div>
    <h1 class="article-title">{html.escape(a["title"])}</h1>
    <div class="article-byline">{html.escape(a["author"])} — {a["date_str"]}</div>
    {hero}
    <div class="article-body">
      {a["body_html"]}
    </div>
  </article>
  {render_sidebar(site, articles, exclude_slug=a["slug"])}
</div>
"""
    # path: /YYYY/MM/DD/slug/index.html
    rel = f"{a['date'].strftime('%Y/%m/%d')}/{a['slug']}/index.html"
    page_path = a["url"]  # e.g. /2026/07/08/slug/
    write_file(
        rel,
        shell(
            site,
            a["title"],
            body,
            a["excerpt"],
            path=page_path,
            image=a.get("image") or "",
            og_type="article",
        ),
    )


def build_category(site: dict, articles: list[dict], cat: str):
    items = by_category(articles, cat)
    name = cat_name(site, cat)
    desc = cat_desc(site, cat)
    list_html = "".join(
        f"""
        <article class="cat-item">
          <a href="{a['url']}" class="thumb" {thumb_style(a)}></a>
          <div>
            {story_title_html(a, 'h2')}
            {story_meta_html(a)}
            <p class="story-excerpt">{html.escape(a['excerpt'])}</p>
          </div>
        </article>
        """
        for a in items
    ) or '<p class="empty-state">No stories in this section yet. Add a Markdown file under content/articles/ with this category.</p>'

    body = f"""
<div class="layout-main">
  <div class="content-col">
    <header class="page-header">
      <h1>{html.escape(name)}</h1>
      <p>{html.escape(desc)}</p>
    </header>
    <div class="cat-list">{list_html}</div>
  </div>
  {render_sidebar(site, articles)}
</div>
"""
    write_file(
        f"category/{cat}/index.html",
        shell(site, name, body, desc, path=f"/category/{cat}/", og_type="website"),
    )


def build_static_page(site: dict, articles: list[dict], slug: str, title: str, inner: str):
    body = f"""
<div class="layout-main">
  <div class="content-col">
    <header class="page-header"><h1>{html.escape(title)}</h1></header>
    <div class="prose">{inner}</div>
  </div>
  {render_sidebar(site, articles)}
</div>
"""
    write_file(
        f"{slug}/index.html",
        shell(site, title, body, path=f"/{slug}/", og_type="website"),
    )


def form_page(title: str, fields_note: str) -> str:
    return f"""
<p>{html.escape(fields_note)}</p>
<form class="form-card" data-static>
  <label>Your name</label>
  <input type="text" name="name" required>
  <label>Email</label>
  <input type="email" name="email" required>
  <label>Details</label>
  <textarea name="body" required></textarea>
  <button type="submit">Submit</button>
  <p class="form-success" hidden style="color:green;margin-top:1rem;">Thanks — this demo form does not email yet. Use the Contact page addresses to send your item for real.</p>
  <p class="form-note">Demo form only. Wire to Formspree, Netlify Forms, or email when you deploy.</p>
</form>
"""


def build_pages(site: dict, articles: list[dict]):
    # Markdown pages
    if PAGES.exists():
        for path in PAGES.glob("*.md"):
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            title = meta.get("title") or path.stem.replace("-", " ").title()
            slug = meta.get("slug") or path.stem
            build_static_page(site, articles, slug, title, md_to_html(body))

    # Built-in forms / utility if not overridden by md
    builtins = {
        "submit-news-tip": ("Submit News Tip", "Got a tip from around Mechanicsburg or Champaign County? Send it in."),
        "submit-scores": ("Submit Scores", "Coaches and parents: send scores, box scores, and recaps."),
        "submit-an-obituary": ("Submit an Obituary", "Submit a paid notice. (Parody site — for real notices use a real paper.)"),
        "letter-to-the-editor": ("Letter to the Editor", "Keep letters under 300 words. We edit for length and clarity."),
        "submit-guest-column": ("Submit Guest Column", "Pitch a guest column on local issues."),
        "submit-anniversary": ("Submit Anniversary", "Share an anniversary announcement."),
        "submit-birth": ("Submit Birth", "Share a birth announcement."),
        "submit-engagement": ("Submit Engagement", "Share an engagement announcement."),
        "submit-wedding": ("Submit Wedding", "Share a wedding announcement."),
    }
    existing = {p.stem for p in PAGES.glob("*.md")} if PAGES.exists() else set()
    for slug, (title, note) in builtins.items():
        if slug not in existing:
            build_static_page(site, articles, slug, title, form_page(title, note))

    # Weather
    w = site.get("weather") or {}
    weather_inner = f"""
<p>Current conditions for <strong>{html.escape(str(w.get('city','Mechanicsburg')))}</strong> (static demo data — swap for a live API later).</p>
<p class="weather-widget"><span class="temp">{w.get('temp_f')}° F</span><br>
{html.escape(str(w.get('condition','')))}<br>
High {w.get('high')}° / Low {w.get('low')}° · Humidity {w.get('humidity')}% · Wind {w.get('wind_mph')} mph</p>
"""
    build_static_page(site, articles, "weather", "Weather", weather_inner)

    # Classifieds
    classifieds = """
<p>Community classifieds for Mechanicsburg and Champaign County. (Sample listings — edit in <code>build.py</code> or add a CMS later.)</p>
<div class="classifieds-grid">
  <div class="classified-item"><strong>FOR SALE</strong> Slightly used combine. Only one owner, if you count the bank. Cash preferred. Text Fake Burg Classifieds.</div>
  <div class="classified-item"><strong>HELP WANTED</strong> Someone willing to explain why Main Street has three coffee shops and no shoe store. Flexible hours.</div>
  <div class="classified-item"><strong>LOST</strong> Sense of direction after the 4-way stop in St. Paris. Reward: a wave next time we pass.</div>
  <div class="classified-item"><strong>WANTED</strong> Rideshare to Champaign County Fair. Will pay in funnel cake IOUs.</div>
</div>
"""
    build_static_page(site, articles, "classifieds", "Classifieds", classifieds)

    # Search (client-side list of titles)
    links = "".join(
        f'<li><a href="{a["url"]}">{html.escape(a["title"])}</a> <span class="story-meta">{a["date_str"]} · {html.escape(cat_name(site, a["primary_category"]))}</span></li>'
        for a in articles
    )
    search_inner = f"""
<p>Use your browser find (Ctrl+F) on this list, or add a real search later (Pagefind, Algolia, etc.).</p>
<ul class="cat-list" id="search-index">{links}</ul>
<script>
(function(){{
  var q = new URLSearchParams(location.search).get('q') || '';
  if (!q) return;
  q = q.toLowerCase();
  document.querySelectorAll('#search-index li').forEach(function(li){{
    li.style.display = li.textContent.toLowerCase().indexOf(q) >= 0 ? '' : 'none';
  }});
}})();
</script>
"""
    build_static_page(site, articles, "search", "Search", search_inner)


def build_rss(site: dict, articles: list[dict]):
    items = []
    domain = site.get("domain") or "fakeburgtelegram.com"
    for a in articles[:30]:
        items.append(f"""
    <item>
      <title>{html.escape(a['title'])}</title>
      <link>https://{domain}{a['url']}</link>
      <guid>https://{domain}{a['url']}</guid>
      <pubDate>{a['date'].strftime('%a, %d %b %Y 12:00:00 GMT')}</pubDate>
      <description>{html.escape(a['excerpt'])}</description>
    </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{html.escape(site['name'])}</title>
    <link>https://{domain}/</link>
    <description>{html.escape(site.get('tagline') or '')}</description>
    {''.join(items)}
  </channel>
</rss>
"""
    (DIST / "rss.xml").write_text(rss, encoding="utf-8")


def build():
    site = load_yaml(SITE_YAML)
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    # copy assets
    if ASSETS.exists():
        shutil.copytree(ASSETS, DIST / "assets")

    articles = load_articles()
    print(f"Loaded {len(articles)} articles")

    build_home(site, articles)
    for a in articles:
        build_article(site, articles, a)

    cats = set((site.get("categories") or {}).keys())
    for a in articles:
        cats.update(a["categories"])
    for cat in sorted(cats):
        build_category(site, articles, cat)

    build_pages(site, articles)
    build_rss(site, articles)

    # CNAME for GitHub Pages / custom domain
    (DIST / "CNAME").write_text(site.get("domain") or "fakeburgtelegram.com", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://fakeburgtelegram.com/rss.xml\n",
        encoding="utf-8",
    )

    print(f"Built site → {DIST}")
    print("Preview: python -m http.server 8080 --directory dist")


if __name__ == "__main__":
    build()
