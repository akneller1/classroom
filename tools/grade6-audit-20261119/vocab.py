"""Grade 6 audit #15 (2026-11-19): core Grade 6 terms in the unit vocabulary banks (flashcards, crosswords, vocabulary
activities and games). Appends each term to its unit's entry in worksheet-generator/vocabulary-data-middle-grades.js if
the unit does not already have it. Format: term|definition|example|draw prompt. Idempotent."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

FILE = os.path.join(lib.ROOT, 'worksheet-generator', 'vocabulary-data-middle-grades.js')
ADD = {
    'ratios-rates-percent-proportions': [
        ('double number line', 'Two number lines lined up so that matching amounts sit above each other, which shows equivalent ratios.', '0, 3, 6, 9 cups above 0, 2, 4, 6 eggs', 'Draw a double number line for 2 pizzas for every 5 students.'),
        ('tape diagram', 'A bar split into equal parts that shows how two quantities in a ratio compare.', '3 parts red and 2 parts blue for 3 : 2', 'Draw a tape diagram for the ratio 4 : 1.'),
        ('percent of a number', 'A part found by multiplying the whole by the percent written as a fraction or decimal.', '25% of 80 = 0.25 × 80 = 20', 'Draw a bar of 100% and shade 25% of it.'),
    ],
    'fractions-decimals-operations': [
        ('dividend', 'The number being divided.', 'In 12 ÷ 3, the dividend is 12', 'Draw 12 counters split into equal groups and label the dividend.'),
        ('divisor', 'The number you divide by.', 'In 12 ÷ 3, the divisor is 3', 'Draw 12 counters in groups of 3 and label the divisor.'),
        ('product', 'The result of multiplying.', 'The product of 4 and 2.5 is 10', 'Draw an area model for 4 × 2.5.'),
    ],
    'rational-numbers': [
        ('opposite', 'The number the same distance from 0 on the other side of 0.', 'The opposite of -6 is 6', 'Draw a number line with -6 and 6 marked the same distance from 0.'),
    ],
    'expressions-equations': [
        ('order of operations', 'The rules for which operation to do first: grouping, exponents, multiplication and division left to right, then addition and subtraction left to right.', '5 + 3 × 2 = 11', 'Draw the steps of 2 + 3² × 4 as a flow chart.'),
        ('evaluate', 'Find the value of an expression by replacing each variable with a number.', '3x + 1 when x = 4 is 13', 'Draw a box for x and show 4 going into it.'),
        ('sum', 'The result of adding.', 'The sum of n and 5 is n + 5', 'Draw a bar for n and a bar for 5 joined together.'),
        ('difference', 'The result of subtracting.', 'The difference of 10 and n is 10 - n', 'Draw a bar of 10 with a part n removed.'),
    ],
    'geometry': [
        ('polygon', 'A closed plane figure made of straight sides.', 'Triangles, rectangles and hexagons are polygons', 'Draw three polygons and one shape that is not a polygon.'),
        ('prism', 'A solid with two identical parallel bases joined by rectangles.', 'A box is a rectangular prism', 'Draw a triangular prism and shade its bases.'),
        ('face', 'A flat surface of a solid.', 'A cube has 6 faces', 'Draw a cube and shade one face.'),
        ('edge', 'A segment where two faces of a solid meet.', 'A cube has 12 edges', 'Draw a cube and trace its edges.'),
    ],
    'data-displays': [
        ('distribution', 'How the values of a data set are spread out: their center, spread and shape.', 'A dot plot with a peak at 5 and a tail to the right', 'Draw a dot plot and describe its center, spread and shape.'),
        ('measure of center', 'A single number that describes a typical value: the mean or the median.', 'The median of 2, 4, 9 is 4', 'Draw a dot plot and mark the mean and the median.'),
        ('measure of variability', 'A single number that describes how spread out data are: the range, IQR or MAD.', 'The range of 2, 4, 9 is 7', 'Draw two dot plots with the same center and different spreads.'),
        ('variability', 'How much the values in a data set differ from one another.', 'Test scores 60 to 100 vary more than 78 to 82', 'Draw two dot plots, one with more variability.'),
        ('frequency', 'How many times a value or interval occurs in a data set.', 'The value 7 occurs 3 times', 'Draw a frequency table with tally marks.'),
        ('quartile', 'A value that splits ordered data into quarters: Q1, the median and Q3.', 'In 1–9, Q1 = 2.5 and Q3 = 7.5', 'Draw a box plot and label Q1, the median and Q3.'),
        ('mode', 'The value that occurs most often in a data set.', 'The mode of 2, 3, 3, 8 is 3', 'Draw a dot plot and circle the tallest stack.'),
        ('cluster', 'A group of data values that are close together.', 'Most values are between 10 and 14', 'Draw a dot plot with one cluster and circle it.'),
        ('peak', 'The value or interval with the most data in a distribution.', 'A histogram is tallest at 20–29', 'Draw a histogram and mark its peak.'),
        ('gap', 'An interval with no data values between other values.', 'No values between 12 and 18', 'Draw a dot plot with a gap and label it.'),
    ],
}


def main():
    s = open(FILE, encoding='utf-8').read()
    added = 0
    for unit, rows in ADD.items():
        assert not any(';' in f or '|' in f for r in rows for f in r), unit
        key = 'math6-' + unit
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
