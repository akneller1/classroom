"""1st Grade Math audit #4 (2026-11-19): a context-based open-response item for every skill at every level.

Before the audit every Grade 1 open-response item was "Answer each part" or "Match each problem" with four unrelated
drills, and 7 skill/level combinations had none. Each item below is one short situation with three computed parts and
a tell-how-you-know part. Existing open-response items are rewritten in place; missing combinations get a new item
with an ID ending in -o01. Explanation answers begin "Sample answer:", which the Grade 1 players self-check."""
import random, re
from lib import ABBR, UNITS
import fams
from fams import NAMES, Skip, need, qty, n

NOTE = ('Original Claude-authored item (family: {fam}). 1st Grade Math audit 2026-11-19 (#4, open response); answers '
        'recomputed by scripts/test-grade1-audit.cjs; the explanation part is self-checked.')
O = {}
S = 'Sample answer: '
AT, AS, WP, EQ, CN, TO, CM, AH, ML, TT, DT, SH = (fams.AT, fams.AS, fams.WP, fams.EQ, fams.CN, fams.TO, fams.CM, fams.AH, fams.ML, fams.TT, fams.DT, fams.SH)


def orq(unit, i):
    def d(f):
        O[f'{unit}-skill-{i:02d}'] = f; return f
    return d


def lv(r, L, lo, hi):
    span = (hi - lo + 1) / 3
    return r.randint(int(lo + span * L), int(lo + span * (L + 1)) - 1 if L < 2 else hi)


@orq(AT, 1)
def o_at1(r, L):
    a, b = lv(r, L, 1, 5), r.randint(1, 4); need(a + b <= 9)
    return ('at1_open_fish', f'There are {a} red fish and {b} blue fish in a tank.', [
        ('How many fish are there?', qty(a + b, 'fish'), f'{a} + {b} = {a + b}.'),
        ('How many more fish would make 10?', qty(10 - a - b, 'fish'), f'{a + b} + {10 - a - b} = 10.'),
        ('Are there more red fish or blue fish?', 'red' if a > b else 'blue' if b > a else 'same', 'Compare.'),
        ('Tell how you added.', S + 'I started with the bigger number and counted on.', 'Count on.')])


@orq(AT, 2)
def o_at2(r, L):
    a = lv(r, L, 5, 10); b = r.randint(1, a - 1)
    return ('at2_open_cookies', f'There are {a} cookies on a plate. {r.choice(NAMES)} eats {b}.', [
        ('How many cookies are left?', qty(a - b, 'cookies'), f'{a} − {b} = {a - b}.'),
        ('Write the addition fact that checks it.', S + f'{a - b} + {b} = {a}', 'Add back.'),
        ('If 1 more cookie is eaten, how many are left?', qty(a - b - 1, 'cookies') if a - b > 1 else '0', 'Take away 1.'),
        ('Tell how you subtracted.', S + 'I counted back from the number I started with.', 'Count back.')])


@orq(AT, 3)
def o_at3(r, L):
    a = lv(r, L, 1, 9)
    return ('at3_open_ten_frame', f'A ten frame has {a} dots.', [
        ('How many empty boxes are there?', n(10 - a), f'{a} + {10 - a} = 10.'),
        ('Write the make-ten fact.', S + f'{a} + {10 - a} = 10', 'Fill the frame.'),
        ('If you add 2 more dots, how many dots are there?', n(a + 2), f'{a} + 2.'),
        ('Tell how a ten frame helps you make 10.', S + 'I can see how many boxes are empty.', 'Count the empty boxes.')])


@orq(AT, 4)
def o_at4(r, L):
    w = lv(r, L, 5, 10); a = r.randint(1, w - 1)
    return ('at4_open_partners', f'{w} children play in two groups. {a} children are on the swings.', [
        ('How many children are on the slide?', n(w - a), f'{w} − {a}.'),
        ('Write an addition fact for the two groups.', S + f'{a} + {w - a} = {w}', 'Parts make the whole.'),
        ('Name another way to make the same total with two groups.', S + f'{w - 1} + 1 = {w}', 'Any pair that makes the total.'),
        ('Tell how you found the other group.', S + f'I thought {a} and what make {w}.', 'Number partners.')])


@orq(AS, 1)
def o_as1(r, L):
    a, b = lv(r, L, 4, 9), r.randint(4, 9)
    return ('as1_open_shells', f'{r.choice(NAMES)} finds {a} shells. A friend finds {b} shells.', [
        ('How many shells in all?', qty(a + b, 'shells'), f'{a} + {b} = {a + b}.'),
        ('How many more shells would make 20?', qty(20 - a - b, 'shells'), f'20 − {a + b}.'),
        ('Who found more shells, the first child or the friend?', 'the first child' if a > b else 'the friend' if b > a else 'same', 'Compare.'),
        ('Tell a strategy you used to add.', S + 'I made a ten first, then added the rest.', 'Make a ten or use a double.')])


@orq(AS, 2)
def o_as2(r, L):
    a = lv(r, L, 11, 18); b = r.randint(3, 9)
    return ('as2_open_balloons', f'There are {a} balloons. {b} balloons float away.', [
        ('How many balloons are left?', qty(a - b, 'balloons'), f'{a} − {b} = {a - b}.'),
        ('Write the addition fact that helps.', S + f'{b} + {a - b} = {a}', 'Think addition.'),
        ('How many balloons would make 20?', qty(20 - (a - b), 'balloons'), f'20 − {a - b}.'),
        ('Tell how you subtracted.', S + 'I went back to 10 first, then took away the rest.', 'Go back through ten.')])


@orq(AS, 3)
def o_as3(r, L):
    a, b, c = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6) + L
    return ('as3_open_three_bowls', f'Three bowls have {a}, {b} and {c} grapes.', [
        ('How many grapes in all?', qty(a + b + c, 'grapes'), f'{a} + {b} + {c} = {a + b + c}.'),
        ('How many grapes are in the first two bowls?', qty(a + b, 'grapes'), f'{a} + {b}.'),
        ('Does the order you add change the total? (yes or no)', 'no', 'Any order gives the same sum.'),
        ('Tell which two numbers you added first and why.', S + 'I added two numbers that make 10 or a double first.', 'Easy pairs.')])


@orq(AS, 4)
def o_as4(r, L):
    a, b = lv(r, L, 3, 9), r.randint(3, 9); need(a != b)
    return ('as4_open_family', f'Use the numbers {a}, {b} and {a + b}.', [
        (f'What is {a} + {b}?', n(a + b), 'Add.'),
        (f'What is {a + b} − {a}?', n(b), 'Related fact.'),
        (f'What is {a + b} − {b}?', n(a), 'Related fact.'),
        ('Tell how the facts go together.', S + 'They use the same three numbers, so they are a fact family.', 'Fact family.')])


@orq(WP, 1)
def o_wp1(r, L):
    a, b = lv(r, L, 5, 12), r.randint(2, 7); need(a + b <= 20)
    return ('wp1_open_ducks', f'{a} ducks are in a pond. {b} more ducks come.', [
        ('How many ducks are in the pond now?', qty(a + b, 'ducks'), f'{a} + {b}.'),
        ('Then 3 ducks fly away. How many are left?', qty(a + b - 3, 'ducks'), f'{a + b} − 3.'),
        ('Write an equation for the first part.', S + f'{a} + {b} = {a + b}', 'Add to.'),
        ('Tell how you knew to add.', S + 'More ducks came, so the group got bigger.', 'Add to.')])


@orq(WP, 2)
def o_wp2(r, L):
    t = lv(r, L, 8, 20); a = r.randint(2, t - 2)
    return ('wp2_open_crayons', f'A box has {t} crayons. {a} are red and the rest are blue.', [
        ('How many crayons are blue?', qty(t - a, 'crayons'), f'{t} − {a}.'),
        ('Write an addition equation for the box.', S + f'{a} + {t - a} = {t}', 'Parts make the whole.'),
        ('Are there more red or more blue crayons?', 'red' if a > t - a else 'blue' if t - a > a else 'same', 'Compare.'),
        ('Tell how you found the blue crayons.', S + 'I took the red crayons away from all the crayons.', 'Take apart.')])


@orq(WP, 3)
def o_wp3(r, L):
    a, b = lv(r, L, 5, 15), r.randint(2, 8); need(a + b <= 20)
    return ('wp3_open_compare', f'Ben has {a} cars. Zoe has {b} more cars than Ben.', [
        ('How many cars does Zoe have?', qty(a + b, 'cars'), f'{a} + {b}.'),
        ('How many fewer cars does Ben have than Zoe?', qty(b, 'cars'), 'The difference.'),
        ('How many cars do they have in all?', qty(2 * a + b, 'cars') if 2 * a + b <= 40 else qty(2 * a + b, 'cars'), f'{a} + {a + b}.'),
        ('Tell what "more than" means here.', S + 'It tells how many extra cars Zoe has.', 'Difference.')])


@orq(WP, 4)
def o_wp4(r, L):
    a, b = lv(r, L, 3, 12), r.randint(2, 7); need(a + b <= 20)
    return ('wp4_open_start_unknown', f'Some birds are on a tree. {b} more birds come. Now there are {a + b} birds.', [
        ('How many birds were on the tree at first?', qty(a, 'birds'), f'{a + b} − {b}.'),
        ('Write an equation with a blank.', S + f'___ + {b} = {a + b}', 'Start unknown.'),
        ('If 2 birds fly away now, how many are left?', qty(a + b - 2, 'birds'), 'Take away 2.'),
        ('Tell how you found the start.', S + 'I took away the birds that came.', 'Work backward.')])


@orq(WP, 5)
def o_wp5(r, L):
    a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 5) + L
    return ('wp5_open_three', f'Uma has {a} red beads, {b} blue beads and {c} green beads.', [
        ('How many beads in all?', qty(a + b + c, 'beads'), f'{a} + {b} + {c}.'),
        ('How many beads are not green?', qty(a + b, 'beads'), f'{a} + {b}.'),
        ('How many more beads would make 20?', qty(20 - a - b - c, 'beads'), 'Subtract from 20.'),
        ('Tell which numbers you added first.', S + 'I looked for numbers that make 10 or a double.', 'Easy pairs.')])


@orq(EQ, 1)
def o_eq1(r, L):
    a, b = lv(r, L, 2, 9), r.randint(2, 9); c = r.randint(1, a + b - 1)
    return ('eq1_open_true_false', f'Look at {a} + {b} = {c} + {a + b - c}.', [
        (f'What is {a} + {b}?', n(a + b), 'Add.'),
        (f'What is {c} + {a + b - c}?', n(a + b), 'Add.'),
        ('Is the equation true or false?', 'true', 'Both sides are equal.'),
        ('Tell what the equal sign means.', S + 'Both sides have the same amount.', 'Same value.')])


@orq(EQ, 2)
def o_eq2(r, L):
    a, b = lv(r, L, 3, 12), r.randint(2, 8); need(a + b <= 20)
    return ('eq2_open_missing', f'{a} + ___ = {a + b}.', [
        ('What number is missing?', n(b), f'{a + b} − {a}.'),
        ('Write a subtraction fact that tells the same thing.', S + f'{a + b} − {a} = {b}', 'Related facts.'),
        (f'What is {a + b} − {b}?', n(a), 'Related fact.'),
        ('Tell how you found the missing number.', S + f'I counted on from {a} to {a + b}.', 'Count on.')])


@orq(EQ, 3)
def o_eq3(r, L):
    a, b, c = lv(r, L, 2, 9), r.randint(2, 9), r.randint(2, 9); need(a + b - c > 0 and a + b <= 20)
    return ('eq3_open_balance', f'A balance has {a} + {b} on one side and {c} + ___ on the other side.', [
        ('What is the left side worth?', n(a + b), 'Add.'),
        ('What number makes the sides equal?', n(a + b - c), f'{c} + ___ = {a + b}.'),
        ('Write the whole equation.', S + f'{a} + {b} = {c} + {a + b - c}', 'Both sides equal.'),
        ('Tell how you balanced it.', S + 'I made the right side worth the same as the left side.', 'Same value.')])


@orq(CN, 1)
def o_cn1(r, L):
    b, e = lv(r, L, 2, 11), r.randint(1, 9); need(10 * b + e <= 120)
    return ('cn1_open_bags', f'There are {b} bags of 10 crayons and {e} loose crayons.', [
        ('How many crayons are there?', qty(10 * b + e, 'crayons'), f'{b} tens and {e} ones.'),
        ('How many crayons are in the bags?', qty(10 * b, 'crayons'), f'{b} tens.'),
        ('How many crayons would there be with one more bag?', qty(10 * b + 10 + e, 'crayons'), 'Add 10.'),
        ('Tell why bags of 10 make counting easy.', S + 'I can count by tens and then count on the ones.', 'Count by tens.')])


@orq(CN, 2)
def o_cn2(r, L):
    a = lv(r, L, 20, 114)
    return ('cn2_open_count_on', f'{r.choice(NAMES)} starts counting at {a}.', [
        ('What are the next two numbers?', S + f'{a + 1}, {a + 2}', 'Count on by ones.'),
        ('What number is 5 after the start?', n(a + 5), 'Count on 5.'),
        ('What number comes just before the start?', n(a - 1), 'Count back 1.'),
        ('Tell what happens after a number that ends in 9.', S + 'The ones go back to 0 and there is one more ten.', 'A new ten.')])


@orq(CN, 3)
def o_cn3(r, L):
    v = lv(r, L, 21, 119); need(v % 10)
    return ('cn3_open_write', f'A number has {v // 10} tens and {v % 10} ones.', [
        ('Write the number.', n(v), 'Tens then ones.'),
        ('What number is 1 more?', n(v + 1), 'Add 1.'),
        ('What number is 1 less?', n(v - 1), 'Take away 1.'),
        ('Tell what each digit means.', S + 'The first digits tell the tens and the last digit tells the ones.', 'Place value.')])


@orq(CN, 4)
def o_cn4(r, L):
    a, k = lv(r, L, 20, 110), r.randint(2, 6); need(a + k <= 120)
    return ('cn4_open_count_add', f'Find {a} + {k} by counting on.', [
        ('What is the sum?', n(a + k), f'Count on {k}.'),
        (f'What is {a + k} − {k}?', n(a), f'Count back {k}.'),
        ('What number did you say first when counting on?', n(a + 1), 'One more than the start.'),
        ('Tell why you start with the bigger number.', S + 'It takes fewer counts.', 'Count on from the bigger number.')])


@orq(TO, 1)
def o_to1(r, L):
    t = lv(r, L, 1, 9)
    return ('to1_open_bundles', f'{r.choice(NAMES)} has {t} bundles of 10 sticks.', [
        ('How many sticks is that?', n(10 * t), f'{t} tens.'),
        ('How many ones is 1 bundle?', n(10), '1 ten is 10 ones.'),
        ('How many sticks with 3 more loose sticks?', n(10 * t + 3), 'Add 3 ones.'),
        ('Tell why a bundle is a ten.', S + 'It has 10 ones tied together.', 'Ten ones.')])


@orq(TO, 2)
def o_to2(r, L):
    o = lv(r, L, 1, 9)
    return ('to2_open_teen', f'A number has 1 ten and {o} ones.', [
        ('What is the number?', n(10 + o), f'10 + {o}.'),
        ('How many ones are there in all?', n(10 + o), '10 ones and more.'),
        ('What is the number with 1 more one?', n(11 + o), 'Add 1.'),
        ('Tell how teen numbers are made.', S + 'They are 1 ten and some more ones.', 'Ten and ones.')])


@orq(TO, 3)
def o_to3(r, L):
    a = lv(r, L, 1, 9)
    return ('to3_open_tens_count', f'{r.choice(NAMES)} counts by tens starting at {a}.', [
        ('What are the next two numbers?', S + f'{a + 10}, {a + 20}', 'Add 10.'),
        ('What is the 5th number after the start?', n(a + 50), 'Add 5 tens.'),
        ('Which digit stays the same?', 'the ones digit', 'Only the tens change.'),
        ('Tell what changes when you count by tens.', S + 'The tens digit goes up by 1.', 'Tens digit.')])


@orq(TO, 4)
def o_to4(r, L):
    v = lv(r, L, 21, 99); need(v % 10)
    return ('to4_open_place', f'Look at the number {v}.', [
        ('How many tens?', n(v // 10), 'The first digit.'),
        ('How many ones?', n(v % 10), 'The last digit.'),
        ('What number has the same digits switched?', n((v % 10) * 10 + v // 10), 'Switch the digits.'),
        ('Tell why the two numbers are different.', S + 'The digits are in different places, so they have different values.', 'Place value.')])


@orq(CM, 1)
def o_cm1(r, L):
    a, b = r.sample(range(11 + 20 * L, 59 + 20 * L), 2)
    return ('cm1_open_jars', f'Jar A has {a} beans. Jar B has {b} beans.', [
        ('Which jar has more beans?', 'A' if a > b else 'B', 'Compare tens, then ones.'),
        ('How many tens are in jar A?', n(a // 10), 'The first digit.'),
        ('How many tens are in jar B?', n(b // 10), 'The first digit.'),
        ('Tell how you compared.', S + 'I compared the tens first; if they were the same I compared the ones.', 'Tens first.')])


@orq(CM, 2)
def o_cm2(r, L):
    a, b = r.sample(range(11 + 20 * L, 59 + 20 * L), 2)
    return ('cm2_open_symbols', f'Compare {a} and {b}.', [
        (f'Write >, = or <: {a} ___ {b}', '>' if a > b else '<', 'Compare.'),
        (f'Write >, = or <: {b} ___ {a}', '<' if a > b else '>', 'Switch the order.'),
        ('Which number is greater?', n(max(a, b)), 'Compare.'),
        ('Tell how you remember which symbol to use.', S + 'The open side faces the greater number.', 'Open side.')])


@orq(CM, 3)
def o_cm3(r, L):
    t, o = lv(r, L, 2, 9), r.randint(2, 8)
    return ('cm3_open_digit', f'Find a digit for ? so that {t}? > {10 * t + o}.', [
        ('What is the smallest digit that works?', n(o + 1), f'The ones must be more than {o}.'),
        ('What is the greatest digit that works?', n(9), 'The largest digit.'),
        ('How many digits work?', n(9 - o), f'{o + 1} through 9.'),
        ('Tell how you found the digits.', S + 'The tens are the same, so I compared the ones.', 'Compare ones.')])


@orq(AH, 1)
def o_ah1(r, L):
    a = lv(r, L, 15, 85)
    return ('ah1_open_ten_more', f'{r.choice(NAMES)} has {a} stamps.', [
        ('What is 10 more?', n(a + 10), 'Add a ten.'),
        ('What is 10 less?', n(a - 10), 'Take away a ten.'),
        ('What is 20 more?', n(a + 20), 'Add two tens.'),
        ('Tell which digit changes when you add 10.', S + 'The tens digit goes up by 1.', 'Tens digit.')])


@orq(AH, 2)
def o_ah2(r, L):
    a, b = lv(r, L, 2, 6) * 10, r.randint(1, 3) * 10
    return ('ah2_open_tens', f'A shelf has {a} books. {b} more books are added.', [
        ('How many books now?', qty(a + b, 'books'), f'{a // 10} tens + {b // 10} tens.'),
        (f'Then {b} books are taken away. How many now?', qty(a, 'books'), 'Take away.'),
        ('How many tens is the total?', n((a + b) // 10), 'Count the tens.'),
        ('Tell how adding tens is like adding ones.', S + f'{a // 10} + {b // 10} = {(a + b) // 10}, so {a // 10} tens + {b // 10} tens = {(a + b) // 10} tens.', 'Tens like ones.')])


@orq(AH, 3)
def o_ah3(r, L):
    a, b = lv(r, L, 21, 80), r.randint(1, 8); need(a % 10 + b <= 9)
    return ('ah3_open_ones', f'{r.choice(NAMES)} has {a} marbles and gets {b} more.', [
        ('How many marbles now?', qty(a + b, 'marbles'), f'{a} + {b}.'),
        ('How many tens are in the total?', n((a + b) // 10), 'The tens do not change.'),
        ('How many ones are in the total?', n((a + b) % 10), 'Add the ones.'),
        ('Tell why the tens stayed the same.', S + 'The ones did not make a new ten.', 'No new ten.')])


@orq(AH, 4)
def o_ah4(r, L):
    a, b = lv(r, L, 21, 80), r.randint(2, 9); need(a % 10 + b >= 10)
    return ('ah4_open_new_ten', f'Add {a} + {b}.', [
        ('What is the sum?', n(a + b), 'Make a new ten.'),
        ('How many ones did you have before trading?', n(a % 10 + b), f'{a % 10} + {b}.'),
        ('How many tens are in the sum?', n((a + b) // 10), 'One more ten.'),
        ('Tell what making a new ten means.', S + '10 ones become 1 ten.', 'Trade 10 ones.')])


@orq(AH, 5)
def o_ah5(r, L):
    a, b = lv(r, L, 11, 50), r.randint(11, 40); need(a + b <= 99)
    return ('ah5_open_models', f'Use blocks to add {a} + {b}.', [
        ('How many tens blocks in all?', n(a // 10 + b // 10), 'Add the tens.'),
        ('How many ones blocks in all?', n(a % 10 + b % 10), 'Add the ones.'),
        ('What is the sum?', n(a + b), 'Put them together.'),
        ('Tell how the blocks show the sum.', S + 'I count the tens, then the ones, and trade 10 ones for a ten if I can.', 'Tens and ones.')])


@orq(ML, 1)
def o_ml1(r, L):
    a, b, c = r.sample(range(3, 12 + 3 * L), 3)
    return ('ml1_open_ribbons', f'A red ribbon is {a} cubes long, a blue ribbon is {b} cubes long and a green ribbon is {c} cubes long.', [
        ('Which ribbon is longest?', ['red', 'blue', 'green'][[a, b, c].index(max(a, b, c))], 'The most cubes.'),
        ('Which ribbon is shortest?', ['red', 'blue', 'green'][[a, b, c].index(min(a, b, c))], 'The fewest cubes.'),
        ('How many cubes longer is the longest than the shortest?', qty(max(a, b, c) - min(a, b, c), 'cubes'), 'Subtract.'),
        ('Tell how you put them in order.', S + 'I compared the number of cubes from fewest to most.', 'Compare.')])


@orq(ML, 2)
def o_ml2(r, L):
    a = lv(r, L, 4, 15); b = a + r.randint(1, 4); c = b + r.randint(1, 4)
    return ('ml2_open_indirect', f'A pencil is shorter than a marker. The marker is shorter than a ruler.', [
        ('Which is longest?', 'ruler', 'The ruler is longer than the marker.'),
        ('Which is shortest?', 'pencil', 'The pencil is shorter than the marker.'),
        ('Is the pencil shorter than the ruler? (yes or no)', 'yes', 'Shorter than something shorter.'),
        ('Tell how you knew without putting the pencil next to the ruler.', S + 'The pencil is shorter than the marker, and the marker is shorter than the ruler.', 'Compare through the marker.')])


@orq(ML, 3)
def o_ml3(r, L):
    a = lv(r, L, 3, 15)
    return ('ml3_open_clips', f'A book is {a} paper clips long.', [
        ('How long is the book in paper clips?', qty(a, 'paper clips'), 'Count the clips.'),
        ('How long are 2 books end to end?', qty(2 * a, 'paper clips'), 'Double.'),
        ('A pencil is 3 paper clips shorter than the book. How long is the pencil?', qty(a - 3, 'paper clips'), 'Subtract 3.'),
        ('Tell how to measure with paper clips.', S + 'Put the clips end to end with no gaps or overlaps and count them.', 'No gaps.')])


@orq(ML, 4)
def o_ml4(r, L):
    a = lv(r, L, 4, 12); g = r.randint(1, 3)
    return ('ml4_open_mistake', f'Kim measured a shoe with cubes but left {g} cube-sized gaps. She counted {a} cubes.', [
        ('Is the shoe longer or shorter than she counted?', 'longer', 'The gaps also take up space.'),
        ('How many cubes long is the shoe really?', qty(a + g, 'cubes'), f'{a} + {g}.'),
        ('How many cubes did she miss?', qty(g, 'cubes'), 'The gaps.'),
        ('Tell how to measure correctly.', S + 'Put the cubes end to end with no gaps or overlaps.', 'No gaps or overlaps.')])


@orq(TT, 1)
def o_tt1(r, L):
    h = lv(r, L, 1, 11)
    return ('tt1_open_hour', f'Lunch is at {h} o\'clock.', [
        ('Write the time with numbers.', f'{h}:00', f'{h} o\'clock.'),
        ('Where does the short hand point?', f'at the {h}', 'The hour hand.'),
        ('What time is it one hour later?', f'{h % 12 + 1}:00', 'Add 1 hour.'),
        ('Tell where the long hand points at any o\'clock time.', S + 'It points to the 12.', 'Minute hand at 12.')])


@orq(TT, 2)
def o_tt2(r, L):
    h = lv(r, L, 1, 11)
    return ('tt2_open_half_hour', f'Recess is at half past {h}.', [
        ('Write the time with numbers.', f'{h}:30', 'Half past.'),
        ('Where does the long hand point?', 'at the 6', 'Half past.'),
        ('What time is it half an hour later?', f'{h + 1}:00', 'Add 30 minutes.'),
        ('Tell where the short hand points at half past.', S + f'Halfway between the {h} and the {h + 1}.', 'Between the numbers.')])


@orq(TT, 3)
def o_tt3(r, L):
    h = lv(r, L, 1, 10)
    return ('tt3_open_schedule', f'Art starts at {h}:00 and music starts at {h}:30.', [
        ('Which starts first?', 'art', 'The earlier time.'),
        ('Write the music time in words.', S + f'half past {h}', 'Half past.'),
        ('What time is half an hour after music starts?', f'{h + 1}:00', 'Add 30 minutes.'),
        ('Tell how you know which time is earlier.', S + f'{h}:00 comes before {h}:30 on the clock.', 'Compare.')])


@orq(DT, 1)
def o_dt1(r, L):
    a, b, c = (r.randint(2 + 3 * L, 8 + 4 * L) for _ in range(3)); need(len({a, b, c}) == 3)
    return ('dt1_open_tally', f'A tally chart shows votes: apples {a}, bananas {b}, grapes {c}.', [
        ('How many votes in all?', qty(a + b + c, 'votes'), 'Add.'),
        ('Which fruit got the most votes?', ['apples', 'bananas', 'grapes'][[a, b, c].index(max(a, b, c))], 'Compare.'),
        ('How many more votes did the top fruit get than the bottom fruit?', qty(max(a, b, c) - min(a, b, c), 'votes'), 'Subtract.'),
        ('Tell how tally marks are grouped.', S + 'In bundles of 5 so they are easy to count.', 'Groups of 5.')])


@orq(DT, 2)
def o_dt2(r, L):
    a, b, c = (r.randint(2 + 3 * L, 8 + 4 * L) for _ in range(3)); need(len({a, b, c}) == 3)
    return ('dt2_open_picture_graph', f'A picture graph shows pets: dogs {a}, cats {b}, fish {c}.', [
        ('How many pets in all?', qty(a + b + c, 'pets'), 'Add.'),
        ('How many more dogs than fish?' if a > c else 'How many more fish than dogs?', qty(abs(a - c), 'pets'), 'Subtract.'),
        ('How many dogs and cats together?', qty(a + b, 'pets'), 'Add.'),
        ('Tell how you read a picture graph.', S + 'I count the pictures in each row.', 'Count pictures.')])


@orq(DT, 3)
def o_dt3(r, L):
    a, b, c = (r.randint(3 + 3 * L, 9 + 4 * L) for _ in range(3)); need(len({a, b, c}) == 3)
    return ('dt3_open_table', f'A table shows shapes in a bag: circles {a}, squares {b}, triangles {c}.', [
        ('How many shapes in all?', n(a + b + c), 'Add.'),
        ('How many are not circles?', n(b + c), 'Add the others.'),
        ('How many more of the most common shape than the least?', n(max(a, b, c) - min(a, b, c)), 'Subtract.'),
        ('Tell a question the table can answer.', S + 'How many squares and triangles are there together?', 'Ask about the data.')])


@orq(SH, 1)
def o_sh1(r, L):
    s, k = [('triangle', 3), ('square', 4), ('hexagon', 6)][L]
    return ('sh1_open_shape', f'Draw a {s}.', [
        ('How many sides?', n(k), f'A {s} has {k} sides.'),
        ('How many corners?', n(k), 'Same as the sides.'),
        ('How many sides do 2 of them have?', n(2 * k), 'Double.'),
        ('Tell what makes the shape a ' + s + '.', S + f'It is closed and has {k} straight sides.', 'Defining attributes.')])


@orq(SH, 2)
def o_sh2(r, L):
    s = ['cube', 'cone', 'cylinder'][L]
    facts = {'cube': ('6', 'no', 'square'), 'cone': ('1', 'yes', 'circle'), 'cylinder': ('2', 'yes', 'circle')}[s]
    return ('sh2_open_solid', f'Look at a {s}.', [
        ('How many flat faces does it have?', facts[0], 'Count the flat faces.'),
        ('Can it roll? (yes or no)', facts[1], 'A curved surface can roll.'),
        ('What shape is a flat face?', facts[2], 'Trace a face.'),
        ('Tell an object in the classroom with this shape.', S + {'cube': 'a block', 'cone': 'a party hat', 'cylinder': 'a can'}[s], 'Real objects.')])


@orq(SH, 3)
def o_sh3(r, L):
    k = lv(r, L, 2, 5)
    return ('sh3_open_compose', f'Two triangles make one square. {r.choice(NAMES)} wants to make {k} squares.', [
        ('How many triangles are needed?', n(2 * k), f'{k} squares × 2.'),
        ('How many squares can 10 triangles make?', n(5), '10 is 5 pairs.'),
        ('How many sides does one square have?', n(4), 'A square has 4 sides.'),
        ('Tell how the triangles fit together.', S + 'Their long sides line up to make a square.', 'Put shapes together.')])


@orq(SH, 4)
def o_sh4(r, L):
    m = [2, 4, 4][L]; name = {2: 'halves', 4: 'fourths'}[m]
    return ('sh4_open_cookie', f'A cookie is cut into {name}.', [
        ('How many equal shares?', n(m), f'{name.capitalize()}.'),
        ('If 1 share is eaten, how many are left?', n(m - 1), 'Take away 1.'),
        ('How many shares make the whole cookie?', n(m), 'All the shares.'),
        ('Tell why the shares must be equal.', S + 'Halves and fourths are equal shares.', 'Equal shares.')])


@orq(SH, 5)
def o_sh5(r, L):
    return ('sh5_open_two_pies', 'Two same-size pies: one is cut into halves and one into fourths.', [
        ('Which pie has more shares?', 'fourths', 'Count the shares.'),
        ('Which pie has bigger shares?', 'halves', 'Fewer shares are bigger.'),
        ('How many fourths make one half?', n(2), 'Two fourths fill a half.'),
        ('Tell why more shares are smaller.', S + 'The same pie is cut into more pieces, so each piece is smaller.', 'Same whole.')])


def run(o):
    for u in UNITS:
        for skill in sorted(k for k in O if k.startswith(u + '-skill-')):
            items = [q for q in o.items(u) if q['skillId'] == skill]
            std = max((q['standards'] for q in items), key=lambda s: sum(1 for q in items if q['standards'] == s))
            for li, L in enumerate(['cp2', 'cp1', 'honors']):
                r = random.Random(f'g1-open|{skill}|{L}')
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
                    q = dict({'id': f'm1-{ABBR[u]}-s{skill[-2:]}-{L}-o01', 'skillId': skill, 'level': L, 'format': 'open-response'}, **fields)
                    o.add(u, q, meta)
