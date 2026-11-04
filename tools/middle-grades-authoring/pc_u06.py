"""Precalculus Unit 6 — Matrices (matrices)."""
from hslib import *

UNIT_ID = "matrices"
ABBR = "mat"
M_ = sp.Matrix


def rmat(r, m, n, lo=-9, hi=9):
    return M_([[rint(r, lo, hi) for _ in range(n)] for _ in range(m)])


def inv2(r, L):
    for _ in range(60):
        A = rmat(r, 2, 2, -6, 6)
        d = A.det()
        if d != 0 and (L > 0 or d in (1, -1)) and abs(d) <= 12:
            return A
    raise Reject()


# ============================================================== S1 Notation
@fam("012")
def s1_dims(r, L):
    m, n = rint(r, 1, 4), rint(r, 1, 4)
    A = rmat(r, m, n)
    kind = pick(r, ["dims", "entry"]) if m > 1 and n > 1 else "dims"
    need(kind == "entry" or m != n)
    if kind == "dims":
        return Q(f"What are the dimensions of A = {mat_text(A)}?", f"{m} × {n}", ["Dimensions are rows × columns.", f"{m} rows, {n} columns.", f"{m} × {n}."], [f"{n} × {m}", f"{m * n} × 1", f"{m + n} × 1" if m + n != m * n else f"1 × {m * n}"],
                 PY("dims", m=m, n=n), why=["Listed columns before rows", "Counted all the entries", "Added rows and columns"])
    i, j = rint(r, 1, m), rint(r, 1, n)
    need(i != j and j <= m and i <= n and A[i - 1, j - 1] != A[j - 1, i - 1])
    return Q(f"For A = {mat_text(A)}, find the entry a{str(i).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))}{str(j).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))}.", str(A[i - 1, j - 1]),
             [f"a_ij is in row i, column j.", f"Row {i}, column {j}: {A[i - 1, j - 1]}."], [str(A[j - 1, i - 1]), str(A[i - 1, 0] if j != 1 else A[0, j - 1]), str(A[0, 0]) if (i, j) != (1, 1) else str(A[m - 1, n - 1])],
             H(f"Matrix({A.tolist()})[{i - 1}, {j - 1}]"), why=["Switched row and column", "Read the wrong column", "Used the first entry"])


@fam("012")
def s1_data(r, L):
    stores = ["North", "South", "East"]
    items = ["shirts", "hats", "jackets"]
    A = rmat(r, 3, 3, 5, 60)
    i, j = rint(r, 0, 2), rint(r, 0, 2)
    rows = "; ".join(f"{stores[k_]}: " + ", ".join(f"{A[k_, c_]} {items[c_]}" for c_ in range(3)) for k_ in range(3))
    if L < 2:
        return Q(f"Store sales are organized in a matrix S with rows North, South, East and columns shirts, hats, jackets. {rows}. What is entry s{i + 1}{j + 1}" .translate(str.maketrans("", "")) .replace(f"s{i + 1}{j + 1}", f"s{'₀₁₂₃'[i + 1]}{'₀₁₂₃'[j + 1]}") + " and what does it mean?",
                 f"{A[i, j]} {items[j]} at the {stores[i]} store", [f"Row {i + 1} is {stores[i]}; column {j + 1} is {items[j]}.", f"s = {A[i, j]}."],
                 [f"{A[j, i]} {items[i]} at the {stores[j]} store" if (i != j) else f"{A[i, (j + 1) % 3]} {items[(j + 1) % 3]} at the {stores[i]} store", f"{A[i, j]} {items[i] if i != j else items[(j + 1) % 3]} at the {stores[j] if i != j else stores[(i + 1) % 3]} store", f"{sum(A[i, :])} items at the {stores[i]} store"],
                 PY("data_entry", v=int(A[i, j]), item=items[j], store=stores[i]), why=["Switched row and column", "Mislabeled the entry", "Added the whole row"])
    p = M_([[rint(r, 8, 30)] for _ in range(3)])
    rev = A * p
    return Q(f"Sales matrix S (rows North, South, East; columns shirts, hats, jackets): {mat_text(A)}. Prices (dollars) P = {mat_text(p)} for shirts, hats, jackets. Find the total revenue for the {stores[i]} store using SP.",
             f"${rev[i, 0]}", ["SP multiplies each store's quantities by the prices and adds.", f"{stores[i]}: " + " + ".join(f"{A[i, c_]}({p[c_, 0]})" for c_ in range(3)) + f" = {rev[i, 0]}.", f"${rev[i, 0]}."],
             [f"${sum(A[i, :]) * sum(p)}", f"${(A.T * p)[i, 0]}", f"${sum(A[:, i]) * p[i, 0]}"], H(f"(Matrix({A.tolist()})*Matrix({p.tolist()}))[{i}, 0]"), why=["Multiplied the totals", "Used a column of S instead of a row", "Used one item only"], tags=["modeling"])


# ============================================================== S2 Add/subtract
@fam("012")
def s2_addsub(r, L):
    m, n = (2, 2) if L == 0 else pick(r, [(2, 2), (2, 3), (3, 2)])
    A, B = rmat(r, m, n), rmat(r, m, n)
    op = pick(r, ["+", "-"])
    if L == 2:
        a_, b_ = rint(r, -3, 4, True), rint(r, -3, 4, True)
        R = a_ * A + b_ * B
        expr = f"{T(a_) if a_ not in (1, -1) else ('-' if a_ == -1 else '')}A {'+' if b_ > 0 else '-'} {abs(b_) if abs(b_) != 1 else ''}B"
        w = [mat_text(a_ * A - b_ * B), mat_text(A + B), mat_text(a_ * A + B)]
        code = f"{a_}*Matrix({A.tolist()}) + {b_}*Matrix({B.tolist()})"
    else:
        R = A + B if op == "+" else A - B
        expr = f"A {op} B"
        w = [mat_text(A - B if op == "+" else A + B), mat_text(B - A) if op == "-" else mat_text(A + B + M_.ones(m, n)), mat_text((A + B if op == "+" else A - B).T) if m != n or True else ""]
        code = f"Matrix({A.tolist()}) {op} Matrix({B.tolist()})"
    need(mat_text(R) not in w and len(set(w)) == 3)
    return Q(f"A = {mat_text(A)} and B = {mat_text(B)}. Find {expr}.", mat_text(R), ["Matrices with the same dimensions combine entry by entry.", "Multiply by any scalars first." if L == 2 else f"{'Add' if op == '+' else 'Subtract'} corresponding entries.", mat_text(R) + "."],
             w, H(code, "matrix"), why=["Used the wrong operation (or sign)", "Subtracted in the wrong order" if op == "-" else "Made an arithmetic error", "Transposed the result"])


@fam("12")
def s2_solve(r, L):
    A, B = rmat(r, 2, 2), rmat(r, 2, 2)
    k_ = rint(r, 2, 4)
    X = (B - A) / k_
    need(all(v.q == 1 for v in X) or L == 2)
    return Q(f"Solve for X: {mat_text(A)} + {k_}X = {mat_text(B)}.", mat_text(X), [f"{k_}X = B - A = {mat_text(B - A)}.", f"X = (1/{k_})(B - A).", mat_text(X) + "."],
             [mat_text(B - A), mat_text((A - B) / k_), mat_text((B + A) / k_)], H(f"(Matrix({B.tolist()}) - Matrix({A.tolist()}))/{k_}", "matrix"), why=["Forgot to divide by the scalar", "Subtracted in the wrong order", "Added instead of subtracting"])


# ============================================================== S3 Multiplication
@fam("012")
def s3_product(r, L):
    if L == 0:
        A, B = rmat(r, 2, 2, -5, 5), rmat(r, 2, 2, -5, 5)
    else:
        m, n, p = pick(r, [(2, 3, 2), (2, 2, 3), (3, 2, 2), (2, 3, 3), (1, 3, 2)])
        A, B = rmat(r, m, n, -5, 5), rmat(r, n, p, -5, 5)
    R = A * B
    w = [mat_text(sp.matrix_multiply_elementwise(A, B)) if A.shape == B.shape else mat_text(B.T * A.T), mat_text(B * A) if B.shape[1] == A.shape[0] and (B * A).shape == R.shape and B * A != R else mat_text(R.T) if R.shape[0] == R.shape[1] and R.T != R else mat_text(R + M_.ones(*R.shape)),
         mat_text(R - 2 * M_.ones(*R.shape))]
    need(mat_text(R) not in w and len(set(w)) == 3)
    return Q(f"A = {mat_text(A)} and B = {mat_text(B)}. Find AB.", mat_text(R), [f"A is {A.shape[0]} × {A.shape[1]}, B is {B.shape[0]} × {B.shape[1]}, so AB is {R.shape[0]} × {R.shape[1]}.", "Entry (i, j) = row i of A · column j of B.", mat_text(R) + "."],
             w, H(f"Matrix({A.tolist()})*Matrix({B.tolist()})", "matrix"), why=["Multiplied entry by entry (or in the wrong order)", "Multiplied in the wrong order (BA)", "Made an arithmetic error"])


@fam("012")
def s3_defined(r, L):
    m, n = rint(r, 1, 4), rint(r, 1, 4)
    p, q_ = (n, rint(r, 1, 4)) if r.random() < 0.6 else (rint(r, 1, 4), rint(r, 1, 4))
    ans = f"{m} × {q_}" if n == p else "not defined"
    w = ([f"{n} × {p}", f"{p} × {m}" if (p, m) != (m, q_) else f"{q_} × {m}", "not defined"] if n == p else [f"{m} × {q_}", f"{n} × {p}", f"{m} × {p}"])
    w = [w_ for w_ in w if w_ != ans][:3]
    need(len(set(w)) == 3)
    return Q(f"A is {m} × {n} and B is {p} × {q_}. What are the dimensions of AB, or is it not defined?", ans, ["AB is defined when columns of A = rows of B.", f"{n} {'=' if n == p else '≠'} {p}.", f"AB is {ans}." if n == p else "AB is not defined."],
             w, PY("prod_dims", m=m, n=n, p=p, q=q_), why=["Used the inner dimensions", "Reversed the order", "Mixed up the dimensions"])


@fam("12")
def s3_scalar(r, L):
    A = rmat(r, 2, 3, -6, 6)
    k_ = sp.Rational(rint(r, -4, 4, True), pick(r, [1, 2]))
    need(all((k_ * v).q == 1 for v in A))
    return Q(f"Find {T(k_)}A for A = {mat_text(A)}.", mat_text(k_ * A), [f"Multiply every entry by {T(k_)}.", mat_text(k_ * A) + "."], [mat_text(A + k_ * M_.ones(2, 3)), mat_text(-k_ * A), mat_text(M_([[k_ * A[0, j] if j == 0 else A[0, j] for j in range(3)], [A[1, j] for j in range(3)]]))],
             H(f"{k_}*Matrix({A.tolist()})", "matrix"), why=["Added the scalar", "Made a sign error", "Multiplied only one entry"])


# ============================================================== S4 Augmented matrices and row operations
@fam("012")
def s4_augment(r, L):
    n_ = 2 if L == 0 else 3
    A = rmat(r, n_, n_, -6, 6)
    b = rmat(r, n_, 1, -12, 12)
    vs = ["x", "y", "z"][:n_]
    eqs = [T(sum(A[i, j] * sp.Symbol(vs[j]) for j in range(n_))) + f" = {b[i]}" for i in range(n_)]
    need(all(any(A[i, j] for j in range(n_)) for i in range(n_)))
    aug = A.row_join(b)
    return Q("Write the augmented matrix for the system: " + "; ".join(eqs) + ".", mat_text(aug), ["Each row holds the coefficients of one equation, then its constant.", "Use 0 for a missing variable.", mat_text(aug) + "."],
             [mat_text(A.T.row_join(b)), mat_text(A.row_join(-b)), mat_text(A)], PY("aug", code=f"Matrix({aug.tolist()})"), why=["Wrote the coefficients by columns", "Changed the signs of the constants", "Left out the constants"])


@fam("012")
def s4_rowop(r, L):
    A = rmat(r, 2 if L == 0 else 3, 3 if L == 0 else 4, -6, 6)
    nr = A.shape[0]
    i, j = r.sample(range(nr), 2)
    k_ = rint(r, -3, 3, True)
    B = A.copy()
    B[i, :] = A[i, :] + k_ * A[j, :]
    op = f"R{'₁₂₃'[i]} → R{'₁₂₃'[i]} {'+' if k_ > 0 else '-'} {abs(k_) if abs(k_) != 1 else ''}R{'₁₂₃'[j]}"
    W1 = A.copy(); W1[j, :] = A[j, :] + k_ * A[i, :]
    W2 = A.copy(); W2[i, :] = A[i, :] - k_ * A[j, :]
    W3 = A.copy(); W3[i, :] = k_ * A[j, :]
    return Q(f"Apply the row operation {op} to {mat_text(A)}.", mat_text(B), [f"Only row {i + 1} changes.", f"New row {i + 1} = row {i + 1} {'+' if k_ > 0 else '-'} {abs(k_)}·row {j + 1}.", mat_text(B) + "."],
             [mat_text(W1), mat_text(W2), mat_text(W3)], H(f"(lambda A: Matrix([[A[r_, c_] + ({k_}*A[{j}, c_] if r_ == {i} else 0) for c_ in range(A.cols)] for r_ in range(A.rows)]))(Matrix({A.tolist()}))", "matrix"),
             why=["Changed the wrong row", "Used the wrong sign", "Replaced the row instead of adding"])


# ============================================================== S5 RREF
@fam("012")
def s5_rref(r, L):
    n_ = 2 if L == 0 else 3
    sol = [rint(r, -5, 5) for _ in range(n_)]
    A = rmat(r, n_, n_, -4, 4)
    need(A.det() != 0)
    b = A * M_(sol)
    vs = ["x", "y", "z"][:n_]
    eqs = [T(sum(A[i, j] * sp.Symbol(vs[j]) for j in range(n_))) + f" = {b[i]}" for i in range(n_)]
    ans = "(" + ", ".join(map(str, sol)) + ")"
    return Q("Use the reduced row-echelon form of the augmented matrix (technology allowed) to solve: " + "; ".join(eqs) + ".", ans,
             ["Enter the augmented matrix and compute rref.", f"rref = {mat_text(M_.eye(n_).row_join(M_(sol)))}.", f"Solution: {ans}."],
             ["(" + ", ".join(str(-v) for v in sol) + ")", "(" + ", ".join(map(str, sol[::-1])) + ")", "(" + ", ".join(str(v) for v in b) + ")"], H(f"list(Matrix({A.tolist()}).solve(Matrix({b.tolist()})))", "point"),
             why=["Made sign errors", "Read the variables in reverse order", "Gave the constants"])


@fam("12")
def s5_interpret(r, L):
    kind = pick(r, ["unique", "none", "inf"])
    a_, b_, c_ = rint(r, -6, 6), rint(r, -6, 6), rint(r, -6, 6)
    if kind == "unique":
        R = M_([[1, 0, 0, a_], [0, 1, 0, b_], [0, 0, 1, c_]])
        ans = f"one solution: ({a_}, {b_}, {c_})"
    elif kind == "none":
        R = M_([[1, 0, a_, b_], [0, 1, c_, rint(r, -5, 5)], [0, 0, 0, rint(r, 1, 5)]])
        ans = "no solution"
    else:
        R = M_([[1, 0, a_, b_], [0, 1, c_, rint(r, -5, 5)], [0, 0, 0, 0]])
        ans = "infinitely many solutions"
    opts = ["no solution", "infinitely many solutions", f"one solution: ({a_}, {b_}, {c_})", f"one solution: ({R[0, 3]}, {R[1, 3]}, {R[2, 3]})" if kind != "unique" else f"one solution: ({c_}, {b_}, {a_})"]
    if kind != "unique":
        opts[2] = f"one solution: ({R[0, 3]}, {R[1, 3]}, 0)"
    need(len(set(opts)) == 4 and ans in opts)
    return Q(f"The reduced row-echelon form of a system's augmented matrix (variables x, y, z) is {mat_text(R)}. Describe the solution set.", ans,
             ["Look at the last row.", {"unique": "Each variable has a leading 1: read off the solution.", "none": "0 = nonzero is impossible: no solution.", "inf": "A row of zeros leaves a free variable: infinitely many solutions."}[kind]],
             [o for o in opts if o != ans][:3], PY("rref_kind", code=f"Matrix({R.tolist()})"), why=["Misread the last row", "Ignored the free variable", "Read the wrong column"], mode="mc")


# ============================================================== S6 Networks
@fam("012")
def s6_network(r, L):
    n_ = pick(r, [3, 4]) if L == 0 else pick(r, [4, 4, 5])
    names = "ABCDE"[:n_]
    for _ in range(40):
        A = M_(n_, n_, lambda i, j: 0 if i == j else (1 if r.random() < 0.55 else 0))
        A = (A + A.T).applyfunc(lambda v: 1 if v else 0) if L < 2 else A
        if all(any(A[i, j] for j in range(n_)) for i in range(n_)):
            break
    else:
        raise Reject()
    edges = [f"{names[i]}{'–' if L < 2 else '→'}{names[j]}" for i in range(n_) for j in range(n_) if A[i, j] and (L == 2 or i < j)]
    i, j = r.sample(range(n_), 2)
    A2 = A * A
    if L == 0 and r.random() < 0.5:
        return Q(f"A network has {'roads' if L < 2 else 'one-way flights'}: {', '.join(edges)}. Write its adjacency matrix (order {', '.join(names)}).", mat_text(A),
                 ["Entry (i, j) is 1 if there is a direct connection from i to j, otherwise 0.", "Diagonal entries are 0 (no loops).", mat_text(A) + "."],
                 [mat_text(A + M_.eye(n_)), mat_text(M_.ones(n_, n_) - A), mat_text(A * A)], H(f"Matrix({A.tolist()})", "matrix"), why=["Put 1s on the diagonal", "Swapped connections and non-connections", "Squared the matrix"])
    return Q(f"A network has {'two-way roads' if L < 2 else 'one-way flights'}: {', '.join(edges)}. How many routes of exactly two legs go from {names[i]} to {names[j]}?", str(A2[i, j]),
             ["Write the adjacency matrix A.", "Entry (i, j) of A² counts two-step paths.", f"(A²) at {names[i]}→{names[j]} = {A2[i, j]}."],
             [str(A[i, j]), str(A2[j, i] + 1) if A2[j, i] + 1 != A2[i, j] else str(A2[i, j] + 2), str(sum(A2[i, :]))], PY("two_step", code=f"Matrix({A.tolist()})", i=i, j=j),
             why=["Counted direct connections", "Made an arithmetic error", "Added all two-step routes from the start"], tags=["modeling"])


# ============================================================== S7 Identity and inverse
@fam("012")
def s7_inverse(r, L):
    A = inv2(r, L)
    Ai = A.inv()
    d = A.det()
    adj = M_([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])
    return Q(f"Find the inverse of A = {mat_text(A)}.", mat_text(Ai), [f"det A = ({A[0, 0]})({A[1, 1]}) - ({A[0, 1]})({A[1, 0]}) = {d}.", "A⁻¹ = (1/det A)[d, -b; -c, a].", mat_text(Ai) + "."],
             [mat_text(adj), mat_text(M_([[1 / v if v else 0 for v in A.row(i)] for i in range(2)])) if all(A) else mat_text(-Ai), mat_text(M_([[A[1, 1], A[0, 1]], [A[1, 0], A[0, 0]]]) / d)],
             H(f"Matrix({A.tolist()}).inv()", "matrix"), why=["Forgot to divide by the determinant", "Took reciprocals of the entries", "Forgot to negate b and c"])


@fam("012")
def s7_check(r, L):
    A = inv2(r, 0 if L == 0 else 1)
    good = r.random() < 0.5
    B = A.inv() if good else A.inv() + M_([[0, 0], [0, pick(r, [1, -1])]]) if L else M_([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]]) * (1 if A.det() not in (1,) else -1)
    if not good:
        need(A * B != M_.eye(2))
    return Q(f"Is B = {mat_text(B)} the inverse of A = {mat_text(A)}?", "Yes" if good else "No", ["B is the inverse if AB = I.", f"AB = {mat_text(A * B)}.", "Yes." if good else "No: AB ≠ I."], ["No" if good else "Yes"],
             H(f"'Yes' if Matrix({A.tolist()})*P_matrix('{mat_text(B)}') == eye(2) else 'No'", "text"), mode="sa", why=["Did not multiply to check"])


# ============================================================== S8 Determinants
@fam("012")
def s8_det(r, L):
    n_ = 2 if L == 0 else 3 if L == 2 or r.random() < 0.5 else 2
    A = rmat(r, n_, n_, -6, 6)
    d = A.det()
    if n_ == 2:
        w = [A[0, 0] * A[1, 1] + A[0, 1] * A[1, 0], A[0, 1] * A[1, 0] - A[0, 0] * A[1, 1], A[0, 0] * A[1, 1]]
    else:
        w = [sum(A[0, j] * A[1, (j + 1) % 3] * A[2, (j + 2) % 3] for j in range(3)), -d, d + 2 * A[0, 1] * (A[1, 0] * A[2, 2] - A[1, 2] * A[2, 0])]
    need(d not in w and len(set(w)) == 3)
    return Q(f"Find the determinant of {mat_text(A)}.", str(d), (["det = ad - bc."] if n_ == 2 else ["Expand along row 1: a(ei - fh) - b(di - fg) + c(dh - eg)."]) + [f"det = {d}."], [str(v) for v in w],
             H(f"Matrix({A.tolist()}).det()"), why=["Added instead of subtracting" if n_ == 2 else "Used only the downward diagonals", "Subtracted in the wrong order", "Forgot the second product" if n_ == 2 else "Forgot the alternating sign"])


@fam("12")
def s8_area(r, L):
    pts = [(rint(r, -6, 6), rint(r, -6, 6)) for _ in range(3)]
    (x1, y1), (x2, y2), (x3, y3) = pts
    d = M_([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1]]).det()
    need(d != 0)
    v = sp.Rational(abs(d), 2)
    return Q(f"Use a determinant to find the area of the triangle with vertices ({x1}, {y1}), ({x2}, {y2}), and ({x3}, {y3}).", T(v) + " units²",
             ["Area = (1/2)|det[x₁, y₁, 1; x₂, y₂, 1; x₃, y₃, 1]|.", f"det = {d}.", f"Area = {T(v)} units²."], [str(abs(d)) + " units²", T(sp.Rational(d, 2)) + " units²" if d < 0 else T(v + 1) + " units²", T(sp.Rational(abs(d), 4)) + " units²"],
             H(f"Abs(Matrix([[{x1}, {y1}, 1], [{x2}, {y2}, 1], [{x3}, {y3}, 1]]).det())/2"), why=["Forgot the 1/2", "Kept the negative sign" if d < 0 else "Made an arithmetic error", "Divided by 4"])


# ============================================================== S9 Geometric transformations
TRANS = {"reflection over the x-axis": M_([[1, 0], [0, -1]]), "reflection over the y-axis": M_([[-1, 0], [0, 1]]), "reflection over y = x": M_([[0, 1], [1, 0]]),
         "rotation of 90° counterclockwise": M_([[0, -1], [1, 0]]), "rotation of 180°": M_([[-1, 0], [0, -1]]), "rotation of 270° counterclockwise": M_([[0, 1], [-1, 0]]), "reflection over y = -x": M_([[0, -1], [-1, 0]])}


@fam("012")
def s9_apply(r, L):
    nm = pick(r, list(TRANS))
    T_ = TRANS[nm]
    if L == 2 and r.random() < 0.5:
        k_ = rint(r, 2, 4)
        T_ = k_ * T_
        nm = f"{nm} followed by a dilation by a factor of {k_}"
    P_ = M_([[rint(r, -6, 6) for _ in range(3)], [rint(r, -6, 6) for _ in range(3)]])
    need(len({tuple(P_[:, j]) for j in range(3)}) == 3)
    R = T_ * P_
    if L == 0:
        p = P_[:, 0]
        ans = f"({R[0, 0]}, {R[1, 0]})"
        return Q(f"Use the matrix for a {nm}, {mat_text(T_)}, to find the image of ({p[0]}, {p[1]}).", ans, ["Multiply the transformation matrix by the column vector [x; y].", f"{mat_text(T_)}[{p[0]}; {p[1]}] = [{R[0, 0]}; {R[1, 0]}].", ans + "."],
                 [f"({(T_.T * p)[0]}, {(T_.T * p)[1]})" if T_.T != T_ else f"({-R[0, 0]}, {-R[1, 0]})", f"({p[1]}, {p[0]})" if (p[1], p[0]) != (R[0, 0], R[1, 0]) else f"({-p[1]}, {-p[0]})", f"({-p[0]}, {-p[1]})" if (-p[0], -p[1]) != (R[0, 0], R[1, 0]) else f"({p[0]}, {-p[1]})"],
                 H(f"list(Matrix({T_.tolist()})*Matrix([{p[0]}, {p[1]}]))", "point"), why=["Multiplied by the transpose", "Swapped the coordinates", "Negated both coordinates"])
    return Q(f"The vertices of a triangle are the columns of {mat_text(P_)}. Find the vertex matrix of its image under a {nm}.", mat_text(R),
             [f"Transformation matrix: {mat_text(T_)}.", "Multiply it on the left of the vertex matrix.", mat_text(R) + "."], [mat_text(T_.T * P_) if T_.T != T_ else mat_text(-R), mat_text(-P_) if -P_ != R else mat_text(P_), mat_text(R + M_.ones(2, 3))],
             H(f"Matrix({T_.tolist()})*Matrix({P_.tolist()})", "matrix"), why=["Used the transpose (the inverse rotation)", "Negated every coordinate", "Made an arithmetic error"])


@fam("12")
def s9_area_scale(r, L):
    T_ = rmat(r, 2, 2, -4, 4)
    d = T_.det()
    need(d != 0)
    A0 = rint(r, 3, 30)
    return Q(f"A figure with area {A0} units² is transformed by {mat_text(T_)}. What is the area of the image?", f"{abs(d) * A0} units²", ["The area scale factor is |det|.", f"det = {d}.", f"Area = {abs(d)} · {A0} = {abs(d) * A0} units²."],
             [f"{d * A0} units²" if d < 0 else f"{(d + 1) * A0} units²", f"{A0} units²", f"{d * d * A0} units²"], H(f"Abs(Matrix({T_.tolist()}).det())*{A0}"), why=["Kept the sign of the determinant" if d < 0 else "Made an arithmetic error", "Thought the area is unchanged", "Squared the determinant"])


# ============================================================== S10 Modeling motion
@fam("012")
def s10_motion(r, L):
    A_ = pick(r, list(TRANS))
    B_ = pick(r, [k_ for k_ in TRANS if k_ != A_])
    p = M_([rint(r, -6, 6), rint(r, -6, 6)])
    need(p[0] != p[1] and p[0] != -p[1])
    if L == 0 or (L == 2 and r.random() < 0.6):
        v = M_([rint(r, -5, 5), rint(r, -5, 5)])
        need(any(v))
        if L == 2:
            kd = rint(r, 2, 3)
            A_ = f"{A_} combined with a dilation by {kd}"
            TRANS_ = dict(TRANS)
            TRANS_[A_] = kd * TRANS[A_.split(" combined")[0]]
        else:
            TRANS_ = TRANS
        R = TRANS_[A_] * p + v
        ans = f"({R[0]}, {R[1]})"
        return Q(f"A game sprite at ({p[0]}, {p[1]}) undergoes a {A_} (matrix {mat_text(TRANS_[A_])}) and then moves by the translation vector ⟨{v[0]}, {v[1]}⟩. Where does it end up?", ans,
                 ["First multiply by the matrix.", f"{mat_text(TRANS_[A_])}[{p[0]}; {p[1]}] = [{(TRANS_[A_] * p)[0]}; {(TRANS_[A_] * p)[1]}].", f"Then add ⟨{v[0]}, {v[1]}⟩: {ans}."],
                 [f"({(TRANS_[A_] * (p + v))[0]}, {(TRANS_[A_] * (p + v))[1]})", f"({(TRANS_[A_] * p - v)[0]}, {(TRANS_[A_] * p - v)[1]})", f"({(p + v)[0]}, {(p + v)[1]})"],
                 H(f"list(Matrix({TRANS_[A_].tolist()})*Matrix({p.tolist()}) + Matrix({v.tolist()}))", "point"), why=["Translated before transforming", "Subtracted the translation", "Skipped the matrix"], tags=["modeling"])
    C_ = TRANS[B_] * TRANS[A_]
    need(C_ != TRANS[A_] * TRANS[B_] or L == 1)
    if L == 1:
        R = C_ * p
        ans = f"({R[0]}, {R[1]})"
        return Q(f"A point at ({p[0]}, {p[1]}) undergoes a {A_}, then a {B_}. Find its final position.", ans, [f"First: {mat_text(TRANS[A_])}.", f"Then: {mat_text(TRANS[B_])}.", f"Final: {ans}."],
                 [f"({(TRANS[A_] * TRANS[B_] * p)[0]}, {(TRANS[A_] * TRANS[B_] * p)[1]})" if TRANS[A_] * TRANS[B_] != C_ else f"({-R[0]}, {-R[1]})", f"({(TRANS[A_] * p)[0]}, {(TRANS[A_] * p)[1]})", f"({(TRANS[B_] * p)[0]}, {(TRANS[B_] * p)[1]})"],
                 H(f"list(Matrix({TRANS[B_].tolist()})*(Matrix({TRANS[A_].tolist()})*Matrix({p.tolist()})))", "point"), why=["Applied the transformations in the wrong order", "Stopped after the first transformation", "Applied only the second transformation"], tags=["modeling"])
    return Q(f"Write the single matrix for a {A_} followed by a {B_}.", mat_text(C_), [f"First matrix M₁ = {mat_text(TRANS[A_])}; second M₂ = {mat_text(TRANS[B_])}.", "The composite is M₂M₁ (the first transformation is on the right).", mat_text(C_) + "."],
             [mat_text(TRANS[A_] * TRANS[B_]), mat_text(TRANS[A_] + TRANS[B_]), mat_text(-C_)], H(f"Matrix({TRANS[B_].tolist()})*Matrix({TRANS[A_].tolist()})", "matrix"),
             why=["Multiplied in the wrong order", "Added the matrices", "Made a sign error"], tags=["modeling"])


# ============================================================== S11 Matrix equations
@fam("012")
def s11_system(r, L):
    n_ = 2 if L < 2 else 3
    sol = M_([rint(r, -6, 6) for _ in range(n_)])
    if n_ == 2:
        A = inv2(r, 0 if L == 0 else 1)
    else:
        A = M_.eye(3)
        for _ in range(5):
            i_, j_ = r.sample(range(3), 2)
            A[i_, :] = A[i_, :] + rint(r, -2, 2, True) * A[j_, :]
        if r.random() < 0.5:
            A[0, :], A[2, :] = A[2, :], A[0, :]
        need(max(abs(v) for v in A) <= 6 and sum(1 for v in A if v == 0) <= 3)
    b = A * sol
    ans = "(" + ", ".join(map(str, sol)) + ")"
    vs = ["x", "y", "z"][:n_]
    sys_ = "; ".join(T(sum(A[i, j] * sp.Symbol(vs[j]) for j in range(n_))) + f" = {b[i]}" for i in range(n_))
    wrong1 = list(A.inv().T * b)
    wrong2 = list(A * b)
    return Q(f"Write the system as AX = B and solve with X = A⁻¹B: {sys_}.", ans, [f"A = {mat_text(A)}, B = {mat_text(b)}.", "X = A⁻¹B (multiply on the left).", f"X = {ans}."],
             ["(" + ", ".join(T(v) for v in wrong1) + ")" if wrong1 != list(sol) else "(" + ", ".join(str(-v) for v in sol) + ")", "(" + ", ".join(map(str, wrong2)) + ")", "(" + ", ".join(map(str, sol[::-1])) + ")" if list(sol[::-1]) != list(sol) else "(" + ", ".join(str(v + 1) for v in sol) + ")"],
             H(f"list(Matrix({A.tolist()}).inv()*Matrix({b.tolist()}))", "point"), why=["Used the transpose of A⁻¹", "Multiplied by A instead of A⁻¹", "Listed the variables in the wrong order"])


@fam("12", mode="mc")
def s11_singular(r, L):
    a_, b_ = rint(r, -6, 6, True), rint(r, -6, 6, True)
    k_ = rint(r, -3, 3, True)
    need(k_ != 1)
    A = M_([[a_, b_], [k_ * a_, k_ * b_]]) if r.random() < 0.5 else M_([[a_, b_], [rint(r, -6, 6), rint(r, -6, 6)]])
    d = A.det()
    ans = "A has no inverse, so X = A⁻¹B cannot be used" if d == 0 else "A has an inverse, so X = A⁻¹B gives the unique solution"
    opts = [("A has no inverse, so X = A⁻¹B cannot be used", d == 0), ("A has an inverse, so X = A⁻¹B gives the unique solution", d != 0), ("Every 2 × 2 matrix has an inverse", False), ("The inverse exists only when det A = 0", False)]
    return Q(f"For the system AX = B with A = {mat_text(A)}, which statement is true?", ans, [f"det A = {d}.", "A⁻¹ exists exactly when det A ≠ 0."], options=opts, chk=PY("singular", code=f"Matrix({A.tolist()})"), mode="mc", tags=["reasoning"])


SKILLS = {
    1: dict(name="Matrix Notation and Organizing Data", std=["N-VM.C.6"], fams=[s1_dims, s1_data], extra=[err_of(s1_dims), open_of(s1_dims)]),
    2: dict(name="Adding and Subtracting Matrices", std=["N-VM.C.8"], fams=[s2_addsub, s2_solve], extra=[err_of(s2_addsub), open_of(s2_addsub)]),
    3: dict(name="Scalar and Matrix Multiplication", std=["N-VM.C.7", "N-VM.C.8"], fams=[s3_product, s3_defined, s3_scalar], extra=[err_of(s3_product), open_of(s3_defined)]),
    4: dict(name="Augmented Matrices and Row Reduction", std=["A-REI.C.8"], fams=[s4_augment, s4_rowop], extra=[err_of(s4_rowop), open_of(s4_rowop)]),
    5: dict(name="Reduced Row Echelon Form with Technology", std=["A-REI.C.9"], fams=[s5_rref, s5_interpret], extra=[err_of(s5_rref), open_of(s5_rref)]),
    6: dict(name="Networks and Matrix Models", std=["N-VM.C.6"], fams=[s6_network], extra=[err_of(s6_network), open_of(s6_network)]),
    7: dict(name="Identity and Inverse Matrices", std=["N-VM.C.10", "A-REI.C.9"], fams=[s7_inverse, s7_check], extra=[err_of(s7_inverse), open_of(s7_inverse)]),
    8: dict(name="Determinants of 2 by 2 and 3 by 3 Matrices", std=["N-VM.C.10", "N-VM.C.12"], fams=[s8_det, s8_area], extra=[err_of(s8_det), open_of(s8_det)]),
    9: dict(name="Geometric Transformations with Matrices", std=["N-VM.C.12"], fams=[s9_apply, s9_area_scale], extra=[err_of(s9_apply), open_of(s9_apply)]),
    10: dict(name="Modeling Motion with Matrices", std=["N-VM.C.6", "N-VM.C.12"], fams=[s10_motion], extra=[err_of(s10_motion), open_of(s10_motion)]),
    11: dict(name="Solving Systems with Matrix Equations", std=["A-REI.C.9"], fams=[s11_system, s11_singular], extra=[err_of(s11_system), open_of(s11_system)]),
}
