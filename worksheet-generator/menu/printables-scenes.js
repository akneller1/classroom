/* Color by Number scenes: original line drawings (viewBox 600 × 560), each with exactly 10 color groups.
   A group = one color; every region in it gets the same problem number. Groups are drawn in order (background
   first). `labels` are where the number is printed; `extra` is drawn on top as plain lines (rays, ropes, eyes). */
(function (G) {
  'use strict';
  var PR = (G.MKMENU.printables = G.MKMENU.printables || {});
  var C = {
    'Light Blue': '#9fd6f5', Blue: '#2f6fd6', Yellow: '#f6d53f', Orange: '#f39a2b', Red: '#e0393e', Pink: '#f39bc4', Purple: '#8a55c9',
    Green: '#3aa655', 'Light Green': '#a6dc6f', Brown: '#8b5a2b', Gray: '#b4bac3', Tan: '#e8cf9a', Black: '#3a3a3a'
  };
  PR.SCENE_COLORS = C;
  function cloud(x, y, w) {   // flat-bottomed cloud with three bumps
    var a = w * 0.32, b = w * 0.42, c = w - a - b;
    return '<path d="M' + x + ' ' + y + ' a' + a / 2 + ' ' + a / 2 + ' 0 0 1 ' + a + ' 0 a' + b / 2 + ' ' + b / 2 + ' 0 0 1 ' + b + ' 0 a' + c / 2 + ' ' + c / 2 + ' 0 0 1 ' + c + ' 0 z"/>';
  }
  function star(cx, cy, R, r) {
    var p = [];
    for (var k = 0; k < 10; k++) { var ang = -Math.PI / 2 + k * Math.PI / 5, rr = k % 2 ? r : R; p.push((cx + rr * Math.cos(ang)).toFixed(1) + ',' + (cy + rr * Math.sin(ang)).toFixed(1)); }
    return '<polygon points="' + p.join(' ') + '"/>';
  }
  function rays(cx, cy, r1, r2, n) {
    var s = '';
    for (var k = 0; k < n; k++) { var a = k * 2 * Math.PI / n; s += '<line x1="' + (cx + r1 * Math.cos(a)).toFixed(1) + '" y1="' + (cy + r1 * Math.sin(a)).toFixed(1) + '" x2="' + (cx + r2 * Math.cos(a)).toFixed(1) + '" y2="' + (cy + r2 * Math.sin(a)).toFixed(1) + '"/>'; }
    return s;
  }
  function circle(x, y, r) { return '<circle cx="' + x + '" cy="' + y + '" r="' + r + '"/>'; }
  function rect(x, y, w, h, rx) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '"' + (rx ? ' rx="' + rx + '"' : '') + '/>'; }
  function path(d) { return '<path d="' + d + '"/>'; }
  var T = 'M300 118';   // balloon top
  PR.SCENES = {
    balloon: { name: 'Hot-air balloon', groups: [
      { color: 'Light Blue', shapes: [rect(0, 0, 600, 560)], labels: [[60, 60], [200, 40], [330, 50], [60, 300], [560, 300], [120, 380], [470, 390]] },
      { color: 'Orange', shapes: [circle(495, 92, 42)], labels: [[495, 97]] },
      { color: 'Gray', shapes: [cloud(40, 200, 130), cloud(420, 250, 150), cloud(60, 345, 120)], labels: [[105, 188], [495, 238], [120, 333]] },
      { color: 'Light Green', shapes: [path('M0 470 C150 425 330 440 600 415 L600 560 L0 560 Z')], labels: [[520, 450], [60, 485]] },
      { color: 'Green', shapes: [path('M0 520 C180 490 420 515 600 492 L600 560 L0 560 Z')], labels: [[300, 535], [530, 530]] },
      { color: 'Pink', shapes: [path(T + ' C195 118 160 270 255 372 L280 372 C228 290 240 150 300 118 Z'), path(T + ' C405 118 440 270 345 372 L320 372 C372 290 360 150 300 118 Z')], labels: [[225, 260], [375, 260]] },
      { color: 'Yellow', shapes: [path(T + ' C240 150 228 290 280 372 L292 372 C275 300 282 160 300 118 Z'), path(T + ' C360 150 372 290 320 372 L308 372 C325 300 318 160 300 118 Z')], labels: [[262, 240], [338, 240]] },
      { color: 'Red', shapes: [path(T + ' C282 160 275 300 292 372 L308 372 C325 300 318 160 300 118 Z')], labels: [[300, 200], [300, 300]] },
      { color: 'Purple', shapes: [path('M255 372 L345 372 L330 402 L270 402 Z')], labels: [[300, 392]] },
      { color: 'Brown', shapes: [path('M268 468 L332 468 L326 520 L274 520 Z')], labels: [[300, 499]] }],
      extra: rays(495, 92, 52, 72, 12) + '<line x1="272" y1="402" x2="276" y2="468"/><line x1="328" y1="402" x2="324" y2="468"/><line x1="290" y1="402" x2="292" y2="468"/><line x1="310" y1="402" x2="308" y2="468"/>' },
    sailboat: { name: 'Sailboat', groups: [
      { color: 'Light Blue', shapes: [rect(0, 0, 600, 365)], labels: [[200, 40], [460, 170], [80, 230], [540, 60], [120, 330]] },
      { color: 'Yellow', shapes: [circle(85, 85, 40)], labels: [[85, 90]] },
      { color: 'Gray', shapes: [cloud(360, 70, 150), cloud(160, 150, 110)], labels: [[435, 58], [215, 138]] },
      { color: 'Green', shapes: [path('M410 365 C440 300 540 290 600 320 L600 365 Z')], labels: [[540, 340]] },
      { color: 'Blue', shapes: [path('M0 365 L600 365 L600 560 L0 560 Z')], labels: [[70, 470], [300, 515], [540, 470], [150, 400]] },
      { color: 'Brown', shapes: [path('M140 380 L460 380 L405 448 L195 448 Z')], labels: [[300, 432]] },
      { color: 'Red', shapes: [path('M150 384 L450 384 L440 398 L160 398 Z')], labels: [[300, 394]] },
      { color: 'Orange', shapes: [path('M306 112 L306 362 L478 362 Z')], labels: [[360, 300]] },
      { color: 'Pink', shapes: [path('M294 132 L294 362 L165 362 Z')], labels: [[255, 310]] },
      { color: 'Purple', shapes: [path('M302 84 L348 98 L302 112 Z')], labels: [[318, 102]] }],
      extra: rays(85, 85, 50, 68, 10) + '<line x1="300" y1="84" x2="300" y2="380" stroke-width="5"/><path d="M60 420 q15 -10 30 0 q15 10 30 0 M420 500 q15 -10 30 0 q15 10 30 0 M220 480 q15 -10 30 0 q15 10 30 0" fill="none"/>' },
    house: { name: 'House', groups: [
      { color: 'Light Blue', shapes: [rect(0, 0, 600, 560)], labels: [[60, 120], [290, 60], [560, 200], [420, 160], [60, 330]] },
      { color: 'Yellow', shapes: [circle(510, 80, 40)], labels: [[510, 85]] },
      { color: 'Gray', shapes: [cloud(40, 70, 130), cloud(250, 120, 120)], labels: [[105, 58], [310, 108]] },
      { color: 'Light Green', shapes: [path('M0 448 C150 428 450 458 600 438 L600 560 L0 560 Z')], labels: [[80, 500], [300, 520], [520, 505]] },
      { color: 'Tan', shapes: [rect(150, 262, 230, 188)], labels: [[265, 285], [175, 420], [345, 420]] },
      { color: 'Red', shapes: [path('M128 268 L265 160 L402 268 Z')], labels: [[265, 235]] },
      { color: 'Brown', shapes: [rect(240, 362, 50, 88), rect(470, 360, 26, 92)], labels: [[265, 410], [483, 420]] },
      { color: 'Blue', shapes: [rect(172, 300, 50, 46), rect(308, 300, 50, 46)], labels: [[197, 328], [333, 328]] },
      { color: 'Green', shapes: [path('M483 250 C540 250 560 300 540 330 C560 370 500 390 483 372 C460 392 410 370 428 330 C410 300 430 250 483 250 Z')], labels: [[483, 320]] },
      { color: 'Pink', shapes: [circle(60, 470, 11), circle(110, 485, 11), circle(400, 480, 11), circle(560, 470, 11)], labels: [[60, 474], [110, 489], [400, 484], [560, 474]] }],
      extra: rays(510, 80, 50, 66, 10) + '<line x1="197" y1="300" x2="197" y2="346"/><line x1="172" y1="323" x2="222" y2="323"/><line x1="333" y1="300" x2="333" y2="346"/><line x1="308" y1="323" x2="358" y2="323"/><circle cx="282" cy="408" r="3" fill="#000"/>' },
    rocket: { name: 'Rocket', groups: [
      { color: 'Purple', shapes: [rect(0, 0, 600, 560)], labels: [[60, 300], [540, 120], [420, 260], [180, 500], [520, 330], [60, 60], [390, 520]] },
      { color: 'Yellow', shapes: [star(250, 70, 18, 8), star(470, 180, 16, 7), star(80, 410, 18, 8), star(540, 260, 14, 6), star(410, 400, 14, 6)], labels: [[250, 74], [470, 184], [80, 414], [540, 264], [410, 404]] },
      { color: 'Green', shapes: [circle(120, 150, 58)], labels: [[120, 128]] },
      { color: 'Tan', shapes: ['<path fill-rule="evenodd" d="M30 160 a90 26 -15 1 0 180 -40 a90 26 -15 1 0 -180 40 Z M50 156 a70 16 -15 1 0 140 -32 a70 16 -15 1 0 -140 32 Z"/>'], labels: [[45, 175]] },
      { color: 'Gray', shapes: [circle(500, 470, 55)], labels: [[500, 455]] },
      { color: 'Orange', shapes: [path('M272 462 Q300 560 328 462 Z')], labels: [[300, 490]] },
      { color: 'Light Blue', shapes: [path('M255 230 L345 230 L345 462 L255 462 Z')], labels: [[300, 370], [300, 430]] },
      { color: 'Red', shapes: [path('M255 390 L212 470 L255 452 Z'), path('M345 390 L388 470 L345 452 Z')], labels: [[240, 445], [360, 445]] },
      { color: 'Pink', shapes: [path('M255 230 Q300 110 345 230 Z')], labels: [[300, 200]] },
      { color: 'Blue', shapes: [circle(300, 296, 28)], labels: [[300, 301]] }],
      extra: '<circle cx="482" cy="490" r="9" fill="none"/><circle cx="520" cy="452" r="7" fill="none"/><circle cx="510" cy="500" r="5" fill="none"/>' },
    ocean: { name: 'Under the sea', groups: [
      { color: 'Blue', shapes: [rect(0, 0, 600, 560)], labels: [[60, 60], [540, 80], [100, 330], [550, 220], [330, 400], [520, 380]] },
      { color: 'Tan', shapes: [path('M0 470 C150 440 400 482 600 455 L600 560 L0 560 Z')], labels: [[80, 520], [460, 530]] },
      { color: 'Gray', shapes: [path('M210 480 C210 440 280 430 300 470 C310 450 350 455 350 485 Z'), path('M500 470 C505 440 565 440 570 468 Z')], labels: [[268, 466], [535, 461]] },
      { color: 'Green', shapes: [path('M60 470 C40 420 90 390 65 340 C50 300 85 280 80 250 L92 250 C100 290 66 300 82 340 C102 390 58 420 76 470 Z'), path('M120 475 C110 430 145 400 128 360 L140 360 C158 400 124 430 134 475 Z'), path('M410 462 C395 420 430 390 412 345 L424 345 C444 390 410 420 424 462 Z')], labels: [[72, 425], [127, 440], [418, 425]] },
      { color: 'Red', shapes: [path('M560 456 L560 380 C545 370 540 350 552 340 C560 360 568 360 572 345 C584 360 586 380 575 395 L575 456 Z')], labels: [[566, 420]] },
      { color: 'Pink', shapes: [star(170, 505, 32, 13)], labels: [[170, 510]] },
      { color: 'Orange', shapes: [path('M160 220 C190 160 300 160 330 220 C300 280 190 280 160 220 Z')], labels: [[230, 240]] },
      { color: 'Yellow', shapes: [path('M330 220 L390 175 L385 265 Z'), path('M220 172 C240 140 280 140 290 172 Z'), path('M220 268 C245 290 270 288 280 268 Z')], labels: [[368, 222], [255, 162], [250, 280]] },
      { color: 'Purple', shapes: [path('M400 320 C420 285 480 285 495 320 C480 355 420 355 400 320 Z M495 320 L530 295 L528 345 Z')], labels: [[450, 330], [516, 320]] },
      { color: 'Light Blue', shapes: [circle(340, 140, 12), circle(360, 105, 9), circle(372, 75, 6), circle(380, 270, 9), circle(392, 245, 6)], labels: [[340, 144], [360, 109]] }],
      extra: '<circle cx="190" cy="212" r="7" fill="#fff"/><circle cx="190" cy="212" r="3" fill="#000"/><circle cx="420" cy="314" r="5" fill="#fff"/><circle cx="420" cy="314" r="2.3" fill="#000"/>' },
    lighthouse: { name: 'Lighthouse', groups: [
      { color: 'Light Blue', shapes: [rect(0, 0, 600, 400)], labels: [[300, 40], [540, 230], [420, 300], [40, 60], [560, 60]] },
      { color: 'Gray', shapes: [cloud(360, 80, 150), cloud(420, 200, 110)], labels: [[435, 68], [475, 188]] },
      { color: 'Blue', shapes: [rect(0, 400, 600, 160)], labels: [[450, 470], [540, 530], [380, 520]] },
      { color: 'Brown', shapes: [path('M0 330 L262 330 L322 400 L335 560 L0 560 Z')], labels: [[110, 450], [250, 500]] },
      { color: 'Green', shapes: [path('M0 318 C80 300 180 306 272 320 L262 336 L0 336 Z')], labels: [[40, 326], [230, 327]] },
      { color: 'Red', shapes: [path('M95 140 L175 140 L178 185 L92 185 Z'), path('M89 230 L181 230 L184 275 L86 275 Z')], labels: [[135, 165], [135, 255]] },
      { color: 'Tan', shapes: [path('M92 185 L178 185 L181 230 L89 230 Z'), path('M86 275 L184 275 L187 320 L83 320 Z')], labels: [[110, 210], [160, 210], [105, 300]] },
      { color: 'Purple', shapes: [rect(140, 282, 26, 38)], labels: [[153, 304]] },
      { color: 'Yellow', shapes: [rect(100, 105, 70, 35), path('M170 110 L330 78 L330 152 Z')], labels: [[135, 126], [300, 116]] },
      { color: 'Black', shapes: [path('M90 105 L135 70 L180 105 Z')], labels: [[135, 96]] }],
      extra: '<line x1="118" y1="105" x2="118" y2="140"/><line x1="152" y1="105" x2="152" y2="140"/><path d="M380 450 q15 -10 30 0 q15 10 30 0 M470 500 q15 -10 30 0 q15 10 30 0" fill="none"/>' }
  };
})(typeof window !== 'undefined' ? window : globalThis);
