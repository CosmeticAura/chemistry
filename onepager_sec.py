RUBRIC = [
 {"p": "The one pager is graded all or nothing on each line of this rubric (8 points). Check every line before you hand it in."},
 {"table": {"head": ["Criteria", "What it needs", "Pts"], "rows": [
   ["**Layout**", "Fills the whole page, organized structure, legible", "1"],
   ["**Color**", "Color differentiates or groups ideas in a logical way", "2"],
   ["**Diagrams**", "At least 3 relevant diagrams or sketches", "2"],
   ["**Worked sample problems**", "At least 3 UNIQUE worked problems", "2"],
   ["**Chemistry content**", "All the specified information from the unit", "1"]]}},
 {"h": "What has to be on it (the 8 test topics)"},
 {"list": ["**Atomic theories:** Democritus, Dalton, Thomson, Rutherford, Bohr, modern theory (electron cloud), each with what they said",
           "**Atoms, ions and isotopes:** protons = atomic #, neutrons = mass # − atomic #, electrons = protons − charge",
           "**Average atomic mass:** the 4 steps, plus a worked example",
           "**Bohr's model:** a Bohr diagram, filling 2, 8, 8, and what it's used for (valence electrons, reactivity), plus an electron dot diagram",
           "**Electromagnetic spectrum:** the order, wavelength vs frequency vs energy",
           "**Ground vs excited state:** both definitions and an example",
           "**Electron configuration:** Aufbau, Pauli, Hund, normal vs noble gas notation",
           "**Orbital diagrams:** the s, p, d, f table (orbitals, max electrons, shapes) and a box diagram"]},
 {"h": "Ideas that score"},
 {"list": ["**Color:** pick a color per group of topics and say so in a key, like blue for what atoms are made of, orange for energy and light, green for where electrons go. Random colors don't count as logical.",
           "**Diagrams:** a Bohr diagram, a dot diagram, an orbital box diagram, the EM spectrum strip, the atomic model sketches. Five is safer than three.",
           "**Worked problems, all different:** particles in an ion (Fe³⁺), average atomic mass (chlorine), a configuration in full and noble gas notation (Fe or Fe²⁺).",
           "**Fill the page:** no empty corners. Plan the boxes in pencil first."]},
]
RUBRIC_CARDS = [
 ["One pager: layout (1 pt)", "Fills the page, organized, legible"],
 ["One pager: color (2 pts)", "Color groups ideas in a logical way"],
 ["One pager: diagrams (2 pts)", "At least 3 relevant diagrams or sketches"],
 ["One pager: worked problems (2 pts)", "At least 3 unique worked sample problems"],
 ["One pager: content (1 pt)", "Everything specified from the unit is included"],
]
def section(with_image=False):
    notes = list(RUBRIC)
    if with_image:
        notes = [{"p": "This is a finished example that hits every line of the rubric. Use it to study, and copy the structure into your sketchbook in your own handwriting."},
                 {"img": "img/u2/one-pager.png"}, {"alt": "Unit 2 one pager with blue, orange and green boxes"}] + notes
    return {"id": "onepager", "title": "One pager (rubric)", "quizlet": "", "notes": notes, "cards": RUBRIC_CARDS,
            "points": ["Fills the page", "Color by group, with a key", "3+ diagrams", "3+ unique worked problems", "All 8 topics"]}
