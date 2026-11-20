"""Statistics objective gaps (2026-11-19, follow-up to the 2026-11-18 audit): items for the 19 AP Statistics learning
objectives that had no question-bank practice on the pacing page (statistics-pacing/), one per level for each objective,
filed under the skill that teaches it. Short answer only, so the AP practice exams (built from multiple-choice items by
s3_print.py) do not change. Every number is computed here, with scipy for Normal and chi-square values, and checked with
assertions. Written answers are self-checked by students; s2polish.py adds their self-check lists and the CP2 hints.

Rerunning removes this script's items (marked by TAG in sourceNotes) and writes them again, so the result is the same.
retag.py keeps the objectives written here. The ids are listed in added-gaps.json.
Run from the repository root, or through run_all.sh."""
import json, os, sys
from fractions import Fraction
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib
from s2common import item, f, UNIT_OF, LEVELS

TAG = 'objective gaps 2026-11-19'
NOTE = ('Original Claude-authored item (family: {fam}). Statistics {tag}: practice for an AP objective that had none; '
        'key computed in tools/statistics-audit-20261118/gap_items.py.')
ITEMS = []   # (unit_no, skill k, objective codes, family, {level: (prompt, answer, steps)})


def add(unit_no, k, codes, fam, by_level):
    assert set(by_level) == set(LEVELS)
    ITEMS.append((unit_no, k, codes, fam, by_level))


def ordinal(n):
    n = int(n)
    return f'{n}' + ('th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))


def pct(x, d=1):
    return f(100 * x, d) + '%'


# ---------------------------------------------------------------- 1.1.B and 1.10.A: investigative questions (Unit 2, skill 1)
add(2, 1, ['1.1.B'], 'gap_investigative_question', {
    'cp2': ('The cafeteria manager at a large high school wants to find out how many of the school\'s students eat breakfast '
            'on school days. Write an investigative question the manager could answer with a survey.',
            'What proportion of students at this high school eat breakfast on school days?',
            ['An investigative question names the group (population) and the variable, and can be answered with data.',
             'Group: students at this high school. Variable: whether a student eats breakfast on school days (categorical).',
             'Question: What proportion of students at this high school eat breakfast on school days?']),
    'cp1': ('A town council wonders whether residents who live near the new bike path ride bicycles more than residents '
            'who live farther away. Write an investigative question that a statistical study could answer.',
            'Do residents who live near the bike path ride bicycles more hours per week, on average, than residents who live farther away?',
            ['Name the population (town residents), the two groups being compared (near the path, farther away) and a variable that can be measured.',
             'Bicycle riding can be measured as hours ridden per week, a quantitative variable, so the groups can be compared by their means.',
             'Question: Do residents who live near the bike path ride bicycles more hours per week, on average, than residents who live farther away?']),
    'honors': ('A student proposes this study question: "Is social media bad?" Explain why it is not a good investigative '
               'question, and rewrite it so that a study of students at her school could answer it.',
               'It names no population and no measurable variable ("bad" is not defined). Better: Is there an association between daily hours of social media use and hours of sleep on school nights for students at this school?',
               ['A good investigative question names who is studied and what is measured, and data can answer it.',
                '"Is social media bad?" names no group and no variable; "bad" cannot be measured as stated.',
                'Rewrite with a population (students at this school) and measurable variables (daily hours of social media use; hours of sleep on school nights).',
                'Question: Is there an association between daily hours of social media use and hours of sleep on school nights for students at this school?'])})

add(2, 1, ['1.10.A'], 'gap_question_components', {
    'cp2': ('Investigative question: "What is the mean number of books read last summer by seventh graders in the district?" '
            'Name the population and the variable, and say whether the variable is categorical or quantitative.',
            'Population: seventh graders in the district. Variable: number of books read last summer; quantitative.',
            ['The population is the whole group the question is about: seventh graders in the district.',
             'The variable is what is recorded for each one: number of books read last summer.',
             'A count with a meaningful mean is quantitative.']),
    'cp1': ('Investigative question: "Is the proportion of adults who recycle higher in City A than in City B?" Name the '
            'population(s), the variable, its type, and the parameter the question is about.',
            'Populations: adults in City A and adults in City B. Variable: whether an adult recycles; categorical. Parameter: the difference p_A − p_B in the proportions who recycle.',
            ['Two populations are compared: adults in City A and adults in City B.',
             'For each adult we record whether he or she recycles: a categorical (yes/no) variable.',
             'The question is about the proportions who recycle, so the parameter is p_A − p_B.']),
    'honors': ('Investigative question: "For customers of an online store, is there a relationship between the number of '
               'items in an order and the shipping time in days?" Name the population, both variables and their types, and '
               'the kind of display and statistic you would use to answer it.',
               'Population: orders (customers) of the online store. Variables: number of items (quantitative) and shipping time in days (quantitative). Use a scatterplot and the correlation r (and a regression line if the pattern is linear).',
               ['The observational units are the store\'s orders; the population is all of its orders (customers).',
                'Both variables are quantitative: number of items and shipping time in days.',
                'A relationship between two quantitative variables is shown with a scatterplot.',
                'Summarize a linear pattern with the correlation r and, if linear, a least-squares regression line.'])})


# ---------------------------------------------------------------- 1.3.A, 1.4.B, 1.4.C: one categorical variable (Unit 1, skill 6)
def rel_table(counts):
    n = sum(counts.values())
    return n, {k: Fraction(v, n) for k, v in counts.items()}


TRAVEL = {'Bus': 7, 'Car': 8, 'Walk': 3, 'Bike': 2}
n, rf = rel_table(TRAVEL)
assert n == 20 and sum(rf.values()) == 1
seq = ['Car', 'Bus', 'Walk', 'Car', 'Bus', 'Bus', 'Car', 'Bike', 'Car', 'Bus',
       'Walk', 'Car', 'Bus', 'Car', 'Bus', 'Walk', 'Car', 'Bike', 'Bus', 'Car']
assert {k: seq.count(k) for k in TRAVEL} == TRAVEL
GRADE = {'A': 18, 'B': 27, 'C': 12, 'D or F': 3}
n2, rf2 = rel_table(GRADE)
PETS = {'Dog': 46, 'Cat': 31, 'Fish': 9, 'Other': 14}
n3, rf3 = rel_table(PETS)
add(1, 6, ['1.3.A'], 'gap_relative_frequency_table', {
    'cp2': (f'Twenty students said how they get to school: {", ".join(seq)}. Make a frequency table. How many students '
            'chose each way?',
            'Bus 7, Car 8, Walk 3, Bike 2',
            ['Tally each response: Bus 7, Car 8, Walk 3, Bike 2.', 'Check: 7 + 8 + 3 + 2 = 20 responses.']),
    'cp1': (f'A teacher recorded the grade on a quiz for {n2} students: A {GRADE["A"]}, B {GRADE["B"]}, C {GRADE["C"]}, D or F '
            f'{GRADE["D or F"]}. Make a relative frequency table (each grade as a proportion of the class, two decimal places).',
            ', '.join(f'{k} {f(float(v), 2)}' for k, v in rf2.items()),
            [f'Total: {n2} students.'] + [f'{k}: {GRADE[k]}/{n2} = {f(float(v), 2)}.' for k, v in rf2.items()][:3] +
            [f'D or F: {GRADE["D or F"]}/{n2} = {f(float(rf2["D or F"]), 2)}; the proportions add to 1.']),
    'honors': (f'In a survey of {n3} households, {PETS["Dog"]} said their main pet is a dog, {PETS["Cat"]} a cat, '
               f'{PETS["Fish"]} fish and the rest another animal. Make a relative frequency table in percents, and find the '
               'percent of households whose main pet is not a dog or a cat.',
               ', '.join(f'{k} {pct(float(v), 0)}' for k, v in rf3.items()) + f'; not a dog or cat: {pct(float(rf3["Fish"] + rf3["Other"]), 0)}',
               [f'Other: {n3} − {PETS["Dog"]} − {PETS["Cat"]} − {PETS["Fish"]} = {PETS["Other"]} households.',
                'Divide each count by ' + str(n3) + ': ' + ', '.join(f'{k} {pct(float(v), 0)}' for k, v in rf3.items()) + '.',
                f'Not a dog or a cat: fish + other = {PETS["Fish"]} + {PETS["Other"]} = {PETS["Fish"] + PETS["Other"]} of {n3} = {pct(float(rf3["Fish"] + rf3["Other"]), 0)}.'])})

VOTE = {'Pizza': 27, 'Tacos': 14, 'Pasta': 9}
nv = sum(VOTE.values())
CLUB = {'Soccer': 34, 'Band': 22, 'Robotics': 19, 'Art': 25}
nc = sum(CLUB.values())
COLOR = {'Gray': 19, 'White': 31, 'Black': 26, 'Blue': 12, 'Red': 12}
ncol = sum(COLOR.values())
assert nv == 50 and nc == 100 and ncol == 100
add(1, 6, ['1.4.B'], 'gap_bar_graph_claim', {
    'cp2': (f'A bar graph shows the lunch choices of {nv} students: Pizza {VOTE["Pizza"]}, Tacos {VOTE["Tacos"]}, Pasta '
            f'{VOTE["Pasta"]}. Does the graph support the claim "More than half of these students chose pizza"? Explain.',
            f'Yes. {VOTE["Pizza"]} of {nv} = {pct(VOTE["Pizza"] / nv, 0)}, which is more than 50%.',
            [f'Half of {nv} is {nv // 2}.', f'The pizza bar is at {VOTE["Pizza"]}, and {VOTE["Pizza"]}/{nv} = {pct(VOTE["Pizza"] / nv, 0)}.',
             'That is more than half, so the graph supports the claim.']),
    'cp1': (f'A bar graph shows the after-school club of {nc} students: Soccer {CLUB["Soccer"]}, Band {CLUB["Band"]}, '
            f'Robotics {CLUB["Robotics"]}, Art {CLUB["Art"]}. A student claims "Soccer is chosen by more students than Band '
            'and Robotics together." Does the graph support the claim? Justify with the counts.',
            f'No. Band and Robotics together have {CLUB["Band"] + CLUB["Robotics"]} students, more than Soccer\'s {CLUB["Soccer"]}.',
            [f'Band + Robotics = {CLUB["Band"]} + {CLUB["Robotics"]} = {CLUB["Band"] + CLUB["Robotics"]}.',
             f'Soccer = {CLUB["Soccer"]}, which is less than {CLUB["Band"] + CLUB["Robotics"]}.',
             'The graph does not support the claim.']),
    'honors': (f'A bar graph of the colors of {ncol} cars in a lot has bars Gray {COLOR["Gray"]}, White {COLOR["White"]}, '
               f'Black {COLOR["Black"]}, Blue {COLOR["Blue"]} and Red {COLOR["Red"]}, but its vertical axis starts at 10. '
               'A dealer says the graph shows "white cars are about twice as common as gray cars." Does the data support the '
               'claim? Explain what about the graph could mislead a reader.',
               f'No. White/Gray = {COLOR["White"]}/{COLOR["Gray"]} ≈ {f(COLOR["White"] / COLOR["Gray"], 2)}, not about 2. Because the axis starts at 10, the White bar is drawn {COLOR["White"] - 10}/{COLOR["Gray"] - 10} ≈ {f((COLOR["White"] - 10) / (COLOR["Gray"] - 10), 1)} times as tall as the Gray bar, which exaggerates the difference.',
               [f'Compare the counts: {COLOR["White"]} white and {COLOR["Gray"]} gray cars; {COLOR["White"]}/{COLOR["Gray"]} ≈ {f(COLOR["White"] / COLOR["Gray"], 2)}.',
                'White cars are about 1.6 times as common, not twice as common.',
                f'With the axis starting at 10, the drawn bar heights are {COLOR["White"] - 10} and {COLOR["Gray"] - 10}, a ratio of about {f((COLOR["White"] - 10) / (COLOR["Gray"] - 10), 1)}.',
                'The truncated axis makes the difference look larger than it is, so the claim is not supported.'])})
assert abs(COLOR['White'] / COLOR['Gray'] - 1.63) < 0.01

A = {'Yes': 84, 'No': 36}
B = {'Yes': 150, 'No': 90}
pa, pb = Fraction(A['Yes'], sum(A.values())), Fraction(B['Yes'], sum(B.values()))
assert pa == Fraction(7, 10) and pb == Fraction(5, 8)
S1 = {'Phone': 45, 'Laptop': 30, 'Tablet': 25}
S2 = {'Phone': 132, 'Laptop': 54, 'Tablet': 54}
q1 = {k: Fraction(v, sum(S1.values())) for k, v in S1.items()}
q2 = {k: Fraction(v, sum(S2.values())) for k, v in S2.items()}
H1 = {'Fiction': 58, 'Nonfiction': 22, 'Graphic novel': 40}
H2 = {'Fiction': 87, 'Nonfiction': 75, 'Graphic novel': 18}
r1 = {k: Fraction(v, sum(H1.values())) for k, v in H1.items()}
r2 = {k: Fraction(v, sum(H2.values())) for k, v in H2.items()}
assert r1['Fiction'] == r2['Fiction'] and H2['Fiction'] > H1['Fiction']
add(1, 6, ['1.4.C'], 'gap_compare_categorical', {
    'cp2': (f'At School A, {A["Yes"]} of {sum(A.values())} students said yes to a later start time. At School B, {B["Yes"]} '
            f'of {sum(B.values())} said yes. School B has more "yes" answers. Which school has the greater proportion saying yes?',
            f'School A ({pct(float(pa), 0)} vs {pct(float(pb), 1)})',
            [f'School A: {A["Yes"]}/{sum(A.values())} = {pct(float(pa), 0)}.', f'School B: {B["Yes"]}/{sum(B.values())} = {pct(float(pb), 1)}.',
             'Compare proportions, not counts, when the groups have different sizes: School A is higher.']),
    'cp1': (f'A table shows the main device used for homework. Survey 1 ({sum(S1.values())} students): Phone {S1["Phone"]}, '
            f'Laptop {S1["Laptop"]}, Tablet {S1["Tablet"]}. Survey 2 ({sum(S2.values())} students): Phone {S2["Phone"]}, '
            f'Laptop {S2["Laptop"]}, Tablet {S2["Tablet"]}. A segmented bar graph shows the same data. Which survey has the '
            'greater proportion using a laptop, and by how many percentage points?',
            f'Survey 1, by {f(100 * float(q1["Laptop"] - q2["Laptop"]), 1)} percentage points ({pct(float(q1["Laptop"]), 1)} vs {pct(float(q2["Laptop"]), 1)})',
            [f'Survey 1: {S1["Laptop"]}/{sum(S1.values())} = {pct(float(q1["Laptop"]), 1)}.',
             f'Survey 2: {S2["Laptop"]}/{sum(S2.values())} = {pct(float(q2["Laptop"]), 1)}.',
             f'Difference: {f(100 * float(q1["Laptop"]), 1)} − {f(100 * float(q2["Laptop"]), 1)} = {f(100 * float(q1["Laptop"] - q2["Laptop"]), 1)} percentage points; the segmented bars show the same proportions.']),
    'honors': (f'Library 1 lent {sum(H1.values())} books last week: Fiction {H1["Fiction"]}, Nonfiction {H1["Nonfiction"]}, '
               f'Graphic novel {H1["Graphic novel"]}. Library 2 lent {sum(H2.values())}: Fiction {H2["Fiction"]}, Nonfiction '
               f'{H2["Nonfiction"]}, Graphic novel {H2["Graphic novel"]}. A side-by-side bar graph of the counts makes Library 2 '
               'look more fiction-heavy. Compare the distributions with relative frequencies and say whether that impression is right.',
               f'No. Fiction is the same share at both ({pct(float(r1["Fiction"]), 1)} vs {pct(float(r2["Fiction"]), 1)}). The real differences are graphic novels ({pct(float(r1["Graphic novel"]), 1)} vs {pct(float(r2["Graphic novel"]), 1)}) and nonfiction ({pct(float(r1["Nonfiction"]), 1)} vs {pct(float(r2["Nonfiction"]), 1)}).',
               ['Library 2 lends more books in total, so its count bars are taller; compare proportions.',
                'Library 1: ' + ', '.join(f'{k} {pct(float(v), 1)}' for k, v in r1.items()) + '.',
                'Library 2: ' + ', '.join(f'{k} {pct(float(v), 1)}' for k, v in r2.items()) + '.',
                'Fiction is the same share at both; Library 1 lends a much larger share of graphic novels and Library 2 a larger share of nonfiction.'])})


# ---------------------------------------------------------------- 1.6.B, 1.7.E, 1.9.A: comparing distributions (Unit 1, skill 4)
HIST = [(0, 10, 4), (10, 20, 9), (20, 30, 12), (30, 40, 10), (40, 50, 5)]
nh = sum(c for _, _, c in HIST)
at30 = sum(c for lo, _, c in HIST if lo >= 30)
DOT = {1: 2, 2: 5, 3: 8, 4: 6, 5: 3, 6: 1}
nd = sum(DOT.values())
le3 = sum(c for v, c in DOT.items() if v <= 3)
WAIT = [(0, 5, 22), (5, 10, 14), (10, 15, 7), (15, 20, 4), (20, 25, 2), (25, 30, 1)]
nw = sum(c for _, _, c in WAIT)
add(1, 4, ['1.6.B'], 'gap_distribution_claim', {
    'cp2': (f'A dot plot shows the number of pets owned by {nd} students: 1 pet {DOT[1]}, 2 pets {DOT[2]}, 3 pets {DOT[3]}, '
            f'4 pets {DOT[4]}, 5 pets {DOT[5]}, 6 pets {DOT[6]}. Does the dot plot support the claim "Most of these students own '
            '3 or fewer pets"? Explain.',
            f'Yes. {le3} of {nd} students ({pct(le3 / nd, 0)}) own 3 or fewer pets, which is more than half.',
            [f'Count the dots at 1, 2 and 3: {DOT[1]} + {DOT[2]} + {DOT[3]} = {le3}.', f'{le3}/{nd} = {pct(le3 / nd, 0)}, more than half.',
             'So the dot plot supports the claim.']),
    'cp1': (f'A histogram shows the minutes {nh} students spent reading on Saturday, with bars 0–10: {HIST[0][2]}, 10–20: '
            f'{HIST[1][2]}, 20–30: {HIST[2][2]}, 30–40: {HIST[3][2]}, 40–50: {HIST[4][2]} (each bar includes its left endpoint). '
            'A librarian claims "At least 40% of these students read for 30 minutes or more." Does the histogram support the claim?',
            f'No. {at30} of {nh} students ({pct(at30 / nh, 0)}) read 30 minutes or more, which is less than 40%.',
            [f'Students at 30 minutes or more: {HIST[3][2]} + {HIST[4][2]} = {at30}.', f'{at30}/{nh} = {pct(at30 / nh, 0)}.',
             'That is less than 40%, so the histogram does not support the claim.']),
    'honors': (f'A histogram of the wait times (minutes) for {nw} customers at a clinic has bars 0–5: {WAIT[0][2]}, 5–10: '
               f'{WAIT[1][2]}, 10–15: {WAIT[2][2]}, 15–20: {WAIT[3][2]}, 20–25: {WAIT[4][2]}, 25–30: {WAIT[5][2]}. The clinic '
               'advertises "a typical wait of about 15 minutes," using the midpoint of the range. Use the shape of the '
               'distribution to justify whether that is a fair description, and say which interval contains the median.',
               'Not fair. The distribution is strongly skewed right: most waits are short, and the median is in the 5–10 minute interval, not near 15 minutes.',
               [f'The counts fall from {WAIT[0][2]} to {WAIT[5][2]} as the wait grows: the distribution is skewed right.',
                f'There are {nw} customers, so the median is the average of the 25th and 26th values.',
                f'The first bar has {WAIT[0][2]} values and the first two have {WAIT[0][2] + WAIT[1][2]}, so the 25th and 26th values are in 5–10 minutes.',
                'The midpoint of the range (15) is pulled toward the few long waits; a typical wait is under 10 minutes.'])})
assert nw == 50 and WAIT[0][2] < 25 <= WAIT[0][2] + WAIT[1][2]

add(1, 4, ['1.7.E'], 'gap_compare_summaries', {
    'cp2': ('Two classes took the same test. Class A: mean 78, standard deviation 6. Class B: mean 78, standard deviation '
            '12. Both distributions are roughly symmetric. Compare the centers and the spreads.',
            'The centers are the same (mean 78). Class B has about twice the spread (SD 12 vs 6), so its scores vary more.',
            ['Center: both means are 78, so the typical score is the same.', 'Spread: SD 12 is twice SD 6.',
             'Class B\'s scores vary more from the mean than Class A\'s.']),
    'cp1': ('Weekly hours of part-time work. Group 1 (seniors): median 12, IQR 8, mean 14. Group 2 (juniors): median 9, IQR 5, '
            'mean 9.5. Group 1\'s distribution is skewed right. Compare the two groups using the statistics that suit the shapes.',
            'Use the median and IQR because Group 1 is skewed. Seniors work more hours typically (median 12 vs 9) and their hours vary more (IQR 8 vs 5).',
            ['Group 1 is skewed right, so its mean is pulled up by large values; use the resistant median and IQR.',
             'Center: median 12 for seniors vs 9 for juniors.', 'Spread: IQR 8 for seniors vs 5 for juniors.',
             'Seniors typically work more hours, and their hours are more variable.']),
    'honors': ('Delivery times (minutes) from two restaurants. Restaurant P: mean 31, median 30, SD 4, IQR 5, roughly symmetric. '
               'Restaurant Q: mean 31, median 26, SD 11, IQR 9, skewed right. A customer wants the delivery most likely to '
               'arrive within 35 minutes. Compare the distributions and recommend a restaurant, with a reason.',
               'Restaurant P. Q has a lower median (26 vs 30) but much more variability (IQR 9 vs 5, SD 11 vs 4) and a long right tail, so Q is more likely to have very late deliveries; P\'s times stay close to 30 minutes.',
               ['Compare centers with the median because Q is skewed: Q 26, P 30.', 'Compare spreads: Q has IQR 9 and SD 11; P has IQR 5 and SD 4.',
                'Q\'s right tail means more deliveries take much longer than 35 minutes.',
                'P\'s times are consistent and centered near 30, so P is the safer choice for arriving within 35 minutes.'])})

add(1, 4, ['1.9.A'], 'gap_compare_boxplots', {
    'cp2': ('Side-by-side box plots show plant heights (cm). Fertilizer: min 12, Q1 18, median 22, Q3 25, max 30. No '
            'fertilizer: min 10, Q1 13, median 16, Q3 20, max 24. Which group has the greater median, and by how much?',
            'Fertilizer, by 6 cm (22 vs 16)',
            ['Read the line inside each box: 22 cm (fertilizer) and 16 cm (no fertilizer).', '22 − 16 = 6 cm.']),
    'cp1': ('Box plots of commute times (minutes). Town X: min 8, Q1 15, median 20, Q3 24, max 31. Town Y: min 5, Q1 12, '
            'median 20, Q3 33, max 52. Compare the two distributions (center and spread).',
            'Same median (20 minutes). Town Y is more variable: IQR 21 vs 9 and range 47 vs 23.',
            ['Center: both medians are 20 minutes.', 'IQR: X 24 − 15 = 9; Y 33 − 12 = 21.', 'Range: X 31 − 8 = 23; Y 52 − 5 = 47.',
             'Town Y\'s commute times are much more spread out.']),
    'honors': ('Box plots of the number of steps (thousands) walked on a school day. Grade 9: min 3, Q1 5, median 6, Q3 8, '
               'max 15. Grade 12: min 1, Q1 3, median 5, Q3 7, max 9. Compare shape, center, spread and outliers '
               '(use the 1.5 × IQR rule).',
               'Grade 9 has a higher median (6 vs 5) and a smaller IQR (3 vs 4). Grade 9 is skewed right with a high outlier (15 > 12.5); Grade 12 is roughly symmetric with no outliers (fences −3 and 13).',
               ['Center: medians 6 (Grade 9) and 5 (Grade 12).', 'Spread: IQR 8 − 5 = 3 for Grade 9 and 7 − 3 = 4 for Grade 12.',
                'Grade 9 fences: 5 − 4.5 = 0.5 and 8 + 4.5 = 12.5, so 15 is an outlier.',
                'Grade 12 fences: 3 − 6 = −3 and 7 + 6 = 13, so there are no outliers.',
                'Grade 9 is skewed right (median near Q1, long upper tail and an outlier); Grade 12 is roughly symmetric (median centered, equal whiskers).'])})


# ---------------------------------------------------------------- 2.11.B and 2.11.F: Normal models (Unit 1, skill 5)
def zq(p):
    return round(stats.norm.ppf(p), 2)   # Table A convention: z to two decimals


z90, z25 = zq(0.90), zq(0.25)
s1 = (61.4 - 50) / z90
lo10, hi90 = 168.0, 192.0
mu3, sd3 = (lo10 + hi90) / 2, (hi90 - lo10) / (2 * zq(0.90))
assert z90 == 1.28 and z25 == -0.67
add(1, 5, ['2.11.B'], 'gap_normal_parameters', {
    'cp2': ('The weights of apples in an orchard are approximately Normal. About 68% of the apples weigh between 140 and '
            '180 grams, centered on the mean. Find the mean and standard deviation of the weights.',
            'Mean = 160 g, SD = 20 g',
            ['About 68% of a Normal distribution is within 1 SD of the mean.', 'The mean is the center: (140 + 180)/2 = 160 g.',
             'One SD is the distance from the mean to either end: 180 − 160 = 20 g.']),
    'cp1': (f'Scores on a test are approximately Normal with mean 50. The 90th percentile is 61.4. Find the standard deviation. '
            'Use Table A (z to two decimal places) and round to one decimal place.',
            f'SD ≈ {f(s1, 1)}',
            [f'The 90th percentile has z = {f(z90, 2)} (Table A).', 'z = (x − μ)/σ, so σ = (x − μ)/z.',
             f'σ = (61.4 − 50)/{f(z90, 2)} ≈ {f(s1, 1)}.']),
    'honors': (f'Heights of adult men in a country are approximately Normal. The 10th percentile is {lo10:.0f} cm and the '
               f'90th percentile is {hi90:.0f} cm. Find the mean and standard deviation. Use Table A (z to two decimal places) '
               'and round the SD to one decimal place.',
               f'Mean = {f(mu3, 0)} cm, SD ≈ {f(sd3, 1)} cm',
               [f'The 10th and 90th percentiles are symmetric about the mean: μ = ({lo10:.0f} + {hi90:.0f})/2 = {f(mu3, 0)} cm.',
                f'The 90th percentile has z = {f(z90, 2)}, so {hi90:.0f} = μ + {f(z90, 2)}σ.',
                f'σ = ({hi90:.0f} − {f(mu3, 0)})/{f(z90, 2)} ≈ {f(sd3, 1)} cm.'])})

za, zb = (88 - 80) / 5, (91 - 82) / 7
zc1, zc2 = (24.1 - 22.0) / 1.4, (13.6 - 12.4) / 0.6
zh1, zh2 = (2140 - 1800) / 250, (49 - 44) / 4.5
assert za > zb and zc2 > zc1 and zh1 > zh2
add(1, 5, ['2.11.F'], 'gap_compare_relative_position', {
    'cp2': ('Maya scored 88 on a history test (class mean 80, SD 5). Jon scored 91 on a science test (class mean 82, SD 7). '
            'Who did better relative to their class? Give both z-scores.',
            f'Maya (z = {f(za, 2)} vs {f(zb, 2)})',
            [f'Maya: z = (88 − 80)/5 = {f(za, 2)}.', f'Jon: z = (91 − 82)/7 ≈ {f(zb, 2)}.',
             'A larger z-score means farther above the class mean, so Maya did better relative to her class.']),
    'cp1': ('Two swimmers in different events. Lena swam 100 m freestyle in 24.1 s (event mean 22.0 s, SD 1.4 s). Rosa swam '
            '50 m freestyle in 13.6 s (event mean 12.4 s, SD 0.6 s). Lower times are better. Who did better relative to her '
            'event? Give both z-scores (two decimal places).',
            f'Lena (z = {f(zc1, 2)} vs {f(zc2, 2)})',
            [f'Lena: z = (24.1 − 22.0)/1.4 = {f(zc1, 2)}.', f'Rosa: z = (13.6 − 12.4)/0.6 = {f(zc2, 2)}.',
             'Lower times are better, so the smaller z-score (fewer SDs slower than average) is better: Lena.']),
    'honors': ('A college compares two applicants. Ana scored 2140 on an exam with mean 1800 and SD 250. Ben scored 49 on a '
               'different exam with mean 44 and SD 4.5. Both distributions are approximately Normal. Who scored better relative '
               'to the other test takers, and what percentile is each score? Use z to two decimal places and Table A.',
               f'Ana. Her z-score of {f(zh1, 2)} (about the {ordinal(f(100 * stats.norm.cdf(round(zh1, 2)), 0))} percentile) is higher than Ben\'s {f(zh2, 2)} (about the {ordinal(f(100 * stats.norm.cdf(round(zh2, 2)), 0))} percentile).',
               [f'Ana: z = (2140 − 1800)/250 = {f(zh1, 2)}.', f'Ben: z = (49 − 44)/4.5 ≈ {f(zh2, 2)}.',
                f'Table A: P(Z < {f(zh1, 2)}) ≈ {f(stats.norm.cdf(round(zh1, 2)), 4)} and P(Z < {f(zh2, 2)}) ≈ {f(stats.norm.cdf(round(zh2, 2)), 4)}.',
                'Ana\'s score is farther above its mean in SDs, so she did better relative to the other test takers.'])})


# ---------------------------------------------------------------- 3.9.B and 4.6.B: conditions for differences (Unit 3, skill 9)
add(3, 9, ['3.9.B'], 'gap_conditions_two_proportions', {
    'cp2': ('Random samples of 200 students from School A and 150 from School B are taken; each school has more than 3,000 '
            'students. In the populations, 30% of A and 40% of B ride the bus. Check the Large Counts condition for the sampling '
            'distribution of p̂_A − p̂_B.',
            'Met: 200(0.30) = 60, 200(0.70) = 140, 150(0.40) = 60, 150(0.60) = 90 are all at least 10.',
            ['Large Counts needs n₁p₁, n₁(1 − p₁), n₂p₂ and n₂(1 − p₂) all at least 10.',
             'School A: 200(0.30) = 60 and 200(0.70) = 140.', 'School B: 150(0.40) = 60 and 150(0.60) = 90.',
             'All four are at least 10, so the sampling distribution of p̂_A − p̂_B is approximately Normal.']),
    'cp1': ('A researcher takes independent random samples of 80 adults from a city of 50,000 and 60 adults from a town of '
            '500. In the populations, 15% of city adults and 10% of town adults bike to work. Check the Random, 10% and Large '
            'Counts conditions for the sampling distribution of p̂_city − p̂_town.',
            'Random: met (independent random samples). 10%: met for the city (80 ≤ 5,000) but not the town (60 > 50). Large Counts: not met for the town, 60(0.10) = 6 < 10 (city: 12 and 68; town: 54).',
            ['Random: independent random samples from each population, so met.',
             '10%: city 80 ≤ 0.10(50,000) = 5,000, met; town 60 > 0.10(500) = 50, not met.',
             'Large Counts: city 80(0.15) = 12 and 80(0.85) = 68; town 60(0.10) = 6 and 60(0.90) = 54.',
             'The town count 6 is below 10, so the Normal model for p̂_city − p̂_town is not justified.']),
    'honors': ('In a randomized experiment, 120 volunteers are randomly assigned to a new allergy medicine and 120 to a '
               'placebo. Assume the true proportions with relief are 0.55 and 0.35. Justify whether the sampling distribution '
               'of p̂_new − p̂_placebo is approximately Normal, and explain why the 10% condition is not needed here.',
               'Approximately Normal: 120(0.55) = 66, 120(0.45) = 54, 120(0.35) = 42, 120(0.65) = 78 are all at least 10. The 10% condition is for sampling without replacement from a population; here the groups come from random assignment of volunteers, so independence comes from the random assignment.',
               ['Random: the treatments were randomly assigned.',
                'Large Counts: 66, 54, 42 and 78 are all at least 10, so the distribution is approximately Normal.',
                'The 10% condition checks sampling without replacement from a population; there is no such sampling here.',
                'Random assignment makes the two groups independent, so the condition does not apply.'])})

add(3, 9, ['4.6.B'], 'gap_conditions_two_means', {
    'cp2': ('Independent random samples of 40 boys and 45 girls are taken from a large school to compare mean hours of sleep. '
            'The population distributions are unknown. Is the sampling distribution of x̄_boys − x̄_girls approximately Normal? Explain.',
            'Yes. Both samples are at least 30 (40 and 45), so by the Central Limit Theorem each x̄, and their difference, is approximately Normal.',
            ['With unknown population shapes, each sample needs n ≥ 30 (CLT).', 'n_boys = 40 and n_girls = 45 are both at least 30.',
             'So x̄_boys − x̄_girls is approximately Normal.']),
    'cp1': ('A company takes independent random samples of 12 batteries of Brand A and 15 of Brand B. Lifetimes of Brand A are '
            'known to be Normal; Brand B\'s sample dot plot is strongly skewed right with an outlier. Justify whether the '
            'sampling distribution of x̄_A − x̄_B can be treated as Normal.',
            'No. Brand A is fine (Normal population), but Brand B\'s sample is small (15 < 30) and strongly skewed with an outlier, so x̄_B, and the difference, may not be Normal.',
            ['Each sample mean must be approximately Normal.', 'Brand A: the population is Normal, so x̄_A is Normal for any n.',
             'Brand B: n = 15 < 30, and the data are strongly skewed with an outlier.',
             'The condition fails for Brand B, so the difference cannot be treated as Normal.']),
    'honors': ('Researchers compare mean reaction times for two age groups using independent random samples of 25 teens (from '
               '2,000 at a school) and 25 adults (from a city of 80,000). Both sample dot plots are roughly symmetric with no '
               'outliers. Check every condition for the sampling distribution of x̄_teens − x̄_adults.',
               'Random: independent random samples, met. 10%: 25 ≤ 200 teens and 25 ≤ 8,000 adults, met. Normal: n = 25 < 30 for both, but both samples are roughly symmetric with no outliers, so the populations are plausibly Normal and the difference is approximately Normal.',
               ['Random: two independent random samples.', '10%: 25 ≤ 0.10(2,000) = 200 and 25 ≤ 0.10(80,000) = 8,000.',
                'Normal/Large sample: both n = 25 < 30, so look at the data.',
                'Both dot plots are roughly symmetric with no outliers, so the condition is reasonably met.'])})


# ---------------------------------------------------------------- 3.14.D and 3.15.C: chi-square (Unit 4, skill 13)
def expected(table):
    rows, cols = [sum(r) for r in table], [sum(c) for c in zip(*table)]
    n = sum(rows)
    return [[Fraction(rows[i] * cols[j], n) for j in range(len(cols))] for i in range(len(rows))]


T1 = [[30, 20, 10], [25, 30, 15]]
E1 = expected(T1)
T2 = [[12, 9, 4], [18, 11, 6]]
E2 = expected(T2)
T3 = [[40, 25, 15, 6], [35, 30, 20, 9]]
E3 = expected(T3)
m1, m2, m3 = min(map(min, E1)), min(map(min, E2)), min(map(min, E3))
assert m1 >= 5 and m2 < 5 and m3 >= 5
add(4, 13, ['3.14.D'], 'gap_chisq_conditions', {
    'cp2': ('A random sample of 130 adults was classified by age group and favorite season. The smallest expected count in '
            f'the two-way table is {f(float(m1), 2)}. Is the Large Counts condition for a chi-square test met? Explain.',
            f'Yes. All expected counts are at least 5 (the smallest is {f(float(m1), 2)}).',
            ['The Large Counts condition for chi-square tests needs every expected count to be at least 5.',
             f'The smallest expected count is {f(float(m1), 2)}, which is at least 5, so all are.', 'The condition is met.']),
    'cp1': ('A random sample of 60 students was classified by grade (rows) and lunch choice (columns). Observed counts: '
            'Grade 9: 12, 9, 4; Grade 10: 18, 11, 6. Find the smallest expected count and say whether the chi-square test '
            'for independence is appropriate.',
            f'Smallest expected count ≈ {f(float(m2), 2)}, which is less than 5, so the Large Counts condition is not met and the test is not appropriate.',
            ['Expected count = (row total)(column total)/(table total).',
             f'Row totals 25 and 35; column totals 30, 20 and 10; total 60.',
             f'Smallest: (25)(10)/60 ≈ {f(float(m2), 2)}.', 'It is below 5, so the chi-square test is not appropriate.']),
    'honors': ('Independent random samples of 86 customers from Store 1 and 94 from Store 2 were asked their preferred '
               'payment (card, phone, cash, check): Store 1: 40, 25, 15, 6; Store 2: 35, 30, 20, 9. Each store has thousands '
               'of customers. Check all the conditions for a chi-square test for homogeneity.',
               f'Random: independent random samples, met. 10%: 86 and 94 are less than 10% of each store\'s thousands of customers, met. Large Counts: the smallest expected count is (86)(15)/180 ≈ {f(float(m3), 2)}, at least 5, so all expected counts are at least 5. The test is appropriate.',
               ['Random: independent random samples from the two stores.', '10%: each sample is less than 10% of the store\'s customers.',
                'Expected counts: (row total)(column total)/180; the smallest uses the check column (15).',
                f'(86)(15)/180 ≈ {f(float(m3), 2)} ≥ 5, so every expected count is at least 5.'])})

add(4, 13, ['3.15.C'], 'gap_chisq_pvalue', {
    'cp2': ('A chi-square test for independence of grade level and favorite sport gives a p-value of 0.03. Interpret the '
            'p-value.',
            'Assuming grade level and favorite sport are independent, there is a 0.03 probability of getting a chi-square statistic as large as or larger than the one observed, by chance alone.',
            ['A p-value is a probability calculated assuming the null hypothesis is true.',
             'H₀: grade level and favorite sport are independent (no association).',
             'P = 0.03 is the chance of a χ² value at least as large as the observed one if H₀ were true.']),
    'cp1': ('Independent random samples of voters from three districts were asked whether they support a park levy. A '
            'chi-square test for homogeneity gives χ² = 7.92 with df = 2 and a p-value of 0.019. Interpret the p-value in context '
            'and state a conclusion at α = 0.05.',
            'If the distribution of support were the same in all three districts, there would be a 0.019 probability of getting χ² = 7.92 or larger by chance. Since 0.019 < 0.05, reject H₀: there is convincing evidence that support differs among the districts.',
            ['H₀: the distribution of support is the same in the three districts.',
             'Assuming H₀, P(χ² ≥ 7.92) with df = 2 is 0.019.', 'p-value 0.019 < α = 0.05, so reject H₀.',
             'There is convincing evidence that the distribution of support differs among the districts.']),
    'honors': (f'A random sample of adults was classified by exercise level and sleep quality. A chi-square test for '
               f'independence gives χ² = 5.40 with df = 4. Find the p-value, interpret it, and explain why "the p-value is the '
               'probability that exercise and sleep are independent" is not a correct interpretation.',
               f'p-value ≈ {f(stats.chi2.sf(5.40, 4), 3)}. If exercise level and sleep quality were independent, there would be about a {f(stats.chi2.sf(5.40, 4), 3)} probability of getting χ² ≥ 5.40 by chance. The p-value is computed assuming H₀ is true, so it is not the probability that H₀ is true.',
               [f'P(χ² ≥ 5.40) with df = 4 ≈ {f(stats.chi2.sf(5.40, 4), 3)} (technology).',
                'Interpretation: assuming independence, a statistic this large or larger happens with that probability by chance.',
                'The p-value is a probability about the data given H₀, not about H₀ itself.',
                'With a p-value this large, there is not convincing evidence of an association.'])})


# ---------------------------------------------------------------- 4.3.B: claim from a t-interval (Unit 4, skill 4)
add(4, 4, ['4.3.B'], 'gap_t_interval_claim', {
    'cp2': ('A 95% confidence interval for the mean amount of soda in "20-ounce" bottles is 19.6 to 19.9 ounces. Does the '
            'interval support the claim that the mean is 20 ounces? Explain.',
            'No. 20 is not in the interval (19.6, 19.9); all plausible values for the mean are below 20 ounces.',
            ['A confidence interval gives the plausible values of the population mean.', '20 is above 19.9, so it is not in the interval.',
             'The interval suggests the mean is less than 20 ounces.']),
    'cp1': ('A 90% t-interval for the mean daily screen time of students at a school is (4.1, 5.3) hours. The principal '
            'claims students average more than 4 hours a day. A parent claims the mean is 5 hours. Which claims does the '
            'interval support? Explain.',
            'Both are plausible. Every value in (4.1, 5.3) is more than 4, which supports the principal; 5 is inside the interval, so 5 hours is plausible, but so are other values.',
            ['All values in the interval are plausible values of μ.', 'The whole interval is above 4, so "more than 4 hours" is supported.',
             '5 is inside the interval, so μ = 5 is plausible; the interval does not prove it equals 5.']),
    'honors': ('A paired study of 18 runners gives a 95% t-interval for the mean difference in 5K time (old shoes − new '
               'shoes) of (−0.4, 1.8) minutes. The shoe company claims the new shoes make runners faster. Does the interval '
               'support the claim? What would a 99% interval look like?',
               'No. The interval includes 0 (and negative values), so "no difference" is plausible; there is not convincing evidence the new shoes are faster. A 99% interval would be wider and would still include 0.',
               ['μ_diff > 0 would mean the old-shoe time is longer, so the new shoes are faster.',
                'The interval (−0.4, 1.8) contains 0 and negative values.', 'So the data do not give convincing evidence that the new shoes help.',
                'A higher confidence level gives a wider interval around the same center, so it would also contain 0.'])})


# ---------------------------------------------------------------- 4.7.A, 4.7.B, 4.9.C: two-sample t (Unit 4, skill 10)
add(4, 10, ['4.7.A'], 'gap_identify_two_sample_interval', {
    'cp2': ('A researcher takes independent random samples of 35 fourth graders and 35 eighth graders and records hours of '
            'sleep. She wants to estimate how much more sleep fourth graders get, on average. Name the procedure and the parameter.',
            'Two-sample t-interval for μ₄ − μ₈, the difference in mean hours of sleep (fourth graders minus eighth graders).',
            ['Two independent groups, a quantitative variable (hours), and the goal is to estimate: a two-sample t-interval.',
             'Parameter: μ₄ − μ₈, mean sleep of all fourth graders minus mean sleep of all eighth graders.']),
    'cp1': ('Twenty volunteers are randomly assigned, 10 to a new study method and 10 to the usual method, and their test '
            'scores are recorded. The teacher wants to estimate the difference in mean scores. Name the procedure, define the '
            'parameter, and explain why it is not a paired procedure.',
            'Two-sample t-interval for μ_new − μ_usual (the difference in true mean scores for the two methods). It is not paired because each volunteer gets only one method; the groups are separate.',
            ['Two separate groups formed by random assignment, a quantitative response, and an estimate: two-sample t-interval.',
             'Parameter: μ_new − μ_usual, the true mean score with the new method minus the true mean score with the usual method.',
             'A paired procedure needs two measurements on the same individual or matched pairs; here each volunteer has one score.']),
    'honors': ('A nutritionist wants to estimate how much the mean sodium content differs between two brands of canned soup. '
               'Plan 1: measure 20 randomly chosen cans of each brand. Plan 2: for 20 soup flavors, measure one can of each '
               'brand. Name the correct interval procedure and parameter for each plan.',
               'Plan 1: two-sample t-interval for μ_A − μ_B (difference in mean sodium of all cans of the two brands). Plan 2: paired t-interval for μ_diff, the mean of the flavor-by-flavor differences (Brand A − Brand B).',
               ['Plan 1 uses two independent samples, so use a two-sample t-interval for μ_A − μ_B.',
                'Plan 2 matches the cans by flavor, so the data are paired.',
                'For paired data, take the difference for each flavor and use a one-sample t-interval for the mean difference μ_diff.'])})

add(4, 10, ['4.7.B'], 'gap_conditions_two_sample_interval', {
    'cp2': ('Independent random samples of 40 cars from Lot A and 36 from Lot B (each lot has hundreds of cars) are used to '
            'estimate the difference in mean mileage. Check the Random, 10% and Normal/Large Sample conditions for a '
            'two-sample t-interval.',
            'Random: independent random samples, met. 10%: 40 and 36 are each less than 10% of hundreds of cars, met. Large Sample: 40 ≥ 30 and 36 ≥ 30, met.',
            ['Random: independent random samples from the two lots.', '10%: each sample is less than 10% of its lot.',
             'Normal/Large Sample: both sample sizes are at least 30.']),
    'cp1': ('Fourteen plants were randomly assigned to two light conditions, 7 each, and growth (cm) was recorded. Each '
            'group\'s dot plot is roughly symmetric with no outliers. Check the conditions for a two-sample t-interval.',
            'Random: random assignment, met. 10%: not needed for random assignment. Normal: n = 7 < 30 in each group, but both dot plots are roughly symmetric with no outliers, so the condition is reasonably met.',
            ['Random: the plants were randomly assigned to conditions.', '10%: not needed, because there is no sampling without replacement.',
             'Normal: both samples are small, so check the data: roughly symmetric with no outliers in each group.']),
    'honors': ('A study compares mean monthly phone bills for adults under 30 and over 50 using random samples of 22 and '
               '25 from a city. A boxplot of the under-30 sample shows two high outliers and strong right skew; the over-50 '
               'boxplot is roughly symmetric. Can a two-sample t-interval be used? What could the researcher do?',
               'Not safely. The under-30 sample is small (22 < 30) and strongly skewed with outliers, so the Normal condition fails for that group. The researcher could take a larger sample (at least 30 in each group) or use a method that does not assume Normality.',
               ['Each group must satisfy the Normal/Large Sample condition.', 'Over 50: n = 25 < 30, but the data are roughly symmetric, so it is reasonable.',
                'Under 30: n = 22 < 30 with strong skew and outliers, so the condition fails.',
                'A larger sample (n ≥ 30 in each group) would let the Central Limit Theorem justify the procedure.'])})

add(4, 10, ['4.9.C'], 'gap_conditions_two_sample_test', {
    'cp2': ('A teacher randomly assigns 32 students to a quiz with music and 32 to a quiz without music to test whether mean '
            'scores differ. Check the conditions for a two-sample t-test.',
            'Random: random assignment, met. 10%: not needed for an experiment. Large Sample: 32 ≥ 30 in each group, met.',
            ['Random: the students were randomly assigned to the two conditions.', '10%: not needed, because there is no sampling from a population.',
             'Large Sample: both groups have 32 ≥ 30.']),
    'cp1': ('To test whether mean commute times differ between two towns, a planner surveys every resident who answers the '
            'phone on one morning: 45 in Town A and 50 in Town B. Is the Random condition for a two-sample t-test met? Explain.',
            'No. The samples are not random: they include only residents who answered the phone that morning, a convenience sample that may differ from each town\'s population.',
            ['The Random condition needs random samples from each population (or random assignment).',
             'Calling and keeping whoever answers is not a random sample of residents.', 'The results may not represent the towns, so the condition is not met.']),
    'honors': ('A researcher tests whether a coaching program raises mean SAT math scores. Independent random samples: 28 '
               'coached students (from 600) and 26 uncoached students (from 900). Both sample dot plots are slightly skewed '
               'with no outliers. Check every condition for the two-sample t-test and state whether a cause-and-effect '
               'conclusion would be justified.',
               'Random: independent random samples, met. 10%: 28 ≤ 60 and 26 ≤ 90, met. Normal: both n < 30, but only slight skew and no outliers, so reasonably met. The test can be done, but this is an observational study (no random assignment), so a significant result would not show that coaching causes higher scores.',
               ['Random: independent random samples from the two groups.', '10%: 28 ≤ 0.10(600) = 60 and 26 ≤ 0.10(900) = 90.',
                'Normal: both samples are under 30 but show no strong skew or outliers.',
                'Without random assignment, a difference could be due to other variables, so no cause-and-effect conclusion.'])})


# ---------------------------------------------------------------- 5.1.A: construct a scatterplot (Unit 1, skill 7)
FT = [(50, 60), (80, 65), (120, 70), (150, 78), (200, 74), (250, 85)]
_xb = sum(x for x, _ in FT) / len(FT); _yb = sum(y for _, y in FT) / len(FT)
_b = sum((x - _xb) * (y - _yb) for x, y in FT) / sum((x - _xb) ** 2 for x, _ in FT)
_res = {x: y - (_yb + _b * (x - _xb)) for x, y in FT}
assert min(_res, key=_res.get) == 200 and _b > 0   # (200, 74%) is farthest below the least-squares line
add(1, 7, ['5.1.A'], 'gap_construct_scatterplot', {
    'cp2': ('A student recorded hours studied and test score for 5 classmates: (1, 64), (2, 70), (3, 75), (4, 82), (5, 88), '
            'written as (hours, score). To make a scatterplot, which variable goes on the horizontal axis, and where is the point '
            'for the student who studied 4 hours?',
            'Hours studied (explanatory) on the horizontal axis; the point is at (4, 82).',
            ['Put the explanatory variable (hours studied) on the horizontal axis and the response (score) on the vertical axis.',
             'The student who studied 4 hours scored 82, so plot the point (4, 82).']),
    'cp1': ('Data on outdoor temperature (°F) and number of hot chocolates sold at a stand: 30°F, 52 sold; 40°F, 41; 50°F, 33; '
            '60°F, 20; 70°F, 12. Describe how to construct a scatterplot of the data (axes, labels, scales) and give the '
            'coordinates of the five points.',
            'Temperature (°F, explanatory) on the horizontal axis from about 25 to 75; hot chocolates sold on the vertical axis from 0 to 60; label both axes with units. Points: (30, 52), (40, 41), (50, 33), (60, 20), (70, 12).',
            ['Temperature explains sales, so it goes on the horizontal axis; sales go on the vertical axis.',
             'Choose scales that cover the data: about 25–75 °F and 0–60 sold, with equal spacing.',
             'Label both axes with the variable and its units.', 'Plot (30, 52), (40, 41), (50, 33), (60, 20), (70, 12).']),
    'honors': ('A coach records, for 6 players, the number of practice free throws in a week and the free-throw percentage in '
               'the next game: 50, 60%; 80, 65%; 120, 70%; 150, 78%; 200, 74%; 250, 85%. A student makes a scatterplot with '
               'percentage on the horizontal axis and starts the vertical axis at 50. Explain what should be changed and why, '
               'and name the point that will lie farthest below the overall upward trend.',
               'Put practice free throws (explanatory) on the horizontal axis and percentage (response) on the vertical axis, with scales that cover the data and labels with units. The point (200, 74%) lies below the trend: it is lower than the player with 150 practice shots.',
               ['The explanatory variable (practice shots) should be on the horizontal axis; the response (percentage) on the vertical axis.',
                'Use scales that cover 50–250 shots and about 55%–90%, and label both axes.',
                'The percentages rise with practice except at 200 shots: 74% is below the 78% at 150 shots.',
                'So (200, 74%) lies farthest below the upward trend.'])})


def main():
    banks = lib.load()
    added = []
    for u in banks:
        banks[u]['questions'] = [q for q in banks[u]['questions'] if TAG not in q.get('sourceNotes', '')]
    seen = {(q['skillId'], q['prompt']) for _, q in lib.items(banks)}
    count = {}
    for unit_no, k, codes, fam, by_level in ITEMS:
        u = UNIT_OF[unit_no]
        for lv in LEVELS:
            prompt, answer, steps = by_level[lv]
            n = count[(u, k, lv)] = count.get((u, k, lv), 0) + 1
            qid = f'stat-u{unit_no}-s{k:02d}-{lv}-o{n:02d}'
            q = item(qid, unit_no, k, lv, 'short-answer', prompt, answer, steps, codes, fam)
            q['sourceNotes'] = NOTE.format(fam=fam, tag=TAG)
            assert (q['skillId'], prompt) not in seen, qid
            seen.add((q['skillId'], prompt))
            qs = banks[u]['questions']
            last = max(i for i, x in enumerate(qs) if x['skillId'] == q['skillId'])
            qs.insert(last + 1, q)
            added.append(qid)
    lib.save(banks)
    json.dump(sorted(added), open(os.path.join(HERE, 'added-gaps.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'added-gaps.json'), 'a').write('\n')
    print(f'objective-gap items: {len(added)} ({len(ITEMS)} objectives × 3 levels)')


if __name__ == '__main__':
    main()
