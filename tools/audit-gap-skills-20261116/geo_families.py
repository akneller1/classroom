"""Geometry gap skills (2026-11-16).

right-triangles-trigonometry: "Law of Sines and Law of Cosines" (G-SRT.D.10, G-SRT.D.11) — first bank items for this unit.
foundations-geometry: "Conditional Statements, Converses, and Biconditionals" (G-CO.C.9), built from statements.json.
"""
import json, math, os
from core import I, Reject, need, ri, g, W, levels, safe_round

TRI = "In △ABC (sides a, b, c are opposite angles A, B, C), "
rad = math.radians


def sides(r, L):
    return (lambda: ri(r, 5, 20)) if L == 0 else (lambda: ri(r, 6, 40)) if L == 1 else (lambda: ri(r, 50, 400) / 10)


def angle(r, lo=25, hi=110):
    return ri(r, lo, hi)


def l_sine_side(r, L):
    A, B = angle(r), angle(r)
    need(A + B <= 150 and A != B)
    a = sides(r, L)()
    b = a * math.sin(rad(B)) / math.sin(rad(A))
    safe_round(b, 1)
    given = f"A = {A}°, B = {B}°, and a = {g(a)}"
    prompt = f"{TRI}{given}. Find b to the nearest tenth."
    ans = f"{b:.1f}"
    wr = [(f"{a * math.sin(rad(A)) / math.sin(rad(B)):.1f}", "set up the proportion upside down, matching a with sin B"), (f"{a * B / A:.1f}", "used the angle measures instead of their sines"), (f"{a * math.cos(rad(B)) / math.cos(rad(A)):.1f}" if A != 90 else f"{a * math.sin(rad(B)):.1f}", "used cosine in place of sine"), (f"{a * math.sin(rad(B)):.1f}", "did not divide by sin A")]
    wr = [(t, w) for t, w in wr if float(t) > 0 and abs(float(t) - b) > 0.3]
    steps = ["Law of Sines: a/sin A = b/sin B.", f"b = {g(a)} · sin {B}° ÷ sin {A}°.", f"b ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="tri", given=dict(A=A, B=B, a=g(a)), find="b", dp=1, show=[given]), "law_sines_side")


def l_sine_aas(r, L):
    levels(L, 1, 2)
    A, B = angle(r), angle(r)
    need(A + B <= 150 and A != B)
    C = 180 - A - B
    need(C != A and C != B)
    c = sides(r, L)()
    a = c * math.sin(rad(A)) / math.sin(rad(C))
    safe_round(a, 1)
    given = f"A = {A}°, B = {B}°, and c = {g(c)}"
    prompt = f"{TRI}{given}. Find a to the nearest tenth."
    ans = f"{a:.1f}"
    wr = [(f"{c * math.sin(rad(A)) / math.sin(rad(B)):.1f}", "paired side c with angle B instead of first finding angle C"), (f"{c * math.sin(rad(C)) / math.sin(rad(A)):.1f}", "set up the proportion upside down"), (f"{c * A / C:.1f}", "used the angle measures instead of their sines"), (f"{c * math.sin(rad(A)):.1f}", "did not divide by sin C")]
    wr = [(t, w) for t, w in wr if abs(float(t) - a) > 0.3]
    steps = [f"Find the third angle: C = 180° − {A}° − {B}° = {C}°.", "Law of Sines: a/sin A = c/sin C.", f"a = {g(c)} · sin {A}° ÷ sin {C}° ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="tri", given=dict(A=A, B=B, c=g(c)), find="a", dp=1, show=[given]), "law_sines_aas")


def l_sine_angle(r, L):
    A = angle(r, 35, 115)
    a = sides(r, L)()
    b = sides(r, L)()
    need(b < a * 0.95)
    s = b * math.sin(rad(A)) / a
    B = math.degrees(math.asin(s))
    safe_round(B, 1)
    given = f"A = {A}°, a = {g(a)}, and b = {g(b)}"
    prompt = f"{TRI}{given}. Find angle B to the nearest tenth of a degree. (Because b < a, angle B is acute.)"
    ans = f"{B:.1f}°"
    inv = a * math.sin(rad(A)) / b
    wr = [(f"{A * b / a:.1f}°", "used a proportion with the angle measure instead of its sine"), (f"{180 - A - B:.1f}°", "found angle C instead of angle B"), (f"{math.degrees(math.asin(inv)):.1f}°" if inv < 1 else f"{180 - B:.1f}°", "set up the proportion upside down" if inv < 1 else "gave the obtuse angle with the same sine")]
    wr = [(t, w) for t, w in wr if abs(float(t[:-1]) - B) > 1]
    steps = ["Law of Sines: sin B / b = sin A / a.", f"sin B = {g(b)} · sin {A}° ÷ {g(a)} ≈ {s:.4f}.", f"B = sin⁻¹({s:.4f}) ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="tri", given=dict(A=A, a=g(a), b=g(b)), find="B", dp=1, show=[given]), "law_sines_angle")


def l_cos_side(r, L):
    C = angle(r, 25, 130)
    need(C != 90)
    a, b = sides(r, L)(), sides(r, L)()
    need(a != b)
    c2 = a * a + b * b - 2 * a * b * math.cos(rad(C))
    c = math.sqrt(c2)
    safe_round(c, 1)
    given = f"a = {g(a)}, b = {g(b)}, and C = {C}°"
    prompt = f"{TRI}{given}. Find c to the nearest tenth."
    ans = f"{c:.1f}"
    wr = [(f"{math.sqrt(a * a + b * b):.1f}", "used the Pythagorean Theorem, which needs a right angle"), (f"{math.sqrt(a * a + b * b + 2 * a * b * math.cos(rad(C))):.1f}", "added 2ab·cos C instead of subtracting"), (f"{c2:.1f}", "did not take the square root"), (f"{math.sqrt(abs(a * a + b * b - a * b * math.cos(rad(C)))):.1f}", "left out the factor 2")]
    steps = ["Law of Cosines: c² = a² + b² − 2ab·cos C.", f"c² = {g(a)}² + {g(b)}² − 2({g(a)})({g(b)})cos {C}° ≈ {c2:.2f}.", f"c ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="tri", given=dict(a=g(a), b=g(b), C=C), find="c", dp=1, show=[given]), "law_cosines_side")


def l_cos_angle(r, L):
    a, b, c = sorted([sides(r, L)(), sides(r, L)(), sides(r, L)()])
    need(a + b > c * 1.08 and a != b and b != c)
    r.shuffle(x := [a, b, c])
    a, b, c = x
    cosC = (a * a + b * b - c * c) / (2 * a * b)
    C = math.degrees(math.acos(cosC))
    Aang = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    Bang = 180 - C - Aang
    safe_round(C, 1)
    need(abs(C - 90) > 0.5)
    given = f"a = {g(a)}, b = {g(b)}, and c = {g(c)}"
    prompt = f"{TRI}{given}. Find angle C to the nearest tenth of a degree."
    ans = f"{C:.1f}°"
    wr = [(f"{Aang:.1f}°", "found angle A; angle C is opposite side c"), (f"{Bang:.1f}°", "found angle B; angle C is opposite side c"), (f"{180 - C:.1f}°", "made a sign error in the numerator, giving the supplement"), (f"{math.degrees(math.asin(min(1, c / (a + b)))):.1f}°", "used a right-triangle ratio in a triangle that is not a right triangle")]
    steps = ["Law of Cosines: cos C = (a² + b² − c²) ÷ (2ab).", f"cos C = ({g(a)}² + {g(b)}² − {g(c)}²) ÷ (2 · {g(a)} · {g(b)}) ≈ {cosC:.4f}.", f"C = cos⁻¹({cosC:.4f}) ≈ {ans}.".replace("-", "−")]
    return I(prompt, ans, steps, wr, dict(k="tri", given=dict(a=g(a), b=g(b), c=g(c)), find="C", dp=1, show=[given]), "law_cosines_angle")


def l_which(r, L):
    kind = r.choice(["SAS", "SSS", "AAS", "ASA", "SSA"])
    s = sides(r, L)
    if kind == "SAS":
        given, gd = f"a = {g(x := s())}, b = {g(y := s())}, and C = {(C := angle(r))}°", None
        gd = dict(a=g(x), b=g(y), C=C)
    elif kind == "SSS":
        x, y = s(), s()
        z = round(abs(x - y) + 0.5 * min(x, y), 1 if L == 2 else 0)
        need(z > 0)
        given, gd = f"a = {g(x)}, b = {g(y)}, and c = {g(z)}", dict(a=g(x), b=g(y), c=g(z))
    elif kind == "AAS":
        A, B = angle(r, 25, 70), angle(r, 25, 70)
        given, gd = f"A = {A}°, B = {B}°, and a = {g(x := s())}", None
        gd = dict(A=A, B=B, a=g(x))
    elif kind == "ASA":
        A, B = angle(r, 25, 70), angle(r, 25, 70)
        given, gd = f"A = {A}°, B = {B}°, and c = {g(x := s())}", None
        gd = dict(A=A, B=B, c=g(x))
    else:
        A = angle(r, 30, 100)
        x = s()
        y = round(x * 0.6, 1 if L == 2 else 0)
        given, gd = f"A = {A}°, a = {g(x)}, and b = {g(y)}", dict(A=A, a=g(x), b=g(y))
    cos = kind in ("SAS", "SSS")
    prompt = f"{TRI}you know {given}. Which law should you use first to find another part of the triangle?"
    ans = "Law of Cosines" if cos else "Law of Sines"
    why = {"SAS": "two sides and the included angle are known, so no side is paired with its opposite angle", "SSS": "three sides are known and no angle is known", "AAS": "side a is paired with its opposite angle A", "ASA": "the third angle C can be found and paired with side c", "SSA": "side a is paired with its opposite angle A"}[kind]
    wr = [("Law of Sines" if cos else "Law of Cosines", f"did not notice that {why}"), ("Pythagorean Theorem", "used a right-triangle tool; the triangle is not given as a right triangle"), ("SOH-CAH-TOA right-triangle ratios", "used right-triangle ratios; the triangle is not given as a right triangle")]
    steps = [f"The given information is {kind}: {why}.", f"Start with the {ans}."]
    return I(prompt, ans, steps, wr, dict(k="whichLaw", given=gd, show=[given]), "law_choice")


APP = [("cos", "Two hikers leave the same campsite. One walks {a} km and the other walks {b} km, and their paths form a {C}° angle. How far apart are the hikers, to the nearest tenth of a kilometer?", "km"),
       ("cos", "A triangular garden has two sides of {a} m and {b} m that meet at a {C}° angle. Find the length of the third side to the nearest tenth of a meter.", "m"),
       ("cos", "Two ships leave a port at the same time. After an hour one has sailed {a} miles and the other {b} miles, on courses that form a {C}° angle. How far apart are the ships, to the nearest tenth of a mile?", "miles"),
       ("sin", "Two rangers at stations A and B, {c} km apart, spot a fire at point C. The angle at A is {A}° and the angle at B is {B}°. How far is the fire from station A, to the nearest tenth of a kilometer?", "km"),
       ("sin", "A surveyor marks points A and B, {c} m apart, on one bank of a river and sights a tree at point C on the other bank. The angle at A is {A}° and the angle at B is {B}°. Find the distance from A to the tree to the nearest tenth of a meter.", "m")]


def l_app(r, L):
    levels(L, 1, 2)
    kind, sent, unit = r.choice(APP)
    s = sides(r, L)
    if kind == "cos":
        a, b, C = s(), s(), angle(r, 30, 130)
        need(a != b and C != 90)
        c2 = a * a + b * b - 2 * a * b * math.cos(rad(C))
        v = math.sqrt(c2)
        safe_round(v, 1)
        prompt = sent.format(a=g(a), b=g(b), C=C)
        wr = [(math.sqrt(a * a + b * b), "used the Pythagorean Theorem, which needs a right angle"), (math.sqrt(a * a + b * b + 2 * a * b * math.cos(rad(C))), "added 2ab·cos C instead of subtracting"), (math.sqrt(abs(a * a + b * b - a * b * math.cos(rad(C)))), "left out the factor 2"), (a + b, "added the two side lengths")]
        steps = ["The two sides and the included angle are known (SAS), so use the Law of Cosines.", f"c² = {g(a)}² + {g(b)}² − 2({g(a)})({g(b)})cos {C}° ≈ {c2:.2f}.", f"c ≈ {v:.1f} {unit}."]
        chk = dict(k="tri", given=dict(a=g(a), b=g(b), C=C), find="c", dp=1, unit=unit, show=[f"{g(a)} {unit.replace('miles', 'miles').split()[0] if unit != 'miles' else 'miles'}", f"{C}° angle"])
    else:
        c, A, B = s(), angle(r, 30, 80), angle(r, 30, 80)
        need(A != B)
        Cc = 180 - A - B
        v = c * math.sin(rad(B)) / math.sin(rad(Cc))   # AC = side b
        safe_round(v, 1)
        prompt = sent.format(c=g(c), A=A, B=B)
        wr = [(c * math.sin(rad(A)) / math.sin(rad(Cc)), "found the distance from B (side a) instead of the distance from A (side b)"), (c * math.sin(rad(B)) / math.sin(rad(A)), "paired the known side with angle A instead of the angle at C"), (c * math.sin(rad(Cc)) / math.sin(rad(B)), "set up the proportion upside down"), (c * math.sin(rad(B)), "did not divide by sin C")]
        steps = [f"The angle at C is 180° − {A}° − {B}° = {Cc}°.", "The distance from A to C is side b, opposite angle B. Law of Sines: b/sin B = c/sin C.", f"b = {g(c)} · sin {B}° ÷ sin {Cc}° ≈ {v:.1f} {unit}."]
        chk = dict(k="tri", given=dict(c=g(c), A=A, B=B), find="b", dp=1, unit=unit, show=[f"{g(c)} {unit} apart", f"angle at A is {A}°", f"angle at B is {B}°"])
    ans = f"{v:.1f} {unit}"
    wr = [(f"{w:.1f} {unit}", why) for w, why in wr if abs(w - v) > 0.15]
    return I(prompt, ans, steps, wr, chk, "law_application")


# ---------------------------------------------------------------- conditional statements
ST = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "statements.json"), encoding="utf-8"))


def cap(s):
    return s[0].upper() + s[1:]


def cond(s, p, q):
    return f"If {s['s']} {p}, then {s['it']} {q}."


def forms(s):
    return dict(original=cond(s, s["p"], s["q"]), converse=cond(s, s["q"], s["p"]), inverse=cond(s, s["np"], s["nq"]), contrapositive=cond(s, s["nq"], s["np"]))


def pick(r):
    i = ri(r, 0, len(ST) - 1)
    return i, ST[i], forms(ST[i])


def k_parts(r, L):
    levels(L, 0)
    i, s, f = pick(r)
    part = r.choice(["hypothesis", "conclusion"])
    hyp, con = f"{s['s']} {s['p']}", f"{s['it']} {s['q']}"
    ans, other = (hyp, con) if part == "hypothesis" else (con, hyp)
    prompt = f"Identify the {part} of the conditional statement: \"{f['original']}\""
    wr = [(other, f"gave the {'conclusion' if part == 'hypothesis' else 'hypothesis'}; the hypothesis follows \"if\" and the conclusion follows \"then\""), (f"{s['s']} {s['np']}" if part == "hypothesis" else f"{s['it']} {s['nq']}", "negated the part instead of copying it"), (f["original"], "copied the whole statement instead of one part")]
    steps = ["In \"If p, then q,\" p is the hypothesis and q is the conclusion.", f"The {part} is \"{ans}.\""]
    return I(prompt, ans, steps, wr, dict(k="cond", sid=i, fam="parts", part=part, show=[f["original"], part]), "conditional_parts")


def related(kind, okL):
    def fn(r, L):
        levels(L, *okL)
        i, s, f = pick(r)
        prompt = f"Write the {kind} of the conditional statement: \"{f['original']}\""
        ans = f[kind]
        whys = {"original": "repeated the original statement", "converse": "switched the hypothesis and conclusion (the converse)", "inverse": "negated both parts without switching them (the inverse)", "contrapositive": "switched and negated both parts (the contrapositive)"}
        wr = [(f[k2], whys[k2]) for k2 in ("converse", "inverse", "contrapositive", "original") if k2 != kind]
        how = {"converse": "Switch the hypothesis and the conclusion.", "inverse": "Negate both the hypothesis and the conclusion.", "contrapositive": "Switch the hypothesis and the conclusion, and negate both."}[kind]
        return I(prompt, ans, [how, ans], wr, dict(k="cond", sid=i, fam=kind, show=[f["original"], kind]), "conditional_" + kind)
    fn.__name__ = "k_" + kind
    return fn


k_converse = related("converse", (0, 1))
k_inverse = related("inverse", (0, 1, 2))
k_contrapositive = related("contrapositive", (1, 2))


def k_equiv(r, L):
    levels(L, 1, 2)
    i, s, f = pick(r)
    prompt = f"Write the related conditional that is always logically equivalent to: \"{f['original']}\""
    ans = f["contrapositive"]
    wr = [(f["converse"], "wrote the converse, which is not always equivalent to the original statement"), (f["inverse"], "wrote the inverse, which is equivalent to the converse, not to the original statement"), (cond(s, s["q"], s["np"]), "switched the parts but negated only one of them")]
    steps = ["A conditional and its contrapositive always have the same truth value.", "Switch the hypothesis and conclusion and negate both.", ans]
    return I(prompt, ans, steps, wr, dict(k="cond", sid=i, fam="equiv", show=[f["original"], "logically equivalent"]), "conditional_equivalent")


def k_truth(r, L):
    i, s, f = pick(r)
    prompt = f"The statement \"{f['original']}\" is true. Is its converse true or false? If it is false, give a counterexample."
    if s["conv"]:
        ans = "True"
        wr = [("False", "assumed the converse of a true statement must be false"), ("False; the converse of a true statement is always false.", "used a rule that does not exist; the converse must be checked on its own"), ("It cannot be determined.", "did not test the converse")]
        steps = [f"Converse: {f['converse']}", "No counterexample exists, so the converse is true."]
    else:
        ans = f"False; counterexample: {s['cx']}."
        wr = [("True", "assumed the converse of a true statement must be true"), ("True; a statement and its converse always have the same truth value.", "confused the converse with the contrapositive"), ("It cannot be determined.", "did not look for a counterexample")]
        steps = [f"Converse: {f['converse']}", f"Counterexample: {s['cx']} fits the hypothesis of the converse but not its conclusion.", "The converse is false."]
    return I(prompt, ans, steps, wr, dict(k="cond", sid=i, fam="truth", show=[f["original"], "converse true or false"]), "converse_truth")


def k_bicond(r, L):
    levels(L, 1, 2)
    i, s, f = pick(r)
    bi = f"{s['s']} {s['p']} if and only if {s['it']} {s['q']}."
    prompt = f"The statement \"{f['original']}\" is true. Can it be rewritten as a true biconditional? If so, write the biconditional."
    if s["conv"]:
        ans = f"Yes; {bi}"
        wr = [("No; the converse is false.", "decided the converse was false without checking"), (f"Yes; {s['s']} {s['np']} if and only if {s['it']} {s['q']}.", "negated the hypothesis"), ("No; a biconditional can never be formed from a conditional.", "used a rule that does not exist")]
        steps = [f"Converse: {f['converse']} This is also true.", "A true conditional with a true converse can be written with \"if and only if.\"", cap(bi)]
    else:
        ans = "No; the converse is false."
        wr = [(f"Yes; {bi}", "did not check the converse"), (f"Yes; {s['s']} {s['q']} if and only if {s['it']} {s['p']}.", "did not check the converse"), ("No; the contrapositive is false.", "gave the wrong reason; the contrapositive of a true statement is always true")]
        steps = [f"Converse: {f['converse']}", f"The converse is false (counterexample: {s['cx']}).", "A biconditional is true only when both the conditional and its converse are true."]
    return I(prompt, ans, steps, wr, dict(k="cond", sid=i, fam="bicond", show=[f["original"], "biconditional"]), "biconditional")


SKILLS = {
    ("geometry", "right-triangles-trigonometry", "Law of Sines and Law of Cosines"): dict(fns=[l_sine_side, l_sine_aas, l_sine_angle, l_cos_side, l_cos_angle, l_which, l_app], stds=["G-SRT.D.10", "G-SRT.D.11"], prefix="geo-rt", new_bank=True),
    ("geometry", "foundations-geometry", "Conditional Statements, Converses, and Biconditionals"): dict(fns=[k_parts, k_converse, k_inverse, k_contrapositive, k_equiv, k_truth, k_bicond], stds=["G-CO.C.9"], prefix="geo-fg"),
}
