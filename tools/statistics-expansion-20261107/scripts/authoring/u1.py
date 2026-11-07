from common import *
import plots as P

U = "exploring-data"
IA, IB, IC, ID, IE, IIIC = "APSTATS.I.A", "APSTATS.I.B", "APSTATS.I.C", "APSTATS.I.D", "APSTATS.I.E", "APSTATS.III.C"


def stem_text(data, key_note):
    """Stemplot as text lines: stems are tens."""
    stems = {}
    for v in sorted(data):
        stems.setdefault(v // 10, []).append(v % 10)
    lo, hi = min(stems), max(stems)
    lines = [f"{s} | {' '.join(str(l) for l in stems.get(s, []))}".rstrip() for s in range(lo, hi + 1)]
    return "\n".join(lines) + f"\nKey: {key_note}"


def s01():
    k = 1
    # ---- CP2 ----
    MC(U, k, "cp2", "A survey records each student's number of siblings. What type of variable is this?",
       "Quantitative and discrete", ["Quantitative and continuous", "Categorical", "Categorical and ordinal only"],
       ["Number of siblings is a count (0, 1, 2, …), so it is quantitative.", "Counts take separate whole-number values, so the variable is discrete."],
       family="u1_vartype", std=[IA])
    MC(U, k, "cp2", "A nurse records each patient's blood type (A, B, AB, or O). What type of variable is this?",
       "Categorical", ["Quantitative and discrete", "Quantitative and continuous", "Neither; it is an individual"],
       ["Blood type places each patient into a group; arithmetic on the labels makes no sense, so it is categorical."],
       family="u1_vartype", std=[IA])
    SEL(U, k, "cp2", "A school collects these variables about each student. Select ALL that are quantitative.",
        ["Height in centimeters", "Minutes spent on homework last night", "Number of AP classes taken"],
        ["Homeroom number", "Favorite subject", "Zip code"],
        ["Quantitative variables are numerical measurements or counts where averages make sense.",
         "Height, minutes, and number of AP classes are quantitative.",
         "Homeroom number and zip code are labels (categorical) even though they use digits; favorite subject is categorical."],
        family="u1_vartype_sel", std=[IA])
    d = [2, 3, 3, 4, 4, 4, 5, 5, 6, 8]
    src = P.dotplot("u1_dot_pets", d, "Number of books read over summer break", "Books read by 10 students")
    SA(U, k, "cp2", "The dotplot shows the number of books read over summer break by 10 students (each dot is one student). How many students read at least 5 books?",
       "4", ["Count the dots at 5 and above: 5 has 2 dots, 6 has 1, 8 has 1.", "2 + 1 + 1 = 4 students."],
       family="u1_dotplot_read", std=[IA], check={"kind": "count_ge", "data": d, "c": 5},
       diagram=P.image(src, "Dotplot of books read by 10 students. Values: 2 (1 dot), 3 (2 dots), 4 (3 dots), 5 (2 dots), 6 (1 dot), 8 (1 dot)."))
    st1 = [12, 15, 18, 21, 23, 23, 27, 29, 30, 34, 36, 41, 45]
    SA(U, k, "cp2", "A stemplot shows the ages of 13 people at a community 5K run.\n" + stem_text(st1, "2 | 3 = 23 years") +
       "\nHow many runners are in their 20s (20–29 years old)?", "5",
       ["The 20s are the stem 2 row: leaves 1, 3, 3, 7, 9.", "That row has 5 leaves, so 5 runners."],
       family="u1_stem_read", std=[IA], check={"kind": "count_between", "data": st1, "lo": 20, "hi": 29, "no_print_check": "data printed as a stemplot"})
    MC(U, k, "cp2", "Which graph is NOT appropriate for displaying the heights of 25 students?",
       "Pie chart", ["Dotplot", "Histogram", "Stemplot"],
       ["Height is quantitative. Dotplots, stemplots, and histograms display quantitative data.",
        "Pie charts show parts of a whole for categories, so they are not appropriate here."],
       family="u1_choose_display", std=[IA])
    # ---- CP1 ----
    st2 = [41, 43, 47, 52, 52, 55, 58, 61, 63, 64, 66, 70, 72, 79, 85]
    SA(U, k, "cp1", "Test scores for 15 students are shown in a stemplot.\n" + stem_text(st2, "5 | 2 = 52 points") +
       "\nFind the median score.", "61",
       ["n = 15, so the median is the 8th value in order.", "Counting leaves: 41, 43, 47, 52, 52, 55, 58, 61 → the 8th value is 61."],
       family="u1_stem_median", std=[IA, IB], check={"kind": "median", "data": st2, "no_print_check": "data printed as a stemplot"})
    edges = [0, 10, 20, 30, 40, 50, 60]
    counts = [3, 7, 9, 5, 4, 2]
    src = P.histogram("u1_hist_commute", edges, counts, "Commute time (minutes)", "Commute times of 30 workers")
    SA(U, k, "cp1", "The histogram shows the commute times of 30 workers. Each bar includes its left endpoint but not its right endpoint (for example, 10 to under 20). What percent of the workers commute 30 minutes or more? Round to the nearest tenth of a percent.",
       "36.7%", ["Bars at 30–40, 40–50, 50–60 have 5 + 4 + 2 = 11 workers.", "11/30 ≈ 0.3667, about 36.7%."],
       family="u1_hist_percent", std=[IA], check={"kind": "hist_pct_ge", "edges": edges, "counts": counts, "c": 30},
       diagram=P.image(src, "Histogram of commute times for 30 workers with bars 0–10: 3, 10–20: 7, 20–30: 9, 30–40: 5, 40–50: 4, 50–60: 2."))
    MC(U, k, "cp1", "Using the same commute-time frequencies (0–10: 3, 10–20: 7, 20–30: 9, 30–40: 5, 40–50: 4, 50–60: 2 workers; 30 workers total), which interval contains the median commute time?",
       "20 to under 30 minutes", ["10 to under 20 minutes", "30 to under 40 minutes", "0 to under 10 minutes"],
       ["The median is between the 15th and 16th ordered values.", "Cumulative counts: 3, 10, 19 → the 15th and 16th values fall in the 20–30 bar."],
       family="u1_hist_median_bin", std=[IA, IB], check={"kind": "hist_median_bin", "edges": edges, "counts": counts, "key_lo": 20})
    MC(U, k, "cp1", "A back-to-back stemplot shows resting pulse rates for athletes (left leaves) and non-athletes (right leaves), with stems in tens (key: 6 | 2 means 62 bpm on the right; 2 | 6 means 62 bpm on the left).\n"
       "Athletes | Stem | Non-athletes\n      8 7 | 4 |\n  9 6 5 2 | 5 | 8\n    4 3 1 | 6 | 2 4 6 9\n        0 | 7 | 0 3 5 8\n          | 8 | 1 4\nWhich statement is supported by the plot?",
       "Athletes tend to have lower pulse rates than non-athletes.",
       ["The two groups have the same center.", "Non-athletes' pulse rates are less variable than athletes' because they have more leaves.", "Athletes have a higher median pulse rate."],
       ["Athletes: 47, 48, 52, 55, 56, 59, 61, 63, 64, 70 (median 57.5).",
        "Non-athletes: 58, 62, 64, 66, 69, 70, 73, 75, 78, 81, 84 (median 70).",
        "The athletes' distribution is shifted lower, so they tend to have lower pulse rates."],
       family="u1_backtoback", std=[IA, IC])
    SEL(U, k, "cp1", "Select ALL statements that are true about histograms and bar graphs.",
        ["Histogram bars touch because the intervals of a quantitative variable are adjacent.",
         "The order of bars in a bar graph of categories can be rearranged without losing information.",
         "Changing the bin width of a histogram can change the apparent shape of the distribution."],
        ["A bar graph can display the distribution of a quantitative variable like height directly.",
         "Histogram bars should have gaps between them to show categories.",
         "A histogram shows each individual data value exactly."],
        ["Histograms summarize quantitative data in numeric intervals; adjacent intervals make bars touch, and bin width affects appearance.",
         "Bar graphs show categories; their order is arbitrary. Histograms do not show individual values."],
        family="u1_hist_vs_bar_sel", std=[IA])
    MC(U, k, "cp1", "A cumulative relative frequency table of 50 quiz scores lists: score ≤ 6: 0.10; ≤ 7: 0.26; ≤ 8: 0.58; ≤ 9: 0.84; ≤ 10: 1.00. How many students scored exactly 8?",
       "16", ["29", "32", "13"],
       ["Proportion scoring exactly 8 = 0.58 − 0.26 = 0.32.", "0.32 × 50 = 16 students."],
       family="u1_cumrel_count", std=[IA], check={"kind": "cum_diff_count", "hi": 0.58, "lo": 0.26, "n": 50})
    # ---- Honors ----
    MC(U, k, "honors", "A histogram of 200 home prices uses $100,000-wide bins and looks unimodal and right-skewed. A second histogram of the same data uses $10,000-wide bins and shows two distinct peaks. What is the best conclusion?",
       "Wide bins can hide features such as a second cluster; the data may be bimodal, so the finer histogram should be examined.",
       ["The second histogram must be wrong because the data did not change.", "The data are definitely unimodal; narrow bins always create false peaks.", "Bin width affects only the y-axis scale, not the shape."],
       ["Bin width changes how observations are grouped.", "Very wide bins can merge clusters; checking several reasonable widths reveals real features."],
       family="u1_binwidth", std=[IA])
    edges2 = [50, 60, 70, 80, 90, 100]
    counts2 = [4, 6, 12, 10, 8]
    src = P.histogram("u1_hist_scores40", edges2, counts2, "Final exam score", "Final exam scores of 40 students")
    SA(U, k, "honors", "The histogram shows final exam scores for 40 students (each bar includes its left endpoint but not its right endpoint). In which interval does the 30th score in increasing order lie, and what does that tell you about the 75th percentile?",
       "80 to under 90; about 75% of scores are below a value in the 80s",
       ["Cumulative counts: 50–60: 4, 60–70: 10, 70–80: 22, 80–90: 32, 90–100: 40.",
        "The 23rd through 32nd scores are in the 80–90 bar, so the 30th score is in 80 to under 90.",
        "30/40 = 75%, so the 75th percentile (about Q3) is somewhere in the 80s; the histogram cannot give its exact value."],
       family="u1_hist_percentile_bin", std=[IA, IB], check={"kind": "hist_rank_bin", "edges": edges2, "counts": counts2, "rank": 30, "key_lo": 80},
       diagram=P.image(src, "Histogram of 40 final exam scores: 50–60: 4, 60–70: 6, 70–80: 12, 80–90: 10, 90–100: 8."))
    MC(U, k, "honors", "Which variable is categorical even though its values are numbers?",
       "Area code of each student's phone number", ["Number of text messages sent per day", "Age in months", "Battery percentage remaining on each phone"],
       ["Area codes are labels identifying regions; averaging them is meaningless.", "The other variables are measurements or counts."],
       family="u1_vartype_numeric_label", std=[IA])
    st3 = [58, 61, 63, 64, 66, 66, 67, 69, 70, 71, 72, 72, 73, 75, 78, 84]
    MC(U, k, "honors", "Heights (inches) of 16 adults are shown in a split stemplot (each stem is split into leaves 0–4 and 5–9).\n5 | 8\n6 | 1 3 4\n6 | 6 6 7 9\n7 | 0 1 2 2 3\n7 | 5 8\n8 | 4\nKey: 7 | 2 = 72 inches.\nWhy might a statistician split the stems for these data?",
       "With only three unsplit stems, the plot would be too compressed to show the shape; splitting spreads the data over more rows.",
       ["Splitting stems removes outliers from the display.", "Splitting stems changes the median of the data.", "Stems must always be split when n is greater than 10."],
       ["Unsplit stems 5, 6, 7, 8 would put most values into two rows.", "Split stems create more rows, so the shape (center, spread, skew) is easier to see. Splitting does not change any data values."],
       family="u1_split_stems", std=[IA])
    OR(U, k, "honors", "A teacher recorded the number of minutes 20 students spent on a practice test:\n22, 25, 27, 28, 30, 31, 31, 33, 34, 35, 36, 36, 38, 40, 41, 43, 45, 52, 58, 71",
       [("Make a stemplot with stems in tens. Include a key.", "2 | 2 5 7 8; 3 | 0 1 1 3 4 5 6 6 8; 4 | 0 1 3 5; 5 | 2 8; 6 | ; 7 | 1; key 3 | 1 = 31 minutes"),
        ("Make a frequency table using intervals 20–29, 30–39, 40–49, 50–59, 60–69, 70–79.", "4, 9, 4, 2, 0, 1"),
        ("Describe the shape of the distribution and identify any gap or possible outlier.", "Skewed right (single peak in the 30s); gap from 59 to 70; 71 is a possible outlier"),
        ("Which display shows the exact time for each student, the stemplot or the histogram? Explain.", "The stemplot, because each leaf records an individual value; a histogram shows only counts per interval")],
       ["1 point: correct stemplot with key.", "1 point: correct frequencies summing to 20.",
        "1 point: right skew with the gap/possible outlier at 71 identified.", "1 point: stemplot chosen with a correct reason."],
       family="u1_stem_or", std=[IA], check={"kind": "freq", "data": [22, 25, 27, 28, 30, 31, 31, 33, 34, 35, 36, 36, 38, 40, 41, 43, 45, 52, 58, 71],
                                              "edges": [20, 30, 40, 50, 60, 70, 80], "expect": [4, 9, 4, 2, 0, 1]})
    MC(U, k, "honors", "A dotplot of the number of siblings for 30 students has a tall stack at 0 and 1, fewer dots at 2 and 3, and one dot at 7. Which description is most complete?",
       "The distribution is unimodal and skewed right, centered around 1 sibling, ranging from 0 to 7, with a possible outlier at 7.",
       ["The distribution is symmetric with mean 7.", "The distribution is skewed left because most values are small.", "The distribution is bimodal with peaks at 0 and 7."],
       ["A complete description addresses shape, center, spread, and unusual features in context.", "Most values are low with a long tail to the right, so it is skewed right; 7 stands apart."],
       family="u1_describe_dotplot", std=[IA])
    SEL(U, k, "honors", "Select ALL situations in which a stemplot would be a poor choice of display.",
        ["Incomes of 5,000 households", "Comparing the favorite colors of students in two schools"],
        ["Test scores of 20 students", "Comparing heights of two small classes with a back-to-back stemplot"],
        ["Stemplots work for small to moderate quantitative data sets.", "With 5,000 values a stemplot is unwieldy (use a histogram); favorite color is categorical."],
        family="u1_stem_suit_sel", std=[IA])


def s02():
    k = 2
    MC(U, k, "cp2", "A distribution has a long tail stretching toward larger values. How is its shape described?",
       "Skewed right", ["Skewed left", "Symmetric", "Uniform"],
       ["Skew is named for the direction of the long tail.", "A tail toward larger values is a right skew."], family="u1_shape_tail", std=[IA])
    d = [3, 4, 4, 5, 5, 5, 6, 6, 7, 15]
    src = P.dotplot("u1_dot_shoes", d, "Number of pairs of shoes owned", "Pairs of shoes owned by 10 students", xticks=range(2, 16))
    MC(U, k, "cp2", "The dotplot shows the number of pairs of shoes owned by 10 students. Which value appears to be an outlier?",
       "15", ["3", "5", "7"],
       ["Most values are between 3 and 7.", "15 is far from the rest of the data, so it appears to be an outlier."],
       family="u1_dot_outlier", std=[IA], check={"kind": "outliers", "data": d, "expect": [15]},
       diagram=P.image(src, "Dotplot of pairs of shoes for 10 students: 3 (1), 4 (2), 5 (3), 6 (2), 7 (1), 15 (1)."))
    for data, ctx, key in [([10, 12, 13, 13, 14, 15, 16, 30], "Scores on a 30-point quiz for 8 students", "30"),
                           ([2, 41, 44, 45, 47, 48, 50, 51, 53], "Number of pages read by 9 students", "2")]:
        q1, q3 = quartiles(data)
        i = q3 - q1
        lo, hi = q1 - 1.5 * i, q3 + 1.5 * i
        SA(U, k, "cp2", f"{ctx}: {lst(data)}. Q1 = {fmt(q1)} and Q3 = {fmt(q3)}. Use the 1.5 × IQR rule to find the lower and upper fences, then name any outlier.",
           f"Fences {fmt(lo)} and {fmt(hi)}; outlier: {key}",
           [f"IQR = {fmt(q3)} − {fmt(q1)} = {fmt(i)}.", f"Lower fence = {fmt(q1)} − 1.5({fmt(i)}) = {fmt(lo)}.",
            f"Upper fence = {fmt(q3)} + 1.5({fmt(i)}) = {fmt(hi)}.", f"Only {key} lies outside the fences."],
           family="u1_fences_given_q", std=[IA, IB], check={"kind": "fences_outliers", "data": data, "expect_out": [float(key)]})
    MC(U, k, "cp2", "The heights of players on a basketball team are mostly between 72 and 80 inches, with the values piling up in the middle and tapering off equally on both sides. What is the shape?",
       "Roughly symmetric", ["Skewed right", "Skewed left", "Bimodal"],
       ["Equal tapering on both sides of the center describes a roughly symmetric distribution."], family="u1_shape_words", std=[IA])
    MC(U, k, "cp2", "A data set of daily rainfall amounts has many days with 0 inches and a few days with large amounts. Which measure of center is better to report?",
       "The median, because the distribution is skewed right", ["The mean, because it uses every value", "The mode, because it is always largest", "The range, because it shows the spread"],
       ["Many zeros and a few big values make the data strongly skewed right.", "The median is resistant to the extreme values, so it better describes a typical day."],
       family="u1_center_choice", std=[IA, IB])
    SEL(U, k, "cp2", "Select ALL features that should be included when describing the distribution of a quantitative variable.",
        ["Shape", "Center", "Spread", "Outliers or other unusual features"], ["The order in which data were collected", "The name of the person who collected the data"],
        ["Describe shape, center, spread, and unusual features (outliers, gaps, clusters), in context."], family="u1_socs_sel", std=[IA])
    MC(U, k, "cp2", "A distribution of exam scores has most students scoring between 85 and 100, with a few students scoring between 40 and 60. What is the shape?",
       "Skewed left", ["Skewed right", "Symmetric", "Uniform"],
       ["The long tail stretches toward the low scores (the left).", "A left tail means the distribution is skewed left."], family="u1_shape_words", std=[IA])
    MC(U, k, "cp2", "Which statement about outliers is correct?",
       "An outlier should be investigated; it may be a recording error or a real unusual value.",
       ["Outliers should always be deleted.", "Every data set has at least one outlier.", "An outlier is any value above the mean."],
       ["Outliers are values that fall outside the overall pattern.", "They are investigated, not automatically removed."], family="u1_outlier_concept", std=[IA])
    # CP1
    for data, ctx in [([51, 55, 58, 60, 61, 63, 64, 66, 67, 69, 70, 98], "Weights (kg) of 12 adults in a fitness class"),
                      ([4, 18, 20, 21, 22, 23, 23, 25, 26, 28, 31], "Daily high temperatures (°C) for 11 days")]:
        q1, q3 = quartiles(data)
        i = q3 - q1
        lo, hi = q1 - 1.5 * i, q3 + 1.5 * i
        outs = [v for v in data if v < lo or v > hi]
        SA(U, k, "cp1", f"{ctx}: {lst(data)}. Use the 1.5 × IQR rule (quartiles = medians of the lower and upper halves) to identify any outliers. Show the fences.",
           f"Q1 = {fmt(q1)}, Q3 = {fmt(q3)}, fences {fmt(lo)} and {fmt(hi)}; outlier(s): {lst(outs)}",
           [f"n = {len(data)}; Q1 = {fmt(q1)}, Q3 = {fmt(q3)}, IQR = {fmt(i)}.", f"Fences: {fmt(q1)} − {fmt(1.5 * i)} = {fmt(lo)} and {fmt(q3)} + {fmt(1.5 * i)} = {fmt(hi)}.",
            f"Values outside the fences: {lst(outs)}."],
           family="u1_outliers_full", std=[IA, IB], check={"kind": "fences_outliers", "data": data, "expect_out": outs})
    MC(U, k, "cp1", "The mean of a data set is 42 and the median is 35. What can you most likely conclude?",
       "The distribution is skewed right; a long upper tail pulls the mean above the median.",
       ["The distribution is skewed left.", "The distribution is symmetric.", "There are no outliers."],
       ["The mean is pulled toward the long tail.", "Mean much greater than median suggests right skew."], family="u1_mean_median_shape", std=[IA, IB])
    MC(U, k, "cp1", "A dotplot of the ages of people at a family reunion has one cluster from ages 3 to 14 and another cluster from ages 35 to 50, with almost no one in between. What is the best description of the shape?",
       "Bimodal, with two clusters (children and adults)", ["Unimodal and symmetric", "Skewed right with one peak", "Uniform"],
       ["Two separate peaks with a gap between them indicate a bimodal distribution.", "Context explains the clusters: children and their parents."],
       family="u1_bimodal", std=[IA])
    # Honors
    MC(U, k, "honors", "In a right-skewed data set with one high outlier, the outlier is corrected to a smaller value that is still the maximum. Which statement is true?",
       "The mean and standard deviation decrease, while the median and IQR do not change.",
       ["All four statistics decrease.", "Only the median changes.", "The mean decreases but the standard deviation increases."],
       ["The median and IQR depend only on the middle of the ordered data, which did not change.", "The mean and SD use every value, so lowering the maximum decreases both."],
       family="u1_resistance_change", std=[IA, IB])
    data = [12, 14, 15, 15, 16, 17, 18, 19, 20, 22, 23, 41]
    q1, q3 = quartiles(data)
    i = q3 - q1
    hi = q3 + 1.5 * i
    new_max = int(math.floor(hi))
    SA(U, k, "honors", f"Data: {lst(data)}. If the value 41 were replaced by a different number (still the largest value), what is the largest whole-number value it could be replaced with and NOT be an outlier by the 1.5 × IQR rule?",
       str(new_max),
       [f"Replacing the maximum does not change Q1 = {fmt(q1)} or Q3 = {fmt(q3)} (median-of-halves).", f"IQR = {fmt(i)}; upper fence = {fmt(q3)} + 1.5({fmt(i)}) = {fmt(hi)}.",
        f"A value is an outlier only if it is greater than {fmt(hi)}, so the largest whole number allowed is {new_max}.",
        "Check: the value must also stay the maximum, and 23 < " + str(new_max) + "."],
       family="u1_fence_reverse", std=[IA, IB], check={"kind": "upper_fence_floor", "data": data, "expect": new_max})
    OR(U, k, "honors", "Annual salaries (thousands of dollars) of the 11 employees at a small company: 32, 34, 35, 36, 38, 40, 41, 43, 45, 48, 150",
       [("Find the mean and the median salary. Round the mean to one decimal place.", "Mean ≈ 49.3; median = 40"),
        ("Use the 1.5 × IQR rule to determine whether 150 is an outlier.", "Q1 = 35, Q3 = 45, IQR = 10, upper fence = 60; 150 > 60, so it is an outlier"),
        ("Which measure of center better represents a typical employee? Explain.", "The median, because the distribution is skewed right by the 150 outlier, which pulls the mean up"),
        ("If the 150 value is removed, how do the mean and median change?", "Mean drops to 39.2; median drops only slightly to 39")],
       ["1 point: correct mean and median.", "1 point: fences computed and 150 identified as an outlier.",
        "1 point: median chosen with reference to skew/outlier.", "1 point: both new values with comparison (mean changes much more)."],
       family="u1_salary_or", std=[IA, IB], check={"kind": "salary_or", "data": [32, 34, 35, 36, 38, 40, 41, 43, 45, 48, 150]})
    MC(U, k, "honors", "Two data sets have the same median and the same IQR, but data set A has a much larger standard deviation. What is the most likely explanation?",
       "Data set A has more extreme values in its tails (or outliers), which affect the SD but not the median or IQR.",
       ["Data set A must have a larger mean.", "Data set A has more observations.", "The standard deviations must have been calculated incorrectly."],
       ["The median and IQR describe only the middle half.", "The SD is sensitive to how far the extreme values are from the mean."], family="u1_sd_vs_iqr", std=[IB])
    SEL(U, k, "honors", "A distribution of household sizes in a town has mean 2.8 and median 2. Select ALL statements that are reasonable.",
        ["The distribution is likely skewed right.", "Some households are much larger than typical.", "More than half of households have 2 or fewer people."],
        ["The distribution is likely skewed left.", "The mean is resistant to the large households."],
        ["Mean > median indicates a right tail of large households.", "Median 2 means at least half the households have 2 or fewer people — the third statement is true by the definition of the median.",
         "The mean is not resistant."], family="u1_mean_median_sel", std=[IA, IB])
    MC(U, k, "honors", "A data set has Q1 = 20, median = 24, Q3 = 40. Without more information, what does this summary suggest about the middle half of the data?",
       "It is skewed right: the upper quarter of the middle half (24 to 40) is spread out more than the lower quarter (20 to 24).",
       ["It is skewed left because Q1 is closest to the median.", "It is symmetric because the median is between Q1 and Q3.", "There must be an outlier above 40."],
       ["Distance from Q1 to median = 4; median to Q3 = 16.", "The longer upper section suggests right skew in the middle half."], family="u1_quartile_skew", std=[IA, IB])


def s03():
    k = 3
    sets = [("cp2", "Number of minutes 7 students spent reading last night", [20, 35, 15, 40, 25, 30, 45]),
            ("cp2", "Number of goals scored by a soccer team in 8 games", [0, 3, 1, 2, 2, 5, 1, 2])]
    for lv, ctx, d in sets:
        m = sum(d) / len(d)
        SA(U, k, lv, f"{ctx}: {lst(d)}. Find the mean and the range.", f"Mean = {fmt(m, 2)}; range = {fmt(max(d) - min(d))}",
           [f"Sum = {sum(d)}; mean = {sum(d)}/{len(d)} = {fmt(m, 2)}.", f"Range = max − min = {max(d)} − {min(d)} = {max(d) - min(d)}."],
           family="u1_mean_range", std=[IB], check={"kind": "mean_range", "data": d})
    d = [6, 8, 9, 11, 13, 14, 16, 19]
    num_mc(U, k, "cp2", f"Number of hours 8 students worked at part-time jobs last week: {lst(d)}. Find the median.", median(d),
           [sum(d) / len(d), d[3], d[4], (d[0] + d[-1]) / 2], 1,
           ["n = 8 is even, so the median is the average of the 4th and 5th values.", f"(11 + 13)/2 = {fmt(median(d), 1)} hours."],
           family="u1_median_even", std=[IB], check={"kind": "median", "data": d})
    MC(U, k, "cp2", "Five friends have a mean of $12 in their pockets. A sixth friend joins with $30. What is the new mean?",
       "$15", ["$21", "$12", "$42"],
       ["Original total = 5 × 12 = $60.", "New total = 60 + 30 = $90; new mean = 90/6 = $15."],
       family="u1_mean_add_value", std=[IB], check={"kind": "mean_after_add", "no_print_check": "n written as a word", "n": 5, "mean": 12, "new": 30, "expect": 15})
    MC(U, k, "cp2", "Which measure of spread uses only the largest and smallest values?",
       "Range", ["Interquartile range", "Standard deviation", "Median"],
       ["Range = maximum − minimum, so it depends only on the two extreme values."], family="u1_spread_def", std=[IB])
    # CP1
    d = [4, 7, 8, 10, 11]
    m = sum(d) / len(d)
    devs = [x - m for x in d]
    ss = sum(v * v for v in devs)
    SA(U, k, "cp1", f"Find the sample standard deviation of 4, 7, 8, 10, 11 by hand. Show the deviations and round the final answer to two decimal places.",
       f"sₓ ≈ {fmt(math.sqrt(ss / 4), 2)}",
       [f"Mean = 40/5 = {fmt(m)}.", "Deviations: " + ", ".join(fmt(v) for v in devs) + ".",
        "Squared deviations: " + ", ".join(fmt(v * v) for v in devs) + f"; sum = {fmt(ss)}.",
        f"Variance = {fmt(ss)}/(5 − 1) = {fmt(ss / 4)}; sₓ = √{fmt(ss / 4)} ≈ {fmt(math.sqrt(ss / 4), 2)}."],
       family="u1_sd_by_hand", std=[IB], check={"kind": "sd_sample", "data": d})
    MC(U, k, "cp1", "Every value in a data set is increased by 10. What happens to the mean and the standard deviation?",
       "The mean increases by 10; the standard deviation does not change.",
       ["Both increase by 10.", "The mean does not change; the standard deviation increases by 10.", "Both are multiplied by 10."],
       ["Adding a constant shifts the whole distribution, moving every measure of center by that constant.", "Distances between values do not change, so measures of spread stay the same."],
       family="u1_shift_effect", std=[IB])
    MC(U, k, "cp1", "Two classes took the same quiz. Class A: mean 78, SD 4. Class B: mean 78, SD 11. Which statement is correct?",
       "Class B's scores are more spread out around 78 than Class A's.", ["Class B did better on average.", "Class A has more students.", "Class B has a higher median."],
       ["Equal means show similar centers.", "A larger SD indicates scores are typically farther from the mean."], family="u1_sd_interpret", std=[IB])
    SA(U, k, "cp1", "Does the data set 2, 2, 3, 5, 8 have mean 4 and median 3? Show the calculation for each.",
       "Yes: mean = 20/5 = 4 and median = 3",
       ["Sum = 2 + 2 + 3 + 5 + 8 = 20, mean = 20/5 = 4.", "Ordered values: the middle (3rd) value is 3."],
       family="u1_construct_mean_median", std=[IB], check={"kind": "mean_median", "data": [2, 2, 3, 5, 8]})
    # Honors
    MC(U, k, "honors", "A data set has mean 50 and standard deviation 8. Each value x is converted to y = 3x − 20. What are the mean and standard deviation of y?",
       "Mean 130, SD 24", ["Mean 130, SD 4", "Mean 150, SD 24", "Mean 130, SD 72"],
       ["Mean: 3(50) − 20 = 130.", "SD: multiply by |3| = 24; subtracting 20 does not affect spread."],
       family="u1_linear_transform", std=[IB], check={"kind": "lin_both", "a": -20, "b": 3, "mean": 50, "sd": 8, "expect": [130, 24]})
    MC(U, k, "honors", "Which data set has the largest standard deviation?",
       "1, 1, 1, 9, 9, 9", ["4, 5, 5, 5, 5, 6", "1, 3, 5, 5, 7, 9", "5, 5, 5, 5, 5, 5"],
       ["All four sets have mean 5.", "In 1, 1, 1, 9, 9, 9 every value is 4 away from the mean — the largest typical distance."],
       family="u1_sd_compare_sets", std=[IB], check={"kind": "argmax_sd", "sets": [[1, 1, 1, 9, 9, 9], [4, 5, 5, 5, 5, 6], [1, 3, 5, 5, 7, 9], [5, 5, 5, 5, 5, 5]], "expect": 0})
    OR(U, k, "honors", "A coach records the 40-yard dash times (seconds) of 6 players: 4.8, 5.1, 5.0, 5.4, 4.9, 5.2",
       [("Find the mean time.", "5.07 s (exactly 30.4/6)"), ("Find the sample standard deviation. Round to three decimal places.", "sₓ ≈ 0.216 s"),
        ("Interpret the standard deviation in context.", "The players' times typically differ from the mean time of about 5.07 s by about 0.22 s"),
        ("A seventh player runs exactly 5.07 s (equal to the current mean, rounded). Without calculating, explain whether sₓ will increase or decrease.", "Decrease: a value at the mean adds nearly zero squared deviation while n − 1 grows")],
       ["1 point: correct mean.", "1 point: correct sₓ using n − 1.", "1 point: interpretation as typical distance from the mean, in context.",
        "1 point: correct direction with reasoning."], family="u1_sd_or", std=[IB],
       check={"kind": "mean_sd", "data": [4.8, 5.1, 5.0, 5.4, 4.9, 5.2], "expect": [5.0667, 0.2160], "tol": 0.001})


def s04():
    k = 4
    for lv, ctx, d in [("cp2", "Number of pages in 9 library books (in tens of pages)", [12, 15, 18, 20, 22, 25, 28, 31, 40]),
                       ("cp2", "Points scored by a basketball player in 10 games", [8, 10, 12, 12, 15, 16, 18, 20, 22, 29]),
                       ("cp1", "Ages of 14 volunteers at a food bank", [16, 17, 19, 22, 25, 28, 31, 34, 38, 41, 45, 52, 60, 67])]:
        mn, mx = min(d), max(d)
        q1, q3 = quartiles(d)
        SA(U, k, lv, f"{ctx}: {lst(d)}. Find the five-number summary and the IQR. Use the medians of the lower and upper halves as the quartiles (leave out the median when n is odd).",
           f"{fmt(mn)}, {fmt(q1)}, {fmt(median(d))}, {fmt(q3)}, {fmt(mx)}; IQR = {fmt(q3 - q1)}",
           [f"n = {len(d)}; median = {fmt(median(d))}.", f"Q1 = {fmt(q1)}, Q3 = {fmt(q3)}.", f"Min = {mn}, Max = {mx}; IQR = {fmt(q3 - q1)}."],
           family="u1_fivenum_iqr", std=[IB], check={"kind": "five_iqr", "data": d})
    src = P.boxplots("u1_box_two_classes", [("Class B", (55, 68, 74, 80, 92), []), ("Class A", (60, 70, 78, 84, 95), [])], "Test score")
    MC(U, k, "cp2", "The boxplots show test scores for two classes. Which class has the higher median?",
       "Class A (median 78 vs 74)", ["Class B (median 74 vs 78)", "They have the same median", "Cannot tell from boxplots"],
       ["The median is the line inside each box.", "Class A's median is 78; Class B's is 74."], family="u1_box_read", std=[IB, IC],
       diagram=P.image(src, "Parallel boxplots of test scores. Class A: min 60, Q1 70, median 78, Q3 84, max 95. Class B: min 55, Q1 68, median 74, Q3 80, max 92."))
    MC(U, k, "cp2", "On a boxplot, about what percent of the data lie between Q1 and Q3?",
       "50%", ["25%", "75%", "100%"], ["Q1 is the 25th percentile and Q3 the 75th, so about 75% − 25% = 50% lie in the box."], family="u1_box_concept", std=[IB])
    d = [62, 65, 68, 70, 71, 73, 75, 77, 80, 84]
    MC(U, k, "cp2", f"Heights (inches) of 10 people: {lst(d)}. A person who is 77 inches tall is at what percentile (percent of values less than 77)?",
       "70th percentile", ["80th percentile", "77th percentile", "8th percentile"],
       ["7 of the 10 values are less than 77.", "7/10 = 70%, so the 70th percentile."], family="u1_percentile_data", std=[IB],
       check={"kind": "percentile_below", "data": d, "value": 77, "expect": 70})
    MC(U, k, "cp2", "Ana's score is at the 85th percentile on a state test. What does this mean?",
       "About 85% of test takers scored lower than Ana.", ["Ana answered 85% of the questions correctly.", "Ana scored 85 points.", "15% of test takers scored lower than Ana."],
       ["A percentile is the percent of values below a given value; it is not a percent correct."], family="u1_percentile_meaning", std=[IB])
    # CP1
    src = P.boxplots("u1_box_sleep", [("Seniors", (4, 5.5, 6.5, 7, 9), []), ("Freshmen", (5, 7, 8, 8.5, 10), [])], "Hours of sleep on a school night")
    SEL(U, k, "cp1", "The boxplots summarize hours of sleep on a school night for freshmen and seniors. Select ALL correct statements.",
        ["The median for freshmen is higher than the median for seniors.", "The IQRs are equal (1.5 hours each).", "At least 75% of freshmen sleep 7 or more hours."],
        ["The seniors' range is smaller than the freshmen's range.", "Exactly half of the seniors sleep 7 hours."],
        ["Freshmen: 5, 7, 8, 8.5, 10 (IQR 1.5, range 5). Seniors: 4, 5.5, 6.5, 7, 9 (IQR 1.5, range 5).",
         "Freshmen Q1 = 7, so at least 75% of freshmen are at or above 7.", "Ranges are equal (5 and 5), so the fourth statement is false; 7 is the seniors' Q3, not the median."],
        family="u1_box_compare_sel", std=[IB, IC])
    Q_SRC = src
    ITEMS[U][-1]["diagram"] = P.image(Q_SRC, "Parallel boxplots of hours of sleep. Freshmen: min 5, Q1 7, median 8, Q3 8.5, max 10. Seniors: min 4, Q1 5.5, median 6.5, Q3 7, max 9.")
    MC(U, k, "cp1", "Two boxplots have the same median and the same range, but Box A is much wider than Box B. What does this show?",
       "The middle 50% of A is more spread out (larger IQR).", ["A has more observations.", "A has a larger mean.", "A has outliers and B does not."],
       ["The box width is the IQR, which measures the spread of the middle half."], family="u1_box_width", std=[IB, IC])
    MC(U, k, "cp1", "Which feature of a distribution can a boxplot hide?",
       "Clusters, gaps, or two peaks (bimodality) in the data", ["The median", "The range", "Outliers identified by the 1.5 × IQR rule"],
       ["A boxplot shows only five summary values plus outliers; peaks and gaps inside a section are invisible."], family="u1_box_limits", std=[IB])
    # Honors
    MC(U, k, "honors", "Data set A: 10, 20, 30, 40, 50, 60, 70. Data set B: 10, 38, 39, 40, 41, 42, 70. Which statement is true?",
       "They have identical medians and ranges but very different IQRs, so their boxplots would look different.",
       ["Their boxplots would be identical.", "They have the same IQR.", "B has a larger standard deviation than A."],
       ["Both: median 40, range 60.", "A: Q1 = 20, Q3 = 60 (IQR 40). B: Q1 = 38, Q3 = 42 (IQR 4).", "B's values cluster near 40, so its SD is smaller than A's."],
       family="u1_box_same_range", std=[IB, IC], check={"kind": "iqr_pair", "a": [10, 20, 30, 40, 50, 60, 70], "b": [10, 38, 39, 40, 41, 42, 70], "expect": [40, 4], "verify_only": True})
    p2 = [21, 24, 26, 27, 28, 30, 31, 33, 35, 36]
    p5 = [15, 18, 20, 22, 29, 33, 34, 38, 41, 48]
    OR(U, k, "honors", "Number of push-ups completed in one minute by two groups of 10 students:\nGroup 1: 21, 24, 26, 27, 28, 30, 31, 33, 35, 36\nGroup 2: 15, 18, 20, 22, 29, 33, 34, 38, 41, 48",
       [("Give the five-number summary for each group (median-of-halves quartiles).", "Group 1: 21, 26, 29, 33, 36; Group 2: 15, 20, 31, 38, 48"),
        ("Find the IQR for each group.", "Group 1: 7; Group 2: 18"),
        ("Are there any outliers by the 1.5 × IQR rule? Show the fences.", "None. Group 1 fences 15.5 and 43.5; Group 2 fences −7 and 65"),
        ("Compare the two distributions in context.", "Similar centers (medians 29 and 31), but Group 2 is much more variable (IQR 18 vs 7, range 33 vs 15); neither has outliers")],
       ["1 point: both five-number summaries.", "1 point: both IQRs.", "1 point: fences and conclusion.", "1 point: comparison of center and spread with context and comparative language."],
       family="u1_compare_or", std=[IB, IC], check={"kind": "five_pair", "a": p2, "b": p5})
    SEL(U, k, "honors", "A student's z-score is 0 and her percentile is 50 on a test whose scores are approximately Normal. Select ALL statements that must be true.",
        ["Her score equals the mean.", "Her score is approximately the median."], ["She scored 50%.", "Her score is an outlier."],
        ["z = 0 means the score equals the mean.", "For an approximately Normal (symmetric) distribution, the mean is about the median (50th percentile). Neither says anything about percent correct."],
        family="u1_z_percentile_sel", std=[IB])
    MC(U, k, "honors", "Two boxplots of house prices: Town A has median $250k and IQR $40k; Town B has median $240k and IQR $120k. A buyer wants the best chance of finding a house under $200k. Which town should she search, and why?",
       "Town B: its larger spread means more of its houses fall far below its median, so a larger share may be under $200k.",
       ["Town A, because its median is higher.", "Town A, because its IQR is smaller.", "Either; their medians are almost the same."],
       ["Town A's middle half spans only $40k around a $250k median, so few of its houses are likely to be as low as $200k.", "Town B's middle half spans $120k around a $240k median, so its lower quartile is likely far below $240k, possibly near or under $200k.",
        "Spread, not just center, determines how much of a distribution reaches a given value; a boxplot of each town would confirm."], family="u1_box_decision", std=[IC])


def s05():
    k = 5
    num_mc(U, k, "cp2", "Scores on a test have mean 70 and standard deviation 6. Find the z-score for a score of 82.", 2.0, [12, -2.0, 0.5, 1.2], 2,
           ["z = (82 − 70)/6 = 12/6 = 2.00."], family="u1_z_basic", std=[IB], check={"kind": "zscore", "x": 82, "mean": 70, "sd": 6})
    SA(U, k, "cp2", "Heights of a plant species have mean 40 cm and SD 5 cm. What height has a z-score of −1.4?", "33 cm",
       ["x = mean + z·SD = 40 + (−1.4)(5) = 40 − 7 = 33 cm."], family="u1_x_from_z", std=[IB], check={"kind": "x_from_z", "z": -1.4, "mean": 40, "sd": 5, "expect": 33})
    num_mc(U, k, "cp2", "Pulse rates are approximately Normal with mean 72 and SD 8. Use the 68–95–99.7 rule: what percent of people have pulse rates between 64 and 80?",
           68, [95, 34, 99.7, 50], 0, ["64 and 80 are one SD below and above the mean (72 ± 8).", "About 68% fall within 1 SD."],
           family="u1_empirical_basic", std=[IIIC], unit_txt="%", check={"kind": "empirical", "lo_k": -1, "hi_k": 1})
    MC(U, k, "cp2", "Which statement about the standard Normal distribution is true?",
       "It has mean 0 and standard deviation 1.", ["It has mean 1 and standard deviation 0.", "It is skewed right.", "Its total area is 100 square units."],
       ["The standard Normal (Z) distribution is N(0, 1); total area under any density curve is 1."], family="u1_std_normal", std=[IIIC])
    MC(U, k, "cp2", "A z-score of −2 means the value is",
       "2 standard deviations below the mean", ["2 units below the mean", "2 standard deviations above the mean", "in the bottom 2% of the data"],
       ["z measures distance from the mean in standard-deviation units; negative means below the mean."], family="u1_z_meaning", std=[IB])
    # CP1
    num_mc(U, k, "cp1", "Cholesterol levels of adults are approximately Normal with mean 190 mg/dL and SD 30 mg/dL. Find the proportion of adults with levels above 241 mg/dL. Round to four decimal places (use z rounded to two decimals).",
           1 - Phi(1.70), [Phi(1.70), 0.0228, 0.5 - (1 - Phi(1.70))], 4, ["z = (241 − 190)/30 = 1.70.", f"P(Z > 1.70) = 1 − {fmt(Phi(1.7), 4)} = {fmt(1 - Phi(1.7), 4)}."],
           family="u1_normal_right", std=[IIIC], bounds=(0, 1), check={"kind": "normal_area", "mean": 190, "sd": 30, "type": "gt", "a": 241})
    SA(U, k, "cp1", "Battery lives are approximately Normal with mean 500 hours and SD 40 hours. What lifetime separates the shortest 20% of batteries from the rest? Round to the nearest hour.", "466 hours",
       ["Area to the left = 0.20 → z ≈ −0.84 (invNorm gives −0.8416).", "x = 500 + (−0.8416)(40) ≈ 466.3 → about 466 hours."],
       family="u1_invnorm_left", std=[IIIC], check={"kind": "normal_inverse", "mean": 500, "sd": 40, "area_left": 0.20, "tol": 1})
    MC(U, k, "cp1", "On a density curve, the area under the curve between 2 and 5 is 0.35. What does this mean?",
       "About 35% of observations fall between 2 and 5.", ["35 observations fall between 2 and 5.", "The curve's height at 3.5 is 0.35.", "The probability of exactly 2 or exactly 5 is 0.35."],
       ["Area under a density curve over an interval equals the proportion of observations in that interval."], family="u1_density_area", std=[IIIC])
    # Honors
    SA(U, k, "honors", "A machine fills cereal boxes with weights that are Normal with SD 0.2 oz. The company wants only 2% of boxes to contain less than 16 oz. What should the mean fill weight be? Round to two decimal places.",
       "16.41 oz", ["We need P(X < 16) = 0.02, so z = invNorm(0.02) ≈ −2.054.", "16 = μ + (−2.054)(0.2) → μ = 16 + 0.411 ≈ 16.41 oz."],
       family="u1_solve_mean", std=[IIIC], check={"kind": "solve_mean", "x": 16, "sd": 0.2, "area_left": 0.02, "tol": 0.01})
    MC(U, k, "honors", "A uniform density curve is a horizontal line from 0 to 4. What proportion of observations are between 1 and 2.5?",
       "0.375", ["0.25", "1.5", "0.625"],
       ["Height = 1/4 so the total area is 1.", "Area from 1 to 2.5 = (2.5 − 1)(1/4) = 0.375."], family="u1_uniform_density", std=[IIIC],
       check={"kind": "uniform_area", "a": 0, "b": 4, "lo": 1, "hi": 2.5, "expect": 0.375})
    OR(U, k, "honors", "SAT Math scores are approximately Normal with mean 528 and SD 117. ACT Math scores are approximately Normal with mean 20.8 and SD 5.4. Maya scored 690 on the SAT; her friend Jo scored 29 on the ACT.",
       [("Find Maya's z-score (two decimals).", "z ≈ 1.38"), ("Find Jo's z-score (two decimals).", "z ≈ 1.52"),
        ("Who did better relative to other test takers? Explain.", "Jo, because her z-score is higher (1.52 > 1.38)"),
        ("What percent of SAT takers scored higher than Maya? Use z rounded to two decimals.", "About 8.38% (P(Z > 1.38) = 0.0838)")],
       ["1 point each part; part (c) needs a comparison of standardized scores, not raw scores."], family="u1_z_compare_or", std=[IB, IIIC],
       check={"kind": "z_or", "a": [690, 528, 117], "b": [29, 20.8, 5.4], "expect": [1.38, 1.52, 0.0838]})


def s06():
    k = 6
    # Self-contained two-way tables
    tab1 = ("Phone type by grade for 200 students:\n"
            "            | Android | iPhone | Total\nJuniors     |    38   |   62   |  100\nSeniors     |    27   |   73   |  100\nTotal       |    65   |  135   |  200")
    num_mc(U, k, "cp2", tab1 + "\nWhat proportion of all students use an iPhone? Round to three decimal places.", 135 / 200, [62 / 100, 73 / 135, 135 / 100 / 2 + 0.1], 3,
           ["Use the marginal total for iPhone: 135.", "135/200 = 0.675."], family="u1_tw_marginal", std=[IE], bounds=(0, 1),
           check={"kind": "twoway", "table": [[38, 62], [27, 73]], "type": "marginal_col", "col": 1})
    num_mc(U, k, "cp2", tab1 + "\nWhat proportion of all students are seniors who use Android? Round to three decimal places.", 27 / 200, [27 / 100, 27 / 65, 65 / 200], 3,
           ["Joint frequency for Seniors and Android: 27.", "27/200 = 0.135 (divide by the grand total)."], family="u1_tw_joint", std=[IE], bounds=(0, 1),
           check={"kind": "twoway", "table": [[38, 62], [27, 73]], "type": "joint", "row": 1, "col": 0})
    num_mc(U, k, "cp2", tab1 + "\nAmong juniors, what proportion use Android? Round to three decimal places.", 38 / 100, [38 / 200, 38 / 65, 65 / 200], 3,
           ["Condition on juniors: the denominator is the junior total, 100.", "38/100 = 0.380."], family="u1_tw_cond", std=[IE], bounds=(0, 1),
           check={"kind": "twoway", "table": [[38, 62], [27, 73]], "type": "cond_given_row", "row": 0, "col": 0})
    MC(U, k, "cp2", "In a two-way table, what is a marginal distribution?",
       "The distribution of one variable alone, using the row or column totals", ["The distribution of one variable within a single category of the other", "The count in one cell", "The difference between two cells"],
       ["Marginal distributions come from the totals in the margins of the table."], family="u1_tw_vocab", std=[IE])
    tab2 = ("Pet ownership by home type for 150 households:\n"
            "          | Dog | Cat | No pet | Total\nHouse     |  40 |  25 |   15   |   80\nApartment |  10 |  30 |   30   |   70\nTotal     |  50 |  55 |   45   |  150")
    SA(U, k, "cp2", tab2 + "\nWhat percent of apartment households own a cat? Round to one decimal place.", "42.9%",
       ["Condition on apartments: 70 households.", "30/70 ≈ 0.4286 → 42.9%."], family="u1_tw_cond", std=[IE],
       check={"kind": "twoway", "table": [[40, 25, 15], [10, 30, 30]], "type": "cond_given_row", "row": 1, "col": 1, "pct": True})
    SA(U, k, "cp2", tab2 + "\nHow many households own a dog? What percent of all households is that? Round to one decimal place.", "50; 33.3%",
       ["Column total for Dog: 40 + 10 = 50.", "50/150 ≈ 33.3%."], family="u1_tw_marginal", std=[IE],
       check={"kind": "twoway_count_pct", "count": 50, "total": 150})
    # CP1
    num_mc(U, k, "cp1", tab2 + "\nAmong households that own a dog, what proportion live in a house? Round to three decimal places.", 40 / 50, [40 / 80, 40 / 150, 50 / 150], 3,
           ["Condition on dog owners (column total 50).", "40/50 = 0.800."], family="u1_tw_cond_col", std=[IE], bounds=(0, 1),
           check={"kind": "twoway", "table": [[40, 25, 15], [10, 30, 30]], "type": "cond_given_col", "row": 0, "col": 0})
    MC(U, k, "cp1", tab2 + "\nWhich comparison best shows whether home type and pet ownership are associated?",
       "Compare the conditional distributions of pet ownership for houses (50%, 31.25%, 18.75%) and apartments (14.3%, 42.9%, 42.9%).",
       ["Compare the counts 40 and 10 directly.", "Compare the row totals 80 and 70.", "Compare the grand total 150 with the column totals."],
       ["Groups have different sizes, so compare conditional percents.", "Houses: 40/80, 25/80, 15/80. Apartments: 10/70, 30/70, 30/70.",
        "The distributions differ a lot, so there is an association."], family="u1_tw_association", std=[IE])
    SEL(U, k, "cp1", tab1 + "\nSelect ALL correct statements.",
        ["62% of juniors use an iPhone.", "73% of seniors use an iPhone.", "About 41.5% of Android users are seniors."],
        ["62% of iPhone users are juniors.", "Grade and phone type are independent because each grade has 100 students."],
        ["Within juniors: 62/100 = 62%; within seniors: 73/100 = 73%.", "Android users: 27/65 ≈ 41.5% are seniors.",
         "iPhone users who are juniors: 62/135 ≈ 45.9%, not 62%.", "Different conditional percents (62% vs 73%) show some association; equal group sizes do not imply independence."],
        family="u1_tw_sel", std=[IE])
    MC(U, k, "cp1", "A segmented bar graph shows, for each of two schools, the percent of students who bike, walk, or ride the bus. If the segments are nearly identical for both schools, what does that suggest?",
       "There is little or no association between school and mode of transportation.", ["There is a strong association.", "Both schools have the same number of students.", "Biking causes walking."],
       ["Similar conditional distributions across groups indicate little association."], family="u1_segbar", std=[IE])
    # Honors
    OR(U, k, "honors", "A random sample of 300 adults was classified by age group and preferred news source:\n"
       "          | Social media | TV | Print/website | Total\n18–34     |      72      | 18 |      30       |  120\n35–54     |      36      | 36 |      28       |  100\n55+       |      12      | 44 |      24       |   80\nTotal     |     120      | 98 |      82       |  300",
       [("Find the marginal distribution of news source (as percents, one decimal).", "Social media 40.0%, TV 32.7%, Print/website 27.3%"),
        ("Find the conditional distribution of news source for each age group (percents, one decimal).", "18–34: 60.0%, 15.0%, 25.0%; 35–54: 36.0%, 36.0%, 28.0%; 55+: 15.0%, 55.0%, 30.0%"),
        ("Is there an association between age group and news source? Justify.", "Yes; social media share falls from 60% to 15% and TV rises from 15% to 55% as age increases"),
        ("Can you conclude that being older causes people to prefer TV? Explain.", "No; this is an observational sample, so association does not show causation (habits, access, and other lurking variables)")],
       ["1 point each: (a) correct marginals; (b) all three conditional distributions; (c) association with specific comparison; (d) no causal claim with reason."],
       family="u1_tw_or", std=[IE], check={"kind": "twoway_or", "table": [[72, 18, 30], [36, 36, 28], [12, 44, 24]]})
    MC(U, k, "honors", "In a two-way table of treatment (A, B) by outcome (improved, not), 60 of 100 A patients and 45 of 75 B patients improved. Are treatment and outcome associated in these data?",
       "No; both groups have the same improvement rate (60%), so the conditional distributions are identical.",
       ["Yes; more A patients improved (60 vs 45).", "Yes; the group sizes differ.", "Cannot tell without the grand total."],
       ["A: 60/100 = 0.60. B: 45/75 = 0.60.", "Identical conditional distributions mean no association in the data."], family="u1_tw_noassoc", std=[IE],
       check={"kind": "equal_rates", "a": [60, 100], "b": [45, 75], "expect": True})
    MC(U, k, "honors", "Simpson's paradox: Hospital A has a higher overall survival rate than Hospital B, but Hospital B has a higher survival rate for both mild and severe cases. What explains this?",
       "Hospital B treats a much larger share of severe cases, and severity is a lurking variable that changes the overall comparison.",
       ["Hospital B's data must contain an error.", "Hospital A has more patients.", "Overall rates always agree with the rates within groups."],
       ["Aggregating over a lurking variable (severity) can reverse a comparison when groups have different mixes of that variable."], family="u1_simpson", std=[IE])
    SA(U, k, "honors", "Use the data: Hospital A treated 900 mild patients (870 survived) and 100 severe patients (30 survived). Hospital B treated 200 mild (196 survived) and 800 severe (320 survived). Find each hospital's overall survival rate and each rate within mild and severe cases (percents, one decimal).",
       "Overall: A 90.0%, B 51.6%; Mild: A 96.7%, B 98.0%; Severe: A 30.0%, B 40.0%",
       ["A overall: 900/1000 = 90.0%. B overall: 516/1000 = 51.6%.", "Mild: A 870/900 ≈ 96.7%, B 196/200 = 98.0%.", "Severe: A 30/100 = 30.0%, B 320/800 = 40.0%.",
        "B is better within each severity group but worse overall — Simpson's paradox caused by B treating mostly severe cases."],
       family="u1_simpson_calc", std=[IE], check={"kind": "simpson", "a": [[870, 900], [30, 100]], "b": [[196, 200], [320, 800]]})


def s07():
    k = 7
    MC(U, k, "cp2", "A researcher wants to predict a student's final exam score from the number of practice quizzes completed. Which is the response variable?",
       "Final exam score", ["Number of practice quizzes", "The student", "The researcher"],
       ["The response variable is the outcome being predicted."], family="u1_expl_resp", std=[ID])
    x = [1, 2, 3, 4, 5, 6]
    y = [30, 26, 25, 20, 16, 12]
    src = P.scatter("u1_sc_neg", x, y, "Weeks since purchase", "Price of a used game ($)")
    MC(U, k, "cp2", "The scatterplot shows the resale price of a video game against weeks since its release. What is the direction of the association?",
       "Negative", ["Positive", "No association", "Curved upward"],
       ["As weeks increase, prices decrease, so the association is negative."], family="u1_scatter_dir", std=[ID],
       diagram=P.image(src, "Scatterplot: weeks 1–6 on x; price $30, $26, $25, $20, $16, $12 on y; points fall steadily from upper left to lower right."))
    MC(U, k, "cp2", "Which correlation shows the weakest linear association?",
       "r = 0.12", ["r = −0.85", "r = 0.64", "r = −0.47"], ["Strength depends on |r|; 0.12 is closest to 0."], family="u1_r_strength", std=[ID])
    MC(U, k, "cp2", "A correlation of r = −0.92 between hours of TV watched and GPA means that",
       "there is a strong negative linear association: students who watch more TV tend to have lower GPAs",
       ["watching TV causes lower GPAs", "92% of students watch TV", "there is a weak association"],
       ["|r| close to 1 is strong; the negative sign gives the direction.", "Correlation does not establish causation."], family="u1_r_interpret", std=[ID])
    SEL(U, k, "cp2", "Select ALL values that are possible correlation coefficients.", ["−0.99", "0", "0.4"], ["1.3", "−2"],
        ["r is always between −1 and 1 inclusive."], family="u1_r_range_sel", std=[ID])
    # CP1
    x2 = [2, 4, 5, 7, 9]
    y2 = [3, 6, 7, 10, 12]
    r = float(np.corrcoef(x2, y2)[0, 1])
    num_mc(U, k, "cp1", f"Find the correlation r for these data (x: {lst(x2)}; y: {lst(y2)}). Round to three decimal places.", r, [r * r, -r, 0.9], 3,
           ["Use technology (LinReg) or r = Σ(zₓ·z_y)/(n − 1).", f"r ≈ {fmt(r, 3)}: a very strong positive linear association."],
           family="u1_r_calc", std=[ID], check={"kind": "correlation", "x": x2, "y": y2})
    MC(U, k, "cp1", "The correlation between height in inches and weight in pounds for a group is r = 0.68. If height is converted to centimeters and weight to kilograms, what is the new correlation?",
       "0.68", ["0.68 × 2.54", "0.68 / 2.2", "It cannot be determined"], ["r has no units and is unchanged by linear changes of units."], family="u1_r_units", std=[ID])
    MC(U, k, "cp1", "A scatterplot shows a strong curved (U-shaped) pattern, and r = 0.05. What is the best conclusion?",
       "There is a strong nonlinear relationship; r only measures linear association.", ["There is no relationship between the variables.", "The relationship is weak and linear.", "r was computed incorrectly."],
       ["r near 0 means no LINEAR association, but a clear curve is a strong relationship of another form."], family="u1_r_curve", std=[ID])
    MC(U, k, "cp1", "Swapping which variable is on the x-axis and which is on the y-axis changes",
       "neither the correlation nor its sign", ["the sign of the correlation", "the correlation to its reciprocal", "the correlation to its square"],
       ["r is symmetric in x and y."], family="u1_r_swap", std=[ID])
    # Honors
    SEL(U, k, "honors", "Select ALL true statements about the correlation r.",
        ["r is not resistant; a single outlier can change it a lot.", "Adding the same constant to every y-value leaves r unchanged.", "r = 1 means all points lie on a line with positive slope."],
        ["r = 0.8 means 80% of the points lie on the line.", "A high r proves that x causes y."],
        ["r uses means and SDs, which outliers affect.", "Linear changes of units (with positive multipliers) do not change r.", "r² (not r) relates to variation explained; correlation is not causation."],
        family="u1_r_props_sel", std=[ID])
    MC(U, k, "honors", "For a data set, zₓ and z_y are computed for each point and r = Σ(zₓz_y)/(n − 1). Most points are in quadrants where zₓ and z_y have opposite signs. What can you conclude?",
       "r is negative because most products zₓz_y are negative.", ["r is positive.", "r is zero.", "r is greater than 1."],
       ["Opposite signs make negative products; their sum (and r) is negative."], family="u1_r_quadrants", std=[ID])
    x3 = [1, 2, 3, 4, 5, 6, 7, 8]
    y3 = [2, 4, 3, 5, 6, 5, 7, 20]
    r_all = float(np.corrcoef(x3, y3)[0, 1])
    r_wo = float(np.corrcoef(x3[:-1], y3[:-1])[0, 1])
    SA(U, k, "honors", f"x: {lst(x3)}; y: {lst(y3)}. Find r with all points and r without the point (8, 20). Round to three decimals. What does the comparison show?",
       f"With: r ≈ {fmt(r_all, 3)}; without: r ≈ {fmt(r_wo, 3)}",
       [f"LinReg on all 8 points: r ≈ {fmt(r_all, 3)}.", f"Removing (8, 20): r ≈ {fmt(r_wo, 3)}.",
        "The single extreme point changes r noticeably, so r is not resistant; report both and investigate the point."],
       family="u1_r_outlier_effect", std=[ID], check={"kind": "r_pair", "x": x3, "y": y3})
    OR(U, k, "honors", "A study of 12 cities found r = 0.81 between the number of fast-food restaurants and the number of hospitals.",
       [("Describe the association indicated by r.", "Strong, positive, linear association"),
        ("Does this show that fast-food restaurants cause more hospitals to be built? Explain.", "No; correlation does not imply causation"),
        ("Identify a plausible lurking variable and explain how it could create the association.", "City population: larger cities have more of both restaurants and hospitals"),
        ("How could the researcher adjust the analysis to reduce the effect of that variable?", "Use rates per 100,000 residents (or compare cities of similar population) before correlating")],
       ["1 point each part; (c) must explain how the lurking variable relates to BOTH variables."], family="u1_r_lurking_or", std=[ID])


def s08():
    k = 8
    MC(U, k, "cp2", "A regression line for predicting a car's value (dollars) from its age (years) is ŷ = 24,000 − 1,800x. Predict the value of a 5-year-old car.",
       "$15,000", ["$22,200", "$9,000", "$33,000"], ["ŷ = 24,000 − 1,800(5) = 24,000 − 9,000 = $15,000."], family="u1_predict", std=[ID],
       check={"kind": "predict", "a": 24000, "b": -1800, "x": 5, "expect": 15000})
    MC(U, k, "cp2", "The line ŷ = 3.2 + 0.5x predicts plant height (cm) from days of growth. What does the slope 0.5 mean?",
       "For each additional day, predicted height increases by 0.5 cm.", ["Plants start at 0.5 cm.", "Height increases by 3.2 cm per day.", "Every plant grows exactly 0.5 cm per day."],
       ["Slope = predicted change in y per one-unit increase in x; use “predicted.”"], family="u1_slope_interp", std=[ID])
    SA(U, k, "cp2", "ŷ = 12 + 4x predicts a student's quiz score from hours studied. Liam studied 3 hours and scored 20. Find his predicted score and his residual.", "Predicted 24; residual −4",
       ["ŷ = 12 + 4(3) = 24.", "Residual = actual − predicted = 20 − 24 = −4 (he scored 4 points below the prediction)."], family="u1_resid_basic", std=[ID],
       check={"kind": "pred_resid", "a": 12, "b": 4, "x": 3, "y": 20})
    MC(U, k, "cp2", "If r = 0.9, what is r², and what does it tell you?",
       "0.81; about 81% of the variation in y is accounted for by the linear model.", ["0.9; 90% of predictions are correct.", "0.81; the slope is 0.81.", "1.8; the line is very steep."],
       ["r² = 0.9² = 0.81."], family="u1_r2_basic", std=[ID], check={"kind": "r_squared", "r": 0.9, "expect": 0.81, "skip_distractors": True})
    MC(U, k, "cp2", "Which point is always on the least-squares regression line?",
       "(x̄, ȳ)", ["(0, 0)", "(0, ȳ)", "The point with the largest residual"], ["The LSRL always passes through the point of means (x̄, ȳ)."], family="u1_lsrl_mean_point", std=[ID])
    MC(U, k, "cp2", "The line ŷ = 50 + 2x predicts weight (lb) of a puppy from age (weeks). What is the predicted weight of a 0-week-old puppy, and does it make sense?",
       "50 lb; it does not make sense because a newborn puppy weighs far less — x = 0 is outside the data", ["2 lb; it makes sense", "52 lb; it makes sense", "0 lb; it makes sense"],
       ["ŷ(0) = 50 is the y-intercept.", "Interpreting it requires x = 0 to be within or near the data; here it is not realistic."], family="u1_intercept_sense", std=[ID])
    # CP1
    for (xb, sx, yb, sy, r, ctx) in [(68, 3, 160, 22, 0.6, "Height (in) and weight (lb) of adults: x̄ = 68, sₓ = 3, ȳ = 160, s_y = 22, r = 0.6."),
                                     (12, 4, 85, 6, -0.5, "Absences (x) and final grade (y) in a course: x̄ = 12, sₓ = 4, ȳ = 85, s_y = 6, r = −0.5.")]:
        b = r * sy / sx
        a = yb - b * xb
        SA(U, k, "cp1", ctx + " Find the equation of the least-squares regression line. Round to two decimal places.",
           f"ŷ = {fmt(a, 2)} + {fmt(b, 2)}x" if b >= 0 else f"ŷ = {fmt(a, 2)} − {fmt(-b, 2)}x",
           [f"b = r·s_y/sₓ = {fmt(r)}({sy}/{sx}) = {fmt(b, 4)}.", f"a = ȳ − b·x̄ = {yb} − ({fmt(b, 4)})({xb}) = {fmt(a, 2)}."],
           family="u1_lsrl_summary", std=[ID], check={"kind": "lsrl_summary_both", "mx": xb, "sx": sx, "my": yb, "sy": sy, "r": r})
    MC(U, k, "cp1", "A regression of y on x has r = 0.7, and x is 2 standard deviations above its mean. How many standard deviations above ȳ is the predicted ŷ?",
       "1.4", ["2", "0.7", "2.7"], ["In standardized units, predicted z_y = r·zₓ = 0.7(2) = 1.4 (regression to the mean)."], family="u1_regression_to_mean", std=[ID],
       check={"kind": "product", "values": [0.7, 2], "expect": 1.4})
    MC(U, k, "cp1", "The regression of the number of ice cream cones sold on daily high temperature (°F) is ŷ = −120 + 4.2x, built from days with highs between 60 and 95 °F. Why is the prediction for a 20 °F day unreliable?",
       "20 °F is far outside the data (extrapolation); the model even predicts an impossible negative number of cones (−36).",
       ["Because the slope is positive.", "Because r² is not given.", "Because predictions are only valid at x = x̄."],
       ["ŷ = −120 + 4.2(20) = −120 + 84 = −36 cones, which is impossible.", "Using the line far outside the observed x-values is extrapolation."],
       family="u1_extrapolate", std=[ID], check={"kind": "predict", "a": -120, "b": 4.2, "x": 20, "expect": -36})
    # Honors
    x = [2, 3, 5, 6, 8, 9, 11, 12]
    y = [65, 70, 72, 78, 80, 86, 88, 93]
    b, a = np.polyfit(x, y, 1)
    r = float(np.corrcoef(x, y)[0, 1])
    OR(U, k, "honors", f"Hours of tutoring (x) and test score (y) for 8 students:\nx: {lst(x)}\ny: {lst(y)}",
       [("Find the least-squares regression line (round to three decimals).", f"ŷ = {fmt(a, 3)} + {fmt(b, 3)}x"),
        ("Interpret the slope in context.", f"Each additional hour of tutoring is associated with an increase of about {fmt(b, 2)} points in predicted test score"),
        ("Find and interpret r².", f"r² ≈ {fmt(r * r, 3)}; about {fmt(100 * r * r, 1)}% of the variation in test scores is accounted for by the linear model with hours of tutoring"),
        ("A student with 20 hours of tutoring is added. Explain one reason the prediction for this student may be unreliable.", "20 hours is far beyond the observed range (2–12), so it is extrapolation; scores also cannot exceed 100")],
       ["1 point each part; slope interpretation must say “predicted” and include units."], family="u1_lsrl_or", std=[ID], check={"kind": "lsrl_r2", "x": x, "y": y})
    MC(U, k, "honors", "For predicting y from x, the slope is b = 1.5 with r = 0.6. If instead we regress x on y, which is true?",
       "The new slope is r·sₓ/s_y, which is NOT 1/1.5; the two regression lines are different.",
       ["The new slope is 1/1.5 ≈ 0.667.", "The new slope is still 1.5.", "Regressing x on y gives the same line."],
       ["b_y·x = r s_y/sₓ and b_x·y = r sₓ/s_y; their product is r² = 0.36, not 1.", "So b_x·y = 0.36/1.5 = 0.24."],
       family="u1_reverse_regression", std=[ID], check={"kind": "reverse_slope", "b": 1.5, "r": 0.6, "expect": 0.24, "verify_only": True})
    SA(U, k, "honors", "A regression of y on x has slope b = 1.5 and r = 0.6. Find the slope of the least-squares line for predicting x from y.", "0.24",
       ["b_yx · b_xy = (r s_y/sₓ)(r sₓ/s_y) = r².", "b_xy = r²/b_yx = 0.36/1.5 = 0.24."], family="u1_reverse_regression", std=[ID],
       check={"kind": "reverse_slope", "b": 1.5, "r": 0.6, "expect": 0.24})
    SEL(U, k, "honors", "Select ALL true statements about least-squares regression.",
        ["The sum of the residuals is 0.", "The line minimizes the sum of squared residuals.", "The slope has the same sign as r."],
        ["The line passes through (0, ȳ).", "r² equals the slope squared."],
        ["Least squares minimizes Σ(residual²); residuals sum to 0; b = r·s_y/sₓ shares r's sign.", "The line passes through (x̄, ȳ); r² ≠ b² in general."],
        family="u1_lsrl_props_sel", std=[ID])
    MC(U, k, "honors", "Two regressions predict college GPA: from SAT score r² = 0.25; from high-school GPA r² = 0.40. Which statement is justified?",
       "High-school GPA accounts for more of the variation in college GPA (40% vs 25%) in these data.",
       ["SAT score is a useless predictor.", "High-school GPA causes college GPA.", "Using both predictors would explain 65% of the variation."],
       ["Compare r² values as proportions of variation explained by each linear model.", "Variation explained by two predictors together is not simply the sum when the predictors are related."],
       family="u1_r2_compare", std=[ID])


def s09():
    k = 9
    MC(U, k, "cp2", "A residual is",
       "the actual y-value minus the predicted y-value", ["the predicted y-value minus the actual y-value", "the distance from a point to the mean", "the slope of the line"],
       ["Residual = y − ŷ."], family="u1_resid_def", std=[ID])
    MC(U, k, "cp2", "A point has a positive residual. Where is the point relative to the regression line?",
       "Above the line (the model underpredicted)", ["Below the line", "On the line", "To the right of x̄"], ["Positive residual: y > ŷ, so the point is above the line."], family="u1_resid_sign", std=[ID])
    for (a, b, x, y, ctx) in [(30, 2.5, 8, 47, "Predicting pounds of recycling (y) from number of residents in a building floor (x): ŷ = 30 + 2.5x. A floor with 8 residents recycled 47 lb."),
                              (95, -3, 6, 80, "Predicting a test score (y) from number of absences (x): ŷ = 95 − 3x. A student with 6 absences scored 80.")]:
        yh = a + b * x
        SA(U, k, "cp2", ctx + " Find the residual and say whether the model overpredicted or underpredicted.",
           f"Residual = {fmt(y - yh)}; the model {'underpredicted' if y > yh else 'overpredicted'}",
           [f"ŷ = {fmt(a)} + ({fmt(b)})({x}) = {fmt(yh)}.", f"Residual = {y} − {fmt(yh)} = {fmt(y - yh)}.",
            "Positive residual → actual is above prediction (underpredicted)." if y > yh else "Negative residual → actual is below prediction (overpredicted)."],
           family="u1_resid_calc", std=[ID], check={"kind": "residual", "a": a, "b": b, "x": x, "y": y})
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    resid = [3, 1, -1, -2, -3, -1, 1, 3]
    src = P.scatter("u1_resid_curve", x, resid, "x", "Residual", "Residual plot", hline0=True)
    MC(U, k, "cp2", "The residual plot for a linear model is shown. What does it suggest?",
       "A curved pattern, so a linear model is not appropriate", ["Random scatter, so a linear model is appropriate", "One outlier", "The slope is negative"],
       ["Residuals go from positive to negative and back to positive — a U-shaped pattern.", "A pattern in residuals means the line misses the form of the relationship."],
       family="u1_resid_plot", std=[ID], diagram=P.image(src, "Residual plot with residuals 3, 1, −1, −2, −3, −1, 1, 3 at x = 1 through 8, forming a U shape around the zero line."))
    MC(U, k, "cp2", "A residual plot shows points scattered randomly above and below zero with no pattern. What does this mean?",
       "A linear model is appropriate for the data.", ["The data have no relationship.", "There is a strong curve.", "All predictions are exactly correct."],
       ["Random scatter means the line has captured the form; leftover variation is just noise."], family="u1_resid_random", std=[ID])
    SEL(U, k, "cp2", "Select ALL reasons a prediction from a regression line might be unreliable.",
        ["The x-value is far outside the range of the data.", "The residual plot shows a curved pattern."],
        ["The residuals sum to zero.", "The line passes through (x̄, ȳ)."],
        ["Extrapolation and a non-linear form make predictions unreliable.", "Residuals summing to zero and passing through the means are always true for least squares."],
        family="u1_unreliable_sel", std=[ID])
    MC(U, k, "cp2", "Which point in a scatterplot is most likely to be influential?",
       "A point with an x-value far from the other points that does not follow their pattern", ["A point near (x̄, ȳ)", "A point with a small residual in the middle of the data", "Any point with a positive residual"],
       ["Points far out in the x-direction have high leverage; if off the pattern, they move the line a lot."], family="u1_influential", std=[ID])
    MC(U, k, "cp2", "Residuals from a linear model have standard deviation s = 3.2 points. What does s tell us?",
       "Predictions from the line are typically off by about 3.2 points.", ["The slope is 3.2.", "3.2% of points are outliers.", "The correlation is 3.2."],
       ["s measures the typical size of a residual (prediction error)."], family="u1_s_interp", std=[ID])
    # CP1
    x = [1, 2, 3, 4, 5, 6]
    y = [5, 7, 8, 11, 12, 15]
    b, a = np.polyfit(x, y, 1)
    res = [yy - (a + b * xx) for xx, yy in zip(x, y)]
    s = math.sqrt(sum(e * e for e in res) / (len(x) - 2))
    SA(U, k, "cp1", f"x: {lst(x)}; y: {lst(y)}. The LSRL is ŷ = {fmt(a, 3)} + {fmt(b, 3)}x. Find the residual for x = 4 and the standard deviation of the residuals s (use n − 2). Round to three decimals.",
       f"Residual at x = 4: {fmt(res[3], 3)}; s ≈ {fmt(s, 3)}",
       [f"ŷ(4) = {fmt(a, 3)} + {fmt(b, 3)}(4) = {fmt(a + 4 * b, 3)}; residual = 11 − {fmt(a + 4 * b, 3)} = {fmt(res[3], 3)}.",
        "Residuals: " + ", ".join(fmt(e, 3) for e in res) + ".", f"s = √(Σresid²/(n − 2)) = √({fmt(sum(e * e for e in res), 4)}/4) ≈ {fmt(s, 3)}."],
       family="u1_s_calc", std=[ID], check={"kind": "resid_s", "x": x, "y": y, "at": 4})
    MC(U, k, "cp1", "A residual plot shows residuals that are small for small x and spread out more and more as x increases (a fan shape). What does this indicate?",
       "Predictions are less precise for larger x; the variability of y is not constant.", ["The linear model is perfect.", "The correlation is negative.", "There are no outliers."],
       ["A fan shape shows changing spread, so prediction error grows with x."], family="u1_resid_fan", std=[ID])
    MC(U, k, "cp1", "A point lies far above all the others in the y-direction but near x̄. Removing it will most likely",
       "change the y-intercept a little and increase r, but barely change the slope", ["greatly change the slope", "make r negative", "have no effect on anything"],
       ["A point near x̄ has low leverage, so the slope barely moves.", "Its large residual weakens r; removing it raises r and lowers the line slightly."], family="u1_outlier_y", std=[ID])
    MC(U, k, "cp1", "A data set relating population (y) to year (x) shows clear exponential growth. What is an appropriate first step before fitting a line?",
       "Transform y with a logarithm and check whether log(y) vs. x is linear.", ["Use the original data; lines fit everything.", "Remove the largest points.", "Swap x and y."],
       ["Exponential growth becomes linear after taking log(y)."], family="u1_transform", std=[ID])
    # Honors
    x = [1, 2, 3, 4, 5, 6, 7, 15]
    y = [3, 5, 6, 8, 9, 11, 12, 10]
    b_all, a_all = np.polyfit(x, y, 1)
    b_wo, a_wo = np.polyfit(x[:-1], y[:-1], 1)
    SA(U, k, "honors", f"x: {lst(x)}; y: {lst(y)}. Find the LSRL slope with all 8 points and without (15, 10). Round to three decimals. Is (15, 10) influential?",
       f"Slope with: {fmt(b_all, 3)}; without: {fmt(b_wo, 3)}; yes, it is influential",
       [f"All points: b ≈ {fmt(b_all, 3)}.", f"Without (15, 10): b ≈ {fmt(b_wo, 3)}.",
        "The slope changes substantially, so the high-leverage point (far right, below the pattern) is influential."],
       family="u1_influence_calc", std=[ID], check={"kind": "slope_pair", "x": x, "y": y})
    MC(U, k, "honors", "A high-leverage point lies exactly on the line formed by the other points. Which is true?",
       "It has a small residual and does not change the slope much, but it increases r.", ["It must be influential.", "It decreases r.", "It changes the slope a lot."],
       ["Influence depends on whether a point follows the pattern.", "A far-out point consistent with the line strengthens the apparent linear association."],
       family="u1_leverage_on_line", std=[ID])
    OR(U, k, "honors", "A linear model predicts the number of calories burned (y) from minutes of exercise (x) for 15 adults: ŷ = 12 + 7.8x, r² = 0.91, s = 18 calories. The residual plot shows random scatter, except that one adult who exercised 60 minutes has a residual of −95.",
       [("Interpret s in context.", "Predictions of calories burned are typically off by about 18 calories"),
        ("Find the actual number of calories burned by the adult with the −95 residual.", "Predicted 12 + 7.8(60) = 480; actual = 480 − 95 = 385 calories"),
        ("Is this adult an outlier in the regression? Explain.", "Yes; a residual of −95 is more than 5 times s = 18, far from the other residuals"),
        ("Does the random scatter in the rest of the residual plot support a linear model? What should the analyst do about the unusual point?", "Yes; the linear form is appropriate. Investigate the point (recording error, different exercise intensity) and report the fit with and without it")],
       ["1 point each part; (b) requires actual = predicted + residual."], family="u1_resid_or", std=[ID], check={"kind": "actual_from_resid", "a": 12, "b": 7.8, "x": 60, "resid": -95, "expect": 385})
    # Error-analysis item (purpose-written)
    SA(U, k, "honors", "Error analysis. A student found the residual for a point (6, 40) using ŷ = 10 + 4x:\nStep 1: ŷ = 10 + 4(6) = 34\nStep 2: residual = ŷ − y = 34 − 40 = −6\nStep 3: “The point is below the line, so the model overpredicted.”\nIdentify the error and give the correct residual and interpretation.",
       "Step 2 is wrong: residual = y − ŷ = 40 − 34 = 6; the point is above the line, so the model underpredicted.",
       ["Step 1 is correct: ŷ = 34.", "Step 2 reverses the order; the residual is actual − predicted = 40 − 34 = 6.",
        "Step 3 follows from the wrong sign; a positive residual means the point is above the line and the model underpredicted."],
       family="u1_resid_error", std=[ID], check={"kind": "residual", "a": 10, "b": 4, "x": 6, "y": 40})


def extras():
    """Additional distinct items to bring thin cells to target."""
    # s01 extras
    MC(U, 1, "cp2", "A dotplot is best used for",
       "showing each value of a small quantitative data set on a number line", ["showing the percent of a whole for each category", "comparing two categorical variables", "displaying a relationship between two quantitative variables"],
       ["Each dot represents one observation on a number line, which works well for small quantitative data sets."], family="u1_dotplot_purpose", std=[IA])
    MC(U, 1, "cp1", "A frequency table of 25 students' number of siblings is: 0 siblings: 4, 1: 9, 2: 7, 3: 3, 4: 2. What is the median number of siblings?",
       "1", ["2", "1.5", "9"], ["n = 25, so the median is the 13th value.", "Cumulative counts: 0 → 4, 1 → 13. The 13th value is 1."], family="u1_freq_median", std=[IA, IB],
       check={"kind": "freq_median", "values": [0, 1, 2, 3, 4], "counts": [4, 9, 7, 3, 2], "expect": 1})
    SA(U, 1, "cp1", "Using the frequency table (0 siblings: 4, 1: 9, 2: 7, 3: 3, 4: 2; 25 students), find the mean number of siblings.", "1.6",
       ["Total siblings = 0(4) + 1(9) + 2(7) + 3(3) + 4(2) = 0 + 9 + 14 + 9 + 8 = 40.", "Mean = 40/25 = 1.6."], family="u1_freq_mean", std=[IA, IB],
       check={"kind": "freq_mean", "values": [0, 1, 2, 3, 4], "counts": [4, 9, 7, 3, 2], "expect": 1.6})
    # s02 extras
    MC(U, 2, "cp1", "Which type of distribution would most likely be skewed right?",
       "Annual incomes of all adults in a city", ["Scores on an easy quiz where most students did well", "Heights of adult women", "Ages at retirement"],
       ["Incomes have a floor near zero but a long tail of very high earners."], family="u1_shape_context", std=[IA])
    # s03 extras
    MC(U, 3, "cp1", "The variance of a data set is 49 square inches. What is the standard deviation?", "7 inches", ["49 inches", "24.5 inches", "2401 inches"],
       ["SD = √variance = √49 = 7, in the original units."], family="u1_variance_sd", std=[IB], check={"kind": "sqrt", "v": 49, "expect": 7})
    MC(U, 3, "honors", "Adding a new value equal to the current mean to a data set will",
       "leave the mean unchanged and decrease the standard deviation", ["increase both", "leave both unchanged", "decrease the mean"],
       ["The sum of deviations stays 0, so the mean is unchanged.", "The sum of squared deviations is unchanged while n − 1 grows, so sₓ decreases."], family="u1_add_mean_value", std=[IB])
    MC(U, 3, "cp2", f"Six students' quiz scores are 7, 9, 9, 10, 6, 7. What is the mode?", "7 and 9 (bimodal)", ["9", "8", "7"],
       ["7 appears twice and 9 appears twice; every other value once.", "There are two modes, 7 and 9."], family="u1_mode", std=[IB])
    # s04 extras
    MC(U, 4, "cp1", "If the largest value in a data set is increased by 50, which part of the boxplot changes?",
       "Only the upper whisker (or an outlier mark) changes", ["The median", "The box", "The lower whisker"],
       ["Quartiles and the median do not depend on the maximum's exact value."], family="u1_box_change_max", std=[IB])
    SA(U, 4, "cp1", "In a class of 30 students, Kai's score is higher than 24 of his classmates' scores. What is Kai's percentile (percent of scores below his)?", "80th percentile",
       ["24 of the 30 scores are below Kai's.", "24/30 = 0.80 → 80th percentile."], family="u1_percentile_rank", std=[IB],
       check={"kind": "ratio_pct", "num": 24, "den": 30, "expect": 80})
    MC(U, 4, "honors", "A boxplot of 40 commute times shows Q1 = 15 min and Q3 = 35 min, and an asterisk at 90 min. Which statement is guaranteed?",
       "At least one commute time is greater than 65 minutes.", ["The mean is 25 minutes.", "Exactly 10 times are between 15 and 25 minutes.", "The maximum whisker ends at 65 minutes."],
       ["IQR = 20; upper fence = 35 + 30 = 65.", "The asterisk marks an outlier above 65 (at 90)."], family="u1_box_fence_reason", std=[IB],
       check={"kind": "upper_fence", "q1": 15, "q3": 35, "expect": 65, "skip_distractors": True})
    # s05 extras
    num_mc(U, 5, "cp1", "Women's heights are approximately Normal with mean 64.5 in and SD 2.5 in. What proportion of women are between 62 and 68 inches tall? Round to four decimal places (z to two decimals).",
           Phi(1.4) - Phi(-1.0), [Phi(1.4), 1 - (Phi(1.4) - Phi(-1.0)), 0.68], 4,
           ["z₁ = (62 − 64.5)/2.5 = −1.00; z₂ = (68 − 64.5)/2.5 = 1.40.", f"Area = {fmt(Phi(1.4), 4)} − {fmt(Phi(-1), 4)} = {fmt(Phi(1.4) - Phi(-1), 4)}."],
           family="u1_normal_between", std=[IIIC], bounds=(0, 1), check={"kind": "normal_area", "mean": 64.5, "sd": 2.5, "type": "between", "a": 62, "b": 68})
    MC(U, 5, "cp2", "On a Normal curve, the mean, median, and mode are",
       "all equal, at the center of the curve", ["all different", "equal only if the SD is 1", "located at the inflection points"],
       ["A Normal curve is symmetric and unimodal, so all three centers coincide."], family="u1_normal_centers", std=[IIIC])
    MC(U, 5, "honors", "A Normal probability plot for a data set curves upward at the right end (points rise above the line). What does this suggest?",
       "The largest values are larger than a Normal model predicts — the distribution is skewed right.", ["The data are exactly Normal.", "The data are skewed left.", "There are too few observations."],
       ["In a Normal probability plot, a long right tail shows as points bending away from the line at the high end."], family="u1_nplot", std=[IIIC])
    # s06 extras
    MC(U, 6, "cp1", "In a survey, 30% of 200 freshmen and 30% of 150 sophomores say they bring lunch from home. What does this suggest?",
       "No association between grade and bringing lunch in these data", ["A strong association, because more freshmen bring lunch (60 vs 45)", "Sophomores are more likely to bring lunch", "The table must be wrong"],
       ["Conditional percents are equal (30% and 30%).", "Comparing counts is misleading when group sizes differ."], family="u1_tw_equal_pct", std=[IE])
    # s07 extras
    MC(U, 7, "honors", "In a scatterplot of exam score vs. hours of sleep for 30 students, r = 0.35. A student claims, “If I sleep more I will score higher.” What is the best response?",
       "The association is weak and observational; it does not show that more sleep causes higher scores for any individual.",
       ["Correct; r is positive so more sleep causes higher scores.", "Wrong; r = 0.35 means sleep lowers scores.", "Correct, because 35% of the variation is explained."],
       ["r = 0.35 is a weak positive association (r² ≈ 0.12).", "Observational data cannot show causation."], family="u1_r_causal", std=[ID])
    MC(U, 7, "cp1", "When describing a scatterplot, “form” refers to",
       "whether the pattern is linear, curved, or has clusters", ["whether the association is positive or negative", "how closely points follow the pattern", "the units of the variables"],
       ["Direction = positive/negative; form = linear/curved; strength = how tightly points follow the form."], family="u1_scatter_vocab", std=[ID])
    # s08 extras
    MC(U, 8, "honors", "A regression of weight (kg) on height (cm) has slope 0.9 kg per cm. If height were measured in meters instead, what would the slope be?",
       "90 kg per meter", ["0.009 kg per meter", "0.9 kg per meter", "9 kg per meter"],
       ["1 m = 100 cm, so a 1-unit increase in x (meters) is 100 times larger.", "Slope = 0.9 × 100 = 90 kg per meter."], family="u1_slope_units", std=[ID],
       check={"kind": "product", "values": [0.9, 100], "expect": 90, "no_print_check": "100 cm per m implied"})
    MC(U, 8, "cp1", "For the regression ŷ = 2.1 + 0.35x, r² = 0.64. What is r?", "0.8", ["−0.8", "0.64", "0.4096"],
       ["r = ±√0.64 = ±0.8.", "The slope is positive, so r = 0.8."], family="u1_r_from_r2", std=[ID], check={"kind": "sqrt", "v": 0.64, "expect": 0.8})


def build():
    for f in (s01, s02, s03, s04, s05, s06, s07, s08, s09, extras):
        f()
