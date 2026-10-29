#!/usr/bin/env python3
"""Build a studynow class site: a home page, one study loop page per unit, and a review page.

Usage: python3 build.py course.py OUT_DIR
course.py defines COURSE (a dict, see the skill). A .json file with the same shape also works.
unit.html and home.html must sit next to this script.
"""
import sys, os, json, copy, shutil, runpy, re, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
C = json.load(open(src)) if src.endswith(".json") else runpy.run_path(src)["COURSE"]
base = os.path.dirname(os.path.abspath(src))
UNIT = open(os.path.join(HERE, "unit.html")).read()
HOME = open(os.path.join(HERE, "home.html")).read()
problems, notes = [], []
esc = lambda s: html.escape(str(s or ""), quote=True)

def lower_first(s):
    return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s

def fix(o):
    """Unit pages live one folder down, so image paths gain ../"""
    if isinstance(o, str): return "../" + o if o.startswith("img/") else o
    if isinstance(o, list): return [fix(x) for x in o]
    if isinstance(o, dict): return {k: fix(v) for k, v in o.items()}
    return o

def walk_text(o):
    if isinstance(o, str): yield o
    elif isinstance(o, list):
        for x in o: yield from walk_text(x)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("img", "quizlet", "id", "home"): yield from walk_text(v)

def check(unit):
    ids = set()
    for s in unit["sections"]:
        sid = s.get("id")
        if not sid or sid in ids: problems.append(f"{unit['label']}: missing or repeated section id {sid!r}")
        ids.add(sid)
        steps = s.get("steps") or [0, 1, 2, 3, 4, 5]
        if not s.get("notes"): problems.append(f"{sid}: no notes")
        if 2 in steps and len(s.get("cards", [])) < 5: problems.append(f"{sid}: fewer than 5 flashcards")
        if 5 in steps and not s.get("points"): problems.append(f"{sid}: no key points")
        if 5 in steps and not (5 <= len(s.get("points", [])) <= 12): notes.append(f"{sid}: {len(s.get('points', []))} key points, aim for 5 to 12")
        fronts = [c[0].strip().lower() for c in s.get("cards", [])]
        if len(fronts) != len(set(fronts)): problems.append(f"{sid}: repeated flashcard front")
        for c in s.get("cards", []):
            if len(c) > 2 and c[2] and not os.path.exists(os.path.join(img_root(), c[2][4:] if c[2].startswith("img/") else c[2])):
                problems.append(f"{sid}: missing image {c[2]}")
        for b in s.get("notes", []):
            if "img" in b and not os.path.exists(os.path.join(img_root(), b["img"][4:])):
                problems.append(f"{sid}: missing image {b['img']}")
        for t in walk_text(s):
            if re.search(r"\s[—–-]\s|—", t): notes.append(f"{sid}: dash used as punctuation: {t[:70]}")
    return ids

def img_root():
    return os.path.join(base, C.get("img", "img"))

def page(deck, folder, title):
    js = "const DECK = " + json.dumps(fix(deck), ensure_ascii=False, indent=1) + ";"
    a = UNIT.index("/* DECK_START */") + len("/* DECK_START */"); b = UNIT.index("/* DECK_END */")
    h = UNIT[:a] + "\n" + js + "\n" + UNIT[b:]
    h = h.replace("<title>Study now</title>", "<title>" + esc(title) + "</title>")
    os.makedirs(os.path.join(out, folder), exist_ok=True)
    open(os.path.join(out, folder, "index.html"), "w").write(h)
    # parse check on the page script
    body = h[h.index("/* DECK_START */"):h.rindex("</script>")]
    p = os.path.join(out, folder, ".check.js"); open(p, "w").write(body)
    try:
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        if r.returncode: problems.append(f"{folder}: script does not parse: {r.stderr[:300]}")
    except FileNotFoundError:
        notes.append("node not found, script parse check skipped")
    os.remove(p)

if os.path.exists(out):
    for f in os.listdir(out):
        if f.startswith("unit-") or f in ("review", "index.html", "img"):
            p = os.path.join(out, f); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(out, exist_ok=True)
if os.path.isdir(img_root()): shutil.copytree(img_root(), os.path.join(out, "img"))

units = C["units"]
short = C.get("short") or C["name"].split(",")[0]
brk, dump = C.get("breakMinutes", 5), C.get("dumpMinutes", 7)
all_ids, cards_by = set(), []
for i, u in enumerate(units, 1):
    u.setdefault("label", f"Unit {i}")
    u.setdefault("slug", re.sub(r"[^a-z0-9]+", "-", u["label"].lower()).strip("-") or "unit-" + str(i))
    u.setdefault("title", f"{short} {u['label'].lower()}")
    for s in u["sections"]: s.setdefault("quizlet", "")
    ids = check(u)
    clash = ids & all_ids
    if clash: problems.append(f"{u['label']}: section ids used in another unit too: {sorted(clash)}")
    all_ids |= ids
    rv = u.get("review") or {"must": [], "secs": {}}
    deck = {"home": "../index.html", "review": rv, "title": u["title"], "subtitle": u.get("chip", ""),
            "source": u.get("source", ""), "breakMinutes": brk, "dumpMinutes": dump, "sections": u["sections"]}
    page(deck, u["slug"], u["title"])

def join_labels(ls):
    if all(l.startswith("Unit ") for l in ls):
        n = [l[5:] for l in ls]
        return "Units " + (", ".join(n[:-1]) + " and " + n[-1])
    return ", ".join(ls[:-1]) + " and " + ls[-1]

review = len(units) > 1
if review:
    A = []
    for u in units:
        for s in copy.deepcopy(u["sections"]):
            s["group"] = u["label"] + ", " + lower_first(u["name"]); A.append(s)
    must, secs = [], {}
    for u in units:
        rv = u.get("review") or {}
        must += rv.get("must", []); secs.update(rv.get("secs", {}))
    page({"home": "../index.html", "review": {"must": must, "secs": secs}, "title": short + ", everything so far",
          "subtitle": join_labels([u["label"] for u in units]),
          "source": "Every section from every unit so far, for cumulative review", "breakMinutes": brk,
          "dumpMinutes": dump, "sections": A}, "review", short + " review")

# home page
intro = C.get("intro", "")
lead = "One study loop per unit."
if C.get("cumulative") and review: lead += " Every test in this class is cumulative, so the review page covers everything so far."
elif review: lead += " The review page puts every unit in one place."
body = [f'<div>{"<span class=\"eyebrow\">" + esc(C["eyebrow"]) + "</span>" if C.get("eyebrow") else ""}<h1>{esc(C["name"])}</h1><p class="sub">{esc((lead + " " + intro).strip())}</p></div>']
for u in units:
    n, c = len(u["sections"]), sum(len(s.get("cards", [])) for s in u["sections"])
    topics = u.get("topics") or ", ".join(lower_first(s["title"]) for s in u["sections"] if (s.get("steps") or [0, 1]) != [0])
    topics = topics[:1].upper() + topics[1:]
    chip = f'<span class="chip">{esc(u["chip"])}</span>' if u.get("chip") else ""
    body.append(f'<a class="unit" href="{u["slug"]}/index.html"><div class="top"><span class="eyebrow">{esc(u["label"])}</span><h2>{esc(u["name"])}</h2>{chip}</div>'
                f'<p class="topics">{esc(topics)}</p><div class="meter" data-key="studyloop:{esc(u["title"])}" data-n="{n}"><span class="lbl">{n} sections, {c} flashcards</span><span class="track"><span class="fill"></span></span></div></a>')
if review:
    body.append(f'<a class="unit review" href="review/index.html"><div class="top"><span class="eyebrow">{esc(join_labels([u["label"] for u in units]))}</span><h2>Review everything so far</h2></div>'
                f'<p class="topics">Every section from every unit in one place, with a memory jog that covers all of it. Use it before a cumulative test or the final.</p></a>')
for x in C.get("extras", []):
    body.append(f'<a class="unit review" href="{esc(x["href"])}"><div class="top"><span class="eyebrow">{esc(x.get("eyebrow", ""))}</span><h2>{esc(x["title"])}</h2></div>'
                f'<p class="topics">{esc(x.get("text", ""))}</p></a>')
h = HOME.replace("{{TITLE}}", esc(C["name"])).replace("{{BODY}}", "\n".join(body))
open(os.path.join(out, "index.html"), "w").write(h)

tot = sum(len(s.get("cards", [])) for u in units for s in u["sections"])
print(f"Built {out}: {len(units)} unit(s), {sum(len(u['sections']) for u in units)} sections, {tot} flashcards" + (", review page" if review else ""))
for n in notes: print("note:", n)
for p in problems: print("PROBLEM:", p)
sys.exit(1 if problems else 0)
