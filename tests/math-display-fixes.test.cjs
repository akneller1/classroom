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
