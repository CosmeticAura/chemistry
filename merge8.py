# Unit 2 regrouped into the 8 topics that make up the unit test (Nov 13).
import copy
from em2 import EM, EM_DUMP


def split_notes(notes, at):
    """Split notes at the first {'h': at}."""
    for i, n in enumerate(notes):
        if n.get("h") == at:
            return notes[:i], notes[i:]
    return notes, []


def cut(sec, notes=None, cards=None, points=None, title=None):
    s = copy.deepcopy(sec)
    if notes is not None: s["notes"] = notes
    if cards is not None: s["cards"] = cards
    if points is not None: s["points"] = points
    if title: s["title"] = title
    return s


def merge(sections, review):
    by = {s["id"]: s for s in sections}
    secs = review.get("secs", {})

    iso = by["isotopes"]
    iso_a, iso_b = split_notes(iso["notes"], "Average atomic mass")
    tail = [n for n in iso_b if "Not isotopes" in n.get("p", "")]
    iso_b = [n for n in iso_b if n not in tail]
    iso_cards_a = [c for c in iso["cards"] if not any(w in c[0].lower() for w in ("average", "atomic mass", "%", "averages", "amu", "abundan", "cesium", "copper", "chlorine", "boron", "element z"))]
    iso_cards_b = [c for c in iso["cards"] if c not in iso_cards_a]

    ex = by["explain"]["notes"]
    ex_a, ex_b = split_notes(ex, "Why does 4s fill before 3d, but empty first?")
    ex_cards = by["explain"]["cards"]

    qm = by["qmmodel"]
    qm_theory = [n for n in qm["notes"] if any(k in n.get("p", "") for k in ("Schrödinger", "Heisenberg", "electron cloud"))]
    qm_orb = [n for n in qm["notes"] if n not in qm_theory]
    qm_cards_t = [c for c in qm["cards"] if c[0] in ("Quantum mechanical model (who, when)", "Quantum mechanical model", "Electron cloud", "Heisenberg uncertainty principle", "The modern model of the atom", "Do electrons travel in definite paths?")]
    qm_cards_o = [c for c in qm["cards"] if c not in qm_cards_t]

    exc = by["excited"]
    exc_cards = [c for c in exc["cards"] if c[0] != "Electromagnetic spectrum"]

    def group(gid, title, parts, points, dump=None, max_cards=32):
        notes, pools, seen = [], [], set()
        for h, ns, cs in parts:
            if h: notes.append({"h": h})
            notes += copy.deepcopy(ns)
            pool = []
            for c in cs:
                k = c[0].strip().lower()
                if k not in seen:
                    seen.add(k); pool.append(c)
            pools.append(pool)
        pick, i = [], 0
        while len(pick) < max_cards and any(i < len(p) for p in pools):
            for p in pools:
                if i < len(p) and len(pick) < max_cards: pick.append(p[i])
            i += 1
        keep = {id(c) for c in pick}
        cards = [c for p in pools for c in p if id(c) in keep]
        g = {"id": gid, "title": title, "quizlet": "", "notes": notes, "cards": cards, "points": points}
        if dump: g["dump"] = dump
        return g

    P = lambda i, k: by[i]["points"][k]
    groups = [
        group("theories", "Atomic theories", [
            ("The five models side by side", by["models"]["notes"], by["models"]["cards"]),
            ("Early atomic theory and Dalton", by["dalton"]["notes"], by["dalton"]["cards"]),
            ("Thomson, Rutherford and the gold foil", by["goldfoil"]["notes"], by["goldfoil"]["cards"]),
            ("The quantum mechanical model", qm_theory, qm_cards_t)],
            [P("dalton", 1), P("dalton", 3), P("goldfoil", 0), P("goldfoil", 6),
             "Class order: Democritus (first atomic theory), Dalton (atoms can't be created, divided or destroyed), Thomson (plum pudding), Rutherford (gold foil, nucleus), Bohr (electrons in paths around the nucleus), modern theory (electron clouds)",
             qm["points"][0], qm["points"][2]]),
        group("atoms", "Atoms, ions and isotopes", [
            ("The nucleus, atomic number and mass number", by["nucleus"]["notes"], by["nucleus"]["cards"]),
            ("Ions", by["ions"]["notes"], by["ions"]["cards"]),
            ("Isotopes", iso_a + tail, iso_cards_a),
            ("Explain it", ex_a, [c for c in ex_cards if "isotope" in c[0].lower() or "mg" in c[0].lower()])],
            [P("nucleus", 0), P("nucleus", 4), P("nucleus", 5), P("ions", 1), P("ions", 2), P("ions", 3),
             iso["points"][0], iso["points"][1], iso["points"][9]]),
        group("avgmass", "Average atomic mass", [
            ("", iso_b[1:] if iso_b and iso_b[0].get("h") else iso_b, iso_cards_b),
            ("Practice", by["mass"]["notes"], [])],
            [iso["points"][2], iso["points"][3], iso["points"][5], iso["points"][7], iso["points"][8],
             "Practice answers: Cl 35.45, X 10.81 (boron), Cu 63.55, Si 28.09"],
            dump=[{"p": "Write the formula and the steps from memory. Then solve these with a calculator."},
                  {"list": ["Chlorine: 34.969 amu (75.78%), 36.966 amu (24.22%)",
                            "Element X: 10.013 amu (19.9%), 11.009 amu (80.1%). Which element?",
                            "Copper: 62.930 amu (69.15%), 64.928 amu (30.85%)",
                            "Silicon: 27.977 (92.23%), 28.976 (4.68%), 29.974 (3.09%)"]}]),
        cut(by["bohr"], title="Bohr's model"),
        dict(copy.deepcopy(EM), dump=EM_DUMP),
        cut(exc, cards=exc_cards, title="Ground state vs excited state"),
        group("econfig", "Electron configuration", [
            ("Electron configurations and the Aufbau principle", by["econfig"]["notes"], by["econfig"]["cards"]),
            ("Noble gas notation, exceptions and ions", by["noblegas"]["notes"], by["noblegas"]["cards"]),
            ("Valence electrons", by["valence"]["notes"], by["valence"]["cards"]),
            ("Explain it", ex_b, [c for c in ex_cards if "4s" in c[0] or "cr" in c[0].lower() or "cu" in c[0].lower()]),
            ("Drills", by["drills"]["notes"], [])],
            [by["econfig"]["points"][1], by["econfig"]["points"][2], by["econfig"]["points"][4],
             by["noblegas"]["points"][0], by["noblegas"]["points"][2], by["noblegas"]["points"][4], by["valence"]["points"][1],
             "Drills: Ni [Ar] 4s² 3d⁸, Zn²⁺ [Ar] 3d¹⁰, Mn²⁺ and Fe³⁺ [Ar] 3d⁵, Co²⁺ [Ar] 3d⁷, Cl⁻ [Ar]"],
            dump=[{"p": "Write the filling order and every rule you remember. Then write these, full and in noble gas notation."},
                  {"list": ["Cu", "Cr", "Ni", "Zn²⁺", "Mn²⁺", "Fe³⁺", "Co²⁺", "Cl⁻"]}]),
        group("orbdiag", "Orbital diagrams", [
            ("Orbitals: s, p, d and f", qm_orb, qm_cards_o),
            ("Orbital diagrams, Pauli and Hund's rule", by["orbdiag"]["notes"], by["orbdiag"]["cards"])],
            [qm["points"][3], qm["points"][4], by["orbdiag"]["points"][0], by["orbdiag"]["points"][1],
             by["orbdiag"]["points"][2], by["orbdiag"]["points"][3]]),
    ]
    for g in groups:
        if g["id"] == "bohr": g["id"] = "bohr"
    aliases = {"dalton": "theories", "goldfoil": "theories", "models": "theories", "qmmodel": "orbdiag",
               "nucleus": "atoms", "ions": "atoms", "isotopes": "atoms", "mass": "avgmass", "excited": "excited",
               "noblegas": "econfig", "valence": "econfig", "drills": "econfig", "explain": "econfig",
               "qnumbers": "orbdiag", "quantum": "orbdiag", "config": "econfig"}
    groupmap = {"theories": ["dalton", "goldfoil"], "atoms": ["nucleus", "ions", "isotopes"], "avgmass": [],
                "bohr": ["bohr"], "emspec": [], "excited": ["excited"], "econfig": ["econfig", "noblegas", "valence"],
                "orbdiag": ["qmmodel", "orbdiag"]}
    new_secs = {g: [x for i in ids for x in secs.get(i, [])] for g, ids in groupmap.items()}
    new_secs["emspec"] = ["Order: Radio, Microwave, Infrared, Visible, UV, X-ray, Gamma", "Short wavelength = high frequency = high energy", "Red least energy, violet most", "Emission = bright lines, absorption = dark lines"]
    new_secs = {k: v for k, v in new_secs.items() if v}
    rest = [s for s in sections if s["id"] == "packet"]
    G = {g["id"]: g for g in groups}
    # Class one-pager reference (Nov 9): steps, reactivity, dot diagrams, orbital shapes, box diagrams
    th = G["theories"]
    th["cards"] = [["Atom (class vocab)", "The basic building block of matter, the smallest particle an element can be divided into"],
                   ["Law of conservation of mass (class vocab)", "Even though matter can change form, its total mass stays the same"]] + th["cards"]
    th["notes"] = [{"key": "**Class vocab:** an **atom** is the basic building block of matter, the smallest particle an element can be divided into. **Law of conservation of mass:** even though matter can change form, its total mass stays the same."}] + th["notes"]
    am = G["avgmass"]
    am["notes"] = [{"key": "**The class's 4 steps:**\n1. Identify the isotopes.\n2. Find each isotope's mass and abundance.\n3. Multiply each mass by its abundance (as a decimal).\n4. Add all the results together."}] + am["notes"]
    am["cards"] = [["Average atomic mass, the 4 class steps", "1. Identify the isotopes. 2. Find mass and abundance. 3. Multiply mass by abundance. 4. Add the results."]] + am["cards"]
    b = G["bohr"]
    b["notes"] = [{"key": "**What a ring can hold vs what an atom has.** Ring 1 holds up to **2** electrons, ring 2 up to **8**, ring 3 up to **8**. You fill from the inside out and stop when you run out.\nMagnesium has 12: ring 1 takes 2 (10 left), ring 2 takes 8 (2 left), ring 3 gets the last 2. So **Mg = 2-8-2**. Chlorine has 17: **2-8-7**.\nIt matches the configuration: ring 1 is 1s (2), ring 2 is 2s + 2p (2 + 6 = 8), ring 3 is 3s + 3p."}] + b["notes"]
    b["notes"] += [
        {"p": "Chemists use Bohr diagrams to **predict how reactive an element is**: the outer ring shows the **valence electrons**, and an atom with a nearly full or nearly empty outer ring reacts easily."},
        {"h": "Electron dot diagrams"},
        {"p": "A dot diagram (Lewis dot) shows only the **valence electrons**: the last number of the Bohr configuration. Write the symbol, then place dots **clockwise** starting at the top, one per side, and only start pairing after all four sides have one."},
        {"list": ["Write the element's symbol, like **Cl**.",
                  "Count the valence electrons: the last number of the Bohr configuration. Cl is 2-8-7, so **7**.",
                  "Dots 1 to 4: one on the **top**, one on the **right**, one on the **bottom**, one on the **left**.",
                  "Dots 5 to 8: go around again in the same order, putting each new dot next to the first one to make a **pair**.",
                  "Cl ends with three pairs and one single dot on the left. 8 dots is the most a dot diagram ever has."]},
        {"img": "img/u2/cl-dot-steps.png"},
        {"alt": "Chlorine's 7 dots numbered in the order you draw them, then the finished diagram"},
        {"img": "img/u2/dot-diagrams.png"},
        {"alt": "Dot diagrams for Na (1 dot), Mg (2), N (5), Cl (7) and Ne (8)"},
        {"key": "Chlorine is 2-8-7, so 7 dots: three pairs and one single. Neon is 2-8, so 8 dots, a full octet."}]
    b["cards"] += [["Electron dot diagram", "The symbol with one dot per valence electron"],
                   ["How do you place dots in a dot diagram?", "Clockwise from the top, one per side, then pair them up (max 8)"],
                   ["Dot diagram for chlorine (2-8-7)", "Cl with 7 dots: three pairs and one single dot"],
                   ["What do chemists use Bohr models for?", "To predict reactivity: the outer ring shows the valence electrons"]]
    b["points"] = b["points"] + ["Dot diagram: valence electrons only, clockwise from the top, pair after all four sides have one"]
    e = G["emspec"]
    e["notes"].insert(2, {"p": "Another way to say it: the EM spectrum is the **full range of all types of electromagnetic radiation, ordered by frequency and wavelength**."})
    ec = G["econfig"]
    ec["notes"] = [{"h": "One element, written three ways"},
                   {"p": "Tests often ask for the same element as a **normal** configuration, in **noble gas** notation, and as an **orbital diagram**. Oxygen has only 8 electrons, so all three are short."},
                   {"img": "img/u2/oxygen-three-ways.png"},
                   {"alt": "Oxygen: 1s² 2s² 2p⁴, [He] 2s² 2p⁴, and boxes 1s ↑↓, 2s ↑↓, 2p ↑↓ ↑ ↑"},
                   {"list": ["**Normal:** write every sublevel: 1s² 2s² 2p⁴ (2 + 2 + 4 = 8).",
                             "**Noble gas:** the noble gas before oxygen is helium (1s²), so swap that part for [He]: **[He] 2s² 2p⁴**.",
                             "**Orbital diagram:** one box per orbital (1s, 2s, three 2p). In 2p put one ↑ in each box first (Hund), then the 4th electron pairs up in the first box: ↑↓ ↑ ↑.",
                             "**Unpaired** means an electron alone in its box. Oxygen has **2 unpaired**, nitrogen (2p³: ↑ ↑ ↑) has 3."]}] + ec["notes"]
    ec["cards"] = [["Oxygen, normal configuration", "1s² 2s² 2p⁴"], ["Oxygen, noble gas notation", "[He] 2s² 2p⁴"],
                   ["Oxygen orbital diagram", "1s ↑↓ · 2s ↑↓ · 2p ↑↓ ↑ ↑ (2 unpaired)"],
                   ["What does unpaired mean?", "An electron alone in its orbital box (no ↓ partner)"]] + ec["cards"]
    b["cards"] = [["How many electrons can rings 1, 2 and 3 hold?", "Up to 2, then 8, then 8 (fill inside out, stop when you run out)"],
                  ["Why is Mg 2-8-2 and not 2-8-8?", "Mg only has 12 electrons: 2 + 8 uses 10, so ring 3 only gets the last 2"]] + b["cards"]
    o = G["orbdiag"]
    for n in o["notes"]:
        if "table" in n:
            for r in n["table"]["rows"]:
                if r[0] == "s": r[3] = "Sphere"
                if r[0] == "d": r[3] = "Cloverleaf"
                if r[0] == "f": r[3] = "Complex"
    i = next((k for k, n in enumerate(o["notes"]) if n.get("h", "").startswith("Orbital diagrams")), len(o["notes"]))
    o["notes"][i + 1:i + 1] = [{"img": "img/u2/orbital-boxes.png"}, {"alt": "Orbital box diagrams: fluorine, nitrogen drawn right, nitrogen breaking Hund's rule, helium breaking Pauli"},
                               {"p": "Draw one box per orbital: 1 box for s, 3 for p, 5 for d, 7 for f. Put one arrow of each spin in each box before you double up."}]
    o["cards"] += [["Shape of an s orbital", "Sphere"], ["Shape of a p orbital", "Dumbbell"], ["Shape of a d orbital", "Cloverleaf"], ["Shape of an f orbital", "Complex shapes"],
                   ["Boxes per sublevel in an orbital diagram", "s 1, p 3, d 5, f 7"]]
    return groups, rest, aliases, dict(review, secs=new_secs)
