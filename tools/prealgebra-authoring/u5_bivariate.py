"""Unit 5 — Patterns and Bivariate Data (patterns-bivariate-data)."""
from lib import *

UNIT_ID = "patterns-bivariate-data"
ABBR = "biv"

CONTEXTS = [("hours studied", "test score", (0, 10), (40, 100), 1, 10, "pos"), ("outside temperature (°F)", "hot cocoa sold", (30, 90), (0, 60), 10, 10, "neg"),
            ("hours of TV per day", "hours of sleep", (0, 8), (4, 12), 1, 1, "neg"), ("shoe size", "spelling score", (4, 12), (0, 20), 1, 2, "none"),
            ("age of car (years)", "value ($1,000s)", (0, 12), (0, 30), 1, 5, "neg"), ("height (in.)", "arm span (in.)", (50, 75), (50, 75), 5, 5, "pos"),
            ("minutes practiced", "free throws made", (0, 60), (0, 20), 10, 2, "pos"), ("birth month", "number of pets", (1, 12), (0, 6), 1, 1, "none")]


def gen_scatter(r, kind, n=10, xr=(0, 10), yr=(0, 10)):
    """Integer data with a clear pattern of the given kind."""
    for _ in range(200):
        xs = sorted(r.sample(range(xr[0], xr[1] + 1), n)) if xr[1] - xr[0] + 1 >= n else sorted(r.randint(*xr) for _ in range(n))
        span_y = yr[1] - yr[0]
        if kind in ("pos", "neg"):
            m = span_y / max(1, (xr[1] - xr[0])) * r.uniform(0.6, 0.9) * (1 if kind == "pos" else -1)
            b = (yr[0] + span_y * 0.15) if kind == "pos" else (yr[1] - span_y * 0.15)
            ys = [round(b + m * (x - xr[0]) + r.uniform(-0.08, 0.08) * span_y) for x in xs]
        elif kind == "none":
            ys = [r.randint(yr[0] + 1, yr[1] - 1) for _ in xs]
        else:  # nonlinear (curved)
            mid = (xr[0] + xr[1]) / 2
            ys = [round(yr[0] + span_y * (0.9 - 3.2 * ((x - mid) / (xr[1] - xr[0])) ** 2) + r.uniform(-0.04, 0.04) * span_y) for x in xs]
        if all(yr[0] <= y <= yr[1] for y in ys) and len(set(zip(xs, ys))) == len(xs):
            rr = corr(xs, ys)
            if kind == "pos" and rr > 0.85 or kind == "neg" and rr < -0.85 or kind == "none" and abs(rr) < 0.2 or kind == "curve" and abs(rr) < 0.3:
                return xs, ys
    raise Reject()


def corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


def scatter_draw(xs, ys, xr, yr, xs_step, ys_step, xl, yl, line=None, labels=None, size=6.3):
    def draw_on(ax):
        data_axes(ax, (xr[0] - (xs_step if xr[0] else 0) * 0, xr[1]), yr, xs_step, ys_step, xl, yl)
        ax.scatter(xs, ys, color="#1f4e9c", s=42, zorder=5)
        if line:
            m, b = line
            ax.plot(list(xr), [float(m) * x + float(b) for x in xr], color="#b23a3a", lw=2)
        if labels:
            for (x, y, t) in labels:
                ax.annotate(t, (x, y), textcoords="offset points", xytext=(6, 6), fontsize=12, fontweight="bold")

    def draw(path):
        fig, ax = new_fig(size, size * 0.8)
        draw_on(ax)
        save(fig, path)
    draw.draw_on = draw_on
    return draw


def data_text(xs, ys, xl, yl):
    return f"{xl}: " + ", ".join(map(str, xs)) + f"; {yl}: " + ", ".join(map(str, ys))


def pick_ctx(r, kind=None):
    c = pick(r, [c for c in CONTEXTS if kind is None or c[6] == kind])
    return c


# ======================================================================= S1 Constructing scatter plots
@fam("012", mode="mc")
def s1_which_plot(r, L):
    c = pick_ctx(r)
    xs, ys = gen_scatter(r, c[6] if c[6] != "none" else "none", n=8, xr=c[2], yr=c[3])
    variants = [(xs, ys), (ys_to_xs := xs, [c[3][0] + c[3][1] - y for y in ys]), (xs, ys[::-1]), ([x for x in xs], [y + (c[3][1] - c[3][0]) // 5 if i % 2 else y for i, y in enumerate(ys)])]
    variants[3] = (xs, [min(c[3][1], y + c[5]) if i == 2 else y for i, y in enumerate(ys)])
    need(len({tuple(v[1]) for v in variants}) == 4)
    order = [0, 1, 2, 3]
    r.shuffle(order)
    good = "ABCD"[order.index(0)]
    drawers = [scatter_draw(variants[i][0], variants[i][1], c[2], c[3], c[4], c[5], c[0], c[1]) for i in order]
    return P(f"The table gives data for {len(xs)} students. {data_text(xs, ys, c[0], c[1])}. Which scatter plot shows the data?", f"Graph {good}",
             ["Plot each (x, y) pair: x from the first list, y from the second list in the same position.", f"Graph {good} matches every pair."],
             options=[(f"Graph {l}", l == good) for l in "ABCD"], chk=chk_py("scatter_match", pts=[[a, b] for a, b in zip(xs, ys)], panels=[[[a, b] for a, b in zip(*variants[i])] for i in order], show=[str(v) for v in ys]),
             diagram={"draw": panels_draw(drawers), "alt": "Four scatter plots: " + "; ".join(f"Graph {l}: points " + ", ".join(pt(a, b) for a, b in zip(*variants[i])) for l, i in zip("ABCD", order))},
             tags=["graph", "multiple-representations"], mode="mc")


@fam("012")
def s1_point_for_row(r, L):
    c = pick_ctx(r)
    xs, ys = gen_scatter(r, "pos" if c[6] == "pos" else "neg" if c[6] == "neg" else "none", n=6, xr=c[2], yr=c[3])
    k = r.randint(0, 5)
    return P(f"Data: {data_text(xs, ys, c[0], c[1])}. When this data is graphed as a scatter plot with {c[0]} on the horizontal axis, what ordered pair represents data pair number {k + 1} (counting from the left of each list)?",
             pt(xs[k], ys[k]), [f"Horizontal axis: {c[0]} = {xs[k]}. Vertical axis: {c[1]} = {ys[k]}.", f"Point {pt(xs[k], ys[k])}."],
             [pt(ys[k], xs[k]), pt(xs[k], ys[k - 1]) if ys[k - 1] != ys[k] else pt(xs[k], ys[k] + 1), pt(xs[k - 1], ys[k]) if xs[k - 1] != xs[k] else pt(xs[k] + 1, ys[k])],
             chk_py("row_point", xs=xs, ys=ys, k=k, show=[str(xs[k]), str(ys[k])]), tags=["multiple-representations"])


@fam("12")
def s1_scale(r, L):
    lo, hi = r.randint(0, 20), r.randint(150, 480)
    step = pick(r, [10, 20, 25, 50])
    ticks = math.ceil((hi - lo) / step)
    return P(f"The y-values of a data set range from {lo} to {hi}. Using a scale that starts at 0 with intervals of {step}, how many intervals are needed on the y-axis to include every value?",
             str(math.ceil(hi / step)), [f"The axis must reach at least {hi}.", f"{hi} ÷ {step} = {D(F(hi, step), 2) if F(hi, step).denominator != 1 else hi // step}, so {math.ceil(hi / step)} intervals (up to {math.ceil(hi / step) * step})."],
             [str(math.floor(hi / step)), str(ticks), str(math.ceil(hi / step) + 1)] if math.floor(hi / step) != math.ceil(hi / step) else [str(math.ceil(hi / step) + 1), str(math.ceil(hi / step) - 1), str(math.ceil((hi - lo) / step) + 2)],
             chk_py("axis_intervals", hi=hi, step=step), tags=["reasoning"])


@fam("012", mode="sa")
def s1_axes(r, L):
    pairs = [("the number of hours a candle burns", "the candle's height", "hours burned"), ("the number of pages read", "the time spent reading", "time spent reading"),
             ("a car's speed", "the distance needed to stop", "speed"), ("the number of workers", "the time to finish a job", "number of workers")]
    a, b, ans = pick(r, pairs)
    q = pick(r, ["explanatory", "horizontal"])
    if ans not in (a, b):
        ans = a
    return P(f"Kim wants to see whether {b} depends on {a}. Which variable should go on the horizontal (x) axis?", a,
             ["The variable that might explain or cause the change (the independent variable) goes on the x-axis."], [b], {"kind": "text", "accept": [a]}, tags=["reasoning"], mode="sa")


@fam("012")
def s1_error(r, L):
    c = pick_ctx(r, "pos")
    xs, ys = gen_scatter(r, "pos", n=5, xr=c[2], yr=c[3])
    k = r.randint(0, 4)
    need(xs[k] != ys[k])
    return P(f"Data: {data_text(xs, ys, c[0], c[1])}. Zoe plotted data pair number {k + 1} as {pt(ys[k], xs[k])} with {c[0]} on the x-axis. What point should she have plotted?",
             pt(xs[k], ys[k]), ["Zoe reversed the coordinates.", f"x is {c[0]} = {xs[k]}; y is {c[1]} = {ys[k]}."], [pt(ys[k], xs[k]), pt(xs[k], xs[k]), pt(ys[k], ys[k])],
             chk_py("row_point", xs=xs, ys=ys, k=k), tags=["error-analysis", "misconception"])


@fam("012")
def s1_select(r, L):
    c = pick_ctx(r)
    xs, ys = gen_scatter(r, "none", n=5, xr=c[2], yr=c[3])
    opts = [(pt(x, y), True) for x, y in zip(xs[:3], ys[:3])] + [(pt(ys[i], xs[i]), False) for i in range(3, 5)] + [(pt(xs[0], ys[1]), ys[0] == ys[1])]
    need(len({o[0] for o in opts}) == 6 and not opts[-1][1] and all(ys[i] != xs[i] for i in (3, 4)))
    return P(f"Data: {data_text(xs, ys, c[0], c[1])}. Select ALL points that belong on the scatter plot ({c[0]} on the x-axis).", None,
             ["Each point is (x-value, y-value) from the same position in the lists."], options=opts, chk=chk_py("in_dataset", xs=xs, ys=ys), tags=["multiple-representations"])


@fam("012")
def s1_open(r, L):
    c = pick_ctx(r, "pos")
    xs, ys = gen_scatter(r, "pos", n=6, xr=c[2], yr=c[3])
    return P(f"Use the data to build a scatter plot: {data_text(xs, ys, c[0], c[1])}.", None, ["x-axis variable.", "Least and greatest x.", "Least and greatest y.", "Pattern."],
             parts=[("Which variable goes on the horizontal axis?", c[0], {"kind": "text", "accept": [c[0]]}),
                    ("What are the least and greatest x-values?", f"{min(xs)} and {max(xs)}", chk_py("min_max", vals=xs)),
                    ("What are the least and greatest y-values?", f"{min(ys)} and {max(ys)}", chk_py("min_max", vals=ys)),
                    ("Describe the association: positive, negative, or none?", "positive", chk_py("assoc_dir", xs=xs, ys=ys))], tags=["multiple-representations"])


# ======================================================================= S2 Analyzing scatter plots
@fam("012")
def s2_outlier(r, L):
    c = pick_ctx(r, pick(r, ["pos", "neg"]))
    xs, ys = gen_scatter(r, c[6], n=10, xr=c[2], yr=c[3])
    k = r.randint(2, 7)
    span = c[3][1] - c[3][0]
    oy = ys[k] - round(span * 0.55) if ys[k] - round(span * 0.55) >= c[3][0] else ys[k] + round(span * 0.55)
    need(c[3][0] <= oy <= c[3][1])
    ys2 = ys[:]
    ys2[k] = oy
    drw = scatter_draw(xs, ys2, c[2], c[3], c[4], c[5], c[0], c[1])
    return P(f"The scatter plot shows {c[1]} versus {c[0]}. Which data point is an outlier?", pt(xs[k], oy),
             ["An outlier is far from the overall pattern of the other points.", f"{pt(xs[k], oy)} is far from the trend."],
             [pt(xs[0], ys2[0]), pt(xs[-1], ys2[-1]), pt(xs[(k + 3) % 10], ys2[(k + 3) % 10])], chk_py("outlier_pt", xs=xs, ys=ys2),
             diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys2)) + "."}, tags=["graph"])


@fam("012")
def s2_count(r, L):
    c = pick_ctx(r)
    xs, ys = gen_scatter(r, c[6] if c[6] != "none" else "none", n=10, xr=c[2], yr=c[3])
    thr = pick(r, sorted(set(ys))[2:-2])
    need(thr not in ys)
    cnt = sum(1 for y in ys if y > thr)
    drw = scatter_draw(xs, ys, c[2], c[3], c[4], c[5], c[0], c[1])
    return P(f"The scatter plot shows {c[1]} versus {c[0]} for 10 people. How many people had a {c[1]} greater than {thr}?", str(cnt),
             [f"Count the points above the horizontal level y = {thr}.", f"{cnt} points."], [str(cnt + 1), str(10 - cnt), str(cnt - 1)], chk_py("count_above", ys=ys, t=thr),
             diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."}, tags=["graph"])


@fam("012")
def s2_read(r, L):
    c = pick_ctx(r)
    xs, ys = gen_scatter(r, c[6], n=8, xr=c[2], yr=c[3])
    k = r.randint(0, 7)
    need(xs.count(xs[k]) == 1)
    drw = scatter_draw(xs, ys, c[2], c[3], c[4], c[5], c[0], c[1])
    return P(f"Use the scatter plot (all points have whole-number coordinates). What is the {c[1]} for the data point with {c[0]} = {xs[k]}?", str(ys[k]),
             [f"Find x = {xs[k]} and read the height of its point: {ys[k]}."], [str(ys[k] + c[5]), str(ys[k] - c[5]), str(xs[k])], chk_py("lookup_y", xs=xs, ys=ys, x=xs[k]),
             diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."}, tags=["graph"])


@fam("12", mode="mc")
def s2_cluster(r, L):
    lo_x = r.sample(range(0, 4), 3)
    hi_pts = r.sample([(x, y) for x in range(6, 11) for y in range(6, 10)], 7)
    xs = lo_x + [p[0] for p in hi_pts]
    ys = [r.randint(1, 4) for _ in lo_x] + [p[1] for p in hi_pts]
    drw = scatter_draw(xs, ys, (0, 10), (0, 10), 1, 1, "x", "y")
    good = "A cluster of points with x from 6 to 10"
    opts = [(good, True), ("A cluster of points with x from 0 to 3", False), ("No clusters; the points are evenly spread", False), ("A single outlier at (10, 10)", False)]
    r.shuffle(opts)
    return P("Which statement best describes a cluster in the scatter plot?", good, ["Most points (7 of 10) are grouped with x from 6 to 10."], options=opts,
             chk=chk_py("cluster_stmt", xs=xs, ys=ys), diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."}, tags=["graph"], mode="mc")


@fam("012")
def s2_trend_predict(r, L):
    c = pick_ctx(r, pick(r, ["pos", "neg"]))
    xs, ys = gen_scatter(r, c[6], n=10, xr=c[2], yr=c[3])
    q = pick(r, ["increase", "decrease"])
    want = ("increase" if c[6] == "pos" else "decrease")
    return P(f"Data: {data_text(xs, ys, c[0], c[1])}. As {c[0]} increases, does {c[1]} tend to increase or decrease?", want,
             [f"Look at the pattern from left to right: y tends to {want}."], ["decrease" if want == "increase" else "increase"], chk_py("trend_word", xs=xs, ys=ys), tags=["reasoning"], mode="sa")


@fam("012")
def s2_error(r, L):
    xs = list(range(1, 9))
    ys = [y for y in [2, 3, 3, 5, 6, 6, 8, 9]]
    k = pick(r, [2, 5])
    ys = [y + r.randint(0, 1) for y in ys]
    opts = [("No. Association does not prove that one variable causes the other.", True), ("Yes. A positive association proves cause and effect.", False),
            ("No. The association is negative.", False), ("Yes. Every point lies exactly on a line.", False)]
    r.shuffle(opts)
    return P("A scatter plot shows that cities with more ice cream sales also have more sunburn cases (a positive association). Lou says eating ice cream causes sunburn. Is Lou correct?",
             opts[[c for _, c in opts].index(True)][0], ["Both may increase because of a third factor (hot, sunny weather).", "Association is not causation."], options=opts,
             chk={"kind": "text", "accept": ["No. Association does not prove that one variable causes the other."]}, tags=["error-analysis", "reasoning"], mode="mc")


@fam("012")
def s2_select(r, L):
    c = pick_ctx(r, "pos")
    xs, ys = gen_scatter(r, "pos", n=8, xr=c[2], yr=c[3])
    stm = [(f"The greatest {c[1]} is {max(ys)}.", True), (f"The least {c[0]} is {min(xs)}.", True), ("The association is positive.", True),
           (f"The greatest {c[1]} is {max(ys) + c[5]}.", False), ("The association is negative.", False), (f"There are {len(xs) + 1} data points.", False)]
    drw = scatter_draw(xs, ys, c[2], c[3], c[4], c[5], c[0], c[1])
    return P("Select ALL true statements about the scatter plot.", None, [f"Points: " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."], options=stm,
             chk=chk_py("scatter_stmt", xs=xs, ys=ys, xl=c[0], yl=c[1]), diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."}, tags=["graph"])


@fam("012")
def s2_open(r, L):
    c = pick_ctx(r, "neg")
    xs, ys = gen_scatter(r, "neg", n=8, xr=c[2], yr=c[3])
    return P(f"Data: {data_text(xs, ys, c[0], c[1])}.", None, ["Count.", "Greatest y.", "Direction.", "Range."],
             parts=[("How many data points are there?", str(len(xs)), chk_val(str(len(xs)))), (f"What is the greatest {c[1]}?", str(max(ys)), chk_val(str(max(ys)))),
                    ("Is the association positive, negative, or none?", "negative", chk_py("assoc_dir", xs=xs, ys=ys)),
                    (f"What is the range of the {c[1]} values?", str(max(ys) - min(ys)), chk_val(f"{max(ys)} - ({min(ys)})"))], tags=["reasoning"])


# ======================================================================= S3 Linear and nonlinear association
@fam("012", mode="mc")
def s3_classify_plot(r, L):
    kind = pick(r, ["pos", "neg", "none", "curve"] if L else ["pos", "neg", "none"])
    xs, ys = gen_scatter(r, kind, n=12, xr=(0, 12), yr=(0, 12))
    drw = scatter_draw(xs, ys, (0, 12), (0, 12), 1, 1, "x", "y")
    want = {"pos": "positive linear association", "neg": "negative linear association", "none": "no association", "curve": "nonlinear association"}[kind]
    opts = [(t, t == want) for t in ["positive linear association", "negative linear association", "no association", "nonlinear association"]]
    return P("Which best describes the association shown in the scatter plot?", want,
             [{"pos": "Points rise left to right along a line-like pattern.", "neg": "Points fall left to right along a line-like pattern.", "none": "No clear pattern.", "curve": "The points follow a curve, not a line."}[kind]],
             options=opts, chk=chk_py("assoc_type", xs=xs, ys=ys), diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."},
             tags=["graph", "reasoning"], mode="mc")


@fam("012", mode="sa")
def s3_context(r, L):
    ctx = [("the number of hours a student spends practicing piano and the number of mistakes in a recital", "negative"),
           ("a person's height and their shoe size", "positive"), ("the day of the month a person was born and their test score", "no association"),
           ("the number of people at a party and the amount of food eaten", "positive"), ("the age of a phone and its battery life", "negative"),
           ("the outdoor temperature and the number of people at a pool", "positive"), ("the number of absences and a student's grade", "negative"),
           ("a student's favorite number and their height", "no association")]
    s, ans = pick(r, ctx)
    return P(f"Would you expect a positive association, a negative association, or no association between {s}?", ans,
             [{"positive": "As one increases, the other tends to increase.", "negative": "As one increases, the other tends to decrease.", "no association": "There is no reason for one to change with the other."}[ans]],
             [x for x in ["positive", "negative", "no association"] if x != ans], {"kind": "text", "accept": [ans]}, tags=["reasoning", "modeling"], mode="sa")


@fam("012", mode="sa")
def s3_table(r, L):
    kind = pick(r, ["pos", "neg", "none"] if L < 2 else ["pos", "neg", "curve", "none"])
    xs, ys = gen_scatter(r, kind, n=8, xr=(1, 12), yr=(0, 40))
    want = {"pos": "positive", "neg": "negative", "none": "no association", "curve": "nonlinear"}[kind]
    q = "Is the association positive, negative, or none?" if L < 2 else "Is the association positive linear, negative linear, nonlinear, or none?"
    if L == 2:
        want = {"pos": "positive linear", "neg": "negative linear", "none": "none", "curve": "nonlinear"}[kind]
    return P(f"Data: {data_text(xs, ys, 'x', 'y')}. {q}", want, ["Look at how y changes as x increases.", want + "."], [], chk_py("assoc_word", xs=xs, ys=ys, L=L),
             tags=["multiple-representations"], mode="sa")


@fam("12", mode="mc")
def s3_strength(r, L):
    a = gen_scatter(r, "pos", n=10, xr=(0, 10), yr=(0, 10))
    xs = list(range(1, 11))
    ys_weak = [max(0, min(10, x + r.randint(-3, 3))) for x in xs]
    need(0.3 < corr(xs, ys_weak) < 0.75)
    order = ["strong", "weak"]
    r.shuffle(order)
    data = {"strong": a, "weak": (xs, ys_weak)}
    drawers = [scatter_draw(*data[k], (0, 10), (0, 10), 1, 1, "x", "y") for k in order]

    def draw(path):
        p = plt()
        fig, axs = p.subplots(1, 2, figsize=(10, 4.4), dpi=100)
        for ax, d, lab in zip(axs, drawers, "AB"):
            d.draw_on(ax)
            ax.set_title(f"Plot {lab}", fontsize=14, fontweight="bold")
        fig.tight_layout()
        save(fig, path)
    good = "Plot " + "AB"[order.index("strong")]
    return P("Both scatter plots show a positive association. Which plot shows the stronger linear association?", good,
             ["The stronger association has points packed more closely around a line."], options=[("Plot A", good == "Plot A"), ("Plot B", good == "Plot B"), ("They are equally strong", False), ("Neither has an association", False)],
             chk=chk_py("stronger", A=[list(d) for d in data[order[0]]], B=[list(d) for d in data[order[1]]]),
             diagram={"draw": draw, "alt": "Two scatter plots. " + "; ".join(f"Plot {l}: points " + ", ".join(pt(a_, b_) for a_, b_ in zip(*data[k])) for l, k in zip("AB", order))},
             tags=["graph", "reasoning"], mode="mc")


@fam("012")
def s3_error(r, L):
    xs, ys = gen_scatter(r, "neg", n=10, xr=(0, 10), yr=(0, 10))
    drw = scatter_draw(xs, ys, (0, 10), (0, 10), 1, 1, "hours of video games", "hours of homework")
    opts = [("No. The points fall from left to right, so the association is negative.", True), ("Yes. The points form a pattern, so it is positive.", False),
            ("No. There is no association.", False), ("Yes. Negative values are not possible here.", False)]
    r.shuffle(opts)
    return P("Abe says the scatter plot shows a positive association because the points \"make a line.\" Is Abe correct?", opts[[c for _, c in opts].index(True)][0],
             ["A clear linear pattern can be positive or negative.", "Here y decreases as x increases: negative association."], options=opts, chk=chk_py("assoc_claim", xs=xs, ys=ys),
             diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."}, tags=["error-analysis", "graph"], mode="mc")


@fam("012")
def s3_select(r, L):
    sets = [(gen_scatter(r, "pos", n=6, xr=(1, 12), yr=(0, 30)), True), (gen_scatter(r, "pos", n=6, xr=(1, 12), yr=(0, 30)), True), (gen_scatter(r, "pos", n=6, xr=(1, 12), yr=(0, 30)), True),
            (gen_scatter(r, "neg", n=6, xr=(1, 12), yr=(0, 30)), False), (gen_scatter(r, "neg", n=6, xr=(1, 12), yr=(0, 30)), False), (gen_scatter(r, "none", n=6, xr=(1, 12), yr=(0, 30)), False)]
    opts = [(data_text(a, b, "x", "y"), c) for (a, b), c in sets]
    need(len({o[0] for o in opts}) == 6)
    return P("Select ALL data sets that show a positive association.", None, ["Positive: y tends to increase as x increases."], options=opts, chk=chk_py("assoc_is", want="positive"), tags=["reasoning"])


@fam("012")
def s3_open(r, L):
    xs = [1, 2, 3, 4, 5, 6]
    a = r.randint(2, 4)
    ys = [a * x * x for x in xs]
    d1 = [b - a_ for a_, b in zip(ys, ys[1:])]
    return P(f"Data: {data_text(xs, ys, 'x', 'y')}.", None, ["Compute differences.", "Not constant.", "Curved pattern.", "Positive direction."],
             parts=[("List the differences in y between consecutive x-values.", ", ".join(map(str, d1)), {"kind": "text", "accept": [", ".join(map(str, d1))]}),
                    ("Are the differences constant? Answer yes or no.", "no", {"kind": "text", "accept": ["no"]}),
                    ("Is the association linear or nonlinear?", "nonlinear", chk_py("table_linear2", xs=xs, ys=ys)),
                    ("Is the association positive or negative?", "positive", chk_py("assoc_dir", xs=xs, ys=ys))], tags=["reasoning"])


# ======================================================================= S4 Lines of best fit
FIT = [("hours studied", "test score", "points per hour"), ("months since planting", "tree height (cm)", "cm per month"), ("age of car (years)", "value ($1,000s)", "thousand dollars per year"),
       ("minutes of exercise", "calories burned", "calories per minute")]


@fam("012")
def s4_predict(r, L):
    c = pick(r, FIT)
    m = F(r.randint(2, 12)) * (-1 if "value" in c[1] else 1)
    b = F(r.randint(20, 60))
    x = r.randint(3, 15)
    if L == 2:
        m = m / 2
    v = m * x + b
    return P(f"A line of best fit for {c[1]} (y) versus {c[0]} (x) is y = {mx_b(m, b)}. Predict the {c[1]} when x = {x}.", N(v) if v.denominator == 1 else D(v),
             [f"Substitute x = {x}: y = {N(m)}({x}) + {N(b)} = {D(v)}."], [D(m * x), D(v + m), D(m + b) if m + b != v else D(v + 2)], chk_val(f"{N(m)}*{x} + {N(b)}"), tags=["modeling"])


@fam("012")
def s4_interpret(r, L):
    c = pick(r, FIT)
    m = F(r.randint(2, 12)) * (-1 if "value" in c[1] else 1)
    b = F(r.randint(20, 60))
    q = pick(r, ["slope", "int"])
    if q == "slope":
        ans = f"The {c[1]} changes by {N(m)} for each 1 increase in {c[0]}."
        wr = [f"The {c[1]} is {N(m)} when {c[0]} is 0.", f"The {c[1]} changes by {N(b)} for each 1 increase in {c[0]}.", f"The {c[0]} changes by {N(m)} for each 1 increase in {c[1]}."]
    else:
        ans = f"The predicted {c[1]} is {N(b)} when {c[0]} is 0."
        wr = [f"The {c[1]} changes by {N(b)} for each 1 increase in {c[0]}.", f"The predicted {c[0]} is {N(b)} when {c[1]} is 0.", f"The predicted {c[1]} is {N(m)} when {c[0]} is 0."]
    return P(f"The line of best fit y = {mx_b(m, b)} models {c[1]} (y) from {c[0]} (x). What does the {'slope' if q == 'slope' else 'y-intercept'} mean?", ans,
             ["Slope: change in y per 1 unit of x. y-intercept: predicted y when x = 0."], wr, chk_py("fit_meaning", m=N(m), b=N(b), xl=c[0], yl=c[1]), tags=["modeling"])


@fam("12", mode="mc")
def s4_best_line(r, L):
    xs, ys = gen_scatter(r, pick(r, ["pos", "neg"]), n=10, xr=(0, 10), yr=(0, 10))
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sl = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    m0 = F(round(sl * 2), 2)
    b0 = F(round((my - float(m0) * mx) * 2), 2)
    cands = [(m0, b0), (m0, b0 + 3), (-m0, b0), (m0 * 2, b0 - 2)]
    need(len(set(cands)) == 4 and m0 != 0)
    sse = [sum((y - float(m) * x - float(b)) ** 2 for x, y in zip(xs, ys)) for m, b in cands]
    opt = sum((y - (my + sl * (x - mx))) ** 2 for x, y in zip(xs, ys))
    need(sse[0] < 0.8 * min(sse[1:]) and sse[0] <= 1.2 * opt + 0.5)
    drw = scatter_draw(xs, ys, (0, 10), (0, 10), 1, 1, "x", "y")
    opts = [(f"y = {mx_b(m, b)}", i == 0) for i, (m, b) in enumerate(cands)]
    r.shuffle(opts)
    return P("Which equation is the best line of fit for the scatter plot?", f"y = {mx_b(m0, b0)}",
             ["A good line follows the trend with about as many points above as below it.", f"y = {mx_b(m0, b0)} has the right direction, steepness and position."],
             options=opts, chk=chk_py("best_fit", xs=xs, ys=ys), diagram={"draw": drw, "alt": "Scatter plot with points " + ", ".join(pt(a, b) for a, b in zip(xs, ys)) + "."},
             tags=["graph", "reasoning"], mode="mc")


@fam("012")
def s4_equation_from_line(r, L):
    xs, ys = gen_scatter(r, pick(r, ["pos", "neg"]), n=10, xr=(0, 10), yr=(0, 10))
    m = F(round(corr(xs, ys) * 2) or 1, 2) if False else None
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sl = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    m = F(round(sl * 2), 2)
    need(m != 0)
    b = F(round(my - float(m) * mx))
    p1, p2 = (0, b), (2, b + 2 * m)
    need(0 <= b <= 10 and 0 <= p2[1] <= 10)
    drw = scatter_draw(xs, ys, (0, 10), (0, 10), 1, 1, "x", "y", line=(m, b), labels=[(0, float(b), pt(*p1)), (2, float(p2[1]), pt(*p2))])
    return P("A line of fit is drawn on the scatter plot through the labeled points. Write its equation.", f"y = {mx_b(m, b)}",
             [f"slope = ({N(p2[1])} - {N(b)}) ÷ (2 - 0) = {N(m)}.", f"y-intercept {N(b)}."], [f"y = {mx_b(-m, b)}", f"y = {mx_b(m, b + 1)}", f"y = {mx_b(1 / m, b)}"],
             chk_py("line_through", pts=[[0, N(b)], [2, N(p2[1])]]), diagram={"draw": drw, "alt": f"Scatter plot with a line of fit through {pt(*p1)} and {pt(*p2)}."}, tags=["graph"])


@fam("12")
def s4_residual(r, L):
    m, b = F(r.randint(2, 6)), F(r.randint(10, 40))
    x = r.randint(2, 12)
    actual = m * x + b + nz(r, -9, 9)
    pred = m * x + b
    return P(f"A line of best fit predicts y = {mx_b(m, b)}. A data point is ({x}, {N(actual)}). How far is the actual y-value above (+) or below (-) the predicted value?", N(actual - pred),
             [f"Predicted: {N(m)}({x}) + {N(b)} = {N(pred)}.", f"Actual - predicted = {N(actual)} - {N(pred)} = {N(actual - pred)}."], [N(pred - actual), N(pred), N(actual - pred + m)],
             chk_val(f"{N(actual)} - ({N(m)}*{x} + {N(b)})"), tags=["reasoning", "challenge"])


@fam("012")
def s4_error(r, L):
    m, b = F(r.randint(2, 6)), F(r.randint(10, 40))
    opts = [("No. 40 hours is far outside the data, so the prediction may not be reliable.", True), ("Yes. A line of best fit works for any x-value.", False),
            ("No. The slope is negative.", False), ("Yes. Predictions are exact.", False)]
    r.shuffle(opts)
    return P(f"A line of best fit y = {mx_b(m, b)} models test score from hours studied, using data from 0 to 6 hours. Eva says a student who studies 40 hours will score {N(m * 40 + b)}. Is her reasoning sound?",
             opts[[c for _, c in opts].index(True)][0], ["Predicting far beyond the data (extrapolating) can give impossible results, such as a score above 100."],
             options=opts, chk={"kind": "text", "accept": ["No. 40 hours is far outside the data, so the prediction may not be reliable."]}, tags=["error-analysis", "reasoning"], mode="mc")


@fam("012")
def s4_select(r, L):
    m, b = F(r.randint(2, 6)), F(r.randint(10, 30))
    stm = [(f"For x = 2, the predicted y is {N(2 * m + b)}.", True), (f"The predicted y increases by {N(m)} for each 1 increase in x.", True), (f"When x = 0, the predicted y is {N(b)}.", True),
           (f"For x = 2, the predicted y is {N(2 * (m + b))}.", False), (f"The predicted y increases by {N(b)} for each 1 increase in x.", False), (f"When x = 0, the predicted y is {N(m)}.", False)]
    return P(f"A line of best fit is y = {mx_b(m, b)}. Select ALL true statements.", None, ["Substitute and interpret slope and intercept."], options=stm,
             chk=chk_py("fit_stmt", m=N(m), b=N(b)), tags=["modeling"])


@fam("012")
def s4_open(r, L):
    m, b = F(r.randint(3, 9)), F(r.randint(20, 50))
    return P(f"A line of best fit for plant height h (cm) after w weeks is h = {N(m)}w + {N(b)}.", None, ["Slope meaning.", "Intercept.", "Predict.", "Solve."],
             parts=[("What is the predicted growth per week?", f"{N(m)} cm", chk_val(N(m))), ("What is the predicted height at week 0?", f"{N(b)} cm", chk_val(N(b))),
                    ("Predict the height at week 5.", f"{N(5 * m + b)} cm", chk_val(f"{N(m)}*5 + {N(b)}")),
                    (f"In which week is the predicted height {N(8 * m + b)} cm?", "8", {"kind": "eq", "eq": f"{N(m)}w + {N(b)} = {N(8 * m + b)}", "var": "w"})], tags=["modeling"])


# ======================================================================= S5 Constructing two-way tables
GROUPS = [(("Grade 7 students", "Grade 8 students"), ("play a sport", "do not play a sport")), (("boys", "girls"), ("have a pet", "have no pet")),
          (("morning-shift workers", "evening-shift workers"), ("bought lunch", "brought lunch")), (("juniors", "seniors"), ("have a job", "have no job")),
          (("adults", "teens"), ("prefer movies", "prefer games"))]


def tw_data(r, big=False):
    g = pick(r, GROUPS)
    a, b, c, d = [r.randint(5, 40 if big else 25) for _ in range(4)]
    return g, (a, b, c, d)


def tw_text(g, t):
    (r1, r2), (c1, c2) = g
    a, b, c, d = t
    return f"{r1}: {a} {c1}, {b} {c2}. {r2}: {c} {c1}, {d} {c2}"


@fam("012")
def s5_fill_cell(r, L):
    g, (a, b, c, d) = tw_data(r, L > 0)
    (r1, r2), (c1, c2) = g
    tot = a + b + c + d
    q = pick(r, ["row", "col", "grand", "cell"])
    if q == "row":
        p = f"Survey results — {r1}: {a} {c1}, {b} {c2}. How many {r1} were surveyed in all (row total)?"
        v = a + b
        wr = [a + c, tot, b]
    elif q == "col":
        p = f"Survey results — {r1}: {a} {c1}, {b} {c2}. {r2}: {c} {c1}, {d} {c2}. What is the column total for \"{c1}\"?"
        v = a + c
        wr = [a + b, tot, c + d]
    elif q == "grand":
        p = f"Survey results — {r1}: {a} {c1}, {b} {c2}. {r2}: {c} {c1}, {d} {c2}. How many people were surveyed in all?"
        v = tot
        wr = [a + b, a + c, tot - d]
    else:
        p = f"In a survey of {tot} people, {a + b} were {r1} and the rest were {r2}. Of the {r1}, {a} {c1}. In all, {a + c} people {c1}. How many {r2} {c2}?"
        v = d
        wr = [c, b, tot - (a + c)]
    need(len({v, *wr}) == 4)
    return P(p, str(v), ["Row totals add across; column totals add down; the grand total is the sum of all cells.", f"Answer: {v}."], [str(w) for w in wr],
             chk_py("twoway_cell", t=[a, b, c, d], q=q, show=[str(a)]), tags=["multiple-representations"])


@fam("012")
def s5_build(r, L):
    g, (a, b, c, d) = tw_data(r)
    (r1, r2), (c1, c2) = g
    tot = a + b + c + d
    p = f"{tot} students were surveyed. {a + b} are {r1}; the rest are {r2}. {a + c} {c1}; the rest {c2}. {a} of the {r1} {c1}. Complete the two-way table: how many {r2} {c2}?" if L else \
        f"Make a two-way table from these counts: {tw_text(g, (a, b, c, d))}. What is the total number of {r2}?"
    v = d if L else c + d
    return P(p, str(v), ["Fill known cells, then use row and column totals to find missing cells." if L else f"Row total for {r2}: {c} + {d}.", f"Answer: {v}."],
             [str(c), str(tot - a), str(b)] if L else [str(c), str(d), str(a + c)], chk_py("twoway_cell", t=[a, b, c, d], q="cell" if L else "row2"), tags=["multistep"])


@fam("12", mode="mc")
def s5_which_table(r, L):
    g, (a, b, c, d) = tw_data(r)
    (r1, r2), (c1, c2) = g
    good = f"{r1}: {a}, {b} | {r2}: {c}, {d} (columns: {c1}, {c2})"
    bads = [f"{r1}: {a}, {c} | {r2}: {b}, {d} (columns: {c1}, {c2})", f"{r1}: {b}, {a} | {r2}: {d}, {c} (columns: {c1}, {c2})", f"{r1}: {a}, {b} | {r2}: {d}, {c} (columns: {c1}, {c2})"]
    opts = [(good, True)] + [(x, False) for x in bads]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return P(f"Survey: {a} {r1} {c1} and {b} {r1} {c2}; {c} {r2} {c1} and {d} {r2} {c2}. Which table is correct?", good,
             ["Each row is a group; each column is a response. Match every count to its row and column."], options=opts, chk=chk_py("twoway_layout", t=[a, b, c, d]), tags=["multiple-representations"], mode="mc")


@fam("012")
def s5_error(r, L):
    g, (a, b, c, d) = tw_data(r)
    (r1, r2), (c1, c2) = g
    need(a + b != a + c)
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}. Ty says the total for \"{c1}\" is {a + b}. What is the correct column total for \"{c1}\"?", str(a + c),
             [f"Ty added across the {r1} row ({a} + {b}).", f"Column total: {a} + {c} = {a + c}."], [str(a + b), str(a + b + c + d), str(c + d)], chk_py("twoway_cell", t=[a, b, c, d], q="col"),
             tags=["error-analysis", "misconception"])


@fam("012")
def s5_select(r, L):
    g, (a, b, c, d) = tw_data(r)
    (r1, r2), (c1, c2) = g
    need(len({a + b, c + d, a + c, b + d, a + b + c + d}) == 5)
    stm = [(f"The {r1} row total is {a + b}.", True), (f"The \"{c2}\" column total is {b + d}.", True), (f"The grand total is {a + b + c + d}.", True),
           (f"The {r1} row total is {a + c}.", False), (f"The \"{c2}\" column total is {c + d}.", False), (f"The grand total is {a + b + c + d + a}.", False)]
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}. Select ALL true statements.", None, ["Compute row, column and grand totals."], options=stm,
             chk=chk_py("twoway_stmt", t=[a, b, c, d], g=[list(g[0]), list(g[1])]), tags=["multiple-representations"])


@fam("012")
def s5_open(r, L):
    g, (a, b, c, d) = tw_data(r)
    (r1, r2), (c1, c2) = g
    return P(f"Use the survey data to complete a two-way table: {tw_text(g, (a, b, c, d))}.", None, ["Row.", "Row.", "Column.", "Grand."],
             parts=[(f"Total {r1}?", str(a + b), chk_py("twoway_cell", t=[a, b, c, d], q="row")), (f"Total {r2}?", str(c + d), chk_py("twoway_cell", t=[a, b, c, d], q="row2")),
                    (f"Total who {c1}?", str(a + c), chk_py("twoway_cell", t=[a, b, c, d], q="col")), ("Grand total?", str(a + b + c + d), chk_py("twoway_cell", t=[a, b, c, d], q="grand"))],
             tags=["multiple-representations"])


# ======================================================================= S6 Interpreting two-way tables
@fam("012")
def s6_relfreq(r, L):
    g, (a, b, c, d) = tw_data(r, True)
    (r1, r2), (c1, c2) = g
    q = pick(r, ["joint", "row", "col"] if L else ["joint", "row"])
    tot = a + b + c + d
    if q == "joint":
        v, txt, base = F(a, tot), f"What fraction of all people surveyed are {r1} who {c1}?", f"{a} ÷ {tot}"
        wr = [F(a, a + b), F(a, a + c), F(a + b, tot)]
    elif q == "row":
        v, txt, base = F(a, a + b), f"What fraction of the {r1} {c1}?", f"{a} ÷ ({a} + {b})"
        wr = [F(a, tot), F(a, a + c), F(b, a + b)]
    else:
        v, txt, base = F(a, a + c), f"Of the people who {c1}, what fraction are {r1}?", f"{a} ÷ ({a} + {c})"
        wr = [F(a, a + b), F(a, tot), F(c, a + c)]
    need(len({v, *wr}) == 4)
    pct = L == 2
    ans = f"{Rd(v * 100, 1)}%" if pct else N(v)
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}. {txt}" + (" Give a percent rounded to the nearest tenth." if pct else " Write the fraction in simplest form."), ans,
             [f"{base} = {N(v)}" + (f" ≈ {Rd(v * 100, 1)}%." if pct else ".")], [f"{Rd(w * 100, 1)}%" if pct else N(w) for w in wr],
             chk_py("relfreq", t=[a, b, c, d], q=q, pct=pct, show=[str(a), str(b), str(c), str(d)]), tags=["reasoning"])


@fam("12", mode="mc")
def s6_association(r, L):
    g = pick(r, GROUPS)
    (r1, r2), (c1, c2) = g
    assoc = r.random() < 0.5
    n1, n2 = r.randint(30, 60), r.randint(30, 60)
    p1 = F(r.randint(60, 80), 100)
    p2 = (p1 - F(r.randint(30, 45), 100)) if assoc else p1 + F(pick(r, [-2, 0, 2]), 100)
    a, c = round(n1 * p1), round(n2 * p2)
    b, d = n1 - a, n2 - c
    need(min(a, b, c, d) > 0)
    f1, f2 = F(a, a + b), F(c, c + d)
    has = abs(f1 - f2) >= F(1, 5)
    need(has == assoc and (assoc or abs(f1 - f2) <= F(1, 20)))
    good = (f"Yes, because {Rd(f1 * 100, 0)}% of {r1} {c1} compared with {Rd(f2 * 100, 0)}% of {r2}." if assoc else
            f"No, because about the same percent of each group {c1} ({Rd(f1 * 100, 0)}% and {Rd(f2 * 100, 0)}%).")
    opts = [(good, True), (f"Yes, because more {r1 if a > c else r2} {c1} in total." if a != c else f"Yes, because the counts are equal.", False),
            ("No, because the groups have different sizes.", False), (f"{'No' if assoc else 'Yes'}, because the row totals are {'different' if n1 != n2 else 'equal'}.", False)]
    r.shuffle(opts)
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}. Is there evidence of an association between group and response?", good,
             ["Compare relative frequencies within each row, not raw counts.", f"{r1}: {a}/{a + b} ≈ {Rd(f1 * 100, 0)}%; {r2}: {c}/{c + d} ≈ {Rd(f2 * 100, 0)}%."],
             options=opts, chk=chk_py("twoway_assoc", t=[a, b, c, d]), tags=["reasoning", "challenge"], mode="mc")


@fam("012")
def s6_compare(r, L):
    g, (a, b, c, d) = tw_data(r, True)
    (r1, r2), (c1, c2) = g
    f1, f2 = F(a, a + b), F(c, c + d)
    need(f1 != f2)
    ans = r1 if f1 > f2 else r2
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}. Which group has the greater relative frequency of people who {c1}: {r1} or {r2}?", ans,
             [f"{r1}: {a} ÷ {a + b} ≈ {Rd(f1, 3)}; {r2}: {c} ÷ {c + d} ≈ {Rd(f2, 3)}.", f"{ans} is greater."], [r2 if ans == r1 else r1, "They are equal"],
             chk_py("greater_group", t=[a, b, c, d], names=[r1, r2]), tags=["reasoning", "misconception"])


@fam("2")
def s6_missing_from_rf(r, L):
    n = pick(r, [20, 25, 40, 50, 80])
    p = F(r.randint(1, 9), 10)
    need((n * p).denominator == 1)
    return P(f"In a row of a two-way table, {Rd(p * 100, 0)}% of the {n} {pick(r, ['students', 'customers', 'players'])} chose \"yes.\" How many chose \"no\"?", str(n - int(n * p)),
             [f"Yes: {Rd(p * 100, 0)}% of {n} = {int(n * p)}.", f"No: {n} - {int(n * p)} = {n - int(n * p)}."], [str(int(n * p)), str(n), str(n - int(n * p) + 1)],
             chk_val(f"{n} - {n}*{D(p)}"), tags=["reasoning"])


@fam("012")
def s6_error(r, L):
    g, (a, b, c, d) = tw_data(r, True)
    (r1, r2), (c1, c2) = g
    need(a + b != a + c)
    tot = a + b + c + d
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}. Ken says the relative frequency of {r1} who {c1}, among all {r1}, is {a}/{tot}. What is the correct relative frequency?",
             N(F(a, a + b)), [f"\"Among all {r1}\" means divide by the {r1} row total {a + b}, not the grand total {tot}.", f"{a}/{a + b} = {N(F(a, a + b))}."],
             [N(F(a, tot)), N(F(a, a + c)), N(F(b, a + b))], chk_py("relfreq", t=[a, b, c, d], q="row", pct=False), tags=["error-analysis", "misconception"])


@fam("012")
def s6_select(r, L):
    g, (a, b, c, d) = tw_data(r, True)
    (r1, r2), (c1, c2) = g
    tot = a + b + c + d
    need(len({F(a, a + b), F(a, tot), F(c, c + d), F(a, a + c)}) == 4)
    stm = [(f"Among {r1}, the relative frequency of \"{c1}\" is {N(F(a, a + b))}.", True), (f"Among all people, the relative frequency of {r1} who {c1} is {N(F(a, tot))}.", True),
           (f"Among {r2}, the relative frequency of \"{c1}\" is {N(F(c, c + d))}.", True), (f"Among {r1}, the relative frequency of \"{c1}\" is {N(F(a, tot))}.", False),
           (f"Among {r2}, the relative frequency of \"{c1}\" is {N(F(c, a + c))}.", F(c, a + c) == F(c, c + d)), (f"Among all people, the relative frequency of {r1} who {c1} is {N(F(a, a + b))}.", False)]
    need(not stm[4][1])
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}. Select ALL true statements.", None, ["Use the correct total for each relative frequency."], options=stm,
             chk=chk_py("rf_stmt", t=[a, b, c, d], g=[list(g[0]), list(g[1])]), tags=["reasoning"])


@fam("012")
def s6_open(r, L):
    g, (a, b, c, d) = tw_data(r, True)
    (r1, r2), (c1, c2) = g
    f1, f2 = F(a, a + b), F(c, c + d)
    need(f1 != f2)
    return P(f"Two-way table — {tw_text(g, (a, b, c, d))}.", None, ["Row relative frequency.", "Row relative frequency.", "Compare.", "Grand total."],
             parts=[(f"What fraction of {r1} {c1}?", N(f1), chk_py("relfreq", t=[a, b, c, d], q="row", pct=False)),
                    (f"What fraction of {r2} {c1}?", N(f2), chk_py("relfreq", t=[a, b, c, d], q="row2", pct=False)),
                    (f"Which group is more likely to say \"{c1}\"?", r1 if f1 > f2 else r2, chk_py("greater_group", t=[a, b, c, d], names=[r1, r2])),
                    ("How many people were surveyed?", str(a + b + c + d), chk_val(f"{a}+{b}+{c}+{d}"))], tags=["reasoning"])


SKILLS = {
    1: dict(name="Constructing scatter plots", std=["8.SP.A.1"], fams=[s1_which_plot, s1_point_for_row, s1_scale, s1_axes], extra=[s1_error, s1_select, s1_open]),
    2: dict(name="Analyzing scatter plots", std=["8.SP.A.1"], fams=[s2_outlier, s2_count, s2_read, s2_cluster, s2_trend_predict], extra=[s2_error, s2_select, s2_open]),
    3: dict(name="Linear and nonlinear association", std=["8.SP.A.1"], fams=[s3_classify_plot, s3_context, s3_table, s3_strength], extra=[s3_error, s3_select, s3_open]),
    4: dict(name="Lines of best fit", std=["8.SP.A.2", "8.SP.A.3"], fams=[s4_predict, s4_interpret, s4_best_line, s4_equation_from_line, s4_residual], extra=[s4_error, s4_select, s4_open]),
    5: dict(name="Constructing two-way tables", std=["8.SP.A.4"], fams=[s5_fill_cell, s5_build, s5_which_table], extra=[s5_error, s5_select, s5_open]),
    6: dict(name="Interpreting two-way tables", std=["8.SP.A.4"], fams=[s6_relfreq, s6_association, s6_compare, s6_missing_from_rf], extra=[s6_error, s6_select, s6_open]),
}
