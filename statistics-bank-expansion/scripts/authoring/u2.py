from common import *

U = "sampling-experimentation"
A, B, C_, D = "APSTATS.II.A", "APSTATS.II.B", "APSTATS.II.C", "APSTATS.II.D"
STD = {1: [A, B + ".2"], 2: [B + ".4"], 3: [B + ".3"], 4: [A + ".3", A + ".4"], 5: [C_ + ".1", C_ + ".2"], 6: [C_ + ".3"], 7: [C_ + ".4", C_ + ".5"], 8: [D]}


def mcs(k, level, rows, fam):
    for prompt, correct, wrongs, steps in rows:
        MC(U, k, level, prompt, correct, wrongs, steps, family=fam, std=STD[k])


def s01():
    k = 1
    mcs(k, "cp2", [
        ("A city council wants to know what percent of its 48,000 registered voters support a new park. It surveys 600 registered voters. What is the sample?",
         "The 600 registered voters who were surveyed", ["All 48,000 registered voters", "The city council", "The percent who support the park"],
         ["The sample is the part of the population from which data are actually collected."]),
        ("A cereal company checks the weight of 40 boxes from today's production of 12,000 boxes. What is the population?",
         "All 12,000 boxes produced today", ["The 40 boxes weighed", "The weights of the 40 boxes", "All cereal boxes ever made by every company"],
         ["The population is the entire group the company wants information about: today's production."]),
        ("A town wants to know the percent of its 420 households that have solar panels. Why might it be reasonable to take a census instead of a sample?",
         "The population is small enough that contacting every household is practical, and a census avoids sampling variability.",
         ["Censuses are always cheaper than samples.", "Samples cannot estimate percents.", "A census never has any errors."],
         ["When a population is small and easy to reach, a census is feasible; it still can have nonresponse or measurement errors."]),
        ("In a sample of 250 students at a school, 38% said they eat breakfast every day. What is the 38% called?",
         "A statistic", ["A parameter", "A population", "A census"], ["A number that describes a sample is a statistic."]),
        ("The true percent of all U.S. households that own a dog is an example of a",
         "parameter", ["statistic", "sample", "variable"], ["A number describing an entire population is a parameter (usually unknown)."]),
    ], "u2_pop_sample")
    SEL(U, k, "cp2", "Select ALL situations in which data are collected from a sample rather than the whole population of interest.",
        ["A teen magazine surveys 500 readers to learn about all U.S. teens.", "A factory tests 30 batteries from a batch of 10,000."],
        ["A teacher records every student's grade in her class to compute the class average.", "A family records the height of each of its four members."],
        ["A sample is a subset of the population of interest.", "The class and the family are complete populations, so those are censuses."],
        family="u2_census_sel", std=STD[k])
    SA(U, k, "cp2", "A school librarian wants to know the average number of books read last summer by the 1,350 students at her school. She asks 90 students in the library one morning. Identify the population and the sample.",
       "Population: all 1,350 students at the school. Sample: the 90 students asked in the library.",
       ["Population = the whole group of interest (all students at the school).", "Sample = those actually asked (90 students in the library). (This convenience sample may not represent the population.)"],
       family="u2_identify_pop_sample_sa", std=STD[k])
    mcs(k, "cp1", [
        ("A company that makes light bulbs wants to know the average lifetime of a production run. Why must it use a sample instead of a census?",
         "Measuring lifetime destroys the bulb, so testing every bulb would leave none to sell.", ["A census is always less accurate than a sample.", "Light bulbs cannot be counted.", "Samples are required by law."],
         ["When measurement is destructive, a census is impossible in practice."]),
        ("Which pair of symbols correctly matches a population parameter with the sample statistic that estimates it?",
         "μ is estimated by x̄", ["x̄ is estimated by μ", "p̂ is estimated by p", "σ is estimated by p̂"],
         ["Parameters (Greek letters, p) describe populations; statistics (x̄, sₓ, p̂) describe samples and estimate them."]),
        ("A list of individuals from which a sample is actually drawn is called the",
         "sampling frame", ["population parameter", "response variable", "treatment group"],
         ["The sampling frame is the list used to select the sample; ideally it matches the population."]),
        ("Inference in statistics means",
         "using information from a sample to draw conclusions about a population", ["collecting data from every member of a population", "describing only the sample that was collected", "assigning treatments to subjects"],
         ["Statistical inference generalizes from a sample to the population, with a statement of uncertainty."]),
        ("A survey reports that the mean commute time in a random sample of 400 city workers is 27.4 minutes. Which statement is correct?",
         "27.4 minutes is a statistic that estimates the mean commute time of all city workers.", ["27.4 minutes is the parameter for all city workers.", "All city workers commute exactly 27.4 minutes.", "The population is the 400 workers."],
         ["The sample mean is a statistic; the population mean (parameter) is unknown."]),
        ("Why might a well-designed sample give more accurate results than an attempted census of a large population?",
         "A census of a large population is hard to complete carefully, so it can have more nonresponse and measurement errors than a careful sample.",
         ["A sample always has less sampling variability than a census.", "A census never includes everyone, by definition.", "Samples cannot have any bias."],
         ["Accuracy depends on how carefully data are collected; huge censuses often suffer from errors a smaller, well-run sample avoids."]),
    ], "u2_census_vs_sample")
    SA(U, k, "cp1", "A state wildlife agency wants to estimate the proportion of all deer in a state forest that carry a certain tick. Rangers capture and test 120 deer; 27 carry the tick. Identify the population, the parameter, the sample, and the statistic (with its value as a decimal).",
       "Population: all deer in the forest; parameter: the proportion p of all deer in the forest with the tick; sample: the 120 tested deer; statistic: p̂ = 27/120 = 0.225",
       ["Population = all deer in the state forest.", "Parameter = p, the true proportion of those deer carrying the tick (unknown).",
        "Sample = the 120 captured deer.", "Statistic = p̂ = 27/120 = 0.225."],
       family="u2_identify_all", std=STD[k], check={"kind": "ratio", "num": 27, "den": 120})
    SEL(U, k, "cp1", "Select ALL of the following that are statistics (not parameters).",
        ["The mean GPA of 80 randomly selected seniors", "The proportion of 1,000 surveyed voters who approve of the mayor"],
        ["The mean height of all players currently in the NBA", "The percent of all U.S. adults who smoke"],
        ["Statistics come from samples; parameters describe whole populations."], family="u2_param_stat_sel", std=STD[k])
    mcs(k, "honors", [
        ("A researcher wants to estimate the proportion of all adults in a state who have a library card, but her sampling frame is the list of people who borrowed a book last year. What is the main problem?",
         "The frame excludes adults with cards who did not borrow books (and includes only active users), so the sample cannot represent all adults.",
         ["The sample size will be too large.", "There is no problem; borrowers are adults.", "A sampling frame must always be a phone book."],
         ["When the sampling frame does not match the population, some members cannot be selected — a source of bias."]),
        ("A survey of 2,000 randomly selected Ohio high school students finds that 64% have a part-time job. To which population can the result be generalized?",
         "All Ohio high school students (the population that was sampled)", ["All U.S. teenagers", "All Ohio adults", "Only the 2,000 students"],
         ["Random sampling allows generalization to the population that was sampled, not to other populations."]),
        ("A researcher must define the population precisely before sampling. Which definition is most useful for a survey about weekend sleep?",
         "Students enrolled at Central High School in grades 9–12 on October 1 of this year", ["Teenagers", "People who sleep", "Some students at a high school"],
         ["A precise population names who is included, where, and when, so a matching sampling frame can be built."]),
        ("A company surveys a random sample of its online customers about shipping speed. A manager uses the results to describe all of its customers, including those who shop only in its stores. What is wrong?",
         "The sample came from online customers only; in-store customers were not in the sampled population, so the results may not apply to them.",
         ["Nothing; online customers are a random sample of all customers.", "The sample was too small.", "Online surveys always produce voluntary response bias."],
         ["Conclusions should be limited to the population actually sampled."]),
        ("A poll reports, “In a random sample of 1,025 adults, 52% favor the proposal, with a margin of error of 3 percentage points.” What does the margin of error account for?",
         "Only the chance variation from random sampling", ["Undercoverage and nonresponse", "Biased question wording", "Every possible error in the poll"],
         ["The margin of error measures sampling variability; it does not cover bias from poor data collection."]),
        ("Which is the best reason to take a random sample instead of choosing a “representative” sample by judgment?",
         "Random selection removes the researcher's personal choices, so the sample is not systematically biased and probability can describe its variability.",
         ["Random samples are always larger.", "Judgment samples cannot be analyzed with a calculator.", "Random samples guarantee the statistic equals the parameter."],
         ["Randomization guards against selection bias and makes probability-based inference possible."]),
    ], "u2_frame_scope")
    OR(U, k, "honors", "A school district with 9,200 students wants to estimate the proportion of students who have reliable home internet access. The district has an enrollment list with every student's name and school.",
       [("Define the population and the parameter of interest.", "Population: all 9,200 students in the district; parameter: the proportion p of these students with reliable home internet access"),
        ("Explain why an online survey e-mailed to all students would give a misleading estimate.", "Students without reliable internet are less likely to receive or complete it, so the estimate would be too high (undercoverage/nonresponse)"),
        ("Describe how to select an SRS of 300 students from the enrollment list.", "Number the students 1–9,200; use a random number generator to pick 300 different numbers; survey those students"),
        ("Describe a data-collection method that would reduce the problem in part (b).", "Contact the selected students by paper form at school or by phone/in person, and follow up with nonresponders")],
       ["1 point each part; (b) must state the direction of the bias with a reason."], family="u2_survey_design_or", std=STD[k])
    SA(U, k, "honors", "A sample survey of 1,500 randomly chosen adults reports that 31% exercise daily. Name the parameter, give the statistic, and explain why a different random sample of 1,500 adults would likely give a different statistic.",
       "Parameter: the proportion of all adults who exercise daily; statistic: p̂ = 0.31; different samples contain different individuals, so p̂ varies from sample to sample (sampling variability)",
       ["The parameter p describes all adults and is unknown.", "The statistic p̂ = 0.31 comes from this sample.", "Each random sample includes different people, so p̂ changes from sample to sample.", "This sampling variability is what a margin of error describes."],
       family="u2_sampling_variability", std=STD[k])


def s02():
    k = 2
    mcs(k, "cp2", [
        ("A teacher puts the names of all 28 students on identical slips, mixes them in a bag, and draws 5 names. This is",
         "a simple random sample", ["a stratified random sample", "a cluster sample", "a convenience sample"],
         ["Every group of 5 students has the same chance of being chosen, which defines an SRS."]),
        ("A store manager surveys every customer who enters during the first hour of the day. This is",
         "a convenience sample", ["a simple random sample", "a stratified sample", "a cluster sample"],
         ["Selecting whoever is easiest to reach is convenience sampling; no randomness is used."]),
        ("A school separates its students by grade (9, 10, 11, 12) and randomly selects 30 students from each grade. This is",
         "a stratified random sample", ["a cluster sample", "a simple random sample", "a systematic random sample"],
         ["The population is divided into groups (strata) and an SRS is taken from every stratum."]),
        ("An airline randomly selects 6 of its 120 flights on a given day and surveys every passenger on those flights. This is",
         "a cluster sample", ["a stratified random sample", "a simple random sample of passengers", "a convenience sample"],
         ["Entire groups (flights) are chosen at random and everyone in them is surveyed."]),
        ("A factory inspector randomly picks one of the first 20 items off the line and then inspects every 20th item after that. This is",
         "a systematic random sample", ["a stratified random sample", "a cluster sample", "a simple random sample"],
         ["A random start followed by every kth item is systematic sampling."]),
        ("Why does a researcher number every individual in the population before using a random number generator?",
         "So that each individual can be matched to a random number and every individual has a chance to be chosen", ["To make the sample larger", "So the researcher can choose favorite numbers", "To put the individuals in strata"],
         ["Labels let random numbers select individuals without researcher choice."]),
    ], "u2_identify_method")
    digits = "19223 95034 05756 28713 96409"
    SA(U, k, "cp2", f"Use the random digits {digits} to select 4 students from a class labeled 01–30. Read two digits at a time from left to right, skipping numbers outside 01–30 and repeats. List the labels chosen in order.",
       "19, 22, 05, 13",
       ["Split into pairs: 19 22 39 50 34 05 75 62 87 13 …", "19 (choose), 22 (choose); 39, 50, 34 (skip: over 30); 05 (choose).",
        "75, 62, 87 (skip); 13 (choose).", "Sample: 19, 22, 05, 13."],
       family="u2_random_digits", std=STD[k], check={"kind": "random_digits", "digits": digits, "width": 2, "lo": 1, "hi": 30, "n": 4})
    digits = "71487 09984 29077 14863 61683 47052 62224 51025"
    SA(U, k, "cp1", f"A company labels its 480 employees 001–480. Use the random digits {digits} to choose 3 employees. Read three digits at a time from left to right, skipping 000, numbers over 480, and repeats. Which labels are chosen, in order?",
       "429, 077, 148",
       ["Triples: 714 870 998 429 077 148 …", "714, 870, 998 are greater than 480, so skip them.", "429 is chosen, then 077, then 148.", "Sample: employees 429, 077, 148."],
       family="u2_random_digits3", std=STD[k], check={"kind": "random_digits", "digits": digits, "width": 3, "lo": 1, "hi": 480, "n": 3})
    SA(U, k, "cp1", "A university has 6,000 undergraduates, 3,000 graduate students, and 1,000 professional students. It wants a stratified random sample of 400 with sample sizes proportional to the size of each group. How many should be sampled from each group?",
       "Undergraduates 240, graduate 120, professional 40",
       ["Total = 10,000 students.", "Undergraduates: 400 × 6,000/10,000 = 240.", "Graduate: 400 × 3,000/10,000 = 120.", "Professional: 400 × 1,000/10,000 = 40."],
       family="u2_proportional_alloc", std=STD[k], check={"kind": "alloc", "sizes": [6000, 3000, 1000], "n": 400})
    mcs(k, "cp1", [
        ("A researcher wants to estimate average household income in a city where incomes differ sharply by neighborhood but are similar within neighborhoods. Which method is most likely to give a precise estimate?",
         "Stratify by neighborhood and take an SRS within each neighborhood", ["Randomly choose two neighborhoods and survey everyone in them", "Survey the first 500 households on a list", "Take a convenience sample downtown"],
         ["Strata that are similar inside and different from each other make stratified sampling precise."]),
        ("A health department wants to interview residents of a rural county spread over 50 small towns, and travel is expensive. Which method is most practical?",
         "Randomly select a few towns and interview residents in the selected towns (cluster sampling)", ["Take an SRS of residents from the whole county", "Interview only residents of the largest town", "Ask residents to call in"],
         ["Cluster sampling reduces travel cost by concentrating interviews in randomly chosen groups."]),
        ("Which property is true of a simple random sample but NOT of a systematic random sample of the same size?",
         "Every possible group of n individuals has the same chance to be the sample.", ["Every individual has the same chance of being selected.", "It uses a random number generator.", "It requires a list of the population."],
         ["In systematic sampling every individual can have equal chance, but many groups (e.g., two neighbors on the list) can never be selected together."]),
    ], "u2_method_choice")
    SEL(U, k, "cp1", "Select ALL statements that are true.",
        ["In stratified sampling, an SRS is taken from every stratum.", "In cluster sampling, every individual in each selected cluster is included."],
        ["In cluster sampling, an SRS is taken from every cluster.", "A stratified sample is always a simple random sample."],
        ["Stratified: sample within every group. Cluster: choose some groups, take all of them.", "A stratified sample is not an SRS because some combinations (e.g., all from one stratum) are impossible."],
        family="u2_strat_cluster_sel", std=STD[k])
    mcs(k, "honors", [
        ("To estimate the mean number of hours students study, a principal can stratify by grade level or by first letter of last name. Which is better, and why?",
         "Grade level, because study time likely differs between grades and is similar within a grade; last names are unrelated to study time.",
         ["Last name, because it creates more strata.", "Either; any strata reduce variability equally.", "Neither; stratifying always increases bias."],
         ["Stratification helps only when the stratifying variable is related to the response."]),
        ("A state samples school districts at random, then randomly selects schools within those districts, and then randomly selects classrooms in those schools. This is",
         "a multistage sample", ["a simple random sample", "a census", "a systematic sample"],
         ["Sampling in several stages (clusters within clusters) is multistage sampling, common in large surveys."]),
        ("A cluster sample of apartment buildings is used to estimate the proportion of residents who rent. Why could this give a less precise estimate than an SRS of the same number of residents?",
         "Residents within a building tend to be alike (all renters or all owners), so each cluster adds little new information.",
         ["Cluster samples are biased by definition.", "Cluster samples always have fewer individuals.", "Buildings cannot be numbered."],
         ["When clusters are internally similar, the effective information is closer to the number of clusters than the number of people."]),
    ], "u2_method_honors")
    SA(U, k, "honors", "A city has 4 wards with 12,000, 9,000, 6,000, and 3,000 registered voters. A poll will use a stratified random sample of 750 voters with proportional allocation. How many voters should be sampled from each ward? Explain why proportional allocation keeps the sample representative.",
       "300, 225, 150, 75; each ward is represented in the same proportion as in the population",
       ["Total voters = 30,000.", "Ward sizes as fractions: 0.4, 0.3, 0.2, 0.1.", "Multiply by 750: 300, 225, 150, 75.", "Each ward's share of the sample equals its share of the population, so no ward is over- or under-represented."],
       family="u2_proportional_alloc", std=STD[k], check={"kind": "alloc", "sizes": [12000, 9000, 6000, 3000], "n": 750})
    OR(U, k, "honors", "A large high school (2,400 students: 700 freshmen, 650 sophomores, 550 juniors, 500 seniors) wants to estimate the mean time students spend on social media per day using a sample of 120 students.",
       [("Describe how to take a simple random sample of 120 students.", "Number students 1–2,400 using the enrollment list; use a random number generator to choose 120 different numbers; survey those students"),
        ("Describe a stratified random sample by grade with proportional allocation, giving each sample size.", "Exact shares are 35, 32.5, 27.5, 25; round to whole numbers summing to 120 (e.g., 35, 33, 27, 25) and take an SRS within each grade"),
        ("Explain one advantage of the stratified sample.", "If social media time differs by grade, stratifying ensures each grade is represented and reduces variability of the estimate"),
        ("The principal suggests sampling 4 randomly chosen homerooms instead. Name this method and give one disadvantage.", "Cluster sample; homerooms may be similar inside (e.g., same grade), so the estimate can be less precise or unrepresentative")],
       ["1 point each part; (b) needs proportional sizes summing to 120 and an SRS within each grade."], family="u2_methods_or", std=STD[k],
       check={"kind": "alloc", "sizes": [700, 650, 550, 500], "n": 120})
    SA(U, k, "honors", "Error analysis. A student describes an SRS of 50 from 1,000 club members: “Number the members 1–1,000. Put the numbers 1–1,000 into a random number generator and take the first 50 numbers it produces.”\nWhat is the flaw, and how should it be fixed?",
       "The procedure does not say to skip repeated numbers, so the same member could be chosen twice; generate numbers until 50 DIFFERENT labels are obtained (sample without replacement).",
       ["Labeling 1–1,000 is correct.", "A random number generator can repeat values.", "An SRS of 50 requires 50 different members.", "Fix: ignore repeats (or use a ‘no repeats’ setting) until 50 distinct labels are chosen."],
       family="u2_srs_error", std=STD[k])


def s03():
    k = 3
    mcs(k, "cp2", [
        ("A radio host asks listeners to call in and say whether they support a new stadium. What type of bias is most likely?",
         "Voluntary response bias", ["Undercoverage only", "Response bias from wording", "No bias; callers are random"],
         ["People choose whether to respond; those with strong (often negative) opinions are more likely to call."]),
        ("A survey of adults is conducted by calling numbers from a list of landline telephones. Which group is most likely to be underrepresented?",
         "Adults who have only cell phones", ["Adults with landlines", "Adults who answer surveys", "Adults over 65"],
         ["Adults without landlines cannot be selected — undercoverage."]),
        ("A random sample of 800 residents was mailed a survey; 210 returned it. What is the main concern?",
         "Nonresponse bias", ["Voluntary response bias in selecting the sample", "Undercoverage of the sample", "The sample size is too large"],
         ["The sample was random, but most chosen people did not respond; responders may differ from nonresponders."]),
        ("A question asks, “Do you agree that our hard-working teachers deserve a raise?” What type of bias does the wording create?",
         "Response bias from a leading question", ["Undercoverage", "Nonresponse", "Voluntary response"],
         ["Loaded phrases (“hard-working,” “deserve”) push respondents toward “yes.”"]),
        ("Students are asked by their coach, in person, whether they have ever skipped practice. The results are likely to",
         "underestimate how often students skip practice", ["overestimate how often students skip practice", "be accurate because the coach knows the students", "be accurate if the sample is large"],
         ["Students may not answer honestly to an authority figure, so “yes” is under-reported (response bias)."]),
        ("Which change would reduce bias in a survey?",
         "Selecting participants at random from a complete list of the population", ["Doubling the number of volunteers", "Surveying the people who are easiest to reach", "Asking only people with strong opinions"],
         ["Random selection from a good frame reduces selection bias; a larger biased sample is still biased."]),
    ], "u2_bias_type")
    SEL(U, k, "cp2", "Select ALL sampling methods that are likely to be biased.",
        ["Surveying the first 40 students in the lunch line", "Posting an online poll on the school website", "Interviewing shoppers at one mall on a weekday morning"],
        ["Choosing 40 students with a random number generator from the full enrollment list", "Drawing 40 names from a well-mixed hat containing every student's name"],
        ["Convenience and voluntary response methods are biased.", "Random selection from the full population is not biased in its selection."],
        family="u2_bias_sel", std=STD[k])
    SA(U, k, "cp2", "A school newspaper wants to know whether students like the new schedule. It surveys students in the library after school. Name one likely source of bias and explain how it could affect the results.",
       "Convenience sampling/undercoverage: students in the library after school (e.g., those without jobs or sports) may differ from other students, so their opinions may not represent the school.",
       ["The sample is chosen by convenience, not randomly.", "Students who are in the library after school may have different schedules or opinions.", "So the results may over- or under-state support for the schedule."],
       family="u2_bias_explain", std=STD[k])
    mcs(k, "cp1", [
        ("A random sample of households is selected from the list of homes with property tax records. Which group is undercovered?",
         "People who rent their homes or are homeless", ["Homeowners", "People who answer the survey", "People with strong opinions"],
         ["Renters and people without homes are not on a property tax list, so they cannot be selected."]),
        ("A poll asks: “Given the rising number of accidents, do you support lowering the speed limit?” Compared with a neutral question, the percent who say yes will likely be",
         "higher, because the preamble suggests a reason to support it", ["lower", "the same", "impossible to predict"],
         ["The introductory clause leads respondents toward “yes,” creating response bias."]),
        ("A survey about time spent volunteering is mailed to a random sample; busy people are least likely to return it. How will this likely affect the estimate of average volunteering time?",
         "It will likely be overestimated, if people with more free time both volunteer more and respond more.", ["It will be underestimated.", "No effect, because the sample was random.", "It will be exact if the response rate is above 20%."],
         ["Nonresponse bias: responders differ systematically from nonresponders.", "Here responders likely have more free time, which is related to volunteering."]),
        ("Which statement about bias and sample size is correct?",
         "A larger sample reduces variability but does not reduce bias.", ["A larger sample removes bias.", "Bias and variability are the same thing.", "Small samples are never biased."],
         ["Bias is systematic error in the method; more data from a biased method just gives a more precise wrong answer."]),
    ], "u2_bias_cp1")
    SA(U, k, "cp1", "A website asks visitors, “Should the city ban plastic bags?” Of 3,400 votes, 78% say no. Name the type of bias, state the likely direction, and explain.",
       "Voluntary response bias; the 78% likely overstates opposition because people who strongly object to a ban are most motivated to vote.",
       ["Respondents chose themselves (voluntary response).", "People with strong feelings, often negative ones, are more likely to respond.", "The percent opposed is likely too high for the whole city."],
       family="u2_bias_direction", std=STD[k])
    SEL(U, k, "cp1", "A random sample of students is asked in front of classmates, “Have you ever cheated on a test?” Select ALL correct statements.",
        ["The question invites response bias.", "The proportion answering “yes” likely underestimates the true proportion.", "Anonymous written responses would likely reduce the bias."],
        ["The sample is biased because it was chosen randomly.", "A larger sample asked the same way would remove the bias."],
        ["Sensitive questions asked publicly lead to dishonest answers (response bias, usually toward “no”).", "Anonymity reduces this; more respondents do not."],
        family="u2_response_bias_sel", std=STD[k])
    mcs(k, "honors", [
        ("Two polls on a ballot measure: Poll A — random sample of 600 likely voters, response rate 62%. Poll B — online opt-in panel of 12,000 volunteers. Which is likely more trustworthy, and why?",
         "Poll A, because random selection and a reasonable response rate reduce bias; Poll B's size cannot correct self-selection.",
         ["Poll B, because it has 20 times as many people.", "Neither can be trusted at all.", "Poll A, because smaller samples always have less bias."],
         ["Size reduces variability, not bias.", "Self-selected panels can be biased no matter how large."]),
        ("A random sample of 1,000 adults is asked about their income. Many high-income adults decline to answer. How will this affect the estimated mean income, and what type of bias is it?",
         "Underestimate; nonresponse bias", ["Overestimate; undercoverage", "Underestimate; voluntary response bias", "No effect; the sample was random"],
         ["The selected sample is random, but nonresponse is related to the variable (income).", "Missing many high values pulls the mean down."]),
        ("Which change reduces undercoverage in a phone survey of all adults in a state?",
         "Using random-digit dialing of both landline and cell phone numbers", ["Calling more landline numbers", "Calling only during business hours", "Offering a prize to those who answer"],
         ["Including cell numbers adds people who could not be reached before."]),
        ("A television station reports that 70% of 9,000 viewers who texted in support a new law. A random-sample poll of 900 adults finds 48% support. Which estimate is more trustworthy?",
         "The 48% from the random sample, because the text-in results come from a voluntary response sample", ["The 70%, because 9,000 is a larger sample", "Both are equally trustworthy", "Neither, because they disagree"],
         ["A large voluntary response sample is still biased; random selection is what makes the poll representative."]),
    ], "u2_bias_honors")
    OR(U, k, "honors", "A city council member wants to know how residents feel about building a new skate park. She considers three plans:\nPlan 1: Post a poll on the council's social media page.\nPlan 2: Interview people at the existing skate park on Saturday.\nPlan 3: Mail a survey to an SRS of 800 addresses from the city's address list.",
       [("Identify the main source of bias in Plan 1 and its likely direction.", "Voluntary response bias; people with strong opinions (likely skateboarders or strong opponents) respond, so results may be distorted toward extreme views"),
        ("Identify the main source of bias in Plan 2 and its likely direction.", "Convenience sample/undercoverage; park users likely support a new park, so support would be overestimated"),
        ("Name one possible bias in Plan 3 and how to reduce it.", "Nonresponse; follow up with nonresponders by phone or a second mailing (or undercoverage of residents without a listed address)"),
        ("Which plan is best, and why?", "Plan 3, because random selection from a list of the population avoids self-selection and convenience bias")],
       ["1 point each part; direction of bias required in (a) and (b)."], family="u2_bias_or", std=STD[k])
    SA(U, k, "honors", "Rewrite this survey question to remove response bias, and explain what made it biased: “Don't you think the outdated library hours should be extended?”",
       "Neutral version: “Do you favor or oppose extending the library's hours?” The original is leading (“Don't you think”) and loaded (“outdated”).",
       ["“Don't you think” invites agreement.", "“Outdated” signals the expected answer.", "A neutral question names both options and avoids loaded words.", "The neutral version: “Do you favor or oppose extending the library's hours?”"],
       family="u2_reword", std=STD[k])


def s04():
    k = 4
    mcs(k, "cp2", [
        ("Researchers record the diets of 5,000 adults for ten years and compare heart disease rates for those who ate fish often and those who did not. This is",
         "an observational study", ["an experiment", "a census", "a matched pairs experiment"],
         ["The researchers did not assign diets; they observed what people chose."]),
        ("A teacher randomly assigns half of her students to use flashcards and half to use a review game, then compares quiz scores. This is",
         "an experiment", ["an observational study", "a sample survey", "a census"],
         ["The teacher imposed the treatments (flashcards or game), so it is an experiment."]),
        ("What is the main difference between an observational study and an experiment?",
         "In an experiment, the researcher deliberately imposes treatments; in an observational study, the researcher only observes.",
         ["Experiments use larger samples.", "Observational studies always use random sampling.", "Experiments can only be done in laboratories."],
         ["The defining feature of an experiment is imposing treatments."]),
        ("A study finds that students who play a musical instrument have higher math scores than students who do not. Which conclusion is justified?",
         "There is an association, but music has not been shown to cause higher scores.", ["Playing music causes higher math scores.", "Higher math scores cause students to play music.", "There is no relationship."],
         ["This is observational; other differences between the groups may explain the association."]),
        ("Why is an experiment the only way to show cause and effect convincingly?",
         "Random assignment makes the groups similar except for the treatment, so differences in the response can be attributed to the treatment.",
         ["Experiments always have more subjects.", "Experiments do not need a response variable.", "Observational studies never find associations."],
         ["Random assignment balances other variables across groups."]),
        ("A researcher measures the number of hours students sleep and their reaction times, without changing anything about their routines. This is",
         "an observational study", ["an experiment", "a block design", "a placebo-controlled study"],
         ["Nothing was imposed, so it is observational."]),
    ], "u2_obs_vs_exp")
    SEL(U, k, "cp2", "Select ALL studies that are experiments.",
        ["Volunteers are randomly assigned to sleep 6 or 8 hours, and their reaction times are measured.", "Tomato plants are randomly assigned to two fertilizers, and their yields are compared."],
        ["Students report how many hours they sleep, and their GPAs are compared.", "Records of 1,000 patients are reviewed to compare smokers and nonsmokers."],
        ["In experiments the researchers impose treatments (sleep amount, fertilizer).", "Self-reported or record-based comparisons are observational."],
        family="u2_exp_sel", std=STD[k])
    SA(U, k, "cp2", "A researcher compares the blood pressure of people who drink coffee daily with people who do not, using medical records. Is this an observational study or an experiment? Explain in one sentence.",
       "Observational study, because the researcher did not assign coffee drinking; the people chose it themselves.",
       ["Ask: did the researcher impose a treatment?", "No — coffee habits were already chosen by the subjects, so it is observational."],
       family="u2_obs_vs_exp_sa", std=STD[k])
    mcs(k, "cp1", [
        ("Researchers want to know whether smoking during pregnancy affects birth weight. Why must they use an observational study?",
         "It would be unethical to assign pregnant women to smoke.", ["Experiments cannot measure birth weight.", "Observational studies show causation better.", "There are not enough pregnant women."],
         ["When a treatment is harmful, assigning it would be unethical, so researchers observe instead."]),
        ("An observational study finds that people who take vitamin D supplements have fewer colds. A lurking variable that could explain this is",
         "people who take supplements may also exercise, eat better, or have better health habits", ["the number of colds", "vitamin D", "the sample size"],
         ["A lurking variable is related to both the explanatory (supplements) and the response (colds)."]),
        ("A study follows 2,000 teenagers for 5 years, recording screen time each year and later measuring sleep quality. What kind of study is this?",
         "A prospective observational study", ["A retrospective observational study", "A randomized experiment", "A matched pairs experiment"],
         ["Subjects are followed forward in time without assigning treatments — prospective observational study."]),
        ("A hospital examines past records to compare outcomes of patients who had surgery A with those who had surgery B. This is",
         "a retrospective observational study", ["a prospective observational study", "an experiment", "a census"],
         ["Looking back at existing records is retrospective; doctors and patients chose the surgeries."]),
    ], "u2_obs_cp1")
    SA(U, k, "cp1", "A school wants to know if a new homework app improves grades. Describe how the study could be done as an observational study and as an experiment, and say which one could establish causation.",
       "Observational: compare grades of students who chose to use the app with those who did not. Experiment: randomly assign students to use the app or not, then compare grades. Only the experiment can establish causation.",
       ["Observational: no assignment; students self-select.", "Experiment: random assignment of app use.", "Self-selection could confound the observational comparison (e.g., motivated students choose the app).", "Random assignment balances such variables, so only the experiment shows cause and effect."],
       family="u2_obs_exp_design", std=STD[k])
    SEL(U, k, "cp1", "An observational study finds that students who eat breakfast have higher GPAs. Select ALL valid conclusions or critiques.",
        ["The study shows an association between eating breakfast and GPA.", "Family income could be a lurking variable related to both breakfast and GPA."],
        ["The study proves breakfast causes higher GPAs.", "Because the study is observational, the association cannot be real."],
        ["Observational studies can show associations but not causation.", "Lurking variables such as income or sleep habits may explain the association."],
        family="u2_obs_sel", std=STD[k])
    mcs(k, "honors", [
        ("A study of 100,000 adults finds that those who use a standing desk have lower rates of back pain. Which additional evidence would most strengthen a causal claim?",
         "A randomized experiment assigning adults to standing or sitting desks showing the same difference", ["A larger observational study of 1,000,000 adults", "Testimonials from standing-desk users", "A higher correlation in the same observational data"],
         ["Only random assignment removes confounding from self-selection; more observational data cannot."]),
        ("Which situation makes an observational study the best choice?",
         "Studying whether living near a highway is associated with childhood asthma", ["Testing whether a new fertilizer increases corn yield", "Comparing two teaching methods in randomly assigned classes", "Testing whether a cough syrup reduces coughing"],
         ["You cannot ethically or practically assign children to live near highways; the others can be experiments."]),
        ("In an observational study, researchers compare people who chose to buy organic food with those who did not, and they control for income by comparing within income groups. Why might confounding still remain?",
         "Other variables besides income (such as diet, exercise, or health awareness) may still differ between the groups.",
         ["Controlling for one variable removes all confounding.", "Organic food has no effect.", "Income cannot be a confounding variable."],
         ["Statistical adjustment handles only the variables measured; unmeasured lurking variables can remain."]),
    ], "u2_obs_honors")
    OR(U, k, "honors", "A news article states: “A study of 3,500 middle schoolers found that those who play competitive sports have 15% higher test scores. Parents should sign their kids up for sports to boost grades.”",
       [("Was this study likely an observational study or an experiment? Explain.", "Observational; students (or families) chose whether to play sports"),
        ("Identify a lurking variable and explain how it could produce the association.", "Family income or parental involvement: it can make both sports participation and higher scores more likely"),
        ("Is the article's recommendation justified? Explain.", "No; an association from an observational study does not show that sports cause higher scores"),
        ("Describe an experiment that could test whether sports participation causes higher scores, and one practical obstacle.", "Randomly assign willing students to a sports program or a control activity for a semester and compare score changes; obstacle: students/families may not comply with assigned activities")],
       ["1 point each part; (d) requires random assignment and a comparison."], family="u2_obs_or", std=STD[k])
    SA(U, k, "honors", "Explain the difference between an explanatory variable and a confounding variable, using this example: an observational study finds that cities with more police officers have more crimes.",
       "Explanatory variable: number of police officers. A confounding variable such as city population is related to both police numbers and crime counts, so its effect cannot be separated from that of police.",
       ["The explanatory variable is the one we think may explain the response (police officers).", "Population size affects both the number of officers and the number of crimes.",
        "Because population changes with police numbers, its effect is mixed (confounded) with any effect of police.", "Comparing crime rates per resident would reduce this problem."],
       family="u2_confound_explain", std=STD[k])


def s05():
    k = 5
    mcs(k, "cp2", [
        ("In an experiment, the specific conditions applied to the experimental units are called",
         "treatments", ["responses", "lurking variables", "samples"], ["Treatments are the conditions imposed (combinations of factor levels)."]),
        ("A researcher tests whether listening to music while studying affects test scores. Students are randomly assigned to study with music or in silence. What is the response variable?",
         "Test score", ["Music or silence", "The students", "Study time"], ["The response is the outcome measured to compare treatments."]),
        ("In the experiment where students are randomly assigned to study with music or in silence, what is the purpose of the silence group?",
         "It is a control group that provides a baseline for comparison.", ["It gives the students a break.", "It doubles the sample size.", "It prevents the placebo effect."],
         ["A control group lets us compare and separate the treatment effect from other influences."]),
        ("Why should subjects be randomly assigned to treatments instead of letting them choose?",
         "Random assignment creates roughly equivalent groups, so differences in the response can be attributed to the treatments.", ["It guarantees the treatment works.", "It makes the experiment shorter.", "It makes the sample random."],
         ["Self-selection can make groups differ in many ways; randomization balances those differences."]),
    ], "u2_exp_vocab")
    SA(U, k, "cp2", "An experiment tests 3 brands of paper towels (A, B, C) at 2 water temperatures (cold, hot). How many treatments are there? List them.",
       "6 treatments: A-cold, A-hot, B-cold, B-hot, C-cold, C-hot",
       ["Factor 1 (brand) has 3 levels; factor 2 (temperature) has 2 levels.", "Treatments are all combinations: 3 × 2 = 6.", "List: A-cold, A-hot, B-cold, B-hot, C-cold, C-hot.", "Each treatment is one brand used at one temperature."],
       family="u2_treatment_count", std=STD[k], check={"kind": "count_product", "levels": [3, 2]})
    SA(U, k, "cp2", "A gardener tests 4 amounts of fertilizer on tomato plants and uses 5 plants for each amount. How many plants are needed?",
       "20",
       ["There is 1 factor (fertilizer amount) with 4 levels, so 4 treatments.", "Each treatment is replicated on 5 plants.", "Total plants = 4 × 5 = 20.", "Randomly assign the 20 plants so that 5 receive each amount."],
       family="u2_units_needed", std=STD[k], check={"kind": "count_product", "levels": [4], "reps": 5})
    SA(U, k, "cp2", "Describe how to randomly assign 24 volunteers to two groups of 12 for a sleep experiment, using slips of paper.",
       "Write each volunteer's name on an identical slip, mix them in a container, and draw 12 slips; those 12 get treatment 1 and the remaining 12 get treatment 2.",
       ["Use identical slips so each name is equally likely to be drawn.", "Mix thoroughly.", "The first 12 names drawn form group 1; the rest form group 2."],
       family="u2_random_assign_sa", std=STD[k])
    mcs(k, "cp1", [
        ("An experiment studies the effect of caffeine dose (0 mg, 50 mg, 100 mg) and time of day (morning, evening) on reaction time. Identify the factors.",
         "Caffeine dose and time of day", ["Reaction time and caffeine dose", "The 6 treatments", "The subjects"],
         ["Factors are the explanatory variables manipulated; reaction time is the response."]),
        ("An experiment compares 2 brands of batteries, with 1 battery of each brand tested. Brand A lasts longer. Why is this weak evidence?",
         "With only one unit per treatment (no replication), the difference could easily be due to chance variation between individual batteries.", ["There is no response variable.", "Batteries cannot be randomly assigned.", "Two treatments are too many."],
         ["Replication on many units lets us separate a real treatment effect from unit-to-unit variation."]),
    ], "u2_exp_cp1")
    MC(U, k, "cp1", "An experiment tests 3 levels of light and 2 levels of water on plant growth, with 4 plants per treatment. How many plants are needed?",
       "24", ["12", "9", "20"], ["Treatments = 3 × 2 = 6.", "Plants = 6 × 4 = 24."], family="u2_units_mc", std=STD[k],
       check={"kind": "count_product", "levels": [3, 2], "reps": 4})
    SA(U, k, "cp1", "An experiment compares 3 study methods across 4 lengths of study session (15, 30, 45, 60 minutes), with 6 students per treatment. How many treatments and how many students are needed?",
       "12 treatments; 72 students",
       ["Factor 1 has 3 levels and factor 2 has 4 levels.", "Treatments = 3 × 4 = 12.", "Students = 12 treatments × 6 per treatment = 72.", "Students would be randomly assigned so 6 receive each treatment."],
       family="u2_treatment_units", std=STD[k], check={"kind": "count_product", "levels": [3, 4], "reps": 6})
    SEL(U, k, "cp1", "Select ALL principles of a well-designed experiment.",
        ["Comparison of two or more treatments", "Random assignment of units to treatments", "Replication on enough units in each group", "Control of other variables that might affect the response"],
        ["Letting subjects choose their treatment", "Using a single experimental unit per treatment"],
        ["The four principles: comparison, random assignment, control, and replication."], family="u2_principles_sel", std=STD[k])
    mcs(k, "honors", [
        ("A researcher randomly assigns 40 rats to two diets but keeps all rats on Diet A in a warm room and all on Diet B in a cool room. What is the problem?",
         "Room temperature is confounded with diet, so any difference cannot be attributed to diet alone.", ["There is no control group.", "There is too much replication.", "Rats cannot be randomly assigned."],
         ["Every other condition should be the same for all groups; here temperature varies with treatment."]),
        ("Why might a researcher choose experimental units that are very similar (for example, plants of the same variety and age)?",
         "It reduces variability in the response, making treatment differences easier to detect — but it limits the scope of conclusions.",
         ["It removes the need for random assignment.", "It allows conclusions about all plants.", "It eliminates bias completely."],
         ["Homogeneous units reduce noise; the trade-off is narrower generalization."]),
        ("Why are treatment effects judged by comparing groups rather than by measuring a single group before and after treatment?",
         "Without a comparison group, changes could be due to time, the placebo effect, or other factors rather than the treatment.",
         ["Comparison is required only when samples are large.", "Before/after measurements are impossible.", "A single group always shows no change."],
         ["Comparison separates the treatment effect from other influences acting over the same period."]),
    ], "u2_exp_honors")
    OR(U, k, "honors", "A sports scientist wants to know whether a new sports drink improves endurance. She has 60 volunteer runners who will run on a treadmill until exhaustion.",
       [("Identify the explanatory variable, response variable, and experimental units.", "Explanatory: drink (new sports drink vs. comparison drink); response: time until exhaustion; units: the 60 runners"),
        ("Describe how to randomly assign the runners to two groups of 30.", "Number runners 1–60; use a random number generator to choose 30 different numbers for the new drink; the other 30 get the comparison drink"),
        ("What should the comparison group drink, and why?", "A drink that looks and tastes the same but lacks the active ingredients (a placebo), so expectations are the same in both groups"),
        ("Name two variables that should be kept the same for all runners and explain why.", "Treadmill speed/incline and time since last meal (or room temperature); keeping them constant prevents them from affecting the response differently in the groups")],
       ["1 point each part."], family="u2_exp_design_or", std=STD[k])
    SA(U, k, "honors", "Error analysis. A student designs an experiment: “I will let each of the 40 volunteers choose either the new or old shampoo, then compare ratings. This is randomized because the volunteers were chosen at random from the school.” Identify two problems with the reasoning.",
       "Letting volunteers choose is not random assignment (self-selection can confound); random selection of volunteers is not the same as random assignment to treatments.",
       ["Problem 1: subjects choose their own treatment, so groups may differ systematically.", "Problem 2: random sampling decides who is studied, not who receives which treatment.",
        "Fix: randomly assign 20 volunteers to each shampoo.", "Random assignment is what supports cause-and-effect conclusions."],
       family="u2_assignment_error", std=STD[k])
    SA(U, k, "honors", "A three-factor experiment uses 2 types of soil, 3 watering schedules, and 2 light levels. Each treatment is applied to 3 plants. How many plants are needed?",
       "36",
       ["Treatments = 2 × 3 × 2 = 12.", "Replication: 3 plants per treatment.", "Plants = 12 × 3 = 36.", "Each plant must be randomly assigned to exactly one of the 12 treatments."],
       family="u2_three_factor", std=STD[k], check={"kind": "count_product", "levels": [2, 3, 2], "reps": 3})


def s06():
    k = 6
    mcs(k, "cp2", [
        ("A placebo is",
         "a fake treatment that looks like the real treatment but has no active ingredient", ["a treatment that always works", "a group that receives no attention", "a variable that causes confounding"],
         ["Placebos let researchers account for the effect of simply receiving a treatment."]),
        ("The placebo effect is",
         "improvement in subjects' responses because they believe they are receiving a treatment", ["the effect of a real drug", "a type of sampling bias", "the difference between two treatments"],
         ["Belief alone can change responses such as pain or mood."]),
        ("In a single-blind experiment,",
         "either the subjects or the people evaluating them do not know which treatment was given", ["no one knows the treatments", "the researchers do not know the results", "subjects receive no treatment"],
         ["Single-blind: one of those groups is unaware; double-blind: both."]),
        ("In a double-blind experiment,",
         "neither the subjects nor those who measure the response know which treatment each subject received", ["two placebos are used", "subjects are blindfolded", "the experiment is repeated twice"],
         ["Double-blinding prevents expectations from affecting responses or measurements."]),
        ("Two variables are confounded when",
         "their effects on the response cannot be distinguished from each other", ["they are both categorical", "they have the same mean", "one is the response variable"],
         ["Confounding means the effects are mixed together."]),
        ("A coach tries a new warm-up with the varsity team and the old warm-up with the junior varsity team. Varsity players get fewer injuries. What is confounded with the warm-up?",
         "Team level (varsity players differ in age, fitness, and experience)", ["The number of injuries", "The warm-up routine", "Nothing; the comparison is fair"],
         ["Each warm-up was used with a different kind of team, so team differences are mixed with the warm-up effect."]),
    ], "u2_placebo_blind")
    SEL(U, k, "cp2", "Select ALL situations where blinding the subjects is possible.",
        ["Comparing a pain pill to an identical-looking sugar pill", "Comparing two flavors of cough syrup in identical bottles"],
        ["Comparing surgery to no surgery", "Comparing running outdoors to swimming"],
        ["Subjects can be blinded only when treatments can be made to look and feel the same."], family="u2_blind_sel", std=STD[k])
    SA(U, k, "cp2", "In a study of a new acne cream, why should the doctor who rates each patient's skin not know which cream the patient used?",
       "So the doctor's expectations cannot influence the ratings; this is blinding the evaluator.",
       ["A doctor who knows the treatment might rate the new cream more favorably.", "Blinding the evaluator prevents that bias in measuring the response."],
       family="u2_blind_evaluator", std=STD[k])
    MC(U, k, "cp2", "A teacher tests a new vocabulary game in her first-period class and uses the old worksheet in her last-period class. First period scores higher. Which statement is correct?",
       "Class period is confounded with the teaching method, so the game's effect cannot be isolated.", ["The game clearly works better.", "The worksheet class is a placebo group.", "The experiment is double-blind."],
       ["Each method was used with a different class at a different time of day; those differences are mixed with the method's effect."],
       family="u2_confound_class", std=STD[k])
    mcs(k, "cp1", [
        ("A new headache medicine is compared with a placebo. 64% of the medicine group and 41% of the placebo group report relief. What does the placebo group's 41% show?",
         "A substantial placebo effect; without a placebo group, the medicine's effect would be overstated.", ["The placebo works as well as the medicine.", "The experiment is invalid.", "41% of headaches go away because of the medicine."],
         ["Comparing to a placebo isolates the effect of the active ingredient (64% vs 41%)."]),
        ("In an experiment comparing two reading programs, all students in Program A meet in the morning and all students in Program B meet in the afternoon. Which statement is correct?",
         "Time of day is confounded with the reading program.", ["Time of day is a placebo.", "The experiment is double-blind.", "Time of day is the response variable."],
         ["Each program is tied to a time of day, so their effects cannot be separated."]),
        ("Why is it often impossible to blind subjects in an experiment comparing physical therapy with surgery?",
         "Subjects obviously know whether they had surgery, so they cannot be unaware of their treatment.", ["Surgery is a placebo.", "Physical therapy is a confounding variable.", "Blinding is never used in medicine."],
         ["Blinding requires treatments that cannot be told apart; evaluators may still be blinded."]),
        ("In an experiment on a new reading program, the teachers who score the final reading test know which students used the new program. What problem can this cause?",
         "The teachers' expectations could bias the scores (lack of evaluator blinding).", ["It causes undercoverage.", "It makes the experiment double-blind.", "It creates a placebo effect in the teachers."],
         ["Evaluators who know the treatment might score favored students more generously."]),
    ], "u2_confound_cp1")
    SA(U, k, "cp1", "A study gives a new vitamin to volunteers who ask for it and compares their energy levels with volunteers who did not ask. Explain two problems with this design related to confounding and the placebo effect.",
       "Self-selection: volunteers who ask may already be more health-conscious (confounding). Placebo: those who knowingly take the vitamin may report more energy because they expect to.",
       ["Subjects chose their own treatment, so they may differ in other ways.", "Those ways (health habits) affect energy and are confounded with the vitamin.",
        "The vitamin group knows it is treated, so expectations may raise reported energy.", "Fix: random assignment and an identical placebo, double-blind."],
       family="u2_confound_placebo_sa", std=STD[k])
    SEL(U, k, "cp1", "A double-blind, placebo-controlled experiment tests a sleep aid. Select ALL true statements.",
        ["Subjects do not know whether they received the sleep aid or the placebo.", "The researchers who score sleep quality do not know which treatment subjects received.", "The placebo group helps measure the placebo effect."],
        ["The placebo group receives a smaller dose of the sleep aid.", "Double-blinding eliminates the need for random assignment."],
        ["Double-blind = subjects and evaluators unaware; a placebo has no active ingredient; randomization is still required."],
        family="u2_double_blind_sel", std=STD[k])
    mcs(k, "honors", [
        ("In a weight-loss study, subjects on a new diet also receive weekly coaching, while control subjects receive no contact. The diet group loses more weight. Why is the conclusion “the diet works” questionable?",
         "Coaching (attention) is confounded with the diet; the control group should receive equal contact.", ["The diet group is too large.", "Weight loss cannot be measured.", "Coaching is a placebo, so it has no effect."],
         ["Any extra condition given only to one group is confounded with the treatment."]),
        ("A placebo-controlled trial finds no difference between a drug and the placebo, but both groups improved a lot. Which conclusion is most reasonable?",
         "The improvement may come from the placebo effect or natural recovery; the drug shows no evidence of an added benefit.", ["The drug works because the drug group improved.", "The placebo is an effective drug.", "The study should have had no control group."],
         ["Only the difference between groups measures the drug's effect."]),
        ("Why is the placebo effect a concern even when the response is an objective measurement such as blood pressure?",
         "Expectations can change behavior and physiology (e.g., stress, diet, adherence), and evaluators may take readings differently if they know the treatment.",
         ["It is not a concern for objective responses.", "Blood pressure cannot change.", "Placebos raise blood pressure by definition."],
         ["Both subject and evaluator expectations can affect even measured outcomes, so blinding still matters."]),
    ], "u2_confound_honors")
    OR(U, k, "honors", "A company wants to test whether its new memory supplement improves recall. It recruits 80 adults.",
       [("Explain why a placebo is needed.", "Subjects who believe they are taking a memory supplement may perform better from expectation alone; a placebo group experiences the same expectation"),
        ("Describe how to make the experiment double-blind.", "Supplement and placebo pills look identical and are coded; neither subjects nor the staff giving and scoring the recall test know the codes"),
        ("The company proposes giving the supplement to subjects who say their memory is poor and the placebo to the others. Explain the problem.", "Initial memory is confounded with treatment; groups would differ before treatment, so differences can't be attributed to the supplement"),
        ("Describe a better way to assign treatments.", "Randomly assign 40 subjects to each group (or block by self-reported memory and randomize within blocks)")],
       ["1 point each part."], family="u2_blind_or", std=STD[k])
    SA(U, k, "honors", "Error analysis. A student writes: “Our experiment is double-blind because the subjects did not know which treatment they got and the treatments were randomly assigned.” What is missing from the student's reasoning?",
       "Double-blind also requires that the people who interact with subjects and measure the response do not know the treatments; random assignment is a separate principle.",
       ["Subject blinding alone makes the study single-blind.", "Double-blind needs evaluator/administrator blinding too.", "Random assignment controls confounding but is not blinding.", "Correct statement: neither subjects nor evaluators know the treatment assignments."],
       family="u2_blind_error", std=STD[k])


def s07():
    k = 7
    mcs(k, "cp2", [
        ("In a completely randomized design,",
         "all experimental units are randomly assigned to the treatments", ["units are first grouped into blocks", "each unit receives every treatment", "units choose their treatments"],
         ["Completely randomized: assignment of all units to treatments is entirely random."]),
        ("A block in an experimental design is",
         "a group of experimental units that are similar in a way expected to affect the response", ["a treatment", "a placebo group", "a group of researchers"],
         ["Blocks group similar units; treatments are randomized within each block."]),
        ("Each of 20 twin pairs is split so that one twin gets a new tutoring method and the other gets the standard method (decided by a coin flip). This is",
         "a matched pairs design", ["a completely randomized design", "an observational study", "a cluster sample"],
         ["Similar units (twins) are paired, and treatments are randomly assigned within each pair."]),
        ("Why might an experimenter block by gender when comparing two exercise programs?",
         "If men and women respond differently, blocking separates that variation so the program comparison is clearer.", ["To make the groups larger", "Because gender is a treatment", "To avoid random assignment"],
         ["Blocking accounts for a variable known to affect the response."]),
        ("Each student tries both a red pen and a blue pen (order decided by coin flip) and rates how well each writes. This is",
         "a matched pairs design with each subject receiving both treatments", ["a completely randomized design", "a randomized block design with two blocks of students", "a convenience sample"],
         ["Each subject serves as his or her own pair; randomizing order prevents order effects."]),
    ], "u2_design_id")
    SEL(U, k, "cp2", "Select ALL true statements about randomized block designs.",
        ["Random assignment happens separately within each block.", "Blocks are formed from units that are similar in a way that affects the response."],
        ["Blocks are the same as treatments.", "Each block receives only one treatment."],
        ["In a block design, all treatments are randomly assigned within every block."], family="u2_block_sel", std=STD[k])
    SA(U, k, "cp2", "A teacher has 30 students: 18 who take the bus and 12 who walk. She wants to compare two homework formats and thinks commuting may affect homework time. Describe a randomized block design.",
       "Block by commute: within the 18 bus riders, randomly assign 9 to each format; within the 12 walkers, randomly assign 6 to each format; compare formats within each block.",
       ["Form blocks: bus riders and walkers.", "Randomly assign formats within each block (9/9 and 6/6).", "Compare the formats within blocks, then combine the results."],
       family="u2_block_describe", std=STD[k])
    SA(U, k, "cp2", "Error analysis. A student says, “In a matched pairs design, I give the new treatment to the first person in each pair and the old treatment to the second person.” What is the error and how should it be fixed?",
       "Treatments should be randomly assigned within each pair (e.g., flip a coin), not assigned by position in the pair.",
       ["Assigning by position is not random and could be confounded with how pairs were listed.", "Flip a coin for each pair to decide which member gets the new treatment."],
       family="u2_pairs_error", std=STD[k])
    mcs(k, "cp1", [
        ("A farmer compares two corn varieties on 20 plots. Plots on the hillside are drier than plots in the valley. What design is best?",
         "Block by location (hill vs valley) and randomly assign varieties within each block.", ["Completely randomized design ignoring location", "Plant variety A on the hill and B in the valley", "Use only the valley plots and do not randomize"],
         ["Moisture affects yield, so grouping plots by location reduces variability in the comparison."]),
        ("What is the main advantage of a matched pairs design compared with a completely randomized design?",
         "It reduces the effect of differences between subjects, so a treatment effect is easier to detect.", ["It requires no random assignment.", "It uses more subjects.", "It allows conclusions about all populations."],
         ["Comparing within pairs (or within a subject) removes much of the subject-to-subject variation."]),
        ("In a taste test, each subject tastes Brand A and Brand B. Why should the order be randomized?",
         "To prevent order effects (for example, the second sample tasting better or worse just because it is second) from being confounded with brand.", ["To make it double-blind", "So each subject tastes only one brand", "To create blocks"],
         ["If everyone tasted A first, brand would be confounded with tasting order."]),
    ], "u2_design_cp1")
    SA(U, k, "cp1", "Explain the difference between blocking and stratifying.",
       "Stratifying groups the population before random sampling (in surveys); blocking groups experimental units before random assignment of treatments (in experiments).",
       ["Both group similar individuals.", "Strata are used to select a sample.", "Blocks are used to assign treatments.", "Each reduces variability caused by the grouping variable."],
       family="u2_block_vs_strata", std=STD[k])
    SEL(U, k, "cp1", "Select ALL experiments that use matched pairs.",
        ["Each patient's blood pressure is measured on drug A and on drug B (random order, with a washout period).", "Pairs of students with similar GPAs are formed, and a coin flip decides which student in each pair gets tutoring."],
        ["100 students are randomly split into two groups of 50.", "Students are grouped by grade, and treatments are randomized within each grade with 40 students per grade."],
        ["Matched pairs: two treatments compared within each pair or subject.", "Grade-level grouping with many students per group is a block design, not pairs."],
        family="u2_pairs_sel", std=STD[k])
    mcs(k, "honors", [
        ("In a block design comparing two fertilizers, the blocks are soil types. If soil type turns out to have NO effect on yield, what is lost by blocking?",
         "Very little; the comparison is still valid, though blocking provided no reduction in variability.", ["The experiment becomes biased.", "Random assignment is no longer valid.", "The treatments are now confounded with soil."],
         ["Blocking on an unhelpful variable does not create bias; it simply doesn't help precision."]),
        ("Which is the strongest reason to use a matched pairs design with each subject receiving both treatments?",
         "Subjects vary a lot in their baseline response, and each subject can be measured under both treatments without carryover effects.", ["Subjects are identical to each other.", "Only one treatment exists.", "The response variable is categorical."],
         ["Using each subject as his or her own control removes between-subject variation, provided carryover is avoided."]),
        ("An experiment compares 3 treatments using 4 blocks of 6 units each. How should the randomization be done?",
         "Within each block, randomly assign 2 of the 6 units to each of the 3 treatments.", ["Randomly assign the 4 blocks to the 3 treatments.", "Assign each block entirely to one treatment.", "Randomly assign all 24 units ignoring blocks."],
         ["In a block design, every treatment appears in every block, with randomization within the block."]),
    ], "u2_design_honors")
    OR(U, k, "honors", "A company wants to compare two keyboard layouts (standard and new) on typing speed. It has 24 employees whose typing speeds vary a lot.",
       [("Describe a completely randomized design.", "Randomly assign 12 employees to each layout (e.g., draw 12 names from a hat for the new layout); measure typing speed after a practice period and compare means"),
        ("Describe a matched pairs design in which each employee uses both layouts.", "Each employee types on both layouts; a coin flip decides which layout comes first; compare each employee's two speeds"),
        ("Explain why the matched pairs design is likely better here.", "Because typing ability varies a lot, comparing within each employee removes that variation and makes a layout difference easier to detect"),
        ("Identify one possible problem with the matched pairs design and how to address it.", "Learning/fatigue (order) effects; randomize the order and allow rest or practice between sessions")],
       ["1 point each part."], family="u2_design_or", std=STD[k])


def s08():
    k = 8
    mcs(k, "cp2", [
        ("A study randomly selected 1,200 adults from a state and asked about exercise. To which group can the results be generalized?",
         "All adults in that state", ["All adults in the country", "Only the 1,200 adults", "All people of any age in the state"],
         ["Random selection allows generalization to the population that was sampled."]),
        ("An experiment randomly assigned volunteers to two diets. What kind of conclusion does random assignment allow?",
         "A cause-and-effect conclusion about the diets for subjects like these volunteers", ["A conclusion about all people in the country", "Only a description of the volunteers' opinions", "No conclusion at all"],
         ["Random assignment supports causation; generalizing beyond the volunteers needs random selection."]),
        ("Which kind of study can show that one variable causes changes in another?",
         "A well-designed randomized experiment", ["A large observational study", "A sample survey", "Any study with a strong correlation"],
         ["Only random assignment of treatments controls for lurking variables."]),
        ("A survey finds that people who sleep more report less stress. Which statement is justified?",
         "Sleep and stress are associated in this sample.", ["More sleep causes less stress.", "Less stress causes more sleep.", "There is no relationship."],
         ["A survey is observational; it shows association only."]),
        ("A study randomly assigns 80 volunteers to a new or old allergy medicine. What can be concluded if the new medicine works significantly better?",
         "The new medicine causes better results for people like these volunteers.", ["The new medicine works better for everyone in the country.", "Nothing, because volunteers were used.", "Only that the two medicines are associated with symptoms."],
         ["Random assignment → causation; volunteers → limited generalization."]),
    ], "u2_scope_basic")
    SEL(U, k, "cp2", "Select ALL conclusions that need random assignment to be justified.",
        ["The new teaching method causes higher test scores.", "Taking the medication reduces blood pressure."],
        ["About 40% of adults in the city own a bicycle.", "Students who play sports tend to have higher attendance."],
        ["Cause-and-effect conclusions require random assignment.", "Estimating a proportion or describing an association does not."],
        family="u2_causal_sel", std=STD[k])
    SA(U, k, "cp2", "A school randomly assigns 60 of its students to a new reading program and 60 to the old program. Can the school conclude the program caused any difference in reading scores? Can it generalize to all U.S. students? Explain both.",
       "Yes for causation (random assignment), but no for generalizing to all U.S. students (the students were not randomly selected from all U.S. students); conclusions apply to students like these.",
       ["Random assignment → cause-and-effect conclusions are justified.", "No random sample of U.S. students → results apply only to similar students (this school)."],
       family="u2_scope_sa", std=STD[k])
    SA(U, k, "cp2", "For each study type, state whether we can (1) generalize to the population and (2) conclude cause and effect.\nA: random selection, no random assignment\nB: no random selection, random assignment\nC: random selection and random assignment\nD: neither",
       "A: generalize yes, cause no; B: generalize no, cause yes; C: both yes; D: neither",
       ["Random selection → generalize to the sampled population.", "Random assignment → cause and effect.", "Apply each rule to A–D."], family="u2_scope_table", std=STD[k])
    mcs(k, "cp1", [
        ("A random sample of 500 county residents was taken, and each was randomly assigned to receive a text reminder or no reminder about recycling. Which conclusion is justified?",
         "Reminders cause a change in recycling, and the result applies to all county residents.", ["Reminders cause a change only for the 500 residents.", "Reminders are associated with recycling for all residents, but no causal claim is possible.", "No conclusion is possible."],
         ["Random selection and random assignment together support both generalization and causation."]),
        ("An experiment found a statistically significant difference between two treatments. What does “statistically significant” mean?",
         "The difference is too large to be plausibly explained by the random assignment alone.", ["The difference is large enough to be important in practice.", "The experiment had more than 30 subjects.", "Every subject benefited from the treatment."],
         ["Statistical significance means chance alone is an unlikely explanation."]),
        ("Volunteers at one gym were randomly assigned to two warm-up routines, and injuries were compared. To whom do the conclusions apply?",
         "To gym-goers similar to these volunteers", ["To all athletes in the world", "To all adults", "To no one, because volunteers were used"],
         ["Random assignment supports causation within the volunteer group; without random sampling, generalize cautiously."]),
    ], "u2_scope_cp1")
    SA(U, k, "cp1", "A study reports a statistically significant association between the number of hours teens spend on social media and anxiety scores, using a random sample of 3,000 U.S. teens. State what can and cannot be concluded.",
       "Can conclude: there is an association between social media time and anxiety among U.S. teens (random sample). Cannot conclude: that social media use causes anxiety (no random assignment).",
       ["Random sample → generalize the association to U.S. teens.", "Observational → no cause-and-effect conclusion.", "Possible lurking variables or reverse causation (anxious teens may use more social media)."],
       family="u2_scope_obs", std=STD[k])
    SEL(U, k, "cp1", "Researchers randomly assigned 200 volunteer college students to study with or without background music. Students without music scored significantly higher. Select ALL correct statements.",
        ["The data give evidence that background music causes lower scores for students like these volunteers.", "The results should be generalized beyond college volunteers only with caution."],
        ["The results prove that music lowers scores for all students everywhere.", "Because the subjects were volunteers, no causal conclusion is allowed."],
        ["Random assignment supports causation for this group; lack of random selection limits generalization."], family="u2_scope_sel", std=STD[k])
    mcs(k, "honors", [
        ("A strong association between X and Y could be due to all of the following EXCEPT:",
         "random assignment of X in a well-designed experiment showing no effect", ["X causes Y", "Y causes X (reverse causation)", "A lurking variable affects both X and Y"],
         ["Causation, reverse causation, and common response all produce associations; an experiment showing no effect would not."]),
        ("A randomized experiment on 40 rats finds that a food additive increases tumor rates. A news story says, “Additive causes cancer in humans.” What is the main problem?",
         "The results apply to rats like these; extending them to humans goes beyond the study's scope.", ["Rats were randomly assigned, so the result applies to humans.", "There was no control group.", "40 rats is too many."],
         ["Random assignment supports causation in the units studied, not in a different population or species."]),
    ], "u2_scope_honors")
    OR(U, k, "honors", "Three studies examine whether a mindfulness app reduces stress.\nStudy 1: A random sample of 800 adults reports app use and stress levels.\nStudy 2: 120 volunteers are randomly assigned to use the app or a placebo app for 8 weeks.\nStudy 3: 2,000 adults randomly selected from a state are randomly assigned to use the app or not.",
       [("Which study (or studies) can support a cause-and-effect conclusion? Explain.", "Studies 2 and 3, because they use random assignment"),
        ("Which study (or studies) allow generalization to a larger population? Name it.", "Studies 1 and 3: Study 1 to the population sampled; Study 3 to adults in that state"),
        ("Study 1 finds that app users report lower stress. Give an alternative explanation.", "Reverse causation or a lurking variable (e.g., people with less stressful lives have time to use the app)"),
        ("Which study gives the strongest evidence overall? Explain.", "Study 3: random selection and random assignment support both causation and generalization")],
       ["1 point each part."], family="u2_scope_or", std=STD[k])


def build():
    for f in (s01, s02, s03, s04, s05, s06, s07, s08):
        f()
