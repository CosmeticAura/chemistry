# Chemistry study site, built with the studynow kit: python3 build.py course.py site
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit1 import SECTIONS as U1, REVIEW as R1
from unit2 import SECTIONS as U2, REVIEW as R2
from quiz2 import QUIZ
from plan2 import PLAN_SECTIONS
from merge8 import merge
from merge1 import merge as merge1
MOCK = {"id": "mock2", "title": "Mock test (timed, grades itself)", "steps": [0], "cards": [], "points": [],
 "notes": [
  {"p": "40 minutes, 30 points: atomic theories, atoms and ions, isotopes and average atomic mass, configurations, noble gas notation and orbital diagrams. Work on paper, type the final answers, then press Grade my test and send the results to Claude."},
  {"p": "**[Open the mock test](https://cosmeticaura.github.io/chemistry/mock-test/)**"},
  {"p": "Already took it? **[Mock test B](https://cosmeticaura.github.io/chemistry/mock-test-2/)** has all new questions, same format, for Sunday."}]}
U1, _R1REST, ALIASES1, R1 = merge1(U1, R1)
U1 = U1 + _R1REST
GROUPED, REST, ALIASES, R2 = merge(PLAN_SECTIONS + U2, R2)
U2 = GROUPED + [QUIZ] + REST

COURSE = {
 "name": "Chemistry, 10th grade",
 "eyebrow": "The Clinton School, 2026 to 2027",
 "intro": "Quizzes can be unannounced and run about 1 minute per point.",
 "cumulative": True,
 "img": "img",
 "breakMinutes": 2.5, "dumpMinutes": 7,
 "extras": [{"eyebrow": "Unit 2 quiz, Nov 2", "title": "Quiz mock tests", "text": "Mock tests A and B from the Nov 2 quiz.", "href": "mock-test/"}],
 "units": [
  {"label": "Unit 1", "name": "Matter and measurement", "title": "Chemistry unit 1",
   "chip": "Test was Friday, Oct 16",
   "topics": "Classification of matter, properties and changes, states of matter, separation, lab tools, metric system, scientific notation, sig figs, density, accuracy and precision, graphs",
   "source": "From your study guide doc, sections 1 to 11",
   "sections": U1, "review": R1, "aliases": ALIASES1},
  {"label": "Unit 2", "name": "Atomic structure", "title": "Chemistry unit 2",
   "chip": "Unit test Fri, Nov 13",
   "topics": "The 8 topics on the unit test: atomic theories, atoms, ions and isotopes, average atomic mass, Bohr's model, electromagnetic spectra, ground vs excited state, electron configuration, orbital diagrams",
   "source": "From class, the Atom Practice Packet, CK-12, the class drive and the scribe notes. Grouped into the 8 topics on the unit test.",
   "sections": U2, "review": R2, "aliases": ALIASES}]}
