"""2nd Grade Math audit #4 (2026-11-19): a context-based open-response item for every skill at every level.

Before the audit every Grade 2 open-response item was "Answer each part" or "Match each problem" with four unrelated
drills, and 8 skill/level combinations had none. Each item below is one situation with three computed parts and an
explain-your-thinking part. Existing open-response items are rewritten in place (ID, skill and level kept); missing
combinations get a new item with an ID ending in -o01. Explanation answers begin "Sample answer:", which the Grade 2
players self-check. Numbers grow with the level."""
import random, re
from lib import ABBR, UNITS, n
import fams
from fams import NAMES, Skip, need, qty, tm

NOTE = ('Original Claude-authored item (family: {fam}). 2nd Grade Math audit 2026-11-19 (#4, open response); answers '
        'recomputed by scripts/test-grade2-audit.cjs; the explanation part is self-checked.')
O = {}
S = 'Sample answer: '
AF, AH, WP, PV, CC, AT, OE, ML, LN, TM, GD, SH = (fams.AF, fams.AH, fams.WP, fams.PV, fams.CC, fams.AT, fams.OE, fams.ML, fams.LN, fams.TM, fams.GD, fams.SH)


def orq(unit, i):
    def d(f):
        O[f'{unit}-skill-{i:02d}'] = f; return f
    return d


def lv(r, L, lo, hi):
    span = (hi - lo + 1) / 3
    return r.randint(int(lo + span * L), int(lo + span * (L + 1)) - 1 if L < 2 else hi)


# ---------------------------------------------------------------- within 20
@orq(AF, 1)
def o_af1(r, L):
    a, b = lv(r, L, 3, 9), r.randint(3, 9)
    return ('af1_open_apples', f'Ben picks {a} apples. Cora picks {b} apples.', [
        ('How many apples do they pick in all?', qty(a + b, 'apples'), f'{a} + {b} = {a + b}.'),
        ('How many more apples would make 20?', qty(20 - a - b, 'apples'), f'20 − {a + b} = {20 - a - b}.'),
        (f'If Ben picks {a} more, how many does Ben have?', qty(2 * a, 'apples'), f'{a} + {a} = {2 * a}.'),
        ('Explain a strategy you used to add.', S + 'I made a ten first, then added the rest.', 'Make a ten or use a double.')])


@orq(AF, 2)
def o_af2(r, L):
    a, b = lv(r, L, 11, 18), r.randint(3, 9)
    need(a - b >= 5)
    return ('af2_open_balloons', f'There are {a} balloons. {b} balloons pop.', [
        ('How many balloons are left?', qty(a - b, 'balloons'), f'{a} − {b} = {a - b}.'),
        ('Write the addition fact that checks your answer.', S + f'{a - b} + {b} = {a}', 'Add the parts.'),
        ('How many more balloons pop if only 5 are left at the end?', qty(a - b - 5, 'balloons') if a - b > 5 else qty(0, 'balloons'), f'{a - b} − 5 = {max(a - b - 5, 0)}.'),
        ('Explain how you subtracted.', S + 'I counted back to 10, then counted back the rest.', 'Go back through ten.')])


@orq(AF, 3)
def o_af3(r, L):
    a, b = lv(r, L, 3, 9), r.randint(3, 9); need(a != b)
    return ('af3_open_fact_family', f'A box has {a} red and {b} blue crayons.', [
        ('How many crayons are in the box?', qty(a + b, 'crayons'), f'{a} + {b} = {a + b}.'),
        (f'If the {a} red crayons are taken out, how many are left?', qty(b, 'crayons'), f'{a + b} − {a} = {b}.'),
        (f'If the {b} blue crayons are taken out, how many are left?', qty(a, 'crayons'), f'{a + b} − {b} = {a}.'),
        ('Explain how the facts are related.', S + f'They use the same three numbers: {a}, {b} and {a + b}.', 'A fact family.')])


@orq(AF, 4)
def o_af4(r, L):
    a, b, c = lv(r, L, 2, 9), r.randint(2, 9), r.randint(2, 9); need(a + b - c > 0 and a + b <= 20)
    return ('af4_open_balance', f'A balance has {a} + {b} cubes on one side and {c} cubes plus some more on the other side.', [
        ('How many cubes are on the first side?', qty(a + b, 'cubes'), f'{a} + {b} = {a + b}.'),
        ('How many more cubes make the sides equal?', qty(a + b - c, 'cubes'), f'{c} + ___ = {a + b}.'),
        ('Write the equation.', S + f'{a} + {b} = {c} + {a + b - c}', 'Both sides are equal.'),
        ('Explain what the equal sign means.', S + 'It means both sides have the same value.', 'Same value.')])

# ---------------------------------------------------------------- within 100


@orq(AH, 1)
def o_ah1(r, L):
    a, b = lv(r, L, 15, 50), r.randint(15, 40); need(a + b <= 100)
    return ('ah1_open_cans', f'Class A collected {a} cans. Class B collected {b} cans.', [
        ('How many cans did they collect in all?', qty(a + b, 'cans'), f'{a} + {b} = {a + b}.'),
        ('How many tens are in the total?', n((a + b) // 10), f'{a + b} has {(a + b) // 10} tens.'),
        ('How many more cans make 100?', qty(100 - a - b, 'cans'), f'100 − {a + b} = {100 - a - b}.'),
        ('Explain how you added the tens and the ones.', S + 'I added the tens, then the ones, and made a new ten when the ones were 10 or more.', 'Place value.')])


@orq(AH, 2)
def o_ah2(r, L):
    a, b = lv(r, L, 40, 99), r.randint(11, 39); need(a > b)
    need(a - b >= 10)
    return ('ah2_open_pages', f'A book has {a} pages. Mia has read {b} pages.', [
        ('How many pages are left?', qty(a - b, 'pages'), f'{a} − {b} = {a - b}.'),
        ('Write the addition that checks your answer.', S + f'{a - b} + {b} = {a}', 'Add back.'),
        ('If Mia reads 10 more pages, how many are left?', qty(a - b - 10, 'pages') if a - b >= 10 else qty(0, 'pages'), f'{a - b} − 10.'),
        ('Explain when you need to trade a ten.', S + 'When there are not enough ones to subtract, I trade 1 ten for 10 ones.', 'Regroup.')])


@orq(AH, 3)
def o_ah3(r, L):
    a, b = lv(r, L, 15, 60), r.randint(11, 39); need(a + b <= 99)
    return ('ah3_open_missing', f'Raj had {a} marbles. After a friend gave him some, he had {a + b}.', [
        ('Write an addition equation with a blank.', S + f'{a} + ___ = {a + b}', 'Start + change = end.'),
        ('How many marbles did the friend give?', qty(b, 'marbles'), f'{a + b} − {a} = {b}.'),
        ('Write a subtraction equation for the same story.', S + f'{a + b} − {a} = {b}', 'Related facts.'),
        ('Explain how addition and subtraction are related.', S + 'Subtraction can find a missing addend.', 'Think addition.')])


@orq(AH, 4)
def o_ah4(r, L):
    xs = [r.randint(11, 30) for _ in range(3 + (L > 0))]; need(sum(xs) <= 100)
    return ('ah4_open_points', f'A team scored {", ".join(map(str, xs[:-1]))} and {xs[-1]} points in {len(xs)} games.', [
        ('How many points did the team score in all?', qty(sum(xs), 'points'), ' + '.join(map(str, xs)) + f' = {sum(xs)}.'),
        ('How many points in the first two games?', qty(xs[0] + xs[1], 'points'), f'{xs[0]} + {xs[1]}.'),
        ('How many more points were scored in the highest game than the lowest?', qty(max(xs) - min(xs), 'points'), 'Subtract.'),
        ('Explain how you chose the order to add.', S + 'I added numbers that make tens first, because order does not change the sum.', 'Make tens.')])


@orq(AH, 5)
def o_ah5(r, L):
    a, b = lv(r, L, 21, 59), r.randint(21, 39); need(a + b <= 99 and b % 10)
    return ('ah5_open_strategies', f'Two friends add {a} + {b} in different ways.', [
        (f'What is {a} + {b // 10 * 10}?', n(a + b // 10 * 10), 'Add the tens first.'),
        (f'What is {a} + {b}?', n(a + b), f'Then add {b % 10}.'),
        (f'What is {b} + {a}?', n(a + b), 'Order does not change the sum.'),
        ('Explain why both ways give the same sum.', S + 'Both ways add the same tens and ones, just in a different order.', 'Same parts.')])

# ---------------------------------------------------------------- word problems


@orq(WP, 1)
def o_wp1(r, L):
    a, b, c = lv(r, L, 20, 60), r.randint(10, 30), r.randint(5, 15); need(a + b - c > 0 and a + b <= 100)
    need(b > c)
    return ('wp1_open_bus', f'A bus has {a} people. {b} people get on.', [
        ('How many people are on the bus now?', qty(a + b, 'people'), f'{a} + {b}.'),
        (f'Then {c} people get off. How many are on the bus?', qty(a + b - c, 'people'), f'{a + b} − {c}.'),
        ('How many more people got on than got off?', qty(b - c, 'people') if b > c else qty(0, 'people'), 'Subtract.'),
        ('Explain how you know to add or subtract.', S + 'People getting on adds to the group; people getting off takes away.', 'Add to, take from.')])


@orq(WP, 2)
def o_wp2(r, L):
    a, b = lv(r, L, 15, 45), r.randint(15, 45)
    need(a != b)
    return ('wp2_open_club', f'A club has {a} girls and {b} boys.', [
        ('How many children are in the club?', qty(a + b, 'children'), f'{a} + {b}.'),
        ('Are there more girls or more boys?', 'girls' if a > b else 'boys' if b > a else 'same', 'Compare.'),
        ('How many more?', n(abs(a - b)), 'Subtract.'),
        ('Explain which numbers are the parts and which is the whole.', S + f'{a} and {b} are the parts; {a + b} is the whole.', 'Put together.')])


@orq(WP, 3)
def o_wp3(r, L):
    a, d = lv(r, L, 15, 60), r.randint(5, 30); need(a + d <= 99)
    return ('wp3_open_compare', f'Eli has {a} cards. Lena has {d} more cards than Eli.', [
        ('How many cards does Lena have?', qty(a + d, 'cards'), f'{a} + {d}.'),
        ('How many cards do they have in all?', qty(2 * a + d, 'cards') if 2 * a + d <= 100 else qty(2 * a + d, 'cards'), f'{a} + {a + d}.'),
        ('How many fewer cards does Eli have than Lena?', qty(d, 'cards'), 'The difference.'),
        ('Explain what "more than" tells you.', S + 'It tells the difference between the two amounts.', 'Compare.')])


@orq(WP, 4)
def o_wp4(r, L):
    a, b, c = lv(r, L, 20, 50), r.randint(10, 30), r.randint(5, 20); need(a + b - c > 0)
    return ('wp4_open_two_step', f'Uma had {a} stickers. She got {b} more and then gave away {c}.', [
        ('How many stickers did Uma have after she got more?', qty(a + b, 'stickers'), f'{a} + {b}.'),
        ('How many does she have now?', qty(a + b - c, 'stickers'), f'{a + b} − {c}.'),
        ('Write one equation with a letter for the stickers now.', S + f'{a} + {b} − {c} = s', 'Two steps.'),
        ('Explain how you checked your answer.', S + f'I added {c} back to {a + b - c} to get {a + b}.', 'Work backward.')])

# ---------------------------------------------------------------- place value


@orq(PV, 1)
def o_pv1(r, L):
    t = lv(r, L, 11, 59)
    return ('pv1_open_bundles', f'Sam bundles sticks into tens. He has {t} bundles.', [
        ('How many sticks does Sam have?', n(t * 10), f'{t} tens = {t * 10}.'),
        ('How many hundreds can he make?', n(t // 10), '10 tens make 1 hundred.'),
        ('How many tens are left over?', n(t % 10), f'{t} − {t // 10 * 10} = {t % 10}.'),
        ('Explain why 10 tens is 1 hundred.', S + '10 groups of 10 is 100.', 'Bundle tens.')])


@orq(PV, 2)
def o_pv2(r, L):
    h, t, o = lv(r, L, 1, 9), r.randint(0, 9), r.randint(1, 9); v = h * 100 + t * 10 + o
    need(v + 10 <= 999)
    return ('pv2_open_blocks', f'Ava builds a number with {h} hundreds, {t} tens and {o} ones.', [
        ('What is the number?', n(v), f'{h * 100} + {t * 10} + {o}.'),
        ('What number is 10 more?', n(v + 10), 'Add a ten.'),
        ('What number is 1 less?', n(v - 1), 'Take away a one.'),
        ('Explain what each digit tells you.', S + 'The first digit is hundreds, the next is tens and the last is ones.', 'Place value.')])


@orq(PV, 3)
def o_pv3(r, L):
    s = lv(r, L, 1, 5) * 100
    return ('pv3_open_count_hundreds', f'Max counts by hundreds starting at {s}.', [
        ('What are the next three numbers?', S + f'{s + 100}, {s + 200}, {s + 300}', 'Add 100 each time.'),
        ('How many hundreds is the third number?', n((s + 300) // 100), f'{s + 300} = {(s + 300) // 100} hundreds.'),
        ('How many more hundreds to reach 1,000?', n(10 - (s + 300) // 100), f'1,000 is 10 hundreds.'),
        ('Explain what changes when you count by hundreds.', S + 'Only the hundreds digit changes; it goes up by 1.', 'Hundreds digit.')])


@orq(PV, 4)
def o_pv4(r, L):
    h, t, o = lv(r, L, 1, 9), r.randint(1, 9), r.randint(1, 9); v = h * 100 + t * 10 + o
    return ('pv4_open_check', f'A check is written for {v} dollars.', [
        ('Write the number in expanded form.', S + f'{h * 100} + {t * 10} + {o}', 'Value of each digit.'),
        ('What is the value of the tens digit?', n(t * 10), f'{t} tens.'),
        ('What is the value of the hundreds digit?', n(h * 100), f'{h} hundreds.'),
        ('Explain how you would write the number name.', S + 'Say the hundreds, then the tens and ones, like "two hundred thirty-four".', 'Number names.')])

# ---------------------------------------------------------------- count and compare


@orq(CC, 1)
def o_cc1(r, L):
    a = lv(r, L, 100, 990)
    need(a + 5 <= 999)
    return ('cc1_open_tickets', f'Tickets are numbered in order. The first ticket today is {a}.', [
        ('What is the next ticket number?', n(a + 1), 'Count on 1.'),
        ('What ticket number comes just before?', n(a - 1), 'Count back 1.'),
        ('What is the ticket number 5 after the first?', n(a + 5), 'Count on 5.'),
        ('Explain what happens after a number ending in 9.', S + 'The ones go back to 0 and the tens go up by 1.', 'Make a ten.')])


@orq(CC, 2)
def o_cc2(r, L):
    step = [5, 10, 100][L]; s = r.randint(1, 5) * step
    return ('cc2_open_skip', f'Kai skip counts by {step}s, starting at {s}.', [
        ('What are the next three numbers?', S + ', '.join(str(s + step * i) for i in (1, 2, 3)), f'Add {step} each time.'),
        ('What is the sixth number he says after the start?', n(s + 6 * step), f'{s} + 6 × {step}.'),
        (f'How many jumps of {step} from {s} to {s + 8 * step}?', n(8), 'Count the jumps.'),
        ('Explain a pattern in the numbers.', S + {5: 'The ones digits go 5, 0, 5, 0.', 10: 'The ones digit stays the same and the tens go up by 1.', 100: 'Only the hundreds digit changes.'}[step], 'Look at the digits.')])


@orq(CC, 3)
def o_cc3(r, L):
    h = lv(r, L, 1, 8); a, b = h * 100 + r.randint(10, 99), h * 100 + r.randint(10, 99); need(a != b)
    return ('cc3_open_compare', f'Two schools: Oak has {a} students and Pine has {b} students.', [
        ('Which school has more students?', 'Oak' if a > b else 'Pine', 'Compare tens, then ones.'),
        (f'Write >, = or < : {a} ___ {b}', '>' if a > b else '<', 'Compare.'),
        ('How many more students does that school have?', n(abs(a - b)), 'Subtract.'),
        ('Explain which place you compared first.', S + 'The hundreds are the same, so I compared the tens (then the ones).', 'Compare from the left.')])


@orq(CC, 4)
def o_cc4(r, L):
    a = lv(r, L, 120, 880)
    return ('cc4_open_ten_hundred', f'A score board shows {a} points.', [
        ('What is 10 more?', n(a + 10), 'The tens digit goes up by 1.'),
        ('What is 100 less?', n(a - 100), 'The hundreds digit goes down by 1.'),
        ('What is 10 less than 100 more?', n(a + 90), f'{a + 100} − 10.'),
        ('Explain which digit changes when you add 10.', S + 'The tens digit, unless it is 9 and a new hundred is made.', 'Tens digit.')])

# ---------------------------------------------------------------- within 1,000


@orq(AT, 1)
def o_at1(r, L):
    a, b = lv(r, L, 120, 450), r.randint(110, 450); need(a + b <= 999)
    return ('at1_open_blocks', f'Pia adds {a} + {b} with base-ten blocks.', [
        ('How many hundreds in all?', n(a // 100 + b // 100), 'Add the hundreds.'),
        ('How many tens in all?', n(a // 10 % 10 + b // 10 % 10), 'Add the tens.'),
        ('What is the sum?', n(a + b), f'{a} + {b}.'),
        ('Explain when you need to trade.', S + 'When there are 10 or more ones or tens, I trade 10 for 1 of the next place.', 'Regroup.')])


@orq(AT, 2)
def o_at2(r, L):
    a, b = lv(r, L, 150, 480), r.randint(150, 480); need(a + b <= 999)
    return ('at2_open_tickets', f'A fair sold {a} tickets on Friday and {b} tickets on Saturday.', [
        ('How many tickets were sold in all?', qty(a + b, 'tickets'), f'{a} + {b}.'),
        ('How many more tickets to reach 1,000?', qty(1000 - a - b, 'tickets'), f'1,000 − {a + b}.'),
        ('Which day sold more tickets?', 'Friday' if a > b else 'Saturday', 'Compare.') if a != b else ('How many more on Friday?', '0', 'Same.'),
        ('Explain how you added.', S + 'I added hundreds, tens and ones and made a new ten or hundred when needed.', 'Place value.')])


@orq(AT, 3)
def o_at3(r, L):
    a, b = lv(r, L, 300, 950), r.randint(110, 290)
    need(a - b >= 100)
    return ('at3_open_seats', f'A theater has {a} seats. {b} seats are filled.', [
        ('How many seats are empty?', qty(a - b, 'seats'), f'{a} − {b}.'),
        ('Write the addition that checks your answer.', S + f'{a - b} + {b} = {a}', 'Add back.'),
        ('If 100 more people sit, how many seats are empty?', qty(a - b - 100, 'seats') if a - b >= 100 else qty(0, 'seats'), 'Subtract 100.'),
        ('Explain how you could count up to subtract.', S + f'Start at {b}, count up to the next hundred, then to {a}.', 'Count up.')])


@orq(AT, 4)
def o_at4(r, L):
    a = lv(r, L, 3, 9) * 100; b = r.randint(110, a - 50)
    return ('at4_open_zeros', f'A farm has {a} eggs. {b} eggs are sold.', [
        ('How many eggs are left?', qty(a - b, 'eggs'), f'{a} − {b}.'),
        ('How many hundreds did you trade?', n(1), 'Trade 1 hundred for 10 tens.'),
        ('How many eggs were sold and left in all?', qty(a, 'eggs'), 'The whole.'),
        ('Explain how to subtract across zeros.', S + 'Trade a hundred for 10 tens, then a ten for 10 ones, then subtract.', 'Regroup.')])

# ---------------------------------------------------------------- odd, even, arrays


@orq(OE, 1)
def o_oe1(r, L):
    k = lv(r, L, 5, 20)
    return ('oe1_open_partners', f'{k} children line up in pairs.', [
        ('Is the number of children odd or even?', 'even' if k % 2 == 0 else 'odd', 'Can they all pair up?'),
        ('How many pairs are there?', n(k // 2), f'{k} ÷ 2 pairs.'),
        ('How many children have no partner?', n(k % 2), 'Odd leaves one.'),
        ('Explain how you know if a number is even.', S + 'It can be split into two equal groups, or it ends in 0, 2, 4, 6 or 8.', 'Pairs.')])


@orq(OE, 2)
def o_oe2(r, L):
    d = lv(r, L, 2, 10)
    return ('oe2_open_doubles', f'Nia has {2 * d} socks. She makes two equal piles.', [
        ('How many socks are in each pile?', qty(d, 'socks'), f'{d} + {d} = {2 * d}.'),
        ('Write the doubles fact.', S + f'{d} + {d} = {2 * d}', 'Two equal addends.'),
        ('If she had 1 more sock, could she still make equal piles? (yes or no)', 'no', f'{2 * d + 1} is odd.'),
        ('Explain why a doubles fact always gives an even number.', S + 'Two equal groups can always be paired up.', 'Even numbers.')])


@orq(OE, 3)
def o_oe3(r, L):
    rows, cols = lv(r, L, 2, 5), r.randint(2, 5)
    return ('oe3_open_array', f'Desks are in {rows} rows with {cols} desks in each row.', [
        ('Write a repeated addition for the desks.', S + ' + '.join([str(cols)] * rows), 'Add each row.'),
        ('How many desks are there?', qty(rows * cols, 'desks'), 'Add.'),
        ('How many desks are in each column?', qty(rows, 'desks'), 'One per row.'),
        ('Explain another way to count the desks.', S + f'Add the columns: {" + ".join([str(rows)] * cols)} = {rows * cols}.', 'Columns.')])


@orq(OE, 4)
def o_oe4(r, L):
    rows, cols = lv(r, L, 2, 5), r.randint(2, 5); x = r.randint(1, rows * cols - 1)
    return ('oe4_open_garden', f'A garden has {rows} rows of {cols} plants. {x} plants have flowers.', [
        ('How many plants are there?', qty(rows * cols, 'plants'), 'Repeated addition.'),
        ('How many plants have no flowers?', qty(rows * cols - x, 'plants'), 'Subtract.'),
        ('If one more row is planted, how many plants are there?', qty((rows + 1) * cols, 'plants'), f'Add {cols}.'),
        ('Explain how the array helps you count.', S + 'Every row has the same number, so I can add the same number again and again.', 'Equal rows.')])

# ---------------------------------------------------------------- measuring length


@orq(ML, 1)
def o_ml1(r, L):
    a = lv(r, L, 3, 11)
    return ('ml1_open_ruler', f'A crayon’s end lines up with 0 on a ruler. The other end is at {a} inches.', [
        ('How long is the crayon?', qty(a, 'inches'), 'Read the ruler.'),
        (f'If the crayon started at 2 instead, where would the other end be?', qty(a + 2, 'inches'), 'Add 2.'),
        ('How much shorter is it than 12 inches?', qty(12 - a, 'inches'), 'Subtract.'),
        ('Explain why you line up the end with 0.', S + 'So you count every unit from the start of the object.', 'Start at 0.')])


@orq(ML, 2)
def o_ml2(r, L):
    obj, unit, tool = [('book', 'inches', 'ruler'), ('room', 'feet', 'yardstick'), ('hallway', 'meters', 'meter stick')][L]
    return ('ml2_open_tool', f'Sam wants to measure the length of a {obj}.', [
        ('Which unit is best: inches, feet or meters?', unit, 'Match the unit to the size.'),
        ('Which tool is best: ruler, yardstick or meter stick?', tool, 'Match the tool.'),
        ('Would a measuring tape also work? (yes or no)', 'yes', 'A tape measures many lengths.'),
        ('Explain why the unit should fit the object.', S + 'A unit that is too small takes too many to count; one too big is not exact.', 'Fit the unit.')])


@orq(ML, 3)
def o_ml3(r, L):
    a = lv(r, L, 2, 6)
    return ('ml3_open_two_units', f'A table is {a} feet long.', [
        ('How many inches long is it? (1 foot = 12 inches)', qty(12 * a, 'inches'), f'{a} × 12.'),
        ('Which number is bigger, the feet or the inches?', 'inches', 'Inches are smaller units.'),
        ('How many inches longer is a table that is 1 foot longer?', qty(12, 'inches'), '1 foot.'),
        ('Explain why there are more inches than feet.', S + 'Inches are shorter, so it takes more of them to measure the same length.', 'Smaller unit, bigger number.')])


@orq(ML, 4)
def o_ml4(r, L):
    k = lv(r, L, 4, 12)
    return ('ml4_open_estimate', f'A paper clip is about 1 inch long. A pencil is about {k} paper clips long.', [
        ('About how many inches long is the pencil?', qty(k, 'inches'), 'Each clip is 1 inch.'),
        ('About how long are two of these pencils end to end?', qty(2 * k, 'inches'), 'Double.'),
        ('Is the pencil shorter or longer than 1 foot (12 inches)?', 'shorter' if k < 12 else 'same', 'Compare.') if k != 12 else ('How many feet long is it?', '1', '12 inches.'),
        ('Explain how you estimate a length.', S + 'Compare the object with something whose length I know, then count.', 'Use a benchmark.')])


@orq(ML, 5)
def o_ml5(r, L):
    a, b = lv(r, L, 20, 70), r.randint(10, 40); need(a > b)
    return ('ml5_open_ribbons', f'A red ribbon is {a} centimeters long. A blue ribbon is {b} centimeters long.', [
        ('How much longer is the red ribbon?', qty(a - b, 'centimeters'), 'Subtract.'),
        ('How long are both ribbons together?', qty(a + b, 'centimeters'), 'Add.'),
        ('How much must be cut from the red ribbon to match the blue one?', qty(a - b, 'centimeters'), 'The difference.'),
        ('Explain how you compared the lengths.', S + 'I subtracted the shorter length from the longer length.', 'Difference.')])


@orq(ML, 6)
def o_ml6(r, L):
    vals = [[3, 4, 4, 5, 5, 5], [4, 5, 5, 6, 6, 6, 7], [5, 6, 6, 7, 7, 7, 7, 8]][L]; r.shuffle(vals)
    from collections import Counter
    c = Counter(vals); top = max(c.values()); mode = [k for k, v in c.items() if v == top][0]
    return ('ml6_open_line_plot', f'Pencil lengths in inches: {", ".join(map(str, vals))}. Make a line plot.', [
        ('How many pencils were measured?', n(len(vals)), 'Count the data.'),
        ('Which length has the most X marks?', qty(mode, 'inches'), 'Count each value.'),
        ('How much longer is the longest pencil than the shortest?', qty(max(vals) - min(vals), 'inches'), 'Subtract.'),
        ('Explain how you placed each X.', S + 'I found each length on the number line and put one X above it.', 'One X per pencil.')])

# ---------------------------------------------------------------- length and the number line


@orq(LN, 1)
def o_ln1(r, L):
    a, b = lv(r, L, 10, 45), r.randint(10, 40); need(a + b <= 100)
    need(a != b)
    return ('ln1_open_track', f'Ana runs {a} meters, rests, then runs {b} meters.', [
        ('How far does she run in all?', qty(a + b, 'meters'), 'Add.'),
        ('How much farther is the longer run?', qty(abs(a - b), 'meters'), 'Subtract.'),
        ('How many more meters to reach 100 meters?', qty(100 - a - b, 'meters'), 'Subtract from 100.'),
        ('Explain how a number line shows the runs.', S + f'Start at 0, jump {a}, then jump {b} more.', 'Jumps.')])


@orq(LN, 2)
def o_ln2(r, L):
    a, d = lv(r, L, 5, 50), r.randint(5, 30)
    return ('ln2_open_points', f'Point A is at {a} on a number line. Point B is {d} units to the right.', [
        ('Where is point B?', n(a + d), 'Add.'),
        ('How far is point A from 0?', qty(a, 'units'), 'Count from 0.'),
        ('Where is a point 10 units left of B?', n(a + d - 10), 'Subtract.'),
        ('Explain how the numbers are spaced on a number line.', S + 'Every space is the same length, one unit.', 'Equal spaces.')])


@orq(LN, 3)
def o_ln3(r, L):
    a, b, c = lv(r, L, 15, 50), r.randint(10, 30), r.randint(5, 15)
    need(b != c)
    return ('ln3_open_jumps', f'A frog starts at {a} on a number line. It jumps forward {b}, then back {c}.', [
        ('Where is the frog after the first jump?', n(a + b), 'Add.'),
        ('Where does the frog end?', n(a + b - c), 'Subtract.'),
        ('How far is the end from the start?', qty(b - c, 'units') if b > c else qty(c - b, 'units'), 'Compare.'),
        ('Explain how the jumps show addition and subtraction.', S + 'Jumping right adds and jumping left subtracts.', 'Right adds.')])

# ---------------------------------------------------------------- time and money


@orq(TM, 1)
def o_tm1(r, L):
    h, k = r.randint(1, 11), lv(r, L, 1, 10); t0 = h * 60 + 5 * k
    return ('tm1_open_clock', f'The hour hand is just past the {h} and the minute hand points to the {k}.', [
        ('What time is it?', tm(t0), f'{k} × 5 = {5 * k} minutes.'),
        ('What time will it be in 15 minutes?', tm(t0 + 15), 'Count on by 5s.'),
        ('How many minutes until the next hour?', qty(60 - 5 * k, 'minutes'), '60 minus the minutes.'),
        ('Explain how you read the minute hand.', S + 'I count by 5s for each number on the clock.', 'Count by 5s.')])


@orq(TM, 2)
def o_tm2(r, L):
    a, b = r.randint(6, 9), r.randint(1, 5) + L
    return ('tm2_open_day', f'Kai wakes up at {a}:00 AM and goes to soccer at {b}:00 PM.', [
        ('Is waking up in the morning AM or PM?', 'AM', 'Morning is AM.'),
        ('How many hours from waking up to noon?', qty(12 - a, 'hours'), f'12 − {a}.'),
        ('How many hours from noon to soccer?', qty(b, 'hours'), f'{b}:00 PM is {b} hours after noon.'),
        ('Explain the difference between AM and PM.', S + 'AM is from midnight to noon; PM is from noon to midnight.', 'Before and after noon.')])


@orq(TM, 3)
def o_tm3(r, L):
    q, d, ni, p = r.randint(0, 2) + (L > 0), r.randint(1, 3), r.randint(0, 2), r.randint(1, 4); v = 25 * q + 10 * d + 5 * ni + p; need(v < 100)
    return ('tm3_open_coins', f'Zoe has {q} quarters, {d} dimes, {ni} nickels and {p} pennies.', [
        ('How much money does Zoe have?', f'{v}¢', f'{25 * q} + {10 * d} + {5 * ni} + {p}.'),
        ('How much more does she need to have $1?', f'{100 - v}¢', f'100 − {v}.'),
        ('How much would she have with one more dime?', f'{v + 10}¢', 'Add 10.'),
        ('Explain the order you counted the coins in.', S + 'I counted the coins worth the most first, then counted on.', 'Biggest first.')])


@orq(TM, 4)
def o_tm4(r, L):
    t, f, o = L, r.randint(1, 3), r.randint(1, 4); v = 10 * t + 5 * f + o
    return ('tm4_open_bills', f'Ben has {t} $10 bills, {f} $5 bills and {o} $1 bills.', [
        ('How many dollars does Ben have?', f'${v}', f'{10 * t} + {5 * f} + {o}.'),
        ('How many more dollars to have $50?', f'${50 - v}', f'50 − {v}.'),
        ('How many dollars would he have with one more $5 bill?', f'${v + 5}', 'Add 5.'),
        ('Explain how you counted the bills.', S + 'I counted the $10 bills by tens, the $5 bills by fives, then the $1 bills by ones.', 'Skip count.')])


@orq(TM, 5)
def o_tm5(r, L):
    a, b = lv(r, L, 10, 60), r.randint(10, 35); need(a + b < 100)
    return ('tm5_open_store', f'A pencil costs {a}¢ and an eraser costs {b}¢.', [
        ('How much do both cost?', f'{a + b}¢', 'Add.'),
        ('How much change from $1 (100¢)?', f'{100 - a - b}¢', f'100 − {a + b}.'),
        ('How much more does the pencil cost than the eraser?', f'{abs(a - b)}¢', 'Subtract.'),
        ('Explain how you found the change.', S + 'I subtracted the cost from 100 cents.', 'Subtract from $1.')])

# ---------------------------------------------------------------- graphs


@orq(GD, 1)
def o_gd1(r, L):
    a, b, c = (r.randint(2, 9) for _ in range(3)); need(len({a, b, c}) == 3)
    return ('gd1_open_picture_graph', f'A picture graph shows pets: dogs {a}, cats {b}, fish {c}. Each picture is 1 pet.', [
        ('How many pets in all?', qty(a + b + c, 'pets'), 'Add.'),
        ('Which pet has the most?', ['dogs', 'cats', 'fish'][[a, b, c].index(max(a, b, c))], 'Compare.'),
        ('How many more dogs than fish?', n(a - c) if a > c else n(c - a), 'Subtract.'),
        ('Explain how you read a picture graph.', S + 'I count the pictures in each row.', 'Count pictures.')])


@orq(GD, 2)
def o_gd2(r, L):
    a, b, c = (r.randint(2, 15) for _ in range(3)); need(len({a, b, c}) == 3)
    return ('gd2_open_bar_graph', f'A bar graph shows favorite fruits: apple {a}, banana {b}, grape {c}.', [
        ('How many votes in all?', qty(a + b + c, 'votes'), 'Add.'),
        ('How many more votes did the top fruit get than the bottom fruit?', qty(max(a, b, c) - min(a, b, c), 'votes'), 'Subtract.'),
        ('How many votes for apple and banana together?', qty(a + b, 'votes'), 'Add.'),
        ('Explain how you read the height of a bar.', S + 'I look across from the top of the bar to the number on the scale.', 'Read the scale.')])


@orq(GD, 3)
def o_gd3(r, L):
    a, b = lv(r, L, 5, 15), r.randint(3, 12); need(a != b)
    return ('gd3_open_problem', f'A bar graph shows {a} students walk to school and {b} ride the bus.', [
        ('How many students in all?', qty(a + b, 'students'), 'Add.'),
        ('How many more walk than ride?' if a > b else 'How many more ride than walk?', qty(abs(a - b), 'students'), 'Subtract.'),
        ('If 3 more students walk, how many walk?', qty(a + 3, 'students'), 'Add.'),
        ('Explain how a graph helps you compare.', S + 'You can see which bar is taller and subtract the numbers.', 'Compare bars.')])


@orq(GD, 4)
def o_gd4(r, L):
    a, b, c = (r.randint(2, 9) for _ in range(3))
    return ('gd4_open_make_graph', f'Make a bar graph: red {a}, blue {b}, green {c}.', [
        ('How tall is the red bar?', n(a), 'One for each vote.'),
        ('How many votes in all?', n(a + b + c), 'Add.'),
        ('How much taller is the tallest bar than the shortest?', n(max(a, b, c) - min(a, b, c)), 'Subtract.'),
        ('Explain what you put on the graph to label it.', S + 'A title, the colors along the bottom and numbers up the side.', 'Labels.')])

# ---------------------------------------------------------------- shapes


@orq(SH, 1)
def o_sh1(r, L):
    s, k = [('triangle', 3), ('pentagon', 5), ('hexagon', 6)][L]
    return ('sh1_open_shape', f'Gabi draws a {s}.', [
        ('How many sides does it have?', n(k), f'A {s} has {k} sides.'),
        ('How many angles does it have?', n(k), 'Same as the sides.'),
        ('How many sides do 3 of them have in all?', n(3 * k), 'Add.'),
        ('Explain how you know the name of a shape.', S + 'I count its sides and angles.', 'Count sides.')])


@orq(SH, 2)
def o_sh2(r, L):
    k = [3, 4, 6][L]; name = {3: 'triangle', 4: 'quadrilateral', 6: 'hexagon'}[k]
    return ('sh2_open_draw', f'Draw a closed shape with {k} straight sides.', [
        ('What is the shape called?', name, f'{k} sides.'),
        ('How many angles does it have?', n(k), f'{k} angles.'),
        ('How many vertices (corners) does it have?', n(k), 'One at each angle.'),
        ('Explain what a closed shape is.', S + 'All the sides connect with no gaps.', 'No gaps.')])


@orq(SH, 3)
def o_sh3(r, L):
    k = lv(r, L, 2, 6)
    return ('sh3_open_cubes', f'Omar has {k} cubes.', [
        ('How many faces does one cube have?', n(6), 'A cube has 6 faces.'),
        ('How many faces do all the cubes have?', n(6 * k), f'{" + ".join(["6"] * k)}.'),
        ('What shape is each face?', 'square', 'Cube faces are squares.'),
        ('Explain how you counted the faces of a cube.', S + 'Top, bottom, front, back, left and right: 6 faces.', 'Count each side.')])


@orq(SH, 4)
def o_sh4(r, L):
    rows, cols = lv(r, L, 2, 5), r.randint(2, 5)
    return ('sh4_open_squares', f'A rectangle is split into {rows} rows and {cols} columns of same-size squares.', [
        ('How many squares are there?', n(rows * cols), 'Rows times columns, or repeated addition.'),
        ('How many squares are in one row?', n(cols), 'One per column.'),
        ('If one more row is added, how many squares?', n((rows + 1) * cols), f'Add {cols}.'),
        ('Explain how you counted the squares.', S + f'I added {cols} for each of the {rows} rows.', 'Repeated addition.')])


@orq(SH, 5)
def o_sh5(r, L):
    k = [2, 3, 4][L]; name = {2: 'halves', 3: 'thirds', 4: 'fourths'}[k]; one = {2: 'one half', 3: 'one third', 4: 'one fourth'}[k]
    return ('sh5_open_pizza', f'A pizza is cut into {name}.', [
        ('How many equal shares are there?', n(k), f'{name.capitalize()} means {k} equal shares.'),
        ('What do you call one share?', one, f'One of {k} equal shares.'),
        ('How many shares make the whole pizza?', n(k), f'{k} {name}.'),
        ('Explain why the shares must be equal.', S + 'Halves, thirds and fourths are equal shares of the same whole.', 'Equal shares.')])


@orq(SH, 6)
def o_sh6(r, L):
    k = [2, 3, 4][L]; name = {2: 'halves', 3: 'thirds', 4: 'fourths'}[k]
    return ('sh6_open_two_pizzas', f'Two same-size pizzas: one is cut into {name} and one into {"fourths" if k != 4 else "halves"}.', [
        ('Which pizza has more shares?', 'the first' if k > (4 if k != 4 else 2) else 'the second', 'Count the shares.'),
        ('Which pizza has bigger shares?', 'the second' if k > (4 if k != 4 else 2) else 'the first', 'Fewer shares are bigger.'),
        ('How many shares make a whole of the first pizza?', n(k), f'{k} {name}.'),
        ('Explain why more shares means smaller shares.', S + 'The same whole is cut into more pieces, so each piece is smaller.', 'Same whole.')])


def run(o):
    for u in UNITS:
        for skill in sorted(k for k in O if k.startswith(u + '-skill-')):
            items = [q for q in o.items(u) if q['skillId'] == skill]
            std = max((q['standards'] for q in items), key=lambda s: sum(1 for q in items if q['standards'] == s))
            for li, L in enumerate(['cp2', 'cp1', 'honors']):
                r = random.Random(f'g2-open|{skill}|{L}')
                for _ in range(500):
                    try:
                        fam, prompt, parts = O[skill](r, li)
                        break
                    except (Skip, StopIteration, ValueError, ZeroDivisionError, IndexError):
                        continue
                else:
                    raise SystemExit('no open item for ' + skill)
                assert len(parts) == 4
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
                    q = dict({'id': f'm2-{ABBR[u]}-s{skill[-2:]}-{L}-o01', 'skillId': skill, 'level': L, 'format': 'open-response'}, **fields)
                    o.add(u, q, meta)
