# Chemistry study site, built with the studynow kit: python3 build.py course.py site
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit1 import SECTIONS as U1, REVIEW as R1
from unit2 import SECTIONS as U2, REVIEW as R2
from quiz2 import QUIZ
U2 = [s for s in U2 if s["id"] != "packet"] + [QUIZ] + [s for s in U2 if s["id"] == "packet"]

COURSE = {
 "name": "Chemistry, 10th grade",
 "eyebrow": "The Clinton School, 2026 to 2027",
 "intro": "Quizzes can be unannounced and run about 1 minute per point.",
 "cumulative": True,
 "img": "img",
 "breakMinutes": 5, "dumpMinutes": 7,
 "units": [
  {"label": "Unit 1", "name": "Matter and measurement", "title": "Chemistry unit 1",
   "chip": "Test was Friday, Oct 16",
   "topics": "Classification of matter, properties and changes, states of matter, separation, lab tools, metric system, scientific notation, sig figs, density, accuracy and precision, graphs",
   "source": "From your study guide doc, sections 1 to 11",
   "sections": U1, "review": R1},
  {"label": "Unit 2", "name": "Atomic structure", "title": "Chemistry unit 2",
   "chip": "Quiz Monday, Nov 2",
   "topics": "Dalton's theory, plum pudding, gold foil, the nucleus, ions, isotopes, average atomic mass, Bohr model, ground and excited states, quantum mechanical model, orbitals, quantum numbers, electron configurations, Aufbau, Pauli, Hund's rule, noble gas notation, valence electrons",
   "source": "From class, the Atom Practice Packet, CK-12, the class drive and the scribe notes. More topics get added as the unit goes on.",
   "sections": U2, "review": R2}]}
