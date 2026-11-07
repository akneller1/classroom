from common import *
from math import comb

U = "anticipating-patterns"
PA, PB, PC, PD = "APSTATS.III.A", "APSTATS.III.B", "APSTATS.III.C", "APSTATS.III.D"


def mcs(k, level, rows, fam, std):
    for prompt, correct, wrongs, steps in rows:
        MC(U, k, level, prompt, correct, wrongs, steps, family=fam, std=std)


def bsum(n, p, lo, hi):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(lo, hi + 1))


def s01():
    k, sd_ = 1, [PA + ".1", PA + ".2"]
    mcs(k, "cp2", [
        ("A weather forecast says there is a 30% chance of rain tomorrow. What does this mean?",
         "On many days with conditions like tomorrow's, it rains on about 30% of them.", ["It will rain for 30% of the day.", "It will rain in 30% of the area for sure.", "It will not rain, because 30% is less than 50%."],
         ["Probability is a long-run relative frequency over many similar situations."]),
        ("Which number could NOT be a probability?",
         "1.2", ["0", "0.5", "1"], ["Probabilities are between 0 and 1 inclusive."]),
        ("A spinner is spun 20 times and lands on blue 9 times. What is the relative frequency of blue?",
         "0.45", ["9", "0.09", "0.55"], ["Relative frequency = 9/20 = 0.45."]),
        ("A fair die is rolled 6 times and shows a 4 three times. What does the law of large numbers say?",
         "Over many more rolls, the proportion of 4s will get close to 1/6.", ["The die is unfair.", "The next roll is less likely to be a 4.", "In 6 more rolls, there will be exactly one 4."],
         ["Short runs vary a lot; the long-run proportion approaches the true probability."]),
        ("An event has probability 0.02. Which description fits?",
         "It is very unlikely but can happen; it would occur about 2 times in 100 trials in the long run.", ["It is impossible.", "It will happen exactly 2 times in every 100 trials.", "It is certain."],
         ["Small probabilities describe rare events in the long run."]),
    ], "u3_interpret_prob", sd_)
    SA(U, k, "cp2", "A basketball player made 162 of her last 200 free throws. Estimate the probability that she makes her next free throw, and explain what the estimate means.",
       "About 0.81; in the long run she makes about 81% of her free throws",
       ["Relative frequency = 162/200 = 0.81.", "The estimate describes her long-run success rate, not a guarantee for the next shot."],
       family="u3_relfreq_estimate", std=sd_, check={"kind": "ratio", "num": 162, "den": 200})
    mcs(k, "cp1", [
        ("A coin is tossed 10 times and lands heads 7 times; later it is tossed 1,000 times and lands heads 512 times. Which statement is best supported?",
         "The 1,000-toss proportion (0.512) is a much better estimate of P(heads) than the 10-toss proportion (0.7).", ["The coin is biased toward heads because 0.7 > 0.5.", "The proportion of heads should be exactly 0.5 after 1,000 tosses.", "The 10-toss result is more reliable because it is more recent."],
         ["The law of large numbers: relative frequency settles near the true probability as trials increase."]),
        ("Which is an example of the gambler's fallacy?",
         "After five losses in a row on a fair game, believing a win is now “due.”", ["Estimating a probability from 1,000 trials.", "Saying a fair die has probability 1/6 of showing 3.", "Expecting about half heads in 10,000 coin tosses."],
         ["Independent trials have no memory; past results do not change future probabilities."]),
        ("Two hospitals each record the proportion of births that are boys on each day. One hospital has about 15 births a day, the other about 150. Which will have more days on which over 60% of births are boys?",
         "The smaller hospital", ["The larger hospital", "Both about the same", "Neither; it cannot happen"],
         ["Proportions from small numbers of trials vary more from the long-run value."]),
        ("The probability that a randomly chosen adult is left-handed is 0.10. In a group of 50 randomly chosen adults, which statement is true?",
         "The number of left-handed adults will vary, but about 5 is expected on average.", ["Exactly 5 will be left-handed.", "At least 10 will be left-handed.", "None can be left-handed if the first 10 are right-handed."],
         ["0.10 × 50 = 5 is a long-run average; actual counts vary."]),
    ], "u3_lln", sd_)
    SEL(U, k, "cp1", "Select ALL statements consistent with the law of large numbers.",
        ["As the number of coin tosses increases, the proportion of heads tends to get closer to 0.5.", "A casino can predict its long-run earnings even though single bets are unpredictable."],
        ["After 10 tails in a row, heads becomes more likely.", "In 100 tosses of a fair coin, there will be exactly 50 heads."],
        ["LLN concerns long-run proportions; it does not make single outcomes predictable or compensate for streaks."], family="u3_lln_sel", std=sd_)
    mcs(k, "honors", [
        ("After 1,000 tosses of a fair coin, there are 520 heads. As tossing continues to 100,000, what most likely happens?",
         "The proportion of heads gets closer to 0.5, even though the difference between the number of heads and tails may not shrink.", ["Tails must catch up so the counts become equal.", "The proportion stays at 0.52.", "The proportion of heads will move further from 0.5."],
         ["LLN works by swamping, not compensating: the proportion converges while the count difference can grow."]),
        ("An insurance company sells 100,000 policies, each with a small chance of a large claim. Why can the company set prices confidently?",
         "With many independent policies, the proportion of claims will be close to the long-run probability, making total payouts predictable.", ["Because no claims will occur.", "Because each customer pays exactly the expected claim.", "Because claims are not random."],
         ["Large numbers of independent trials make averages stable (law of large numbers)."]),
        ("A student says, “The probability of rolling a 6 is 1/6, so in 60 rolls I'll get exactly ten 6s.” What is the best correction?",
         "About ten 6s is expected on average, but the actual count varies from one set of 60 rolls to another.", ["The probability changes after each roll.", "You will get exactly ten 6s only if the die is fair.", "Probability does not apply to 60 rolls."],
         ["Expected counts are long-run averages, not guarantees."]),
    ], "u3_lln_honors", sd_)
    OR(U, k, "honors", "A class tossed a thumbtack 500 times. The cumulative proportion of “point up” after 10, 50, 100, 250, and 500 tosses was 0.70, 0.58, 0.63, 0.61, and 0.616.",
       [("How many tosses landed point up in all 500 tosses?", "308"),
        ("Estimate the probability of “point up” and explain why the 500-toss value is used.", "About 0.616; the long-run proportion over many tosses is the best estimate"),
        ("Why was the proportion after 10 tosses so far from the later values?", "With few trials, proportions vary a lot by chance"),
        ("If the class tossed 2,000 more times, describe what you would expect the cumulative proportion to do.", "Stay close to about 0.6, varying less and less (law of large numbers)")],
       ["1 point each part."], family="u3_lln_or", std=sd_, check={"kind": "product", "values": [0.616, 500], "expect": 308})
    SA(U, k, "honors", "In 1,000 rolls of a die, the face 6 came up 210 times. Compare 210 with the number expected for a fair die, and explain what further evidence would help decide whether the die is unfair.",
       "Expected about 166.7 sixes; 210 is about 43 more, which seems unusually high, but a formal test or many more rolls would be needed to decide.",
       ["Expected count = 1,000 × 1/6 ≈ 166.7.", "210 − 166.7 ≈ 43 extra sixes.", "Some variation is expected, so judge whether 43 is unusually large (e.g., by simulation or a significance test).", "More rolls would make the estimate of P(6) more precise."],
       family="u3_unfair_die", std=sd_, check={"kind": "product", "values": [1000, 1 / 6], "no_print_check": "1/6 implied by a fair die", "tol": 0.05})


def s02():
    k, sd_ = 2, [PA + ".3"]
    for lv, pa, pb, pab, ctx, ask in [("cp2", 0.45, 0.30, 0.12, "At a school, 45% of students play a sport, 30% are in a club, and 12% do both.", "Find P(sport or club)."),
                                      ("cp1", 0.58, 0.40, 0.25, "In a town, 58% of households have a dog, 40% have a cat, and 25% have both.", "Find P(dog or cat).")]:
        u = pa + pb - pab
        num_mc(U, k, lv, ctx + " " + ask, u, [pa + pb, pab, pa * pb], 2,
               ["General addition rule: P(A or B) = P(A) + P(B) − P(A and B).", f"= {fmt(pa)} + {fmt(pb)} − {fmt(pab)} = {fmt(u, 2)}."],
               family="u3_addition", std=sd_, bounds=(0, 1), check={"kind": "union", "pa": pa, "pb": pb, "pab": pab})
    num_mc(U, k, "cp2", "A card is drawn from a standard 52-card deck. What is P(heart or king)? Round to four decimal places.", 16 / 52, [17 / 52, 13 / 52, 4 / 52], 4,
           ["P(heart) = 13/52, P(king) = 4/52, P(king of hearts) = 1/52.", "P(heart or king) = 13/52 + 4/52 − 1/52 = 16/52 ≈ 0.3077."],
           family="u3_addition_cards", std=sd_, bounds=(0, 1), check={"kind": "union", "pa": 13 / 52, "pb": 4 / 52, "pab": 1 / 52, "no_print_check": "deck facts"})
    num_mc(U, k, "cp2", "A fair coin is tossed and a fair die is rolled. What is P(heads and a 6)? Round to four decimal places.", 1 / 12, [1 / 2 + 1 / 6, 1 / 6, 1 / 2], 4,
           ["The coin and die are independent.", "P(H and 6) = (1/2)(1/6) = 1/12 ≈ 0.0833."], family="u3_mult_indep", std=sd_, bounds=(0, 1),
           check={"kind": "indep_and", "pa": 0.5, "pb": 1 / 6, "no_print_check": "fair coin/die"})
    num_mc(U, k, "cp2", "The probability a randomly chosen student walks to school is 0.15. What is the probability a randomly chosen student does NOT walk to school?", 0.85, [0.15, 0.5, 1.15], 2,
           ["Complement rule: P(not A) = 1 − P(A) = 1 − 0.15 = 0.85."], family="u3_complement", std=sd_, bounds=(0, 1),
           check={"kind": "neither", "pa": 0.15, "pb": 0, "pab": 0, "no_print_check": "complement"})
    MC(U, k, "cp2", "Events A and B are mutually exclusive. Which statement is true?",
       "P(A or B) = P(A) + P(B)", ["P(A and B) = P(A)P(B)", "P(A) + P(B) must equal 1", "A and B must be independent"],
       ["Mutually exclusive events cannot happen together, so P(A and B) = 0 and the addition rule simplifies."], family="u3_disjoint", std=sd_)
    SEL(U, k, "cp2", "A die is rolled once. Select ALL pairs of events that are mutually exclusive.",
        ["Rolling an even number; rolling a 3", "Rolling a 1; rolling a 6"], ["Rolling an even number; rolling a number greater than 3", "Rolling a 2; rolling an even number"],
        ["Mutually exclusive events share no outcomes.", "Even = {2,4,6}; >3 = {4,5,6} share 4 and 6; 2 is itself even."], family="u3_disjoint_sel", std=sd_)
    num_mc(U, k, "cp1", "A machine has two independent alarms. Each alarm works with probability 0.92. What is the probability that at least one alarm works when needed? Round to four decimal places.",
           1 - 0.08 ** 2, [0.92 ** 2, 0.92, 2 * 0.92 - 1], 4, ["P(at least one works) = 1 − P(both fail).", "P(both fail) = 0.08 × 0.08 = 0.0064.", "1 − 0.0064 = 0.9936."],
           family="u3_atleast_alarm", std=sd_, bounds=(0, 1), check={"kind": "atleast", "p": 0.92, "n": 2})
    SA(U, k, "cp1", "In a class, 60% of students have a sibling, 25% have both a pet and a sibling, and 70% have a sibling or a pet. What percent of students have a pet?",
       "35%",
       ["P(S or P) = P(S) + P(P) − P(S and P).", "0.70 = 0.60 + P(P) − 0.25.", "P(P) = 0.70 − 0.60 + 0.25 = 0.35.", "So 35% have a pet."],
       family="u3_addition_solve", std=sd_, check={"kind": "union", "pa": 0.70, "pb": 0.25, "pab": 0.60})
    SA(U, k, "cp1", "Two cards are drawn from a standard deck without replacement. Find P(both are aces). Round to four decimal places.",
       "0.0045", ["P(first ace) = 4/52.", "P(second ace | first ace) = 3/51.", "P(both) = (4/52)(3/51) = 12/2652 ≈ 0.0045."],
       family="u3_without_replacement", std=sd_, check={"kind": "indep_and", "pa": 4 / 52, "pb": 3 / 51, "no_print_check": "deck facts"})
    MC(U, k, "cp1", "P(A) = 0.4 and P(B) = 0.5, and A and B are independent. What is P(A or B)?", "0.7", ["0.9", "0.2", "0.1"],
       ["P(A and B) = 0.4 × 0.5 = 0.2 (independent).", "P(A or B) = 0.4 + 0.5 − 0.2 = 0.7."], family="u3_indep_union", std=sd_,
       check={"kind": "union", "pa": 0.4, "pb": 0.5, "pab": 0.2, "no_print_check": "pab computed"})
    SA(U, k, "honors", "A security system has three independent sensors that detect an intruder with probabilities 0.80, 0.70, and 0.60. The alarm sounds if at least one sensor detects. Find P(alarm sounds).",
       "0.976",
       ["P(a sensor fails) = 0.20, 0.30, 0.40.", "Independent: P(all fail) = 0.20 × 0.30 × 0.40 = 0.024.", "P(at least one detects) = 1 − 0.024 = 0.976.", "The complement is easier than adding many overlapping cases."],
       family="u3_atleast_three", std=sd_, check={"kind": "neither", "pa": 0.024, "pb": 0, "pab": 0, "no_print_check": "computed"})
    SA(U, k, "honors", "P(A) = 0.5, P(B) = 0.6, and P(A or B) = 0.8. Find P(A and B) and determine whether A and B are independent.",
       "P(A and B) = 0.3; independent, because P(A)P(B) = 0.3",
       ["P(A and B) = P(A) + P(B) − P(A or B) = 0.5 + 0.6 − 0.8 = 0.3.", "Check independence: P(A)P(B) = 0.5 × 0.6 = 0.30.", "Since P(A and B) = P(A)P(B), A and B are independent."],
       family="u3_indep_check", std=sd_, check={"kind": "indep_and", "pa": 0.5, "pb": 0.6})
    MC(U, k, "honors", "Which statement correctly distinguishes mutually exclusive events from independent events (both with positive probabilities)?",
       "Mutually exclusive events cannot both occur; independent events can both occur and knowing one occurred doesn't change the other's probability.",
       ["They mean the same thing.", "Mutually exclusive events are always independent.", "Independent events cannot occur together."],
       ["If A and B are disjoint with positive probabilities, P(B | A) = 0 ≠ P(B), so they are dependent."], family="u3_disjoint_vs_indep", std=sd_)
    OR(U, k, "honors", "A quality-control process inspects phones. 3% of phones have a screen defect, 5% have a battery defect, and 1% have both.",
       [("Find the probability a randomly chosen phone has at least one of these defects.", "0.07"),
        ("Find the probability a phone has neither defect.", "0.93"),
        ("Find the probability a phone has a screen defect but no battery defect.", "0.02"),
        ("Are the two defects independent? Justify.", "No; P(screen)·P(battery) = 0.0015 ≠ 0.01")],
       ["1 point each part."], family="u3_venn_or", std=sd_, check={"kind": "union", "pa": 0.03, "pb": 0.05, "pab": 0.01})
    SA(U, k, "honors", "Error analysis. A student computes the probability of getting at least one 6 in 3 rolls of a fair die as 1/6 + 1/6 + 1/6 = 1/2. Explain the error and find the correct probability (four decimals).",
       "The events overlap (not mutually exclusive), so probabilities cannot simply be added. Correct: 1 − (5/6)³ ≈ 0.4213.",
       ["Rolling a 6 on roll 1 and on roll 2 can both happen, so adding double counts.", "Use the complement: P(no 6 in 3 rolls) = (5/6)³ = 125/216.", "P(at least one 6) = 1 − 125/216 = 91/216 ≈ 0.4213.", "Adding would give probabilities above 1 for 7 or more rolls, which is impossible."],
       family="u3_atleast_error", std=sd_, check={"kind": "atleast", "p": 1 / 6, "n": 3, "no_print_check": "fair die"})


TAB = ("Grade level and phone ownership for 300 students:\n          | Has phone | No phone | Total\nGrade 9   |    110    |    40    |  150\n"
       "Grade 12  |    140    |    10    |  150\nTotal     |    250    |    50    |  300")


def s03():
    k, sd_ = 3, [PA + ".3"]
    num_mc(U, k, "cp2", TAB + "\nA student is chosen at random. Find P(has phone | grade 9). Round to four decimal places.", 110 / 150, [110 / 250, 110 / 300, 250 / 300], 4,
           ["Condition on grade 9: denominator 150.", "110/150 ≈ 0.7333."], family="u3_cond_table", std=sd_, bounds=(0, 1), check={"kind": "cond", "pab": 110, "pb": 150})
    num_mc(U, k, "cp2", TAB + "\nFind P(grade 12 | no phone). Round to four decimal places.", 10 / 50, [10 / 150, 10 / 300, 50 / 300], 4,
           ["Condition on no phone: denominator 50.", "10/50 = 0.2000."], family="u3_cond_table", std=sd_, bounds=(0, 1), check={"kind": "cond", "pab": 10, "pb": 50})
    MC(U, k, "cp2", "P(A | B) means",
       "the probability that A happens, given that B has happened", ["the probability that both A and B happen", "the probability that A or B happens", "P(A) divided by P(B)"],
       ["The vertical bar means “given.”"], family="u3_cond_meaning", std=sd_)
    SA(U, k, "cp2", "In a group of 40 students, 24 like pizza, and 18 of those 24 also like tacos. A student who likes pizza is chosen at random. What is the probability the student likes tacos?",
       "0.75", ["We know the student likes pizza, so there are 24 possible students.", "18 of the 24 like tacos: 18/24 = 0.75."], family="u3_cond_count", std=sd_,
       check={"kind": "cond", "pab": 18, "pb": 24})
    num_mc(U, k, "cp2", "P(A and B) = 0.18 and P(B) = 0.45. Find P(A | B).", 0.4, [0.081, 0.63, 0.27], 2,
           ["P(A | B) = P(A and B)/P(B) = 0.18/0.45 = 0.40."], family="u3_cond_formula", std=sd_, bounds=(0, 1), check={"kind": "cond", "pab": 0.18, "pb": 0.45})
    MC(U, k, "cp2", "Events A and B are independent if",
       "P(A | B) = P(A)", ["P(A and B) = 0", "P(A) + P(B) = 1", "A and B cannot happen together"],
       ["Independence: knowing B occurred does not change the probability of A."], family="u3_indep_def", std=sd_)
    SEL(U, k, "cp2", TAB + "\nSelect ALL correct statements.",
        ["P(has phone) = 250/300", "P(has phone | grade 12) = 140/150"], ["P(has phone | grade 12) = 140/250", "P(grade 9 and no phone) = 40/150"],
        ["Marginal: 250/300.", "Conditional on grade 12: 140/150.", "Joint uses the grand total: 40/300, not 40/150."], family="u3_cond_sel", std=sd_)
    SA(U, k, "cp1", TAB + "\nAre “has phone” and “grade 12” independent? Justify with probabilities (four decimals).",
       "No: P(has phone | grade 12) = 0.9333 but P(has phone) = 0.8333",
       ["P(phone | grade 12) = 140/150 ≈ 0.9333.", "P(phone) = 250/300 ≈ 0.8333.", "These differ, so the events are not independent."],
       family="u3_indep_table", std=sd_, check={"kind": "cond", "pab": 140, "pb": 150})
    for pa, pba, pbna, q, typ in [
        (0.40, 0.70, 0.20, "40% of a store's customers are members. 70% of members use a coupon, while 20% of non-members do. What proportion of all customers use a coupon?", "total"),
        (0.40, 0.70, 0.20, "40% of a store's customers are members. 70% of members use a coupon, while 20% of non-members do. A customer uses a coupon. What is the probability the customer is a member? Round to four decimal places.", "bayes")]:
        j = pa * pba
        tot = j + (1 - pa) * pbna
        val = tot if typ == "total" else j / tot
        num_mc(U, k, "cp1", q, val, [pba, j, pa] if typ == "bayes" else [pba + pbna, j, pba * pbna], 4 if typ == "bayes" else 2,
               [f"Tree: P(member and coupon) = {fmt(pa)}({fmt(pba)}) = {fmt(j)}; P(non-member and coupon) = {fmt(1 - pa)}({fmt(pbna)}) = {fmt((1 - pa) * pbna)}.",
                f"P(coupon) = {fmt(tot)}." + ("" if typ == "total" else f" P(member | coupon) = {fmt(j)}/{fmt(tot)} ≈ {fmt(val, 4)}.")],
               family="u3_tree", std=sd_, bounds=(0, 1), check={"kind": "tree", "pa": pa, "pba": pba, "pbna": pbna, "type": typ})
    MC(U, k, "cp1", "Which pair of events is most likely independent?",
       "Getting heads on a coin toss and rolling a 5 on a die", ["Being tall and being on the basketball team", "Rain today and carrying an umbrella today", "Studying more and scoring higher"],
       ["Physically separate random devices do not influence each other; the others are plausibly related."], family="u3_indep_context", std=sd_)
    SA(U, k, "honors", "A disease affects 1% of a population. A test detects it 98% of the time when present and gives a false positive 3% of the time when absent. A randomly chosen person tests positive. Find the probability the person has the disease (four decimals), and explain why it is so low.",
       "0.2481; the disease is rare, so most positives come from the large healthy group",
       ["P(D and +) = 0.01 × 0.98 = 0.0098.", "P(no D and +) = 0.99 × 0.03 = 0.0297.", "P(+) = 0.0098 + 0.0297 = 0.0395.", "P(D | +) = 0.0098/0.0395 ≈ 0.2481. False positives from the 99% without disease outnumber true positives."],
       family="u3_bayes_disease", std=sd_, check={"kind": "tree", "pa": 0.01, "pba": 0.98, "pbna": 0.03, "type": "bayes"})
    MC(U, k, "honors", "For events with positive probabilities, which statement is always true?",
       "P(A | B) · P(B) = P(B | A) · P(A)", ["P(A | B) = P(B | A)", "P(A | B) = P(A) + P(B)", "P(A | B) ≤ P(A)"],
       ["Both sides equal P(A and B)."], family="u3_cond_identity", std=sd_)
    SA(U, k, "honors", "Error analysis. Using the table (Grade 9: 110 with phone, 40 without; Grade 12: 140 with phone, 10 without; 300 students), a student computes P(grade 9 | no phone) = 40/150 ≈ 0.267. Identify the error and correct it.",
       "The student divided by the grade 9 total instead of the “no phone” total; P(grade 9 | no phone) = 40/50 = 0.80.",
       ["“Given no phone” restricts attention to the 50 students without a phone.", "Of these, 40 are in grade 9.", "P = 40/50 = 0.80.", "40/150 is P(no phone | grade 9) — the reverse conditional."],
       family="u3_cond_error", std=sd_, check={"kind": "cond", "pab": 40, "pb": 50})


def s04():
    k, sd_ = 4, [PA + ".5"]
    mcs(k, "cp2", [
        ("A simulation uses random digits to model a free-throw shooter who makes 80% of her shots. Which assignment works?",
         "Digits 0–7 represent a make; 8–9 represent a miss.", ["Digits 0–8 represent a make; 9 represents a miss.", "Digits 1–8 represent a make; 0 represents a miss.", "Even digits represent a make."],
         ["8 of 10 equally likely digits (0–7) give probability 0.8."]),
        ("Why are simulations useful in probability?",
         "They estimate probabilities of complicated chance processes by imitating them many times.", ["They give exact probabilities every time.", "They replace the need for random numbers.", "They make unlikely events more likely."],
         ["Simulation estimates long-run relative frequencies when exact calculation is hard."]),
        ("A simulation of 50 trials estimates a probability as 0.34. How could the estimate be made more reliable?",
         "Run many more trials", ["Round the estimate to 0.3", "Use the same 50 random numbers again", "Change the model so the event is more likely"],
         ["More trials → the simulated proportion is closer to the true probability (law of large numbers)."]),
        ("To simulate rolling a fair die with a random digit table, which method works?",
         "Use digits 1–6 for the faces and skip 0, 7, 8, 9.", ["Use digits 0–5 for faces 1–6 and 6–9 for face 6.", "Use digits 0–9 and divide by 6.", "Use digit pairs 01–06 and treat all others as a 6."],
         ["Each face must be equally likely; skipping unused digits keeps the six outcomes equally likely."]),
    ], "u3_sim_setup", sd_)
    SA(U, k, "cp2", "Use the random digits 37542 04805 64894 74296 to simulate 10 free throws by a 70% shooter, with 0–6 = make and 7–9 = miss. Read the first 10 digits. How many makes are there?",
       "8", ["First 10 digits: 3, 7, 5, 4, 2, 0, 4, 8, 0, 5.", "Misses are digits 7–9: here 7 and 8 (2 misses).", "Makes = 10 − 2 = 8.", "This is one simulated set of 10 shots; repeating it many times shows the variability."],
       family="u3_sim_count", std=sd_, check={"kind": "count_between", "data": [3, 7, 5, 4, 2, 0, 4, 8, 0, 5], "lo": 0, "hi": 6, "no_print_check": "digits printed as groups"})
    SEL(U, k, "cp2", "A simulation models a 25% chance of winning a prize with each cereal box. Select ALL correct ways to model one box.",
        ["Use digits 0–1 as a win and 2–7 as a loss, ignoring 8 and 9", "Use digit pairs 00–24 as a win and 25–99 as a loss"],
        ["Use digits 0–2 as a win and 3–9 as a loss", "Use one digit: 0 is a win, 1–9 are losses"],
        ["0–1 out of 0–7 is 2/8 = 0.25.", "00–24 out of 00–99 is 25/100 = 0.25.", "0–2 of 10 digits is 0.30; 0 alone is 0.10."], family="u3_sim_assign_sel", std=sd_)
    SA(U, k, "cp2", "A simulation of 200 trials of “roll two dice and check whether the sum is 7” found 35 sevens. Give the simulated estimate of P(sum = 7) and compare it with the exact probability 6/36 (four decimals).",
       "Estimate 0.175; exact 0.1667", ["Estimate = 35/200 = 0.175.", "Exact: 6 of 36 equally likely outcomes give 7, so 6/36 ≈ 0.1667.", "The estimate is close; more trials would bring it closer."],
       family="u3_sim_vs_exact", std=sd_, check={"kind": "ratio", "num": 35, "den": 200})
    mcs(k, "cp1", [
        ("A cereal brand puts one of 4 equally likely toys in each box. To simulate buying boxes until you have all 4 toys, what is one trial?",
         "Generate random integers from 1 to 4 until all four values have appeared, and record how many were needed.", ["Generate four random integers and stop.", "Generate one random integer from 1 to 4.", "Generate random integers from 1 to 4 until a 4 appears."],
         ["A trial must reproduce the whole chance process: keep buying until all 4 toys are collected."]),
        ("In a simulation, why must the random numbers used in each trial be independent?",
         "Because the real chance process has independent outcomes, and dependence would make the model unrealistic.", ["To make the simulation shorter.", "Because independence guarantees the exact answer.", "So that every trial gives the same result."],
         ["The model's assumptions must match the real situation."]),
        ("A simulation of 1,000 trials gives 23 trials in which an event occurred. What is the best interpretation?",
         "The probability of the event is estimated to be about 0.023.", ["The event will occur exactly 23 times in the next 1,000 trials.", "The event is impossible.", "The probability is 23."],
         ["Relative frequency from many trials estimates probability."]),
    ], "u3_sim_cp1", sd_)
    SA(U, k, "cp1", "Describe how to use a random number generator to simulate whether at least 2 of 5 randomly chosen adults are left-handed, if 10% of adults are left-handed.",
       "Let 1 = left-handed and 2–10 = right-handed. Generate 5 random integers from 1 to 10 (one per adult); record whether 2 or more are 1s. Repeat many times; the proportion of trials with at least two 1s estimates the probability.",
       ["Assign outcomes: integer 1 (1 out of 10) = left-handed.", "One trial = 5 integers (independent, since adults are chosen at random).", "Record whether at least two are 1s.", "Repeat many trials; the proportion of “yes” estimates the probability."],
       family="u3_sim_describe", std=sd_)
    SA(U, k, "cp1", "A simulation estimates P(at least one 6 in 4 rolls of a fair die) as 0.512. Find the exact probability (four decimals) for comparison.",
       "0.5177", ["P(no 6 in 4 rolls) = (5/6)^4 ≈ 0.4823.", "P(at least one 6) = 1 − 0.4823 = 0.5177.", "The simulated 0.512 is close to the exact value.", "More trials would bring the simulation closer."],
       family="u3_sim_exact", std=sd_, check={"kind": "atleast", "p": 1 / 6, "n": 4, "no_print_check": "fair die"})
    OR(U, k, "honors", "A basketball player makes 60% of her free throws. A sportswriter notices she made 9 of her first 10 shots in a game and claims she is “on fire.”",
       [("Describe how to simulate 10 free throws using random digits.", "Digits 0–5 = make, 6–9 = miss; read 10 digits as one game"),
        ("Find the exact probability of making at least 9 of 10 (four decimals).", f"{fmt(bsum(10, 0.6, 9, 10), 4)}"),
        ("Interpret this probability.", "If she shoots 60% independently, about 4.6% of 10-shot sets would have 9 or more makes"),
        ("Does 9 of 10 give strong evidence she is “on fire”? Explain.", "Somewhat unusual (about 5%), but in a long season such streaks will happen by chance; one streak is not strong evidence")],
       ["1 point each part."], family="u3_sim_or", std=sd_, check={"kind": "binom", "n": 10, "p": 0.6, "k": 9, "type": "ge"})
    mcs(k, "honors", [
        ("A simulation is run with 100 trials and then with 10,000 trials. How do the two estimates compare?",
         "Both estimate the same probability, but the 10,000-trial estimate is likely much closer to the true value.", ["The 100-trial estimate is more accurate.", "They must be exactly equal.", "The 10,000-trial estimate is biased."],
         ["The variability of a simulated proportion shrinks as the number of trials grows."]),
        ("A simulation for a two-child family uses one random digit per child: even = boy, odd = girl. What assumption does this model make?",
         "Each birth is equally likely to be a boy or a girl and births are independent.", ["Boys are more likely than girls.", "The second child must differ from the first.", "Families stop after a boy."],
         ["Even and odd digits each have probability 0.5, and separate digits are independent."]),
    ], "u3_sim_honors", sd_)
    SA(U, k, "honors", "A game: roll two fair dice; you win if the sum is 8 or more. A simulation of 500 games gives 210 wins. Find the exact P(win) as a fraction and decimal (four places), and say whether the simulation result is reasonable.",
       "15/36 ≈ 0.4167; the simulated 210/500 = 0.42 is very close, so it is reasonable",
       ["Sums ≥ 8: sum 8 (5 ways), 9 (4), 10 (3), 11 (2), 12 (1) = 15 ways.", "P(win) = 15/36 ≈ 0.4167.", "Simulated: 210/500 = 0.420.", "The difference (0.003) is small, consistent with chance variation."],
       family="u3_dice_sum", std=sd_, check={"kind": "sum_dice_prob", "cond": "s >= 8"})


def s05():
    k, sd_ = 5, [PA + ".4"]
    dist = ([0, 1, 2, 3], [0.2, 0.4, 0.3, 0.1])
    MC(U, k, "cp2", "Which table is a valid probability distribution?",
       "x: 0, 1, 2; P(x): 0.3, 0.5, 0.2", ["x: 0, 1, 2; P(x): 0.4, 0.5, 0.2", "x: 0, 1, 2; P(x): 0.6, −0.1, 0.5", "x: 0, 1, 2; P(x): 0.2, 0.2, 0.2"],
       ["Probabilities must be between 0 and 1 and sum to 1.", "0.3 + 0.5 + 0.2 = 1."], family="u3_valid_dist", std=sd_)
    SA(U, k, "cp2", "X = number of pets owned by a randomly chosen student has distribution x: 0, 1, 2, 3; P(x): 0.20, 0.40, 0.30, k. Find k.", "0.10",
       ["Probabilities must sum to 1.", "k = 1 − (0.20 + 0.40 + 0.30) = 0.10."], family="u3_missing_p", std=sd_, check={"kind": "missing_p", "p": [0.2, 0.4, 0.3]})
    num_mc(U, k, "cp2", "X = number of pets owned by a randomly chosen student: x: 0, 1, 2, 3; P(x): 0.20, 0.40, 0.30, 0.10. Find P(X ≥ 2).", 0.4, [0.3, 0.7, 0.6], 2,
           ["P(X ≥ 2) = P(2) + P(3) = 0.30 + 0.10 = 0.40."], family="u3_rv_cum", std=sd_, bounds=(0, 1), check={"kind": "rv_cum", "x": dist[0], "p": dist[1], "cond": "x >= 2"})
    num_mc(U, k, "cp2", "X = number of pets owned by a randomly chosen student: x: 0, 1, 2, 3; P(x): 0.20, 0.40, 0.30, 0.10. Find P(X < 2).", 0.6, [0.4, 0.9, 0.3], 2,
           ["P(X < 2) = P(0) + P(1) = 0.20 + 0.40 = 0.60 (does not include 2)."], family="u3_rv_cum", std=sd_, bounds=(0, 1), check={"kind": "rv_cum", "x": dist[0], "p": dist[1], "cond": "x < 2"})
    MC(U, k, "cp2", "Which is a discrete random variable?",
       "The number of heads in 10 coin tosses", ["The time it takes to run a mile", "The weight of a randomly chosen apple", "The height of a randomly chosen student"],
       ["Discrete random variables take a countable set of values (0, 1, …, 10)."], family="u3_discrete_vs_cont", std=sd_)
    SA(U, k, "cp2", "Two fair coins are tossed. Let X = number of heads. Write the probability distribution of X.", "x: 0, 1, 2; P(x): 0.25, 0.50, 0.25",
       ["Sample space: HH, HT, TH, TT (equally likely).", "X = 0: TT (1/4); X = 1: HT, TH (2/4); X = 2: HH (1/4).", "Distribution: 0.25, 0.50, 0.25."],
       family="u3_build_dist", std=sd_, check={"kind": "binom", "n": 2, "p": 0.5, "k": 1, "type": "eq", "no_print_check": "fair coins"})
    SEL(U, k, "cp2", "X has distribution x: 1, 2, 3, 4; P(x): 0.1, 0.3, 0.4, 0.2. Select ALL true statements.",
        ["P(X = 3) = 0.4", "P(X ≤ 2) = 0.4", "P(X > 1) = 0.9"], ["P(X ≥ 3) = 0.4", "The most likely value is 4"],
        ["P(X ≤ 2) = 0.1 + 0.3 = 0.4; P(X > 1) = 1 − 0.1 = 0.9.", "P(X ≥ 3) = 0.4 + 0.2 = 0.6; the most likely value is 3."], family="u3_rv_sel", std=sd_)
    num_mc(U, k, "cp1", "Let X = number of cars a dealer sells in a day: x: 0, 1, 2, 3, 4, 5; P(x): 0.05, 0.15, 0.30, 0.25, 0.15, 0.10. Find P(1 ≤ X ≤ 3).", 0.70, [0.55, 0.85, 0.45], 2,
           ["Include 1, 2, and 3: 0.15 + 0.30 + 0.25 = 0.70."], family="u3_rv_interval", std=sd_, bounds=(0, 1),
           check={"kind": "rv_cum", "x": [0, 1, 2, 3, 4, 5], "p": [0.05, 0.15, 0.30, 0.25, 0.15, 0.10], "cond": "1 <= x <= 3"})
    SA(U, k, "cp1", "A fair die is rolled twice. Let X = the larger of the two rolls (or the common value if equal). Find P(X = 4) as a fraction and a decimal (four places).",
       "7/36 ≈ 0.1944", ["Outcomes with both rolls ≤ 4: 16. Outcomes with both ≤ 3: 9.", "Maximum exactly 4: 16 − 9 = 7 outcomes.", "List: (4,1),(4,2),(4,3),(1,4),(2,4),(3,4),(4,4).", "P(X = 4) = 7/36 ≈ 0.1944."],
       family="u3_max_dice", std=sd_, check={"kind": "sum_dice_prob", "cond": "max(a, b) == 4"})
    SA(U, k, "cp1", "In a game you pay $2 to spin a spinner: 50% chance of $0, 30% chance of $2, 20% chance of $6. Let W = net winnings (prize − $2). Write the probability distribution of W.",
       "w: −2, 0, 4; P(w): 0.5, 0.3, 0.2", ["Net winnings = prize − 2: $0 → −2, $2 → 0, $6 → 4.", "Probabilities stay the same: 0.5, 0.3, 0.2."],
       family="u3_net_dist", std=sd_)
    MC(U, k, "cp1", "X = number of girls in a family with 3 children (each child equally likely to be a girl, independently). What is P(X = 2)?", "0.375", ["0.25", "0.5", "0.125"],
       ["Outcomes with exactly 2 girls: GGB, GBG, BGG → 3 of 8.", "3/8 = 0.375."], family="u3_three_children", std=sd_,
       check={"kind": "binom", "n": 3, "p": 0.5, "k": 2, "type": "eq", "no_print_check": "equally likely"})
    MC(U, k, "cp1", "A continuous random variable X is uniform on 0 to 10. What is P(X = 4)?", "0", ["0.1", "0.4", "0.04"],
       ["For a continuous random variable, any single value has probability 0; probabilities come from areas over intervals."], family="u3_continuous_point", std=sd_)
    SEL(U, k, "cp1", "Select ALL properties that every discrete probability distribution must satisfy.",
        ["Each probability is between 0 and 1.", "The probabilities sum to 1."], ["The distribution is symmetric.", "Each value has the same probability."],
        ["Only the first two are required."], family="u3_dist_props_sel", std=sd_)
    SA(U, k, "honors", "Let X = the sum of two fair four-sided dice (faces 1–4). Write the probability distribution of X and find P(X ≥ 6).",
       "x: 2, 3, 4, 5, 6, 7, 8; P(x): 1/16, 2/16, 3/16, 4/16, 3/16, 2/16, 1/16; P(X ≥ 6) = 6/16 = 0.375",
       ["16 equally likely outcomes.", "Count sums: 2 (1), 3 (2), 4 (3), 5 (4), 6 (3), 7 (2), 8 (1).", "P(X ≥ 6) = (3 + 2 + 1)/16 = 6/16.", "= 0.375."],
       family="u3_d4_sum", std=sd_, check={"kind": "ratio", "num": 6, "den": 16, "no_print_check": "counted"})
    MC(U, k, "honors", "Two cards are drawn without replacement from 3 red and 2 black cards. Let X = number of red cards drawn. What is P(X = 1)?", "0.6", ["0.48", "0.3", "0.4"],
       ["P(X = 1) = [C(3,1)C(2,1)]/C(5,2) = 6/10 = 0.6.", "Draws are not independent, so binomial does not apply (0.48 is the with-replacement answer)."], family="u3_hypergeom", std=sd_,
       check={"kind": "ratio", "num": comb(3, 1) * comb(2, 1), "den": comb(5, 2), "no_print_check": "counted"})
    OR(U, k, "honors", "A carnival game costs $3. You draw one card from a well-shuffled standard deck: an ace pays $15, a face card (J, Q, K) pays $5, and anything else pays nothing.",
       [("Write the probability distribution of the payout (as fractions).", "$15: 4/52; $5: 12/52; $0: 36/52"),
        ("Write the distribution of net winnings W = payout − 3.", "W = 12: 4/52; W = 2: 12/52; W = −3: 36/52"),
        ("Find P(W > 0).", "16/52 ≈ 0.3077"),
        ("Find E(W) and explain whether the game favors the player or the carnival.", "E(W) = (48 + 24 − 108)/52 ≈ −0.69; it favors the carnival")],
       ["1 point each part."], family="u3_carnival_or", std=sd_, check={"kind": "rv", "x": [12, 2, -3], "p": [4 / 52, 12 / 52, 36 / 52], "out": "mean", "no_print_check": "deck facts"})


def s06():
    k, sd_ = 6, [PA + ".6"]
    for lv, ctx, xs, ps in [("cp2", "X = number of goals a soccer team scores in a game", [0, 1, 2, 3], [0.25, 0.35, 0.30, 0.10]),
                            ("cp2", "X = number of books a student checks out", [1, 2, 3, 4], [0.4, 0.3, 0.2, 0.1]),
                            ("cp1", "X = number of customers waiting in line when a bank opens", [0, 1, 2, 3, 4], [0.15, 0.30, 0.25, 0.20, 0.10])]:
        m = sum(x * p for x, p in zip(xs, ps))
        v = sum(p * (x - m) ** 2 for x, p in zip(xs, ps))
        txt = "x: " + ", ".join(map(str, xs)) + "; P(x): " + ", ".join(fmt(p) for p in ps)
        if lv == "cp2":
            num_mc(U, k, lv, f"{ctx}: {txt}. Find E(X).", m, [sum(xs) / len(xs), max(ps) * len(xs), m + 0.5], 2,
                   ["E(X) = Σ x·P(x) = " + " + ".join(f"{x}({fmt(p)})" for x, p in zip(xs, ps)) + f" = {fmt(m, 2)}."],
                   family="u3_ev", std=sd_, check={"kind": "rv", "x": xs, "p": ps, "out": "mean"})
        else:
            SA(U, k, lv, f"{ctx}: {txt}. Find the mean and standard deviation of X (three decimals for the SD).", f"μ = {fmt(m, 2)}, σ ≈ {fmt(math.sqrt(v), 3)}",
               [f"μ = Σ x·P(x) = {fmt(m, 2)}.", f"Var = Σ (x − μ)²P(x) = {fmt(v, 4)}.", f"σ = √{fmt(v, 4)} ≈ {fmt(math.sqrt(v), 3)}."],
               family="u3_ev_sd", std=sd_, check={"kind": "rv", "x": xs, "p": ps})
    MC(U, k, "cp2", "A raffle ticket costs $5. The expected value of a ticket's prize is $3.20. What is the expected net gain per ticket?", "−$1.80", ["$1.80", "$3.20", "−$3.20"],
       ["Expected net = 3.20 − 5 = −1.80 dollars per ticket."], family="u3_ev_net", std=sd_)
    MC(U, k, "cp2", "The expected number of points per game is E(X) = 14.6. What does this mean?",
       "Over many, many games, the average number of points is about 14.6.", ["The team scores 14.6 points in every game.", "The most common score is 14.6.", "The team will never score more than 14.6."],
       ["Expected value is a long-run average."], family="u3_ev_meaning", std=sd_)
    SA(U, k, "cp2", "A game pays $10 with probability 0.1, $2 with probability 0.3, and $0 otherwise. Find the expected payout.", "$1.60",
       ["E = 10(0.1) + 2(0.3) + 0(0.6) = 1.0 + 0.6 + 0 = $1.60."], family="u3_ev_game", std=sd_, check={"kind": "rv", "x": [10, 2, 0], "p": [0.1, 0.3, 0.6], "out": "mean", "no_print_check": "0.6 is the remainder"})
    MC(U, k, "cp1", "X has mean 12 and SD 3. Let Y = 4X − 5. Find the mean and SD of Y.", "μ = 43, σ = 12", ["μ = 43, σ = 7", "μ = 48, σ = 12", "μ = 43, σ = 144"],
       ["μ_Y = 4(12) − 5 = 43.", "σ_Y = |4|(3) = 12 (subtracting 5 doesn't change spread)."], family="u3_lin_rv", std=sd_, check={"kind": "lin_rv", "a": -5, "b": 4, "mean": 12, "sd": 3})
    MC(U, k, "cp1", "Temperature X (°C) at noon has mean 22 and SD 4. Convert to °F: Y = 1.8X + 32. What is the SD of Y?", "7.2 °F", ["39.2 °F", "4 °F", "12.96 °F"],
       ["σ_Y = 1.8 × 4 = 7.2; adding 32 does not affect spread."], family="u3_lin_rv_sd", std=sd_,
       check={"kind": "lin_rv", "a": 32, "b": 1.8, "mean": 22, "sd": 4, "verify_only": True, "expect": [71.6, 7.2]})
    SA(U, k, "cp1", "An insurance policy costs $250 per year. The company pays $20,000 with probability 0.005, $5,000 with probability 0.02, and $0 otherwise. Find the expected payout and the company's expected profit per policy.",
       "Expected payout $200; expected profit $50", ["Expected payout = 20,000(0.005) + 5,000(0.02) = 100 + 100 = $200.", "Expected profit = 250 − 200 = $50 per policy."], family="u3_insurance", std=sd_,
       check={"kind": "rv", "x": [20000, 5000, 0], "p": [0.005, 0.02, 0.975], "out": "mean", "no_print_check": "remainder probability"})
    xs_, ps_ = [10, 15, 20, 25], [0.2, 0.4, 0.3, 0.1]
    mu_ = sum(x * p for x, p in zip(xs_, ps_))
    sg_ = math.sqrt(sum(p * (x - mu_) ** 2 for x, p in zip(xs_, ps_)))
    OR(U, k, "honors", "A food truck sells X sandwiches per hour with distribution x: 10, 15, 20, 25; P(x): 0.2, 0.4, 0.3, 0.1. Each sandwich earns $4 profit, and the truck pays $12 per hour to park, so hourly profit is Y = 4X − 12.",
       [("Find E(X).", fmt(mu_, 2)), ("Find σ_X (three decimals).", f"≈ {fmt(sg_, 3)}"),
        ("Find E(Y) and σ_Y.", f"E(Y) = 4({fmt(mu_)}) − 12 = ${fmt(4 * mu_ - 12, 2)}; σ_Y = 4({fmt(sg_)}) = ${fmt(4 * sg_, 2)}"),
        ("Interpret E(Y) in context.", f"Over many hours, the truck's profit averages about ${fmt(4 * mu_ - 12)} per hour")],
       ["1 point each part; σ_Y must use |4|σ_X with no effect from −12."], family="u3_foodtruck_or", std=sd_, check={"kind": "rv", "x": [10, 15, 20, 25], "p": [0.2, 0.4, 0.3, 0.1]})
    SA(U, k, "honors", "Error analysis. X has mean 50 and SD 6. A student finds the SD of Y = 10 − 2X as follows: “σ_Y = 10 − 2(6) = −2.” Identify the error and give the correct mean and SD of Y.",
       "SD is unaffected by adding 10 and is multiplied by |−2|: σ_Y = 12; μ_Y = 10 − 2(50) = −90.",
       ["Adding a constant shifts the mean but not the spread.", "Multiplying by −2 multiplies the SD by |−2| = 2.", "σ_Y = 2 × 6 = 12 (an SD cannot be negative).", "μ_Y = 10 − 2(50) = −90."],
       family="u3_lin_rv_error", std=sd_, check={"kind": "lin_rv", "a": 10, "b": -2, "mean": 50, "sd": 6})
    MC(U, k, "honors", "Game A pays $100 with probability 0.01 (else $0). Game B pays $1 for sure. Which is true?",
       "Both have expected payout $1, but Game A has a much larger standard deviation.", ["Game A has the larger expected payout.", "Both have the same SD.", "Game B has the larger expected payout."],
       ["E(A) = 100(0.01) = 1 = E(B).", "SD(A) = √(0.01·99² + 0.99·1²) ≈ 9.95; SD(B) = 0."], family="u3_ev_vs_risk", std=sd_,
       check={"kind": "rv", "x": [100, 0], "p": [0.01, 0.99], "out": "mean", "skip_distractors": True, "no_print_check": "remainder"})


def s07():
    k, sd_ = 7, [PA + ".4"]
    MC(U, k, "cp2", "Which situation is binomial?",
       "Counting the number of 3s in 12 rolls of a fair die", ["Rolling a die until a 3 appears", "Measuring the time between buses", "Counting the number of rolls needed to get two 3s"],
       ["Binomial: fixed n, success/failure, independent trials, constant p.", "“Until” situations are geometric or other waiting-time models."], family="u3_binom_id", std=sd_)
    num_mc(U, k, "cp2", "A quiz has 5 multiple-choice questions, each with 4 choices. A student guesses on every question. Find P(exactly 2 correct). Round to four decimal places.",
           comb(5, 2) * 0.25 ** 2 * 0.75 ** 3, [0.25 ** 2 * 0.75 ** 3, 0.4, comb(5, 2) * 0.25 ** 2], 4,
           ["X ~ Binomial(n = 5, p = 0.25).", "P(X = 2) = C(5,2)(0.25)²(0.75)³ = 10(0.0625)(0.421875) ≈ 0.2637."], family="u3_binom_pmf", std=sd_, bounds=(0, 1),
           check={"kind": "binom", "n": 5, "p": 0.25, "k": 2, "type": "eq", "no_print_check": "p from 4 choices"})
    MC(U, k, "cp2", "A fair coin is tossed 20 times. What is the expected number of heads?", "10", ["20", "5", "0.5"],
       ["Binomial mean μ = np = 20(0.5) = 10."], family="u3_binom_mean", std=sd_)
    num_mc(U, k, "cp2", "A basketball player makes 70% of her free throws. What is the probability that her first miss is on her 3rd shot (make, make, miss)? Round to four decimal places.",
           0.7 * 0.7 * 0.3, [0.3, 0.7 ** 3, 3 * 0.7 * 0.7 * 0.3], 4, ["Geometric with success = miss, p = 0.3.", "P = (0.7)(0.7)(0.3) = 0.147."],
           family="u3_geom_pmf", std=sd_, bounds=(0, 1), check={"kind": "geom", "p": 0.3, "k": 3, "type": "eq", "no_print_check": "p = 1 − 0.7"})
    SA(U, k, "cp2", "15% of a store's customers use a gift card. On average, how many customers will the cashier serve until the first one uses a gift card? Round to two decimal places.",
       "6.67", ["Geometric random variable with p = 0.15.", "Mean = 1/p = 1/0.15 ≈ 6.67 customers."], family="u3_geom_mean", std=sd_, check={"kind": "geom_mean", "p": 0.15})
    SEL(U, k, "cp2", "Select ALL conditions required for a binomial setting.",
        ["A fixed number of trials", "Each trial is a success or failure", "Trials are independent", "The probability of success is the same on each trial"],
        ["The number of trials is random", "Success must be more likely than failure"],
        ["BINS: Binary, Independent, Number fixed, Same p."], family="u3_bins_sel", std=sd_)
    v = bsum(25, 0.12, 0, 2)
    SA(U, k, "cp1", "Twelve percent of adults are left-handed. In a random sample of 25 adults, find P(at most 2 left-handed). Round to four decimal places.",
       f"{fmt(v, 4)}", ["X ~ Binomial(25, 0.12).", "P(X ≤ 2) = P(0) + P(1) + P(2).", f"= binomcdf(25, 0.12, 2) ≈ {fmt(v, 4)}.", "The 10% condition holds, so the binomial model is reasonable."],
       family="u3_binom_cdf", std=sd_, check={"kind": "binom", "n": 25, "p": 0.12, "k": 2, "type": "le"})
    SA(U, k, "cp1", "In a binomial setting with n = 40 and p = 0.35, find the mean and standard deviation of X (three decimals).",
       f"μ = 14, σ ≈ {fmt(math.sqrt(40 * 0.35 * 0.65), 3)}", ["μ = np = 40(0.35) = 14.", f"σ = √(np(1 − p)) = √(9.1) ≈ {fmt(math.sqrt(9.1), 3)}."],
       family="u3_binom_ms", std=sd_, check={"kind": "binom_ms", "n": 40, "p": 0.35})
    num_mc(U, k, "cp1", "A manufacturer finds that 5% of its light bulbs are defective. Bulbs are tested one at a time. What is the probability the first defective bulb is found within the first 10 tested? Round to four decimal places.",
           1 - 0.95 ** 10, [0.95 ** 10, 0.05 * 10, 0.95 ** 9 * 0.05], 4, ["Geometric with p = 0.05.", "P(X ≤ 10) = 1 − (0.95)^10 ≈ 1 − 0.5987 = 0.4013."],
           family="u3_geom_cdf", std=sd_, bounds=(0, 1), check={"kind": "geom", "p": 0.05, "k": 10, "type": "le"})
    MC(U, k, "cp1", "Ten cards are dealt without replacement from a 52-card deck, and X = number of hearts. Why is X NOT binomial?",
       "The trials are not independent; the probability of a heart changes after each card (and 10 is more than 10% of 52).", ["There is no fixed number of trials.", "There are more than two outcomes for each card.", "Hearts are too rare."],
       ["Without replacement from a small population, p changes from card to card."], family="u3_binom_not", std=sd_)
    hi, lo = bsum(15, 0.8, 13, 15), bsum(15, 0.8, 0, 10)
    SA(U, k, "honors", "A drug works for 80% of patients. In a group of 15 patients, find P(at least 13 respond) and P(at most 10 respond). Round to four decimal places, and comment on whether 10 or fewer responders would be unusual.",
       f"P(X ≥ 13) ≈ {fmt(hi, 4)}; P(X ≤ 10) ≈ {fmt(lo, 4)}; 10 or fewer is somewhat unusual (about 1 time in 6) but not rare",
       ["X ~ Binomial(15, 0.8).", f"P(X ≥ 13) = 1 − P(X ≤ 12) ≈ {fmt(hi, 4)}.", f"P(X ≤ 10) ≈ {fmt(lo, 4)}.", "A probability near 0.16 is not small enough to call the result very surprising."],
       family="u3_binom_ge", std=sd_, check={"kind": "binom", "n": 15, "p": 0.8, "k": 13, "type": "ge"})
    MC(U, k, "honors", "A binomial distribution has n = 50. For which p is the distribution most nearly symmetric?", "p = 0.5", ["p = 0.05", "p = 0.9", "p = 0.98"],
       ["Binomial distributions are symmetric when p = 0.5 and skewed when p is near 0 or 1."], family="u3_binom_shape", std=sd_)
    OR(U, k, "honors", "A company claims that 90% of its packages arrive on time. A customer tracks 20 randomly selected packages and finds only 15 arrived on time.",
       [("Assuming the claim is true, what are the mean and SD of the number of on-time packages? (three decimals)", "μ = 18, σ ≈ 1.342"),
        ("Find P(X ≤ 15) if the claim is true (four decimals).", f"≈ {fmt(bsum(20, 0.9, 0, 15), 4)}"),
        ("Does the customer's result give convincing evidence against the claim? Explain.", f"Fairly convincing; 15 or fewer happens only about {fmt(100 * bsum(20, 0.9, 0, 15), 1)}% of the time if p = 0.9"),
        ("Name one condition that must hold for the binomial model to be valid here.", "Packages' on-time results are independent (e.g., not all shipped on the same delayed truck), with the same p")],
       ["1 point each part."], family="u3_binom_or", std=sd_, check={"kind": "binom", "n": 20, "p": 0.9, "k": 15, "type": "le"})


def s08():
    k, sd_ = 8, [PB + ".1", PB + ".2"]
    MC(U, k, "cp2", "X has mean 10 and Y has mean 6. What is the mean of X + Y?", "16", ["4", "60", "Cannot be found without the SDs"],
       ["The mean of a sum is the sum of the means: 10 + 6 = 16 (true whether or not X and Y are independent)."], family="u3_comb_mean", std=sd_)
    MC(U, k, "cp2", "X and Y are independent with variances 9 and 16. What is the variance of X + Y?", "25", ["7", "5", "144"],
       ["For independent random variables, variances add: 9 + 16 = 25."], family="u3_comb_var", std=sd_)
    MC(U, k, "cp2", "X and Y are independent with SDs 3 and 4. What is the SD of X − Y?", "5", ["1", "7", "25"],
       ["Variances add even for a difference: 9 + 16 = 25.", "SD = √25 = 5."], family="u3_comb_sd_diff", std=sd_,
       check={"kind": "combine", "signs": [1, -1], "means": [0, 0], "sds": [3, 4], "verify_only": True, "expect": [0, 5]})
    SA(U, k, "cp2", "The time to walk to the bus stop is independent of the bus ride. Walk: mean 8 min, SD 2 min. Ride: mean 22 min, SD 4 min. Find the mean and SD of the total commute time (two decimals).",
       f"Mean 30 min, SD ≈ {fmt(math.sqrt(20), 2)} min", ["Mean = 8 + 22 = 30 minutes.", "Var = 2² + 4² = 20.", f"SD = √20 ≈ {fmt(math.sqrt(20), 2)} minutes."],
       family="u3_commute", std=sd_, check={"kind": "combine", "signs": [1, 1], "means": [8, 22], "sds": [2, 4]})
    MC(U, k, "cp2", "Why do we add variances, not standard deviations, when combining independent random variables?",
       "Variances of independent variables add mathematically; SDs do not, so we add variances and then take the square root.", ["Because SDs are always larger than variances.", "Because variances are measured in the original units.", "We should add SDs; adding variances is a shortcut."],
       ["Var(X ± Y) = Var(X) + Var(Y) for independent X, Y; SD = √Var."], family="u3_why_var", std=sd_)
    SEL(U, k, "cp2", "X and Y are independent random variables. Select ALL true statements.",
        ["μ_(X+Y) = μ_X + μ_Y", "μ_(X−Y) = μ_X − μ_Y", "σ²_(X−Y) = σ²_X + σ²_Y"], ["σ_(X+Y) = σ_X + σ_Y", "σ²_(X−Y) = σ²_X − σ²_Y"],
        ["Means add or subtract; variances add for both sums and differences (independence)."], family="u3_comb_sel", std=sd_)
    SA(U, k, "cp1", "Ana's bowling score A has mean 165 and SD 12; Ben's score B has mean 150 and SD 16, independent. Find the mean and SD of A − B, the amount by which Ana beats Ben.",
       "Mean 15, SD 20", ["μ = 165 − 150 = 15.", "σ² = 12² + 16² = 144 + 256 = 400.", "σ = 20."], family="u3_comb_diff", std=sd_,
       check={"kind": "combine", "signs": [1, -1], "means": [165, 150], "sds": [12, 16]})
    num_mc(U, k, "cp1", "Ana's bowling score A is Normal with mean 165 and SD 12; Ben's score B is Normal with mean 150 and SD 16, independent. Find P(Ben beats Ana), i.e., P(A − B < 0). Use z rounded to two decimals; give four decimals.",
           Phi(-0.75), [1 - Phi(-0.75), Phi(-15 / 28), 0.5], 4, ["D = A − B is Normal with mean 15, SD 20.", "z = (0 − 15)/20 = −0.75.", f"P(Z < −0.75) ≈ {fmt(Phi(-0.75), 4)}."],
           family="u3_comb_prob", std=sd_ + [PC], bounds=(0, 1), check={"kind": "combine_prob", "signs": [1, -1], "means": [165, 150], "sds": [12, 16], "c": 0, "type": "lt"})
    SA(U, k, "cp1", "A recipe uses 3 independent scoops of flour, each with mean 120 g and SD 5 g. Find the mean and SD of the total flour (two decimals). Explain why the SD is not 3 × 5.",
       f"Mean 360 g, SD ≈ {fmt(math.sqrt(75), 2)} g; three independent scoops are added, so their variances add (3 × 25 = 75), not the SDs",
       ["Total T = S₁ + S₂ + S₃ (independent).", "μ = 3 × 120 = 360 g.", f"σ² = 25 + 25 + 25 = 75; σ ≈ {fmt(math.sqrt(75), 2)} g.", "3 × 5 = 15 would be the SD of 3 × S (one scoop tripled), a different random variable."],
       family="u3_sum_vs_multiple", std=sd_, check={"kind": "combine", "signs": [1, 1, 1], "means": [120, 120, 120], "sds": [5, 5, 5]})
    z = round(140 / math.sqrt(6300), 2)
    SA(U, k, "honors", "An elevator has a limit of 1,400 lb. Adult weights are Normal with mean 180 lb and SD 30 lb. If 7 randomly chosen adults board, what is the probability their total weight exceeds the limit? Use z rounded to two decimals; give four decimals.",
       f"≈ {fmt(1 - Phi(z), 4)}",
       ["T = sum of 7 independent weights: μ = 7 × 180 = 1,260 lb.", f"σ = √(7 × 30²) = √6,300 ≈ {fmt(math.sqrt(6300), 2)} lb.",
        f"z = (1,400 − 1,260)/{fmt(math.sqrt(6300), 2)} ≈ {fmt(z, 2)}.", f"P(T > 1,400) ≈ {fmt(1 - Phi(z), 4)}."],
       family="u3_elevator", std=sd_ + [PC], check={"kind": "combine_prob", "signs": [1] * 7, "means": [180] * 7, "sds": [30] * 7, "c": 1400, "type": "gt", "no_print_check": "7 repeated"})
    MC(U, k, "honors", "X = height of a randomly chosen husband, Y = height of his wife. Why is it NOT valid to compute SD(X − Y) as √(σ²_X + σ²_Y)?",
       "Heights of spouses are likely correlated, so X and Y are not independent.", ["Because heights are not Normal.", "Because the mean of X − Y is negative.", "Because variances must be subtracted for differences."],
       ["The variance rule requires independence; spouses' heights tend to be related."], family="u3_indep_required", std=sd_)
    z2 = round(140 / math.sqrt(11700), 2)
    OR(U, k, "honors", "A coffee shop's daily sales: drinks D with mean $820 and SD $90; food F with mean $340 and SD $60. Assume D and F are independent and Normal.",
       [("Find the mean and SD of total daily sales D + F (two decimals).", f"Mean $1,160; SD ≈ ${fmt(math.sqrt(11700), 2)}"),
        ("Find the probability total sales exceed $1,300 (z to two decimals).", f"z ≈ {fmt(z2, 2)}; ≈ {fmt(1 - Phi(z2), 4)}"),
        ("Find the mean and SD of D − F.", f"Mean $480; SD ≈ ${fmt(math.sqrt(11700), 2)}"),
        ("Why might the independence assumption be questionable?", "Busy days raise both drink and food sales, so D and F are likely positively correlated")],
       ["1 point each part."], family="u3_shop_or", std=sd_ + [PC], check={"kind": "combine", "signs": [1, 1], "means": [820, 340], "sds": [90, 60]})


def s09():
    k, sd_ = 9, [PD + ".1", PD + ".2"]
    for lv, p, n, ctx in [("cp2", 0.6, 100, "60% of students at a large school ride the bus. For SRSs of 100 students,"),
                          ("cp1", 0.15, 400, "15% of a city's adults bike to work. For random samples of 400 adults,")]:
        sdv = math.sqrt(p * (1 - p) / n)
        SA(U, k, lv, ctx + " find the mean and standard deviation of the sampling distribution of p̂ (four decimals).", f"Mean {fmt(p)}, SD ≈ {fmt(sdv, 4)}",
           [f"μ_p̂ = p = {fmt(p)}.", f"σ_p̂ = √(p(1 − p)/n) = √({fmt(p)}·{fmt(1 - p)}/{n}) ≈ {fmt(sdv, 4)}.", "This SD formula requires the 10% condition (sample less than 10% of the population)."],
           family="u3_phat_ms", std=sd_, check={"kind": "phat_ms", "p": p, "n": n})
    SA(U, k, "cp2", "Scores on a test have mean 64 and SD 8. For random samples of 16 students, find the mean and standard deviation of the sampling distribution of x̄.",
       "Mean 64, SD 2", ["μ_x̄ = μ = 64.", "σ_x̄ = σ/√n = 8/√16 = 8/4 = 2."], family="u3_xbar_ms", std=sd_, check={"kind": "xbar_ms", "mu": 64, "sigma": 8, "n": 16})
    MC(U, k, "cp2", "The sampling distribution of a statistic is",
       "the distribution of the statistic's values over all possible samples of the same size", ["the distribution of data in one sample", "the population distribution", "a list of all individuals in a sample"],
       ["It shows how a statistic varies from sample to sample."], family="u3_sampdist_def", std=sd_)
    MC(U, k, "cp2", "A population proportion is p = 0.3. Which describes the center of the sampling distribution of p̂ for samples of size 50?", "0.3", ["15", "0.06", "0.5"],
       ["p̂ is unbiased: its sampling distribution is centered at p = 0.3."], family="u3_phat_center", std=sd_)
    MC(U, k, "cp2", "“In a sample of 80 batteries, the mean life was 41.2 hours; the manufacturer's process mean is 40 hours.” Which is a parameter and which is a statistic?",
       "41.2 is a statistic (x̄); 40 is a parameter (μ).", ["41.2 is a parameter; 40 is a statistic.", "Both are statistics.", "Both are parameters."],
       ["Sample values are statistics; process/population values are parameters."], family="u3_param_stat", std=sd_)
    sdv = math.sqrt(0.08 * 0.92 / 200)
    z = round(0.02 / sdv, 2)
    num_mc(U, k, "cp2", "A large shipment has 8% defective items. In an SRS of 200 items, what is the probability that the sample proportion defective exceeds 0.10? Use z rounded to two decimals; give four decimals.",
           1 - Phi(z), [Phi(z), 0.10, 0.5], 4,
           ["Large counts: 200(0.08) = 16 and 200(0.92) = 184, both ≥ 10.", f"σ_p̂ = √(0.08·0.92/200) ≈ {fmt(sdv, 4)}.", f"z = (0.10 − 0.08)/{fmt(sdv, 4)} ≈ {fmt(z, 2)}.", f"P(Z > {fmt(z, 2)}) ≈ {fmt(1 - Phi(z), 4)}."],
           family="u3_phat_prob", std=sd_, bounds=(0, 1), check={"kind": "phat_prob", "p": 0.08, "n": 200, "c": 0.10, "type": "gt"})
    s8 = 4 / math.sqrt(8)
    z = round(-2 / s8, 2)
    SA(U, k, "cp1", "Bottle fills are Normal with mean 500 mL and SD 4 mL. For random samples of 8 bottles, find P(x̄ < 498) using z rounded to two decimals; give four decimals.",
       f"≈ {fmt(Phi(z), 4)}",
       [f"σ_x̄ = 4/√8 ≈ {fmt(s8, 4)} mL.", "The population is Normal, so x̄ is Normal for any n.", f"z = (498 − 500)/{fmt(s8, 4)} ≈ {fmt(z, 2)}.", f"P ≈ {fmt(Phi(z), 4)}."],
       family="u3_xbar_prob", std=sd_, check={"kind": "xbar_prob", "mu": 500, "sigma": 4, "n": 8, "c": 498, "type": "lt"})
    MC(U, k, "cp1", "For which sample is the Normal approximation for p̂ appropriate if p = 0.04?", "n = 300", ["n = 100", "n = 150", "n = 200"],
       ["Need np ≥ 10 and n(1 − p) ≥ 10.", "300(0.04) = 12 ✓; 200(0.04) = 8 ✗."], family="u3_large_counts", std=sd_)
    MC(U, k, "cp1", "Why does the formula σ_p̂ = √(p(1 − p)/n) require the sample to be less than 10% of the population?",
       "When sampling without replacement, observations are nearly independent only if the sample is a small fraction of the population.", ["So that the sampling distribution is Normal.", "To make p̂ unbiased.", "Because n must be at least 10."],
       ["The 10% condition justifies the independence used in the SD formula."], family="u3_ten_pct", std=sd_)
    z = round(-0.06 / math.sqrt(0.16 / 150), 2)
    OR(U, k, "honors", "A candy company says 20% of its candies are orange. A student takes a random sample of 150 candies and finds 21 orange ones.",
       [("Find p̂.", "0.14"), ("Describe the sampling distribution of p̂ if the company's claim is true (shape, center, spread to four decimals).", f"Approximately Normal (150(0.2) = 30 and 150(0.8) = 120 ≥ 10), mean 0.20, SD ≈ {fmt(math.sqrt(0.16 / 150), 4)}"),
        ("Find P(p̂ ≤ 0.14) if the claim is true (z to two decimals).", f"z ≈ {fmt(z, 2)}; ≈ {fmt(Phi(z), 4)}"),
        ("Does the sample give convincing evidence that the company's claim is too high? Explain.", f"Yes; a sample proportion this low would occur only about {fmt(100 * Phi(z), 1)}% of the time if p = 0.20")],
       ["1 point each part."], family="u3_phat_or", std=sd_, check={"kind": "phat_prob", "p": 0.2, "n": 150, "c": 0.14, "type": "lt"})
    SA(U, k, "honors", "Error analysis. For a population with mean 50 and SD 12 (strongly skewed), a student finds P(x̄ > 53) for samples of n = 4 by computing z = (53 − 50)/(12/√4) = 0.5 and using the Normal table. What is wrong?",
       "With n = 4 from a strongly skewed population, the sampling distribution of x̄ is not approximately Normal, so the Normal table should not be used (the CLT needs a larger n).",
       ["The mean and SD of x̄ are computed correctly (50 and 6).", "But a Normal calculation requires x̄ to be approximately Normal.", "The population is strongly skewed and n = 4 is small, so the CLT does not apply.", "A larger sample (e.g., n ≥ 30) or a simulation would be needed."],
       family="u3_clt_error", std=sd_ + [PD + ".3"])
    MC(U, k, "honors", "Two samples give p̂₁ from n = 100 and p̂₂ from n = 400, both from a large population with p = 0.5. How do the SDs of their sampling distributions compare?",
       "SD for n = 400 is half the SD for n = 100.", ["They are equal.", "SD for n = 400 is one-fourth the SD for n = 100.", "SD for n = 400 is twice as large."],
       ["σ ∝ 1/√n; √(400/100) = 2."], family="u3_sd_ratio", std=sd_)


def s10():
    k, sd_ = 10, [PD + ".2", PD + ".3"]
    mcs(k, "cp2", [
        ("What happens to the variability of a sample statistic as the sample size increases (with random sampling)?",
         "It decreases.", ["It increases.", "It stays the same.", "It becomes biased."], ["Larger random samples give statistics that vary less from sample to sample."]),
        ("A statistic is called unbiased if",
         "the center of its sampling distribution equals the parameter", ["it always equals the parameter", "it comes from a large sample", "it has a small standard deviation"],
         ["Unbiased = correct on average."]),
        ("A dartboard picture shows darts tightly grouped but far from the bullseye. In statistical terms this shows",
         "low variability, high bias", ["high variability, low bias", "low variability, low bias", "high variability, high bias"],
         ["Tight grouping = low variability; off-center = biased."]),
        ("The Central Limit Theorem says that for large n,",
         "the sampling distribution of x̄ is approximately Normal regardless of the population's shape", ["the population becomes Normal", "every sample is Normal", "x̄ equals μ"],
         ["The CLT is about the distribution of sample means."]),
        ("Which change makes a sampling distribution of x̄ narrower?",
         "Increasing the sample size", ["Increasing the population size from 1 million to 2 million", "Using a biased sampling method", "Decreasing the sample size"],
         ["σ_x̄ = σ/√n depends on n, not on the population size (when n is small relative to it)."]),
    ], "u3_bias_var_basic", sd_)
    SA(U, k, "cp2", "A population has SD σ = 20. Find σ_x̄ for samples of size 25 and of size 100. By what factor did the SD shrink?",
       "4 and 2; it was cut in half", ["n = 25: 20/√25 = 4.", "n = 100: 20/√100 = 2.", "Quadrupling n halves σ_x̄."], family="u3_sd_shrink", std=sd_)
    SEL(U, k, "cp2", "Select ALL statements that are true about a sample mean x̄ from a random sample.",
        ["x̄ is an unbiased estimator of μ.", "x̄ varies less for larger samples."], ["x̄ always equals μ.", "Larger samples make x̄ biased."],
        ["μ_x̄ = μ; σ_x̄ = σ/√n."], family="u3_xbar_sel", std=sd_)
    SA(U, k, "cp1", "A population has σ = 15. How large a sample is needed so that the standard deviation of x̄ is at most 2?",
       "57", ["Need 15/√n ≤ 2.", "√n ≥ 7.5, so n ≥ 56.25.", "Round up: n = 57.", "Check: 15/√57 ≈ 1.99 ≤ 2."], family="u3_n_for_sd", std=sd_, check={"kind": "n_for_sd", "sigma": 15, "target": 2})
    MC(U, k, "cp1", "Incomes in a town are strongly skewed right with mean $52,000 and SD $30,000. Which has an approximately Normal distribution?",
       "The mean income of a random sample of 100 residents", ["The income of one randomly chosen resident", "The incomes of a random sample of 100 residents", "The mean income of a random sample of 3 residents"],
       ["The CLT applies to sample means with large n; individual values and small-sample means stay skewed."], family="u3_clt_apply", std=sd_)
    MC(U, k, "honors", "The sample range is used to estimate the population range. Why is it a biased estimator?",
       "A sample's range can never exceed the population's range and is usually smaller, so on average it underestimates.", ["Its sampling distribution has no center.", "It always overestimates.", "Ranges cannot be computed from samples."],
       ["The sampling distribution of the sample range is centered below the population range."], family="u3_range_biased", std=sd_)
    MC(U, k, "honors", "A population of 1,000,000 and another of 10,000 each have p = 0.4. Random samples of n = 500 are taken from each. How do the SDs of p̂ compare?",
       "Approximately equal, because both samples are no more than 10% of their populations", ["The larger population gives a much larger SD", "The smaller population gives a much larger SD", "Cannot compare without p̂"],
       ["σ_p̂ = √(p(1−p)/n) does not depend on population size when n ≤ 10% of N (500 ≤ 1,000 ✓)."], family="u3_pop_size", std=sd_)
    OR(U, k, "honors", "Wait times at a clinic are strongly skewed right with mean 18 minutes and SD 12 minutes. An administrator will take a random sample of wait times.",
       [("Can you find the probability that one randomly selected patient waits more than 24 minutes using a Normal model? Explain.", "No; individual wait times are strongly skewed, not Normal"),
        ("For random samples of 36 patients, describe the sampling distribution of x̄ (shape, center, spread).", "Approximately Normal by the CLT (n = 36 ≥ 30); mean 18 min; SD 12/√36 = 2 min"),
        ("Find P(x̄ > 21) for n = 36 (z to two decimals).", f"z = 1.50; P ≈ {fmt(1 - Phi(1.5), 4)}"),
        ("How would the answer to (c) change for n = 144? Explain without exact calculation.", "Smaller: σ_x̄ = 1, so 21 is 3 SDs above the mean and the probability is much smaller")],
       ["1 point each part."], family="u3_clt_or", std=sd_, check={"kind": "xbar_prob", "mu": 18, "sigma": 12, "n": 36, "c": 21, "type": "gt"})
    SA(U, k, "honors", "Two methods estimate a parameter θ = 50. Method A's sampling distribution has mean 50 and SD 6. Method B has mean 48 and SD 1. Which would you prefer, and why? Consider bias and variability.",
       "Method B is likely preferable: although slightly biased (by 2), its much smaller variability means its estimates are usually closer to 50 than Method A's.",
       ["A is unbiased but spread out: estimates typically about 6 away from 50.", "B is biased by 2 but has SD 1: estimates are typically within about 2–3 of 50.", "Overall error matters: B's typical error is smaller.", "Ideal estimators have both low bias and low variability."],
       family="u3_bias_tradeoff", std=sd_)


def build():
    for f in (s01, s02, s03, s04, s05, s06, s07, s08, s09, s10):
        f()
