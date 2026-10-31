from lib import Bank, graph
from mathlite import *
import math

STD = {1: ["F-IF.A.3", "F-BF.A.2"], 2: ["F-IF.A.3", "F-BF.A.2"], 3: ["F-BF.A.2", "F-IF.A.3"], 4: ["A-SSE.B.4"], 5: ["A-SSE.B.4"], 6: ["A-SSE.B.4"], 7: ["A-SSE.B.4"], 8: ["F-LE.A.2", "F-BF.A.2"]}
B = Bank("sequences-series", "ss", STD)
lst = lambda v: ", ".join(fr(t) for t in v)


def arith(a1, d, n): return [F(a1) + k * F(d) for k in range(n)]
def geom(a1, r, n): return [F(a1) * F(r) ** k for k in range(n)]
def lin_n(a1, d):  # explicit formula text a_n = d n + (a1 - d)
    return f"aₙ = {pstr(P([F(a1) - F(d), F(d)], 'n'))}"
def geo_n(a1, r):
    return f"aₙ = {fr(a1) if a1 != 1 else ''}({fr(r)})^(n - 1)".replace("= (", "= (") if a1 != 1 else f"aₙ = ({fr(r)})^(n - 1)"


# ---------------- Skill 1: arithmetic sequences ----------------
S = 1
for a1, d, n_, lvl in [(5, 3, 20, "cp2"), (-4, 6, 15, "cp2"), (40, -7, 12, "cp2"), (F(1, 2), F(3, 2), 30, "cp1"), (100, -2.5, 41, "cp1"), (-11, 4, 50, "cp1")]:
    d = F(d).limit_denominator(100); v = arith(a1, d, 4); an = F(a1) + (n_ - 1) * d
    B.sa(S, lvl, f"Find the {n_}th term of the arithmetic sequence {lst(v)}, …", fr(an), [f"d = {fr(d)}.", f"aₙ = a₁ + (n - 1)d = {fr(a1)} + {n_ - 1}({fr(d)}) = {fr(an)}."])
for a1, d in [(7, 4), (-3, -5), (12, F(1, 2)), (0, 9)]:
    B.sa(S, "cp2" if d.__class__ is int else "cp1", f"Write an explicit formula for the arithmetic sequence {lst(arith(a1, d, 4))}, …", lin_n(a1, d), [f"a₁ = {fr(a1)}, d = {fr(d)}.", f"aₙ = {fr(a1)} + (n - 1)({fr(d)}) = {lin_n(a1, d)[5:]}."])
for (m, am), (k, ak) in [((4, 19), (10, 43)), ((3, -2), (8, -27)), ((5, 12), (12, 33)), ((2, 7), (20, -2))]:
    d = F(ak - am, k - m); a1 = am - (m - 1) * d
    B.sa(S, "cp1" if d.denominator == 1 else "honors", f"In an arithmetic sequence, a{''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(m))} = {am} and a{''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(k))} = {ak}. Find a₁ and d, then write the explicit formula.",
         f"a₁ = {fr(a1)}, d = {fr(d)}; {lin_n(a1, d)}", [f"d = ({ak} - ({am}))/({k} - {m}) = {fr(d)}.", f"a₁ = {am} - {m - 1}({fr(d)}) = {fr(a1)}."])
for seq, isar in [("3, 7, 11, 15, …", True), ("2, 4, 8, 16, …", False), ("10, 6, 2, -2, …", True), ("1, 4, 9, 16, …", False), ("-5, -5, -5, …", True)]:
    B.mc(S, "cp2", f"Is {seq} an arithmetic sequence?", "Yes" + (f", d = {fr(F(seq.split(', ')[1]) - F(seq.split(', ')[0]))}" if isar else "") if isar else "No, the differences are not constant",
         ["Yes, d = 2" if not isar else "No, the differences are not constant", "Yes, d = 1" if not isar else f"Yes, d = {fr(F(seq.split(', ')[0]) - F(seq.split(', ')[1]))}" if seq[0] != "-" else "Yes, d = 1", "Cannot be determined"],
         ["Check differences between consecutive terms."])
B.sa(S, "cp1", "Which term of 4, 11, 18, … equals 186?", "n = 27", ["aₙ = 7n - 3 = 186 → n = 27."])
assert 7 * 27 - 3 == 186
B.sa(S, "honors", "Is 500 a term of 3, 10, 17, …? Explain.", "Yes, it is the 72nd term", ["aₙ = 7n - 4; 7n - 4 = 500 → n = 72, a whole number."])
assert 7 * 72 - 4 == 500
B.sa(S, "honors", "Is 250 a term of 3, 10, 17, …? Explain.", "No: 7n - 4 = 250 gives n = 254/7, not a whole number", ["Solve 7n - 4 = 250.", "n must be a positive integer."], tags=["reasoning"])
B.mc(S, "cp1", "The graph of an arithmetic sequence is…", "a set of points on a line", ["a smooth curve", "a parabola", "an exponential curve"], ["aₙ is a linear function of n with domain the positive integers."], tags=["connections"])
sel_auto(B, S, "cp1", "Select ALL arithmetic sequences.", ["2, 5, 8, 11", "9, 4, -1, -6", "1/2, 1, 3/2, 2", "3, 6, 12, 24", "1, 1, 2, 3, 5", "7, 7, 7, 7", "1, 3, 6, 10"],
         lambda s_: len({F(b) - F(a) for a, b in zip(s_.split(", "), s_.split(", ")[1:])}) == 1, ["Constant difference between consecutive terms."])
sel_auto(B, S, "honors", "aₙ = 5 - 3n. Select ALL true statements.", ["a₁ = 2", "d = -3", "a₁₀ = -25", "-40 is a term", "d = 5", "-41 is a term"],
         lambda s_: {"a₁ = 2": True, "d = -3": True, "a₁₀ = -25": 5 - 30 == -25, "-40 is a term": (5 + 40) % 3 == 0, "d = 5": False, "-41 is a term": (5 + 41) % 3 == 0}[s_], ["a₁ = 2, d = -3.", "5 - 3n = -40 → n = 15; 5 - 3n = -41 → n = 46/3."])
B.orq(S, "cp1", "A theater has 18 seats in the first row and 3 more in each row after.", [("Write an explicit formula.", "aₙ = 3n + 15"), ("How many seats in row 12?", "51"), ("Which row has 60 seats?", "row 15"), ("Is the sequence linear or exponential? Why?", "linear: constant difference 3")],
      ["a₁ = 18, d = 3.", "3(12) + 15.", "3n + 15 = 60.", "Arithmetic."], tags=["modeling"])
B.orq(S, "honors", "Three numbers form an arithmetic sequence with sum 27 and product 504.", [("Write them as a - d, a, a + d. Find a.", "9"), ("Write an equation for d.", "9(81 - d²) = 504"), ("Find d.", "±5"), ("List the numbers.", "4, 9, 14")],
      ["3a = 27.", "(9 - d)(9)(9 + d).", "81 - d² = 56.", "Either order."], tags=["challenge"])
assert 4 * 9 * 14 == 504
B.sa(S, "cp2", "Find the common difference of 12, 9, 6, 3, …", "d = -3", ["9 - 12."])

# ---------------- Skill 2: geometric sequences ----------------
S = 2
for a1, r, n_, lvl in [(3, 2, 8, "cp2"), (81, F(1, 3), 6, "cp2"), (5, -2, 7, "cp1"), (1000, F(1, 10), 5, "cp2"), (-2, 3, 6, "cp1"), (64, F(-1, 2), 9, "cp1")]:
    v = geom(a1, r, 4); an = F(a1) * F(r) ** (n_ - 1)
    B.sa(S, lvl, f"Find the {n_}th term of the geometric sequence {lst(v)}, …", fr(an), [f"r = {fr(r)}.", f"aₙ = a₁·r^(n - 1) = {fr(a1)}({fr(r)})^{n_ - 1} = {fr(an)}."])
for a1, r in [(4, 3), (200, F(1, 2)), (-1, 5), (6, F(-1, 3))]:
    B.sa(S, "cp2" if isinstance(r, int) else "cp1", f"Write an explicit formula for the geometric sequence {lst(geom(a1, r, 4))}, …", geo_n(a1, r), [f"a₁ = {fr(a1)}, r = {fr(r)}.", f"aₙ = a₁·r^(n - 1)."])
for (m, am), (k, ak), r in [((2, 12), (5, 324), 3), ((3, 20), (6, F(5, 2)), F(1, 2)), ((1, 5), (4, -40), -2)]:
    a1 = F(am) / F(r) ** (m - 1); assert a1 * F(r) ** (k - 1) == ak
    B.sa(S, "cp1" if r > 0 else "honors", f"A geometric sequence has a{'₀₁₂₃₄₅₆₇₈₉'[m]} = {fr(am)} and a{'₀₁₂₃₄₅₆₇₈₉'[k]} = {fr(ak)}. Find r and a₁.", f"r = {fr(r)}, a₁ = {fr(a1)}",
         [f"r^{k - m} = {fr(ak)}/{fr(am)} = {fr(F(ak) / F(am))} → r = {fr(r)}.", f"a₁ = {fr(am)}/r^{m - 1} = {fr(a1)}."])
B.sa(S, "honors", "Find the geometric mean of 4 and 49, and the two possible geometric sequences 4, x, 49.", "x = ±14", ["x² = 4·49 = 196."], tags=["connections"])
for seq, kind in [("2, 6, 18, 54", "geometric"), ("5, 10, 15, 20", "arithmetic"), ("1, -1, 1, -1", "geometric"), ("1, 2, 4, 7", "neither"), ("16, 8, 4, 2", "geometric"), ("3, 3, 3, 3", "both")]:
    B.mc(S, "cp2", f"Classify the sequence {seq}, …", kind, [k for k in ["arithmetic", "geometric", "neither", "both"] if k != kind][:3], ["Check for a constant difference (arithmetic) and a constant ratio (geometric)."])
B.mc(S, "cp1", "A student says 2, 6, 18, … has r = 4 because 6 - 2 = 4. What is correct?", "r = 3 (divide consecutive terms)", ["r = 4", "d = 4 and r = 3", "r = 1/3"], ["The ratio is 6/2 = 3; 4 is the first difference."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "Select ALL geometric sequences.", ["3, 12, 48, 192", "100, 50, 25, 12.5", "2, -4, 8, -16", "1, 4, 9, 16", "5, 10, 15, 20", "1/3, 1, 3, 9", "2, 4, 6, 8"],
         lambda s_: len({F(b) / F(a) for a, b in zip(s_.split(", "), s_.split(", ")[1:])}) == 1, ["Constant ratio between consecutive terms."])
sel_auto(B, S, "honors", "aₙ = 6(-1/2)^(n - 1). Select ALL true statements.", ["a₁ = 6", "r = -1/2", "a₄ = -3/4", "The terms alternate in sign", "a₂ = 3", "|aₙ| increases"],
         lambda s_: s_ in ("a₁ = 6", "r = -1/2", "a₄ = -3/4", "The terms alternate in sign"), ["6, -3, 3/2, -3/4, …", "|r| < 1 → magnitudes shrink."])
B.orq(S, "cp1", "A ball is dropped from 81 ft and rebounds to 2/3 of its previous height each bounce.", [("Write a formula for the height of the nth rebound.", "hₙ = 54(2/3)^(n - 1)"), ("Find the height of the 4th rebound.", "16 ft"), ("Which rebound is the first below 5 ft?", f"the {next(n for n in range(1, 20) if 54 * (2 / 3) ** (n - 1) < 5)}th"), ("Is this sequence geometric? Why?", "Yes, constant ratio 2/3")],
      ["First rebound 81·2/3 = 54.", "54(8/27).", "Test values.", "Ratio."], tags=["modeling"])
assert 54 * F(2, 3) ** 3 == 16
B.mc(S, "cp1", "The graph of a geometric sequence with r > 1 looks like…", "points on an exponential curve", ["points on a line", "a parabola", "a horizontal line"], ["aₙ = a₁rⁿ⁻¹ is exponential in n."], tags=["connections"])
B.sa(S, "cp2", "Find the common ratio of 5, -15, 45, …", "r = -3", ["-15/5."])

# ---------------- Skill 3: recursive and explicit formulas ----------------
S = 3
for a1, rule, kind, p in [(4, "aₙ = aₙ₋₁ + 5", "a", 5), (2, "aₙ = 3aₙ₋₁", "g", 3), (-1, "aₙ = aₙ₋₁ - 4", "a", -4), (100, "aₙ = 0.5aₙ₋₁", "g", F(1, 2)), (1, "aₙ = 2aₙ₋₁ + 1", "x", None), (3, "aₙ = (aₙ₋₁)² - 2", "y", None)]:
    v = [F(a1)]
    for _ in range(4):
        v.append(v[-1] + p if kind == "a" else v[-1] * p if kind == "g" else 2 * v[-1] + 1 if kind == "x" else v[-1] ** 2 - 2)
    B.sa(S, "cp2" if kind in "ag" else "cp1", f"Write the first five terms: a₁ = {a1}, {rule}.", lst(v), ["Apply the rule repeatedly starting from a₁."])
for a1, d in [(6, 4), (-2, 7), (10, -3)]:
    B.mc(S, "cp1", f"Which explicit formula matches a₁ = {a1}, aₙ = aₙ₋₁ {'+' if d > 0 else '-'} {abs(d)}?", lin_n(a1, d), [lin_n(d, a1), f"aₙ = {d}n + {a1}".replace("+ -", "- "), lin_n(a1, -d)], ["Arithmetic with d = " + str(d) + ".", f"aₙ = {a1} + (n - 1)({d})."])
for a1, r in [(5, 2), (48, F(1, 4)), (-3, -2)]:
    B.mc(S, "cp1", f"Which explicit formula matches a₁ = {fr(a1)}, aₙ = {fr(r)}·aₙ₋₁?", geo_n(a1, r), [geo_n(r, a1) if a1 != r else geo_n(a1, -r), f"aₙ = {fr(a1)}({fr(r)})^n", f"aₙ = {fr(a1)} + {fr(r)}(n - 1)"], ["Geometric with r = " + fr(r) + "."])
for expl, rec in [("aₙ = 8n - 3", "a₁ = 5, aₙ = aₙ₋₁ + 8"), ("aₙ = 2(5)^(n - 1)", "a₁ = 2, aₙ = 5aₙ₋₁"), ("aₙ = 20 - 6n", "a₁ = 14, aₙ = aₙ₋₁ - 6"), ("aₙ = -(1/3)^(n - 1)", "a₁ = -1, aₙ = (1/3)aₙ₋₁")]:
    B.sa(S, "cp1", f"Write a recursive formula for {expl}.", rec, ["Find a₁ by substituting n = 1.", "Find the common difference or ratio."])
B.sa(S, "cp1", "The Fibonacci sequence: a₁ = 1, a₂ = 1, aₙ = aₙ₋₁ + aₙ₋₂. Find a₁₀.", "55", ["1, 1, 2, 3, 5, 8, 13, 21, 34, 55."])
B.mc(S, "cp1", "Which is an advantage of an explicit formula over a recursive one?", "It finds any term directly without computing previous terms", ["It always has fewer symbols", "It works only for arithmetic sequences", "It needs the previous term"], ["Explicit: aₙ in terms of n."], tags=["reasoning"])
sel_auto(B, S, "cp1", "Select ALL formulas that generate 3, 6, 12, 24, …", ["a₁ = 3, aₙ = 2aₙ₋₁", "aₙ = 3(2)^(n - 1)", "aₙ = (3/2)(2)^n", "aₙ = 3n", "a₁ = 3, aₙ = aₙ₋₁ + 3", "aₙ = 3(2)^n"],
         lambda s_: s_ in ("a₁ = 3, aₙ = 2aₙ₋₁", "aₙ = 3(2)^(n - 1)", "aₙ = (3/2)(2)^n"), ["Check the first few terms of each formula.", "(3/2)·2ⁿ = 3·2ⁿ⁻¹."])
sel_auto(B, S, "honors", "a₁ = 2 and aₙ = aₙ₋₁ + 2n. Select ALL true statements.", ["a₂ = 6", "a₃ = 12", "a₄ = 20", "aₙ = n(n + 1)", "The sequence is arithmetic", "a₅ = 25"],
         lambda s_: s_ in ("a₂ = 6", "a₃ = 12", "a₄ = 20", "aₙ = n(n + 1)"), ["2, 6, 12, 20, 30: differences 4, 6, 8, … are not constant.", "n(n + 1) matches every term."], tags=["challenge"])
B.orq(S, "cp1", "A savings account starts with $50 and $15 is added each week.", [("Write a recursive formula.", "a₁ = 50, aₙ = aₙ₋₁ + 15"), ("Write an explicit formula.", "aₙ = 15n + 35"), ("Find the balance in week 20.", "$335"), ("Which formula is easier for week 20? Why?", "Explicit: substitute n = 20 directly")],
      ["Add 15 each week.", "50 + 15(n - 1).", "15(20) + 35.", "No need for prior terms."], tags=["modeling"])
B.orq(S, "honors", "aₙ = 3aₙ₋₁ - 4 with a₁ = 3.", [("Find a₂, a₃, a₄.", "5, 11, 29"), ("Let bₙ = aₙ - 2. Find b₁, b₂, b₃.", "1, 3, 9"), ("What kind of sequence is bₙ?", "geometric with r = 3"), ("Write an explicit formula for aₙ.", "aₙ = 3^(n - 1) + 2")],
      ["Iterate.", "Subtract 2.", "Ratio 3.", "aₙ = bₙ + 2."], tags=["challenge"])
v = [3]
for _ in range(5): v.append(3 * v[-1] - 4)
assert all(v[k] == 3 ** k + 2 for k in range(6))

# ---------------- Skill 4: arithmetic series ----------------
S = 4
for a1, d, n_, lvl in [(2, 3, 20, "cp2"), (50, -4, 15, "cp1"), (-7, 5, 30, "cp1"), (1, 1, 100, "cp2"), (F(1, 2), F(1, 2), 40, "cp1"), (100, -3, 34, "cp1")]:
    an = F(a1) + (n_ - 1) * F(d); Sn = F(n_) * (F(a1) + an) / 2
    assert Sn == sum(arith(a1, d, n_))
    B.sa(S, lvl, f"Find the sum of the first {n_} terms of the arithmetic series {lst(arith(a1, d, 3))}, …", fr(Sn), [f"aₙ = {fr(a1)} + {n_ - 1}({fr(d)}) = {fr(an)}.", f"Sₙ = n(a₁ + aₙ)/2 = {n_}({fr(a1)} + {fr(an)})/2 = {fr(Sn)}."])
for a1, d, last in [(3, 4, 99), (10, 5, 200), (-20, 3, 40), (97, -6, 1)]:
    n_ = (last - a1) // d + 1; Sn = n_ * (a1 + last) // 2; assert sum(range(a1, last + (1 if d > 0 else -1), d)) == Sn
    B.sa(S, "cp1", f"Find the sum {a1} + {a1 + d} + {a1 + 2 * d} + … + {last}.".replace("+ -", "- "), str(Sn), [f"Number of terms: ({last} - ({a1}))/{d} + 1 = {n_}.", f"S = {n_}({a1} + {last})/2 = {Sn}."])
B.mc(S, "cp1", "What is the sum of the first 50 positive odd numbers?", "2500", ["2550", "1275", "5000"], ["1 + 3 + … + 99: 50 terms, sum = 50(1 + 99)/2 = 2500 = 50²."])
B.mc(S, "cp1", "A student finds 2 + 5 + 8 + … + 62 using 62 terms. How many terms are there?", "21", ["62", "20", "60"], ["(62 - 2)/3 + 1 = 21."], tags=["error-analysis"])
B.sa(S, "honors", "How many terms of 5 + 9 + 13 + … give a sum of 495?", "15", ["Sₙ = n(5 + 4n + 1)/2 = 2n² + 3n.", "2n² + 3n - 495 = 0 → (2n + 33)(n - 15) = 0."], tags=["challenge"])
assert sum(arith(5, 4, 15)) == 495
B.sa(S, "honors", "Find the sum of all multiples of 7 between 100 and 500.", str(sum(k for k in range(100, 501) if k % 7 == 0)), ["First 105, last 497: 57 terms.", "S = 57(105 + 497)/2."])
sel_auto(B, S, "cp1", "Select ALL expressions equal to 1 + 2 + 3 + … + 40.", ["40·41/2", "820", "20·41", "40²/2", "(1 + 40)·20", "40·40"], lambda s_: same(peval(s_), 820), ["Sₙ = n(n + 1)/2 = 820."])
B.orq(S, "cp1", "A stack of logs has 24 logs on the bottom row and one fewer in each row above, ending with 10 logs on top.", [("How many rows?", "15"), ("Write the series.", "24 + 23 + … + 10"), ("Find the total number of logs.", "255"), ("How many rows would a full stack to 1 log have?", "24")],
      ["24 - 10 + 1.", "Arithmetic, d = -1.", "15(24 + 10)/2.", "24 down to 1."], tags=["modeling"])
B.orq(S, "honors", "Derive the arithmetic series formula.", [("Write S = a₁ + (a₁ + d) + … + aₙ forward and backward.", "S = aₙ + (aₙ - d) + … + a₁"), ("Add the two lines term by term.", "2S = n(a₁ + aₙ)"), ("Solve for S.", "S = n(a₁ + aₙ)/2"), ("Use it for 1 + 2 + … + 1000.", "500,500")],
      ["Reverse order.", "Each pair sums to a₁ + aₙ; n pairs.", "Divide by 2.", "1000·1001/2."], tags=["reasoning"])
B.sa(S, "cp2", "Find the sum 4 + 8 + 12 + … + 40.", "220", ["10 terms; 10(4 + 40)/2."])

# ---------------- Skill 5: geometric series ----------------
S = 5
for a1, r, n_, lvl in [(3, 2, 8, "cp1"), (1, 3, 6, "cp2"), (64, F(1, 2), 7, "cp1"), (5, -2, 9, "cp1"), (2, F(1, 3), 5, "honors"), (1000, F(11, 10), 4, "cp1")]:
    Sn = F(a1) * (1 - F(r) ** n_) / (1 - F(r)); assert Sn == sum(geom(a1, r, n_))
    B.sa(S, lvl, f"Find the sum of the first {n_} terms of the geometric series {lst(geom(a1, r, 3))}, …", fr(Sn), [f"r = {fr(r)}.", f"Sₙ = a₁(1 - rⁿ)/(1 - r) = {fr(a1)}(1 - ({fr(r)})^{n_})/(1 - {frp(r)}) = {fr(Sn)}."])
for a1, r, last in [(2, 3, 486), (1, 2, 512), (729, F(1, 3), 1), (3, -2, 192)]:
    n_ = next(k for k in range(1, 40) if F(a1) * F(r) ** (k - 1) == last); Sn = sum(geom(a1, r, n_))
    B.sa(S, "cp1", f"Find the sum {a1} + {fr(F(a1) * r)} + {fr(F(a1) * F(r) ** 2)} + … + {last}.".replace("+ -", "- "), fr(Sn), [f"r = {fr(r)}; {last} is term {n_}.", f"S = {fr(a1)}(1 - ({fr(r)})^{n_})/(1 - {frp(r)}) = {fr(Sn)}."])
B.mc(S, "cp1", "A student uses Sₙ = a₁(1 - rⁿ)/(1 - r) with r = 1. What happens?", "Division by zero; when r = 1 the sum is n·a₁", ["The sum is 0", "The sum is a₁", "The sum is infinite"], ["Every term equals a₁."], tags=["reasoning"])
B.mc(S, "cp1", "Find 1 + 2 + 4 + … + 2⁹.", "1023", ["1024", "512", "2047"], ["S₁₀ = (2¹⁰ - 1)/(2 - 1)."])
B.sa(S, "honors", "How many terms of 3 + 6 + 12 + … are needed for the sum to exceed 10,000?", "12", ["Sₙ = 3(2ⁿ - 1) > 10,000 → 2ⁿ > 3334.3.", "2¹¹ = 2048, 2¹² = 4096 → n = 12."], tags=["challenge"])
assert 3 * (2 ** 11 - 1) < 10000 < 3 * (2 ** 12 - 1)
B.sa(S, "honors", "A geometric series has a₁ = 4 and S₃ = 52. Find all possible r.", "r = 3 or r = -4", ["4(1 + r + r²) = 52 → r² + r - 12 = 0.", "(r + 4)(r - 3) = 0."], tags=["challenge"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to 2 + 6 + 18 + 54 + 162.", ["2(3⁵ - 1)/(3 - 1)", "242", "3⁵ - 1", "2(1 - 3⁵)/(1 - 3)", "5·2·3", "2·3⁵"], lambda s_: same(peval(s_), 242), ["S₅ = 2(3⁵ - 1)/2 = 242."])
B.orq(S, "cp1", "You save $1 the first day and double the amount each day.", [("How much do you save on day 10?", "$512"), ("Total after 10 days?", "$1023"), ("Total after 20 days?", "$1,048,575"), ("On which day does the total first exceed $1,000,000?", "day 20")],
      ["2⁹.", "2¹⁰ - 1.", "2²⁰ - 1.", "2¹⁹ - 1 = 524,287 < 1,000,000."], tags=["modeling"])
B.orq(S, "honors", "Derive Sₙ for a geometric series.", [("Write Sₙ and rSₙ.", "Sₙ = a₁ + a₁r + … + a₁rⁿ⁻¹; rSₙ = a₁r + … + a₁rⁿ"), ("Subtract.", "Sₙ - rSₙ = a₁ - a₁rⁿ"), ("Solve for Sₙ.", "Sₙ = a₁(1 - rⁿ)/(1 - r)"), ("Use it for 5 + 15 + … to 6 terms.", "1820")],
      ["Multiply by r.", "Middle terms cancel.", "Factor.", "5(3⁶ - 1)/2."], tags=["reasoning"])
assert 5 * (3 ** 6 - 1) // 2 == 1820
B.sa(S, "cp2", "Find 1 + 3 + 9 + 27.", "40", ["Add, or 1(3⁴ - 1)/2."])

# ---------------- Skill 6: sigma notation ----------------
S = 6
for lo, hi, expr, f_ in [(1, 5, "(2k + 1)", lambda k: 2 * k + 1), (1, 4, "k²", lambda k: k * k), (0, 4, "3(2)^k", lambda k: 3 * 2 ** k), (3, 7, "(10 - k)", lambda k: 10 - k), (1, 6, "(-1)^k·k", lambda k: (-1) ** k * k), (2, 5, "1/k", lambda k: F(1, k))]:
    terms = [F(f_(k)) for k in range(lo, hi + 1)]
    B.sa(S, "cp2" if "^" not in expr and "/" not in expr else "cp1", f"Evaluate Σ from k = {lo} to {hi} of {expr}.", fr(sum(terms)), [f"Terms: {lst(terms)}.", f"Sum = {fr(sum(terms))}."])
for lo, hi, a, b in [(1, 20, 3, -1), (1, 50, 2, 5), (1, 30, -4, 100), (5, 24, 1, 0)]:
    tot = sum(a * k + b for k in range(lo, hi + 1)); nt = hi - lo + 1
    B.sa(S, "cp1", f"Evaluate Σ from k = {lo} to {hi} of ({fr(a)}k {'+' if b >= 0 else '-'} {abs(b)}).".replace("(1k", "(k").replace(" + 0)", ")").replace("of (k)", "of k"), str(tot),
         [f"Arithmetic series with {nt} terms: first {a * lo + b}, last {a * hi + b}.", f"S = {nt}({a * lo + b} + {a * hi + b})/2 = {tot}."])
for lo, hi, a, r in [(1, 8, 2, 3), (1, 6, 5, F(1, 2)), (0, 9, 1, 2)]:
    tot = sum(F(a) * F(r) ** (k - 1 if lo == 1 else k) for k in range(lo, hi + 1))
    expr = f"{a}({fr(r)})^(k - 1)" if lo == 1 else f"{fr(r)}^k"
    B.sa(S, "cp1", f"Evaluate Σ from k = {lo} to {hi} of {expr}.", fr(tot), ["This is a geometric series.", f"a₁ = {fr(a if lo == 1 else 1)}, r = {fr(r)}, n = {hi - lo + 1}.", f"S = {fr(tot)}."])
for series, sig in [("3 + 6 + 9 + … + 60", "Σ from k = 1 to 20 of 3k"), ("2 + 4 + 8 + … + 256", "Σ from k = 1 to 8 of 2^k"), ("1 + 4 + 9 + … + 100", "Σ from k = 1 to 10 of k²"), ("5 + 9 + 13 + … + 41", "Σ from k = 1 to 10 of (4k + 1)"), ("1/2 + 1/4 + … + 1/64", "Σ from k = 1 to 6 of (1/2)^k")]:
    B.sa(S, "cp1", f"Write {series} in sigma notation.", sig + " (other forms possible)", ["Find a formula for the kth term.", "Find the index of the last term."])
B.mc(S, "cp2", "How many terms are in Σ from k = 4 to 15 of (k + 2)?", "12", ["11", "15", "13"], ["15 - 4 + 1 = 12."], tags=["misconception"])
B.mc(S, "cp1", "Which equals Σ from k = 1 to 10 of 5?", "50", ["5", "55", "10"], ["Ten terms, each 5."], tags=["misconception"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to Σ from k = 1 to 5 of 2k.", ["2 + 4 + 6 + 8 + 10", "30", "2·Σ from k = 1 to 5 of k", "Σ from j = 2 to 6 of 2(j - 1)", "Σ from k = 1 to 5 of k²", "2·5"],
         lambda s_: s_ in ("2 + 4 + 6 + 8 + 10", "30", "2·Σ from k = 1 to 5 of k", "Σ from j = 2 to 6 of 2(j - 1)"), ["2(1 + 2 + 3 + 4 + 5) = 30.", "Shifting the index: j = k + 1."])
sel_auto(B, S, "honors", "Select ALL true properties of sigma notation.", ["Σ(aₖ + bₖ) = Σaₖ + Σbₖ", "Σ c·aₖ = c·Σaₖ", "Σ from k = 1 to n of c = cn", "Σ aₖbₖ = (Σaₖ)(Σbₖ)", "Σ aₖ² = (Σaₖ)²", "Σ(aₖ/bₖ) = Σaₖ/Σbₖ"],
         lambda s_: s_ in ("Σ(aₖ + bₖ) = Σaₖ + Σbₖ", "Σ c·aₖ = c·Σaₖ", "Σ from k = 1 to n of c = cn"), ["Sums split over addition and constants factor out.", "Products and quotients do not distribute."], tags=["reasoning"])
B.orq(S, "honors", "Evaluate Σ from k = 1 to 20 of (k² + 3k) using Σk = n(n + 1)/2 and Σk² = n(n + 1)(2n + 1)/6.", [("Find Σk² for n = 20.", "2870"), ("Find Σk for n = 20.", "210"), ("Combine.", "2870 + 630 = 3500"), ("Check with the first 3 terms (k = 1, 2, 3).", "4 + 10 + 18 = 32")],
      ["20·21·41/6.", "20·21/2.", "Σk² + 3Σk.", "Direct."], tags=["challenge"])
assert sum(k * k + 3 * k for k in range(1, 21)) == 3500
B.orq(S, "cp1", "Consider Σ from n = 1 to 6 of (20 - 3n).", [("Write out the terms.", "17, 14, 11, 8, 5, 2"), ("Is this arithmetic or geometric?", "arithmetic, d = -3"), ("Find the sum.", "57"), ("Rewrite with index starting at 0.", "Σ from n = 0 to 5 of (17 - 3n)")],
      ["Substitute n = 1…6.", "Constant difference.", "6(17 + 2)/2.", "Shift n → n + 1."])

# ---------------- Skill 7: finite and infinite geometric series ----------------
S = 7
for a1, r in [(12, F(1, 2)), (9, F(1, 3)), (5, F(-1, 4)), (100, F(3, 5)), (F(3, 4), F(1, 4)), (8, F(-1, 2))]:
    Ssum = F(a1) / (1 - F(r))
    B.sa(S, "cp1" if r > 0 else "honors", f"Find the sum of the infinite geometric series {lst(geom(a1, r, 3))}, …", fr(Ssum), [f"|r| = {fr(abs(r))} < 1, so the series converges.", f"S = a₁/(1 - r) = {fr(a1)}/(1 - {frp(r)}) = {fr(Ssum)}."])
for a1, r, conv in [(3, 2, False), (10, F(9, 10), True), (1, -1, False), (7, F(-5, 4), False), (2, F(-1, 3), True)]:
    ans = f"Converges to {fr(F(a1) / (1 - F(r)))}" if conv else "Diverges"
    B.mc(S, "cp1", f"Does the infinite geometric series with a₁ = {fr(a1)} and r = {fr(r)} converge? If so, find its sum.", ans,
         ["Diverges" if conv else f"Converges to {fr(F(a1) / (1 - F(r)))}", f"Converges to {fr(F(a1) / (1 + F(r)))}" if F(r) != -1 else "Converges to 0", f"Converges to {fr(F(a1) * F(r))}"], ["Converges only when |r| < 1; then S = a₁/(1 - r)."])
for dec_, fr_ in [("0.777…", F(7, 9)), ("0.454545…", F(5, 11)), ("0.1666…", F(1, 6)), ("2.3333…", F(7, 3))]:
    B.sa(S, "honors" if dec_ in ("0.1666…", "2.3333…") else "cp1", f"Write {dec_} as a fraction using an infinite geometric series.", fr(fr_), ["Write the repeating part as a series, e.g. 0.7 + 0.07 + 0.007 + ….", "Use S = a₁/(1 - r) and simplify."], tags=["connections"])
B.mc(S, "cp1", "A student says 1 + 1/2 + 1/4 + … never ends, so its sum is infinite. What is correct?", "The sum is 2 because |r| = 1/2 < 1", ["The sum is infinite", "The sum is 1", "The sum cannot be found"], ["Partial sums 1, 1.5, 1.75, … approach 2."], tags=["misconception", "error-analysis"])
B.mc(S, "honors", "For which x does Σ from n = 0 to ∞ of xⁿ converge?", "-1 < x < 1", ["x < 1", "x > 0", "all x"], ["Geometric with r = x; need |x| < 1."], tags=["reasoning"])
sel_auto(B, S, "cp1", "Select ALL infinite geometric series that converge.", ["4 + 2 + 1 + …", "1 - 1/3 + 1/9 - …", "0.9 + 0.81 + 0.729 + …", "2 + 4 + 8 + …", "1 - 1 + 1 - …", "5 + 5 + 5 + …"],
         lambda s_: s_ in ("4 + 2 + 1 + …", "1 - 1/3 + 1/9 - …", "0.9 + 0.81 + 0.729 + …"), ["Check |r| < 1: 1/2, 1/3, 0.9 converge; 2, 1, 1 do not."])
B.sa(S, "honors", "An infinite geometric series has sum 12 and first term 4. Find r.", "r = 2/3", ["12 = 4/(1 - r) → 1 - r = 1/3."])
B.sa(S, "honors", "Find x if 1 + x + x² + … = 4.", "x = 3/4", ["1/(1 - x) = 4 with |x| < 1."])
B.orq(S, "cp1", "Consider 6 + 3 + 3/2 + 3/4 + …", [("Find r.", "1/2"), ("Find S₅.", fr(sum(geom(6, F(1, 2), 5)))), ("Find the infinite sum.", "12"), ("How far is S₅ from the infinite sum?", fr(12 - sum(geom(6, F(1, 2), 5))))],
      ["3/6.", "6(1 - (1/2)⁵)/(1/2).", "6/(1/2).", "Subtract."])
B.orq(S, "honors", "A ball dropped from 10 m rebounds to 60% of its previous height each time.", [("Distance on the first fall.", "10 m"), ("Write the total upward distance as a series.", "6 + 3.6 + 2.16 + …"), ("Find the total upward distance.", "15 m"), ("Find the total distance traveled.", "40 m")],
      ["Given.", "a₁ = 6, r = 0.6.", "6/0.4.", "10 + 2(15)."], tags=["modeling", "challenge"])
B.sa(S, "cp2", "Find the sum 1 + 1/3 + 1/9 + …", "3/2", ["1/(1 - 1/3)."])

# ---------------- Skill 8: applications ----------------
S = 8
B.sa(S, "cp1", "A salary starts at $42,000 and rises $1,500 per year. What is the salary in year 10, and the total earned over 10 years?", "$55,500; $487,500", ["a₁₀ = 42000 + 9(1500) = 55,500.", "S₁₀ = 10(42000 + 55500)/2."], tags=["modeling"])
B.sa(S, "cp1", "A salary starts at $42,000 and rises 3% per year. What is the salary in year 10 (nearest dollar), and the total over 10 years?", f"${42000 * 1.03 ** 9:,.0f}; ${42000 * (1.03 ** 10 - 1) / 0.03:,.0f}", ["a₁₀ = 42000(1.03)⁹.", "S₁₀ = 42000(1.03¹⁰ - 1)/0.03."], tags=["modeling"])
B.mc(S, "honors", "Which salary plan pays more over 10 years: $42,000 + $1,500/yr or $42,000 with 3% raises?", "$1,500 raises" if 487500 > 42000 * (1.03 ** 10 - 1) / 0.03 else "3% raises", ["3% raises" if 487500 > 42000 * (1.03 ** 10 - 1) / 0.03 else "$1,500 raises", "They are equal", "Cannot tell"],
     [f"Arithmetic total $487,500; geometric total ≈ ${42000 * (1.03 ** 10 - 1) / 0.03:,.0f}."], tags=["modeling", "reasoning"])
B.sa(S, "cp1", "A pyramid display has 1 can on top, 3 in the next row, 5 in the next, and so on for 12 rows. How many cans?", "144", ["Odd numbers: 12² = 144."], tags=["modeling"])
B.sa(S, "cp1", "A car worth $28,000 loses 15% each year. Find its value after 6 years (nearest dollar).", f"${28000 * 0.85 ** 6:,.0f}", ["a₇ = 28000(0.85)⁶ (value after 6 years)."], tags=["modeling"])
B.sa(S, "honors", "Deposits of $200 are made at the start of each month into an account earning 0.5% per month. What is the balance right after the 12th deposit (nearest cent)?", f"${200 * (1.005 ** 12 - 1) / 0.005:,.2f}",
     ["Balance = 200(1.005)¹¹ + … + 200(1.005) + 200.", "Geometric: 200(1.005¹² - 1)/0.005."], tags=["modeling", "challenge"])
B.sa(S, "cp1", "A drug dose of 50 mg is taken daily; 30% remains from each previous dose. Find the amount right after the 4th dose.", f"{50 * (1 - 0.3 ** 4) / 0.7:.2f} mg", ["50 + 15 + 4.5 + 1.35 (geometric r = 0.3).", "S₄ = 50(1 - 0.3⁴)/0.7."], tags=["modeling"])
B.sa(S, "honors", "In the long run, how much of the drug (50 mg daily, 30% remains) is in the body right after a dose?", f"{50 / 0.7:.2f} mg", ["Infinite geometric series: 50/(1 - 0.3)."], tags=["modeling"])
B.mc(S, "cp1", "A pattern adds 4 tiles each step, starting with 6 tiles. Which model fits?", "Arithmetic: tₙ = 4n + 2", ["Geometric: tₙ = 6(4)^(n - 1)", "Arithmetic: tₙ = 6n + 4", "Geometric: tₙ = 4(6)^(n - 1)"], ["Constant addition → arithmetic; t₁ = 6, d = 4."], tags=["modeling"])
B.mc(S, "cp1", "A chain email: 1 person sends it in week 1, 4 people in week 2, 16 in week 3, and so on. How many people send it in week 5?", "256", ["20", "1024", "64"], ["Geometric: aₙ = 4ⁿ⁻¹; a₅ = 4⁴ = 256."], tags=["modeling"])
sel_auto(B, S, "cp1", "Select ALL situations modeled by an arithmetic sequence.", ["Seats increase by 2 per row", "A gym charges $30 plus $10 per month (total paid)", "Temperature drops 3°F each hour", "Bacteria double every hour", "A car loses 12% of its value yearly", "Interest compounds at 5%"],
         lambda s_: s_ in ("Seats increase by 2 per row", "A gym charges $30 plus $10 per month (total paid)", "Temperature drops 3°F each hour"), ["Constant change → arithmetic; constant percent change → geometric."])
B.sel(S, "honors", "Select ALL statements that are true about the total distance of a ball dropped from 12 ft that rebounds to 3/4 of its height.", ["The total distance is finite", "The first rebound is 9 ft", "The total distance is 84 ft"], ["The total distance is infinite", "The total distance is 48 ft"],
      ["Down 12, then up and down 9, 6.75, …: 12 + 2(9/(1 - 3/4)) = 12 + 72 = 84."], tags=["modeling"])
B.orq(S, "cp1", "An auditorium has 20 seats in row 1, and each row has 2 more seats than the previous one. There are 25 rows.", [("Seats in row 25?", "68"), ("Total seats?", "2200"), ("Which row has 50 seats?", "row 16"), ("How many seats in rows 1–10?", "290")],
      ["20 + 24(2).", "25(20 + 68)/2.", "20 + 2(n - 1) = 50.", "10(20 + 38)/2."], tags=["modeling"])
B.orq(S, "honors", "A loan of $10,000 is repaid at $500 per month; each month 1% interest is charged on the remaining balance before the payment.", [("Balance after month 1.", "$9,600"), ("Balance after month 2.", "$9,196"), ("Write a recursive formula.", "b₀ = 10000, bₙ = 1.01bₙ₋₁ - 500"), ("Is the balance sequence arithmetic, geometric, or neither?", "neither")],
      ["10000(1.01) - 500.", "9600(1.01) - 500.", "Interest then payment.", "Differences and ratios vary."], tags=["modeling", "challenge"])
assert round(10000 * 1.01 - 500, 2) == 9600 and round(9600 * 1.01 - 500, 2) == 9196
B.orq(S, "cp1", "A plant is 4 cm tall and grows 1.5 cm per week. Another is 2 cm and grows 20% per week.", [("Write a formula for each after n weeks.", "A = 4 + 1.5n; B = 2(1.2)^n"), ("Find each height after 8 weeks.", f"16 cm and {2 * 1.2 ** 8:.2f} cm"), ("After which whole week is B taller?", f"week {next(n for n in range(1, 50) if 2 * 1.2 ** n > 4 + 1.5 * n)}"), ("Which type of growth eventually wins?", "geometric (exponential)")],
      ["Linear vs exponential.", "Substitute.", "Compare week by week.", "Constant ratio > 1 beats constant difference."], tags=["modeling", "connections"])
B.sa(S, "cp2", "A runner adds 0.5 mi each week, starting at 3 mi. How far in week 6?", "5.5 mi", ["3 + 5(0.5)."], tags=["modeling"])

# ================= additions: format balance =================
for a1, d in [(4, 6), (-9, 2.5)]:
    d = F(d).limit_denominator(10); v = arith(a1, d, 30)
    st = {f"a₁₀ = {fr(v[9])}": True, f"a₁₀ = {fr(v[9] + d)}": False, f"d = {fr(d)}": True, f"a₂₀ - a₁₀ = {fr(10 * d)}": True, f"aₙ = {fr(d)}n + {fr(a1)}": d == 0, f"{fr(v[24])} is a term": True, f"{fr(v[24] + d / 2)} is a term": False}
    B.sel(1, "cp1", f"The arithmetic sequence {lst(v[:4])}, … Select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["aₙ = a₁ + (n - 1)d.", "Differences of terms are multiples of d."])
for a1, r in [(2, 3), (96, F(1, 2)), (-1, -2), (5, F(2, 5))]:
    v = geom(a1, r, 10); good = fr(v[7])
    B.mc(2, "cp1", f"What is the 8th term of {lst(v[:4])}, …?", good, [fr(v[8]), fr(F(a1) * F(r) * 8), fr(v[6])], ["aₙ = a₁rⁿ⁻¹.", f"a₈ = {fr(a1)}({fr(r)})⁷ = {good}.", "Using rⁿ instead of rⁿ⁻¹ gives the 9th term."], tags=["misconception"])
for tbl, rec, wr in [("n: 1, 2, 3, 4; aₙ: 7, 11, 15, 19", "a₁ = 7, aₙ = aₙ₋₁ + 4", ["a₁ = 4, aₙ = aₙ₋₁ + 7", "a₁ = 7, aₙ = 4aₙ₋₁", "aₙ = aₙ₋₁ + 4 (no a₁ needed)"]),
                     ("n: 1, 2, 3, 4; aₙ: 5, 15, 45, 135", "a₁ = 5, aₙ = 3aₙ₋₁", ["a₁ = 5, aₙ = aₙ₋₁ + 10", "a₁ = 3, aₙ = 5aₙ₋₁", "aₙ = 5·3n"]),
                     ("n: 1, 2, 3, 4; aₙ: 80, 40, 20, 10", "a₁ = 80, aₙ = (1/2)aₙ₋₁", ["a₁ = 80, aₙ = aₙ₋₁ - 40", "a₁ = 80, aₙ = 2aₙ₋₁", "a₁ = 10, aₙ = 2aₙ₋₁"]),
                     ("n: 1, 2, 3, 4; aₙ: 2, 5, 11, 23", "a₁ = 2, aₙ = 2aₙ₋₁ + 1", ["a₁ = 2, aₙ = aₙ₋₁ + 3", "a₁ = 2, aₙ = 3aₙ₋₁ - 1", "a₁ = 2, aₙ = 2aₙ₋₁"])]:
    B.mc(3, "cp1" if "+ 1" not in rec else "honors", f"Which recursive formula matches the table? {tbl}", rec, wr, ["A recursive formula needs a starting term and a rule using the previous term.", "Test the rule on every pair of consecutive terms."], tags=["multiple-representations"])
vv = [2]
for _ in range(3): vv.append(2 * vv[-1] + 1)
assert vv == [2, 5, 11, 23]
for a1, d, n_ in [(9, 4, 6), (-3, 5, 8)]:
    B.orq(3, "cp1", f"A sequence has a₁ = {a1} and aₙ = aₙ₋₁ {'+' if d > 0 else '-'} {abs(d)}.", [("List the first four terms.", lst(arith(a1, d, 4))), ("Write the explicit formula.", lin_n(a1, d)), (f"Find a{'₀₁₂₃₄₅₆₇₈₉'[n_]} two ways and compare.", fr(arith(a1, d, n_)[-1])), ("Graph type of (n, aₙ)?", "points on a line")],
          ["Add d repeatedly.", "aₙ = a₁ + (n - 1)d.", "Iterate or substitute.", "Arithmetic → linear."])
B.sel(3, "honors", "Select ALL sequences that CANNOT be written as aₙ = aₙ₋₁ + d or aₙ = r·aₙ₋₁.", ["1, 1, 2, 3, 5, 8", "1, 4, 9, 16", "2, 5, 11, 23"], ["3, 3, 3, 3", "10, 7, 4, 1", "1, -2, 4, -8"], ["Neither differences nor ratios are constant for the first three."], tags=["reasoning"])
B.sa(3, "cp2", "a₁ = 10, aₙ = aₙ₋₁ - 3. Find a₄.", "1", ["10, 7, 4, 1."])
for a1, d, n_ in [(6, 5, 12), (40, -3, 15), (1, 2, 25), (-10, 4, 20), (F(3, 2), F(1, 2), 10)]:
    an = F(a1) + (n_ - 1) * F(d); Sn = sum(arith(a1, d, n_))
    B.mc(4, "cp1", f"Find the sum of the first {n_} terms of {lst(arith(a1, d, 3))}, …", fr(Sn), [fr(n_ * (F(a1) + an)), fr(an), fr(F(n_) * (F(a1) + an - F(d)) / 2)], [f"a{n_} = {fr(an)}.", f"S = n(a₁ + aₙ)/2 = {fr(Sn)}.", "Forgetting to divide by 2 doubles the sum."], tags=["misconception"])
for a1, d, n_ in [(3, 7, 10), (100, -8, 12), (-5, 3, 16)]:
    v = arith(a1, d, n_); Sn = sum(v)
    st = {f"S{''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n_))} = {fr(Sn)}": True, f"a{''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n_))} = {fr(v[-1])}": True, f"The average term is {fr(Sn / n_)}": True,
          f"S{''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n_))} = {fr(2 * Sn)}": False, f"The average term is {fr(F(d) * n_)}": False}
    B.sel(4, "cp1", f"For the arithmetic series {lst(v[:3])}, … with {n_} terms, select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Last term a₁ + (n - 1)d.", "S = n·(average of first and last)."])
for a1, last, d in [(7, 151, 4), (90, 6, -6)]:
    n_ = (last - a1) // d + 1; Sn = n_ * (a1 + last) // 2
    B.orq(4, "cp1", f"Consider the arithmetic series {a1} + {a1 + d} + … + {last}.", [("Find d.", str(d)), ("Find the number of terms.", str(n_)), ("Find the sum.", str(Sn)), ("Write it in sigma notation.", f"Σ from k = 1 to {n_} of ({pstr(P([a1 - d, d], 'k'))})")],
          ["Subtract consecutive terms.", "(last - first)/d + 1.", "n(first + last)/2.", "kth term a₁ + (k - 1)d."])
    assert sum(range(a1, last + (1 if d > 0 else -1), d)) == Sn
B.sa(4, "honors", "The sum of the first n terms of an arithmetic series is Sₙ = 3n² + 2n. Find a₁ and d.", "a₁ = 5, d = 6", ["a₁ = S₁ = 5.", "a₂ = S₂ - S₁ = 16 - 5 = 11, so d = 6."], tags=["challenge"])
B.sa(4, "cp1", "Find the sum of the integers from 1 to 200 that are divisible by 4.", "5100", ["4 + 8 + … + 200: 50 terms.", "50(4 + 200)/2."])
assert sum(range(4, 201, 4)) == 5100
for a1, r, n_ in [(4, 3, 6), (1, 2, 12), (81, F(1, 3), 5), (6, -2, 7), (10, F(1, 2), 6)]:
    Sn = sum(geom(a1, r, n_))
    B.mc(5, "cp1", f"Find the sum of the first {n_} terms of {lst(geom(a1, r, 3))}, …", fr(Sn), [fr(geom(a1, r, n_)[-1]), fr(sum(geom(a1, r, n_ + 1))), fr(F(a1) * (1 - F(r) ** n_) / (1 + F(r))) if F(r) != -1 else "0"], ["Sₙ = a₁(1 - rⁿ)/(1 - r).", f"= {fr(Sn)}."])
for a1, r, n_ in [(5, 2, 8), (243, F(1, 3), 6)]:
    v = geom(a1, r, n_)
    B.orq(5, "cp1", f"Consider the geometric series {lst(v[:3])}, … with {n_} terms.", [("Find r.", fr(r)), ("Find the last term.", fr(v[-1])), ("Find the sum.", fr(sum(v))), ("Write it in sigma notation.", f"Σ from k = 1 to {n_} of {fr(a1)}({fr(r)})^(k - 1)")],
          ["Ratio of consecutive terms.", "a₁rⁿ⁻¹.", "Sₙ formula.", "kth term a₁rᵏ⁻¹."])
B.sel(5, "cp1", "S = 3 + 6 + 12 + … + 384. Select ALL true statements.", ["r = 2", "There are 8 terms", "S = 765"], ["There are 7 terms", "S = 768", "r = 3"], ["384 = 3·2⁷ → 8 terms.", "3(2⁸ - 1) = 765."])
assert sum(geom(3, 2, 8)) == 765
B.sel(5, "honors", "Select ALL expressions equal to 1 + r + r² + … + r⁹ (r ≠ 1).", ["(1 - r¹⁰)/(1 - r)", "(r¹⁰ - 1)/(r - 1)", "Σ from k = 0 to 9 of rᵏ"], ["(1 - r⁹)/(1 - r)", "10r", "(r⁹ - 1)/(r - 1)"], ["10 terms starting at r⁰."], tags=["reasoning"])
B.sa(5, "cp1", "Find 2 - 4 + 8 - 16 + 32 - 64.", "-42", ["a₁ = 2, r = -2, n = 6: 2(1 - 64)/3."])
assert sum(geom(2, -2, 6)) == -42
B.sa(5, "honors", "A geometric series has r = 2 and S₆ = 189. Find a₁.", "3", ["a₁(2⁶ - 1) = 189 → 63a₁ = 189."])
B.sa(5, "cp1", "Find the sum of the first 8 terms of 1000, 1100, 1210, … (nearest whole).", f"{1000 * (1.1 ** 8 - 1) / 0.1:,.0f}", ["r = 1.1; S₈ = 1000(1.1⁸ - 1)/0.1."])
for lo, hi, expr, f_ in [(1, 6, "(3k - 2)", lambda k: 3 * k - 2), (1, 5, "2^k", lambda k: 2 ** k), (2, 6, "k(k - 1)", lambda k: k * (k - 1))]:
    tot = sum(f_(k) for k in range(lo, hi + 1))
    B.mc(6, "cp1", f"Evaluate Σ from k = {lo} to {hi} of {expr}.", str(tot), [str(tot - f_(lo)), str(tot + f_(hi + 1)), str(f_(hi))], ["Substitute every k from the lower to the upper limit, then add.", f"Total {tot}."], tags=["misconception"])
B.sel(6, "cp1", "Select ALL sigma expressions equal to 4 + 7 + 10 + 13 + 16.", ["Σ from k = 1 to 5 of (3k + 1)", "Σ from k = 0 to 4 of (3k + 4)", "Σ from k = 2 to 6 of (3k - 2)"], ["Σ from k = 1 to 5 of (3k + 4)", "Σ from k = 1 to 16 of k", "Σ from k = 4 to 16 of 3"], ["Check the first and last terms and the count."])
B.sa(6, "honors", "Find n if Σ from k = 1 to n of (2k - 1) = 225.", "n = 15", ["Sum of the first n odd numbers is n².", "n² = 225."])
B.sa(6, "cp2", "Write out the terms of Σ from k = 1 to 4 of 5k.", "5 + 10 + 15 + 20", ["k = 1, 2, 3, 4."])
for dec_, fr_, a1, r in [("0.333…", F(1, 3), "3/10", "1/10"), ("0.272727…", F(3, 11), "27/100", "1/100"), ("0.8181…", F(9, 11), "81/100", "1/100"), ("1.444…", F(13, 9), "4/10", "1/10")]:
    B.mc(7, "cp1", f"Which fraction equals {dec_}?", fr(fr_), [fr(fr_ + F(1, 10)), fr(F(int(dec_[2:4]), 100)), fr(fr_ * 2)], [f"Repeating part: a₁ = {a1}, r = {r}.", f"S = a₁/(1 - r); total {fr(fr_)}."], tags=["connections"])
for a1, r in [(20, F(1, 4)), (15, F(-1, 2)), (7, F(2, 3))]:
    Ssum = F(a1) / (1 - r); s5 = sum(geom(a1, r, 5))
    st = {f"The series converges": True, f"The sum is {fr(Ssum)}": True, f"S₅ = {fr(s5)}": True, f"The sum is {fr(F(a1) / (1 + r))}": False, "The series diverges": False}
    B.sel(7, "cp1", f"For {lst(geom(a1, r, 3))}, … select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], [f"|r| = {fr(abs(r))} < 1.", f"S = {fr(a1)}/(1 - {frp(r)}) = {fr(Ssum)}."])
B.sa(7, "cp1", "Evaluate Σ from k = 1 to ∞ of 5(0.2)^(k - 1).", "25/4", ["a₁ = 5, r = 0.2: 5/0.8."])
for base, raise_ in [(48000, 2000), (36000, 1800), (55000, 2500)]:
    B.sa(8, "cp1", f"A job pays ${base:,} the first year with a ${raise_:,} raise each year. Find the total earned in 8 years.", f"${8 * (2 * base + 7 * raise_) // 2:,}", [f"Arithmetic series: a₁ = {base}, d = {raise_}, n = 8.", f"S₈ = 8(2·{base} + 7·{raise_})/2."], tags=["modeling"])
for base, pct in [(48000, 4), (36000, 5)]:
    tot = base * ((1 + pct / 100) ** 8 - 1) / (pct / 100)
    B.mc(8, "cp1", f"A job pays ${base:,} the first year with a {pct}% raise each year. About how much is earned in 8 years?", f"${tot:,.0f}", [f"${base * (1 + pct / 100) ** 7:,.0f}", f"${base * 8 * (1 + pct / 100):,.0f}", f"${base * 8:,.0f}"], ["Geometric series a₁ = base, r = 1 + rate, n = 8."], tags=["modeling"])
for start, mult, hrs in [(500, 2, 6), (120, 3, 4)]:
    B.orq(8, "cp1", f"A culture of {start} bacteria multiplies by {mult} every hour.", [("Write an explicit formula for the count after n hours.", f"aₙ = {start}({mult})^n"), (f"Find the count after {hrs} hours.", f"{start * mult ** hrs:,}"),
          ("Is this arithmetic or geometric?", "geometric"), ("After how many whole hours does it first exceed 1,000,000?", str(next(k for k in range(1, 60) if start * mult ** k > 10 ** 6)))],
          [f"Multiply by {mult} each hour.", "Substitute.", "Constant ratio.", "Test powers."], tags=["modeling"])
B.sel(8, "cp1", "A gym membership costs $50 to join plus $25 per month. Select ALL true statements about the total cost Tₙ after n months.", ["Tₙ = 25n + 50", "T₁₂ = $350", "The sequence is arithmetic"], ["Tₙ = 50(25)^n", "T₁₂ = $300", "The sequence is geometric"], ["Constant monthly increase.", "25(12) + 50 = 350."], tags=["modeling"])
B.mc(8, "honors", "A ball dropped from 20 ft rebounds to 80% of its height each bounce. What total distance does it travel before coming to rest?", "180 ft", ["100 ft", "200 ft", "160 ft"], ["Down 20; then up-and-down pairs 2(16 + 12.8 + …) = 2·16/0.2 = 160.", "Total 20 + 160."], tags=["modeling", "challenge"])
B.sa(8, "cp1", "A store stacks boxes: 15 on the bottom row, 13 in the next, decreasing by 2, until 1 on top. How many boxes in total?", "64", ["15, 13, …, 1: 8 terms.", "8(15 + 1)/2."], tags=["modeling"])
B.sa(8, "honors", "A company's sales were $2.0 million in year 1 and grow 6% per year. In which year do cumulative sales first exceed $30 million?", f"year {next(n for n in range(1, 60) if 2 * (1.06 ** n - 1) / 0.06 > 30)}", ["Sₙ = 2(1.06ⁿ - 1)/0.06 > 30.", "Test n."], tags=["modeling"])
B.sa(8, "cp2", "Seats: row 1 has 12, each row adds 3. How many seats in row 8?", "33", ["12 + 7(3)."], tags=["modeling"])

B.orq(8, "honors", "Option A pays $1,000 per day for 30 days. Option B pays 1¢ on day 1 and doubles daily for 30 days.", [("Total for A.", "$30,000"), ("Write the total for B as a series.", "0.01 + 0.02 + 0.04 + … + 0.01(2²⁹)"), ("Total for B.", f"${0.01 * (2 ** 30 - 1):,.2f}"), ("On which day does B's daily pay first exceed $1,000?", f"day {next(n for n in range(1, 31) if 0.01 * 2 ** (n - 1) > 1000)}")],
      ["30·1000.", "Geometric, r = 2.", "0.01(2³⁰ - 1).", "0.01·2ⁿ⁻¹ > 1000."], tags=["modeling", "reasoning"])
B.mc(8, "cp1", "A sequence models a car's value: 24000, 20400, 17340, … Which describes it?", "Geometric with r = 0.85 (15% depreciation)", ["Arithmetic with d = -3600", "Geometric with r = 1.15", "Arithmetic with d = -15%"], ["20400/24000 = 17340/20400 = 0.85.", "Differences are 3600 then 3060 (not constant)."], tags=["modeling", "multiple-representations"])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
