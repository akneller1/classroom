from lib import Bank, graph
from mathlite import *
import math

STD = {1: ["S-CP.B.9"], 2: ["S-CP.B.9"], 3: ["S-CP.A.2", "S-CP.B.8"], 4: ["S-CP.A.3", "S-CP.A.4", "S-CP.B.6"], 5: ["S-MD.A.1"], 6: ["S-MD.A.2", "S-MD.B.5"], 7: ["S-ID.A.4"], 8: ["S-IC.A.1", "S-IC.B.3", "S-IC.B.4"]}
B = Bank("probability-statistics", "ps", STD)
C, Pm, fact = math.comb, math.perm, math.factorial
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))


def pct(v, d=1): return f"{v * 100:.{d}f}%"


# ---------------- Skill 1: counting and permutations ----------------
S = 1
for desc, ans, steps, lvl in [("A menu has 4 appetizers, 6 entrées, and 3 desserts. How many 3-course meals are possible?", 72, ["Fundamental counting principle: 4·6·3."], "cp2"),
                              ("How many 4-digit PINs are possible if digits may repeat?", 10000, ["10⁴."], "cp2"),
                              ("How many license plates have 3 letters followed by 3 digits (repetition allowed)?", 26 ** 3 * 10 ** 3, ["26³·10³."], "cp1"),
                              ("How many 3-letter codes use distinct letters?", 26 * 25 * 24, ["26·25·24."], "cp1"),
                              ("A quiz has 8 true/false questions. How many answer keys are possible?", 256, ["2⁸."], "cp2"),
                              ("How many even 3-digit numbers can be formed from the digits 1–6 without repetition?", 3 * 5 * 4, ["Last digit even: 3 choices; then 5 and 4."], "honors")]:
    B.sa(S, lvl, desc, f"{ans:,}", steps)
for n_, r in [(5, 5), (7, 3), (10, 4), (8, 2), (6, 6), (12, 3)]:
    B.sa(S, "cp2" if n_ == r else "cp1", f"Evaluate ₙPᵣ for n = {n_}, r = {r}.", f"{Pm(n_, r):,}", [f"{n_}!/({n_} - {r})!.", f"= {Pm(n_, r):,}."])
for word in ["MATH", "LEVEL", "BANANA", "MISSISSIPPI", "STATS"]:
    cnt = {c: word.count(c) for c in set(word)}; tot = fact(len(word))
    for v in cnt.values(): tot //= fact(v)
    B.sa(S, "cp1" if len(word) < 7 else "honors", f"How many distinguishable arrangements of the letters in {word}?", f"{tot:,}", [f"{len(word)}! divided by the factorial of each repeated letter count.", f"= {tot:,}."])
for n_, r, ctx in [(10, 3, "gold, silver, and bronze medals are awarded among 10 runners"), (8, 8, "8 students line up for a photo"), (12, 4, "a president, VP, secretary, and treasurer are chosen from 12 members")]:
    B.mc(S, "cp1", f"In how many ways can {ctx}?", f"{Pm(n_, r):,}", [f"{C(n_, r):,}" if C(n_, r) != Pm(n_, r) else f"{n_ ** r:,}", f"{n_ ** r:,}" if n_ ** r != Pm(n_, r) else f"{fact(n_) * 2:,}", f"{n_ * r:,}"], ["Order matters → permutation.", f"{n_}P{r} = {Pm(n_, r):,}."], tags=["misconception"])
B.mc(S, "cp1", "In how many ways can 6 people sit around a circular table (rotations are the same)?", "120", ["720", "36", "6"], ["Fix one person: (6 - 1)! = 120."], tags=["challenge"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to ₇P₃.", ["7·6·5", "210", "7!/4!", "7!/3!", "C(7, 3)·3!", "7³"], lambda s_: {"7·6·5": 210, "210": 210, "7!/4!": 210, "7!/3!": 840, "C(7, 3)·3!": 210, "7³": 343}[s_] == 210, ["ₙPᵣ = n!/(n - r)! = C(n, r)·r!."])
sel_auto(B, S, "honors", "Select ALL situations where order matters.", ["Arranging books on a shelf", "Assigning 1st, 2nd, 3rd place", "Creating a password", "Choosing 3 toppings for a pizza", "Selecting a 5-person committee", "Dealing a 5-card hand"],
         lambda s_: s_ in ("Arranging books on a shelf", "Assigning 1st, 2nd, 3rd place", "Creating a password"), ["Different orders give different outcomes → permutation."], tags=["reasoning"])
B.orq(S, "cp1", "Using the digits 1, 2, 3, 4, 5 without repetition:", [("How many 5-digit numbers?", "120"), ("How many 3-digit numbers?", "60"), ("How many 3-digit numbers are odd?", "36"), ("How many 3-digit numbers are greater than 300?", "36")],
      ["5!.", "5·4·3.", "Last digit 1, 3, 5: 3·4·3.", "First digit 3, 4, 5: 3·4·3."])
B.orq(S, "honors", "Seven people (including Ana and Ben) line up.", [("Total arrangements.", "5040"), ("Arrangements with Ana first.", "720"), ("Arrangements with Ana and Ben together.", "1440"), ("Arrangements with Ana and Ben not together.", "3600")],
      ["7!.", "6!.", "Treat as a block: 6!·2.", "5040 - 1440."], tags=["challenge"])
assert fact(6) * 2 == 1440 and 5040 - 1440 == 3600
B.sa(S, "cp2", "Evaluate 5!.", "120", ["5·4·3·2·1."])

# ---------------- Skill 2: combinations ----------------
S = 2
for n_, r in [(6, 2), (10, 3), (8, 5), (12, 6), (52, 5), (20, 1), (15, 13)]:
    B.sa(S, "cp2" if n_ <= 10 else "cp1", f"Evaluate C({n_}, {r}).", f"{C(n_, r):,}", [f"C(n, r) = n!/(r!(n - r)!).", f"= {C(n_, r):,}."])
for ctx, n_, r in [("choose 4 students from 15 for a committee", 15, 4), ("choose 3 toppings from 10", 10, 3), ("select 5 cards from a 52-card deck", 52, 5), ("pick 2 co-captains from 18 players", 18, 2)]:
    B.mc(S, "cp1", f"In how many ways can you {ctx}?", f"{C(n_, r):,}", [f"{Pm(n_, r):,}", f"{n_ ** r:,}", f"{C(n_, r - 1):,}"], ["Order does not matter → combination.", f"C({n_}, {r}) = {C(n_, r):,}."], tags=["misconception"])
for desc, ans, steps in [("A committee of 5 is chosen from 7 teachers and 6 students. How many committees have exactly 3 teachers?", C(7, 3) * C(6, 2), ["C(7, 3)·C(6, 2) = 35·15."]),
                         ("How many 5-card hands contain exactly 2 aces?", C(4, 2) * C(48, 3), ["C(4, 2)·C(48, 3)."]),
                         ("A pizza place offers 8 toppings. How many pizzas have at most 2 toppings?", C(8, 0) + C(8, 1) + C(8, 2), ["C(8, 0) + C(8, 1) + C(8, 2) = 1 + 8 + 28."]),
                         ("How many 5-card hands are all hearts?", C(13, 5), ["C(13, 5)."]),
                         ("From 10 people, how many committees of 4 include a specific person?", C(9, 3), ["Include that person; choose 3 more from 9."])]:
    B.sa(S, "cp1" if "exactly 3" in desc or "all hearts" in desc else "honors", desc, f"{ans:,}", steps)
for n_, r in [(5, 2), (7, 3)]:
    B.sa(S, "cp1", f"Show that C({n_}, {r}) = C({n_}, {n_ - r}) and explain why.", f"Both equal {C(n_, r)}; choosing {r} to include is the same as choosing {n_ - r} to leave out", ["Compute both.", "Complement reasoning."], tags=["reasoning"])
B.mc(S, "cp1", "A student computes the number of 3-person teams from 9 people as ₉P₃ = 504. What is correct?", "84, because order does not matter: C(9, 3)", ["504", "729", "27"], ["C(9, 3) = 504/3! = 84."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to C(8, 3).", ["56", "C(8, 5)", "8!/(3!5!)", "₈P₃/3!", "₈P₃", "8·7·6", "C(8, 3) + C(8, 4) - C(9, 4)"],
         lambda s_: {"56": 56, "C(8, 5)": C(8, 5), "8!/(3!5!)": 56, "₈P₃/3!": 56, "₈P₃": 336, "8·7·6": 336, "C(8, 3) + C(8, 4) - C(9, 4)": C(8, 3) + C(8, 4) - C(9, 4)}[s_] == 56, ["C(n, r) = C(n, n - r) = ₙPᵣ/r!.", "Pascal: C(8, 3) + C(8, 4) = C(9, 4), so the last is 0."])
B.orq(S, "cp1", "A class of 12 boys and 10 girls chooses a 4-person team.", [("Total teams.", f"{C(22, 4):,}"), ("Teams of all girls.", f"{C(10, 4)}"), ("Teams with 2 boys and 2 girls.", f"{C(12, 2) * C(10, 2):,}"), ("Teams with at least 1 boy.", f"{C(22, 4) - C(10, 4):,}")],
      ["C(22, 4).", "C(10, 4).", "C(12, 2)·C(10, 2).", "Complement."], tags=["multistep"])
B.orq(S, "honors", "Use Pascal's triangle and combinations.", [("Write row 5 of Pascal's triangle.", "1, 5, 10, 10, 5, 1"), ("Which entry is C(5, 2)?", "10"), ("Expand (x + y)⁴'s x²y² coefficient.", "6"), ("Find the sum of row 6.", "64")],
      ["Each entry is C(5, k).", "Third entry.", "C(4, 2).", "2⁶."], tags=["connections"])
B.sa(S, "cp2", "Evaluate C(9, 0).", "1", ["There is one way to choose nothing."])

# ---------------- Skill 3: independent and dependent events ----------------
S = 3
for pa, pb in [(F(1, 2), F(1, 6)), (F(3, 10), F(2, 5)), (F(1, 4), F(1, 4)), (F(7, 10), F(9, 10))]:
    B.sa(S, "cp2", f"A and B are independent with P(A) = {fr(pa)} and P(B) = {fr(pb)}. Find P(A and B).", fr(pa * pb), ["Independent: P(A and B) = P(A)·P(B)."])
for (r_, b_, k), rep in [((5, 3, 2), False), ((4, 6, 2), True), ((7, 3, 3), False), ((2, 8, 2), False)]:
    tot = r_ + b_
    p = F(r_, tot) ** k if rep else math.prod(F(r_ - i, tot - i) for i in range(k))
    B.sa(S, "cp1", f"A bag has {r_} red and {b_} blue marbles. {k} are drawn {'with' if rep else 'without'} replacement. Find P(all red).", fr(p),
         ["With replacement: same probability each draw (independent)." if rep else "Without replacement: the denominator and red count drop each draw (dependent).", f"= {fr(p)}."])
for desc, ans, steps, lvl in [("Roll two dice. Find P(both show 6).", "1/36", ["(1/6)(1/6)."], "cp2"), ("Flip a coin 5 times. Find P(all heads).", "1/32", ["(1/2)⁵."], "cp2"),
                              ("Draw 2 cards without replacement. Find P(both aces).", "1/221", ["(4/52)(3/51)."], "cp1"), ("Draw 2 cards with replacement. Find P(both hearts).", "1/16", ["(13/52)²."], "cp1"),
                              ("Flip a coin 4 times. Find P(at least one head).", "15/16", ["1 - P(no heads) = 1 - 1/16."], "cp1"), ("Roll a die 3 times. Find P(at least one 6).", "91/216", ["1 - (5/6)³."], "honors")]:
    B.sa(S, lvl, desc, ans, steps)
assert F(4, 52) * F(3, 51) == F(1, 221) and 1 - F(5, 6) ** 3 == F(91, 216)
B.mc(S, "cp1", "P(A) = 0.4, P(B) = 0.5, P(A and B) = 0.2. Are A and B independent?", "Yes, because 0.4·0.5 = 0.2", ["No, because 0.4 + 0.5 ≠ 0.2", "No, because they are mutually exclusive", "Cannot tell"], ["Independent ⇔ P(A and B) = P(A)P(B)."])
B.mc(S, "cp1", "P(A) = 0.3, P(B) = 0.6, P(A and B) = 0.1. Are A and B independent?", "No, because 0.3·0.6 = 0.18 ≠ 0.1", ["Yes, because 0.1 < 0.3", "Yes, because 0.3 + 0.6 < 1", "Cannot tell"], ["Compare P(A and B) with P(A)P(B)."])
B.mc(S, "cp1", "A student says mutually exclusive events with nonzero probabilities are independent. What is correct?", "They are dependent: if one occurs, the other cannot", ["Correct", "They are always independent", "Only if P(A) = P(B)"], ["P(A and B) = 0 ≠ P(A)P(B) > 0."], tags=["misconception"])
sel_auto(B, S, "cp1", "Select ALL pairs of independent events.", ["Rolling a 4 on a die; flipping heads", "Drawing a red card, replacing it, then drawing a red card", "Two different students' birthdays being in May", "Drawing two aces without replacement", "Being late to school and oversleeping", "Rain today and carrying an umbrella"],
         lambda s_: s_ in ("Rolling a 4 on a die; flipping heads", "Drawing a red card, replacing it, then drawing a red card", "Two different students' birthdays being in May"), ["Independent: one outcome does not change the other's probability."])
B.orq(S, "cp1", "A spinner has 4 equal sections (red, blue, green, yellow). Spin twice.", [("P(red then blue).", "1/16"), ("P(both the same color).", "1/4"), ("P(at least one red).", "7/16"), ("Are the spins independent?", "Yes")], ["(1/4)(1/4).", "4·(1/16).", "1 - (3/4)².", "One spin does not affect the other."])
B.orq(S, "honors", "A box has 3 defective and 9 good bulbs. Two are chosen without replacement.", [("P(both defective).", "1/22"), ("P(both good).", "6/11"), ("P(exactly one defective).", "9/22"), ("Check that the three probabilities sum to 1.", "1/22 + 12/22 + 9/22 = 1")],
      ["(3/12)(2/11).", "(9/12)(8/11).", "2·(3/12)(9/11).", "Sum."], tags=["multistep"])
assert F(3, 12) * F(2, 11) + F(9, 12) * F(8, 11) + 2 * F(3, 12) * F(9, 11) == 1

# ---------------- Skill 4: conditional probability ----------------
S = 4
tab = {"Junior": (30, 20), "Senior": (25, 45)}  # (plays sport, does not)
tot = sum(sum(v) for v in tab.values())
B.sa(S, "cp1", "Table — Juniors: 30 play a sport, 20 do not. Seniors: 25 play, 45 do not. Find P(plays a sport | senior).", "5/14", ["Restrict to seniors: 70.", "25/70 = 5/14."], tags=["multiple-representations"])
B.sa(S, "cp1", "Same table. Find P(senior | plays a sport).", "5/11", ["Restrict to sport players: 55.", "25/55."], tags=["multiple-representations"])
B.sa(S, "cp1", "Same table. Find P(junior and does not play).", "1/6", ["20/120."])
B.mc(S, "honors", "Same table. Are 'senior' and 'plays a sport' independent?", "No: P(sport | senior) = 5/14 ≠ P(sport) = 11/24", ["Yes: both are about half", "Yes: 25 + 45 = 70", "Cannot tell"], ["Compare P(sport | senior) with P(sport) = 55/120."], tags=["reasoning"])
for pab, pb in [(F(1, 5), F(1, 2)), (F(3, 20), F(3, 5)), (F(1, 8), F(1, 4)), (F(2, 9), F(2, 3))]:
    B.sa(S, "cp2", f"P(A and B) = {fr(pab)} and P(B) = {fr(pb)}. Find P(A | B).", fr(pab / pb), ["P(A | B) = P(A and B)/P(B)."])
for pa, pba, pbna in [(F(1, 100), F(95, 100), F(5, 100)), (F(2, 10), F(9, 10), F(2, 10)), (F(3, 10), F(8, 10), F(1, 10))]:
    pb = pa * pba + (1 - pa) * pbna; post = pa * pba / pb
    B.sa(S, "honors", f"P(D) = {fr(pa)}. A test is positive with probability {fr(pba)} if D, and {fr(pbna)} if not D. Find P(D | positive).", fr(post),
         [f"P(positive) = {fr(pa)}·{fr(pba)} + {fr(1 - pa)}·{fr(pbna)} = {fr(pb)}.", f"P(D | +) = {fr(pa * pba)}/{fr(pb)} = {fr(post)}."], tags=["challenge", "modeling"])
B.sa(S, "cp1", "Roll two dice. Find P(sum is 8 | at least one die shows 5).", "2/11", ["Outcomes with a 5: 11.", "Sum 8 among them: (3, 5), (5, 3)."])
assert sum(1 for a in range(1, 7) for b in range(1, 7) if 5 in (a, b) and a + b == 8) == 2 and sum(1 for a in range(1, 7) for b in range(1, 7) if 5 in (a, b)) == 11
B.sa(S, "cp1", "Draw two cards without replacement. Find P(second is a king | first is a king).", "1/17", ["3 kings left of 51."])
B.mc(S, "cp1", "A student says P(A | B) = P(B | A) always. Which example shows the error?", "P(king | face card) = 1/3 but P(face card | king) = 1", ["P(heads | heads) = 1", "P(6 | even) = 1/3", "No example exists"], ["Conditioning on different events changes the sample space."], tags=["misconception", "error-analysis"])
B.mc(S, "cp1", "P(A) = 0.5, P(B) = 0.4, P(A | B) = 0.5. Which is true?", "A and B are independent", ["A and B are mutually exclusive", "P(A and B) = 0.9", "P(B | A) = 0.5"], ["P(A | B) = P(A) → independent.", "P(A and B) = 0.2; P(B | A) = 0.4."])
sel_auto(B, S, "cp1", "In a group, P(cat) = 0.4, P(dog) = 0.5, P(cat and dog) = 0.15. Select ALL true statements.", ["P(cat or dog) = 0.75", "P(dog | cat) = 0.375", "P(cat | dog) = 0.3", "P(neither) = 0.25", "P(cat or dog) = 0.9", "The events are independent"],
         lambda s_: s_ in ("P(cat or dog) = 0.75", "P(dog | cat) = 0.375", "P(cat | dog) = 0.3", "P(neither) = 0.25"), ["Addition rule: 0.4 + 0.5 - 0.15.", "0.15/0.4 and 0.15/0.5.", "0.4·0.5 = 0.2 ≠ 0.15."])
B.orq(S, "cp1", "Survey of 200: 120 like math; 80 like science; 50 like both.", [("Find P(likes math or science).", "3/4"), ("Find P(science | math).", "5/12"), ("Find P(math | science).", "5/8"), ("Find P(neither).", "1/4")],
      ["(120 + 80 - 50)/200.", "50/120.", "50/80.", "1 - 3/4."], tags=["multiple-representations"])
B.orq(S, "honors", "Use a tree: 60% of a store's customers use a card; 30% of card users and 10% of others buy over $50.", [("P(card and over $50).", "0.18"), ("P(over $50).", "0.22"), ("P(card | over $50) (nearest hundredth).", "0.82"), ("Are card use and spending over $50 independent?", "No")],
      ["0.6·0.3.", "0.18 + 0.4·0.1.", "0.18/0.22.", "0.3 ≠ 0.22."], tags=["modeling"])
B.sa(S, "cp2", "P(A and B) = 0.12 and P(A) = 0.3. Find P(B | A).", "0.4", ["0.12/0.3."])

# ---------------- Skill 5: probability distributions ----------------
S = 5
for vals, probs, ask in [([0, 1, 2, 3], ["0.1", "0.3", "k", "0.2"], "k"), ([1, 2, 3, 4, 5], ["0.05", "0.15", "0.4", "k", "0.1"], "k"), ([-1, 0, 2], ["1/4", "k", "1/3"], "k")]:
    known = sum(F(p) for p in probs if p != "k"); k = 1 - known
    B.sa(S, "cp2", f"A distribution has X = {', '.join(map(str, vals))} with P = {', '.join(probs)}. Find k.", fr(k) if "/" in "".join(probs) else f"{float(k):g}", ["Probabilities sum to 1.", f"k = 1 - {fr(known) if '/' in ''.join(probs) else f'{float(known):g}'}."])
for n_, p, k in [(5, F(1, 2), 3), (6, F(1, 6), 1), (10, F(1, 4), 2), (8, F(3, 5), 6), (4, F(1, 3), 0)]:
    v = C(n_, k) * p ** k * (1 - p) ** (n_ - k)
    B.sa(S, "cp1" if n_ <= 6 else "honors", f"X is binomial with n = {n_} and p = {fr(p)}. Find P(X = {k}) (exact, then to 4 decimals).", f"{fr(v)} ≈ {float(v):.4f}", ["P(X = k) = C(n, k)pᵏ(1 - p)ⁿ⁻ᵏ.", f"C({n_}, {k})({fr(p)})^{k}({fr(1 - p)})^{n_ - k}."])
for n_, p in [(3, F(1, 2)), (4, F(1, 4))]:
    dist = ", ".join(f"P({k}) = {fr(C(n_, k) * p ** k * (1 - p) ** (n_ - k))}" for k in range(n_ + 1))
    B.sa(S, "cp1", f"Write the probability distribution of X = number of successes in {n_} trials with p = {fr(p)}.", dist, ["Binomial: C(n, k)pᵏ(1 - p)ⁿ⁻ᵏ for each k."])
B.mc(S, "cp1", "Which could be a probability distribution?", "P(0) = 0.2, P(1) = 0.5, P(2) = 0.3", ["P(0) = 0.5, P(1) = 0.6, P(2) = -0.1", "P(0) = 0.3, P(1) = 0.3, P(2) = 0.3", "P(0) = 0.4, P(1) = 0.4, P(2) = 0.4"], ["Each probability is between 0 and 1, and they sum to 1."])
B.mc(S, "cp1", "Which situation is binomial?", "Number of heads in 10 coin flips", ["Number of flips until the first head", "Height of 10 students", "Number of cards drawn until an ace (no replacement)"], ["Fixed n, two outcomes, independent trials, constant p."], tags=["reasoning"])
sel_auto(B, S, "cp1", "X = number of sixes in 3 rolls of a die. Select ALL true statements.", ["X is binomial with n = 3, p = 1/6", "P(X = 0) = 125/216", "P(X = 3) = 1/216", "P(X ≥ 1) = 91/216", "P(X = 1) = 1/6", "X can equal 4"],
         lambda s_: s_ in ("X is binomial with n = 3, p = 1/6", "P(X = 0) = 125/216", "P(X = 3) = 1/216", "P(X ≥ 1) = 91/216"), ["(5/6)³ = 125/216.", "P(X = 1) = 3(1/6)(5/6)² = 75/216."])
assert 3 * F(1, 6) * F(5, 6) ** 2 == F(75, 216)
B.orq(S, "cp1", "A quiz has 5 multiple-choice questions with 4 choices each. A student guesses on all.", [("What are n and p?", "n = 5, p = 1/4"), ("P(all wrong).", f"{fr(F(3, 4) ** 5)}"), ("P(exactly 2 right).", f"{fr(C(5, 2) * F(1, 4) ** 2 * F(3, 4) ** 3)}"), ("P(at least 1 right).", f"{fr(1 - F(3, 4) ** 5)}")],
      ["Binomial.", "(3/4)⁵.", "C(5, 2)(1/4)²(3/4)³.", "Complement."], tags=["modeling"])
B.orq(S, "honors", "X: P(X = 1) = 0.2, P(X = 2) = 0.5, P(X = 3) = 0.3.", [("Find P(X ≥ 2).", "0.8"), ("Find the mean.", "2.1"), ("Find E(X²).", "4.9"), ("Find the variance.", "0.49")], ["0.5 + 0.3.", "Σ x·P.", "Σ x²·P.", "E(X²) - μ²."], tags=["challenge"])
assert abs(0.2 + 1.0 + 0.9 - 2.1) < 1e-12 and abs(0.2 + 2.0 + 2.7 - 4.9) < 1e-12 and abs(4.9 - 2.1 ** 2 - 0.49) < 1e-12
B.sa(S, "cp2", "For a fair coin flipped 4 times, what is P(exactly 2 heads)?", "3/8", ["C(4, 2)/16 = 6/16."])

# ---------------- Skill 6: expected value ----------------
S = 6
for vals, probs in [([0, 1, 2, 3], [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]), ([10, 20, 50], [F(1, 2), F(3, 10), F(1, 5)]), ([-5, 0, 15], [F(1, 2), F(1, 4), F(1, 4)]), ([1, 2, 3, 4, 5, 6], [F(1, 6)] * 6)]:
    E = sum(v * p for v, p in zip(vals, probs))
    B.sa(S, "cp2" if len(vals) == 6 else "cp1", f"Find E(X): X = {', '.join(map(str, vals))} with P = {', '.join(fr(p) for p in probs)}.", fr(E), ["E(X) = Σ x·P(x).", f"= {fr(E)}."])
for cost, prizes in [(2, [(100, F(1, 200)), (10, F(1, 20))]), (5, [(500, F(1, 1000)), (20, F(1, 50))]), (1, [(50, F(1, 100))])]:
    E = sum(v * p for v, p in prizes) - cost
    B.sa(S, "cp1", f"A raffle ticket costs ${cost}. Prizes: " + ", ".join(f"${v} with probability {fr(p)}" for v, p in prizes) + ". Find the expected net gain.", f"-${fr(-E)}" if E < 0 else f"${fr(E)}", ["Expected winnings Σ prize·P.", "Subtract the cost."], tags=["modeling"])
B.mc(S, "cp1", "A game: roll a die; win $6 on a 6, lose $1 otherwise. Is it fair?", "No: E = 6(1/6) - 1(5/6) = 1/6 > 0, favoring the player", ["Yes: E = 0", "No: E < 0", "Yes: you win on 1 of 6 outcomes"], ["Fair means E = 0."])
B.mc(S, "cp1", "A student computes E(X) by averaging the values 0, 10, 100 to get 36.7 though P(100) is tiny. What is wrong?", "Values must be weighted by their probabilities", ["Nothing", "Should use the median", "Should add the values"], ["E(X) = Σ x·P(x)."], tags=["misconception"])
B.sa(S, "cp1", "An insurance company charges $300 per year. It pays $50,000 with probability 0.004. Find its expected profit per policy.", "$100", ["300 - 50000(0.004) = 100."], tags=["modeling"])
B.sa(S, "cp1", "Find the expected number of heads in 20 flips of a fair coin.", "10", ["Binomial mean np."])
B.sa(S, "honors", "A basketball player makes 75% of free throws. In a 1-and-1 (second shot only if the first is made), find the expected points.", "1.3125", ["P(0) = 0.25, P(1) = 0.75·0.25, P(2) = 0.75².", "E = 0.1875 + 2(0.5625) = 1.3125."], tags=["challenge"])
assert abs(0.75 * 0.25 + 2 * 0.5625 - 1.3125) < 1e-12
B.sa(S, "honors", "Find the price x that makes this game fair: pay x, roll two dice, win $10 if the sum is 7.", "$5/3 ≈ $1.67", ["P(7) = 1/6.", "Fair: 10(1/6) - x = 0."], tags=["reasoning"])
sel_auto(B, S, "cp1", "X has E(X) = 4. Select ALL true statements.", ["E(2X) = 8", "E(X + 3) = 7", "E(X - 4) = 0", "E(X²) = 16 always", "X must equal 4 sometimes", "E(3X - 1) = 11"],
         lambda s_: s_ in ("E(2X) = 8", "E(X + 3) = 7", "E(X - 4) = 0", "E(3X - 1) = 11"), ["E(aX + b) = aE(X) + b.", "E(X²) depends on the spread; X need not take the value 4."], tags=["reasoning"])
B.orq(S, "cp1", "A carnival game costs $3. Spin a wheel: P($10) = 0.1, P($5) = 0.2, P($0) = 0.7.", [("Expected winnings.", "$2"), ("Expected net gain.", "-$1"), ("Expected net over 50 plays.", "-$50"), ("What prize for the $10 slot makes the game fair?", "$20")],
      ["10(0.1) + 5(0.2).", "2 - 3.", "50·(-1).", "0.1x + 1 = 3."], tags=["modeling"])
B.orq(S, "honors", "A company can launch product A (60%: +$80k, 40%: -$30k) or B (90%: +$40k, 10%: -$10k).", [("E(A).", "$36,000"), ("E(B).", "$35,000"), ("Which has higher expected value?", "A"), ("Why might the company still choose B?", "Lower risk: B rarely loses money")],
      ["48 - 12.", "36 - 1.", "Compare.", "Variability matters."], tags=["modeling", "reasoning"])
B.sa(S, "cp2", "Find E(X) for a fair coin with X = 1 for heads, 0 for tails.", "1/2", ["1(1/2) + 0(1/2)."])

# ---------------- Skill 7: normal distribution and z-scores ----------------
S = 7
for x, mu, sd in [(85, 70, 10), (52, 60, 4), (180, 150, 20), (3.2, 3.0, 0.4), (61, 70, 6)]:
    z = (x - mu) / sd
    B.sa(S, "cp2", f"Find the z-score of x = {x:g} when μ = {mu:g} and σ = {sd:g}.", f"{z:g}", ["z = (x - μ)/σ.", f"({x:g} - {mu:g})/{sd:g} = {z:g}."])
for lo, hi, ans in [(-1, 1, "68%"), (-2, 2, "95%"), (-3, 3, "99.7%"), (0, 1, "34%"), (1, 2, "13.5%"), (-2, 0, "47.5%"), (2, 99, "2.5%")]:
    rng = f"between μ - {abs(lo)}σ and μ + {hi}σ" if lo < 0 and hi < 99 else (f"between μ and μ + {hi}σ" if lo == 0 else f"between μ + {lo}σ and μ + {hi}σ" if hi < 99 else f"above μ + {lo}σ")
    if lo < 0 and hi == 0: rng = f"between μ - {abs(lo)}σ and μ"
    B.mc(S, "cp2" if hi in (1, 2, 3) and lo == -hi else "cp1", f"Use the empirical rule: what percent of a normal distribution lies {rng}?", ans, [a for a in ["68%", "95%", "99.7%", "34%", "13.5%", "47.5%", "2.5%", "16%"] if a != ans][:3], ["Empirical rule: 68–95–99.7.", "Split symmetrically about the mean."])
for mu, sd, a_, b_ in [(100, 15, 85, 115), (500, 100, 650, None), (64, 3, None, 58), (20, 2, 17, 25)]:
    if a_ is not None and b_ is not None: pr = Phi((b_ - mu) / sd) - Phi((a_ - mu) / sd); q = f"P({a_} < X < {b_})"
    elif a_ is not None: pr = 1 - Phi((a_ - mu) / sd); q = f"P(X > {a_})"
    else: pr = Phi((b_ - mu) / sd); q = f"P(X < {b_})"
    B.sa(S, "cp1", f"X is normal with μ = {mu} and σ = {sd}. Use technology to find {q} (4 decimals).", f"{pr:.4f}", ["Convert to z-scores.", "Use normalcdf or a z-table."])
B.mc(S, "cp1", "Test A: score 82 (μ = 75, σ = 5). Test B: score 88 (μ = 80, σ = 8). On which test did the student do relatively better?", "Test A (z = 1.4 vs z = 1.0)", ["Test B (higher score)", "Equally well", "Cannot compare"], ["Compare z-scores."], tags=["reasoning"])
B.mc(S, "cp1", "Which is NOT a property of every normal distribution?", "It is skewed right", ["It is symmetric about the mean", "Mean = median", "About 95% lies within 2σ of the mean"], ["Normal curves are bell-shaped and symmetric."])
sel_auto(B, S, "cp1", "Heights are normal with μ = 66 in and σ = 3 in. Select ALL true statements.", ["About 68% are between 63 and 69 in", "About 2.5% are taller than 72 in", "A height of 60 in has z = -2", "About 50% are shorter than 66 in", "About 95% are between 60 and 69 in", "A height of 69 in has z = 3"],
         lambda s_: s_ in ("About 68% are between 63 and 69 in", "About 2.5% are taller than 72 in", "A height of 60 in has z = -2", "About 50% are shorter than 66 in"), ["μ ± σ = 63–69; μ + 2σ = 72.", "z = (60 - 66)/3 = -2."])
B.sa(S, "honors", "SAT math: μ = 520, σ = 115. What score marks the 90th percentile (nearest whole)?", f"{round(520 + 1.2816 * 115)}", ["z ≈ 1.2816 for the 90th percentile.", "x = μ + zσ."], tags=["challenge"])
B.orq(S, "cp1", "Battery life is normal with μ = 40 h, σ = 5 h.", [("What percent last 35–45 h?", "68%"), ("What percent last more than 50 h?", "2.5%"), ("Find the z-score of 32 h.", "-1.6"), ("Use technology: P(X < 32) (4 decimals).", f"{Phi(-1.6):.4f}")], ["±1σ.", "Above +2σ.", "(32 - 40)/5.", "normalcdf."], tags=["modeling"])
B.orq(S, "honors", "A machine fills bags: μ = 16.2 oz, σ = 0.15 oz. Bags under 16 oz are rejected.", [("z-score of 16 oz (nearest hundredth).", "-1.33"), ("Percent rejected (nearest tenth).", f"{Phi(-0.2 / 0.15) * 100:.1f}%"), ("To reject only 1%, what mean is needed (σ fixed; nearest hundredth)?", f"{16 + 2.3263 * 0.15:.2f} oz"), ("Name one other way to reduce rejections.", "Reduce σ (more consistent filling)")],
      ["(16 - 16.2)/0.15.", "Φ(z).", "16 = μ - 2.326(0.15).", "Less variability."], tags=["modeling", "challenge"])
B.sa(S, "cp2", "What is the z-score of a value equal to the mean?", "0", ["(μ - μ)/σ."])

# ---------------- Skill 8: sampling, inference, models ----------------
S = 8
for desc, ans in [("Every 10th customer entering a store is surveyed.", "systematic"), ("Names are drawn from a hat containing every student's name.", "simple random"), ("Each grade level is sampled randomly in proportion to its size.", "stratified"),
                  ("Three homerooms are randomly chosen and every student in them is surveyed.", "cluster"), ("A radio host asks listeners to call in.", "voluntary response (biased)"), ("A reporter interviews people walking by the library.", "convenience (biased)")]:
    B.mc(S, "cp2", f"Name the sampling method: {desc}", ans.capitalize(), [a.capitalize() for a in ["systematic", "simple random", "stratified", "cluster", "voluntary response (biased)", "convenience (biased)"] if a != ans][:3], ["Match the description to the method."])
for desc, ans in [("Researchers randomly assign patients to a new drug or a placebo.", "experiment"), ("A survey asks 500 adults about their exercise habits.", "sample survey"), ("Researchers record whether past smokers developed heart disease.", "observational study")]:
    B.mc(S, "cp1", f"Identify the study type: {desc}", ans.capitalize(), [a.capitalize() for a in ["experiment", "sample survey", "observational study", "census"] if a != ans], ["Experiments impose treatments; observational studies do not."])
for p, n_ in [(0.52, 400), (0.35, 1000), (0.6, 150), (0.25, 2500)]:
    moe = 2 * math.sqrt(p * (1 - p) / n_)
    B.sa(S, "cp1", f"A survey of {n_:,} finds p̂ = {p}. Find the approximate 95% margin of error (2·√(p̂(1 - p̂)/n)) and the interval.", f"±{moe:.3f}; ({p - moe:.3f}, {p + moe:.3f})", ["MOE ≈ 2√(p̂(1 - p̂)/n).", "Interval p̂ ± MOE."])
B.mc(S, "cp1", "To cut the margin of error in half, the sample size must be…", "multiplied by 4", ["doubled", "halved", "multiplied by 8"], ["MOE ∝ 1/√n."], tags=["reasoning"])
B.mc(S, "cp1", "Why can an experiment (but not an observational study) show cause and effect?", "Random assignment balances other variables between groups", ["It uses larger samples", "It always uses a placebo", "It surveys more people"], ["Randomization controls for confounding variables."], tags=["reasoning"])
B.mc(S, "honors", "In 200 simulated samples, a sample mean difference of 4.5 or more occurred 3 times. What does this suggest about an observed difference of 4.5?", "It is unlikely by chance alone (≈1.5%), so it is statistically significant", ["It is common, so not significant", "The treatment had no effect", "The simulation is invalid"], ["3/200 = 1.5% < 5%."], tags=["reasoning", "challenge"])
sel_auto(B, S, "cp1", "Select ALL sources of bias.", ["Asking 'Don't you agree the park needs repairs?'", "Surveying only people with landlines", "Letting volunteers decide whether to respond", "Randomly selecting from a full list", "Using a large random sample", "Random assignment to treatments"],
         lambda s_: s_ in ("Asking 'Don't you agree the park needs repairs?'", "Surveying only people with landlines", "Letting volunteers decide whether to respond"), ["Leading questions, undercoverage, and voluntary response bias results."])
sel_auto(B, S, "honors", "A 95% confidence interval for a proportion is (0.42, 0.50). Select ALL correct interpretations or facts.", ["p̂ = 0.46", "The margin of error is 0.04", "We are 95% confident the true proportion is between 0.42 and 0.50", "There is a 95% chance p̂ is in the interval", "95% of people are between 0.42 and 0.50", "The true proportion is definitely 0.46"],
         lambda s_: s_ in ("p̂ = 0.46", "The margin of error is 0.04", "We are 95% confident the true proportion is between 0.42 and 0.50"), ["Center = p̂; half-width = MOE.", "Confidence is about the method capturing the true parameter."], tags=["misconception"])
B.orq(S, "cp1", "A school wants to know what percent of its 1,200 students support a later start time.", [("Describe a simple random sample of 100.", "Number all students; randomly choose 100 numbers"), ("If 64 of 100 support it, find p̂.", "0.64"), ("Find the 95% margin of error (nearest hundredth).", f"±{2 * math.sqrt(.64 * .36 / 100):.2f}"), ("State the interval.", f"({.64 - 2 * math.sqrt(.64 * .36 / 100):.2f}, {.64 + 2 * math.sqrt(.64 * .36 / 100):.2f})")],
      ["Random selection from a full list.", "64/100.", "2√(0.64·0.36/100).", "p̂ ± MOE."], tags=["modeling"])
B.orq(S, "honors", "Design an experiment to test whether a new fertilizer increases tomato yield using 40 plants.", [("Identify the treatments.", "New fertilizer vs. standard (control)"), ("How should plants be assigned?", "Randomly, 20 to each group"), ("Name the response variable.", "Tomato yield per plant"), ("Why replicate with many plants?", "To reduce the effect of natural variation")],
      ["Two groups.", "Random assignment.", "What is measured.", "Replication."], tags=["reasoning"])
B.sa(S, "cp2", "What is a parameter?", "A numerical summary of a population", ["Statistics describe samples; parameters describe populations."])

# ================= additions: format balance =================
for ctx, val, wr in [("How many ways can 5 different books be arranged on a shelf?", fact(5), [5 * 5, 5 ** 5, 15]), ("How many ways can a coach choose a batting order for 9 players?", fact(9), [9 * 9, C(9, 9), 9 ** 9]),
                     ("How many 4-character passwords use digits 0–9 without repetition?", Pm(10, 4), [10 ** 4, C(10, 4), 40]), ("How many ways can 3 of 8 runners finish 1st, 2nd, 3rd?", Pm(8, 3), [C(8, 3), 8 ** 3, 24])]:
    B.mc(1, "cp1", ctx, f"{val:,}", [f"{w:,}" for w in wr], ["Order matters; use the counting principle or ₙPᵣ."], tags=["misconception"])
for ctx, num_, den_ in [("5 cards are dealt. Find P(all 5 are spades).", C(13, 5), C(52, 5)), ("A committee of 3 is chosen at random from 6 girls and 4 boys. Find P(all girls).", C(6, 3), C(10, 3)),
                        ("Choose 2 bulbs from 10, of which 3 are defective. Find P(both defective).", C(3, 2), C(10, 2)), ("A 4-person team is chosen from 12 people including Ana and Ben. Find P(both are chosen).", C(10, 2), C(12, 4)),
                        ("Choose 3 numbers from 1–10. Find P(all are even).", C(5, 3), C(10, 3))]:
    pv = F(num_, den_)
    B.mc(2, "cp1" if den_ < 10 ** 4 else "honors", ctx, fr(pv), [fr(F(num_ + 1, den_)) if num_ + 1 < den_ else "1/2", fr(F(num_, den_ * 2)), fr(pv * 2) if pv * 2 < 1 else "1/3"], ["P = (favorable combinations)/(total combinations).", f"{num_:,}/{den_:,}."])
B.sel(2, "cp1", "Select ALL expressions equal to the number of 2-person handshakes among 10 people.", ["C(10, 2)", "45", "10·9/2"], ["10·9", "₁₀P₂", "20"], ["Each handshake is an unordered pair."])
B.orq(2, "honors", "A lottery picks 6 numbers from 1–49 (order irrelevant).", [("Number of possible tickets.", f"{C(49, 6):,}"), ("P(winning with one ticket).", f"1/{C(49, 6):,}"), ("Number of tickets matching exactly 5.", f"{C(6, 5) * C(43, 1)}"), ("P(matching exactly 5).", fr(F(C(6, 5) * C(43, 1), C(49, 6))))],
      ["C(49, 6).", "Reciprocal.", "C(6, 5)·C(43, 1).", "Divide."], tags=["challenge"])
for r_, b_ in [(6, 4), (3, 9), (5, 5), (2, 6)]:
    t = r_ + b_; wo = F(r_, t) * F(r_ - 1, t - 1); wi = F(r_, t) ** 2
    B.mc(3, "cp1", f"A jar has {r_} red and {b_} blue chips. Two are drawn without replacement. Find P(both red).", fr(wo), [fr(wi), fr(F(r_, t) * F(r_ - 1, t)), fr(F(r_, t))], ["Dependent: (r/t)·((r - 1)/(t - 1)).", "With replacement would give (r/t)²."], tags=["misconception"])
for pa, pb, pab in [("0.5", "0.4", "0.2"), ("0.25", "0.6", "0.15"), ("0.3", "0.3", "0.12")]:
    ind = abs(float(pa) * float(pb) - float(pab)) < 1e-12
    st = {f"P(A or B) = {float(pa) + float(pb) - float(pab):g}": True, "A and B are independent": ind, "A and B are dependent": not ind, f"P(A | B) = {float(pab) / float(pb):g}": True, f"P(A or B) = {float(pa) + float(pb):g}": False}
    B.sel(3, "cp1", f"P(A) = {pa}, P(B) = {pb}, P(A and B) = {pab}. Select ALL true statements.", [k for k, t_ in st.items() if t_], [k for k, t_ in st.items() if not t_], ["Addition rule; compare P(A)P(B) with P(A and B).", "P(A | B) = P(A and B)/P(B)."])
for n_ in (2, 3):
    tot_ = 6 ** n_
    B.orq(3, "cp1", f"Roll {n_} fair dice.", [("P(all show 1).", f"1/{tot_}"), ("P(all even).", fr(F(1, 2) ** n_)), ("P(no 6).", fr(F(5, 6) ** n_)), ("P(at least one 6).", fr(1 - F(5, 6) ** n_))], ["Multiply independent probabilities.", "(1/2)ⁿ.", "(5/6)ⁿ.", "Complement."])
B.sa(3, "cp1", "A family has 3 children. Find P(at least one girl), assuming P(girl) = 1/2.", "7/8", ["1 - (1/2)³."])
B.sa(3, "honors", "How many times must a fair coin be flipped so that P(at least one head) > 0.99?", "7", ["1 - (1/2)ⁿ > 0.99 → (1/2)ⁿ < 0.01.", "2⁷ = 128 > 100."], tags=["challenge"])
assert 0.5 ** 6 > 0.01 > 0.5 ** 7
tables = [(("Owns pet", "No pet"), ("Grade 9", "Grade 10"), (24, 16, 18, 22)), (("Prefers online", "Prefers in-store"), ("Under 30", "30+"), (45, 15, 20, 40)), (("Passed", "Failed"), ("Studied", "Did not study"), (54, 6, 21, 19))]
for (c1, c2), (r1, r2), (a, b, c, d) in tables:
    n_ = a + b + c + d
    B.orq(4, "cp1", f"Two-way table — {r1}: {c1} {a}, {c2} {b}; {r2}: {c1} {c}, {c2} {d}.", [(f"P({c1}).", fr(F(a + c, n_))), (f"P({c1} | {r1}).", fr(F(a, a + b))), (f"P({r1} | {c1}).", fr(F(a, a + c))), (f"Are '{r1}' and '{c1}' independent?", "Yes" if F(a, a + b) == F(a + c, n_) else "No")],
          ["Column total / grand total.", "Restrict to the row.", "Restrict to the column.", "Compare P(col | row) with P(col)."], tags=["multiple-representations"])
    good = fr(F(c, c + d))
    B.mc(4, "cp1", f"Using the same table ({r1}: {a}, {b}; {r2}: {c}, {d}), find P({c1} | {r2}).", good, [fr(F(c, n_)), fr(F(c, a + c)), fr(F(c + d, n_))], ["Condition on the row: divide by the row total."], tags=["misconception"])
    sel_auto(B, 4, "cp1", f"Same table ({r1}: {c1} {a}, {c2} {b}; {r2}: {c1} {c}, {c2} {d}). Select ALL true statements.",
             [f"P({r1}) = {fr(F(a + b, n_))}", f"P({c2} | {r2}) = {fr(F(d, c + d))}", f"P({r1} and {c2}) = {fr(F(b, n_))}", f"P({r1} | {c2}) = {fr(F(b, a + b))}", f"P({r2}) = {fr(F(a + b, n_))}" if a + b != c + d else f"P({r2}) = {fr(F(a, n_))}"],
             lambda s_, a=a, b=b, c=c, d=d, n_=n_, r1=r1, r2=r2, c1=c1, c2=c2: s_ in (f"P({r1}) = {fr(F(a + b, n_))}", f"P({c2} | {r2}) = {fr(F(d, c + d))}", f"P({r1} and {c2}) = {fr(F(b, n_))}") or (s_ == f"P({r1} | {c2}) = {fr(F(b, a + b))}" and F(b, a + b) == F(b, b + d)),
             ["Joint: cell/total; conditional: cell/(given row or column total)."], tags=["misconception"])
B.sa(4, "cp1", "P(rain) = 0.3; P(traffic | rain) = 0.8; P(traffic | no rain) = 0.4. Find P(traffic).", "0.52", ["0.3(0.8) + 0.7(0.4)."], tags=["modeling"])
B.sa(4, "honors", "Using the previous data, find P(rain | traffic) (nearest hundredth).", "0.46", ["0.24/0.52 ≈ 0.4615."], tags=["modeling"])
for n_, p, k in [(6, F(1, 2), 3), (5, F(1, 5), 2), (8, F(1, 2), 8), (4, F(2, 3), 3), (6, F(1, 3), 0)]:
    v = C(n_, k) * p ** k * (1 - p) ** (n_ - k)
    B.mc(5, "cp1", f"X ~ Binomial(n = {n_}, p = {fr(p)}). Find P(X = {k}).", fr(v), [fr(p ** k * (1 - p) ** (n_ - k)) if C(n_, k) > 1 else fr(v * 2 if v * 2 < 1 else v / 2), fr(C(n_, k) * p ** k) if C(n_, k) * p ** k < 1 else fr(p ** k), fr(F(k, n_))], ["C(n, k)pᵏ(1 - p)ⁿ⁻ᵏ.", "Forgetting C(n, k) or (1 - p)ⁿ⁻ᵏ is a common error."], tags=["misconception"])
for n_, p in [(4, F(1, 2)), (3, F(1, 3))]:
    probs = {k: C(n_, k) * p ** k * (1 - p) ** (n_ - k) for k in range(n_ + 1)}
    st = {f"P(X = 0) = {fr(probs[0])}": True, f"P(X ≥ 1) = {fr(1 - probs[0])}": True, f"The mean is {fr(n_ * p)}": True, f"P(X = {n_}) = {fr(probs[n_])}": True, f"P(X = 1) = {fr(p)}": probs[1] == p, f"The mean is {fr(p)}": False}
    B.sel(5, "cp1", f"X ~ Binomial(n = {n_}, p = {fr(p)}). Select ALL true statements.", [k_ for k_, t_ in st.items() if t_], [k_ for k_, t_ in st.items() if not t_], ["Binomial formula; mean np."])
for n_, p in [(3, F(1, 2)), (4, F(1, 5)), (5, F(1, 3))]:
    probs = [C(n_, k) * p ** k * (1 - p) ** (n_ - k) for k in range(n_ + 1)]
    B.orq(5, "cp1" if n_ < 5 else "honors", f"X ~ Binomial(n = {n_}, p = {fr(p)}).", [("Find P(X = 0).", fr(probs[0])), ("Find P(X = 1).", fr(probs[1])), ("Find P(X ≥ 2).", fr(1 - probs[0] - probs[1])), ("Find the mean np.", fr(n_ * p))], ["(1 - p)ⁿ.", "n·p(1 - p)ⁿ⁻¹.", "Complement.", "np."])
for n_, p, k in [(5, F(1, 2), 4), (6, F(1, 6), 2), (10, F(1, 2), 8), (4, F(1, 4), 2)]:
    v = sum(C(n_, j) * p ** j * (1 - p) ** (n_ - j) for j in range(k, n_ + 1))
    B.sa(5, "cp1" if n_ <= 6 else "honors", f"X ~ Binomial(n = {n_}, p = {fr(p)}). Find P(X ≥ {k}).", f"{fr(v)} ≈ {float(v):.4f}", [f"Add P(X = {k}) through P(X = {n_}).", "Or use the complement."])
for vals, probs in [([0, 1, 2], [F(1, 4), F(1, 2), F(1, 4)]), ([1, 3, 5], [F(1, 5), F(2, 5), F(2, 5)]), ([-2, 0, 4], [F(1, 2), F(1, 3), F(1, 6)]), ([2, 4, 6, 8], [F(1, 10), F(2, 10), F(3, 10), F(4, 10)]), ([100, 0], [F(1, 20), F(19, 20)])]:
    E = sum(v * p for v, p in zip(vals, probs)); avg = F(sum(vals), len(vals))
    B.mc(6, "cp1", f"X = {', '.join(map(str, vals))} with P = {', '.join(fr(p) for p in probs)}. Find E(X).", fr(E), [fr(avg) if avg != E else fr(E + 1), fr(sum(probs)), fr(max(vals) * max(probs)), fr(sum(vals)), fr(E / 2)], ["Weight each value by its probability."], tags=["misconception"])
for cost, win, p in [(1, 5, F(1, 6)), (2, 30, F(1, 20)), (5, 12, F(1, 3))]:
    E = win * p - cost
    B.orq(6, "cp1", f"A game costs ${cost}. You win ${win} with probability {fr(p)}.", [("Expected winnings.", f"${fr(win * p)}"), ("Expected net gain.", f"{'-' if E < 0 else ''}${fr(abs(E))}"), ("Is the game fair?", "Yes" if E == 0 else "No"), ("Prize that makes it fair.", f"${fr(cost / p)}")], ["prize·p.", "Subtract cost.", "Fair ⇔ E = 0.", "prize·p = cost."], tags=["modeling"])
B.sel(6, "cp1", "Select ALL games with negative expected net gain for the player.", ["Pay $2; win $10 with probability 1/10", "Pay $1; win $3 with probability 1/4", "Pay $5; win $20 with probability 1/5"], ["Pay $1; win $6 with probability 1/5", "Pay $3; win $9 with probability 1/3", "Pay $2; win $12 with probability 1/4"],
      ["E = prize·p - cost: -1, -0.25, -1; +0.2, 0, +1."], tags=["modeling"])
B.sel(6, "honors", "Select ALL true statements about expected value.", ["It is a long-run average", "It need not be a possible outcome", "E(X + Y) = E(X) + E(Y)"], ["It is the most likely outcome", "It is always a whole number", "It equals the median"], ["Expected value is a weighted mean."], tags=["reasoning"])
B.sa(6, "cp1", "A multiple-choice test gives +4 for correct and -1 for incorrect, 5 choices each. What is the expected score from a random guess?", "0", ["4(1/5) - 1(4/5) = 0."], tags=["modeling"])
B.sa(6, "cp1", "Find the expected number of 6s in 30 rolls of a die.", "5", ["np = 30/6."])
B.sa(6, "honors", "Each box of cereal contains 1 of 4 equally likely prizes. Find the expected number of boxes to collect all 4.", "25/3 ≈ 8.33", ["Expected waits: 1 + 4/3 + 4/2 + 4/1.", "= 1 + 1.333 + 2 + 4."], tags=["challenge"])
assert 1 + F(4, 3) + 2 + 4 == F(25, 3)
for mu, sd, pctl, z in [(70, 8, "84th", 1), (50, 5, "16th", -1), (200, 25, "97.5th", 2), (12, 1.5, "2.5th", -2)]:
    val = mu + z * sd
    B.mc(7, "cp1", f"X is normal with μ = {mu:g}, σ = {sd:g}. Using the empirical rule, about what value is the {pctl} percentile?", f"{val:g}", [f"{mu - z * sd:g}", f"{mu + z * sd / 2:g}", f"{mu:g}"], [f"{pctl} percentile ≈ z = {z}.", "x = μ + zσ."])
B.sel(7, "cp1", "Select ALL values that are more than 2 standard deviations from the mean of N(μ = 100, σ = 10).", ["75", "121", "130"], ["85", "110", "119"], ["Outside 80–120."])
B.sa(7, "cp1", "A z-score is 1.5 with μ = 40 and σ = 6. Find x.", "49", ["x = μ + zσ = 40 + 9."])
B.sa(7, "honors", "Weights are N(μ, σ). 2.5% weigh less than 140 lb and 2.5% weigh more than 200 lb. Find μ and σ.", "μ = 170, σ = 15", ["Symmetric: μ = 170.", "200 = μ + 2σ → σ = 15."], tags=["reasoning"])
for desc, ans in [("Only customers who had a problem respond to the email survey.", "Voluntary response bias"), ("A phone poll misses people without phones.", "Undercoverage"), ("'Most experts agree X is dangerous. Do you agree?'", "Response bias (leading question)"), ("Many selected people never answer the survey.", "Nonresponse bias")]:
    B.mc(8, "cp1", f"Identify the bias: {desc}", ans, [a for a in ["Voluntary response bias", "Undercoverage", "Response bias (leading question)", "Nonresponse bias"] if a != ans], ["Match the flaw to the type of bias."])
B.sel(8, "cp1", "Select ALL features of a well-designed experiment.", ["Random assignment", "A control group", "Replication"], ["Letting subjects choose their group", "Only one subject per treatment", "Telling subjects the hypothesis"], ["Control, randomization, replication."])
B.sel(8, "honors", "A simulation of 1,000 samples (n = 50) from a population with p = 0.40 gives p̂ values with mean 0.40 and SD 0.07. Select ALL valid conclusions.", ["A sample p̂ of 0.55 would be unusual", "About 95% of p̂ values lie within 0.26–0.54", "The SD of p̂ is about √(0.4·0.6/50)"], ["A p̂ of 0.45 proves p ≠ 0.40", "Every sample has p̂ = 0.40"],
      ["0.55 is more than 2 SD above 0.40.", "√(0.24/50) ≈ 0.069."], tags=["challenge"])
assert abs(math.sqrt(0.24 / 50) - 0.069) < 0.001
B.orq(8, "cp1", "A poll of 900 voters finds 54% support a measure.", [("Find the 95% margin of error (nearest tenth of a percent).", f"±{200 * math.sqrt(.54 * .46 / 900):.1f}%"), ("State the interval.", f"{54 - 200 * math.sqrt(.54 * .46 / 900):.1f}% to {54 + 200 * math.sqrt(.54 * .46 / 900):.1f}%"), ("Can the pollster conclude a majority supports it?", "Yes, the whole interval is above 50%"), ("How would a sample of 3,600 change the margin?", "It would be cut in half")],
      ["2√(p̂(1 - p̂)/n).", "p̂ ± MOE.", "Compare with 50%.", "MOE ∝ 1/√n."], tags=["modeling"])
B.sa(8, "cp1", "What is the difference between a census and a sample?", "A census measures every member of the population; a sample measures part of it", ["Definitions."])
B.sa(8, "cp2", "What is a statistic?", "A numerical summary of a sample", ["Statistics describe samples."])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
