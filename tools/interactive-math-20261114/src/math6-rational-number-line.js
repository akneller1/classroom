/* Rational numbers: opposites, absolute value and order on a number line; reflections and distance on the plane. */
var st = { a: -1.5, b: 4, px: 3, py: 2, qx: 3, qy: -4, mode: 'line', seen: {} };
var tabs = L.tabs(P.panel, [{ id: 'line', label: 'Number line' }, { id: 'plane', label: 'Coordinate plane' }], function (id) { st.mode = id; draw(); });
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var fb = L.feedback(P.panel);
var btn = L.h('div', { class: 'btn-row' }, P.panel);
L.button(btn, 'Show opposites', function () { st.showOpp = !st.showOpp; draw(); }, true);
L.button(btn, 'Reflect P across the x-axis', function () { st.qx = st.px; st.qy = -st.py; st.seen.reflX = true; draw(); }, true);
L.button(btn, 'Reflect P across the y-axis', function () { st.qx = -st.px; st.qy = st.py; st.seen.reflY = true; draw(); }, true);
L.reset(btn, function () { st.a = -1.5; st.b = 4; st.px = 3; st.py = 2; st.qx = 3; st.qy = -4; st.showOpp = false; draw(); });
var ch = L.challenges(P.panel, [
  { text: 'Put a on a number whose opposite is 4.5.', check: function () { return st.seen.opp45; } },
  { text: 'Find two different numbers that both have absolute value 6.', check: function () { return st.seen.abs6; } },
  { text: 'Make a &lt; b but |a| &gt; |b|.', check: function () { return st.seen.lessBigger; } },
  { text: 'On the plane, put P in Quadrant III.', check: function () { return st.seen.q3; } },
  { text: 'On the plane, make P and Q share an x-coordinate and be exactly 7 units apart.', check: function () { return st.seen.vert7; } }
]);
L.notice(P.below, '<p><b>Opposites</b> are the same distance from 0 on opposite sides, so a number and its opposite have the same <b>absolute value</b>. The opposite of a negative number is positive.</p>' +
  '<p>On a horizontal number line, the number farther <b>right</b> is greater, so −1 &gt; −5 even though 5 &gt; 1.</p>' +
  '<p>Reflecting a point across the x-axis changes the sign of y; across the y-axis changes the sign of x. Points with the same x-coordinate are |y₁ − y₂| apart.</p>');

var gLine = L.graph(P.stage, { xmin: -10.5, xmax: 10.5, ymin: -1.6, ymax: 2.4, width: 640, height: 220, xstep: 1, xlabelStep: 1, noYAxis: true, noGrid: false, ystep: 10, label: 'Number line with points a and b' });
var gPlane = L.graph(P.stage, { xmin: -8, xmax: 8, ymin: -8, ymax: 8, width: 520, height: 520, xstep: 1, ystep: 1, xlabelStep: 2, ylabelStep: 2, label: 'Coordinate plane with points P and Q' });
function fmt(v) { return L.num(v); }
var draw = L.scheduler(function () {
  var line = st.mode === 'line';
  gLine.svg.style.display = line ? '' : 'none'; gPlane.svg.style.display = line ? 'none' : '';
  if (line) {
    gLine.clear();
    var a = st.a, b = st.b;
    gLine.line(0, 0.55, a, 0.55, { color: 'orange', width: 6 });
    gLine.text((a) / 2, 0.75, '|a| = ' + L.num(Math.abs(a)), { anchor: 'middle', color: 'orange', size: 15 });
    gLine.line(0, -0.55, b, -0.55, { color: 'purple', width: 6 });
    gLine.text(b / 2, -0.95, '|b| = ' + L.num(Math.abs(b)), { anchor: 'middle', color: 'purple', size: 15 });
    if (st.showOpp) { gLine.dot(-a, 0, { color: 'orange', open: true, r: 9 }); gLine.text(-a, 1.5, '−a', { anchor: 'middle', color: 'orange' }); gLine.dot(-b, 0, { color: 'purple', open: true, r: 9 }); gLine.text(-b, -1.4, '−b', { anchor: 'middle', color: 'purple' }); }
    gLine.text(a, 1.5, 'a', { anchor: 'middle', color: 'orange', weight: 800 });
    gLine.text(b, -1.4 + (st.showOpp ? 0 : 0), 'b', { anchor: 'middle', color: 'purple', weight: 800 });
    gLine.handle(a, 0, { color: 'orange', snap: 0.5, label: 'Point a', onDrag: function (x) { st.a = x; draw(); } });
    gLine.handle(b, 0, { color: 'purple', snap: 0.5, label: 'Point b', onDrag: function (x) { st.b = x; draw(); } });
    var rel = a < b ? '&lt;' : a > b ? '&gt;' : '=';
    read.innerHTML = 'a = ' + fmt(a) + ', b = ' + fmt(b) + '<div class="sub">a ' + rel + ' b · opposite of a = ' + fmt(-a) + ' · |a| = ' + fmt(Math.abs(a)) + ' · |b| = ' + fmt(Math.abs(b)) + '</div>';
    fb.set(a === -b && a !== 0 ? 'a and b are opposites: same distance from 0, same absolute value.' : (a < b && Math.abs(a) > Math.abs(b)) ? 'a is less than b, yet a is farther from 0. Absolute value measures distance, not size.' : 'Drag a and b. The bars show each distance from 0.', '');
    if (!st.live) { st.live = true; ch.update(); return; } /* opening state: nothing found until the student changes something */
    if (a === -4.5) st.seen.opp45 = true;
    st.abs6 = st.abs6 || {}; if (Math.abs(a) === 6) st.abs6[a] = 1; if (Math.abs(b) === 6) st.abs6[b] = 1; if (Object.keys(st.abs6).length >= 2) st.seen.abs6 = true;
    if (a < b && Math.abs(a) > Math.abs(b)) st.seen.lessBigger = true;
  } else {
    gPlane.clear();
    var px = st.px, py = st.py, qx = st.qx, qy = st.qy;
    if (px === qx || py === qy) gPlane.line(px, py, qx, qy, { color: 'green', width: 4, dash: '8 6' });
    gPlane.text(px, py, 'P(' + L.num(px) + ', ' + L.num(py) + ')', { dx: 14, dy: -12, color: 'orange', weight: 800 });
    gPlane.text(qx, qy, 'Q(' + L.num(qx) + ', ' + L.num(qy) + ')', { dx: 14, dy: 20, color: 'purple', weight: 800 });
    gPlane.handle(px, py, { color: 'orange', snap: 1, label: 'Point P', onDrag: function (x, y) { st.px = x; st.py = y; draw(); } });
    gPlane.handle(qx, qy, { color: 'purple', snap: 1, label: 'Point Q', onDrag: function (x, y) { st.qx = x; st.qy = y; draw(); } });
    var quad = px > 0 && py > 0 ? 'Quadrant I' : px < 0 && py > 0 ? 'Quadrant II' : px < 0 && py < 0 ? 'Quadrant III' : px > 0 && py < 0 ? 'Quadrant IV' : 'on an axis';
    var dist = px === qx ? Math.abs(py - qy) : py === qy ? Math.abs(px - qx) : null;
    read.innerHTML = 'P is ' + quad + '<div class="sub">' + (dist === null ? 'P and Q share no coordinate.' : 'P and Q share ' + (px === qx ? 'x = ' + L.num(px) : 'y = ' + L.num(py)) + ': distance = |' + (px === qx ? L.num(py) + ' − (' + L.num(qy) + ')' : L.num(px) + ' − (' + L.num(qx) + ')') + '| = ' + L.num(dist)) + '</div>';
    fb.set(qx === px && qy === -py && py !== 0 ? 'Q is the reflection of P across the x-axis: only the sign of y changed.' : qx === -px && qy === py && px !== 0 ? 'Q is the reflection of P across the y-axis: only the sign of x changed.' : 'Drag P and Q, or use the reflect buttons.', '');
    if (px < 0 && py < 0) st.seen.q3 = true;
    if (px === qx && Math.abs(py - qy) === 7) st.seen.vert7 = true;
  }
  ch.update();
});
draw();
