# Teaching notes, units 6–9 (format as in u1_u2.py).
MA = 'matrices'
VE = 'vectors'
PR = 'probability'
SQ = 'sequences-series-limits'
R = {}

R[MA, 1] = dict(obj='use matrix notation to name entries and dimensions and organize data in a matrix',
  idea='An m × n matrix has m rows and n columns; aᵢⱼ is the entry in row i, column j.',
  voc=[['dimensions', 'm × n: rows by columns.'], ['entry aᵢⱼ', 'The number in row i and column j.'], ['square matrix', 'A matrix with the same number of rows and columns.']],
  watch='Reading aᵢⱼ as column i, row j.',
  cards=[dict(h='Matrix notation', big='{{Rows first, then columns}}: dimensions ⟨m \\times n⟩ and entry ⟨a_{ij}⟩ in row ⟨i⟩, column ⟨j⟩. In a data matrix each row is one category and each column another.',
    steps=['⟨A = [-9, 1, 1, -7; -5, 1, -3, 1]⟩ is ⟨{{2 \\times 4}}⟩.', '⟨a_{21}⟩ is row 2, column 1: ⟨{{-5}}⟩.', 'Sales matrix with rows North, South, East and columns shirts, hats, jackets: hats sold in the East is row {{3}}, column {{2}}.'])])

R[MA, 2] = dict(obj='add and subtract matrices of the same dimensions',
  idea='Matrices of the same size are added or subtracted entry by entry.',
  voc=[['same dimensions', 'Required for addition and subtraction.'], ['corresponding entries', 'Entries in the same row and column.'], ['zero matrix', 'A matrix of all zeros; adding it changes nothing.']],
  watch='Subtracting only the first column, or adding matrices of different sizes.',
  cards=[dict(h='Adding and subtracting matrices', big='Check the {{dimensions match}}, then add or subtract each pair of {{corresponding entries}}.',
    steps=['⟨[-9, 9; -5, -8] - [-3, 2; -8, -6] = [{{-6}}, 7; 3, {{-2}}]⟩.', '⟨[-7, 2; -4, 7] + [1, -3; -2, 0] = [-6, -1; -6, {{7}}]⟩.', 'A ⟨2 \\times 3⟩ plus a ⟨3 \\times 2⟩ is {{not defined}}.'])])

R[MA, 3] = dict(obj='multiply a matrix by a scalar and multiply two matrices',
  idea='Entry (i, j) of AB is row i of A times column j of B; AB exists only when A has as many columns as B has rows, and AB is usually not BA.',
  voc=[['scalar multiple', 'kA: every entry multiplied by k.'], ['matrix product', 'AB, rows of A times columns of B.'], ['inner dimensions', 'The columns of A and rows of B, which must match.']],
  watch='Multiplying matrices entry by entry.',
  cards=[dict(h='Matrix multiplication', big='⟨(m \\times n)(n \\times p) = (m \\times p)⟩: the {{inner}} dimensions must match. Each entry is a {{row times a column}}.',
    steps=['⟨[-1, 5; 3, 0][-4, 3; -4, 1]⟩: row 1·col 1 ⟨= 4 - 20 = {{-16}}⟩.', 'Full product ⟨[-16, 2; -12, 9]⟩.', '⟨(2 \\times 4)(3 \\times 1)⟩: ⟨4 \\ne 3⟩ → {{not defined}}.'])])

R[MA, 4] = dict(obj='write augmented matrices and apply row operations to solve systems',
  idea='An augmented matrix stores the coefficients and constants of a system; row operations (swap, scale, add a multiple) do not change the solutions.',
  voc=[['augmented matrix', 'The coefficient matrix with the constants as an extra column.'], ['row operation', 'Swap two rows, multiply a row by a nonzero number, or add a multiple of one row to another.'], ['row echelon form', 'Zeros below each leading entry.']],
  watch='Applying a row operation to only some entries of the row.',
  cards=[dict(h='Augmented matrices', big='Each equation is a {{row}}; the last column holds the {{constants}}. ⟨R_1 \\to R_1 + 2R_2⟩ replaces row 1 with row 1 plus twice row 2.',
    steps=['⟨4x - 4y = 4⟩, ⟨-5x - 2y = 12⟩ → ⟨[4, -4, 4; -5, -2, 12]⟩.', '⟨R_1 \\to R_1 + 2R_2⟩ on ⟨[5, -3, 4; 6, -1, 1]⟩: ⟨R_1 = [{{17}}, {{-5}}, {{6}}]⟩.', 'Row 2 is unchanged: ⟨[6, -1, 1]⟩.'])])

R[MA, 5] = dict(obj='solve systems with reduced row-echelon form using technology',
  idea='In reduced row-echelon form each leading entry is 1 with zeros above and below, so the solution can be read directly.',
  voc=[['reduced row-echelon form', 'Leading 1s, with zeros above and below each one.'], ['rref', 'The calculator command that returns reduced row-echelon form.'], ['pivot', 'A leading 1.']],
  watch='Reading the solution from the wrong column of the rref result.',
  cards=[dict(h='Reduced row-echelon form', big='Enter the {{augmented matrix}}, apply rref, and read each variable from the last column. A row ⟨[0, 0, 1]⟩ means {{no solution}}.',
    steps=['⟨3x - 4y = -15⟩, ⟨x + y = -5⟩: rref ⟨[1, 0, -5; 0, 1, 0]⟩.', 'Solution ⟨({{-5}}, {{0}})⟩.', '⟨-4x + y + 3z = 28⟩, ⟨-2x - 3y - 3z = -8⟩, ⟨4x + 4y - z = -1⟩: ⟨({{-5}}, 5, 1)⟩.'])])

R[MA, 6] = dict(obj='model networks with adjacency matrices and count paths with matrix powers',
  idea='Entry (i, j) of an adjacency matrix is 1 when i and j are connected; entry (i, j) of Aⁿ counts the paths of length n.',
  voc=[['adjacency matrix', 'A square matrix of 0s and 1s recording direct connections.'], ['network', 'Points (vertices) joined by connections (edges).'], ['path of length n', 'A route that uses n edges.']],
  watch='Making an undirected adjacency matrix that is not symmetric.',
  cards=[dict(h='Networks and matrices', big='Put a {{1}} for a direct connection and 0 otherwise; for two-way roads the matrix is {{symmetric}}. ⟨A^2⟩ counts two-step routes.',
    steps=['Roads A–B, B–C (order A, B, C): ⟨[0, 1, 0; 1, 0, 1; 0, 1, 0]⟩.', 'In ⟨A^2⟩, entry (A, C) is ⟨{{1}}⟩: one two-step route A → B → C.', 'Entry (B, B) of ⟨A^2⟩ is ⟨{{2}}⟩: B → A → B and B → C → B.'])])

R[MA, 7] = dict(obj='find the inverse of a 2 × 2 matrix and verify inverses',
  idea='For A = [a, b; c, d], A⁻¹ = (1/(ad − bc))·[d, −b; −c, a] when ad − bc ≠ 0; AA⁻¹ = I.',
  voc=[['identity matrix', 'I = [1, 0; 0, 1]; AI = IA = A.'], ['inverse matrix', 'A⁻¹ with AA⁻¹ = A⁻¹A = I.'], ['singular matrix', 'A matrix with determinant 0 and no inverse.']],
  watch='Swapping b and c instead of a and d, or forgetting to divide by the determinant.',
  cards=[dict(h='Inverse matrices', big='⟨A^{-1} = \\frac{1}{ad - bc}\\begin{bmatrix} d & -b \\\\ -c & a \\end{bmatrix}⟩: {{swap}} ⟨a⟩ and ⟨d⟩, {{negate}} ⟨b⟩ and ⟨c⟩, divide by the determinant. Check: ⟨AA^{-1} = I⟩.',
    steps=['⟨A = [1, -5; -1, 6]⟩: ⟨\\det A = 6 - 5 = 1⟩.', '⟨A^{-1} = [{{6}}, {{5}}; 1, 1]⟩.', 'Is ⟨[2, 3; 3, 4]⟩ the inverse of ⟨[4, -3; -3, 2]⟩? ⟨8 - 9 = -1⟩ in the corner → {{no}}.'])])

R[MA, 8] = dict(obj='evaluate 2 × 2 and 3 × 3 determinants and use them for invertibility and area',
  idea='det[a, b; c, d] = ad − bc; a matrix is invertible exactly when its determinant is not 0, and |det| of two vectors gives a parallelogram’s area.',
  voc=[['determinant', 'A number computed from a square matrix.'], ['cofactor expansion', 'Expanding a 3 × 3 determinant along a row.'], ['invertible', 'Having an inverse; det ≠ 0.']],
  watch='Computing ad + bc or ac − bd.',
  cards=[dict(h='Determinants', big='⟨\\det\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} = {{ad - bc}}⟩. ⟨\\det = 0⟩ → {{no inverse}}. Area of the parallelogram from ⟨\\langle a, c\\rangle⟩ and ⟨\\langle b, d\\rangle⟩: ⟨|ad - bc|⟩.',
    steps=['⟨\\det[4, 5; -3, -5] = -20 - (-15) = {{-5}}⟩.', '⟨[k, 6; 4, 4]⟩ has no inverse when ⟨4k - 24 = 0⟩, ⟨k = {{6}}⟩.', 'Vectors ⟨\\langle 1, -3\\rangle⟩, ⟨\\langle 3, 5\\rangle⟩: area ⟨|5 + 9| = {{14}}⟩.'])])

R[MA, 9] = dict(obj='use matrices to reflect, rotate and dilate points and figures',
  idea='Multiplying a transformation matrix by a point’s column vector gives the image point.',
  voc=[['transformation matrix', 'A 2 × 2 matrix that maps points to images.'], ['reflection over y = x', '[0, 1; 1, 0] swaps the coordinates.'], ['dilation', 'kI, which multiplies both coordinates by k.']],
  watch='Multiplying the point on the left (as a row) by the matrix.',
  cards=[dict(h='Transformations with matrices', big='Image ⟨= M \\begin{bmatrix} x \\\\ y \\end{bmatrix}⟩. Reflect over x-axis ⟨[1, 0; 0, -1]⟩, over y = x ⟨[0, 1; 1, 0]⟩, rotate 90° ⟨[0, -1; 1, 0]⟩.',
    steps=['⟨[0, 1; 1, 0]⟩ on ⟨(-2, 3)⟩: ⟨({{3}}, {{-2}})⟩.', '⟨[1, 0; 0, -1]⟩ on ⟨(-3, 6)⟩: ⟨(-3, {{-6}})⟩.', 'Dilation ⟨2I⟩ on ⟨(4, -1)⟩: ⟨({{8}}, {{-2}})⟩.'])])

R[MA, 10] = dict(obj='model motion with matrix transformations followed by translations',
  idea='Apply the matrix first, then add the translation vector: image = Mp + t.',
  voc=[['translation vector', 'The shift ⟨h, k⟩ added after the transformation.'], ['composition of transformations', 'Doing one transformation after another.'], ['sprite', 'A figure moved on a screen.']],
  watch='Translating before applying the matrix when the order says matrix first.',
  cards=[dict(h='Modeling motion', big='Order matters: {{transform}}, then {{translate}}. Image ⟨= Mp + t⟩.',
    steps=['Sprite at ⟨(-6, 3)⟩, rotate 270° with ⟨[0, 1; -1, 0]⟩: ⟨(3, 6)⟩.', 'Then move by ⟨\\langle -1, -2\\rangle⟩: ⟨({{2}}, {{4}})⟩.', 'Reflect ⟨(0, 5)⟩ over the y-axis, then move ⟨\\langle 2, 3\\rangle⟩: ⟨({{2}}, {{8}})⟩.'])])

R[MA, 11] = dict(obj='write systems as matrix equations AX = B and solve with X = A⁻¹B',
  idea='A system with coefficient matrix A and constant column B has the unique solution X = A⁻¹B when det A ≠ 0.',
  voc=[['coefficient matrix', 'A, the coefficients of the variables.'], ['variable matrix', 'X, the column of unknowns.'], ['constant matrix', 'B, the column of right-hand sides.']],
  watch='Computing BA⁻¹ instead of A⁻¹B.',
  cards=[dict(h='Matrix equations', big='⟨AX = B \\Rightarrow X = {{A^{-1}B}}⟩ (multiply on the left). If ⟨\\det A = 0⟩ there is no unique solution.',
    steps=['⟨-x + 3y = 5⟩, ⟨2x - 5y = -7⟩: ⟨A = [-1, 3; 2, -5]⟩, ⟨\\det A = 5 - 6 = -1⟩.', '⟨A^{-1} = [5, 3; 2, 1]⟩.', '⟨X = A^{-1}B = [5(5) + 3(-7); 2(5) + 1(-7)] = ({{4}}, {{3}})⟩.'])])

# ------------------------------------------------------------------ vectors, complex numbers, polar
R[VE, 1] = dict(obj='add, subtract, multiply and divide complex numbers and solve quadratics with complex zeros',
  idea='Treat i like a variable and replace i² with −1; a negative discriminant gives the conjugate pair (−b ± i√|D|)/(2a).',
  voc=[['imaginary unit', 'i, with i² = −1.'], ['complex conjugate', 'a − bi for a + bi.'], ['standard form', 'a + bi.']],
  watch='Writing i² as 1, or dropping the i when simplifying √(−n).',
  cards=[dict(h='Complex numbers', big='Multiply like binomials and replace ⟨i^2⟩ with {{−1}}. To divide, multiply by the {{conjugate}} of the denominator.',
    steps=['⟨(2 + i)(4 - 6i) = 8 - 12i + 4i - 6i^2 = {{14 - 8i}}⟩.', '⟨x^2 - 8x + 25 = 0⟩: ⟨D = 64 - 100 = -36⟩.', '⟨x = \\frac{8 \\pm 6i}{2} = {{4 \\pm 3i}}⟩.'])])

R[VE, 2] = dict(obj='find modulus, distance and midpoint in the complex plane',
  idea='a + bi is the point (a, b); its modulus |a + bi| = √(a² + b²) is its distance from 0, and distances and midpoints work as for points.',
  voc=[['complex plane', 'Real part on the horizontal axis, imaginary part on the vertical axis.'], ['modulus', '|a + bi| = √(a² + b²).'], ['midpoint', '((a₁ + a₂)/2) + ((b₁ + b₂)/2)i.']],
  watch='Including i inside the square root, as in √(a² + (bi)²).',
  cards=[dict(h='The complex plane', big='Plot ⟨a + bi⟩ at ⟨(a, b)⟩. Modulus ⟨|a + bi| = \\sqrt{a^2 + b^2}⟩. Distance between two numbers = {{modulus of their difference}}.',
    steps=['⟨|8 + 15i| = \\sqrt{64 + 225} = {{17}}⟩.', 'Distance from ⟨-5 - 5i⟩ to ⟨4 - 6i⟩: ⟨|9 - i| = {{\\sqrt{82}}}⟩.', 'Midpoint of ⟨3 + 7i⟩ and ⟨1 - 3i⟩: ⟨{{2 + 2i}}⟩.'])])

R[VE, 3] = dict(obj='represent vectors geometrically, find component form and add vectors',
  idea='A vector has magnitude and direction; from P to Q its components are ⟨x₂ − x₁, y₂ − y₁⟩, and vectors add tip to tail.',
  voc=[['vector', 'A quantity with magnitude and direction.'], ['component form', '⟨a, b⟩: horizontal and vertical change.'], ['resultant', 'The sum of two or more vectors.']],
  watch='Subtracting initial minus terminal (Q − P reversed).',
  cards=[dict(h='Geometric vectors', big='Components = {{terminal − initial}}. The resultant of perpendicular velocities has speed ⟨\\sqrt{a^2 + b^2}⟩.',
    steps=['From ⟨P(0, 2)⟩ to ⟨Q(1, -8)⟩: ⟨\\langle {{1}}, {{-10}}\\rangle⟩.', 'Boat 7 km/h east, current 10 km/h north: ⟨\\sqrt{49 + 100} \\approx {{12.2}}⟩ km/h.', 'Displacement from (−1, 2) to (11, −3): ⟨\\langle 12, -5\\rangle⟩, length ⟨{{13}}⟩.'])])

R[VE, 4] = dict(obj='add, subtract and scale vectors in component form and write vectors from magnitude and direction',
  idea='Work component by component; a vector with magnitude r and direction angle θ is ⟨r cos θ, r sin θ⟩.',
  voc=[['scalar multiplication', 'k⟨a, b⟩ = ⟨ka, kb⟩.'], ['direction angle', 'The angle from the positive x-axis to the vector.'], ['unit vectors i and j', '⟨1, 0⟩ and ⟨0, 1⟩.']],
  watch='Swapping cos and sin in the components.',
  cards=[dict(h='Algebraic vectors', big='⟨\\langle a, b\\rangle + \\langle c, d\\rangle = \\langle a + c, b + d\\rangle⟩. From magnitude and angle: ⟨\\langle r\\cos\\theta, {{r\\sin\\theta}}\\rangle⟩.',
    steps=['⟨\\langle -3, -7\\rangle + \\langle 5, -7\\rangle = \\langle {{2}}, {{-14}}\\rangle⟩.', '⟨r = 17⟩, ⟨\\theta = 210°⟩: ⟨\\langle -\\tfrac{17\\sqrt3}{2}, {{-\\tfrac{17}{2}}}\\rangle⟩.', '⟨3\\langle 2, -1\\rangle - \\langle 1, 4\\rangle = \\langle {{5}}, {{-7}}\\rangle⟩.'])])

R[VE, 5] = dict(obj='find the magnitude, direction angle and unit vector of a vector',
  idea='|⟨a, b⟩| = √(a² + b²); the direction angle comes from tan θ = b/a in the right quadrant; dividing by the magnitude gives a unit vector.',
  voc=[['magnitude', 'The length of a vector.'], ['unit vector', 'A vector of length 1.'], ['direction angle', 'θ with tan θ = b/a, adjusted for the quadrant.']],
  watch='Using tan⁻¹(b/a) without adjusting for Quadrants II and III.',
  cards=[dict(h='Magnitude and direction', big='⟨|v| = \\sqrt{a^2 + b^2}⟩. Unit vector ⟨= \\frac{v}{|v|}⟩. Direction: ⟨\\tan^{-1}\\frac{b}{a}⟩, then {{fix the quadrant}}.',
    steps=['⟨|\\langle -7, -7\\rangle| = \\sqrt{98} = {{7\\sqrt2}}⟩.', 'Unit vector for ⟨\\langle 2, 1\\rangle⟩: ⟨\\langle \\tfrac{2\\sqrt5}{5}, {{\\tfrac{\\sqrt5}{5}}}\\rangle⟩.', 'Direction of ⟨\\langle -1, 1\\rangle⟩: Quadrant II, ⟨{{135°}}⟩.'])])

R[VE, 6] = dict(obj='solve force, navigation and other applied problems with vectors',
  idea='Write each force or velocity in components, add them, then find the resultant’s magnitude and direction; for two vectors with angle θ between them, |u + v|² = |u|² + |v|² + 2|u||v| cos θ.',
  voc=[['resultant force', 'The single force equal to the combined forces.'], ['bearing', 'A direction measured clockwise from north.'], ['airspeed and ground speed', 'Speed through the air versus over the ground.']],
  watch='Using the Law of Cosines with the angle between the vectors instead of the triangle’s angle (or vice versa).',
  cards=[dict(h='Vector applications', big='Resolve every vector into {{components}}, add them, then convert back to magnitude and direction. For two forces at angle ⟨\\theta⟩: ⟨|R|^2 = a^2 + b^2 + 2ab\\cos\\theta⟩.',
    steps=['Forces 40 N and 36 N at 150°: ⟨|R|^2 = 1600 + 1296 + 2880\\cos 150° \\approx 402⟩.', '⟨|R| \\approx {{20.0}}⟩ N.', 'Bearing 90° is due {{east}}: components ⟨\\langle v, 0\\rangle⟩.'])])

R[VE, 7] = dict(obj='transform vectors with 2 × 2 matrices, including rotations',
  idea='Av is a new vector: each component is a row of A times v; the rotation matrix turns v by θ.',
  voc=[['matrix-vector product', 'Av, rows of A times the column v.'], ['linear transformation', 'A map given by v ↦ Av.'], ['rotation matrix', '[cos θ, −sin θ; sin θ, cos θ].']],
  watch='Multiplying columns of A by v instead of rows.',
  cards=[dict(h='Vector transformations', big='⟨Av⟩: first component = {{row 1 · v}}, second = row 2 · v.',
    steps=['⟨[-2, 2; 1, 1]\\langle 5, -6\\rangle = \\langle -10 - 12, 5 - 6\\rangle = \\langle {{-22}}, {{-1}}\\rangle⟩.', 'Rotate ⟨\\langle 3, 4\\rangle⟩ by 90°: ⟨\\langle {{-4}}, {{3}}\\rangle⟩.', 'Rotate ⟨\\langle 2, 0\\rangle⟩ by 60°: ⟨\\langle 1, {{\\sqrt3}}\\rangle⟩.'])])

R[VE, 8] = dict(obj='find dot products, angles between vectors, projections and work',
  idea='u · v = u₁v₁ + u₂v₂ = |u||v| cos θ; u ⊥ v exactly when u · v = 0; proj_v u = ((u · v)/|v|²) v; work W = F · d.',
  voc=[['dot product', 'u · v = u₁v₁ + u₂v₂, a number.'], ['orthogonal', 'Perpendicular; dot product 0.'], ['projection', 'The part of u in the direction of v.']],
  watch='Writing the dot product as a vector ⟨u₁v₁, u₂v₂⟩.',
  cards=[dict(h='Dot products and projections', big='⟨u \\cdot v = u_1v_1 + u_2v_2⟩. ⟨\\cos\\theta = \\frac{u \\cdot v}{|u||v|}⟩. ⟨u \\perp v \\iff u \\cdot v = {{0}}⟩. ⟨\\text{proj}_v u = \\frac{u \\cdot v}{|v|^2}v⟩.',
    steps=['⟨\\langle -7, -5\\rangle \\cdot \\langle 8, 8\\rangle = -56 - 40 = {{-96}}⟩.', 'Force ⟨\\langle 4, 3\\rangle⟩ N over ⟨\\langle 11, -5\\rangle⟩ m: ⟨W = 44 - 15 = {{29}}⟩ J.', '⟨\\text{proj}_{\\langle 4, 0\\rangle}\\langle -3, -3\\rangle = \\frac{-12}{16}\\langle 4, 0\\rangle = \\langle {{-3}}, 0\\rangle⟩.'])])

R[VE, 9] = dict(obj='convert between polar and rectangular coordinates and write complex numbers in polar form',
  idea='x = r cos θ and y = r sin θ; going back, r = √(x² + y²) and θ is the angle in the right quadrant. a + bi = r(cos θ + i sin θ).',
  voc=[['polar coordinates', '(r, θ): distance from the pole and angle.'], ['pole', 'The origin in polar coordinates.'], ['trigonometric form', 'r(cos θ + i sin θ) for a complex number.']],
  watch='Using tan⁻¹(y/x) directly for a point in Quadrant II or III.',
  cards=[dict(h='Polar coordinates', big='Polar → rectangular: ⟨x = r\\cos\\theta⟩, ⟨y = r\\sin\\theta⟩. Rectangular → polar: ⟨r = \\sqrt{x^2 + y^2}⟩, ⟨\\theta⟩ from ⟨\\tan\\theta = \\frac{y}{x}⟩ in the {{correct quadrant}}.',
    steps=['⟨(6, \\tfrac{5\\pi}{3})⟩: ⟨x = 6 \\cdot \\tfrac12 = 3⟩, ⟨y = 6(-\\tfrac{\\sqrt3}{2}) = {{-3\\sqrt3}}⟩.', '⟨(0, 2)⟩ → ⟨({{2}}, {{\\tfrac{\\pi}{2}}})⟩.', '⟨1 + \\sqrt3\\,i = {{2(\\cos\\tfrac{\\pi}{3} + i\\sin\\tfrac{\\pi}{3})}}⟩.'])])

R[VE, 10] = dict(obj='graph polar equations and convert them to rectangular form',
  idea='Replace r cos θ with x, r sin θ with y and r² with x² + y²; rose curves r = a sin(nθ) have n petals for odd n and 2n for even n.',
  voc=[['rose curve', 'r = a cos(nθ) or a sin(nθ).'], ['polar equation', 'An equation in r and θ.'], ['maximum distance', '|a| for r = a cos(nθ), the petal length.']],
  watch='Counting n petals for an even n.',
  cards=[dict(h='Polar graphs', big='Rectangular form: ⟨r\\cos\\theta = x⟩, ⟨r\\sin\\theta = y⟩, ⟨r^2 = x^2 + y^2⟩ (multiply by ⟨r⟩ if needed). Rose ⟨r = a\\sin(n\\theta)⟩: ⟨n⟩ petals if ⟨n⟩ odd, {{2n}} if even.',
    steps=['⟨r = 9\\sin(3\\theta)⟩: ⟨{{3}}⟩ petals; ⟨r = 5\\cos(2\\theta)⟩: ⟨{{4}}⟩ petals.', '⟨r = 3\\sec\\theta⟩: ⟨r\\cos\\theta = 3⟩, so ⟨{{x = 3}}⟩.', '⟨r = 4\\cos\\theta⟩: ⟨r^2 = 4r\\cos\\theta⟩, ⟨{{x^2 + y^2 = 4x}}⟩.'])])

R[VE, 11] = dict(obj='graph parametric equations and eliminate the parameter',
  idea='x(t) and y(t) trace a curve as t changes; solve one equation for t and substitute into the other (or use sin² + cos² = 1).',
  voc=[['parameter', 'The third variable t that x and y depend on.'], ['eliminate the parameter', 'Find one equation in x and y.'], ['orientation', 'The direction the curve is traced as t increases.']],
  watch='Substituting x for t instead of solving x(t) for t.',
  cards=[dict(h='Parametric equations', big='Solve the simpler equation for {{t}}, substitute into the other. For ⟨x = a\\cos t⟩, ⟨y = b\\sin t⟩, use ⟨\\cos^2 t + \\sin^2 t = 1⟩.',
    steps=['⟨x = t + 3⟩, ⟨y = 2t - 5⟩: ⟨t = x - 3⟩, ⟨y = {{2x - 11}}⟩.', '⟨x = 4\\cos t⟩, ⟨y = 3\\sin t⟩: ⟨{{\\tfrac{x^2}{16} + \\tfrac{y^2}{9} = 1}}⟩.', '⟨x = t - 2⟩, ⟨y = 5t⟩: ⟨y = 5(x + 2) = {{5x + 10}}⟩.'])])

# ------------------------------------------------------------------ probability
R[PR, 1] = dict(obj='find probabilities and odds and use probability distributions',
  idea='P(event) = favorable outcomes ÷ total outcomes; odds compare favorable to unfavorable; a probability distribution’s probabilities sum to 1.',
  voc=[['probability', 'A number from 0 to 1 measuring how likely an event is.'], ['odds in favor', 'favorable : unfavorable.'], ['probability distribution', 'The probabilities of every value of a random variable.']],
  watch='Writing odds as favorable : total.',
  cards=[dict(h='Probability and odds', big='⟨P = \\frac{\\text{favorable}}{\\text{total}}⟩; ⟨P(\\text{not } A) = 1 - P(A)⟩. Odds in favor = favorable : {{unfavorable}}.',
    steps=['4 red, 8 black, 8 blue: ⟨P(\\text{not blue}) = \\tfrac{12}{20} = {{\\tfrac35}}⟩.', 'Odds of rolling a 5: ⟨{{1 : 5}}⟩.', '⟨P(X = 0) = \\tfrac13⟩, ⟨\\tfrac{5}{18}⟩, ⟨p⟩, ⟨\\tfrac{1}{18}⟩: ⟨p = 1 - \\tfrac{12}{18} = {{\\tfrac13}}⟩.'])])

R[PR, 2] = dict(obj='find probabilities of independent and dependent events',
  idea='For independent events P(A and B) = P(A)·P(B); without replacement the second probability changes: P(A and B) = P(A)·P(B | A).',
  voc=[['independent events', 'One does not affect the probability of the other.'], ['dependent events', 'The first outcome changes the second probability.'], ['conditional probability', 'P(B | A), the probability of B given A.']],
  watch='Keeping the same total on the second draw without replacement.',
  cards=[dict(h='Independent and dependent events', big='With replacement: {{multiply the original probabilities}}. Without replacement: reduce the counts for the {{second}} draw.',
    steps=['4 white, 3 yellow, 4 red, with replacement: ⟨P(\\text{Y then W}) = \\tfrac{3}{11} \\cdot \\tfrac{4}{11} = {{\\tfrac{12}{121}}}⟩.', 'Without replacement: ⟨\\tfrac{3}{11} \\cdot \\tfrac{4}{10} = {{\\tfrac{6}{55}}}⟩.', 'A die roll and a coin flip are {{independent}}.'])])

R[PR, 3] = dict(obj='count arrangements and selections with permutations and combinations',
  idea='Use permutations nPr = n!/(n − r)! when order matters and combinations nCr = n!/(r!(n − r)!) when it does not.',
  voc=[['permutation', 'An arrangement in which order matters.'], ['combination', 'A selection in which order does not matter.'], ['factorial', 'n! = n(n − 1)···2·1.']],
  watch='Using combinations for ranked or role-based choices (president and vice president).',
  cards=[dict(h='Permutations and combinations', big='Does {{order}} matter? Yes → ⟨_nP_r = \\frac{n!}{(n - r)!}⟩. No → ⟨_nC_r = \\frac{n!}{r!(n - r)!}⟩.',
    steps=['5 finishing places from 12 runners: ⟨_{12}P_5 = {{95\\,040}}⟩.', 'President and vice president from 15: ⟨15 \\cdot 14 = {{210}}⟩.', '2-topping pizzas from 8 toppings: ⟨_8C_2 = {{28}}⟩.'])])

R[PR, 4] = dict(obj='find probabilities of compound events with the addition rule and two-way tables',
  idea='P(A or B) = P(A) + P(B) − P(A and B); in a two-way table, a conditional probability uses only the row or column of the condition.',
  voc=[['addition rule', 'P(A or B) = P(A) + P(B) − P(A and B).'], ['mutually exclusive', 'Events that cannot happen together.'], ['two-way table', 'Counts arranged by two categorical variables.']],
  watch='Adding P(A) and P(B) without subtracting the overlap.',
  cards=[dict(h='Compound events', big='"Or": add and subtract the {{overlap}}. Given a condition, divide by the {{condition’s total}}, not the grand total.',
    steps=['100 students, 59 sport, 27 instrument, 18 both: ⟨P(\\text{sport or instrument}) = \\tfrac{59 + 27 - 18}{100} = {{\\tfrac{17}{25}}}⟩.', '9th graders: 35 cats, 29 dogs; 10th: 16 cats, 14 dogs. ⟨P(\\text{9th} \\mid \\text{cat}) = \\tfrac{35}{51}⟩.', '⟨P(\\text{cat and 9th}) = \\tfrac{35}{94}⟩.'])])

R[PR, 5] = dict(obj='use expected value to evaluate games and decisions',
  idea='E(X) = Σ x·P(x), the long-run average; a game is fair when the expected net gain is 0.',
  voc=[['expected value', 'The probability-weighted average of the outcomes.'], ['fair game', 'Expected net gain 0.'], ['net gain', 'Winnings minus the cost to play.']],
  watch='Forgetting to subtract the cost to play.',
  cards=[dict(h='Expected value and decisions', big='⟨E(X) = \\sum x\\,P(x)⟩. Net gain of a game ⟨= E(\\text{winnings}) - \\text{cost}⟩; {{fair}} when it equals 0.',
    steps=['Cost $4, win $31 with probability ⟨\\tfrac{1}{10}⟩: ⟨3.10 - 4 = {{-\\$0.90}}⟩.', '⟨P(3) = \\tfrac{1}{10}⟩, ⟨P(6) = \\tfrac35⟩, ⟨P(8) = \\tfrac{3}{10}⟩: ⟨E = 0.3 + 3.6 + 2.4 = {{6.3}}⟩.', 'Fair prize for a $2 game won with probability ⟨\\tfrac15⟩: ⟨{{\\$10}}⟩.'])])

R[PR, 6] = dict(obj='classify variables and choose an appropriate display for data',
  idea='Categorical data go in bar graphs or pie charts; one quantitative variable in a histogram, dot plot or box plot; two quantitative variables in a scatterplot.',
  voc=[['categorical variable', 'Values are categories (eye color).'], ['quantitative variable', 'Values are numbers that can be averaged; discrete or continuous.'], ['continuous', 'Any value in an interval (temperature).']],
  watch='Using a histogram for categorical data.',
  cards=[dict(h='Data types and displays', big='Ask: {{categories or numbers}}? One variable or {{two}}? Then pick bar graph, histogram/box plot, or scatterplot.',
    steps=['Temperature at noon: {{quantitative, continuous}}.', 'Shares of students choosing each lunch option: {{bar graph}}.', 'Hours studied vs. test score: {{scatterplot}}.'])])

R[PR, 7] = dict(obj='describe distributions by shape, center and spread and choose matching summaries',
  idea='Symmetric data are summarized by the mean and standard deviation; skewed data or data with outliers by the median and IQR.',
  voc=[['skewed', 'A distribution with a long tail on one side.'], ['bimodal', 'Having two distinct peaks.'], ['resistant measure', 'One not pulled by outliers, such as the median.']],
  watch='Calling a distribution skewed toward the side of the peak (skew is named by the tail).',
  cards=[dict(h='Shapes of distributions', big='Skew is named for the {{tail}}. Skewed or outliers → {{median and IQR}}; roughly symmetric → mean and standard deviation.',
    steps=['Two distinct peaks: {{bimodal}}.', 'Skewed left: summarize with {{the median and IQR}}.', '10, 16, 19, 19, 20, 22, 23, 116: mean ⟨30.6⟩, median ⟨19.5⟩ — the {{median}} is better.'])])

R[PR, 8] = dict(obj='use the empirical rule and z-scores with normal distributions',
  idea='About 68%, 95% and 99.7% of normal data lie within 1, 2 and 3 standard deviations of the mean; z = (x − μ)/σ.',
  voc=[['normal distribution', 'A symmetric, bell-shaped distribution.'], ['empirical rule', '68–95–99.7.'], ['z-score', 'The number of standard deviations from the mean.']],
  watch='Dividing by the variance instead of the standard deviation.',
  cards=[dict(h='Normal distributions', big='Within ⟨1\\sigma⟩: {{68%}}; ⟨2\\sigma⟩: 95%; ⟨3\\sigma⟩: 99.7%. ⟨z = \\frac{x - \\mu}{\\sigma}⟩.',
    steps=['Mean 73, SD 5: between 68 and 78 is about ⟨{{68\\%}}⟩.', 'Mean 76, SD 16, ⟨x = 83⟩: ⟨z = \\tfrac{7}{16} \\approx {{0.44}}⟩.', 'Above ⟨\\mu + 2\\sigma⟩: about ⟨{{2.5\\%}}⟩.'])])

R[PR, 9] = dict(obj='find binomial probabilities and the expected number of successes',
  idea='For n independent trials with success probability p, P(X = k) = C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ and the mean is np.',
  voc=[['binomial setting', 'Fixed n, two outcomes, independent trials, constant p.'], ['binomial coefficient', 'C(n, k), the number of ways to place k successes.'], ['expected value', 'np, the mean number of successes.']],
  watch='Leaving out the C(n, k) factor.',
  cards=[dict(h='Binomial probabilities', big='⟨P(X = k) = \\binom{n}{k}p^k(1 - p)^{n - k}⟩. Mean ⟨= {{np}}⟩.',
    steps=['⟨p = \\tfrac35⟩, ⟨n = 5⟩, ⟨k = 1⟩: ⟨5 \\cdot \\tfrac35 \\cdot (\\tfrac25)^4 = {{\\tfrac{48}{625}}}⟩.', '⟨p = 0.4⟩, ⟨n = 8⟩, ⟨k = 3⟩: ⟨56(0.064)(0.07776) \\approx {{0.2787}}⟩.', '100 seeds at ⟨p = 0.1⟩: expect ⟨{{10}}⟩.'])])

# ------------------------------------------------------------------ sequences, series, limits
R[SQ, 1] = dict(obj='find terms of arithmetic and geometric sequences',
  idea='Arithmetic: aₙ = a₁ + (n − 1)d. Geometric: aₙ = a₁·rⁿ⁻¹.',
  voc=[['common difference d', 'The constant added in an arithmetic sequence.'], ['common ratio r', 'The constant multiplier in a geometric sequence.'], ['explicit formula', 'A rule giving aₙ directly from n.']],
  watch='Using n instead of n − 1 in the formula.',
  cards=[dict(h='Sequences', big='Check differences (constant → {{arithmetic}}) or ratios (constant → {{geometric}}), then use ⟨a_n = a_1 + (n - 1)d⟩ or ⟨a_n = a_1r^{n - 1}⟩.',
    steps=['⟨1, -2, 4, -8, \\dots⟩: ⟨r = -2⟩, ⟨a_5 = 1(-2)^4 = {{16}}⟩.', '⟨-16, -18, -20, \\dots⟩: ⟨a_{57} = -16 + 56(-2) = {{-128}}⟩.', '⟨-6, -12, -24, \\dots⟩: ⟨a_7 = -6 \\cdot 2^6 = {{-384}}⟩.'])])

R[SQ, 2] = dict(obj='find sums of finite arithmetic and geometric series',
  idea='Arithmetic: Sₙ = n(a₁ + aₙ)/2. Geometric: Sₙ = a₁(1 − rⁿ)/(1 − r).',
  voc=[['series', 'The sum of the terms of a sequence.'], ['partial sum Sₙ', 'The sum of the first n terms.'], ['finite series', 'A series with a last term.']],
  watch='Using the arithmetic sum formula for a geometric series.',
  cards=[dict(h='Finite series', big='Arithmetic: find ⟨a_n⟩, then ⟨S_n = \\frac{n(a_1 + a_n)}{2}⟩. Geometric: ⟨S_n = \\frac{a_1(1 - r^n)}{{{1 - r}}}⟩.',
    steps=['⟨9 + 7 + 5 + \\dots⟩, 20 terms: ⟨a_{20} = -29⟩, ⟨S_{20} = \\tfrac{20(9 - 29)}{2} = {{-200}}⟩.', '⟨-3 - 9 - 27 - \\dots⟩, 6 terms: ⟨\\frac{-3(1 - 729)}{1 - 3} = {{-1092}}⟩.', '⟨2 + 4 + 8 + \\dots⟩, 9 terms: ⟨\\frac{2(1 - 512)}{-1} = {{1022}}⟩.'])])

R[SQ, 3] = dict(obj='find sums of infinite geometric series or show that they diverge',
  idea='An infinite geometric series converges to a₁/(1 − r) when |r| < 1 and diverges otherwise.',
  voc=[['converge', 'The partial sums approach a number.'], ['diverge', 'The partial sums do not approach a number.'], ['sum of an infinite series', 'S = a₁/(1 − r) for |r| < 1.']],
  watch='Using the formula when |r| ≥ 1.',
  cards=[dict(h='Infinite geometric series', big='Find ⟨r⟩. If ⟨|r| < 1⟩: ⟨S = \\frac{a_1}{1 - r}⟩. If ⟨|r| \\ge 1⟩: the series {{diverges}}.',
    steps=['⟨13 + \\tfrac{13}{2} + \\dots⟩: ⟨r = \\tfrac12⟩, ⟨S = \\frac{13}{1/2} = {{26}}⟩.', '⟨-26 - \\tfrac{26}{3} - \\dots⟩: ⟨r = \\tfrac13⟩, ⟨S = {{-39}}⟩.', '⟨2 - 4 + 8 - \\dots⟩: ⟨r = -2⟩ → {{diverges}}.'])])

R[SQ, 4] = dict(obj='read, write and evaluate sums in sigma notation',
  idea='Σ from k = m to n of f(k) means add f(m) + … + f(n); there are n − m + 1 terms.',
  voc=[['sigma notation', 'Σ, a compact way to write a sum.'], ['index of summation', 'The variable k that counts the terms.'], ['bounds', 'The starting and ending values of k.']],
  watch='Counting n − m terms instead of n − m + 1.',
  cards=[dict(h='Sigma notation', big='List the terms by substituting each ⟨k⟩ from the lower to the upper {{bound}}; a linear ⟨f(k)⟩ gives an arithmetic series: ⟨\\text{terms} \\times \\frac{\\text{first} + \\text{last}}{2}⟩.',
    steps=['⟨\\sum_{k=1}^{10}(3k + 8)⟩: first ⟨11⟩, last ⟨38⟩, 10 terms: ⟨10 \\cdot \\tfrac{49}{2} = {{245}}⟩.', '⟨\\sum_{k=2}^{7}(6k - 4)⟩: 6 terms, first 8, last 38: ⟨{{138}}⟩.', '⟨\\sum_{k=1}^{4}2^k = 2 + 4 + 8 + 16 = {{30}}⟩.'])])

R[SQ, 5] = dict(obj='evaluate limits by substitution, factoring, conjugates and end behavior',
  idea='Try direct substitution; 0/0 means simplify (factor and cancel, or multiply by a conjugate); for x → ∞ compare the highest powers.',
  voc=[['limit', 'The value f(x) approaches as x approaches a number.'], ['indeterminate form', '0/0, which needs more work.'], ['one-sided limit', 'The limit from the left or the right only.']],
  watch='Stopping at 0/0 and saying the limit does not exist.',
  cards=[dict(h='Introduction to limits', big='Substitute first. {{0/0}} → factor and cancel or use the conjugate, then substitute again. At ⟨\\infty⟩, divide by the {{highest power}} of ⟨x⟩.',
    steps=['⟨\\lim_{x \\to -3}\\frac{x^2 - x - 12}{x + 3} = \\lim(x - 4) = {{-7}}⟩.', '⟨\\lim_{x \\to 0}\\frac{\\sqrt{x + 16} - 4}{x} = \\lim\\frac{1}{\\sqrt{x + 16} + 4} = {{\\tfrac18}}⟩.', '⟨\\lim_{x \\to \\infty}\\frac{3x^2 + 1}{2x^2 - 5} = {{\\tfrac32}}⟩.'])])
