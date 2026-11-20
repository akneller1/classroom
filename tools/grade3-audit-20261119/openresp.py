"""3rd Grade Math audit #4 (2026-11-19): a context-based open-response item for every skill at every level.

Before the audit every Grade 3 open-response item was "Answer each part" or "Match each problem" with four unrelated
drills, and 21 skill/level combinations had none. Each item below is one situation with three computed parts and an
explain-your-thinking part. The existing open-response items are rewritten in place (ID, skill and level kept); the
missing combinations get a new item with an ID ending in -o01. Explanation answers begin "Sample answer:", which the
Grade 3 players self-check (any written answer counts; the sample is shown after). Numbers grow with the level."""
import random, re
from fractions import Fraction as Fr
from lib import ABBR, UNITS, n
import fams
from fams import NAMES, DNAME, Skip, need, qty, rnd, tm

NOTE = ('Original Claude-authored item (family: {fam}). 3rd Grade Math audit 2026-11-19 (#4, open response); answers '
        'recomputed by scripts/test-grade3-audit.cjs; the explanation part is self-checked.')
O = {}
S = 'Sample answer: '
MM, DV, PF, UP, AS, UF, EC, TM, GD, AR, PS = fams.MM, fams.DV, fams.PF, fams.UP, fams.AS, fams.UF, fams.EC, fams.TM, fams.GD, fams.AR, fams.PS


def orq(unit, i):
    def d(f):
        O[f'{unit}-skill-{i:02d}'] = f; return f
    return d


def mixed(x):
    w, p = divmod(x.numerator, x.denominator)
    return str(w) if p == 0 else (f'{w} {p}/{x.denominator}' if w else f'{p}/{x.denominator}')


def lv(r, L, lo, hi):
    """a number from the low, middle or high third of [lo, hi] by level"""
    span = (hi - lo + 1) / 3
    return r.randint(int(lo + span * L), int(lo + span * (L + 1)) - 1 if L < 2 else hi)


# ---------------------------------------------------------------- multiplication meaning
@orq(MM, 1)
def o_mm1(r, L):
    g, k = lv(r, L, 2, 9), r.randint(3, 9)
    return ('mm1_open_baskets', f'A farm stand has {g} baskets. Each basket has {k} peaches.', [
        ('How many groups are there, and how many peaches are in each group?', f'{g} groups of {k}', 'Each basket is one group.'),
        ('Write a multiplication equation for the total.', S + f'{g} × {k} = {g * k}', f'{g} groups of {k} is {g} × {k}.'),
        ('How many peaches are there in all?', qty(g * k, 'peaches'), f'{g} × {k} = {g * k}.'),
        ('Explain how you could check your answer with addition.', S + f'Add {k} a total of {g} times; the sum is {g * k}.', 'Multiplication is repeated addition of equal groups.')])


@orq(MM, 2)
def o_mm2(r, L):
    rows, cols = lv(r, L, 2, 9), r.randint(3, 9); add = r.randint(1, 3)
    return ('mm2_open_garden_array', f'A garden has {rows} rows of plants with {cols} plants in each row.', [
        ('How many plants are in the garden?', qty(rows * cols, 'plants'), f'{rows} × {cols} = {rows * cols}.'),
        (f'If {add} more {"row" if add == 1 else "rows"} of {cols} {"is" if add == 1 else "are"} planted, how many plants will there be?', qty((rows + add) * cols, 'plants'), f'{rows + add} × {cols} = {(rows + add) * cols}.'),
        ('How many plants would be in one column?', qty(rows, 'plants'), f'Each column has one plant from each of the {rows} rows.'),
        ('Explain why turning the array on its side does not change the total.', S + f'The same plants are there, so {rows} × {cols} = {cols} × {rows}.', 'The commutative property.')])


@orq(MM, 3)
def o_mm3(r, L):
    f = [2, 5, 10][L]; a, b = r.randint(2, 9), r.randint(2, 9)
    coin = {2: 'packs of 2 juice boxes', 5: 'packs of 5 pencils', 10: 'packs of 10 stickers'}[f]
    return ('mm3_open_packs', f'A class buys {coin}. Team A gets {a} packs and Team B gets {b} packs.', [
        ('How many items does Team A get?', n(a * f), f'{a} × {f} = {a * f}.'),
        ('How many items does Team B get?', n(b * f), f'{b} × {f} = {b * f}.'),
        ('How many items do the teams get in all?', n((a + b) * f), f'{a * f} + {b * f} = {(a + b) * f}.'),
        (f'Explain a pattern you see when you multiply by {f}.', S + {2: 'Products of 2 are always even.', 5: 'Products of 5 end in 0 or 5.', 10: 'Products of 10 end in 0.'}[f], 'Look at the ones digits.')])


@orq(MM, 4)
def o_mm4(r, L):
    k, e = lv(r, L, 3, 9), r.randint(3, 9); x = r.randint(2, 9)
    return ('mm4_open_bus', f'A school sends {k} vans on a trip. Each van carries {e} students.', [
        ('How many students go on the trip?', qty(k * e, 'students'), f'{k} × {e} = {k * e}.'),
        (f'{x} teachers also go. How many people go in all?', qty(k * e + x, 'people'), f'{k * e} + {x} = {k * e + x}.'),
        ('If one more van of students went, how many students would go?', qty((k + 1) * e, 'students'), f'{k * e} + {e} = {(k + 1) * e}.'),
        ('Explain how you knew to multiply.', S + f'There are {k} equal groups of {e}, so I multiplied.', 'Equal groups mean multiplication.')])

# ---------------------------------------------------------------- division meaning


@orq(DV, 1)
def o_dv1(r, L):
    k, e = lv(r, L, 2, 9), r.randint(3, 9)
    return ('dv1_open_share', f'{k * e} stickers are shared equally among {k} friends.', [
        ('How many stickers does each friend get?', qty(e, 'stickers'), f'{k * e} ÷ {k} = {e}.'),
        ('Write the multiplication fact that checks your answer.', S + f'{k} × {e} = {k * e}', f'{k} friends with {e} each.'),
        ('If one friend gives away 2 stickers, how many does that friend have?', qty(e - 2, 'stickers'), f'{e} − 2 = {e - 2}.'),
        ('Explain what the quotient means in this story.', S + f'It is the number of stickers each friend gets: {e}.', 'Sharing tells the size of each group.')])


@orq(DV, 2)
def o_dv2(r, L):
    s, g = lv(r, L, 2, 9), r.randint(3, 9)
    return ('dv2_open_teams', f'{s * g} players are put into teams of {s}.', [
        ('How many teams are there?', qty(g, 'teams'), f'{s * g} ÷ {s} = {g}.'),
        ('Show the division as repeated subtraction: how many times do you subtract the team size to reach 0?', n(g), f'Subtract {s} a total of {g} times.'),
        (f'If {s} more players join, how many teams can be made?', qty(g + 1, 'teams'), f'{s * g + s} ÷ {s} = {g + 1}.'),
        ('Explain what the quotient means in this story.', S + f'It is the number of teams: {g}.', 'Grouping tells how many groups.')])


@orq(DV, 3)
def o_dv3(r, L):
    a, b = lv(r, L, 2, 10), r.randint(2, 10)
    return ('dv3_open_fact_family', f'A box of {a * b} crayons has {a} crayons in each row.', [
        ('What multiplication fact helps you find the number of rows?', S + f'{a} × {b} = {a * b}', f'Think {a} × ? = {a * b}.'),
        ('How many rows are there?', qty(b, 'rows'), f'{a * b} ÷ {a} = {b}.'),
        ('Write one more division fact from the same fact family.', S + f'{a * b} ÷ {b} = {a}', f'{a}, {b} and {a * b} are a fact family.'),
        ('Explain how multiplication helps you divide.', S + f'Division asks for a missing factor: {a} times what number is {a * b}?', 'Division is an unknown-factor problem.')])


@orq(DV, 4)
def o_dv4(r, L):
    k, e = lv(r, L, 3, 9), r.randint(3, 9); x = r.randint(2, 5)
    return ('dv4_open_bake_sale', f'A bake sale has {k * e} cookies to put on {k} plates equally.', [
        ('How many cookies go on each plate?', qty(e, 'cookies'), f'{k * e} ÷ {k} = {e}.'),
        (f'{x} cookies are added to each plate. How many cookies are on each plate now?', qty(e + x, 'cookies'), f'{e} + {x} = {e + x}.'),
        ('How many cookies are there in all now?', qty(k * (e + x), 'cookies'), f'{k} × {e + x} = {k * (e + x)}.'),
        ('Explain how you chose the operation for the first part.', S + 'The cookies are shared into equal groups, so I divided.', 'Equal sharing is division.')])

# ---------------------------------------------------------------- properties and fact strategies


@orq(PF, 1)
def o_pf1(r, L):
    a, b = lv(r, L, 2, 9), r.randint(3, 9); need(a != b)
    return ('pf1_open_turn_around', f'Ben sets out {a} rows of {b} chairs. Ana sets out {b} rows of {a} chairs.', [
        ('How many chairs does Ben set out?', qty(a * b, 'chairs'), f'{a} × {b} = {a * b}.'),
        ('How many chairs does Ana set out?', qty(a * b, 'chairs'), f'{b} × {a} = {a * b}.'),
        ('How many chairs do they set out in all?', qty(2 * a * b, 'chairs'), f'{a * b} + {a * b} = {2 * a * b}.'),
        ('Explain why both have the same number of chairs.', S + f'Changing the order of the factors does not change the product: {a} × {b} = {b} × {a}.', 'The commutative property.')])


@orq(PF, 2)
def o_pf2(r, L):
    a, b, c = 2, lv(r, L, 2, 9), 5
    return ('pf2_open_boxes', f'There are {b} boxes. Each box has {a} bags, and each bag has {c} marbles.', [
        ('How many marbles are in one box?', qty(a * c, 'marbles'), f'{a} × {c} = {a * c}.'),
        ('How many marbles are in all the boxes?', qty(a * b * c, 'marbles'), f'{b} × {a * c} = {a * b * c}.'),
        ('How many bags are there in all?', qty(a * b, 'bags'), f'{b} × {a} = {a * b}.'),
        ('Explain why multiplying 2 × 5 first makes this easier.', S + f'2 × 5 = 10, and multiplying by 10 is easy: {b} × 10 = {10 * b}.', 'The associative property lets you group factors.')])


@orq(PF, 3)
def o_pf3(r, L):
    a, b = lv(r, L, 3, 9), r.randint(6, 9)
    return ('pf3_open_break_apart', f'A wall has {a} rows of {b} tiles. Kai breaks {b} into 5 + {b - 5}.', [
        (f'What is {a} × 5?', n(a * 5), f'{a} × 5 = {a * 5}.'),
        (f'What is {a} × {b - 5}?', n(a * (b - 5)), f'{a} × {b - 5} = {a * (b - 5)}.'),
        ('How many tiles are on the wall?', qty(a * b, 'tiles'), f'{a * 5} + {a * (b - 5)} = {a * b}.'),
        ('Explain why breaking apart a factor works.', S + f'{a} × {b} is the same as {a} × 5 plus {a} × {b - 5}, because the {b} columns are split into 5 and {b - 5}.', 'The distributive property.')])


@orq(PF, 4)
def o_pf4(r, L):
    k = lv(r, L, 2, 9)
    return ('pf4_open_empty_boxes', f'Mia has {k} boxes. Each box has 1 pencil. Leo has {k} boxes with 0 pencils in each.', [
        ('How many pencils does Mia have?', qty(k, 'pencils'), f'{k} × 1 = {k}.'),
        ('How many pencils does Leo have?', '0', f'{k} × 0 = 0.'),
        (f'If Mia shares her pencils among {k} friends, how many does each get?', qty(1, 'pencils'), f'{k} ÷ {k} = 1.'),
        (f'Explain why 0 ÷ {k} = 0.', S + f'If there are 0 pencils to share among {k} friends, each friend gets 0 pencils.', 'Zero shared is zero each.')])


@orq(PF, 5)
def o_pf5(r, L):
    a = [3, 4, 6, 7, 8, 9][r.randint(0, 2) + 3 * (L == 2)]; b = r.randint(4, 9)
    return ('pf5_open_known_fact', f'Nia knows {a} × {b - 1} = {a * (b - 1)} and wants to find {a} × {b}.', [
        (f'How much more is {a} × {b} than {a} × {b - 1}?', n(a), f'One more group of {a}.'),
        (f'What is {a} × {b}?', n(a * b), f'{a * (b - 1)} + {a} = {a * b}.'),
        (f'What is {a * b} ÷ {a}?', n(b), f'{a} × {b} = {a * b}.'),
        ('Explain another strategy you could use.', S + f'Double a smaller fact, or break {b} into two smaller numbers and add the products.', 'Doubling or breaking apart.')])

# ---------------------------------------------------------------- patterns, unknowns, two-step


@orq(UP, 1)
def o_up1(r, L):
    a, b = lv(r, L, 3, 9), r.randint(2, 9)
    return ('up1_open_unknown', f'A shelf holds {a * b} books in {a} equal stacks. Let s be the number of books in each stack.', [
        ('Write a multiplication equation with s.', S + f'{a} × s = {a * b}', 'Equal stacks.'),
        ('What is s?', n(b), f'{a * b} ÷ {a} = {b}.'),
        ('If there were 2 fewer stacks with the same number in each, how many books would there be?', qty((a - 2) * b, 'books'), f'{a - 2} × {b} = {(a - 2) * b}.'),
        ('Explain how you found the unknown.', S + f'I thought: {a} times what number is {a * b}? That is {b}.', 'Use a related fact.')])


@orq(UP, 2)
def o_up2(r, L):
    k, e = lv(r, L, 3, 9), r.randint(3, 9)
    return ('up2_open_unknown_position', f'{k * e} students sit at tables. There are {e} students at each table.', [
        ('Write an equation with t for the number of tables.', S + f't × {e} = {k * e}', 'The number of tables is unknown.'),
        ('How many tables are there?', qty(k, 'tables'), f'{k * e} ÷ {e} = {k}.'),
        ('If 2 tables leave, how many students are left?', qty((k - 2) * e, 'students'), f'{k - 2} × {e} = {(k - 2) * e}.'),
        ('Explain which number in the story was unknown.', S + 'The number of groups (tables) was unknown.', 'Groups, size or total.')])


@orq(UP, 3)
def o_up3(r, L):
    a, t = lv(r, L, 2, 9), r.randint(2, 9) * 10
    return ('up3_open_tens', f'A theater has {a} rows with {t} seats in each row.', [
        ('How many seats are there?', qty(a * t, 'seats'), f'{a} × {t} = {a} × {t // 10} tens = {a * t}.'),
        (f'How many tens is {a} × {t}?', n(a * t // 10), f'{a} × {t // 10} = {a * t // 10} tens.'),
        ('If 10 seats in each row are closed, how many seats are open?', qty(a * (t - 10), 'seats'), f'{a} × {t - 10} = {a * (t - 10)}.'),
        ('Explain how a basic fact helps you multiply by a multiple of 10.', S + f'{a} × {t // 10} = {a * t // 10}, so {a} × {t} is {a * t // 10} tens, or {a * t}.', 'Think in tens.')])


@orq(UP, 4)
def o_up4(r, L):
    a = lv(r, L, 2, 9)
    xs = [a * k for k in range(1, 6)]
    return ('up4_open_table_pattern', f'Look at the products in the {a}s row of the multiplication table: {", ".join(map(str, xs))}, ...', [
        ('What is the next product?', n(a * 6), f'Add {a}: {xs[-1]} + {a} = {a * 6}.'),
        ('By how much does each product grow?', n(a), f'Each product is {a} more.'),
        (f'What is the 10th product in the row?', n(a * 10), f'{a} × 10 = {a * 10}.'),
        ('Explain a pattern in the ones digits or in even and odd products.', S + ('Every product is even, because the factor is even.' if a % 2 == 0 else 'The products alternate odd and even.'), 'Look at even and odd.')])


@orq(UP, 5)
def o_up5(r, L):
    k, e = lv(r, L, 3, 9), r.randint(3, 9); need(k * e > 15); s = r.randint(10, k * e - 5)
    return ('up5_open_two_step_equation', f'A baker makes {k} trays of {e} rolls and sells {s} rolls. Let r be the number of rolls left.', [
        ('Write one equation for r.', S + f'{k} × {e} − {s} = r', 'Multiply, then subtract.'),
        ('How many rolls were made?', qty(k * e, 'rolls'), f'{k} × {e} = {k * e}.'),
        ('What is r?', n(k * e - s), f'{k * e} − {s} = {k * e - s}.'),
        ('Explain how you know your answer is reasonable.', S + f'About {rnd(k * e, 10)} rolls minus about {rnd(s, 10)} is about {rnd(k * e, 10) - rnd(s, 10)}, close to {k * e - s}.', 'Estimate with rounding.')])


@orq(UP, 6)
def o_up6(r, L):
    p, c = lv(r, L, 3, 9), r.randint(3, 9); bill = ((p * c) // 10 + 1) * 10 + 10 * L
    return ('up6_open_shopping', f'Uma buys {p} books that cost ${c} each. She pays with ${bill}.', [
        ('How much do the books cost?', f'${p * c}', f'{p} × ${c} = ${p * c}.'),
        ('How much change does Uma get?', f'${bill - p * c}', f'${bill} − ${p * c} = ${bill - p * c}.'),
        ('Round the cost to the nearest ten dollars.', f'${rnd(p * c, 10)}', f'${p * c} rounds to ${rnd(p * c, 10)}.'),
        ('Explain how the estimate shows your change is reasonable.', S + f'${bill} − ${rnd(p * c, 10)} is about ${bill - rnd(p * c, 10)}, which is close to ${bill - p * c}.', 'Compare with the estimate.')])

# ---------------------------------------------------------------- add and subtract within 1,000


@orq(AS, 1)
def o_as1(r, L):
    a = lv(r, L, 11, 999); need(a % 10)
    return ('as1_open_round_ten', f'A school collected {a} cans.', [
        ('Round the number of cans to the nearest 10.', n(rnd(a, 10)), f'The ones digit is {a % 10}.'),
        ('What is the greatest number that rounds to the same ten?', n(rnd(a, 10) + 4), f'{rnd(a, 10) + 4} still rounds to {rnd(a, 10)}.'),
        ('What is the least number that rounds to the same ten?', n(rnd(a, 10) - 5), f'{rnd(a, 10) - 5} rounds up to {rnd(a, 10)}.'),
        ('Explain how you rounded.', S + f'I looked at the ones digit. {a % 10} is {"5 or more, so I rounded up" if a % 10 >= 5 else "less than 5, so I rounded down"}.', 'Look at the ones digit.')])


@orq(AS, 2)
def o_as2(r, L):
    a = lv(r, L, 101, 999); need(a % 100 not in (0, 50))
    return ('as2_open_round_hundred', f'A stadium sold {a} tickets.', [
        ('Round the number of tickets to the nearest 100.', n(rnd(a, 100)), f'The tens digit is {a // 10 % 10}.'),
        ('Round the number of tickets to the nearest 10.', n(rnd(a, 10)), f'The ones digit is {a % 10}.'),
        ('How far is the number from the nearest hundred?', n(abs(a - rnd(a, 100))), f'{max(a, rnd(a, 100))} − {min(a, rnd(a, 100))} = {abs(a - rnd(a, 100))}.'),
        ('Explain which digit you look at to round to the nearest 100.', S + 'The tens digit: 5 or more rounds up, less than 5 rounds down.', 'Look one place to the right.')])


@orq(AS, 3)
def o_as3(r, L):
    a, b = lv(r, L, 100, 450), r.randint(100, 450)
    return ('as3_open_reading', f'Class A read {a} pages. Class B read {b} pages.', [
        ('How many pages did both classes read?', qty(a + b, 'pages'), f'{a} + {b} = {a + b}.'),
        ('Estimate the sum by rounding to the nearest 100.', n(rnd(a, 100) + rnd(b, 100)), f'{rnd(a, 100)} + {rnd(b, 100)} = {rnd(a, 100) + rnd(b, 100)}.'),
        ('How many more pages do they need to reach 1,000?', qty(1000 - a - b, 'pages'), f'1,000 − {a + b} = {1000 - a - b}.'),
        ('Explain how you added the hundreds, tens and ones.', S + 'I added each place and regrouped 10 ones as a ten or 10 tens as a hundred when I needed to.', 'Place value and regrouping.')])


@orq(AS, 4)
def o_as4(r, L):
    a, b = lv(r, L, 400, 999), r.randint(100, 399)
    return ('as4_open_seats', f'A theater has {a} seats. {b} seats are filled.', [
        ('How many seats are empty?', qty(a - b, 'seats'), f'{a} − {b} = {a - b}.'),
        ('Write an addition equation that checks your answer.', S + f'{a - b} + {b} = {a}', 'Add the parts.'),
        ('If 50 more people sit down, how many seats are empty?', qty(a - b - 50, 'seats'), f'{a - b} − 50 = {a - b - 50}.'),
        ('Explain when you needed to regroup.', S + 'I regrouped when a digit on top was smaller than the digit below it.', 'Regroup a ten or a hundred.')])


@orq(AS, 5)
def o_as5(r, L):
    a, b = lv(r, L, 120, 480), r.randint(120, 480)
    return ('as5_open_estimate', f'Rosa added {a} + {b}.', [
        ('Round each number to the nearest 100 and add.', n(rnd(a, 100) + rnd(b, 100)), f'{rnd(a, 100)} + {rnd(b, 100)}.'),
        ('Find the exact sum.', n(a + b), f'{a} + {b} = {a + b}.'),
        ('How far is the estimate from the exact sum?', n(abs(rnd(a, 100) + rnd(b, 100) - a - b)), 'Subtract the smaller from the larger.'),
        ('Explain how the estimate helps you check the exact answer.', S + 'If the exact answer is close to the estimate, it is reasonable; if it is far away, I check my work.', 'Compare with the estimate.')])

# ---------------------------------------------------------------- understanding fractions


@orq(UF, 1)
def o_uf1(r, L):
    d = [2, 3, 4, 6, 8][r.randint(0, 2) + L]; d = min(d, 8)
    return ('uf1_open_pizza', f'A pizza is cut into {d} equal slices.', [
        ('What fraction of the pizza is one slice?', f'1/{d}', f'One of {d} equal parts.'),
        ('How many slices make the whole pizza?', n(d), f'{d}/{d} is one whole.'),
        (f'If {d - 1} slices are eaten, what fraction is left?', f'1/{d}', f'{d} − {d - 1} = 1 slice.'),
        ('Explain why the slices must be equal.', S + 'A fraction names equal parts of a whole; unequal pieces are not fourths, sixths and so on.', 'Equal parts.')])


@orq(UF, 2)
def o_uf2(r, L):
    d = [4, 6, 8][L]; k = r.randint(2, d - 1)
    return ('uf2_open_fence', f'A fence has {d} equal sections. Dev paints {k} sections.', [
        ('What fraction of the fence is painted?', f'{k}/{d}', f'{k} of {d} sections.'),
        (f'{k}/{d} is how many copies of 1/{d}?', n(k), f'{k} copies.'),
        ('What fraction is not painted?', f'{d - k}/{d}', f'{d} − {k} = {d - k}.'),
        ('Explain how the painted and unpainted parts make one whole.', S + f'{k}/{d} and {d - k}/{d} together are {d}/{d}, which is 1 whole.', 'The parts make the whole.')])


@orq(UF, 3)
def o_uf3(r, L):
    d = [2, 4, 8][L] if r.random() < .5 else [3, 4, 6][L]
    return ('uf3_open_trail', f'A trail from 0 to 1 mile is marked into {d} equal parts.', [
        ('How long is each part?', f'1/{d} mile', f'1 mile split into {d} equal parts.'),
        ('Where is the first mark after 0?', f'1/{d} mile', 'One part from 0.'),
        ('How many parts do you walk to reach 1 mile?', n(d), f'{d}/{d} = 1.'),
        ('Explain how you split the number line.', S + f'I split the space from 0 to 1 into {d} equal lengths; each length is 1/{d}.', 'Equal lengths.')])


@orq(UF, 4)
def o_uf4(r, L):
    d = [4, 6, 8][L]; k = r.randint(d + 1, 2 * d - 1)
    return ('uf4_open_laps', f'A swim lane is marked in {DNAME[d]} of one lap. Omar swims {k} of those parts.', [
        ('How many laps is that? Write a fraction.', f'{k}/{d} laps', f'{k} parts of size 1/{d}.'),
        ('Is that more or less than 1 lap?', 'more', f'{k} is more than {d}.'),
        ('How many more parts would make 2 laps?', n(2 * d - k), f'2 laps is {2 * d}/{d}; {2 * d} − {k} = {2 * d - k}.'),
        ('Explain how to find the point on a number line.', S + f'Start at 0 and count {k} jumps of 1/{d}.', 'Count equal jumps.')])

# ---------------------------------------------------------------- equivalent and comparing fractions


@orq(EC, 1)
def o_ec1(r, L):
    a, b = [(1, 2), (1, 3), (3, 4)][L]
    return ('ec1_open_strips', f'Two strips are the same size. One shows {a}/{b} shaded. The other is cut into {2 * b} equal parts.', [
        (f'How many of the {2 * b} parts must be shaded to show the same amount?', n(2 * a), f'Each part of the first strip matches 2 small parts.'),
        ('Write the equivalent fraction.', f'{2 * a}/{2 * b}', f'{a}/{b} = {2 * a}/{2 * b}.'),
        (f'If the strip were cut into {4 * b} parts instead, how many would be shaded?', n(4 * a), f'Each part matches 4 small parts.') if 4 * b <= 12 else (f'How many parts are not shaded on the second strip?', n(2 * b - 2 * a), f'{2 * b} − {2 * a}.'),
        ('Explain why the fractions are equal.', S + 'They cover the same amount of the same-size whole.', 'Same size, same point.')])


@orq(EC, 2)
def o_ec2(r, L):
    a, b = [(1, 2), (1, 4), (2, 3)][L]; c = {2: 8, 4: 8, 3: 6}[b]
    return ('ec2_open_recipe', f'A recipe uses {a}/{b} cup of oats. Mia has only a 1/{c} cup scoop.', [
        (f'How many 1/{c} cup scoops equal {a}/{b} cup?', n(a * c // b), f'{a}/{b} = {a * c // b}/{c}.'),
        ('Write the equivalent fraction.', f'{a * c // b}/{c}', f'Multiply the top and bottom by {c // b}.'),
        ('If she doubles the recipe, how many scoops does she need?', n(2 * a * c // b), f'2 × {a * c // b}.'),
        ('Explain why multiplying the top and bottom by the same number keeps the size.', S + 'Each part is cut into the same number of smaller parts, so the shaded amount does not change.', 'Same amount, smaller pieces.')])


@orq(EC, 3)
def o_ec3(r, L):
    w, d = lv(r, L, 2, 6), r.choice([2, 3, 4, 6])
    return ('ec3_open_sandwiches', f'{w} sandwiches are each cut into {d} equal pieces.', [
        ('How many pieces are there?', qty(w * d, 'pieces'), f'{w} × {d} = {w * d}.'),
        ('Write the number of sandwiches as a fraction with that denominator.', f'{w * d}/{d}', f'{w} = {w * d}/{d}.'),
        ('Write the number of sandwiches as a fraction with denominator 1.', f'{w}/1', f'{w} wholes = {w}/1.'),
        ('Explain what the denominator 1 means.', S + f'Each whole is 1 part, so {w}/1 is {w} wholes.', 'One part in each whole.')])


@orq(EC, 4)
def o_ec4(r, L):
    d = [4, 6, 8][L]; a, b = r.sample(range(1, d), 2)
    return ('ec4_open_juice', f'Two same-size bottles: Liam drank {a}/{d} of his and Mei drank {b}/{d} of hers.', [
        ('Who drank more?', 'Liam' if a > b else 'Mei', f'Compare {a} and {b} {DNAME[d]}.'),
        ('Write <, >, or = : ' + f'{a}/{d} ___ {b}/{d}', '>' if a > b else '<', 'Same denominator: compare the numerators.'),
        (f'How many {DNAME[d]} more did that person drink?', n(abs(a - b)), f'{max(a, b)} − {min(a, b)}.'),
        ('Explain why the bottles must be the same size.', S + 'Fractions can only be compared when they are parts of the same size whole.', 'Same whole.')])


@orq(EC, 5)
def o_ec5(r, L):
    a = [1, 2, 3][L]; d1, d2 = r.sample([x for x in (4, 6, 8) if x > a], 2)
    return ('ec5_open_ribbons', f'Two same-size ribbons: Raj used {a}/{d1} of one and Zoe used {a}/{d2} of the other.', [
        ('Who used more ribbon?', 'Raj' if d1 < d2 else 'Zoe', 'Same numerator: fewer parts means bigger parts.'),
        ('Write <, >, or = : ' + f'{a}/{d1} ___ {a}/{d2}', '>' if d1 < d2 else '<', f'{DNAME[min(d1, d2)].capitalize()} are bigger than {DNAME[max(d1, d2)]}.'),
        ('Which is bigger, 1/6 or 1/8?', '1/6', 'Fewer equal parts make bigger parts.'),
        ('Explain how you compared.', S + 'Both used the same number of pieces, so the one with bigger pieces (the smaller denominator) used more.', 'Compare piece sizes.')])

# ---------------------------------------------------------------- time, volume and mass


@orq(TM, 1)
def o_tm1(r, L):
    h, m = r.randint(1, 11), r.randint(1, 11) * 5 + r.randint(1, 4)
    t0 = h * 60 + m
    return ('tm1_open_clock', f'A clock shows {tm(t0)}.', [
        ('How many minutes after the hour is it?', f'{m} minutes', f'{m // 5} × 5 = {m // 5 * 5}, plus {m % 5}.'),
        ('How many minutes until the next hour?', f'{60 - m} minutes', f'60 − {m}.'),
        ('What time will it be 15 minutes later?', tm(t0 + 15), f'{tm(t0)} + 15 minutes.'),
        ('Explain where the hour hand and the minute hand point.', S + f'The hour hand is between the {h} and the {h % 12 + 1}; the minute hand is {m % 5} small marks past the {m // 5}.', 'Count by 5s, then 1s.')])


@orq(TM, 2)
def o_tm2(r, L):
    h = r.randint(1, 10); m = r.randint(0, 40); a, b = r.randint(10, 30), r.randint(10, 20 + 10 * L)
    t0 = h * 60 + m
    return ('tm2_open_afternoon', f'Lena starts homework at {tm(t0)}. Math takes {a} minutes and reading takes {b} minutes.', [
        ('How many minutes does homework take?', f'{a + b} minutes', f'{a} + {b}.'),
        ('What time does Lena finish math?', tm(t0 + a), f'{tm(t0)} + {a} minutes.'),
        ('What time does Lena finish homework?', tm(t0 + a + b), f'{tm(t0 + a)} + {b} minutes.'),
        ('Explain how a number line helps with elapsed time.', S + 'Mark the start time, then jump forward by the minutes, using the next hour as a landmark.', 'Jump to the hour.')])


@orq(TM, 3)
def o_tm3(r, L):
    k, e = lv(r, L, 2, 9), r.randint(2, 9)
    return ('tm3_open_water_jugs', f'A class fills {k} jugs that each hold {e} liters of water.', [
        ('How many liters of water is that?', f'{k * e} liters', f'{k} × {e}.'),
        ('If 3 more liters are added, how many liters are there?', f'{k * e + 3} liters', f'{k * e} + 3.'),
        ('Which unit is best for the water in a bathtub: liters or milliliters?', 'liters', 'A bathtub holds a lot of water.'),
        ('Explain how to read the water level on a container marked in liters.', S + 'Find the line at the top of the water and read the number of liters beside it.', 'Read the scale.')])


@orq(TM, 4)
def o_tm4(r, L):
    w = [10, 20, 50][L]; k = r.randint(2, 9)
    return ('tm4_open_balance', f'A box balances {k} weights of {w} grams each.', [
        ('What is the mass of the box?', f'{k * w} grams', f'{k} × {w}.'),
        ('Two of these boxes are on the scale. How many grams is that?', f'{2 * k * w} grams', f'2 × {k * w}.'),
        ('Which is the best unit for the mass of a car: grams or kilograms?', 'kilograms', 'A car is very heavy.'),
        ('Explain what it means when a balance scale is level.', S + 'Both sides have the same mass.', 'Equal mass.')])


@orq(TM, 5)
def o_tm5(r, L):
    a, b = lv(r, L, 100, 450), r.randint(100, 400)
    return ('tm5_open_crates', f'One crate of apples has a mass of {a} kilograms. Another has a mass of {b} kilograms.', [
        ('What is their total mass?', f'{a + b} kilograms', f'{a} + {b}.'),
        ('How many kilograms heavier is the heavier crate?', f'{abs(a - b)} kilograms', 'Subtract.'),
        ('A truck can carry 1,000 kilograms. How many more kilograms can it carry with both crates on?', f'{1000 - a - b} kilograms', f'1,000 − {a + b}.'),
        ('Explain how you chose to add or subtract.', S + 'To find a total I added; to compare or find how many more, I subtracted.', 'Total or difference.')])

# ---------------------------------------------------------------- graphs and measurement data


@orq(GD, 1)
def o_gd1(r, L):
    s = [2, 5, 10][L]; a, b, c = (r.randint(2, 8) for _ in range(3)); need(len({a, b, c}) == 3)
    return ('gd1_open_picture_graph', f'In a picture graph, each star stands for {s} votes. Dogs have {a} stars, cats have {b} stars and fish have {c} stars.', [
        ('How many votes do dogs have?', f'{a * s} votes', f'{a} × {s}.'),
        ('How many votes are there in all?', f'{(a + b + c) * s} votes', f'{a + b + c} stars × {s}.'),
        ('How many more votes does the top pet have than the bottom pet?', f'{(max(a, b, c) - min(a, b, c)) * s} votes', 'Compare stars, then multiply.'),
        ('Explain how the key helps you read the graph.', S + f'Each star is {s} votes, so I multiply the number of stars by {s}.', 'Use the key.')])


@orq(GD, 2)
def o_gd2(r, L):
    s = [2, 5, 10][L]; a, b = r.randint(2, 9) * s, r.randint(2, 9) * s; need(a != b)
    return ('gd2_open_bar_graph', f'A bar graph has a scale that counts by {s}s. The bar for red ends at {a} and the bar for blue ends at {b}.', [
        ('How many more votes does the taller bar show?', f'{abs(a - b)} votes', 'Subtract.'),
        ('How many votes in all?', f'{a + b} votes', 'Add.'),
        (f'How many jumps of {s} does it take to count up to the end of the red bar?', n(a // s), f'{a} ÷ {s}.'),
        ('Explain why the scale counts by more than 1.', S + 'Counting by a bigger number keeps the bars short enough to fit and easy to read.', 'Scales fit the data.')])


@orq(GD, 3)
def o_gd3(r, L):
    s = [2, 5, 10][L]; xs = [r.randint(1, 9) * s for _ in range(3)]
    return ('gd3_open_make_graph', f'Library books read: Ana {xs[0]}, Ben {xs[1]}, Cruz {xs[2]}. Make a picture graph where each symbol stands for {s} books.', [
        ('How many symbols for Ana?', n(xs[0] // s), f'{xs[0]} ÷ {s}.'),
        ('How many symbols for Ben?', n(xs[1] // s), f'{xs[1]} ÷ {s}.'),
        ('How many symbols in all?', n(sum(xs) // s), 'Add the symbols.'),
        ('Explain how you chose the number of symbols.', S + f'I divided each number by {s}, because each symbol stands for {s} books.', 'Divide by the key.')])


@orq(GD, 4)
def o_gd4(r, L):
    w = r.randint(2, 6); q = [(1, 2), (1, 4), (3, 4)][L]
    return ('gd4_open_ruler', f'A pencil is {w} {q[0]}/{q[1]} inches long.', [
        ('Between which two whole inches is the end of the pencil?', f'{w} and {w + 1}', 'Look at the whole number.'),
        ('How many quarter inches past the whole inch is the end?', n(4 * q[0] // q[1]), f'{q[0]}/{q[1]} = {4 * q[0] // q[1]}/4.'),
        ('How long would two of these pencils be end to end?', mixed(2 * (w + Fr(*q))) + ' inches', 'Add the wholes and the parts.'),
        ('Explain how to measure to the nearest quarter inch.', S + 'Line up the end with 0, then find the closest quarter-inch mark to the other end.', 'Start at 0.')])


@orq(GD, 5)
def o_gd5(r, L):
    vals = [2, 2, 3, 3, 3, 4] if L == 0 else ([1, 1, 2, 2, 2, 3, 3] if L == 1 else [2, 2, 3, 3, 3, 3, 4])
    halves = r.random() < .5
    data = [f'{v} 1/2' if halves and i % 2 else str(v) for i, v in enumerate(vals)]
    from collections import Counter
    c = Counter(data); top = max(c.values()); mode = [k for k, v in c.items() if v == top]
    need(len(mode) == 1)
    return ('gd5_open_line_plot', f'Plant heights in inches: {", ".join(data)}. Make a line plot.', [
        ('How many plants were measured?', n(len(data)), 'Count the data.'),
        ('Which height has the most X marks?', f'{mode[0]} inches', 'Count each value.'),
        ('How many X marks are at that height?', n(top), 'Count the X marks.'),
        ('Explain how you marked the scale of the line plot.', S + ('I marked whole and half inches, because some data are halves.' if halves else 'I marked whole inches, because all the data are whole numbers.'), 'The scale fits the data.')])

# ---------------------------------------------------------------- area


@orq(AR, 1)
def o_ar1(r, L):
    a, b = lv(r, L, 6, 30), r.randint(6, 30); need(a != b)
    return ('ar1_open_tiles', f'Mat A is covered by {a} unit squares with no gaps or overlaps. Mat B is covered by {b} unit squares of the same size.', [
        ('What is the area of mat A?', f'{a} square units', 'Count the unit squares.'),
        ('Which mat has the greater area?', 'A' if a > b else 'B', 'More unit squares.'),
        ('How much greater is it?', f'{abs(a - b)} square units', 'Subtract.'),
        ('Explain why there can be no gaps or overlaps.', S + 'Gaps leave area uncounted and overlaps count some area twice.', 'Cover exactly.')])


@orq(AR, 2)
def o_ar2(r, L):
    u = ['centimeter', 'inch', 'meter'][L]; uu = {'centimeter': 'square centimeters', 'inch': 'square inches', 'meter': 'square meters'}[u]; a, b = r.randint(10, 40), r.randint(5, 20)
    return ('ar2_open_count', f'A shape is covered by {a} squares that are 1 {u} on each side, and another part by {b} more squares of the same size.', [
        ('How many squares cover the whole shape?', n(a + b), 'Add.'),
        ('What is the area?', f'{a + b} {uu}', 'Each square is 1 square unit.'),
        (f'If {min(5, b)} squares are removed, what is the area?', f'{a + b - min(5, b)} {uu}', 'Subtract.'),
        ('Explain why the unit is square ' + u + 's.', S + f'Each tile is a square 1 {u} on each side, so area is counted in square {u}s.', 'Area uses square units.')])


@orq(AR, 3)
def o_ar3(r, L):
    l, w = lv(r, L, 3, 9), r.randint(3, 9)
    return ('ar3_open_rug', f'A rug is {l} feet long and {w} feet wide.', [
        ('What is the area of the rug?', f'{l * w} square feet', f'{l} × {w}.'),
        ('How many rows of 1-foot tiles would cover it?', n(w), f'{w} rows of {l}.'),
        (f'A second rug has the same area and is {w} feet long. How wide is it?', f'{l} feet', f'{l * w} ÷ {w} = {l}.'),
        ('Explain why multiplying gives the same answer as counting tiles.', S + f'There are {w} rows with {l} tiles in each, and {w} × {l} counts them all.', 'Rows times columns.')])


@orq(AR, 4)
def o_ar4(r, L):
    l = lv(r, L, 3, 9); a, b = r.randint(2, 5), r.randint(2, 5)
    return ('ar4_open_two_parts', f'A patio is {l} feet by {a + b} feet. Sam splits the {a + b}-foot side into {a} and {b}.', [
        (f'What is the area of the {l} by {a} part?', f'{l * a} square feet', f'{l} × {a}.'),
        (f'What is the area of the {l} by {b} part?', f'{l * b} square feet', f'{l} × {b}.'),
        ('What is the area of the patio?', f'{l * (a + b)} square feet', f'{l * a} + {l * b}.'),
        ('Explain how this shows the distributive property.', S + f'{l} × {a + b} = {l} × {a} + {l} × {b}.', 'Break apart a side.')])


@orq(AR, 5)
def o_ar5(r, L):
    l1, w1, l2, w2 = lv(r, L, 3, 9), r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
    return ('ar5_open_L_shape', f'An L-shaped room is made of a {l1} by {w1} rectangle and a {l2} by {w2} rectangle that do not overlap.', [
        ('What is the area of the first rectangle?', f'{l1 * w1} square units', f'{l1} × {w1}.'),
        ('What is the area of the second rectangle?', f'{l2 * w2} square units', f'{l2} × {w2}.'),
        ('What is the area of the room?', f'{l1 * w1 + l2 * w2} square units', 'Add the parts.'),
        ('Explain another way to split the room.', S + 'Split it the other way into two different rectangles; the total area is the same.', 'Different splits give the same area.')])

# ---------------------------------------------------------------- perimeter and shapes


@orq(PS, 1)
def o_ps1(r, L):
    l, w = lv(r, L, 3, 20), r.randint(3, 15); need(l != w)
    return ('ps1_open_fence', f'A garden is {l} feet long and {w} feet wide.', [
        ('What is the perimeter?', f'{2 * (l + w)} feet', f'{l} + {w} + {l} + {w}.'),
        ('Fence costs $2 a foot. How much does fence for the whole garden cost?', f'${4 * (l + w)}', f'{2 * (l + w)} × $2.'),
        ('What is the area?', f'{l * w} square feet', f'{l} × {w}.'),
        ('Explain the difference between perimeter and area.', S + 'Perimeter is the distance around; area is the space inside.', 'Around versus inside.')])


@orq(PS, 2)
def o_ps2(r, L):
    a, b, c = lv(r, L, 3, 12), r.randint(3, 12), r.randint(3, 12); d = r.randint(3, 12); P = a + b + c + d
    return ('ps2_open_unknown_side', f'A four-sided garden has a perimeter of {P} feet. Three sides are {a}, {b} and {c} feet.', [
        ('What is the sum of the three known sides?', f'{a + b + c} feet', 'Add.'),
        ('How long is the fourth side?', f'{d} feet', f'{P} − {a + b + c}.'),
        ('If the fourth side were 2 feet longer, what would the perimeter be?', f'{P + 2} feet', 'Add 2.'),
        ('Explain how you found the missing side.', S + 'I added the known sides and subtracted from the perimeter.', 'Subtract the known sides.')])


@orq(PS, 3)
def o_ps3(r, L):
    P = [12, 16, 20][L]; s = P // 2
    pairs = [(a, s - a) for a in range(1, s // 2 + 1)]
    best = max(a * b for a, b in pairs)
    return ('ps3_open_pen', f'Cora has {P} feet of fence to make a rectangular pen with whole-number sides.', [
        ('How many different rectangles can she make?', n(len(pairs)), ', '.join(f'{a} by {b}' for a, b in pairs) + '.'),
        ('What is the greatest area she can make?', f'{best} square feet', f'{s // 2} by {s - s // 2}.'),
        ('What is the least area she can make?', f'{s - 1} square feet', f'1 by {s - 1}.'),
        ('Explain why rectangles with the same perimeter can have different areas.', S + 'The same fence can be long and thin or closer to a square; a shape closer to a square holds more space.', 'Same perimeter, different areas.')])


@orq(PS, 4)
def o_ps4(r, L):
    shape = ['square', 'rectangle', 'rhombus'][L]
    facts = {'square': ('4 sides of equal length and 4 right angles', 'yes', 'yes'),
             'rectangle': ('4 right angles and opposite sides equal', 'yes', 'no'),
             'rhombus': ('4 sides of equal length', 'no', 'yes')}[shape]
    return ('ps4_open_quadrilateral', f'Pia draws a {shape}.', [
        ('How many vertices (corners) does it have?', '4', 'It is a quadrilateral.'),
        ('Is it always a rectangle? (yes or no)', facts[1], 'Rectangles have 4 right angles.'),
        ('Is it always a rhombus? (yes or no)', facts[2], 'A rhombus has 4 equal sides.'),
        ('Explain what makes it a quadrilateral.', S + f'It is a closed shape with 4 straight sides; a {shape} has {facts[0]}.', 'Four sides.')])


@orq(PS, 5)
def o_ps5(r, L):
    tot = [12, 24, 36][L]; p = r.choice([d for d in (2, 3, 4, 6) if tot % d == 0]); x = r.randint(1, p - 1)
    return ('ps5_open_split', f'A rectangle made of {tot} unit squares is split into {p} parts with equal area. {x} {"part is" if x == 1 else "parts are"} shaded.', [
        ('How many unit squares are in each part?', n(tot // p), f'{tot} ÷ {p}.'),
        ('What fraction of the rectangle is each part?', f'1/{p}', f'{p} equal parts.'),
        ('How many unit squares are shaded?', n(tot // p * x), f'{x} × {tot // p}.'),
        ('Explain why parts with different shapes can still be equal parts.', S + 'Equal parts need the same area, not the same shape.', 'Same area.')])


def run(o):
    for u in UNITS:
        for skill in sorted(k for k in O if k.startswith(u + '-skill-')):
            items = [q for q in o.items(u) if q['skillId'] == skill]
            std = max((q['standards'] for q in items), key=lambda s: sum(1 for q in items if q['standards'] == s))
            for li, L in enumerate(['cp2', 'cp1', 'honors']):
                r = random.Random(f'g3-open|{skill}|{L}')
                for _ in range(500):
                    try:
                        fam, prompt, parts = O[skill](r, li)
                        break
                    except (Skip, StopIteration, ValueError, ZeroDivisionError, IndexError):
                        continue
                else:
                    raise SystemExit('no open item for ' + skill)
                assert len(parts) == 4
                # equations, expressions and lists have more than one right form: the players self-check them
                parts = [(p, a if a.startswith(S) or not re.search(r'[=×+−]|; ', a) else S + a, st) for p, a, st in parts]
                fields = {'prompt': prompt, 'parts': [{'prompt': p, 'answer': a} for p, a, _ in parts],
                          'answer': '; '.join(f'({chr(97 + i)}) {a}' for i, (_, a, _) in enumerate(parts)),
                          'solutionSteps': [f'({chr(97 + i)}) {s}' for i, (_, _, s) in enumerate(parts)], 'standards': std,
                          'sourceNotes': NOTE.format(fam=fam)}
                meta = {'questionType': 'explain', 'tags': ['open-response'], 'explanation': parts[2][2]}
                old = [q for q in items if q['level'] == L and q['format'] == 'open-response']
                if old:
                    o.edit(old[0]['id'], **fields)
                    o.meta_set(old[0]['id'], **meta)
                else:
                    q = dict({'id': f'm3-{ABBR[u]}-s{skill[-2:]}-{L}-o01', 'skillId': skill, 'level': L, 'format': 'open-response'}, **fields)
                    o.add(u, q, meta)
