"""Unit 7: Counting and Probability (8 skills). Every count and probability is computed, most by brute-force
enumeration. Prompts state order, repetition, replacement and distinguishability."""
import itertools, math
from fractions import Fraction
from core import Bank, fmt_set, frac, seeded
import figs

U = 'counting-probability'
P, C = math.perm, math.comb


def build():
    b = Bank(U, 'cn', 8)
    for f in (s1, s2, s3, s4, s5, s6, s7, s8, topup, topup2, errors):
        f(b)
    return b


def num_mc(b, k, L, prompt, ans, wr, steps, fam):
    ws = [str(w) for w in dict.fromkeys(wr) if str(w) != str(ans)]
    b.mc(k, L, prompt, str(ans), ws[:3], steps, fam, order='sort')


DICE = list(itertools.product(range(1, 7), repeat=2))
COINS3 = [''.join(p) for p in itertools.product('HT', repeat=3)]


# ---------------------------------------------------------------- 1. sample spaces and events
def s1(b):
    SS = [('cp2', 'A coin is tossed twice. List the sample space (use H and T, in the order HH, HT, ...).', 'HH, HT, TH, TT'),
          ('cp2', 'A spinner has sections red, blue, green and is spun once. List the sample space in that order.', 'red, blue, green'),
          ('cp1', 'A coin is tossed three times. How many outcomes are in the sample space?', '8'),
          ('cp1', 'Two different dice (one red, one blue) are rolled. How many outcomes are in the sample space?', '36'),
          ('honors', 'A family has three children; each outcome records the sexes in birth order (B or G). How many outcomes have at least two girls?', str(sum(1 for s in itertools.product('BG', repeat=3) if s.count('G') >= 2))),
          ('honors', 'Two cards are drawn without replacement from {A, B, C, D}, recording the ordered pair (first, second). How many outcomes are in the sample space?', str(P(4, 2)))]
    for L, t, a in SS:
        b.sa(1, L, t, a, ['List or count every possible outcome; order matters when the outcome records an order.', a], 'sample_space')
    EV = [('cp2', 'Roll one die. Event E: "roll an even number". List E.', '{2, 4, 6}'), ('cp2', 'Roll one die. Event F: "roll a number greater than 4". List F.', '{5, 6}'),
          ('cp1', 'Two dice are rolled (ordered pairs). How many outcomes are in the event "the sum is 7"?', str(sum(1 for a, c in DICE if a + c == 7))),
          ('cp1', 'Three coins are tossed. List the event "exactly two heads" in alphabetical order, separated by commas.', ', '.join(sorted(s for s in COINS3 if s.count('H') == 2))),
          ('honors', 'Two dice are rolled (ordered pairs). How many outcomes are in the event "the maximum of the two numbers is 4"?', str(sum(1 for a, c in DICE if max(a, c) == 4))),
          ('honors', 'Draw one card from a standard 52-card deck. How many outcomes are in the event "a heart or a face card (J, Q, K)"?', str(13 + 12 - 3))]
    for L, t, a in EV:
        b.sa(1, L, t, a, ['An event is a subset of the sample space.', 'Answer: ' + a], 'event')
    b.sel(1, 'cp2', 'A die is rolled once. Which are possible outcomes?', [('1', True), ('6', True), ('3', True), ('7', False), ('0', False)], ['The sample space is {1, 2, 3, 4, 5, 6}.'], 'outcome_select')
    b.sel(1, 'cp1', 'Two coins are tossed. Which events contain exactly two outcomes?', [('"at least one head" ... no', False), ('"exactly one head"', True), ('"the coins match"', True), ('"the first coin is H"', True), ('"two heads"', False)][1:] + [('"at least one head"', False)],
          ['Exactly one head: HT, TH. Match: HH, TT. First H: HH, HT. Two heads: HH. At least one head: HH, HT, TH.'], 'event_select')
    b.sel(1, 'honors', 'Two dice are rolled. Which events are mutually exclusive with "the sum is 12"?', [('"a 1 appears"', True), ('"the sum is odd"', True), ('"both dice are less than 6"', True), ('"doubles"', False), ('"the sum is at least 10"', False)],
          ['Sum 12 means (6, 6). It shares no outcome with the first three events; (6, 6) is doubles and has sum ≥ 10.'], 'event_select')
    b.orq(1, 'cp2', 'A spinner with numbers 1, 2, 3 is spun twice; record (first, second).',
          [('List the sample space.', '(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)'), ('How many outcomes?', '9'), ('List the event "the two spins match".', '(1,1), (2,2), (3,3)'), ('List the event "sum is 4".', '(1,3), (2,2), (3,1)')],
          ['All ordered pairs.', '3·3.', 'Doubles.', 'Pairs adding to 4.'], 'sample_space_or')
    b.orq(1, 'cp1', 'A coin is tossed and a die is rolled.',
          [('How many outcomes are in the sample space?', '12'), ('List the event "heads and an even number".', 'H2, H4, H6'), ('How many outcomes are in "tails or a 6"?', '7'), ('Are "heads" and "tails" mutually exclusive?', 'Yes')],
          ['2·6.', 'Three outcomes.', '6 + 2 − 1.', 'They share no outcome.'], 'sample_space_or')
    b.orq(1, 'honors', 'Two marbles are drawn without replacement from a bag with red, blue and green marbles (one of each); order is recorded.',
          [('List the sample space.', 'RB, RG, BR, BG, GR, GB'), ('How many outcomes include red?', '4'), ('If order is NOT recorded, how many outcomes are there?', '3'),
           ('Why do the two sample spaces have different sizes?', 'Ordered outcomes count RB and BR separately; unordered outcomes count {R, B} once.')],
          ['Permutations of 2 from 3.', 'RB, RG, BR, GR.', 'C(3, 2).', 'Each unordered pair appears twice when ordered.'], 'sample_space_or')


# ---------------------------------------------------------------- 2. lists, sublists, arrays
def s2(b):
    L1 = [('cp2', 'How many integers are in the list 1, 2, 3, ..., 50?', 50), ('cp2', 'How many integers are in the list 10, 11, 12, ..., 25?', 16),
          ('cp1', 'How many integers are in the list 37, 38, ..., 102?', 66), ('cp1', 'How many 3-digit integers (100 to 999) are there?', 900),
          ('honors', 'How many multiples of 7 are between 100 and 500 (inclusive)?', len([n for n in range(100, 501) if n % 7 == 0])),
          ('honors', 'An array A[15], A[16], ..., A[84] is processed. How many elements does it have?', 70),
          ('cp1', 'How many even integers are between 21 and 79?', len([n for n in range(22, 79) if n % 2 == 0])),
          ('honors', 'How many integers from 1 to 1000 are perfect squares?', 31)]
    for L, t, v in L1:
        b.sa(2, L, t, v, ['A list m, m + 1, ..., n contains n − m + 1 integers (for multiples, list the multipliers instead).', 'Answer: %d' % v], 'list_count')
    MC = [('cp2', 'How many integers are in the list 5, 6, ..., 20?', 16, [15, 20, 14]), ('cp1', 'A loop runs for i = 4 to 30 (inclusive). How many times does it run?', 27, [26, 30, 28]),
          ('honors', 'How many integers n with 1 ≤ n ≤ 200 leave remainder 3 when divided by 5?', 40, [39, 41, 200 // 5 + 3])]
    for L, t, v, wr in MC:
        num_mc(b, 2, L, t, v, wr, ['Use n − m + 1, or list n = 5k + 3 and count k.', 'Answer: %d' % v], 'list_count')
    assert len([n for n in range(1, 201) if n % 5 == 3]) == 40
    b.sel(2, 'cp2', 'Which lists contain exactly 10 integers?', [('1, 2, ..., 10', True), ('11, 12, ..., 20', True), ('0, 1, ..., 10', False), ('5, 6, ..., 14', True), ('2, 4, ..., 10', False)],
          ['Count with n − m + 1; 0 to 10 has 11; 2, 4, ..., 10 has 5.'], 'list_select')
    b.sel(2, 'cp1', 'Which statements are correct for the list 12, 13, ..., 48?', [('It has 37 integers', True), ('It has 19 even integers', True), ('It has 18 odd integers', True), ('It has 36 integers', False), ('It has 13 multiples of 3', True)],
          ['48 − 12 + 1 = 37; evens 12, 14, ..., 48: 19; odds 18; multiples of 3: 12, 15, ..., 48 gives 13.'], 'list_select')
    b.sel(2, 'honors', 'An array is indexed A[m], ..., A[n]. Which formulas give the number of elements?', [('n − m + 1', True), ('(n + 1) − m', True), ('n − (m − 1)', True), ('n − m', False), ('n + m − 1', False)],
          ['All three correct forms are algebraically equal.'], 'list_select')
    b.orq(2, 'cp2', 'A theater numbers seats 101 through 160.',
          [('How many seats are there?', '60'), ('How many seats have even numbers?', '30'), ('How many seats are numbered 101 through 125?', '25'), ('Why is 160 − 101 = 59 not the answer?', 'Subtracting counts the gaps; we must add 1 to include both ends.')],
          ['160 − 101 + 1.', 'Half.', '125 − 101 + 1.', 'Fencepost error.'], 'list_or')
    b.orq(2, 'cp1', 'Consider the integers from 1 to 300.',
          [('How many are multiples of 4?', '75'), ('How many are multiples of 6?', '50'), ('How many are multiples of both 4 and 6?', '25'), ('How many are multiples of 4 or 6?', '100')],
          ['⌊300/4⌋.', '⌊300/6⌋.', 'Multiples of 12.', '75 + 50 − 25.'], 'list_or')
    b.orq(2, 'honors', 'A program loops: for i = 3 to n, for j = 1 to i, do one step.',
          [('How many steps when n = 5?', '12'), ('Write the total for general n as a sum.', 'Σ_{i=3}^{n} i'), ('Simplify the sum.', 'n(n + 1)/2 − 3'), ('How many steps when n = 100?', '5047')],
          ['3 + 4 + 5.', 'Inner loop runs i times.', 'Subtract 1 + 2.', '5050 − 3.'], 'list_or')


# ---------------------------------------------------------------- 3. possibility trees
def s3(b):
    p1 = figs.tree(U, 'tree_coin3', [['H', 'T']] * 3)
    for L, t, v in (('cp2', 'The possibility tree shows three coin tosses. How many outcomes (leaves) are there?', 8), ('cp1', 'Use the tree for three coin tosses. How many outcomes have exactly one tail?', 3),
                    ('honors', 'Use the tree for three coin tosses. How many outcomes have no two consecutive heads?', sum(1 for s in COINS3 if 'HH' not in s))):
        r = b.sa(3, L, t, v, ['Count the leaves that match the condition.', 'Answer: %d' % v], 'read_tree')
        b.image(r, p1, 'Possibility tree: three stages, each branching into H and T, giving 8 leaves.')
    p2 = figs.tree(U, 'tree_outfit', [['shirt A', 'shirt B'], ['jeans', 'khakis', 'shorts']], size=(5.2, 3.0))
    for L, t, v in (('cp2', 'The tree shows outfit choices. How many outfits are possible?', 6), ('cp1', 'Using the outfit tree, how many outfits do NOT use shorts?', 4)):
        r = b.sa(3, L, t, v, ['Each path from the root to a leaf is one outfit.', 'Answer: %d' % v], 'read_tree')
        b.image(r, p2, 'Tree: 2 shirts (A, B), each branching to jeans, khakis, shorts: 6 leaves.')
    TR = [('cp2', 'A menu offers 3 sandwiches and 2 drinks. A tree diagram shows every meal. How many leaves does it have?', 6),
          ('cp1', 'Best-of-three match: the first player to win 2 games wins. How many different sequences of game winners are possible (players A, B)?', 6),
          ('honors', 'A team plays until it wins 2 games or loses 2 games (whichever comes first). How many different win-loss sequences are possible?', 6),
          ('honors', 'You draw from a bag with 2 red and 1 blue marble without replacement until you draw blue. How many different color sequences are possible?', 3),
          ('cp1', 'A tree for picking 2 different letters in order from {a, b, c}. How many leaves?', 6)]
    for L, t, v in TR:
        b.sa(3, L, t, v, ['Draw the tree; stop a branch as soon as the process ends.', 'Answer: %d' % v], 'tree_count')
    b.mc(3, 'cp2', 'In a possibility tree for tossing a coin 4 times, how many branches come out of each non-final node?', '2', ['4', '8', '16'], ['Each toss has 2 outcomes.'], 'tree_structure', order='sort')
    b.mc(3, 'cp1', 'A tree for choosing a president, then a vice-president, from 5 people (different people). How many leaves?', '20', ['25', '10', '9'], ['5 choices then 4: 20.'], 'tree_structure', order='sort')
    b.mc(3, 'honors', 'Why might the multiplication rule NOT apply directly to a tree?', 'Different branches can have different numbers of sub-branches', ['Trees always have too many leaves', 'Trees cannot show order', 'Trees only work for coins'],
         ['The multiplication rule needs the same number of choices at each step regardless of earlier choices; a best-of-three tree stops early on some branches.'], 'tree_structure')
    b.sel(3, 'cp1', 'In the best-of-three tree (first to win 2), which sequences are complete outcomes?', [('AA', True), ('ABA', True), ('BAB', True), ('AB', False), ('AAB', False)],
          ['The match ends as soon as someone has 2 wins: AA, ABA, ABB, BAA, BAB, BB.'], 'tree_select')
    b.sel(3, 'cp2', 'A tree shows tossing a coin then rolling a 1–3 spinner. Which are leaves?', [('H1', True), ('T3', True), ('H2', True), ('H4', False), ('HT', False)], ['Coin first, then spinner number.'], 'tree_select')
    b.sel(3, 'honors', 'A tree records drawing letters without replacement from {a, b, c} until c appears. Which are complete outcomes?', [('c', True), ('ac', True), ('bac', True), ('ab', False), ('cab', False)],
          ['Stop as soon as c is drawn: c, ac, bc, abc, bac.'], 'tree_select')
    b.orq(3, 'cp2', 'Draw a possibility tree for choosing a cone (sugar or waffle) and a flavor (vanilla, chocolate).',
          [('How many first-level branches?', '2'), ('How many leaves?', '4'), ('List the leaves.', 'sugar-vanilla, sugar-chocolate, waffle-vanilla, waffle-chocolate'), ('Check with the multiplication rule.', '2·2 = 4')],
          ['Cones.', 'Each cone splits in 2.', 'Paths.', 'Rule matches.'], 'tree_or')
    b.orq(3, 'cp1', 'A coin is tossed until a head appears or 3 tosses are made.',
          [('List all outcomes.', 'H, TH, TTH, TTT'), ('How many outcomes are there?', '4'), ('Are they equally likely for a fair coin?', 'No: H has probability 1/2, TTT has 1/8.'), ('Why is this not 2³ = 8?', 'Branches stop early after a head.')],
          ['Stop at H.', 'Count.', 'Multiply along branches.', 'Unequal tree.'], 'tree_or')
    b.orq(3, 'honors', 'A best-of-five series ends when a team wins 3 games.',
          [('How many sequences end in exactly 3 games?', '2'), ('How many end in exactly 4 games?', '6'), ('How many end in exactly 5 games?', '12'), ('How many sequences in total?', '20')],
          ['AAA or BBB.', 'Winner wins game 4 and 2 of the first 3: 2·C(3, 2).', '2·C(4, 2).', '2 + 6 + 12.'], 'tree_or')


# ---------------------------------------------------------------- 4. addition rule
def s4(b):
    AD = [('cp2', 'A student chooses one book: 7 mysteries or 5 biographies (no book is both). How many choices?', 12),
          ('cp2', 'A lunch special is one soup (3 kinds) or one salad (4 kinds). How many choices?', 7),
          ('cp1', 'How many passwords of length 1, 2 or 3 can be made from the 26 lowercase letters (repetition allowed)?', 26 + 26 ** 2 + 26 ** 3),
          ('cp1', 'How many integers from 1 to 100 are divisible by 2 or 7?', len([n for n in range(1, 101) if n % 2 == 0 or n % 7 == 0])),
          ('honors', 'How many bit strings of length 6 start with 11 or end with 00?', 16 + 16 - 4),
          ('honors', 'How many integers from 1 to 999 contain no digit 7? (Count by number of digits.)', len([n for n in range(1, 1000) if '7' not in str(n)])),
          ('cp1', 'How many 3-digit numbers have all digits odd or all digits even (the first digit cannot be 0)?', 5 ** 3 + 4 * 25),
          ('honors', 'How many 4-letter strings over {a, b, c} contain at least one a? (Use the complement.)', 3 ** 4 - 2 ** 4)]
    for L, t, v in AD:
        b.sa(4, L, t, v, ['If the cases do not overlap, add; if they overlap, subtract the overlap (inclusion-exclusion); the complement rule counts "at least one".', 'Answer: %d' % v], 'addition_rule')
    MC = [('cp2', 'A club elects a leader from 6 juniors or 4 seniors. How many choices?', 10, [24, 6, 4]), ('cp1', 'How many cards in a 52-card deck are kings or clubs?', 16, [17, 13, 4]),
          ('honors', 'How many integers from 1 to 60 are divisible by 3, 4 or 5?', len([n for n in range(1, 61) if n % 3 == 0 or n % 4 == 0 or n % 5 == 0]), [47, 36, 20])]
    for L, t, v, wr in MC:
        num_mc(b, 4, L, t, v, wr, ['Add the cases and subtract overlaps.', 'Answer: %d' % v], 'addition_rule')
    b.sel(4, 'cp1', 'When may you simply ADD the sizes of two sets to count their union?', [('When the sets are disjoint', True), ('When no outcome is in both sets', True), ('When the sets are mutually exclusive events', True), ('Always', False), ('When the sets are the same size', False)],
          ['Addition rule: |A ∪ B| = |A| + |B| exactly when A ∩ B = ∅.'], 'addition_select')
    b.sel(4, 'cp2', 'A snack is one fruit (apple, pear) or one cracker (plain, cheese, wheat). Which statements are true?', [('There are 5 choices', True), ('Choosing an apple is one choice', True), ('There are 6 choices', False), ('The two groups do not overlap', True), ('You must choose both a fruit and a cracker', False)],
          ['"Or" with disjoint groups → add: 2 + 3.'], 'addition_select')
    b.sel(4, 'honors', 'Which counts equal the number of bit strings of length 5 with at least one 1?', [('2⁵ − 1', True), ('31', True), ('C(5,1) + C(5,2) + C(5,3) + C(5,4) + C(5,5)', True), ('5·2⁴', False), ('2⁴', False)],
          ['Complement: 32 − 1; or add by number of 1s.', '5·2⁴ overcounts strings with several 1s.'], 'addition_select')
    b.orq(4, 'cp1', 'Count the integers from 1 to 120 that are divisible by 3 or 5.',
          [('How many are divisible by 3?', '40'), ('How many are divisible by 5?', '24'), ('How many are divisible by both?', '8'), ('How many are divisible by 3 or 5?', '56')],
          ['⌊120/3⌋.', '⌊120/5⌋.', 'Multiples of 15.', '40 + 24 − 8.'], 'addition_or')
    b.orq(4, 'cp2', 'A student picks one elective: 4 art classes, 3 music classes, or 2 drama classes.',
          [('How many electives are there?', '9'), ('Which rule did you use?', 'The addition rule'), ('Why can you add?', 'No class is in two groups.'), ('If one art class is also a music class, how many electives?', '8')],
          ['4 + 3 + 2.', 'Disjoint cases.', 'Disjoint.', 'Subtract the overlap.'], 'addition_or')
    b.orq(4, 'honors', 'Passwords are 6 characters from 26 letters and 10 digits and must contain at least one digit.',
          [('How many 6-character strings use letters and digits?', '36⁶ = 2176782336'), ('How many use only letters?', '26⁶ = 308915776'), ('How many contain at least one digit?', str(36 ** 6 - 26 ** 6)), ('Which rule did you use?', 'Complement (subtraction) rule')],
          ['36 choices each.', '26 choices each.', 'Subtract.', 'Total minus "no digit".'], 'addition_or')


# ---------------------------------------------------------------- 5. multiplication rule
def s5(b):
    MU = [('cp2', 'A restaurant has 4 appetizers, 6 entrées and 3 desserts. How many 3-course meals (one of each)?', 72),
          ('cp2', 'License plates have 2 letters followed by 2 digits (repetition allowed). How many plates?', 26 ** 2 * 100),
          ('cp1', 'How many 4-digit PINs have no repeated digit?', P(10, 4)),
          ('cp1', 'How many 5-letter strings use only vowels (a, e, i, o, u) with repetition allowed?', 5 ** 5),
          ('honors', 'How many 3-digit numbers (100–999) have distinct digits?', 9 * 9 * 8),
          ('honors', 'How many even 3-digit numbers have distinct digits?', len([n for n in range(100, 1000) if n % 2 == 0 and len(set(str(n))) == 3])),
          ('cp1', 'In how many ways can 6 runners finish 1st, 2nd and 3rd (no ties)?', P(6, 3)),
          ('honors', 'How many functions are there from a 3-element set to a 5-element set?', 5 ** 3)]
    for L, t, v in MU:
        b.sa(5, L, t, v, ['Multiply the number of choices at each step (each step\'s count must not depend on earlier choices).', 'Answer: %d' % v], 'multiplication_rule')
    MC = [('cp2', 'You have 3 shirts and 5 pairs of pants. How many outfits (one shirt, one pair of pants)?', 15, [8, 35, 53]),
          ('cp1', 'How many 3-letter strings from the 26 letters have no repeated letter?', P(26, 3), [26 ** 3, C(26, 3), 26 * 3]),
          ('honors', 'How many ways can 5 people sit in a row if Ann and Bo must sit next to each other?', 2 * math.factorial(4), [math.factorial(5), math.factorial(4), 2 * math.factorial(5)])]
    for L, t, v, wr in MC:
        num_mc(b, 5, L, t, v, wr, ['Count step by step; for "next to each other", glue the pair into one unit and arrange the pair internally.', 'Answer: %d' % v], 'multiplication_rule')
    b.sel(5, 'cp1', 'Which situations can be counted with the multiplication rule directly?', [('Choosing a shirt AND a pair of pants', True), ('Assigning 1st, 2nd, 3rd place', True), ('Forming 4-digit PINs', True), ('Choosing a soup OR a salad', False), ('Counting bit strings with no two consecutive 1s', False)],
          ['Sequential "and" choices multiply; "or" adds; the last needs a recursion because the choices depend on earlier bits.'], 'multiplication_select')
    b.sel(5, 'cp2', 'A sandwich has 1 bread (2 kinds) and 1 meat (4 kinds). Which statements are true?', [('There are 8 sandwiches', True), ('Each sandwich is one bread and one meat', True), ('There are 6 sandwiches', False), ('A tree diagram would have 8 leaves', True), ('There are 16 sandwiches', False)],
          ['2·4 = 8.'], 'multiplication_select')
    b.sel(5, 'honors', 'Which expressions count the 4-letter strings over {a, b, c, d, e} with no repeated letter?', [('5·4·3·2', True), ('P(5, 4)', True), ('5!/1!', True), ('5⁴', False), ('C(5, 4)', False)],
          ['Order matters, no repetition: P(5, 4) = 120.'], 'multiplication_select')
    b.orq(5, 'cp2', 'A combination lock uses 3 numbers from 0 to 9 (repetition allowed).',
          [('How many choices for each number?', '10'), ('How many combinations?', '1000'), ('How many combinations have no repeated number?', '720'), ('How many have at least one repeat?', '280')],
          ['0–9.', '10³.', '10·9·8.', '1000 − 720.'], 'multiplication_or')
    b.orq(5, 'cp1', 'A class of 20 elects a president, vice-president and secretary (different people).',
          [('How many choices for president?', '20'), ('How many ways to fill all three offices?', '6840'), ('If Kim must be president, how many ways?', '342'), ('If Kim must hold some office, how many ways?', '1026')],
          ['Anyone.', '20·19·18.', '19·18.', '3 offices for Kim · 19·18.'], 'multiplication_or')
    b.orq(5, 'honors', 'Count 4-digit numbers (1000–9999).',
          [('How many have distinct digits?', '4536'), ('How many are odd with distinct digits?', '2240'), ('How many contain at least one 5?', str(9000 - 8 * 9 ** 3)), ('Explain why the odd count is done by choosing the last digit first.', 'The last digit is restricted, and the first digit cannot be 0; choosing restricted positions first keeps each step\'s count fixed.')],
          ['9·9·8·7.', 'Last digit 5 ways, first 8, then 8·7.', '9000 − (8·9·9·9).', 'Handle restrictions first.'], 'multiplication_or')
    assert len([n for n in range(1000, 10000) if n % 2 and len(set(str(n))) == 4]) == 2240 and len([n for n in range(1000, 10000) if len(set(str(n))) == 4]) == 4536


# ---------------------------------------------------------------- 6. counting systematically (permutations and combinations)
def s6(b):
    PC = [('cp2', 'How many ways can 4 different books be arranged on a shelf?', 24, 'Order matters: 4!.'),
          ('cp2', 'How many ways can a committee of 2 be chosen from 5 people (order does not matter)?', 10, 'C(5, 2).'),
          ('cp1', 'How many ways can a 5-card hand be dealt from a 52-card deck (order does not matter)?', C(52, 5), 'C(52, 5).'),
          ('cp1', 'How many distinct arrangements of the letters in BOOK are there?', 12, '4!/2! because the two O\'s are identical.'),
          ('cp1', 'How many 3-person committees from 8 people include a specific person, Lee?', C(7, 2), 'Lee is in; choose 2 more from 7.'),
          ('honors', 'How many distinct arrangements of MISSISSIPPI are there?', math.factorial(11) // (math.factorial(4) * math.factorial(4) * math.factorial(2)), '11!/(4!·4!·2!).'),
          ('honors', 'How many ways can 3 identical prizes be given to 7 students if no student gets more than one?', C(7, 3), 'Identical prizes → choose the 3 winners.'),
          ('honors', 'How many ways can 10 identical candies be given to 3 children (any child may get 0)?', C(12, 2), 'Stars and bars: C(10 + 2, 2).'),
          ('cp1', 'How many ways can 7 people stand in a line?', math.factorial(7), '7!.'),
          ('honors', 'How many committees of 4 from 6 women and 5 men have exactly 2 women?', C(6, 2) * C(5, 2), 'C(6, 2)·C(5, 2).')]
    for L, t, v, why in PC:
        b.sa(6, L, t, v, [why, 'Answer: %d' % v], 'perm_comb')
    CH = [('cp2', 'Choosing 3 toppings from 10 for a pizza', 'Combination (order does not matter)'), ('cp2', 'Awarding gold, silver and bronze medals to 3 of 10 runners', 'Permutation (order matters)'),
          ('cp1', 'Forming a 4-digit PIN with no repeated digit', 'Permutation (order matters)'), ('cp1', 'Selecting 5 students from 30 for a field trip', 'Combination (order does not matter)'),
          ('honors', 'Choosing which 4 of 12 questions to answer on a test', 'Combination (order does not matter)'), ('honors', 'Assigning 3 different tasks to 3 of 8 volunteers, one task each', 'Permutation (order matters)')]
    for L, t, good in CH:
        b.mc(6, L, 'Which type of count fits? %s' % t, good, ['Permutation (order matters)' if good.startswith('Comb') else 'Combination (order does not matter)', 'Neither: use the addition rule', 'Repetition is required, so use nᵏ'],
             ['Ask whether rearranging the same selection gives a different outcome.', good], 'perm_or_comb')
    b.sel(6, 'cp1', 'Which expressions equal the number of ways to choose 3 of 7 students (order does not matter)?', [('C(7, 3)', True), ('35', True), ('P(7, 3)/3!', True), ('P(7, 3)', False), ('7³', False)],
          ['C(7, 3) = 7·6·5/6 = 35.'], 'count_select')
    b.sel(6, 'cp2', 'Which situations are counted by 5!?', [('Arranging 5 different books in a row', True), ('Ordering 5 runners from 1st to 5th', True), ('Choosing 2 of 5 people', False), ('Lining up 5 students', True), ('Choosing 5 toppings from 10', False)],
          ['5! counts arrangements of 5 distinct objects.'], 'count_select')
    b.sel(6, 'honors', 'Which counts equal C(10, 3)?', [('Bit strings of length 10 with exactly three 1s', True), ('Subsets of size 7 of a 10-element set', True), ('Lattice paths with 3 right and 7 up steps', True), ('Ordered selections of 3 from 10', False), ('Functions from a 3-set to a 10-set', False)],
          ['Choosing positions for the 1s, C(10, 7) = C(10, 3), and choosing which steps go right all give 120.'], 'count_select')
    b.orq(6, 'cp2', 'A club with 6 members chooses people.',
          [('How many ways to choose a president and a treasurer (different people)?', '30'), ('How many ways to choose a 2-person team?', '15'), ('Explain why the answers differ.', 'Offices are ordered roles; a team is unordered, so each team is counted twice as officers.'), ('How many ways to line up all 6 for a photo?', '720')],
          ['6·5.', 'C(6, 2).', 'Divide by 2!.', '6!.'], 'count_or')
    b.orq(6, 'cp1', 'From 8 boys and 7 girls choose a committee of 5.',
          [('How many committees in all?', str(C(15, 5))), ('How many with exactly 3 girls?', str(C(7, 3) * C(8, 2))), ('How many with no girls?', str(C(8, 5))), ('How many with at least one girl?', str(C(15, 5) - C(8, 5)))],
          ['C(15, 5).', 'C(7, 3)·C(8, 2).', 'C(8, 5).', 'Complement.'], 'count_or')
    b.orq(6, 'honors', 'Lattice paths from (0, 0) to (5, 3) using unit steps right (R) and up (U).',
          [('How many steps does each path take?', '8'), ('How many paths are there?', str(C(8, 3))), ('How many pass through (2, 1)?', str(C(3, 1) * C(5, 2))), ('How many avoid (2, 1)?', str(C(8, 3) - C(3, 1) * C(5, 2)))],
          ['5 + 3.', 'Choose positions of the 3 U steps.', 'Multiply the two legs.', 'Complement.'], 'count_or')


# ---------------------------------------------------------------- 7. equally likely probability
def s7(b):
    PR = [('cp2', 'A fair die is rolled. Find P(even).', Fraction(3, 6)), ('cp2', 'A bag has 3 red and 5 blue marbles. One is drawn at random. Find P(red).', Fraction(3, 8)),
          ('cp1', 'Two fair dice are rolled. Find P(sum = 8).', Fraction(sum(1 for a, c in DICE if a + c == 8), 36)),
          ('cp1', 'Three fair coins are tossed. Find P(at least two heads).', Fraction(sum(1 for s in COINS3 if s.count('H') >= 2), 8)),
          ('cp1', 'One card is drawn from a standard 52-card deck. Find P(face card).', Fraction(12, 52)),
          ('honors', 'Two fair dice are rolled. Find P(the product is even).', Fraction(sum(1 for a, c in DICE if a * c % 2 == 0), 36)),
          ('honors', 'Two fair dice are rolled. Find P(the larger number is at most 3).', Fraction(sum(1 for a, c in DICE if max(a, c) <= 3), 36)),
          ('honors', 'A number is chosen at random from 1 to 100. Find P(it is divisible by 3 or 4).', Fraction(len([n for n in range(1, 101) if n % 3 == 0 or n % 4 == 0]), 100))]
    for L, t, v in PR:
        b.sa(7, L, t + ' Give a fraction in lowest terms.', frac(v), ['P(E) = (number of outcomes in E) / (number of equally likely outcomes).', 'P = %s' % frac(v)], 'equally_likely')
    MC = [('cp2', 'A spinner has 4 equal sections: red, blue, blue, green. Find P(blue).', '1/2', ['1/4', '2/3', '1/3']),
          ('cp1', 'Two fair dice are rolled. Find P(doubles).', '1/6', ['1/36', '1/12', '1/3']),
          ('honors', 'Two fair dice are rolled. Find P(sum is 7 or 11).', frac(Fraction(sum(1 for a, c in DICE if a + c in (7, 11)), 36)), ['1/6', '1/18', '5/18'])]
    for L, t, good, bad in MC:
        b.mc(7, L, t, good, bad, ['Count favorable outcomes among equally likely outcomes.', 'P = ' + good], 'equally_likely')
    b.sel(7, 'cp1', 'Two fair coins are tossed. Which statements are true?', [('P(two heads) = 1/4', True), ('P(exactly one head) = 1/2', True), ('P(at least one tail) = 3/4', True), ('P(two heads) = 1/3', False), ('The outcomes HH, one-each, TT are equally likely', False)],
          ['The four equally likely outcomes are HH, HT, TH, TT. "One head" has two outcomes, so it is twice as likely as HH.'], 'probability_select')
    b.sel(7, 'cp2', 'Which numbers could be a probability?', [('0', True), ('1/2', True), ('1', True), ('1.2', False), ('−0.3', False)], ['Probabilities are between 0 and 1 inclusive.'], 'probability_select')
    b.sel(7, 'honors', 'Two fair dice are rolled. Which events have probability 1/6?', [('sum is 7', True), ('doubles', True), ('first die shows 4', True), ('sum is 6', False), ('both dice are even', False)],
          ['6/36 each for the first three; sum 6 is 5/36; both even is 9/36.'], 'probability_select')
    b.orq(7, 'cp2', 'A bag has 4 red, 3 green and 1 yellow marble; draw one at random.',
          [('Find P(red).', '1/2'), ('Find P(green).', '3/8'), ('Find P(not yellow).', '7/8'), ('Find P(purple).', '0')],
          ['4/8.', '3/8.', '1 − 1/8.', 'Impossible.'], 'probability_or')
    b.orq(7, 'cp1', 'Two fair dice are rolled.',
          [('How many equally likely outcomes?', '36'), ('Find P(sum = 9).', '1/9'), ('Find P(sum ≥ 10).', '1/6'), ('Which sum is most likely? Give its probability.', '7, with probability 1/6')],
          ['6·6.', '4/36.', '6/36.', '6 outcomes.'], 'probability_or')
    b.orq(7, 'honors', 'Three fair coins are tossed.',
          [('List the 8 outcomes.', 'HHH, HHT, HTH, HTT, THH, THT, TTH, TTT'), ('Find P(exactly 2 heads).', '3/8'), ('Find P(at least one head).', '7/8'),
           ('A student says the outcomes are 0, 1, 2 or 3 heads, so P(2 heads) = 1/4. Explain the error.', 'Those four outcomes are not equally likely; 1 or 2 heads each happen 3 ways.')],
          ['2³.', '3 of 8.', 'Complement.', 'Equally likely outcomes are required.'], 'probability_or')


# ---------------------------------------------------------------- 8. counting rules + probability
def s8(b):
    AP = [('cp2', 'A 3-digit lock code is set at random (digits 0–9, repetition allowed). Find P(the code is 777).', Fraction(1, 1000)),
          ('cp1', 'Two cards are drawn without replacement from a standard deck. Find P(both are aces).', Fraction(C(4, 2), C(52, 2))),
          ('cp1', 'A 4-person committee is chosen at random from 6 boys and 4 girls. Find P(exactly 2 girls).', Fraction(C(4, 2) * C(6, 2), C(10, 4))),
          ('honors', 'Five cards are dealt from a standard deck. Find P(all five are hearts).', Fraction(C(13, 5), C(52, 5))),
          ('honors', 'The letters of MATH are arranged at random. Find P(the arrangement starts with M).', Fraction(1, 4)),
          ('honors', 'Four people choose seats at random in a row of 4. Find P(Ann and Bo sit next to each other).', Fraction(2 * math.factorial(3), math.factorial(4))),
          ('cp1', 'A coin is tossed 5 times. Find P(exactly 3 heads).', Fraction(C(5, 3), 32)),
          ('honors', 'Three people each pick a random integer from 1 to 10 (independently, repetition allowed). Find P(all three numbers are different).', Fraction(P(10, 3), 1000))]
    for L, t, v in AP:
        b.sa(8, L, t + ' Give a fraction in lowest terms.', frac(v), ['Count favorable outcomes and total outcomes with the same counting model (ordered or unordered).', 'P = %s' % frac(v)], 'counting_probability')
    # brute-force checks of the two seating/arrangement claims
    perms = list(itertools.permutations('ABCD'))
    assert Fraction(sum(1 for p in perms if abs(p.index('A') - p.index('B')) == 1), 24) == Fraction(1, 2)
    MC = [('cp2', 'A letter is chosen at random from the word PROBABILITY. Find P(B).', '2/11', ['1/11', '2/9', '1/5']),
          ('cp1', 'Three people are chosen at random from 5 men and 5 women. Find P(all men).', frac(Fraction(C(5, 3), C(10, 3))), ['1/8', '1/2', '1/6']),
          ('honors', 'A 3-digit number with distinct digits (100–999) is chosen at random. Find P(it is odd).', frac(Fraction(len([n for n in range(100, 1000) if n % 2 and len(set(str(n))) == 3]), 648)), ['1/2', '5/9', '4/9'])]
    for L, t, good, bad in MC:
        b.mc(8, L, t, good, bad, ['Use the same counting model for favorable and total outcomes.', 'P = ' + good], 'counting_probability')
    b.sel(8, 'cp1', 'Two cards are drawn WITHOUT replacement. Which statements are correct?', [('The number of ordered draws is 52·51', True), ('The number of unordered draws is C(52, 2)', True), ('P(two aces) = (4·3)/(52·51)', True), ('P(two aces) = (4/52)²', False), ('There are 52² ordered draws', False)],
          ['Without replacement the second draw has 51 cards; (4/52)² is the with-replacement answer.'], 'cp_select')
    b.sel(8, 'cp2', 'A fair coin is tossed 3 times. Which probabilities are correct?', [('P(HHH) = 1/8', True), ('P(no heads) = 1/8', True), ('P(exactly one head) = 3/8', True), ('P(HHH) = 1/3', False), ('P(exactly one head) = 1/8', False)],
          ['8 equally likely outcomes; exactly one head: HTT, THT, TTH.'], 'cp_select')
    b.sel(8, 'honors', 'A 5-card poker hand is dealt. Which counts are correct?', [('Hands with four aces: 48', True), ('Flushes of hearts: C(13, 5)', True), ('All hands: C(52, 5)', True), ('Hands with no hearts: 39⁵', False), ('Full houses: C(13, 2)·4·4', False)],
          ['Four aces plus any of 48 cards; no hearts is C(39, 5); full house is 13·C(4, 3)·12·C(4, 2).'], 'cp_select')
    b.orq(8, 'cp2', 'A bag has 3 red and 2 blue marbles. Two are drawn WITH replacement.',
          [('How many ordered outcomes (by marble) are there?', '25'), ('Find P(both red).', '9/25'), ('Find P(both blue).', '4/25'), ('Find P(one of each color).', '12/25')],
          ['5·5.', '3·3/25.', '2·2/25.', '1 − 9/25 − 4/25.'], 'cp_or')
    b.orq(8, 'cp1', 'Same bag (3 red, 2 blue), but two marbles are drawn WITHOUT replacement.',
          [('How many unordered outcomes?', '10'), ('Find P(both red).', '3/10'), ('Find P(both blue).', '1/10'), ('Compare with drawing with replacement.', 'Both-red drops from 9/25 to 3/10 because the second draw has fewer reds.')],
          ['C(5, 2).', 'C(3, 2)/10.', 'C(2, 2)/10.', 'Dependence.'], 'cp_or')
    b.orq(8, 'honors', 'Birthday problem: 4 people, 365 equally likely birthdays (ignore leap years; independent).',
          [('Write P(all different) as a product.', '(365·364·363·362)/365⁴'), ('Approximate P(all different) to 4 decimal places.', '%.4f' % (365 * 364 * 363 * 362 / 365 ** 4)),
           ('Find P(at least two share a birthday) to 4 decimal places.', '%.4f' % (1 - 365 * 364 * 363 * 362 / 365 ** 4)), ('State the assumptions used.', '365 equally likely days, independent birthdays, no leap day.')],
          ['Permutations over all assignments.', 'Compute.', 'Complement.', 'Model assumptions.'], 'cp_or')


def topup(b):
    b.strict_unique = True
    try:
        _topup(b)
    finally:
        b.strict_unique = False


def _topup(b):
    from core import DuplicatePrompt
    need = lambda k, L: b.counter.get((k, L), 0) < 10
    rng = seeded('u7top')
    for k in range(1, 9):
        for L in ('cp2', 'cp1', 'honors'):
            g = 0
            while need(k, L) and g < 40:
                g += 1
                try:
                    _one(b, k, L, rng)
                except DuplicatePrompt:
                    pass


def _one(b, k, L, rng):
                if k in (1, 7):
                    tgt = rng.randint(3, 11)
                    cnt = sum(1 for a, c in DICE if a + c == tgt)
                    if k == 1:
                        num_mc(b, 1, L, 'Two dice (red and blue) are rolled; outcomes are ordered pairs. How many outcomes are in the event "the sum is %d"?' % tgt, cnt, [cnt + 1, cnt - 1, 6, 36 - cnt],
                               ['List ordered pairs: ' + ', '.join('(%d,%d)' % x for x in DICE if sum(x) == tgt) + '.', '%d outcomes' % cnt], 'event')
                    else:
                        b.mc(7, L, 'Two fair dice are rolled. Find P(sum = %d).' % tgt, frac(Fraction(cnt, 36)), [frac(Fraction(cnt, 11)), frac(Fraction(cnt + 1, 36)), frac(Fraction(1, 11))],
                             ['36 equally likely ordered outcomes; %d favorable.' % cnt, 'P = %s' % frac(Fraction(cnt, 36))], 'equally_likely')
                elif k == 2:
                    m = rng.randint(5, 60); n = m + rng.randint(10, 90)
                    num_mc(b, 2, L, 'How many integers are in the list %d, %d, ..., %d?' % (m, m + 1, n), n - m + 1, [n - m, n - m + 2, n], ['n − m + 1.', '%d − %d + 1 = %d' % (n, m, n - m + 1)], 'list_count')
                elif k == 3:
                    a, c = rng.randint(2, 4), rng.randint(2, 4)
                    num_mc(b, 3, L, 'A possibility tree has %d branches at the first stage and %d branches from each first-stage node. How many leaves?' % (a, c), a * c, [a + c, a * c + a, c ** a],
                           ['Leaves = %d·%d.' % (a, c), '%d' % (a * c)], 'tree_count')
                elif k == 4:
                    x, y, z = rng.randint(2, 9), rng.randint(2, 9), rng.randint(1, 3)
                    num_mc(b, 4, L, 'A student chooses one activity: %d sports or %d clubs; %d of the options appear on both lists. How many different activities?' % (x + z, y + z, z), x + y + z, [x + y + 3 * z, x + y + 2 * z, (x + z) * (y + z)],
                           ['Inclusion-exclusion: |A ∪ B| = |A| + |B| − |A ∩ B|.', '%d + %d − %d = %d' % (x + z, y + z, z, x + y + z)], 'addition_rule')
                elif k == 5:
                    a, c, d = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 5)
                    num_mc(b, 5, L, 'A phone case comes in %d colors, %d patterns and %d sizes. How many different cases (one of each choice)?' % (a, c, d), a * c * d, [a + c + d, a * c + d, a * c * d * 2],
                           ['Multiply the choices.', '%d·%d·%d = %d' % (a, c, d, a * c * d)], 'multiplication_rule')
                elif k == 6:
                    n, r = rng.randint(5, 10), rng.randint(2, 4)
                    if rng.random() < 0.5:
                        num_mc(b, 6, L, 'How many ways can %d different trophies be awarded to %d of %d students (at most one per student)?' % (r, r, n), P(n, r), [C(n, r), n ** r, r ** n],
                               ['Order matters (different trophies): P(%d, %d).' % (n, r), str(P(n, r))], 'perm_comb')
                    else:
                        num_mc(b, 6, L, 'How many ways can %d students be chosen from %d to form a team (order does not matter)?' % (r, n), C(n, r), [P(n, r), n * r, C(n, r - 1)],
                               ['C(%d, %d).' % (n, r), str(C(n, r))], 'perm_comb')
                elif k == 8:
                    n = rng.randint(4, 7); h = rng.randint(1, n - 1)
                    b.mc(8, L, 'A fair coin is tossed %d times. Find P(exactly %d head%s).' % (n, h, '' if h == 1 else 's'), frac(Fraction(C(n, h), 2 ** n)), list(dict.fromkeys(x for x in [frac(Fraction(h, n)), frac(Fraction(1, 2 ** n)), frac(Fraction(C(n, h), n + 1)), frac(Fraction(h, 2 ** n)), '1/2'] if x != frac(Fraction(C(n, h), 2 ** n)))),
                         ['C(%d, %d) of the 2^%d equally likely sequences have exactly %d heads.' % (n, h, n, h), 'P = %s' % frac(Fraction(C(n, h), 2 ** n))], 'counting_probability')


def errors(b):
    E = b.err
    E(5, 'cp2', '3 shirts and 4 pants. How many outfits?', 'Jordan', ['3 + 4 = 7 outfits.'],
      '12', 'Jordan added instead of multiplying. An outfit needs a shirt AND pants.', '"And" in sequence → multiply; "or" → add.', ['3·4 = 12.'], 'add_vs_multiply_error')
    E(2, 'cp2', 'How many integers are in 15, 16, ..., 40?', 'Sam', ['40 − 15 = 25'],
      '26', 'Sam forgot to count both endpoints (fencepost error).', 'n − m + 1.', ['40 − 15 + 1 = 26.'], 'fencepost_error')
    E(7, 'cp2', 'Two coins: find P(one head and one tail).', 'Riley', ['Outcomes: two heads, two tails, one of each. So P = 1/3.'],
      '1/2', 'Riley used outcomes that are not equally likely; "one of each" can happen as HT or TH.', 'Use the equally likely sample space HH, HT, TH, TT.', ['2/4 = 1/2.'], 'unequal_outcomes_error')
    E(1, 'cp2', 'List the sample space for tossing a coin twice.', 'Casey', ['{H, T}'],
      '{HH, HT, TH, TT}', 'Casey listed outcomes of one toss. Each outcome must record both tosses.', 'Outcomes describe the whole experiment.', ['Two tosses → ordered pairs.'], 'sample_space_error')
    E(6, 'cp2', 'How many 2-person teams from 5 students?', 'Avery', ['5·4 = 20 teams.'],
      '10', 'Avery counted ordered pairs. Team {Ann, Bo} is the same as {Bo, Ann}.', 'Divide by 2! when order does not matter.', ['C(5, 2) = 10.'], 'order_matters_error')
    E(3, 'cp2', 'A tree: choose a drink (2 kinds) then a snack (3 kinds). How many leaves?', 'Morgan', ['The tree has 2 + 3 = 5 branches, so 5 outcomes.'],
      '6', 'Morgan counted branches instead of leaves. Each drink branch splits into 3 snack branches.', 'Leaves = complete outcomes.', ['2·3 = 6 leaves.'], 'branches_leaves_error')
    E(4, 'cp1', 'How many integers 1–50 are divisible by 2 or 5?', 'Taylor', ['25 + 10 = 35'],
      '30', 'Taylor double-counted multiples of 10, which are divisible by both.', 'Subtract the overlap.', ['25 + 10 − 5 = 30.'], 'overlap_error')
    E(8, 'cp1', 'Draw 2 cards without replacement. P(both hearts)?', 'Jamie', ['(13/52)·(13/52) = 1/16'],
      '1/17', 'Jamie assumed replacement. After one heart is drawn, 12 hearts remain among 51 cards.', 'Without replacement the draws are dependent.', ['(13/52)(12/51) = 1/17.'], 'replacement_error')
    E(6, 'cp1', 'Arrangements of the letters in LEVEL.', 'Quinn', ['5! = 120'],
      '30', 'Quinn treated repeated letters as different. The two L\'s and the two E\'s are identical.', 'Divide by the factorials of repeat counts.', ['5!/(2!·2!) = 30.'], 'repeated_letters_error')
    E(5, 'cp1', '4-digit numbers (1000–9999) with distinct digits.', 'Alex', ['10·9·8·7 = 5040'],
      '4536', 'Alex allowed 0 as the first digit, which makes a 3-digit number.', 'Handle restricted positions first.', ['9·9·8·7 = 4536.'], 'leading_zero_error')
    E(7, 'cp1', 'P(sum = 3) with two dice.', 'Jordan', ['Sums 2 to 12 are 11 outcomes, so P = 1/11.'],
      '1/18', 'Jordan treated the sums as equally likely. Sum 3 occurs as (1, 2) or (2, 1) out of 36.', 'Use the 36 ordered outcomes.', ['2/36 = 1/18.'], 'sum_equally_likely_error')
    E(1, 'cp1', 'Are "rolling an even number" and "rolling a number greater than 3" mutually exclusive on one die?', 'Sam', ['Yes; they are different events.'],
      'No; 4 and 6 are in both events', 'Sam confused "different" with "disjoint". Mutually exclusive events share no outcome.', 'Check the intersection.', ['{2, 4, 6} ∩ {4, 5, 6} = {4, 6}.'], 'exclusive_error')
    E(8, 'honors', 'P(at least one 6 in 4 rolls of a fair die).', 'Riley', ['Each roll has a 1/6 chance, so 4·(1/6) = 2/3.'],
      '671/1296', 'Riley added probabilities of overlapping events. Rolls with two 6s are counted more than once.', 'Use the complement: P(no 6) = (5/6)⁴.', ['1 − 625/1296 = 671/1296.'], 'add_overlapping_error')
    E(6, 'honors', 'Ways to give 6 identical candies to 3 kids (any may get 0).', 'Casey', ['Each candy chooses a kid: 3⁶ = 729.'],
      '28', 'Casey treated identical candies as distinct.', 'Identical objects into distinct boxes: stars and bars.', ['C(6 + 2, 2) = 28.'], 'identical_objects_error')
    E(4, 'honors', 'Bit strings of length 8 with at least one 1.', 'Avery', ['Choose a position for the 1 (8 ways), the rest free (2⁷): 8·128 = 1024.'],
      '255', 'Avery overcounted strings with several 1s (and 1024 exceeds 2⁸ = 256).', 'Use the complement.', ['2⁸ − 1 = 255.'], 'overcount_error')
    E(3, 'honors', 'Best-of-three (first to 2 wins): how many game sequences?', 'Morgan', ['Three games, each won by A or B: 2³ = 8.'],
      '6', 'Morgan assumed every match lasts 3 games. The match stops after AA or BB.', 'Trees can have unequal branches.', ['AA, BB, ABA, ABB, BAA, BAB.'], 'tree_stop_error')
    E(7, 'honors', 'A family has two children; at least one is a girl. Find P(both girls), outcomes (older, younger) equally likely.', 'Taylor', ['The other child is a boy or girl, so 1/2.'],
      '1/3', 'Taylor ignored the condition\'s effect on the sample space. Given at least one girl: GG, GB, BG remain.', 'Restrict the sample space to outcomes satisfying the condition.', ['1 of 3 equally likely outcomes.'], 'conditional_space_error')
    E(5, 'honors', 'Seat 5 people in a row with Ann and Bo NOT adjacent.', 'Jamie', ['Ann has 5 seats, Bo has 3 non-adjacent seats, others 3!: 5·3·6 = 90.'],
      '72', 'Jamie assumed Bo always has 3 non-adjacent seats; if Ann is in an end seat Bo has 3, otherwise only 2.', 'Use the complement or split into cases.', ['Total 120; adjacent 2·4! = 48; 120 − 48 = 72.'], 'case_dependent_error')


def topup2(b):
    D3 = list(itertools.product(range(1, 7), repeat=3))
    for t, f in (('the three numbers are all different', lambda x: len(set(x)) == 3), ('the sum is 10', lambda x: sum(x) == 10), ('exactly two of the dice show the same number', lambda x: len(set(x)) == 2)):
        v = sum(1 for x in D3 if f(x))
        num_mc(b, 1, 'honors', 'Three distinguishable dice are rolled; outcomes are ordered triples. How many outcomes are in the event "%s"?' % t, v, [v // 2, v + 6, 216 - v],
               ['There are 216 ordered triples; count those in the event (by cases or a short program-free listing).', '%d outcomes' % v], 'event')
    for t, f in (('the product is 12', lambda a, c: a * c == 12), ('the product is a perfect square', lambda a, c: int((a * c) ** .5) ** 2 == a * c), ('the two numbers differ by 2', lambda a, c: abs(a - c) == 2)):
        v = Fraction(sum(1 for a, c in DICE if f(a, c)), 36)
        b.mc(7, 'honors', 'Two fair dice are rolled. Find P(%s).' % t, frac(v), list(dict.fromkeys(x for x in [frac(v * 2) if v * 2 <= 1 else '1/2', frac(Fraction(v.numerator, 21)), frac(v + Fraction(1, 36)), '1/6'] if x != frac(v))),
             ['36 equally likely ordered outcomes.', 'Favorable: %d, so P = %s.' % (v * 36, frac(v))], 'equally_likely')
    num_mc(b, 3, 'honors', 'A tree shows drawing marbles without replacement from {R, R, B} (the two reds look alike) until a blue appears. How many distinct color sequences are there?', 3, [2, 4, 6],
           ['Sequences: B, RB, RRB.', '3'], 'tree_count')
