# Groups the unit 1 lessons into four study sections so the unit is doable in a sitting or two.
import copy

GROUPS = [
    ("matter", "Matter, changes and separation", ["classification", "properties", "states", "separation"]),
    ("lab", "Lab tools and safety", ["lab"]),
    ("measure", "Measurement math", ["metric", "scinot", "sigfigs", "density"]),
    ("data", "Data, error and graphs", ["accuracy", "graphs"]),
]

# Key points picked per group as (source id, index into that source's points) or written out
POINTS = {
    "matter": ["A pure substance is an element or a compound. A mixture is homogeneous or heterogeneous",
               ("classification", 3), ("classification", 4),
               "Physical properties are seen without changing the substance, chemical properties describe how it reacts",
               "A physical change makes no new substance, a chemical change makes one (burning, rusting, baking)",
               ("properties", 4),
               "Solid has a fixed shape and volume, liquid a fixed volume, gas fills its container",
               "Melting, freezing, evaporation, condensation, sublimation (solid to gas) and deposition (gas to solid) are all physical",
               ("states", 7), ("separation", 0), ("separation", 4)],
    "measure": [("metric", 0), ("metric", 1), ("metric", 3), ("metric", 5), ("scinot", 0),
                "Multiply: multiply the first parts and add the exponents. Divide: divide them and subtract",
                ("sigfigs", 0),
                "Times and divide keep the fewest sig figs, plus and minus keep the fewest decimal places",
                ("density", 0), ("density", 2), ("density", 4)],
    "data": [("accuracy", 0), ("accuracy", 1), ("accuracy", 3), ("accuracy", 5), ("accuracy", 7), ("graphs", 0),
             "The IV is changed on purpose and goes on x, the DV is measured and goes on y (DRY MIX)",
             ("graphs", 5), ("graphs", 6)],
}

DUMP = {}

MAX_CARDS = 30


def _cards(srcs):
    seen, pools = set(), []
    for s in srcs:
        pool = []
        for c in s.get("cards", []):
            k = str(c[0]).strip().lower()
            if k in seen:
                continue
            seen.add(k)
            pool.append(c)
        pools.append(pool)
    total = sum(len(p) for p in pools)
    if total <= MAX_CARDS:
        return [c for p in pools for c in p]
    out, i = [], 0
    while len(out) < MAX_CARDS:
        took = False
        for p in pools:
            if i < len(p) and len(out) < MAX_CARDS:
                out.append(p[i]); took = True
        if not took:
            break
        i += 1
    # keep each source's cards together, in their original order
    keep = {id(c) for c in out}
    return [c for p in pools for c in p if id(c) in keep]


def merge(sections, review=None):
    by = {s["id"]: s for s in sections}
    out, aliases, used = [], {}, set()
    secs = (review or {}).get("secs", {})
    new_secs = {}
    for gid, title, ids in GROUPS:
        srcs = [by[i] for i in ids if i in by]
        if not srcs:
            continue
        used.update(s["id"] for s in srcs)
        if len(srcs) == 1:
            sec = copy.deepcopy(srcs[0]); sec["id"] = gid; sec["title"] = title; sec["cards"] = _cards(srcs)
        else:
            notes = []
            for s in srcs:
                notes.append({"h": s["title"]})
                notes += copy.deepcopy(s.get("notes", []))
            sec = {"id": gid, "title": title, "quizlet": "", "notes": notes, "cards": _cards(srcs)}
            pts = []
            for p in POINTS[gid]:
                if isinstance(p, str):
                    pts.append(p)
                else:
                    src = by.get(p[0])
                    if src and p[1] < len(src.get("points", [])):
                        pts.append(src["points"][p[1]])
            sec["points"] = pts
            if gid in DUMP:
                sec["dump"] = DUMP[gid]
        out.append(sec)
        jog = []
        for s in srcs:
            jog += secs.get(s["id"], [])
            if s["id"] != gid:
                aliases[s["id"]] = gid
        if jog:
            new_secs[gid] = jog
    rest = [s for s in sections if s["id"] not in used]
    if review is not None:
        for k, v in secs.items():
            if k not in used:
                new_secs[k] = v
        review = dict(review, secs=new_secs)
    return out, rest, aliases, review
