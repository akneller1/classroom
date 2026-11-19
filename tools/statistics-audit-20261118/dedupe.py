"""Statistics audit #14 (2026-11-18): exact duplicate prompts inside a skill get a new wording in context.
The answers stay the same, so Partner Check pairs still match. (The repeated "Answer each part. Show your work."
stems are replaced by the free-response problems in batch S2.) Idempotent."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

NEW = {
 'stat-u2-s06-cp2-x04': ('A drug study is run as a double-blind experiment. This means', None),
 'stat-u3-s02-cp2-x08': ('The probability that a randomly chosen student walks to school is 0.35. What is the probability that the student does not walk to school?',
                         ['Complement rule: P(not A) = 1 − P(A).', '1 − 0.35 = 0.65.']),
 'stat-u3-s02-cp1-x09': ('At a school, P(plays a sport) = 0.5, P(in the band) = 0.4, and P(both) = 0.1. Find P(plays a sport or is in the band).',
                         ['Addition rule: P(A or B) = P(A) + P(B) − P(A and B).', '0.5 + 0.4 − 0.1 = 0.8.']),
 'stat-u3-s05-cp1-x10': ('The number of pets X in a household takes the values 0, 1, 2 and 3 with probabilities 0.1, 0.3, 0.45 and k. Find k.',
                         ['The probabilities of a distribution add to 1.', 'k = 1 − (0.1 + 0.3 + 0.45) = 1 − 0.85 = 0.15.']),
 'stat-u3-s10-honors-x08': ('About 4% of a factory\'s parts are defective. What is the smallest sample size n for which the expected number of defective parts, np, is at least 10?',
                            ['Solve np ≥ 10 with p = 0.04.', 'n ≥ 10/0.04 = 250, so n = 250.']),
 'stat-u4-s02-cp2-x15': ('To use a Normal model for the sampling distribution of p̂, which condition must the sample meet?', None),
 'stat-u4-s03-cp2-x12': ('A poll will report a 95% confidence interval for a proportion. What critical value z* does it use?',
                         ['z* cuts off the middle 95% of the standard Normal distribution, leaving 2.5% in each tail.', 'z* = 1.96.']),
 'stat-u4-s02-cp1-x07': ('A lab builds 100 separate 90% confidence intervals from 100 independent random samples. About how many of them should fail to capture the true parameter?',
                         ['In the long run 10% of 90% intervals miss.', '100 × 0.10 = 10.']),
 'stat-u4-s02-cp1-x08': ('A class builds 200 independent 95% confidence intervals for the same parameter. How many would you expect to miss it?',
                         ['In the long run 5% of 95% intervals miss.', '200 × 0.05 = 10.']),
 'stat-u4-s10-cp2-x09': ('Twelve students are measured before and after a training program, and a paired t procedure is used on the 12 differences. How many degrees of freedom does it use?',
                         ['A paired t procedure is a one-sample t procedure on the differences: df = (number of pairs) − 1.', 'df = 12 − 1 = 11.']),
}


def main():
    banks = lib.load()
    seen = set()
    for u, q in lib.items(banks):
        if q['id'] in NEW:
            p, steps = NEW[q['id']]
            q['prompt'] = p
            if steps:
                q['solutionSteps'] = steps
            seen.add(q['id'])
    assert seen == set(NEW), set(NEW) - seen
    lib.save(banks)


if __name__ == '__main__':
    main()
