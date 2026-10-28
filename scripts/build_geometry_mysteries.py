#!/usr/bin/env python3
"""Build the Triangle Relationships and Quadrilaterals & Polygons mystery games from the shared mystery engine
(artifacts/similarity-toy-workshop-theft). Only the CASE data and the title change. Every answer is checked in code."""
import json, os, re, math
from fractions import Fraction
ART = os.path.join(os.path.dirname(__file__), '..', 'artifacts')
tpl = open(os.path.join(ART, 'similarity-toy-workshop-theft', 'index.html'), encoding='utf-8').read()
def fr(a, b): return '<span class="fr"><span>%s</span><span>%s</span></span>' % (a, b)
def q(n, instr, ans, hint, steps, html=''):
    return {"skill": "Clue %d" % n, "instr": instr, "html": html, "answer": {"t": "num", "v": str(ans)},
            "hint": "Start here: " + hint, "steps": steps}
PEOPLE = [("#f1c9a5","bun","#8c8c96","#7a3fb0","#e8d9f5","glasses"),("#d9a074","short","#2a1a12","#f4f4f4","#ffe3c9","none"),
          ("#c68a5b","long","#2a1a12","#2a7f6f","#d3f1ea","bowtie"),("#f0c7a0","short","#5a3a22","#24406e","#d6e2f7","cap"),
          ("#f4d3b5","long","#15151a","#c0392b","#fbdada","none"),("#e7b88f","bald","#d9d9df","#8a5a2b","#f1e4c9","glasses")]
def people(rows):
    return [{"id":"s%d"%i,"name":n,"role":r,"skin":PEOPLE[i][0],"hair":PEOPLE[i][1],"hairColor":PEOPLE[i][2],"color":PEOPLE[i][3],"bg":PEOPLE[i][4],"acc":PEOPLE[i][5]} for i,(n,r) in enumerate(rows)]
def named(prefix, names): return [{"id":"%s%d"%(prefix,i),"name":n} for i,n in enumerate(names)]
RULES = ["Solve each problem correctly to unlock a clue. A wrong answer just means try again; hints appear if you get stuck.",
 "Every clue rules out something on the case board: a suspect and the place they were seen, or a method.",
 "The thief acted alone in a spot nobody else was in, so anyone with an alibi is cleared, and so is the place they were seen.",
 "After all 10 clues, exactly one suspect, one place and one method are left. Make your accusation!"]

# ---------------- Mystery 1: Triangle Relationships ----------------
tri_q = [
 q(1,"A triangle has angles of 40° and 70°. Find the third angle.",70,"the angles of a triangle add to 180°",["40 + 70 = 110","180 − 110 = <b>70°</b>"]),
 q(2,"An exterior angle of a triangle has remote interior angles of 48° and 67°. Find the exterior angle.",115,"exterior angle = sum of the two remote interior angles",["48 + 67","<b>115°</b>"]),
 q(3,"Triangle ABC is isosceles with AB = AC and a vertex angle ∠A = 50°. Find ∠B.",65,"the base angles are equal and the three angles add to 180°",["180 − 50 = 130","130 ÷ 2 = <b>65°</b>"]),
 q(4,"Two sides of a triangle are 7 and 12. What is the largest whole-number length the third side can have?",18,"the third side must be less than the sum: 7 + 12",["third side &lt; 7 + 12 = 19","largest whole number: <b>18</b>"]),
 q(5,"AD is a median of △ABC with D on BC. BC = 18. Find DC.",9,"a median ends at the midpoint of the opposite side",["DC = "+fr("1","2")+" · 18","<b>9</b>"]),
 q(6,"The medians of a triangle meet at G. Median AD has AG = 16. Find GD.",8,"AG is two thirds of the median, so GD is one third",["AG = "+fr("2","3")+" · AD, so AD = 24","GD = 24 − 16 = <b>8</b>"]),
 q(7,"A midsegment of a triangle is parallel to a side of length 26. Find the length of the midsegment.",13,"a midsegment is half as long as the side it is parallel to",[fr("1","2")+" · 26","<b>13</b>"]),
 q(8,"P is on the perpendicular bisector of AB. PA = 4x + 1 and PB = 6x − 7. Find x.",4,"a point on the perpendicular bisector is equidistant from A and B",["4x + 1 = 6x − 7","8 = 2x","<b>4</b>"]),
 q(9,"A point on an angle bisector is (2x + 5) from one side of the angle and (3x − 2) from the other. Find x.",7,"a point on an angle bisector is equidistant from the sides",["2x + 5 = 3x − 2","<b>7</b> = x"]),
 q(10,"The centroid of a triangle lies on a median of length 30. How far is the centroid from the vertex?",20,"the centroid is two thirds of the way from the vertex",[fr("2","3")+" · 30","<b>20</b>"]),
]
tri_case = {"unit":"triangle-relationships","eyebrow":"Case file No. 13","title":"The Harbor Museum Compass Caper",
 "tagline":"The antique ship's compass is missing from the Harbor Museum. Solve each problem to earn a clue.",
 "palette":{"navy":"#12385c","accent":"#5ec8d8"},"labels":{"p":"The Suspects","l":"The Places","m":"The Methods"},
 "placeholder":"Your answer","inputHint":"Type a number or a fraction like 3/2.","symbols":[],
 "intro":["At the Harbor Museum, the curator was about to unveil the pride of the collection: the <b>Admiral's Compass</b>, two hundred years old and still pointing true north. But the glass case was open and the stand was empty!",
          "Six people were in the museum, each in a different spot, and there are six ways to sneak a brass compass out the door. You are the museum detective: find <b>who</b> took it, <b>where</b> they were, and <b>how</b> they got it out."],
 "rules":RULES,
 "suspects":people([("Captain Reed","Curator"),("Ms. Salt","Tour Guide"),("Finn Okafor","Intern"),("Dr. Tidewell","Historian"),("Mrs. Anchor","Gift Shop Manager"),("Mr. Brine","Night Guard")]),
 "places":named("p",["Map Room","Ship Deck","Archive","Lighthouse Tower","Gift Shop","Cafe"]),
 "methods":named("m",["Tucked in a map tube","Wrapped in a flag","Locked in a sailor's trunk","Boxed as a souvenir","Rowed out in a dinghy","Hidden in a lunch cooler"]),
 "clues":[
  {"p":"s0","l":"p0","text":"Captain Reed was unrolling sea charts in the Map Room. The security camera shows him there the whole time."},
  {"m":"m0","text":"Every map tube was opened. Only maps inside."},
  {"p":"s1","l":"p1","text":"Ms. Salt was leading a tour on the Ship Deck. Eleven visitors remember her."},
  {"m":"m2","text":"The sailor's trunk is rusted shut and has not been opened in years."},
  {"p":"s3","l":"p2","text":"Dr. Tidewell was reading old logbooks in the Archive. The sign-in sheet has his name."},
  {"m":"m3","text":"The souvenir boxes were all counted. Each one held a mug or a postcard."},
  {"p":"s4","l":"p4","text":"Mrs. Anchor was counting the till in the Gift Shop, timed by the register."},
  {"m":"m4","text":"The dinghy is still tied up and bone dry."},
  {"p":"s5","l":"p5","text":"Mr. Brine was eating dinner in the Cafe, and the cook confirms it."},
  {"m":"m5","text":"The lunch cooler holds sandwiches and nothing else."}],
 "culprit":{"p":"s2","l":"p3","m":"m1"},"accuseTemplate":"Suspect: {p} · Place: {l} · Method: {m}",
 "ending":"While the guests watched the unveiling, <b>Finn Okafor</b> slipped up the <b>Lighthouse Tower</b> stairs, wrapped the compass in a <b>flag</b>, and walked out carrying it like a banner for the next parade. Every alibi and method you cleared led straight to him. True north!",
 "questions":tri_q}

# ---------------- Mystery 2: Quadrilaterals & Polygons ----------------
quad_q = [
 q(1,"Find the sum of the interior angles of a pentagon.",540,"sum = (n − 2) · 180 with n = 5",["(5 − 2) · 180","3 · 180 = <b>540°</b>"]),
 q(2,"Find the measure of each interior angle of a regular hexagon.",120,"each angle = "+fr("(n − 2) · 180","n"),[fr("4 · 180","6")+" = "+fr("720","6"),"<b>120°</b>"]),
 q(3,"Find the measure of each exterior angle of a regular polygon with 9 sides.",40,"each exterior angle = "+fr("360","n"),[fr("360","9"),"<b>40°</b>"]),
 q(4,"One angle of a parallelogram is 65°. Find the measure of a consecutive angle.",115,"consecutive angles of a parallelogram add to 180°",["180 − 65","<b>115°</b>"]),
 q(5,"A rectangle is 6 cm by 8 cm. Find the length of its diagonal.",10,"the diagonal is the hypotenuse of a right triangle",["6² + 8² = 36 + 64 = 100","√100 = <b>10 cm</b>"]),
 q(6,"A rhombus has diagonals of 10 cm and 24 cm. Find the length of one side.",13,"the diagonals bisect each other at right angles, so the half-diagonals are 5 and 12",["5² + 12² = 25 + 144 = 169","√169 = <b>13 cm</b>"]),
 q(7,"A trapezoid has bases of 12 and 20. Find the length of its midsegment.",16,"midsegment = "+fr("sum of the bases","2"),[fr("12 + 20","2")+" = "+fr("32","2"),"<b>16</b>"]),
 q(8,"A polygon has an interior angle sum of 1260°. How many sides does it have?",9,"solve (n − 2) · 180 = 1260",["n − 2 = 7","<b>n = 9</b>"]),
 q(9,"A kite has two congruent angles of 80° each and a third angle of 100°. Find the fourth angle.",100,"the angles of a quadrilateral add to 360°",["80 + 80 + 100 = 260","360 − 260 = <b>100°</b>"]),
 q(10,"The diagonals of a parallelogram meet at a point. One piece of a diagonal is 3x + 2 and the other piece of the same diagonal is 5x − 6. Find x.",4,"the diagonals of a parallelogram bisect each other, so the two pieces are equal",["3x + 2 = 5x − 6","8 = 2x","<b>4</b>"]),
]
quad_case = {"unit":"quadrilaterals-polygons","eyebrow":"Case file No. 14","title":"The Mosaic Gallery Heist",
 "tagline":"A famous mosaic is missing from the Tessera Gallery. Solve each problem to earn a clue.",
 "palette":{"navy":"#3a1f5c","accent":"#ffb347"},"labels":{"p":"The Suspects","l":"The Places","m":"The Methods"},
 "placeholder":"Your answer","inputHint":"Type a number or a fraction like 3/2.","symbols":[],
 "intro":["At the Tessera Gallery, the director was about to reveal the star of the show: <b>The Golden Mosaic</b>, a small panel made of a thousand colored tiles. But the cover was lifted and the wall was bare!",
          "Six people were in the gallery, each in a different spot, and there are six ways to sneak a mosaic panel out the door. You are the gallery detective: find <b>who</b> took it, <b>where</b> they were, and <b>how</b> they got it out."],
 "rules":RULES,
 "suspects":people([("Ms. Tessa","Gallery Director"),("Mr. Quill","Picture Framer"),("Zoe Park","Student Artist"),("Dr. Hue","Art Critic"),("Mrs. Gallo","Gift Shop Clerk"),("Mr. Dray","Delivery Driver")]),
 "places":named("p",["Main Hall","Framing Shop","Studio","Sculpture Garden","Gift Shop","Loading Dock"]),
 "methods":named("m",["Rolled in a poster tube","Hidden in a picture frame","Carried on a paint cart","Packed in a tote bag","Slipped under a coat","Shipped in a crate"]),
 "clues":[
  {"p":"s0","l":"p0","text":"Ms. Tessa was giving the opening speech in the Main Hall. Two hundred guests saw her."},
  {"m":"m0","text":"The poster tubes were opened one by one. Only posters inside."},
  {"p":"s1","l":"p1","text":"Mr. Quill was gluing a frame in the Framing Shop. The glue on his hands was still wet."},
  {"m":"m2","text":"The paint cart in the hall holds brushes and cans, and the lids are all painted shut."},
  {"p":"s3","l":"p3","text":"Dr. Hue was sketching a statue in the Sculpture Garden. The guard waved to him twice."},
  {"m":"m3","text":"The tote bags were checked at the door. Only lunches and umbrellas."},
  {"p":"s4","l":"p4","text":"Mrs. Gallo was wrapping postcards in the Gift Shop, timed by the register."},
  {"m":"m4","text":"All of the coats were checked. No flat, tile-shaped bulge in any of them."},
  {"p":"s5","l":"p5","text":"Mr. Dray was loading boxes at the Loading Dock, and the dock camera caught him."},
  {"m":"m5","text":"The shipping crate is still sealed. The seal has not been broken."}],
 "culprit":{"p":"s2","l":"p2","m":"m1"},"accuseTemplate":"Suspect: {p} · Place: {l} · Method: {m}",
 "ending":"While everyone listened to the speech, <b>Zoe Park</b> slipped into the <b>Studio</b>, tucked The Golden Mosaic behind a canvas inside a <b>picture frame</b>, and carried it out as if it were her own painting. Every alibi and method you cleared led straight to her. Case closed!",
 "questions":quad_q}

# ---------------- verification ----------------
def check(case):
    for k in ('suspects','places','methods'): assert len(case[k]) == 6, k
    cl = case['clues']; assert len(cl) == 10 and len(case['questions']) == 10
    sus = {c['p'] for c in cl if 'p' in c}; pl = {c['l'] for c in cl if 'l' in c}; me = {c['m'] for c in cl if 'm' in c}
    assert len(sus) == 5 and len(pl) == 5 and len(me) == 5
    cu = case['culprit']; assert cu['p'] not in sus and cu['l'] not in pl and cu['m'] not in me
    assert {s['id'] for s in case['suspects']} - sus == {cu['p']}
    assert {s['id'] for s in case['places']} - pl == {cu['l']}
    assert {s['id'] for s in case['methods']} - me == {cu['m']}
def val(cases):
    # independent recomputation of every numeric answer
    t = {
     'tri': [180-40-70, 48+67, (180-50)//2, 7+12-1, 18//2, 16//2 + 16 - 16 if False else 24-16, 26//2, None, None, 30*2//3],
     'quad': [(5-2)*180, (6-2)*180//6, 360//9, 180-65, int(math.hypot(6,8)), int(math.hypot(5,12)), (12+20)//2, 1260//180+2, 360-260, None]}
    x8 = Fraction(8,2); assert 4*x8+1 == 6*x8-7 and x8 == 4
    x9 = 7; assert 2*x9+5 == 3*x9-2
    x10 = 4; assert 3*x10+2 == 5*x10-6
    t['tri'][7] = 4; t['tri'][8] = 7; t['quad'][9] = 4
    for key, case in (('tri', cases[0]), ('quad', cases[1])):
        got = [int(Fraction(qq['answer']['v'])) for qq in case['questions']]
        assert got == t[key], (key, got, t[key])
check(tri_case); check(quad_case); val((tri_case, quad_case))

def build(case, folder):
    j = json.dumps(case, ensure_ascii=False)
    s = re.sub(r'const CASE=\{.*?\};\n', lambda m: 'const CASE=' + j + ';\n', tpl, count=1, flags=re.S)
    s = s.replace('<title>The Toy Workshop Theft</title>', '<title>%s</title>' % case['title'])
    assert 'Toy Workshop' not in s and 'Tiny Titan' not in s
    out = os.path.join(ART, folder); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(s); print('wrote', folder)
build(tri_case, 'triangle-relationships-harbor-museum-caper')
build(quad_case, 'quadrilaterals-polygons-mosaic-gallery-heist')
