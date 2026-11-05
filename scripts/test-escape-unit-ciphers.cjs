/* Regression for unit-specific Escape Room cipher challenges across all courses.
   Ensures a relevant integer shift exists at every difficulty, with systems
   requiring actual two-equation elimination instead of a generic equation. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
function execute(file,w){
 const src=fs.readFileSync(path.join(root,file),'utf8');
 new vm.Script(src,{filename:file}).runInNewContext(w);
 return src;
}
const env={Math,console};env.window=env;env.globalThis=env;
execute('course-catalog.js',env);
execute('worksheet-generator/games/cipher-questions.js',env);
const model=env.MK_CIPHER_QUESTIONS,skills=env.MK_COURSE_CATALOG.skills;
// Every catalog unit needs its own complete Escape Room theme and solvable key cards.
const themes=JSON.parse(fs.readFileSync(path.join(root,'worksheet-generator/games/escape-themes.json'),'utf8'));
const themeKeys=Object.entries(skills).flatMap(([course,units])=>Object.keys(units).map(unit=>course+'/'+unit));
assert.deepEqual(Object.keys(themes).sort(),themeKeys.sort(),'Theme coverage must match the course catalog');
for(const key of themeKeys){
 const t=themes[key];
 for(const field of ['title','room','intro','introEmoji','endEmoji','word','cipher','clue','ask','outro'])assert.ok(typeof t[field]==='string'&&t[field].trim(),key+': missing '+field);
 assert.match(t.word,/^[A-Z]{5}$/,key+': five-letter final password');
 assert.ok(t.cipher.split(/[^A-Z]+/).includes(t.clue),key+': cipher contains its clue word');
 assert.equal(t.stamps.length,5,key+': five key cards');
 assert.equal(new Set(t.stamps).size,5,key+': stamps must have an unambiguous order');
 assert.equal(t.letters.length,5,key+': five key-card letters');
 assert.equal(t.stamps.map((stamp,i)=>({stamp,letter:t.letters[i]})).sort((a,b)=>a.stamp-b.stamp).map(c=>c.letter).join(''),t.word,key+': ordered key cards spell the final password');
}
for(const field of ['title','word','clue'])assert.equal(new Set(Object.values(themes).map(t=>t[field])).size,themeKeys.length,'Every unit must have a distinct '+field);
console.log('PASS '+themeKeys.length+' unique Escape Room themes, cipher clues and key-card passwords');
let count=0,systems=0;
for(const [course,units] of Object.entries(skills)){
 for(const unit of Object.keys(units)){
  assert.ok(model.familyByUnit[course]?.[unit],course+'/'+unit+': mapped to specific math topic');
  for(const level of ['cp2','cp1','honors'])for(let seed=0;seed<20;seed++){
   const q=model.create({courseId:course,unitId:unit,level});
   assert.ok(q&&q.cipherFamily,course+'/'+unit+': has unit-specific problem');
   assert.ok(Number.isInteger(+q.answer)&&+q.answer>=1&&+q.answer<=25,course+'/'+unit+': shift is valid');
   assert.ok(q.prompt&&q.solutionSteps?.length,course+'/'+unit+': mathematical problem and hints');
   assert.equal(q.format,'short-answer',course+'/'+unit+': number typed, not guessed from choices');
   assert.equal(q.cipherFamily,model.familyByUnit[course][unit],course+'/'+unit+': correct family');
   count++;
   if(q.cipherFamily==='systems'){
    systems++;
    assert.match(q.prompt,/Solve the system:/,course+'/'+unit+': must solve system');
    assert.match(q.prompt,/x .* \d*y =/,course+'/'+unit+': first equation contains x and y');
    assert.match(q.prompt,/and .*x .* \d*y =/,course+'/'+unit+': second equation contains x and y');
    const shift=+q.answer;
    if(level==='cp2'){
      const m=q.prompt.match(/x \+ y = (-?\d+) and x − y = (-?\d+)/);
      assert.ok(m,'CP2: equivalent elimination system');
      assert.equal((+m[1]+(+m[2]))/2,shift,'CP2: x matches the locked shift');
    }else if(level==='cp1'){
      const m=q.prompt.match(/2x \+ (\d+)y = (-?\d+) and 3x − (\d+)y = (-?\d+)/);
      assert.ok(m&&m[1]===m[3],'CP1: y cancels on addition');
      assert.equal((+m[2]+(+m[4]))/5,shift,'CP1: x matches shift');
    }else{
      const m=q.prompt.match(/(\d+)x \+ (\d+)y = (-?\d+) and (\d+)x − (\d+)y = (-?\d+)/);
      assert.ok(m&&m[2]===m[5],'Honors: y cancels on addition');
      assert.equal((+m[3]+(+m[6]))/(+m[1]+(+m[4])),shift,'Honors: x matches shift');
    }
   }
  }
 }
}
assert.equal(model.create({courseId:'algebra',unitId:'not-a-unit',level:'cp1'}),null,
  'an unrecognized unit must not fall back to a generic equation');
const courseSource=fs.readFileSync(path.join(root,'worksheet-generator/games/course-activity.js'),'utf8');
assert.doesNotMatch(courseSource,/backupShift\s*\(/,'old generic equation fallback removed');
assert.match(courseSource,/source\.unit\.id\.includes\('system'\)/,'systems must use system-solving cipher');
assert.match(courseSource,/MK_CIPHER_QUESTIONS/,'shared room uses unit-specific question model');
const html=fs.readFileSync(path.join(root,'worksheet-generator/course-activity.html'),'utf8');
assert.match(html,/cipher-questions\.js[^"]*"><\/script><script src="games\/course-activity\.js/,
 'unit cipher questions must load before course activity');
console.log('PASS: '+count+' unit-aligned questions across 8 courses, 77 units, and three levels; '+systems+' systems solved for x.');
