# Groups the unit 2 lessons into six study sections so the unit is doable in a weekend.
import copy

GROUPS = [
    ("models", "Atomic models and the gold foil", ["dalton", "goldfoil", "models"]),
    ("atoms", "Atoms, ions and isotopes", ["nucleus", "ions", "isotopes", "mass"]),
    ("bohr", "Bohr model and spectra", ["bohr", "excited"]),
    ("quantum", "Quantum model and quantum numbers", ["qmmodel", "qnumbers"]),
    ("config", "Electron configurations and orbital diagrams", ["econfig", "orbdiag", "noblegas", "valence", "drills"]),
    ("explain", "The four explain answers", ["explain"]),
]

# Key points picked per group as (source id, index into that source's points)
POINTS = {
    "models": [("models", 0), ("dalton", 1), ("models", 1), ("dalton", 3), ("goldfoil", 0), ("models", 2),
               ("models", 4), ("models", 5), ("goldfoil", 6), ("models", 6), ("models", 7)],
    "atoms": [("nucleus", 0), ("nucleus", 4), ("nucleus", 5), ("ions", 1), ("ions", 2), ("ions", 3),
              ("isotopes", 0), ("isotopes", 1), ("isotopes", 3), ("isotopes", 5),
              "Practice answers: Cl 35.45, X 10.81 (boron), Cu 63.55, Si 28.09"],
    "bohr": [("bohr", 0), ("bohr", 3), ("bohr", 4), ("bohr", 6), ("bohr", 5), ("excited", 0), ("excited", 1),
             ("excited", 2), ("excited", 3), ("excited", 5)],
    "quantum": [("qmmodel", 0), ("qmmodel", 1), ("qmmodel", 2), ("qmmodel", 3), ("qmmodel", 4), ("qmmodel", 6),
                ("qnumbers", 0), ("qnumbers", 2), ("qnumbers", 3), ("qnumbers", 4), ("qnumbers", 5)],
    "config": [("econfig", 1), ("econfig", 2), ("econfig", 4), ("econfig", 5), ("orbdiag", 2), ("orbdiag", 3),
               ("noblegas", 0), ("noblegas", 2), ("noblegas", 4), ("valence", 1),
               "Drills: Ni [Ar] 4s² 3d⁸, Zn²⁺ [Ar] 3d¹⁰, Mn²⁺ and Fe³⁺ [Ar] 3d⁵, Co²⁺ [Ar] 3d⁷, Cl⁻ [Ar]"],
}

DUMP = {
    "atoms": [{"p": "Write everything you remember about atoms, ions and isotopes. Then solve these with a calculator and add your answers."},
              {"list": ["Chlorine: 34.969 amu (75.78%), 36.966 amu (24.22%)",
                        "Element X: 10.013 amu (19.9%), 11.009 amu (80.1%). Which element?",
                        "Copper: 62.930 amu (69.15%), 64.928 amu (30.85%)",
                        "Silicon: 27.977 (92.23%), 28.976 (4.68%), 29.974 (3.09%)"]}],
    "config": [{"p": "Write everything you remember about configurations and orbital diagrams. Then write these in noble gas notation."},
               {"list": ["Cu", "Cr", "Ni", "Zn²⁺", "Mn²⁺", "Fe³⁺", "Co²⁺", "Cl⁻"]}],
}

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
            sec = copy.deepcopy(srcs[0]); sec["id"] = gid; sec["title"] = title
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
