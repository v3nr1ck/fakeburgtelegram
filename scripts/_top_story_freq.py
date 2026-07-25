import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

arts = list(Path("content/articles").glob("*.md"))
top = []
for p in arts:
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---"):
        continue
    fm = t.split("---", 2)[1]
    is_top = "top_story: true" in fm or "top-stories" in fm
    if not is_top:
        continue
    m = re.search(r"publish_date:\s*['\"]?(\d{4}-\d{2}-\d{2})", fm)
    if not m:
        m = re.search(r"date:\s*['\"]?(\d{4}-\d{2}-\d{2})", fm)
    d = m.group(1) if m else "?"
    top.append((d, p.name))

top.sort()
print(f"Total top_story articles: {len(top)}")
for d, n in top:
    print(f"  {d}  {n}")

dates = sorted({d for d, _ in top if d != "?"})
deltas = []
for a, b in zip(dates, dates[1:]):
    da, db = datetime.strptime(a, "%Y-%m-%d"), datetime.strptime(b, "%Y-%m-%d")
    deltas.append((db - da).days)
if deltas:
    print(f"Avg gap between top-story dates: {sum(deltas)/len(deltas):.1f} days")
    print(f"Min gap: {min(deltas)}  Max gap: {max(deltas)}")

# upcoming (after today)
today = datetime(2026, 7, 25).date()
future = [d for d in dates if datetime.strptime(d, "%Y-%m-%d").date() > today]
past = [d for d in dates if datetime.strptime(d, "%Y-%m-%d").date() <= today]
print(f"Live/past top dates: {len(past)}  Future top dates: {len(future)}")
if future:
    print("Next few future tops:", future[:10])
