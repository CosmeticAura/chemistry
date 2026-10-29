# Unit 2 practice quiz. Every answer is computed here, not typed in.
SYM = 'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag'.split()
NAME = {13: 'aluminum', 5: 'boron', 17: 'chlorine', 18: 'argon', 25: 'manganese', 34: 'selenium', 45: 'rhodium', 33: 'arsenic', 15: 'phosphorus'}
ORDER = '1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p'.split()
CAP = dict(s=2, p=6, d=10, f=14)
SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
CORES = [(36, 'Kr'), (18, 'Ar'), (10, 'Ne'), (2, 'He')]

def fill(n):
    out = []
    for o in ORDER:
        if n <= 0: break
        k = min(n, CAP[o[-1]]); out.append(o + str(k).translate(SUP)); n -= k
    return out

def full(n): return ' '.join(fill(n))

def noble(n):
    for c, s in CORES:
        if n > c: return f'[{s}] ' + ' '.join(fill(n)[len(fill(c)):])

def shells(n):
    out, caps = [], [2, 8, 8, 2]
    for c in caps:
        k = min(n, c); out.append(k); n -= k
        if n == 0: break
    return out

def avg(pairs): return sum(m * p for m, p in pairs) / 100

Q, A = [], []
def q(text, ans): Q.append(text); A.append(ans)

q('Put the atomic models in order and name the model that came right after Rutherford\'s.',
  'Dalton, Thomson, Rutherford, Bohr, Schrödinger (Dogs Trust Really Big Squirrels). After Rutherford came **Bohr\'s planetary model** (1913).')
q('In the gold foil experiment most alpha particles went straight through. What did that show?', 'The atom is **mostly empty space**.')
q('A few alpha particles bounced straight back. What did that show, and why does it mean the nucleus is positive?',
  'A **tiny, dense nucleus** holds the mass. Alpha particles are positive and like charges repel, so the nucleus is **positive**.')
q('Which particle hardly adds to an atom\'s mass?', 'The **electron** (about 1/1840 of a proton).')
p, n, e = 17, 18, 18
q(f'An atom or ion has {p} protons, {n} neutrons and {e} electrons. What is it, what is its mass number and what is its charge?',
  f'**{NAME[p].capitalize()}**, mass number **{p+n}**, charge **{e-p}−** (more electrons than protons), so ³⁵₁₇Cl⁻.')
Z, M, c = 13, 27, 3
q('How many protons, neutrons and electrons are in ²⁷₁₃Al³⁺?', f'**{Z} protons, {M-Z} neutrons, {Z-c} electrons** (electrons = protons − charge).')
q('Carbon-12 and carbon-14 are isotopes. What is different about them, and what is the same?',
  'Different number of **neutrons** (6 and 8), so different mass numbers. Same protons (6), same electrons, same chemistry.')
ga = avg([(68.926, 60.1), (70.925, 39.9)])
q('Gallium is 60.1% Ga-69 (68.926 amu) and 39.9% Ga-71 (70.925 amu). Find the average atomic mass.',
  f'(68.926 × 60.1 + 70.925 × 39.9) ÷ 100 = **{ga:.2f} amu**. It is closer to 69 because Ga-69 is more common.')
b = avg([(10.013, 19.9), (11.009, 80.1)])
q('Element X is 19.9% X-10 (10.013 amu) and 80.1% X-11 (11.009 amu). Find its average atomic mass and name it.',
  f'(10.013 × 19.9 + 11.009 × 80.1) ÷ 100 = **{b:.2f} amu**, which is **boron**.')
ex = [2, 8, 7, 1]; tot = sum(ex)
q('Is 2-8-7-1 a ground state or an excited state? Which element is it?',
  f'{tot} electrons, so it is **{NAME[tot]}**. Its ground state is {"-".join(map(str, shells(tot)))}, so 2-8-7-1 is **excited**.')
q('An electron drops from level 4 to level 2. Does the atom absorb or release energy, and what do you see?',
  'It **releases** energy as light of one color, a line in the **bright line spectrum**. Up = absorb, down = release.')
q('What is the most electrons energy level n = 4 can hold?', f'2n² = 2 × 4² = **{2*4**2}**')
q('Write the full electron configuration of manganese (25).', f'**{full(25)}**')
q('Write the noble gas notation for selenium (34).', f'**{noble(34)}**')
q('Which element is [Kr] 5s² 4d⁷?', f'36 + 2 + 7 = {36+2+7} electrons, so **{NAME[45]} ({SYM[44]})**.')
q('Draw the 3p orbital diagram for phosphorus. How many unpaired electrons does it have, and which rule decides it?',
  '3p **↑ ↑ ↑**, so **3 unpaired**. **Hund\'s rule**: one in each box before any pair up.')
q('A student draws nitrogen\'s 2p as ↑↓ ↑ _. Which rule is broken?', '**Hund\'s rule.** It should be ↑ ↑ ↑.')
q('If n = 3, what values can l have, and how many orbitals are in level 3?', f'l = **0, 1, 2** (s, p, d). n² = **{3**2} orbitals**.')
q('How many valence electrons does arsenic (group 15) have, and how many dots go in its Lewis dot diagram?',
  f'Group 15 − 10 = **{15-10}** valence electrons, so **5 dots** (4s² 4p³).')
q('Write the electron configuration of S²⁻. Which noble gas has the same one?',
  f'16 + 2 = 18 electrons: **{full(18)}**, the same as **argon**.')
q('Write chromium\'s configuration and say why it is an exception.',
  '**[Ar] 4s¹ 3d⁵**, not 4s² 3d⁴. A half full d sublevel is more stable, so one electron moves from 4s to 3d.')

QUIZ = {"id": "u2quiz", "title": "Practice quiz", "steps": [0],
 "notes": [
  {"p": f"{len(Q)} questions in the style of a class quiz, about a minute each. Cover the answers, write yours on paper with the work shown, then check. Redo the loop for any section you missed."},
  {"list": [f'**{i}.** {t}' for i, t in enumerate(Q, 1)]},
  {"h": "Answers"},
  {"table": {"head": ["#", "Answer"], "rows": [[str(i), a] for i, a in enumerate(A, 1)]}}],
 "cards": [], "points": []}

if __name__ == '__main__':
    for i, (t, a) in enumerate(zip(Q, A), 1): print(i, t, '\n   ->', a)
