'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const context=vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(__dirname,'../worksheet-generator/core/math-display.js'),'utf8'),context);
const M=context.MK_MATH_DISPLAY;
test('word hyphens and algebraic minus signs remain distinct',()=>{
 for(const text of ['x-axis','sign-up','24-pound','row-echelon'])assert.ok(M.html(text).includes('-'),text);
 for(const text of ['2x-3','a-b','AB-CD','5-cos(x)'])assert.ok(M.html(text).includes('−'),text);
});
test('money and trig formatting preserve numeric precision and powers',()=>{
 assert.equal(M.money('$2.5 and $1,050.5 and $3.141'),'$2.50 and $1,050.50 and $3.141');
 assert.equal(M.trigSquares('cos(x)² + sec(2x)^2'),'cos²(x) + sec²(2x)');
 assert.equal(M.trigSquares('cos(x)^20'),'cos(x)^20');
});
test('rectangular matrices render as grids while fractions and malformed rows stay separate',()=>{
 assert.ok(M.html('[1, 2; 3, 4]').includes('class="mxg"'));
 assert.ok(M.html('A = [1, 2]').includes('class="mxg"'));
 assert.equal(M.hasMatrix('[[1 ; 2]]'),false);
 assert.equal(M.hasMatrix('[1,2;3]'),false);
 assert.ok(M.html('[[1 ; 2]]').includes('class="fr"'));
 assert.ok(!M.html('<script>alert(1)</script>').includes('<script>'));
});
test('standard-form systems align variable columns below the directions',()=>{
 const prompt='Solve by elimination: 2x + 3y = 7 and -14x - y = 5.';
 const html=M.layout(prompt);
 assert.ok(html.indexOf('elimination')<html.indexOf('mk-givens'));
 assert.match(html,/repeat\(4,auto\)/);
 assert.match(html,/>2<i>x<\/i><\/span><span[^>]*>\+ 3<i>y<\/i>/);
 assert.match(html,/>−14<i>x<\/i><\/span><span[^>]*>− <i>y<\/i>/);
});
test('three-variable systems and inequalities keep empty variable columns',()=>{
 const system=M.layout('Solve the system: x + y + z = 11; x + 2z = 8; y + 3z = 11. Give the answer as (x, y, z).');
 assert.match(system,/repeat\(5,auto\)/);
 assert.match(system,/2<i>z<\/i>/);
 assert.match(system,/<span class="mk-given-term"><\/span>/);
 const region=M.layout('Find the maximum of P = 7x + 9y subject to x ≥ 0, y ≥ 0, x + y ≤ 5.');
 assert.equal((region.match(/class="mk-given-relation"/g)||[]).length,3);
 assert.match(region,/subject<\/span> <span class="tx">to<\/span>:/);
});
test('piecewise branches share columns and inline math in other prompts stays inline',()=>{
 assert.match(M.layout('f(x) = { x² - 1 if x < 2; 3x - 4 if x ≥ 2 }. Find f(-3).'),/class="mk-piecewise".*repeat\(2,auto\).*if.*if.*Find/);
 assert.match(M.layout('f(x) = -2x² for x ≤ 3 and f(x) = mx + b for x > 3. Find m and b.'),/class="mk-piecewise"/);
 for(const prompt of ['Solve 1 ≤ x ≤ 3.', 'Evaluate x²y when x = 6 and y = 5.', 'Write y = 2x/3 - 5/3 in standard form Ax + By = C.'])assert.equal(M.layout(prompt),null,prompt);
});
