/* Cheat-sheet content for the Quantitative Modeling units (2026-11-21). Same shapes as cheat-sheets.mjs.
 * Math inside ⟨...⟩ is rendered by Classroom's KaTeX renderer. */
const palette = ['purple', 'blue', 'green', 'orange', 'pink', 'teal'];
const T = (title, head, rows, after = '') => ({ title, kind: 'table', plain: true, head, rows, after });
const E = (title, text, example, steps, answer) => ({ title, kind: 'example', text, example, steps, answer });
const L = (title, items) => ({ title, kind: 'list', items });
const H = (title, html) => ({ title, kind: 'html', html });
const V = (title, rows) => ({ ...T(title, ['Term', 'Meaning / quick example'], rows), plain: false });
const M = (good, bad) => ({ title: 'Reminders & mistakes', kind: 'mistakes', good, bad });
const sheet = (focus, morefocus, front, back) => ({ focus, morefocus, front: front.map((s, i) => ({ ...s, color: palette[i] })), back: back.map((s, i) => ({ ...s, color: palette[i] })) });

export const sheets = {
consumer: sheet('find sale prices, tax, tips and percent change', 'compare unit prices, coupons and memberships', [
 V('Percent words', [['Percent', 'Per hundred: 18% = 0.18.'], ['Discount', 'Amount off the regular price.'], ['Markup', 'Amount added to a store’s cost.'], ['Unit price', 'Price ÷ quantity.']]),
 T('Multipliers', ['Change', 'Multiply by'], [['25% off', '0.75'], ['40% off', '0.60'], ['6% sales tax', '1.06'], ['15% increase', '1.15']], 'One multiplication does the whole change: ⟨\\text{new}=\\text{old}\\times(1\\pm r)⟩.'),
 E('Sale price', 'Multiply by what is left after the discount.', '$120 jacket, 30% off.', [['Multiplier:', '⟨1-0.30=0.70⟩'], ['Sale price:', '⟨0.70(120)=84⟩']], '$84'),
 E('Stacked discounts', 'The second discount comes off the sale price.', '$100, 20% off, then an extra 10% off.', [['First:', '⟨0.80(100)=80⟩'], ['Second:', '⟨0.90(80)=72⟩']], '$72 — a 28% total discount, not 30%'),
 E('Tax, tip and split', 'Tip on the pre-tax bill (custom). Total = bill + tax + tip.', '$84 bill, 6.25% tax, 20% tip, 3 people.', [['Tax and tip:', '⟨84(0.0625)=5.25;\\ 84(0.20)=16.80⟩'], ['Each:', '⟨\\dfrac{84+5.25+16.80}{3}=35.35⟩']], '$35.35 each'),
 H('Work backward', 'If a known change gave the new amount, divide by the multiplier:<br>⟨\\text{original}=\\dfrac{\\text{new}}{\\text{multiplier}}⟩<div class="ex">Paid $54 after 25% off: ⟨54\\div0.75=72⟩.<br>Receipt $53 with 6% tax: ⟨53\\div1.06=50⟩.</div>')
], [
 E('Percent change', '⟨\\dfrac{\\text{new}-\\text{original}}{\\text{original}}⟩ — always divide by the original.', 'Gas: $3.20 → $3.60.', [['Change:', '⟨3.60-3.20=0.40⟩'], ['Rate:', '⟨0.40\\div3.20=0.125⟩']], '12.5% increase'),
 E('Markup and profit', 'Price = cost × (1 + markup rate); profit = price − cost.', 'Cost $12, 60% markup, 50 sold.', [['Price:', '⟨12(1.60)=19.20⟩'], ['Profit:', '⟨50(19.20-12)=360⟩']], '$19.20 each; $360 profit'),
 T('Successive changes', ['Changes', 'Overall'], [['+10% then −10%', '⟨1.1(0.9)=0.99⟩ → −1%'], ['+50% then −50%', '⟨1.5(0.5)=0.75⟩ → −25%'], ['−20% then −20%', '⟨0.8(0.8)=0.64⟩ → −36%']], 'Percent changes multiply; they do not add.'),
 T('Unit prices', ['Package', 'Unit price'], [['12 oz for $3.60', '⟨3.60\\div12=0.30⟩ per oz'], ['18 oz for $5.94', '⟨5.94\\div18=0.33⟩ per oz']], 'Here the smaller box is the better buy. Use the same unit for every option.'),
 H('Membership break-even', 'A fee F that returns rate r of spending pays for itself at<br>⟨S=\\dfrac{F}{r}⟩<div class="ex">$60 fee, 5% back: ⟨60\\div0.05=1{,}200⟩ of spending a year.</div>Below that, the membership costs more than it saves.'),
 M(['Use one multiplier for each change.', 'Divide by the original for percent change.'], [['20% + 20% = 40% off', 'it is 36% off.'], ['Undo +10% with −10%', 'divide by 1.10 instead.'], ['Bigger box = better deal', 'check the unit price.'], ['Tip on the after-tax total', 'tip on the pre-tax bill by custom.']])
]),
linear: sheet('find rates of change and write linear models', 'compare plans, find break-even points and read tiered prices', [
 V('Linear words', [['Rate of change', 'Change in y per 1 of x (the slope).'], ['y-intercept', 'Value when x = 0: a fee or start.'], ['Fixed cost', 'Same no matter how many.'], ['Variable cost', 'Grows with each unit.']]),
 E('Slope from two points', '⟨m=\\dfrac{y_2-y_1}{x_2-x_1}⟩ with units: dollars per hour.', '2 hours: $210; 4 hours: $330.', [['Rate:', '⟨\\dfrac{330-210}{4-2}=60⟩'], ['Fee:', '⟨210-60(2)=90⟩']], '$60 per hour plus a $90 fee'),
 H('Linear model', '⟨y=mx+b⟩<br>m = rate (per unit); b = fixed starting amount.<div class="ex">Truck: $40 plus $0.80 a mile → ⟨C=0.80d+40⟩.<br>Budget $100: ⟨0.80d+40=100⟩ → ⟨d=75⟩ miles.</div>'),
 E('Goals with “at least”', 'Write an inequality; round whole units up to reach a goal.', '$120 saved, $16 an hour, goal at least $900.', [['Inequality:', '⟨120+16h\\ge900⟩'], ['Solve:', '⟨h\\ge48.75⟩']], '49 hours'),
 T('Reading a model', ['Model', 'Means'], [['C = 12m + 35', '$35 to join, $12 per month'], ['B = 150 − 6.5w', '$150 card, −$6.50 per week'], ['P = 9q − (600 + 3.2q)', 'profit on q plates']], 'Units tell the story: rate units are “per” something.'),
 L('Check a linear model', ['Does x = 0 give the fee or starting value?', 'Does x = 1 add exactly one rate?', 'Are the units in the answer?', 'Is rounding up or down sensible for whole items?'])
], [
 E('Break-even: two plans', 'Set the costs equal and solve.', 'A: $20 + $8 per visit. B: $50 + $5 per visit.', [['Equal:', '⟨20+8x=50+5x⟩'], ['Solve:', '⟨3x=30\\Rightarrow x=10⟩']], 'Same cost at 10 visits; B is cheaper above 10'),
 E('Break-even: a business', 'Each sale covers ⟨p-v⟩ of the fixed cost F.', 'F = $1,800; v = $3.20; p = $9.', [['Per sale:', '⟨9-3.20=5.80⟩'], ['Units:', '⟨1{,}800\\div5.80\\approx310.3⟩']], '311 plates (round up)'),
 H('Profit', '⟨P=(p-v)q-F⟩<div class="ex">q = 400, p = $9, v = $3.20, F = $1,800:<br>⟨5.80(400)-1{,}800=520⟩ → <b>$520 profit</b></div>A negative P is a loss.'),
 E('Tiered electricity', 'Each rate applies only inside its tier.', '$12 fee; $0.12 to 500 kWh; $0.18 above; 700 kWh.', [['Tiers:', '⟨500(0.12)+200(0.18)=96⟩'], ['Bill:', '⟨12+96=108⟩']], '$108'),
 E('“Or part of” and caps', 'Round partial units up; stop at any cap.', '$4 first hour, $2.50 each extra hour or part, $20 max; 3 h 10 min.', [['Billed hours:', '4'], ['Cost:', '⟨4+3(2.50)=11.50⟩']], '$11.50 (under the $20 cap)'),
 M(['Set models equal to compare plans.', 'Bill each tier at its own rate.'], [['Lower fee = cheaper plan', 'only below the break-even.'], ['F ÷ price for break-even', 'use F ÷ (price − variable cost).'], ['All usage at the top tier', 'only usage above the threshold.'], ['Round down for goals', 'round up to reach “at least.”']])
]),
exponential: sheet('model growth and decay with y = a·bᵗ', 'compare linear and exponential change, doubling and half-life', [
 V('Exponential words', [['Growth factor', '1 + rate: 6% → 1.06.'], ['Decay factor', '1 − rate: 15% → 0.85.'], ['Initial value', 'The amount at t = 0.'], ['Depreciation', 'Loss of value over time.']]),
 H('The model', '⟨y=a(1+r)^t⟩ growth &nbsp;·&nbsp; ⟨y=a(1-r)^t⟩ decay<br>a = start, r = rate per period (decimal), t = periods.<div class="ex">⟨V=1{,}100(0.80)^t⟩: a $1,100 laptop losing 20% a year.</div>'),
 E('Growth', 'Multiply by the factor once per period.', '$2,000 at 5% a year for 10 years.', [['Model:', '⟨2{,}000(1.05)^{10}⟩'], ['Value:', '⟨\\approx3{,}257.79⟩']], '$3,257.79'),
 E('Depreciation', 'Keep 1 − r of the value each year.', '$24,000 car, 15% a year, 3 years.', [['Model:', '⟨24{,}000(0.85)^3⟩'], ['Value:', '⟨\\approx14{,}739⟩']], 'About $14,739'),
 E('Rate from two values', 'factor = new ÷ old; rate = |factor − 1|.', 'Car: $30,000 → $25,800 in one year.', [['Factor:', '⟨25{,}800\\div30{,}000=0.86⟩'], ['Rate:', '⟨1-0.86=0.14⟩']], '14% per year'),
 L('Read a model', ['y = 3,200(1.045)ᵗ → starts at 3,200 and grows 4.5% per period.', 'y = 650(0.88)ᵗ → starts at 650 and decays 12% per period.', 'b > 1 grows; 0 < b < 1 decays.'])
], [
 T('Linear or exponential?', ['Table', 'Test', 'Type'], [['100, 130, 160, 190', 'differences +30', 'linear'], ['100, 120, 144, 172.8', 'ratios × 1.2', 'exponential'], ['500, 450, 405, 364.5', 'ratios × 0.9', 'exponential decay']], 'Same difference → linear. Same ratio → exponential.'),
 E('Flat raise vs. percent raise', 'Percent growth always passes linear growth eventually.', '$40,000: +$2,500 a year vs. +5% a year.', [['Year 10, flat:', '⟨40{,}000+2{,}500(10)=65{,}000⟩'], ['Year 10, percent:', '⟨40{,}000(1.05)^{10}\\approx65{,}156⟩']], 'The percent raise is ahead by year 10'),
 H('Rule of 72', '⟨\\text{doubling time}\\approx\\dfrac{72}{\\text{percent rate}}⟩<div class="ex">8% → ⟨72\\div8=9⟩ years. $1,000 becomes about $2,000 in 9 years and $4,000 in 18.</div>A quick estimate; for the exact whole year, find the first t with ⟨(1+r)^t\\ge2⟩.'),
 E('Half-life', 'Count half-lives, then halve that many times.', '320 mg, half-life 6 hours, after 18 hours.', [['Half-lives:', '⟨18\\div6=3⟩'], ['Left:', '⟨320\\left(\\tfrac12\\right)^3=40⟩']], '40 mg'),
 T('Doubling ladder', ['Doublings', 'Multiplier'], [['1', '× 2'], ['2', '× 4'], ['3', '× 8'], ['5', '× 32']], 'A $1,500 coin that doubles every 8 years is worth ⟨1{,}500(2^3)=12{,}000⟩ after 24 years.'),
 M(['Factor = 1 ± rate, not the rate.', 'Count periods carefully.'], [['10% twice = 20%', 'it is 21% (1.1² = 1.21).'], ['Decay reaches $0', 'it only gets closer to 0.'], ['Subtract r% of the original each year', 'that is linear, not exponential.'], ['Rule of 72 is exact', 'it is an estimate.']])
]),
data: sheet('summarize data and read scatterplots and correlation', 'predict with lines of best fit, residuals and honest graphs', [
 V('Data words', [['Mean', 'Sum ÷ count.'], ['Median', 'Middle value in order.'], ['Outlier', 'A value far from the rest.'], ['IQR', 'Q3 − Q1: spread of the middle half.']]),
 E('Mean or median?', 'Outliers pull the mean; the median resists.', 'Salaries $42k, $45k, $48k, $51k, $350k.', [['Median:', '$48,000'], ['Mean:', '⟨536{,}000\\div5=107{,}200⟩']], 'The median ($48,000) is more typical'),
 E('IQR', 'Order the data; Q1 and Q3 are the medians of the lower and upper halves.', '12, 15, 18, 20, 24, 27, 31, 40', [['Q1, Q3:', '⟨Q_1=16.5,\\ Q_3=29⟩'], ['IQR:', '⟨29-16.5=12.5⟩']], '12.5'),
 E('Score needed', 'Target total = target mean × number of scores.', '78, 85, 90; want a mean of 85 after 4.', [['Target total:', '⟨85(4)=340⟩'], ['Needed:', '⟨340-253=87⟩']], '87'),
 T('Reading r', ['r', 'Describe as'], [['−0.86', 'strong negative'], ['0.52', 'moderate positive'], ['0.12', 'weak positive']], 'Strong |r| ≥ 0.7; moderate 0.4–0.7; weak below 0.4. Sign gives direction.'),
 L('Correlation is not causation', ['Look for a lurking variable (heat → ice cream and sunburns).', 'Ask whether the cause could run the other way.', 'Only a randomized experiment shows cause and effect.'])
], [
 H('Line of best fit', '⟨\\hat y=mx+b⟩ — the hat means “predicted.”<br>Slope m: predicted change in y for each 1 unit of x.<div class="ex">⟨\\hat y=-145x+26{,}500⟩ (price vs. thousands of miles):<br>each 1,000 miles → $145 lower predicted price.</div>'),
 E('Predict and solve', 'Substitute x to predict; set ŷ to a value to solve for x.', '⟨\\hat y=-145x+26{,}500⟩', [['x = 60:', '⟨-145(60)+26{,}500=17{,}800⟩'], ['ŷ = $20,700:', '⟨x=(20{,}700-26{,}500)\\div(-145)=40⟩']], '$17,800; 40 thousand miles'),
 E('Residual', '⟨\\text{residual}=\\text{actual}-\\text{predicted}⟩', 'Predicted $17,800; listed $16,200.', [['Residual:', '⟨16{,}200-17{,}800=-1{,}600⟩'], ['Meaning:', 'below the line']], '−$1,600: priced below the model'),
 E('Truncated axis', 'Compare what the bars show with the real difference.', 'Ratings 52 and 58; axis starts at 50.', [['Looks:', '⟨(58-50)\\div(52-50)=4⟩ times as tall'], ['Actually:', '⟨(58-52)\\div52\\approx11.5\\%⟩ higher']], 'A modest gap looks huge'),
 L('Trust a model?', ['Is x inside the range of the data? (no extrapolation)', 'Do residuals look random, not curved?', 'Is the sample large and fair?', 'Do predictions make sense (no scores above 100)?']),
 M(['Sort before finding a median.', 'Residual = actual − predicted.'], [['Strong r means causation', 'look for a lurking variable.'], ['Negative r is weak', 'the sign is direction, |r| is strength.'], ['Predict far outside the data', 'extrapolation is risky.'], ['Bars may start anywhere', 'bar graphs should start at 0.']])
]),
probability: sheet('find probabilities, count outcomes and use complements', 'decide with expected value: games, warranties and lotteries', [
 V('Probability words', [['Probability', '0 to 1 (0% to 100%) chance.'], ['Complement', 'P(not A) = 1 − P(A).'], ['Independent', 'One does not affect the other.'], ['Experimental', 'From trials: frequency ÷ trials.']]),
 E('Basic probability', '⟨P(A)=\\dfrac{\\text{favorable}}{\\text{total}}⟩ for equally likely outcomes.', '6 red, 9 blue, 5 green tickets; draw one.', [['Total:', '20'], ['Green:', '⟨5\\div20=0.25⟩']], '25%'),
 E('Experimental estimate', 'Use the sample rate to predict.', '12 defective of 400 tested; shipment of 5,000.', [['Rate:', '⟨12\\div400=0.03⟩'], ['Expect:', '⟨0.03(5{,}000)=150⟩']], 'About 150 defective'),
 H('“And” and “or”', 'Independent “and”: ⟨P(A\\text{ and }B)=P(A)P(B)⟩<br>“Or”: ⟨P(A\\text{ or }B)=P(A)+P(B)-P(A\\text{ and }B)⟩<div class="ex">Bus late 30%, train late 10%: both ⟨0.3(0.1)=0.03⟩.</div>'),
 T('Counting', ['Situation', 'Count'], [['4 shirts, 3 pants, 2 shoes', '⟨4\\cdot3\\cdot2=24⟩ outfits'], ['3-digit lock, 0–9', '⟨10^3=1{,}000⟩ codes'], ['2 of 8 toppings', '⟨\\tbinom82=28⟩ pizzas']], 'Multiply choices; for “order does not matter,” use combinations.'),
 E('Two-way table', 'For “given B,” use only the B row or column.', '80 seniors, 24 have jobs.', [['P(job | senior):', '⟨24\\div80=0.30⟩']], '30%')
], [
 H('Expected value', '⟨E=\\sum(\\text{outcome})(\\text{probability})⟩ — include the cost as a negative.<div class="ex">$2 to play; win $10 on a 6:<br>⟨\\tfrac16(10)-2\\approx-0.33⟩ per play.</div>A long-run average, not a guarantee.'),
 E('Fair price', 'Fair price = expected winnings (EV = 0).', 'Win $24 if a 10-section spinner lands on 1 of 2 sections.', [['Expected winnings:', '⟨\\tfrac{2}{10}(24)=4.80⟩']], 'A fair price is $4.80'),
 E('Extended warranty', 'EV = P(repair) × repair cost − price.', '$129 plan; 10% chance of a $450 repair.', [['Expected repair:', '⟨0.10(450)=45⟩'], ['EV:', '⟨45-129=-84⟩']], '−$84: costs more than it saves on average'),
 E('Lottery ticket', 'Add prize ÷ odds for each prize, then subtract the price.', '$2 ticket; $1,000 at 1 in 2,500; $4 at 1 in 20.', [['Prizes:', '⟨0.40+0.20=0.60⟩'], ['EV:', '⟨0.60-2=-1.40⟩']], '−$1.40 per ticket'),
 L('Beyond expected value', ['Can I afford the worst case?', 'Do I need the money for sure (rent, tuition)?', 'Is a single play likely to match the average?', 'Independent events have no memory: no “due” wins.']),
 M(['EV is a long-run average.', 'Count each outcome once.'], [['A losing streak means a win is due', 'the gambler’s fallacy.'], ['Add probabilities for “and”', 'multiply for independent events.'], ['Positive EV = sure profit', 'single plays can still lose.'], ['More tickets = better odds of profit', 'more tickets = bigger expected loss.']])
])
};
