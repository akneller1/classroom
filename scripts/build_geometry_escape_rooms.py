#!/usr/bin/env python3
"""Build the Triangle Relationships and Quadrilaterals & Polygons escape rooms from the shared room engine
(artifacts/circles-escape-room). Only the ROOM configuration, title and teacher-key gate change."""
import re, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo_svg import *
ART = os.path.join(os.path.dirname(__file__), '..', 'artifacts')
tpl = open(os.path.join(ART, 'circles-escape-room', 'index.html'), encoding='utf-8').read()

# ---------- Triangle Relationships: Starlight Observatory ----------
A, B, C = (60, 240), (340, 240), (100, 40)
D = mid(B, C); E = foot(B, A, C); G = mid(A, C); K = mid(A, B)
# angle bisector from C meets AB at F (angle bisector theorem)
CA, CB = math.dist(C, A), math.dist(C, B); F = (A[0] + (B[0] - A[0]) * CA / (CA + CB), 240)
# perpendicular bisector of BC meets AB at P
dx, dy = C[0] - B[0], C[1] - B[1]; t = (240 - D[1]) / (-dx) if dx else 0   # direction perpendicular to BC is (-dy, dx)... solve below
nx, ny = -dy, dx
tt = (240 - D[1]) / ny; P = (D[0] + nx * tt, 240)
assert 0 < ((E[0]-A[0])*(C[0]-A[0])+(E[1]-A[1])*(C[1]-A[1]))/(math.dist(A,C)**2) < 1, 'altitude foot must lie on AC'
print({k:tuple(round(x) for x in v) for k,v in dict(E=E,G=G,F=F,K=K,P=P,D=D).items()})
assert A[0] < P[0] < B[0] and A[0] < F[0] < B[0]
cls_svg = ''.join([
  '<polygon points="%s %s %s" fill="rgba(110,193,255,.08)" stroke="#6ec1ff" stroke-width="3"/>' % (pt(A), pt(B), pt(C)),
  line(A, D, '#ff7ab8', 3), tick(B, D, 1), tick(D, C, 1),
  line(B, E, '#7cf29a', 3), rightmark(E, A, B),
  line(C, F, '#ffc857', 3), arc(C, A, F, 26), arc(C, F, B, 31),
  line(G, K, '#c79bff', 3), tick(A, G, 2), tick(G, C, 2),
  line(D, P, '#ff9a4d', 3, '7 5'), rightmark(D, B, P),
  dot(A), dot(B), dot(C), dot(D), dot(E), dot(F), dot(G), dot(K), dot(P),
  text((A[0]-18, A[1]+6), 'A'), text((B[0]+8, B[1]+6), 'B'), text((C[0]-4, C[1]-10), 'C'),
  text((D[0]+9, D[1]-4), 'D'), text((E[0]+8, E[1]-2), 'E'), text((F[0]-4, F[1]+22), 'F'),
  text((G[0]-18, G[1]-2), 'G'), text((K[0]-4, K[1]+22), 'K'), text((P[0]-16, P[1]+20), 'P')])

# stage-5 scene: median with centroid and a midsegment
a2, b2, c2 = (60, 235), (330, 235), (200, 40)
d2 = mid(b2, c2); e2 = mid(a2, c2); g2 = (a2[0]+(d2[0]-a2[0])*2/3, a2[1]+(d2[1]-a2[1])*2/3)
cent_svg = ''.join([
  '<polygon points="%s %s %s" fill="rgba(110,193,255,.08)" stroke="#6ec1ff" stroke-width="3"/>' % (pt(a2), pt(b2), pt(c2)),
  line(a2, d2, '#ff7ab8', 3), line(d2, e2, '#c79bff', 3), tick(b2, d2, 1), tick(d2, c2, 1), tick(a2, e2, 2), tick(e2, c2, 2),
  dot(a2), dot(b2), dot(c2), dot(d2), dot(e2), dot(g2, 5, '#ffc857'),
  text((a2[0]-16, a2[1]+6), 'A'), text((b2[0]+8, b2[1]+6), 'B'), text((c2[0]-5, c2[1]-10), 'C'),
  text((d2[0]+9, d2[1]), 'D'), text((e2[0]-18, e2[1]), 'E'), text((g2[0]+6, g2[1]+18), 'G', 15, '#ffc857'),
  text((165, 258), 'AB = 30', 14, '#ffc857'), text((176, 214), 'AD = 24', 14, '#ffc857')])

tri_room = r"""const ROOM={
 id:'triangle-relationships', title:'Starlight Observatory: Locked Under the Stars', emoji:'🔭', endEmoji:'🌠🔭',
 intro:'The observatory closed for the night, but your class is still inside. The dome door sealed itself, the telescope lights are blinking, and the night watchman is back in <b>10 minutes</b>. Solve the puzzle in each room, collect the key cards, and open the telescope to leave.',
 finalStory:'The telescope controls have five slots. Insert your key cards in order from the smallest stamp to the largest. The letters name what you will see through the lens.',
 finalAsk:'What do you see?', word:'COMET',
 outro:'The telescope swings around and a bright comet glides into view. The dome door clicks open, and the watchman waves you out under the stars. Best field trip ever.',
 stages:[
 {name:'The Dome Door',type:'fields',stamp:14,letter:'C',ui:'dial',
  story:'The dome door has two dials. A brass plaque shows a triangle and a note about another one. Set the dials to the answers.',
  scene:{kind:'emoji',bg:'#0a0d2a',floor:'#1b1f4a',items:[{e:'🔭',x:150,y:190,s:110,msg:'The big telescope, pointing at nothing yet.'},{e:'🌙',x:330,y:80,s:50,msg:'A crescent moon is painted on the dome.'},{e:'⭐',x:80,y:80,s:34,msg:'A star sticker. Not useful.'}],caption:'dial A, then dial B'},
  title:'The Plaque',prompt:`<div class="note">Triangle ABC is isosceles with AB = AC. Its base angles are ∠B = (7x + 3)° and ∠C = (5x + 9)°.</div><p>Dial A: find x.<br>Dial B: a different triangle has two sides of length 3 and 5. How many whole-number lengths could its third side have?</p>`,
  fields:[{label:'A (x)',answer:3},{label:'B (how many)',answer:5}],button:'Open the door',
  hints:['Base angles of an isosceles triangle are equal. Set 7x + 3 = 5x + 9.','x = 3. For dial B, the third side must be greater than 5 − 3 and less than 5 + 3.','The third side is between 2 and 8, not including 2 or 8. List the whole numbers.'],
  key:'7x + 3 = 5x + 9 gives x = 3. The third side c satisfies 2 < c < 8, so c = 3, 4, 5, 6, 7: five values. A = 3, B = 5.'},
 {name:'The Star Map Room',type:'cipher',stamp:27,letter:'O',
  story:'A star map is rolled up in a cabinet, and its location is written in code. A sticky note on the lamp gives the shift. Click things to find it.',
  scene:{kind:'emoji',bg:'#0c1030',floor:'#2a2060',items:[{e:'🗺️',x:130,y:190,s:90,msg:'A big sky chart. The name of the room is scribbled in code.'},{e:'💡',x:270,y:110,s:40,clue:'Stuck to the lamp:<br>An exterior angle of a triangle measures (6x + 4)°.<br>The two remote interior angles measure (2x + 10)° and (3x + 4)°.<br>Shift = x',msg:'You found a sticky note!'},{e:'🪐',x:340,y:170,s:50,msg:'A model of Saturn. It wobbles.'}],caption:'click things to inspect them'},
  plain:'THE STAR MAP IS HIDDEN IN THE TOWER',shift:10,answer:'TOWER',askLabel:'Hiding place',
  hints:['Click the lamp to read the note.','The exterior angle equals the sum of the two remote interior angles: 6x + 4 = (2x + 10) + (3x + 4).','6x + 4 = 5x + 14, so x = 10. Set the shift to 10.'],
  key:'6x + 4 = (2x + 10) + (3x + 4) = 5x + 14, so x = 10. Shift 10. Hiding place: TOWER.'},
 {name:'The Instrument Panel',type:'classify',stamp:41,letter:'M',
  story:'The instrument panel wants the correct name for each marked segment in the sketch of the triangular support frame. Matching tick marks mean equal lengths, and a small square means a right angle.',
  scene:{kind:'svg',viewBox:'0 0 400 300',svg:`__CLS_SVG__`},
  title:'The Name Panel',prompt:'<p style="color:var(--dim)">Choose the name for each one. D is the midpoint of BC, G and K are midpoints of AC and AB, and the two angles at C are equal.</p>',
  items:['Segment <b>AD</b>','Segment <b>BE</b>','Segment <b>CF</b>','Segment <b>GK</b>','Line <b>DP</b> (BD = DC)'],
  options:['Median','Altitude','Angle bisector','Midsegment','Perpendicular bisector'],answer:[0,1,2,3,4],
  hints:['A median goes from a vertex to the midpoint of the opposite side. An altitude meets the opposite side at a right angle.','An angle bisector splits an angle into two equal angles. A midsegment joins the midpoints of two sides.','A perpendicular bisector crosses a side at its midpoint at a right angle, and it does not have to start at a vertex.'],
  key:'AD is a median, BE is an altitude, CF is an angle bisector, GK is a midsegment, DP is a perpendicular bisector of BC.'},
 {name:'The Calibration Log',type:'order',stamp:58,letter:'E',
  story:'The telescope mount sits on a support beam. Point P lies on the perpendicular bisector of segment AB, with PA = 3x + 2 and PB = 5x − 6. Rebuild the calibration log that finds PA.',
  scene:{kind:'emoji',bg:'#0b0e24',floor:'#1b2250',items:[{e:'🔭',x:200,y:180,s:100,msg:'The mount is shaking a little.'},{e:'📏',x:330,y:190,s:40,msg:'A ruler. The log is already measured.'}],caption:'PA = 3x + 2,  PB = 5x − 6'},
  title:'The Log',prompt:'<p style="color:var(--dim)">Put the steps in the correct order, top to bottom.</p>',
  steps:['Every point on the perpendicular bisector of a segment is the same distance from both endpoints, so PA = PB.','Set the expressions equal: 3x + 2 = 5x − 6.','Subtract 3x from both sides: 2 = 2x − 6.','Add 6 to both sides: 8 = 2x, so x = 4.','Substitute: PA = 3(4) + 2 = 14.'],
  hints:['What do you know about a point on a perpendicular bisector and the two endpoints?','Use that fact first, then solve for x, then substitute.','The last step finds PA, not x.'],
  key:'PA = PB, so 3x + 2 = 5x − 6, x = 4, and PA = 3(4) + 2 = 14.'},
 {name:'The Telescope Mount',type:'fields',stamp:70,letter:'T',
  story:'The mount has a triangular frame. Median AD is 24 long, and G is where the medians meet. D and E are midpoints of BC and AC, and AB = 30. Three readings are needed.',
  scene:{kind:'svg',viewBox:'0 0 400 300',svg:`__CENT_SVG__`},
  title:'The Mount Readings',prompt:'<p>Find AG, GD and DE.</p>',
  fields:[{label:'AG',answer:16},{label:'GD',answer:8},{label:'DE',answer:15}],button:'Aim the telescope',
  hints:['The medians meet at the centroid, which is two thirds of the way from each vertex to the midpoint of the opposite side.',`AG = ${fr('2','3')} × 24. Then GD is the rest of the median.`,'DE joins the midpoints of two sides, so it is half as long as the side it is parallel to, AB.'],
  key:`AG = ${fr('2','3')}(24) = 16 and GD = 24 − 16 = 8. DE is a midsegment, so DE = ${fr('1','2')}(30) = 15.`}
 ]};"""

# ---------- Quadrilaterals & Polygons: Tile Factory ----------
quad_room = r"""const ROOM={
 id:'quadrilaterals-polygons', title:'Lockdown at the Tile Factory', emoji:'🧩', endEmoji:'🧩🎉',
 intro:'The Mosaic Tile Factory shut for the night, but your class is still on the floor. The doors locked, the conveyor belts stopped, and the night supervisor returns in <b>10 minutes</b>. Solve the puzzle at each station, collect the key cards, and unlock the front gate.',
 finalStory:'The front gate has a keypad with five slots. Insert your key cards in order from the smallest stamp to the largest. The letters name what the factory makes.',
 finalAsk:'What does the factory make?', word:'TILES',
 outro:'The gate swings open, and the supervisor laughs when she sees you holding the master key. She hands out a free mosaic coaster to every team member.',
 stages:[
 {name:'The Cutting Floor',type:'fields',stamp:11,letter:'T',ui:'dial',
  story:'The cutting machine has two dials. A sign on the wall shows the cutting plans. Set the dials to the answers.',
  scene:{kind:'emoji',bg:'#1a0e2e',floor:'#40305a',items:[{e:'🔧',x:130,y:190,s:80,msg:'A big wrench. The machine is locked, not broken.'},{e:'🧱',x:300,y:190,s:70,msg:'A stack of blank tiles.'},{e:'📐',x:230,y:100,s:40,msg:'A set square hangs on a hook.'}],caption:'dial A, then dial B'},
  title:'The Cutting Plan',prompt:`<div class="note">Plan 1: a hexagon is cut into triangles by drawing every diagonal from one vertex.<br>Plan 2: a polygon has an interior angle sum of 1080°.</div><p>Dial A: how many triangles does Plan 1 make?<br>Dial B: how many sides does the polygon in Plan 2 have?</p>`,
  fields:[{label:'A (triangles)',answer:4},{label:'B (sides)',answer:8}],button:'Start the cutter',
  hints:['A polygon with n sides splits into n − 2 triangles. The interior angle sum is (n − 2) × 180°.','A hexagon has 6 sides, so dial A is 6 − 2.','For dial B solve (n − 2) × 180 = 1080.'],
  key:'A hexagon splits into 6 − 2 = 4 triangles. (n − 2)(180) = 1080 gives n − 2 = 6, so n = 8. A = 4, B = 8.'},
 {name:'The Glaze Room',type:'cipher',stamp:24,letter:'I',
  story:'The glaze cabinet is locked with a word written in code. A sticky note on the kiln gives the shift. Click things to find it.',
  scene:{kind:'emoji',bg:'#21102f',floor:'#4a2a5c',items:[{e:'🏺',x:130,y:190,s:90,msg:'Glaze pots in every color.'},{e:'🔥',x:270,y:150,s:60,clue:'Stuck to the kiln:<br>A parallelogram has opposite sides 4x + 1 and 3x + 6.<br>Shift = x',msg:'You found a sticky note!'},{e:'🎨',x:340,y:190,s:44,msg:'A paint palette. It is dry.'}],caption:'click things to inspect them'},
  plain:'THE TILE KEY IS UNDER THE TABLE',shift:5,answer:'TABLE',askLabel:'Hiding place',
  hints:['Click the kiln to read the note.','Opposite sides of a parallelogram are congruent. Solve 4x + 1 = 3x + 6.','x = 5. Set the shift to 5.'],
  key:'Opposite sides are equal: 4x + 1 = 3x + 6, so x = 5. Shift 5. Hiding place: TABLE.'},
 {name:'The Sorting Belt',type:'classify',stamp:39,letter:'L',
  story:'The sorting belt will only restart if each tile shape is matched to its clue card. Read each description and choose the most specific name.',
  scene:{kind:'emoji',bg:'#150c28',floor:'#3a2a58',items:[{e:'🟦',x:90,y:180,s:60,msg:'A square blue tile.'},{e:'🔶',x:200,y:150,s:60,msg:'An orange diamond tile.'},{e:'🪁',x:310,y:160,s:60,msg:'A kite-shaped tile.'},{e:'📦',x:200,y:230,s:40,msg:'The sorting bins.'}],caption:'click the tiles'},
  title:'The Clue Cards',prompt:'<p style="color:var(--dim)">Choose the most specific name for each tile.</p>',
  items:['Four right angles, but the sides are not all the same length','Four congruent sides; the diagonals are perpendicular, but the angles are not right angles','Four congruent sides and four right angles','Exactly one pair of parallel sides','Two pairs of adjacent congruent sides, and no parallel sides'],
  options:['Rectangle','Rhombus','Square','Trapezoid','Kite'],answer:[0,1,2,3,4],
  hints:['A rectangle has four right angles. A rhombus has four congruent sides. A square has both.','A trapezoid has exactly one pair of parallel sides.','A kite has two pairs of congruent sides that sit next to each other, not across from each other.'],
  key:'Rectangle, rhombus, square, trapezoid, kite.'},
 {name:'The Press Room',type:'order',stamp:52,letter:'E',
  story:'A rhombus tile is pressed with diagonals of 10 cm and 24 cm. The press needs the side length of the tile. Rebuild the solution that finds it.',
  scene:{kind:'emoji',bg:'#190d2b',floor:'#3c2a5a',items:[{e:'⚙️',x:130,y:190,s:90,msg:'Gears turn slowly.'},{e:'🔶',x:290,y:170,s:80,msg:'A rhombus tile with its diagonals scratched in.'}],caption:'diagonals: 10 cm and 24 cm'},
  title:'The Press Log',prompt:'<p style="color:var(--dim)">Put the steps in the correct order, top to bottom.</p>',
  steps:['The diagonals of a rhombus are perpendicular and bisect each other.','Half of each diagonal gives legs of 5 cm and 12 cm in a right triangle.',`The side of the rhombus is the hypotenuse s: 5${sup('2')} + 12${sup('2')} = s${sup('2')}.`,`25 + 144 = 169, so s${sup('2')} = 169.`,'Take the positive square root: s = 13 cm.'],
  hints:['What do you know about the diagonals of a rhombus?','Cut the rhombus into four right triangles. What are their legs?','The side of the rhombus is the hypotenuse of one of those triangles.'],
  key:'Half-diagonals 5 and 12 form a right triangle: 5² + 12² = 169, so the side is 13 cm.'},
 {name:'The Gate Controls',type:'fields',stamp:67,letter:'S',
  story:'The gate controls need three readings from the mosaic plans on the wall. Enter each one.',
  scene:{kind:'emoji',bg:'#12091f',floor:'#35254f',items:[{e:'🔐',x:200,y:180,s:90,msg:'The gate lock.'},{e:'🧩',x:100,y:120,s:46,msg:'A jigsaw puzzle piece. Not useful.'}],caption:'three readings'},
  title:'The Mosaic Plans',prompt:'<div class="note">Plan A: a trapezoid with bases 14 and 26. Its midsegment is m.<br>Plan B: a regular decagon. One interior angle is b°.<br>Plan C: in a parallelogram, one angle is 65°. An angle next to it is c°.</div><p>Find m, b and c.</p>',
  fields:[{label:'m',answer:20},{label:'b (°)',answer:144},{label:'c (°)',answer:115}],button:'Unlock the gate',
  hints:[`The midsegment of a trapezoid is the average of the bases: ${fr('14 + 26','2')}.`,`A regular polygon has interior angle ${fr('(n − 2) · 180','n')}. A decagon has n = 10.`,'Consecutive angles of a parallelogram are supplementary: they add to 180°.'],
  key:`m = ${fr('14 + 26','2')} = 20. b = ${fr('8 · 180','10')} = 144. c = 180 − 65 = 115.`}
 ]};"""

KEYJS = r"""if(location.hash=='#key'){const k=$('#key');k.style.display='block';k.innerHTML='<h2>Teacher answer key</h2><p>Teacher code: <input id="kc" type="password" style="width:90px"> <button onclick="unlockKey()">Show key</button></p><div id="kb"></div>'}
function unlockKey(){if($('#kc').value.trim()!=='205'){$('#kb').textContent='Incorrect code.';return}$('#kb').innerHTML=STAGES.map((s,i)=>`<p><b>Room ${i+1} (${s.name}):</b> ${s.key}</p>`).join('')+`<p><b>Final:</b> sort stamps ${[...STAGES].sort((a,b)=>a.stamp-b.stamp).map(s=>s.stamp).join(', ')} to spell <b>${ROOM.word}</b>.</p>`}"""

def build(room_js, folder, title, emoji):
    s = tpl
    i = s.index('const ROOM={'); k = s.index('stages:[', i)
    m = re.search(r'\n ?\]\s*\n?\};?', s[k:]); e = k + m.end()
    s = s[:i] + room_js + s[e:]
    s = s.replace('<title>Carnival After Dark: Locked In the Midway</title>', '<title>%s</title>' % title)
    s = s.replace('<h1>🎡 Carnival After Dark: Locked In the Midway</h1>', '<h1>%s %s</h1>' % (emoji, title))
    ks = s.index("if(location.hash=='#key')"); ke = s.index('\nintro();', ks)
    s = s[:ks] + KEYJS + s[ke:]
    assert 'Carnival' not in s and 'midway' not in s.lower(), 'leftover template text'
    out = os.path.join(ART, folder); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(s)
    print('wrote', folder, len(s))

tri_room = tri_room.replace('__CLS_SVG__', cls_svg).replace('__CENT_SVG__', cent_svg)
build(tri_room, 'triangle-relationships-escape-room', 'Starlight Observatory: Locked Under the Stars', '🔭')
build(quad_room, 'quadrilaterals-polygons-escape-room', 'Lockdown at the Tile Factory', '🧩')
