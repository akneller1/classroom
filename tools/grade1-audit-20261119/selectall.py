"""1st Grade Math audit #8 (2026-11-19): on-skill select-all items with 2, 3 or 4 correct choices.

Before the audit all 126 Grade 1 select-all items used one template ("Select ALL the problems that are matched with
the correct answer") and had exactly 2 of 4 correct. Each is rewritten in place (ID, skill and level kept) with 5
choices from the skill itself, the number correct cycling 2, 3, 4."""
import random
from lib import UNITS
import fams
from fams import Skip, need

NOTE = ('Original Claude-authored item (family: {fam}). 1st Grade Math audit 2026-11-19 (#8, select-all with {k} correct); '
        'every choice recomputed by scripts/test-grade1-audit.cjs.')
G = {}
AT, AS, WP, EQ, CN, TO, CM, AH, ML, TT, DT, SH = (fams.AT, fams.AS, fams.WP, fams.EQ, fams.CN, fams.TO, fams.CM, fams.AH, fams.ML, fams.TT, fams.DT, fams.SH)


def sel(unit, i):
    def d(f):
        G[f'{unit}-skill-{i:02d}'] = f; return f
    return d


def pick(r, good, bad, k):
    good, bad = list(dict.fromkeys(good)), [b for b in dict.fromkeys(bad) if b not in good]
    need(len(good) >= k and len(bad) >= 5 - k)
    return r.sample(good, k), r.sample(bad, 5 - k)


def sums(r, t, k, lo=0):
    good = [f'{a} + {t - a}' for a in range(lo, t + 1)]
    bad = [f'{a} + {t - a + d}' for a in range(lo, t) for d in (1, -1) if t - a + d >= 0]
    return pick(r, good, bad, k)


def diffs(r, t, k, top):
    good = [f'{a} − {a - t}' for a in range(t, top + 1)]
    bad = [f'{a} − {a - t + d}' for a in range(t + 1, top + 1) for d in (1, -1) if 0 <= a - t + d <= a]
    return pick(r, good, bad, k)


@sel(AT, 1)
def s_at1(r, L, k):
    t = r.randint(5, 10); g, b = sums(r, t, k)
    return ('at1_select_sum', f'Select ALL the facts that make {t}.', g, b, [f'Add each fact and look for {t}.'])


@sel(AT, 2)
def s_at2(r, L, k):
    t = r.randint(1, 6); g, b = diffs(r, t, k, 10)
    return ('at2_select_difference', f'Select ALL the facts that equal {t}.', g, b, [f'Subtract each fact and look for {t}.'])


@sel(AT, 3)
def s_at3(r, L, k):
    g, b = sums(r, 10, k, 1)
    return ('at3_select_make_ten', 'Select ALL the pairs that make 10.', g, b, ['Add each pair and look for 10.'])


@sel(AT, 4)
def s_at4(r, L, k):
    t = r.randint(6, 10); g, b = sums(r, t, k, 1)
    return ('at4_select_partners', f'Select ALL the number partners for {t}.', g, b, [f'The two parts must add to {t}.'])


@sel(AS, 1)
def s_as1(r, L, k):
    t = r.randint(11, 18); g, b = sums(r, t, k, t - 9)
    return ('as1_select_sum', f'Select ALL the facts that make {t}.', g, b, [f'Add each fact and look for {t}.'])


@sel(AS, 2)
def s_as2(r, L, k):
    t = r.randint(3, 9); g, b = diffs(r, t, k, 18)
    return ('as2_select_difference', f'Select ALL the facts that equal {t}.', g, b, [f'Subtract each fact and look for {t}.'])


@sel(AS, 3)
def s_as3(r, L, k):
    t = r.randint(12, 18); good, bad = [], []
    for a in range(1, 10):
        for b in range(1, 10):
            c = t - a - b
            if 1 <= c <= 9: good.append(f'{a} + {b} + {c}')
            if 1 <= c + 1 <= 9: bad.append(f'{a} + {b} + {c + 1}')
    g, bb = pick(r, good, bad, k)
    return ('as3_select_three_sum', f'Select ALL the sums that equal {t}.', g, bb, [f'Add the three numbers and look for {t}.'])


@sel(AS, 4)
def s_as4(r, L, k):
    a, b = r.randint(3, 9), r.randint(3, 9); need(a != b); s = a + b
    good = [f'{a} + {b} = {s}', f'{b} + {a} = {s}', f'{s} − {a} = {b}', f'{s} − {b} = {a}']
    bad = [f'{a} − {b} = {s}', f'{s} + {a} = {b}', f'{s} − {a} = {a}', f'{b} − {a} = {s}', f'{a} + {s} = {b}']
    g, bb = pick(r, good, bad, k)
    return ('as4_select_family', f'Select ALL the facts in the fact family for {a}, {b} and {s}.', g, bb, [f'The family uses {a} + {b} = {s} and the related facts.'])


@sel(WP, 1)
def s_wp1(r, L, k):
    t = r.randint(8, 15); good, bad = [], []
    for a in range(2, t):
        good.append(f'{a} birds, then {t - a} more come')
        bad.append(f'{a} birds, then {t - a + 1} more come')
    for a in range(t + 1, 21):
        good.append(f'{a} birds, then {a - t} fly away'); bad.append(f'{a} birds, then {a - t + 1} fly away')
    g, bb = pick(r, good, bad, k)
    return ('wp1_select_stories_end', f'Select ALL the stories that end with {t} birds.', g, bb, ['Add when more come; subtract when some fly away.'])


@sel(WP, 2)
def s_wp2(r, L, k):
    t = r.randint(8, 16); g, b = sums(r, t, k, 1)
    return ('wp2_select_parts', f'A jar has {t} crayons, some red and some blue. Select ALL the pairs (red + blue) that could be true.', g, b, [f'The parts must add to {t}.'])


@sel(WP, 3)
def s_wp3(r, L, k):
    d = r.randint(2, 6); good = [f'Ben {a}, Zoe {a + d}' for a in range(2, 14)]; bad = [f'Ben {a}, Zoe {a + d + 1}' for a in range(2, 13)] + [f'Ben {a}, Zoe {a + d - 1}' for a in range(2, 13)]
    g, b = pick(r, good, bad, k)
    return ('wp3_select_compare', f'Zoe has {d} more cars than Ben. Select ALL the pairs that could be true.', g, b, [f'Zoe’s number minus Ben’s number must be {d}.'])


@sel(WP, 4)
def s_wp4(r, L, k):
    t = r.randint(9, 18); b0 = r.randint(2, 6)
    good = [f'___ + {b0} = {t}', f'{t} − {b0} = ___', f'{b0} + ___ = {t}']
    bad = [f'{t} + {b0} = ___', f'___ − {b0} = {t}', f'{b0} − {t} = ___', f'{t} + ___ = {b0}']
    need(k <= 3)
    g, bb = pick(r, good, bad, k)
    return ('wp4_select_equations', f'Some birds were on a tree. {b0} more came. Now there are {t}. Select ALL the equations that match the story.', g, bb, [f'The start is unknown: ___ + {b0} = {t}, so {t} − {b0} = ___.'])


@sel(WP, 5)
def s_wp5(r, L, k):
    t = r.randint(10, 18); good, bad = [], []
    for a in range(1, 9):
        for b in range(1, 9):
            c = t - a - b
            if 1 <= c <= 9: good.append(f'{a} red, {b} blue, {c} green')
            if 2 <= c <= 9: bad.append(f'{a} red, {b} blue, {c - 1} green')
    g, bb = pick(r, good, bad, k)
    return ('wp5_select_three_parts', f'Uma has {t} beads in three colors. Select ALL the groups that could be true.', g, bb, [f'The three colors must add to {t}.'])


@sel(EQ, 1)
def s_eq1(r, L, k):
    good, bad = [], []
    for _ in range(40):
        a, b = r.randint(1, 9), r.randint(1, 9); c = r.randint(1, a + b - 1) if a + b > 1 else 1
        good.append(f'{a} + {b} = {c} + {a + b - c}'); bad.append(f'{a} + {b} = {c} + {a + b - c + 1}')
    g, bb = pick(r, good, bad, k)
    return ('eq1_select_true', 'Select ALL the equations that are true.', g, bb, ['Find the value of each side; a true equation has equal sides.'])


@sel(EQ, 2)
def s_eq2(r, L, k):
    x = r.randint(2, 9); good = [f'{a} + ___ = {a + x}' for a in range(1, 11)] + [f'{a + x} − ___ = {a}' for a in range(1, 11)]
    bad = [f'{a} + ___ = {a + x + 1}' for a in range(1, 10)] + [f'{a + x} − ___ = {a + 1}' for a in range(1, 10)]
    g, b = pick(r, good, bad, k)
    return ('eq2_select_missing_is', f'Select ALL the equations where the missing number is {x}.', g, b, [f'Put {x} in the blank and check.'])


@sel(EQ, 3)
def s_eq3(r, L, k):
    t = r.randint(10, 18); good = [f'{a} + {t - a}' for a in range(2, 10) if t - a <= 9]; bad = [f'{a} + {t - a + 1}' for a in range(2, 10) if t - a + 1 <= 9]
    g, b = pick(r, good, bad, k)
    return ('eq3_select_balance', f'One side of a balance is {t}. Select ALL that make the other side equal.', g, b, [f'Each choice must be worth {t}.'])


@sel(CN, 1)
def s_cn1(r, L, k):
    t = r.randint(3, 9) * 10 + r.randint(1, 9)
    good = [f'{t // 10} tens and {t % 10} ones', f'{t // 10} bags of 10 and {t % 10} more', f'{t // 10 - 1} tens and {t % 10 + 10} ones', f'{t} ones']
    bad = [f'{t % 10} tens and {t // 10} ones', f'{t // 10} tens and {t % 10 + 1} ones', f'{t // 10 + 1} tens and {t % 10} ones', f'{t // 10} bags of 10 and {t % 10 - 1} more', f'{t - 1} ones']
    g, bb = pick(r, good, [x for x in bad if x not in good and t % 10 != t // 10], k)
    return ('cn1_select_same_count', f'Select ALL the ways to show {t} crayons.', g, bb, [f'{t} is {t // 10} tens and {t % 10} ones.'])


@sel(CN, 2)
def s_cn2(r, L, k):
    a = r.randint(20, 105); good = [str(a + i) for i in range(1, 10) if a + i <= 120]; bad = [str(a - i) for i in range(0, 5)] + [str(a + 10 + i) for i in range(1, 4) if a + 10 + i <= 120]
    g, b = pick(r, good, bad, k)
    return ('cn2_select_between', f'Select ALL the numbers you say when you count on from {a} to {a + 9}.', g, b, [f'Count on by ones from {a}.'])


@sel(CN, 3)
def s_cn3(r, L, k):
    W = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']; T = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    v = r.randint(21, 99); need(v % 10 and v // 10 != v % 10)
    good = [str(v), f'{T[v // 10]}-{W[v % 10]}', f'{v // 10} tens and {v % 10} ones', f'{v // 10 * 10} + {v % 10}']
    rv = (v % 10) * 10 + v // 10
    bad = [str(rv), f'{T[v % 10] if v % 10 > 1 else "ten"}-{W[v // 10]}', f'{v % 10} tens and {v // 10} ones', f'{v // 10} + {v % 10}', str(v + 10)]
    g, bb = pick(r, good, bad, k)
    return ('cn3_select_names', f'Select ALL the ways to name {v}.', g, bb, [f'{v} is {T[v // 10]}-{W[v % 10]}: {v // 10} tens and {v % 10} ones.'])


@sel(CN, 4)
def s_cn4(r, L, k):
    t = r.randint(30, 110); good = [f'{t - a} + {a}' for a in range(1, 6)] + [f'{t + a} − {a}' for a in range(1, 6) if t + a <= 120]
    bad = [f'{t - a} + {a + 1}' for a in range(1, 6)] + [f'{t + a} − {a + 1}' for a in range(1, 6) if t + a <= 120]
    g, b = pick(r, good, bad, k)
    return ('cn4_select_count_to', f'Select ALL that equal {t}.', g, b, ['Count on to add; count back to subtract.'])


@sel(TO, 1)
def s_to1(r, L, k):
    t = r.randint(2, 9); good = [f'{t} tens', f'{10 * t} ones', f'{t - 1} tens and 10 ones', f'{10 * t}']
    bad = [f'{t} ones', f'{t + 1} tens', f'{10 * t + 1} ones', f'{t * 100}', f'{t - 1} tens']
    g, b = pick(r, good, bad, k)
    return ('to1_select_tens', f'Select ALL that are equal to {t} tens.', g, b, [f'{t} tens = {10 * t} ones.'])


@sel(TO, 2)
def s_to2(r, L, k):
    good = [str(x) for x in range(11, 20)]; bad = [str(x) for x in (1, 2, 5, 9, 10, 20, 21, 30, 31)]
    g, b = pick(r, good, bad, k)
    return ('to2_select_teen', 'Select ALL the numbers that are 1 ten and some ones (teen numbers from 11 to 19).', g, b, ['Teen numbers are 1 ten and 1 to 9 ones.'])


@sel(TO, 3)
def s_to3(r, L, k):
    s = r.randint(1, 9); good = [str(s + 10 * i) for i in range(1, 10) if s + 10 * i <= 120]; bad = [str(s + 10 * i + 1) for i in range(1, 8)] + [str(s + 5 + 10 * i) for i in range(1, 6)]
    g, b = pick(r, good, bad, k)
    return ('to3_select_tens_count', f'Count by tens from {s}. Select ALL the numbers you say.', g, b, [f'Each number is 10 more; the ones digit stays {s}.'])


@sel(TO, 4)
def s_to4(r, L, k):
    t = r.randint(2, 7); good = [str(10 * t + o) for o in range(0, 10)]; bad = [str(10 * (t + 1) + o) for o in range(0, 4)] + [str(10 * (t - 1) + o) for o in range(5, 10)]
    g, b = pick(r, good, bad, k)
    return ('to4_select_tens_digit', f'Select ALL the numbers that have {t} tens.', g, b, [f'The tens digit must be {t}.'])


@sel(CM, 1)
def s_cm1(r, L, k):
    t = r.randint(25, 85); near = [t + d for d in (-15, -10, -9, -1, 1, 2, 9, 10, 11, 15)]
    g, b = pick(r, [str(x) for x in near if x > t], [str(x) for x in near if x < t], k)
    return ('cm1_select_greater', f'Select ALL the numbers greater than {t}.', g, b, ['Compare the tens first, then the ones.'])


@sel(CM, 2)
def s_cm2(r, L, k):
    good, bad = [], []
    for _ in range(40):
        a, b = r.sample(range(11, 99), 2)
        good.append(f'{a} {">" if a > b else "<"} {b}'); bad.append(f'{a} {"<" if a > b else ">"} {b}')
    g, bb = pick(r, good, bad, k)
    return ('cm2_select_true_compare', 'Select ALL the comparisons that are true.', g, bb, ['The open side faces the greater number.'])


@sel(CM, 3)
def s_cm3(r, L, k):
    t, o = r.randint(2, 8), r.randint(3, 7)
    good = [f'{t}{d}' for d in range(o + 1, 10)]; bad = [f'{t}{d}' for d in range(0, o + 1)]
    g, b = pick(r, good, bad, k)
    return ('cm3_select_digit_greater', f'Select ALL the numbers that are greater than {10 * t + o}.', g, b, [f'The tens are the same, so the ones must be more than {o}.'])


@sel(AH, 1)
def s_ah1(r, L, k):
    t = r.randint(3, 9) * 10 + r.randint(1, 9)
    good = [f'10 more than {t - 10}', f'10 less than {t + 10}', f'{t - 10} + 10', f'{t + 10} − 10', f'{t - 20} + 20']
    bad = [f'10 more than {t}', f'10 less than {t}', f'{t - 10} + 1', f'{t + 1} − 10', f'1 more than {t - 10}']
    g, bb = pick(r, good, bad, k)
    return ('ah1_select_equals', f'Select ALL that equal {t}.', g, bb, ['Adding 10 changes the tens digit by 1.'])


@sel(AH, 2)
def s_ah2(r, L, k):
    t = r.randint(5, 9) * 10; good = [f'{a} + {t - a}' for a in range(10, t, 10)] + [f'{t + a} − {a}' for a in range(10, 100 - t, 10)]
    bad = [f'{a} + {t - a + 10}' for a in range(10, t, 10)] + [f'{a} + {t - a + 1}' for a in range(10, t, 10)]
    g, b = pick(r, good, bad, k)
    return ('ah2_select_tens', f'Select ALL that equal {t}.', g, b, ['Add or subtract the tens.'])


@sel(AH, 3)
def s_ah3(r, L, k):
    t = r.randint(3, 9) * 10 + r.randint(5, 9); good = [f'{t - a} + {a}' for a in range(1, t % 10 + 1)]; bad = [f'{t - a} + {a + 1}' for a in range(1, t % 10 + 1)] + [f'{t - a - 10} + {a}' for a in range(1, 3)]
    g, b = pick(r, good, bad, k)
    return ('ah3_select_sum', f'Select ALL that equal {t}.', g, b, ['Add the ones; the tens stay the same.'])


@sel(AH, 4)
def s_ah4(r, L, k):
    good, bad = [], []
    for _ in range(60):
        a, b = r.randint(21, 89), r.randint(2, 9)
        (good if a % 10 + b >= 10 else bad).append(f'{a} + {b}')
    g, bb = pick(r, good, bad, k)
    return ('ah4_select_new_ten', 'Select ALL the sums where you make a new ten.', g, bb, ['Add the ones; 10 or more ones make a new ten.'])


@sel(AH, 5)
def s_ah5(r, L, k):
    t = r.randint(5, 9) * 10 + r.randint(0, 9); good, bad = [], []
    for a in range(11, t - 10, 7):
        good.append(f'{a} + {t - a}'); bad.append(f'{a} + {t - a + 10}')
    g, bb = pick(r, good, bad, k)
    return ('ah5_select_sum', f'Select ALL that equal {t}.', g, bb, ['Add the tens, then the ones.'])


@sel(ML, 1)
def s_ml1(r, L, k):
    t = r.randint(5, 12); good = [f'{x} cubes' for x in range(t + 1, t + 8)]; bad = [f'{x} cubes' for x in range(2, t + 1)]
    g, b = pick(r, good, bad, k)
    return ('ml1_select_longer', f'A pencil is {t} cubes long. Select ALL the lengths that are longer than the pencil.', g, b, [f'Longer means more than {t} cubes.'])


@sel(ML, 2)
def s_ml2(r, L, k):
    good = ['the ruler is longer than the pencil', 'the pencil is shorter than the ruler', 'the marker is longer than the pencil', 'the ruler is longer than the marker']
    bad = ['the pencil is longer than the ruler', 'the pencil is longer than the marker', 'the marker is longer than the ruler', 'the ruler is shorter than the pencil', 'the ruler is shorter than the marker']
    g, b = pick(r, good, bad, k)
    return ('ml2_select_indirect', 'A pencil is shorter than a marker, and the marker is shorter than a ruler. Select ALL that are true.', g, b, ['Pencil < marker < ruler.'])


@sel(SH, 1)
def s_sh1(r, L, k):
    good = ['4 straight sides', '4 square corners', 'sides that are all the same length', 'a closed shape']
    bad = ['3 sides', 'a curved side', 'an open shape', '5 corners', 'it must be blue']
    g, b = pick(r, good, bad, k)
    return ('sh1_select_square', 'Select ALL that are true of every square.', g, b, ['Color and size do not matter; sides and corners do.'])


@sel(SH, 2)
def s_sh2(r, L, k):
    good = ['cube', 'cone', 'cylinder', 'sphere', 'rectangular prism']; bad = ['circle', 'square', 'triangle', 'rectangle', 'hexagon']
    g, b = pick(r, good, bad, k)
    return ('sh2_select_3d', 'Select ALL the shapes that are three-dimensional (solid).', g, b, ['Solid shapes take up space; flat shapes do not.'])


@sel(SH, 3)
def s_sh3(r, L, k):
    good = ['two triangles make a square', 'two squares make a rectangle', 'two half-circles make a circle', 'four squares make a bigger square']
    bad = ['two circles make a square', 'one triangle makes a square', 'two triangles make a circle', 'three squares make a circle', 'a circle and a square make a triangle']
    g, b = pick(r, good, bad, k)
    return ('sh3_select_compose', 'Select ALL the ways that put shapes together correctly.', g, b, ['Fit the shapes edge to edge with no gaps.'])


@sel(SH, 4)
def s_sh4(r, L, k):
    good = ['2 equal shares are halves', '4 equal shares are fourths', 'one of 2 equal shares is one half', 'one of 4 equal shares is one fourth']
    bad = ['2 equal shares are fourths', '4 equal shares are halves', 'shares can be different sizes', 'one of 4 equal shares is one half', '3 equal shares are fourths']
    g, b = pick(r, good, bad, k)
    return ('sh4_select_shares', 'Select ALL that are true.', g, b, ['Halves are 2 equal shares; fourths are 4 equal shares.'])


@sel(SH, 5)
def s_sh5(r, L, k):
    good = ['one half is bigger than one fourth of the same pie', 'two fourths make one half', 'two halves make a whole', 'four fourths make a whole']
    bad = ['one fourth is bigger than one half of the same pie', 'more shares means bigger shares', 'three halves make a whole', 'two fourths make a whole', 'one fourth is the same as one half']
    g, b = pick(r, good, bad, k)
    return ('sh5_select_bigger_share', 'Select ALL that are true.', g, b, ['Cutting the same whole into more shares makes each share smaller.'])


@sel(TT, 1)
def s_tt1(r, L, k):
    h = r.randint(1, 12); good = [f'{h}:00', f'{h} o\'clock', f'the short hand points to {h}, the long hand to 12']
    bad = [f'{h}:30', f'half past {h}', f'the short hand points to 12, the long hand to {h}' if h != 12 else 'the long hand points to 6', f'{h % 12 + 1}:00', f'{h}:12' if h != 12 else '12:30']
    need(k <= 3)
    g, b = pick(r, good, bad, k)
    return ('tt1_select_hour', f'Select ALL that show {h} o\'clock.', g, b, ['At o\'clock the long hand points to 12.'])


@sel(TT, 3)
def s_tt3(r, L, k):
    h = r.randint(1, 11); good = [f'{h}:30', f'half past {h}', f'30 minutes after {h}:00', f'30 minutes before {h + 1}:00']
    bad = [f'{h}:00', f'half past {h + 1}', f'{h + 1}:30', f'{h}:06', f'30 minutes before {h}:00']
    g, b = pick(r, good, bad, k)
    return ('tt3_select_half_past', f'Select ALL that mean the same time as {h}:30.', g, b, [f'{h}:30 is half past {h}.'])


@sel(DT, 1)
def s_dt1(r, L, k):
    t = r.randint(6, 19); good = [f'{t // 5} bundles of 5 and {t % 5} more', f'{t} marks', f'{t - 5} marks and 1 bundle of 5', f'{t} single marks']
    bad = [f'{t // 5} bundles of 5 and {t % 5 + 1} more', f'{t + 1} marks', f'{t // 5 + 1} bundles of 5', f'{t - 1} marks', f'{t // 5} bundles of 10']
    g, bb = pick(r, good, bad, k)
    return ('dt1_select_tally', f'Select ALL the tallies that show {t}.', g, bb, [f'{t} = {t // 5} fives and {t % 5} more.'])


@sel(DT, 2)
def s_dt2(r, L, k):
    a, b, c = r.sample(range(2, 12), 3); V = {'dogs': a, 'cats': b, 'fish': c}
    st = {f'{x} has more than {y}': V[x] > V[y] for x in V for y in V if x != y}
    st.update({f'{x} and {y} have {V[x] + V[y]} together': True for x in V for y in V if x < y})
    st.update({f'{x} and {y} have {V[x] + V[y] + 1} together': False for x in V for y in V if x < y})
    g, bb = pick(r, [s for s, t in st.items() if t], [s for s, t in st.items() if not t], k)
    return ('dt2_select_graph_true', f'A picture graph shows dogs {a}, cats {b} and fish {c}. Select ALL that are true.', g, bb, ['Count the pictures in each row and check each statement.'])


def run(o):
    i = 0
    for u in UNITS:
        for skill in sorted({q['skillId'] for q in o.items(u)}):
            old = sorted([q for q in o.items(u) if q['skillId'] == skill and q['format'] == 'select-all'], key=lambda q: q['id'])
            if not old:
                continue
            if skill not in G:
                raise SystemExit('no select-all family for ' + skill)
            for q in old:
                li = ['cp2', 'cp1', 'honors'].index(q['level'])
                k = 2 + (i % 3); i += 1
                r = random.Random(f'g1-sel|{q["id"]}')
                for _ in range(3000):
                    try:
                        fam, prompt, good, bad, steps = G[skill](r, li, k)
                        break
                    except (Skip, ValueError, IndexError, ZeroDivisionError):
                        k = 2 + (k - 1) % 3 if _ % 500 == 499 else k
                        continue
                else:
                    raise SystemExit('no select-all item for ' + skill)
                opts = [{'text': t, 'correct': True} for t in good] + [{'text': t, 'correct': False} for t in bad]
                r.shuffle(opts)
                ans = [x['text'] for x in opts if x['correct']]
                steps = steps + ['Correct choices: ' + '; '.join(ans) + '. Not correct: ' + '; '.join(bad) + '.']
                o.edit(q['id'], prompt=prompt, answer=ans, options=opts, solutionSteps=steps, sourceNotes=NOTE.format(fam=fam, k=len(good)))
                o.meta_set(q['id'], questionType='conceptual', tags=['select-all'], explanation=steps[0])
