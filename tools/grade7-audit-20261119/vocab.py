"""Grade 7 audit #19 (2026-11-19): core Grade 7 terms in the unit vocabulary banks (flashcards, crosswords, vocabulary
activities and games). Appends each term to its unit's entry in worksheet-generator/vocabulary-data-middle-grades.js if
the unit does not already have it. Format: term|definition|example|draw prompt. Idempotent."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

FILE = os.path.join(lib.ROOT, 'worksheet-generator', 'vocabulary-data-middle-grades.js')
ADD = {
    'algebraic-expressions-integers': [
        ('additive inverse', 'The opposite of a number. A number and its additive inverse add to 0.', '-7 + 7 = 0', 'Draw a number line showing a jump of 5 and a jump of -5 that end back at 0.'),
    ],
    'ratios-proportions-percentages': [
        ('proportional relationship', 'A relationship in which y = kx: every y-value is the same multiple k of its x-value, and the graph is a line through the origin.', 'y = 3x', 'Draw a graph of a proportional relationship and label the origin and the point (1, k).'),
        ('constant of proportionality', 'The unit rate k in y = kx, which is the value of y when x = 1.', 'In y = 2.5x, k = 2.5', 'Draw a table for y = 4x and circle the constant of proportionality.'),
        ('scale drawing', 'A drawing in which every length is the actual length multiplied by the same scale factor.', 'A map where 1 cm represents 5 km', 'Draw a rectangle 6 m by 4 m at a scale of 1 cm : 2 m and label both sizes.'),
        ('scale factor', 'The number every length is multiplied by to go from one figure to a scaled copy.', 'A 4-in. side becomes 10 in.: scale factor 2.5', 'Draw a small triangle and a copy with scale factor 2, and label the matching sides.'),
        ('percent error', 'The size of the error as a percent of the actual value: (difference between the estimate and the actual value) ÷ actual × 100%.', 'Estimate 45, actual 50: 10% error', 'Draw a bar model comparing an estimate with the actual value and shade the error.'),
        ('commission', 'Pay that is a percent of the amount sold.', '5% commission on $2,000 of sales is $100', 'Draw a bar for total sales and shade the commission part.'),
    ],
    'spatial-thinking': [
        ('adjacent angles', 'Two angles that share a vertex and a side but do not overlap.', '∠ABD and ∠DBC share ray BD', 'Draw two adjacent angles and mark the common side.'),
        ('dilation', 'A transformation that enlarges or reduces a figure by a scale factor from a center. Angles stay the same.', '(x, y) → (2x, 2y)', 'Draw a triangle and its dilation by scale factor 2 from the origin.'),
    ],
    'area-volume': [
        ('cross-section', 'The two-dimensional shape you get when a plane slices a solid.', 'Slicing a cylinder parallel to its base gives a circle', 'Draw a rectangular prism and the cross-section made by a slice parallel to the base.'),
    ],
    'data-analysis-probability': [
        ('population', 'The whole group you want information about.', 'All 900 students in a school', 'Draw a large group with a smaller random sample circled inside it.'),
        ('inference', 'A conclusion about a population drawn from data in a random sample.', '12 of 40 sampled students walk, so about 30% of all students walk', 'Draw a sample and an arrow to the conclusion about the population.'),
        ('simulation', 'A model that uses random tools (coins, number cubes, random digits) to estimate a probability.', 'Use a number cube to model a 1/6 chance in each of 3 trials', 'Draw a table of 10 simulated trials and mark the successes.'),
        ('compound event', 'An event made of two or more simple events.', 'Rolling a 6 and then flipping heads', 'Draw a tree diagram for a coin flip followed by a spinner with 3 colors.'),
    ],
}


def main():
    s = open(FILE, encoding='utf-8').read()
    added = 0
    for unit, rows in ADD.items():
        assert not any(';' in f or '|' in f for r in rows for f in r), unit
        key = 'prealgebra7-' + unit
        m = re.search(r'("' + re.escape(key) + r'"\s*:\s*)"((?:[^"\\]|\\.)*)"', s)
        assert m, key
        cur = json.loads('"' + m.group(2) + '"')
        have = {r.split('|')[0].strip().lower() for r in cur.split(';') if r}
        new = cur
        for row in rows:
            if row[0].lower() not in have:
                new = new.rstrip(';') + ';' + '|'.join(row)
                added += 1
        if new != cur:
            s = s[:m.start(2)] + json.dumps(new, ensure_ascii=False)[1:-1] + s[m.end(2):]
    open(FILE, 'w', encoding='utf-8').write(s)
    print('vocabulary terms added:', added)


if __name__ == '__main__':
    main()
