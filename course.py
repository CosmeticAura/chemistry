# Chemistry study site, built with the studynow kit: python3 build.py course.py site
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit1 import SECTIONS as U1, REVIEW as R1
from unit2 import SECTIONS as U2, REVIEW as R2
from quiz2 import QUIZ
MOCK = {"id": "mock2", "title": "Mock test (timed, grades itself)", "steps": [0], "cards": [], "points": [],
 "notes": [
  {"p": "40 minutes, 30 points: atomic theories, atoms and ions, isotopes and average atomic mass, configurations, noble gas notation and orbital diagrams. Work on paper, type the final answers, then press Grade my test and send the results to Claude."},
  {"p": "**[Open the mock test](https://cosmeticaura.github.io/chemistry/mock-test/)**"}]}
U2 = [MOCK] + [s for s in U2 if s["id"] != "packet"] + [QUIZ] + [s for s in U2 if s["id"] == "packet"]

COURSE = {
 "name": "Chemistry, 10th grade",
 "eyebrow": "The Clinton School, 2026 to 2027",
 "intro": "Quizzes can be unannounced and run about 1 minute per point.",
 "cumulative": True,
 "img": "img",
 "breakMinutes": 5, "dumpMinutes": 7,
 "extras": [{"eyebrow": "Test Mon, Nov 2", "title": "Unit 2 mock test", "text": "40 minutes, 30 points: theories, atoms and ions, isotopes, configurations and orbital diagrams. Grades itself and copies your results.", "href": "mock-test/"}],
 "units": [
  {"label": "Unit 1", "name": "Matter and measurement", "title": "Chemistry unit 1",
   "chip": "Test was Friday, Oct 16",
   "topics": "Classification of matter, properties and changes, states of matter, separation, lab tools, metric system, scientific notation, sig figs, density, accuracy and precision, graphs",
   "source": "From your study guide doc, sections 1 to 11",
   "sections": U1, "review": R1},
  {"label": "Unit 2", "name": "Atomic structure", "title": "Chemistry unit 2",
   "chip": "Test Mon, Nov 2",
   "topics": "Dalton's theory, plum pudding, gold foil, the nucleus, ions, isotopes, average atomic mass, Bohr model, ground and excited states, quantum mechanical model, orbitals, quantum numbers, electron configurations, Aufbau, Pauli, Hund's rule, noble gas notation, valence electrons",
   "source": "From class, the Atom Practice Packet, CK-12, the class drive and the scribe notes. More topics get added as the unit goes on.",
   "sections": U2, "review": R2}]}
