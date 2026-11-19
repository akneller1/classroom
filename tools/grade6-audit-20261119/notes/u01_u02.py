import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import rec, card

A, B = 'ratios-rates-percent-proportions', 'fractions-decimals-operations'
R = {}

# ---------- Ratios, Rates, Percent and Proportions ----------
R[A, 1] = rec('write ratios in words and with a colon, and use tape diagrams to find the parts of a ratio',
  'A ratio compares two quantities. 3 : 2 means for every 3 of the first there are 2 of the second. In a tape diagram every box is the same size, so the total divided by the number of boxes gives one box.',
  [('ratio', 'A comparison of two quantities, written a to b, a : b or as a fraction.'), ('tape diagram', 'A drawing of equal boxes that shows the parts of a ratio.')],
  'Writing the ratio in the wrong order: “boys to girls” puts the number of boys first.',
  'For every ___ there are ___, so the ratio is ___ to ___.',
  card('Parts of a ratio with a tape diagram', 'Red to blue is 3 : 2, with 40 marbles in all.',
       'Boxes: 3 + 2 = {{5}}', 'One box: ⟨\\frac{40}{5} = {{8}}⟩', 'Red: ⟨3 \\times 8 = {{24}}⟩ marbles'))
R[A, 2] = rec('find unit rates and use them to solve problems',
  'A unit rate tells how much for one unit. Divide the first quantity by the second: $12 for 4 pounds is ⟨\\frac{12}{4} = 3⟩ dollars per pound.',
  [('rate', 'A ratio of two quantities with different units, such as miles per hour.'), ('unit rate', 'A rate for one unit of the second quantity.')],
  'Dividing in the wrong order: pounds per dollar is not the price per pound.',
  'The unit rate is ___ per ___, so ___ would be ___.',
  card('Find the unit rate', '$4.80 for 16 ounces.',
       '⟨\\frac{4.80}{16} = {{0.30}}⟩ dollars per ounce', '24 ounces: ⟨24 \\times 0.30 = {{7.20}}⟩ dollars'))
R[A, 3] = rec('make tables of equivalent ratios and use double number lines to find missing values',
  'Multiplying or dividing both quantities by the same number gives an equivalent ratio. A double number line lines up matching values, and a table lists them in columns.',
  [('equivalent ratios', 'Ratios that name the same comparison, such as 2 : 3 and 8 : 12.'), ('double number line', 'Two number lines lined up so that matching values are directly across from each other.')],
  'Adding the same number to both quantities: 2 : 3 is not equivalent to 4 : 5.',
  'I multiplied both quantities by ___, so ___ matches ___.',
  card('Equivalent ratios in a table', '2 cups of flour make 12 muffins.',
       '4 cups: ⟨2 \\times 2 = 4⟩, ⟨12 \\times 2 = {{24}}⟩ muffins', '6 cups: ⟨12 \\times 3 = {{36}}⟩ muffins', '1 cup: ⟨\\frac{12}{2} = {{6}}⟩ muffins'))
R[A, 4] = rec('compare ratios by finding unit rates or equivalent ratios with a common term',
  'To compare two ratios, make one of their terms the same (or find each unit rate), then compare the other term.',
  [('compare', 'Decide which of two quantities is greater, or whether they are equal.'), ('common term', 'A value that both ratios share after scaling, so the other values can be compared.')],
  'Comparing only the first numbers: 3 : 9 and 5 : 7 can’t be compared by looking at 3 and 5 alone.',
  'Mix ___ is fruitier because ___ is greater than ___.',
  card('Which mix is fruitier?', 'Mix A: 3 cups juice to 9 cups water. Mix B: 5 cups juice to 7 cups water.',
       'Juice per cup of water, A: ⟨\\frac{3}{9} = {{\\frac{1}{3}}}⟩', 'B: ⟨{{\\frac{5}{7}}}⟩', '⟨\\frac{5}{7} > \\frac{1}{3}⟩, so Mix {{B}}'))
R[A, 5] = rec('use equivalent ratios and unit rates to find a missing value in a proportion',
  'A proportion says two ratios are equal. Find the scale factor between the known terms, or use the unit rate, and apply it to the other term.',
  [('proportion', 'An equation stating that two ratios are equal.'), ('scale factor', 'The number you multiply one quantity by to get the matching quantity.')],
  'Using the scale factor on the wrong quantity: scale 4 → 12 is ×3, so multiply the other term of that same ratio by 3.',
  'The ratio grows by a factor of ___, so the missing value is ___.',
  card('Solve with a scale factor', '⟨\\frac{4}{7} = \\frac{12}{x}⟩',
       '4 to 12 is ⟨\\times {{3}}⟩', '⟨x = 7 \\times 3 = {{21}}⟩'),
  )
R[A, 6] = rec('find a percent of a number and find the whole when a part and the percent are known',
  'Percent means per hundred: 30% is ⟨\\frac{30}{100}⟩. Part = percent × whole, so whole = part ÷ percent.',
  [('percent', 'A rate per 100.'), ('whole', 'The total amount that the percent is taken of; it is 100%.')],
  'Finding the percent of the part instead of the whole: if 18 is 30% of a number, the number is bigger than 18.',
  'The part is ___ and it is ___ percent, so the whole is ___.',
  card('Find the whole', '18 is 30% of what number?',
       '⟨\\frac{30}{100} \\times w = 18⟩', '⟨w = 18 \\times \\frac{100}{30} = {{60}}⟩', 'Check: 30% of 60 is {{18}}'))
R[A, 7] = rec('write fractions and decimals as percents and percents as fractions and decimals',
  'Write the fraction with a denominator of 100, or divide the numerator by the denominator and move the decimal point two places right.',
  [('equivalent', 'Having the same value, such as ⟨\\frac{3}{4}⟩, 0.75 and 75%.'), ('per hundred', 'Out of 100; what “percent” means.')],
  'Moving the decimal point the wrong way: 0.4 is 40%, not 4% or 0.004%.',
  'I wrote ___ as ___ hundredths, which is ___ percent.',
  card('Fraction → decimal → percent', '⟨\\frac{3}{4}⟩',
       '⟨\\frac{3}{4} = \\frac{{{75}}}{100}⟩', '= {{0.75}}', '= {{75}}%'))
R[A, 8] = rec('convert measurement units with ratios',
  'A conversion factor is a ratio equal to 1, such as 12 inches per foot. Multiply when going to a smaller unit and divide when going to a larger unit.',
  [('conversion factor', 'A rate such as 12 inches per 1 foot used to change units.'), ('unit', 'A fixed amount used to measure, such as an inch, a liter or a pound.')],
  'Multiplying when you should divide: 36 inches is fewer feet, so divide by 12.',
  'One ___ is ___ ___, so I ___ by ___.',
  card('Convert with a ratio', '5 feet to inches; 48 ounces to pounds.',
       '⟨5 \\times 12 = {{60}}⟩ inches', '⟨\\frac{48}{16} = {{3}}⟩ pounds'))

# ---------- Operations of Fractions and Decimals ----------
R[B, 1] = rec('divide fractions with models and with multiplication by the reciprocal',
  '⟨a \\div b⟩ asks how many groups of b fit in a. Dividing by a fraction is the same as multiplying by its reciprocal.',
  [('reciprocal', 'One of two numbers whose product is 1, such as ⟨\\frac{2}{3}⟩ and ⟨\\frac{3}{2}⟩.'), ('quotient', 'The answer to a division problem.')],
  'Flipping the first fraction instead of the divisor.',
  'I asked how many groups of ___ fit in ___, and the answer is ___.',
  card('How many groups?', '⟨\\frac{5}{3} \\div \\frac{2}{3}⟩',
       'In thirds: 5 parts ÷ 2 parts', '⟨\\frac{5}{3} \\times \\frac{3}{2} = \\frac{15}{6} = {{2\\frac{1}{2}}}⟩', '2 full groups and {{\\frac{1}{2}}} of a group'))
R[B, 2] = rec('divide whole numbers by fractions and fractions by whole numbers',
  'A whole number divided by a fraction less than 1 gives a larger number: ⟨3 \\div \\frac{1}{4} = 12⟩ because 4 quarters fit in each whole.',
  [('dividend', 'The number being divided.'), ('divisor', 'The number you divide by.')],
  'Expecting division to always make a number smaller.',
  'There are ___ groups of ___ in each whole, so in ___ wholes there are ___.',
  card('Whole number ÷ fraction', '⟨3 \\div \\frac{1}{4}⟩ and ⟨\\frac{3}{4} \\div 3⟩',
       '⟨3 \\times 4 = {{12}}⟩', '⟨\\frac{3}{4} \\times \\frac{1}{3} = {{\\frac{1}{4}}}⟩'))
R[B, 3] = rec('divide mixed numbers and solve word problems with them',
  'Rewrite each mixed number as a fraction, multiply by the reciprocal of the divisor, and simplify. In a word problem, decide whether a remainder is a leftover piece or part of a group.',
  [('mixed number', 'A whole number and a fraction together, such as ⟨2\\frac{1}{2}⟩.'), ('improper fraction', 'A fraction whose numerator is greater than or equal to its denominator.')],
  'Dividing the whole numbers and the fractions separately.',
  'I rewrote ___ as ___ and multiplied by ___.',
  card('Mixed numbers', '⟨8\\frac{1}{4} \\div 1\\frac{3}{4}⟩',
       '⟨\\frac{33}{4} \\div \\frac{7}{4}⟩', '⟨= \\frac{33}{4} \\times \\frac{4}{7} = \\frac{33}{7} = {{4\\frac{5}{7}}}⟩', '4 full shelves; the leftover is {{\\frac{5}{7}}} of a shelf'))
R[B, 4] = rec('divide multi-digit whole numbers with the standard algorithm',
  'Long division repeats: divide, multiply, subtract, bring down. Estimating first tells you how many digits the quotient has.',
  [('remainder', 'What is left over when one whole number does not divide another evenly.'), ('estimate', 'A close answer found with rounded numbers.')],
  'Forgetting a 0 in the quotient when a partial dividend is smaller than the divisor.',
  'I estimated ___, so the quotient has ___ digits.',
  card('Divide, multiply, subtract, bring down', '⟨4{,}235 \\div 35⟩',
       'Estimate: ⟨4{,}200 \\div 35 = {{120}}⟩', '42 ÷ 35 = 1, 73 ÷ 35 = 2, 35 ÷ 35 = 1', 'Quotient: {{121}}'))
R[B, 5] = rec('add and subtract multi-digit decimals',
  'Line up the decimal points so you add tenths to tenths and hundredths to hundredths. Write zeros as placeholders when needed.',
  [('decimal point', 'The point separating the whole-number part from the fractional part.'), ('placeholder zero', 'A zero written so that every number has the same number of decimal places.')],
  'Lining up the last digits instead of the decimal points.',
  'I lined up the ___ and wrote ___ as a placeholder.',
  card('Line up the decimal points', '⟨14.6 - 3.875⟩',
       '⟨14.600 - 3.875⟩', '= {{10.725}}'))
R[B, 6] = rec('multiply and divide multi-digit decimals',
  'To multiply, multiply as whole numbers and count the decimal places in the factors. To divide by a decimal, multiply the divisor and the dividend by the same power of 10 so the divisor is a whole number.',
  [('factor', 'A number being multiplied.'), ('power of ten', 'A number such as 10, 100 or 1,000.')],
  'Placing the decimal point by lining it up, as in addition, when multiplying.',
  'There are ___ decimal places in the factors, so the product has ___.',
  card('Multiply, then divide', '⟨2.4 \\times 0.35⟩ and ⟨6.3 \\div 0.09⟩',
       '⟨24 \\times 35 = 840⟩, 3 places: {{0.840}}', '⟨630 \\div 9 = {{70}}⟩'))
R[B, 7] = rec('find the greatest common factor and least common multiple and use the distributive property to factor a sum',
  'The GCF is the largest number that divides both numbers; the LCM is the smallest number both divide. ⟨36 + 8 = 4(9 + 2)⟩ uses the GCF.',
  [('greatest common factor', 'The largest whole number that is a factor of two or more numbers.'), ('least common multiple', 'The smallest whole number that is a multiple of two or more numbers.')],
  'Mixing them up: for “when will both happen again?” you need the LCM.',
  'The question asks for ___, so I need the ___.',
  card('GCF and LCM of 12 and 18', 'Factors of 12: 1, 2, 3, 4, 6, 12. Factors of 18: 1, 2, 3, 6, 9, 18.',
       'GCF = {{6}}', 'Multiples: 12, 24, 36; 18, 36', 'LCM = {{36}}'))
R[B, 8] = rec('use the distributive property to multiply decimals and whole numbers mentally',
  'Break one factor into friendly parts, multiply each part, then add: ⟨4 \\times 2.05 = 4 \\times 2 + 4 \\times 0.05⟩.',
  [('distributive property', 'a(b + c) = ab + ac.'), ('partial product', 'The product of one factor and one part of the other factor.')],
  'Multiplying only the first part: ⟨4(2 + 0.05)⟩ is not ⟨8 + 0.05⟩.',
  'I split ___ into ___ and ___, then added the products.',
  card('Split and multiply', '⟨6 \\times 3.15⟩',
       '⟨6 \\times 3 + 6 \\times 0.15⟩', '⟨18 + {{0.9}}⟩', '= {{18.9}}'))
