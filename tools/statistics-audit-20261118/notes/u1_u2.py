# Teaching notes, Statistics units 1–2 (Exploring Data; Sampling and Experimentation).
# Each record: obj, idea, voc [[word, meaning]…], watch, cards [{h, big, steps}]. Math in ⟨TeX⟩; {{…}} = blank on guided notes.
ED = 'exploring-data'
SE = 'sampling-experimentation'
R = {}

R[ED, 1] = dict(obj='classify variables and display one quantitative variable with a dot plot, stem plot or histogram',
  idea='First decide what kind of variable you have; the type decides the display. Quantitative data go on a number scale (dot plot, stem plot, histogram); categorical data go in bars.',
  voc=[['categorical variable', 'A variable that places individuals into groups, such as favorite sport.'], ['quantitative variable', 'A variable with numerical values for which an average makes sense.'],
       ['discrete / continuous', 'Discrete values can be counted (number of siblings); continuous values can be any value in an interval (height).']],
  watch='Treating number labels such as zip codes or jersey numbers as quantitative; an average of them means nothing.',
  cards=[dict(h='Pick the display', big='Ask: does an average make sense? If yes, the variable is {{quantitative}} and needs a number scale.',
    steps=['Minutes of homework: quantitative, {{continuous}}; use a dot plot or histogram.', 'Number of pets: quantitative, {{discrete}}.', 'Favorite subject: {{categorical}}; use a bar graph.']),
    dict(h='Stem plot', big='Split each value into a stem (all but the last digit) and a leaf (the last digit). Keep empty stems and add a key.',
    steps=['Values 52, 57, 61, 63, 63, 78: stems 5, 6, 7.', 'Row for 6: 6 | {{133}}.', 'Key: 5 | 2 = {{52}}.'])])

R[ED, 2] = dict(obj='describe a distribution by its shape, center, spread and unusual features, in context',
  idea='Every description has four parts (SOCS): Shape, Outliers, Center and Spread, always with the variable’s name and units.',
  voc=[['skewed right', 'A long tail toward the high values; the mean is pulled above the median.'], ['outlier', 'A value that falls well outside the overall pattern.'],
       ['resistant', 'Not strongly affected by extreme values, like the median and IQR.']],
  watch='Describing the shape of the graph (“it goes up then down”) instead of the distribution, or leaving out context and units.',
  cards=[dict(h='SOCS in one paragraph', big='Shape, Outliers, Center, Spread — and say what the numbers {{measure}}.',
    steps=['Shape: “skewed {{right}}” (tail toward large values).', 'Center: use the {{median}} when the shape is skewed.', 'Spread: report the {{IQR}} with the median.'])])

R[ED, 3] = dict(obj='calculate and interpret the mean, median, range, IQR and standard deviation',
  idea='Center tells a typical value; spread tells how much values vary. The mean and standard deviation use every value; the median and IQR use only the middle of the ordered data.',
  voc=[['mean', 'The sum of the values divided by n.'], ['standard deviation', 'The typical distance of the values from the mean.'], ['interquartile range (IQR)', 'Q3 − Q1, the spread of the middle half.']],
  watch='Dividing by n instead of n − 1 for the sample standard deviation.',
  cards=[dict(h='Sample standard deviation', big='⟨s = \\sqrt{\\dfrac{\\sum (x - \\bar{x})^2}{n - 1}}⟩: find deviations, square, add, divide by {{n − 1}}, take the root.',
    steps=['Data 2, 4, 6: ⟨\\bar{x} = {{4}}⟩.', 'Squared deviations 4, 0, 4 add to {{8}}.', '⟨s = \\sqrt{8/2} = {{2}}⟩.'])])

R[ED, 4] = dict(obj='find quartiles and percentiles, draw box plots and compare distributions',
  idea='The five-number summary splits ordered data into quarters; a box plot pictures it and makes comparisons of center and spread quick.',
  voc=[['five-number summary', 'Minimum, Q1, median, Q3, maximum.'], ['percentile', 'The percent of values at or below a given value.'], ['1.5 × IQR rule', 'Values below Q1 − 1.5·IQR or above Q3 + 1.5·IQR are outliers.']],
  watch='Comparing distributions with numbers only — the comparison needs words like “higher” or “more variable” and context.',
  cards=[dict(h='Outlier fences', big='Lower fence = Q1 − 1.5·IQR; upper fence = Q3 + {{1.5·IQR}}.',
    steps=['Q1 = 20, Q3 = 30, so IQR = {{10}}.', 'Fences: 20 − 15 = {{5}} and 30 + 15 = {{45}}.', 'A value of 48 is an {{outlier}}.'])])

R[ED, 5] = dict(obj='use z-scores and Normal models to find proportions, percentiles and values',
  idea='A z-score says how many standard deviations a value is from the mean. Normal areas come from z: sketch the curve, shade the region, then use Table A or technology.',
  voc=[['z-score', 'z = (x − μ)/σ.'], ['Normal distribution', 'A symmetric, bell-shaped density curve described by μ and σ.'], ['empirical rule', 'About 68%, 95% and 99.7% of values lie within 1, 2 and 3 SDs of the mean.']],
  watch='Using the Table A area (to the left) when the question asks for the area to the right.',
  cards=[dict(h='From value to area', big='Standardize, then find the area: ⟨z = \\dfrac{x - \\mu}{\\sigma}⟩.',
    steps=['Heights ~ N(64, 2.5); P(X > 69): ⟨z = {{2}}⟩.', 'Table A gives 0.9772 to the left, so the right tail is {{0.0228}}.', 'About {{2.3%}} of heights are above 69 in.']),
    dict(h='From area to value', big='For a percentile, find z with that area to its left, then ⟨x = \\mu + z\\sigma⟩.',
    steps=['90th percentile: z ≈ {{1.28}}.', 'x = 64 + 1.28(2.5) = {{67.2}} in.'])])

R[ED, 6] = dict(obj='summarize two categorical variables with two-way tables, marginal and conditional distributions',
  idea='Compare groups with conditional percents (row or column percents), never with raw counts when group sizes differ.',
  voc=[['marginal distribution', 'The distribution of one variable alone, from the table’s totals.'], ['conditional distribution', 'The distribution of one variable within one group of the other.'],
       ['association', 'Knowing one variable changes the likely values of the other.']],
  watch='Dividing by the grand total when the question conditions on a group.',
  cards=[dict(h='Conditional percents', big='“Of the juniors, what percent…?” — divide by the {{juniors’ total}}.',
    steps=['Juniors: 30 bus, 70 car (total 100); bus = {{30%}}.', 'Seniors: 20 bus, 80 car; bus = {{20%}}.', 'The percents differ, so grade and transportation are {{associated}}.'])])

R[ED, 7] = dict(obj='describe a scatterplot and interpret the correlation r',
  idea='Describe direction, form, strength and unusual points. r measures only the strength and direction of a linear relationship and has no units.',
  voc=[['correlation r', 'A number from −1 to 1 measuring linear strength and direction.'], ['explanatory / response variable', 'x may help explain or predict y.'], ['form', 'Linear or curved.']],
  watch='Saying r = 0 means “no relationship” (a strong curve can have r near 0) or that a high r proves causation.',
  cards=[dict(h='Reading r', big='The sign gives {{direction}}; the size |r| gives strength.',
    steps=['r = −0.85: strong, {{negative}}, linear.', 'r = 0.15: {{weak}} linear association.', 'Converting inches to centimeters leaves r {{unchanged}}.'])])

R[ED, 8] = dict(obj='find and interpret the least-squares regression line, predictions and r²',
  idea='The LSRL makes the sum of squared residuals as small as possible; it passes through (x̄, ȳ) and has slope b = r·s_y/s_x.',
  voc=[['slope b', 'The predicted change in y for each 1-unit increase in x.'], ['coefficient of determination r²', 'The fraction of the variation in y explained by the linear model.'],
       ['extrapolation', 'Predicting outside the range of the x-data — unreliable.']],
  watch='Interpreting the slope as an actual change (“y increases by…”) instead of a predicted change.',
  cards=[dict(h='Building the line', big='⟨b = r\\dfrac{s_y}{s_x}⟩ and ⟨a = \\bar{y} - b\\bar{x}⟩.',
    steps=['r = 0.8, s_y = 10, s_x = 2: ⟨b = {{4}}⟩.', 'x̄ = 5, ȳ = 24: ⟨a = 24 - 20 = {{4}}⟩.', '⟨\\hat{y} = 4 + 4x⟩; r² = {{0.64}}: 64% of the variation in y is explained.'])])

R[ED, 9] = dict(obj='calculate and interpret residuals, read residual plots and recognize influential points',
  idea='A residual is actual − predicted. A residual plot with random scatter means a line fits; a curve in the residuals means it does not.',
  voc=[['residual', 'y − ŷ, the vertical distance from the point to the line.'], ['residual plot', 'Residuals graphed against x (or ŷ).'], ['influential point', 'A point whose removal changes the line a lot, often far out in x.']],
  watch='Computing predicted − actual and getting the sign of the residual backwards.',
  cards=[dict(h='Residuals', big='residual = {{actual − predicted}}; positive means the point is above the line.',
    steps=['⟨\\hat{y} = 10 + 2x⟩ at (3, 19): ⟨\\hat{y} = {{16}}⟩.', 'Residual = 19 − 16 = {{3}}.', 'The actual value is 3 {{above}} the prediction.'])])

R[SE, 1] = dict(obj='identify the population, sample, parameter and statistic, and tell a census from a sample survey',
  idea='A parameter describes the whole population and is usually unknown; a statistic describes the sample and is used to estimate it.',
  voc=[['population', 'The entire group we want information about.'], ['sample', 'The part of the population we collect data from.'], ['census', 'Data from every individual in the population.']],
  watch='Calling a sample percent a parameter because the sample was random.',
  cards=[dict(h='Parameter or statistic?', big='Population → {{parameter}} (p, μ); sample → statistic (p̂, x̄).',
    steps=['“41% of the 120 students surveyed” is a {{statistic}}.', '“The proportion of all 1,800 students” is a {{parameter}}.'])])

R[SE, 2] = dict(obj='describe and choose among simple random, stratified, cluster and systematic sampling',
  idea='Random selection avoids bias. Stratify when groups differ in the response (more precision); cluster when it is cheaper to sample whole groups.',
  voc=[['simple random sample (SRS)', 'Every group of n individuals has the same chance to be chosen.'], ['stratified random sample', 'An SRS within each similar group (stratum).'],
       ['cluster sample', 'Randomly choose whole groups (clusters) and use everyone in them.']],
  watch='Mixing up strata and clusters: strata are similar inside and different from each other; clusters each look like the whole population.',
  cards=[dict(h='Describing an SRS', big='Label → randomize → select without repeats → {{measure}}.',
    steps=['Label the 1,200 students 1–1,200.', 'Use a random number generator for {{60}} different labels.', 'Survey the chosen students.']),
    dict(h='Proportional allocation', big='Each stratum gets n × (stratum size ÷ population size).',
    steps=['600 of 2,000 students are freshmen; n = 100.', 'Freshmen in the sample: 100 × 600/2,000 = {{30}}.'])])

R[SE, 3] = dict(obj='identify undercoverage, nonresponse and response bias and the direction each pushes an estimate',
  idea='Bias is a systematic error: who is in the frame (undercoverage), who answers (nonresponse) or how they answer (response bias). A bigger sample does not fix it.',
  voc=[['undercoverage', 'Some members of the population cannot be chosen.'], ['nonresponse', 'Chosen individuals do not respond.'], ['response bias', 'Answers are systematically untrue, for example because of wording.']],
  watch='Claiming a larger sample removes bias — it only reduces variability.',
  cards=[dict(h='Name it and give a direction', big='Say {{which}} bias, why, and whether the estimate is likely too high or too low.',
    steps=['Landline-only phone survey about streaming: {{undercoverage}}, likely too low.', 'Leading question praising a park: response bias, likely too {{high}}.'])])

R[SE, 4] = dict(obj='distinguish observational studies from experiments and explain what each can conclude',
  idea='Only an experiment imposes treatments, and only random assignment lets us conclude cause and effect.',
  voc=[['observational study', 'Researchers observe and measure without assigning treatments.'], ['experiment', 'Researchers deliberately assign treatments.'], ['confounding', 'Two variables’ effects on the response cannot be separated.']],
  watch='Concluding causation from an observational study because the association is strong.',
  cards=[dict(h='Which kind of study?', big='Did the researchers {{assign}} the treatment? Then it is an experiment.',
    steps=['Survey of coffee drinkers’ blood pressure: {{observational study}}.', 'Randomly assigned study methods: {{experiment}}.'])])

R[SE, 5] = dict(obj='identify experimental units, factors, treatments and response, and explain random assignment and replication',
  idea='A well-designed experiment compares treatments, randomly assigns them, controls other variables and replicates on enough units.',
  voc=[['treatment', 'A specific condition applied to the units (a combination of factor levels).'], ['replication', 'Using enough units in each treatment so chance variation averages out.'],
       ['control group', 'A group that gets a placebo or the current treatment for comparison.']],
  watch='Counting factors instead of treatments: 2 brands × 3 temperatures is 6 treatments, not 2 or 3.',
  cards=[dict(h='Treatments', big='Number of treatments = product of the numbers of {{levels}}.',
    steps=['3 fertilizers × 4 watering levels = {{12}} treatments.', 'With 5 plants each: {{60}} plants.'])])

R[SE, 6] = dict(obj='explain confounding, the placebo effect and single- and double-blind designs',
  idea='A placebo group and blinding make the groups differ only in the treatment, so a difference in the response can be blamed on the treatment.',
  voc=[['placebo', 'A fake treatment that looks like the real one.'], ['double-blind', 'Neither the subjects nor the people measuring the response know who got which treatment.'],
       ['placebo effect', 'Improvement because people believe they are treated.']],
  watch='Saying an experiment is double-blind when only the subjects are unaware.',
  cards=[dict(h='Blinding', big='Single-blind: one group unaware. Double-blind: {{both}} subjects and evaluators unaware.',
    steps=['Patients and the nurses who rate pain do not know: {{double-blind}}.', 'Only the runners do not know: {{single-blind}}.'])])

R[SE, 7] = dict(obj='describe completely randomized, randomized block and matched pairs designs and choose among them',
  idea='Block when a variable affects the response, so treatments are compared within similar units; matched pairs is blocking with blocks of size two.',
  voc=[['completely randomized design', 'All units are randomly assigned to treatments in one step.'], ['randomized block design', 'Units are grouped by a variable, then randomized within each block.'],
       ['matched pairs', 'Pairs of similar units (or each unit twice, in random order) compare two treatments.']],
  watch='Blocking on a variable after assigning treatments, or forgetting to randomize within blocks.',
  cards=[dict(h='Why block?', big='Blocking removes variation due to the blocking variable, so treatment differences are easier to {{detect}}.',
    steps=['Runners differ in fitness: give each runner both shoes in random order — {{matched pairs}}.', 'Soil differs by field: block by {{soil type}}, then randomize.'])])

R[SE, 8] = dict(obj='decide what a study allows: generalizing to a population and/or concluding cause and effect',
  idea='Random selection allows generalizing to the population sampled; random assignment allows cause and effect. A study can have one, both or neither.',
  voc=[['scope of inference', 'The population and the kind of conclusion a study supports.'], ['random selection', 'Choosing the sample at random from the population.'], ['random assignment', 'Assigning treatments at random.']],
  watch='Generalizing results from volunteers to everyone because the treatments were randomly assigned.',
  cards=[dict(h='The 2 × 2 table', big='Selection → {{generalize}}; assignment → cause and effect.',
    steps=['Volunteers, random assignment: cause and effect, but only for {{subjects like these}}.', 'Random sample, no assignment: an {{association}} for the population.'])])
