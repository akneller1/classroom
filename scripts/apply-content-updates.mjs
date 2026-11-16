// Classroom-owned overlays applied after assembling the pinned elementary releases.
import fs from 'node:fs';import path from 'node:path';
const out=path.resolve(process.argv[2]||'_site'),source=path.resolve('content-updates/2026-11-15'),read=p=>JSON.parse(fs.readFileSync(p,'utf8')),write=(p,d)=>fs.writeFileSync(p,JSON.stringify(d,null,1)+'\n');let appended=0,edits=0;
function patchBank(file,changes){const d=read(file),byId=new Map(d.questions.map(q=>[q.id,q]));for(const e of changes){const q=byId.get(e.id);if(!q)throw Error('Content update missing item '+e.id+' in '+file);for(const [field,c]of Object.entries(e.changes||{[e.field]:{from:e.from,to:e.to}})){if('append'in c){if(!q[field].includes(c.append))q[field]+=c.append}else if(JSON.stringify(q[field])!==JSON.stringify(c.to)){if(JSON.stringify(q[field]??null)!==JSON.stringify(c.from??null))throw Error('Content update conflict '+e.id+'/'+field);q[field]=c.to;edits++}}}write(file,d)}
const retags=read(path.join(source,'grade1-telling-time-retag.json')).edits;
for(const rel of ['grade1/question-banks/math1/telling-time.json','question-banks/grade1/telling-time.json'])patchBank(path.join(out,rel),retags);
for(const course of ['math1','math2','math3','math4','math5']){
 const folder=path.join(source,'elementary',course);if(!fs.existsSync(folder))continue;const grade=course.replace('math','grade');
 for(const name of fs.readdirSync(folder)){const d=read(path.join(folder,name)),unit=name.replace('.additions.json','');
  for(const rel of [`question-banks/${grade}/${unit}.json`,(course==='math5'?`${grade}/${course}/${unit}.json`:`${grade}/question-banks/${course}/${unit}.json`)]){
   const file=path.join(out,rel),bank=read(file),seen=new Set(bank.questions.map(q=>q.id));for(const original of d.questions){if(rel.startsWith(grade+'/')&&original.format==='plot')continue;if(seen.has(original.id))continue;const q=structuredClone(original);if(q.diagram?.spec?.src){const src=q.diagram.spec.src;if(rel.startsWith(grade+'/'))q.diagram.spec.src='question-banks/assets/content-20261115/'+src.split('/').at(-1);if(rel.startsWith(grade+'/')){const target=path.join(out,grade,q.diagram.spec.src);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(out,src),target)}}if(bank.courseId===grade)q.courseId=grade;bank.questions.push(q);appended++}write(file,bank);
  }
 }
}
const fa=read(path.join(source,'financial-algebra-standards.json'));
for(const folder of ['financial-algebra/question-banks/financial-algebra','financial-algebra/financial/banks','financial/banks']){
 const dir=path.join(out,folder);if(!fs.existsSync(dir))continue;
 for(const name of fs.readdirSync(dir)){if(!name.endsWith('.json')||name==='index.json')continue;const file=path.join(dir,name),bank=read(file);for(const q of bank.questions||[]){const unit=name.replace('.json',''),tags=fa.mapping[q.skillId];if(tags){q.standards=tags;edits++}}write(file,bank)}
}
// Version all touched shared scripts in the final artifact, including copied grade players.
const touched=['math-display.js','math-display.css','graph-input.js','question-bank-adapter.js','algebra2-bank-native.js','practice/practice.js','approved-games.js','approved-game-items.js','resource-eligibility.js','course-catalog.js','course-source.js','bank-printable.js',
 /* 2026-11-16 re-audit fixes */ 'question-bank-loader.js','approved-bank-bridge.js','approved-flashcards.js','algebra2-practice.js','menu/app.js','printables-ui.js','planner-ui.js','skill-setup.js','games/games.js','vendor/games.js','student-game-share.js','course-integrations.js','styles.css','level-labels.js'];
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const f=path.join(dir,e.name);if(e.isDirectory())walk(f);else if(/\.(html|js|mjs)$/.test(e.name)&&!f.includes('/vendor/')){let s=fs.readFileSync(f,'utf8');s=s.replace(/Remedial/g,'Support');if(e.name.endsWith('.html')){for(const name of touched){const escaped=name.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');s=s.replace(new RegExp('('+escaped+')(?:\\?v=[^"\\s<>]*)?(?=")','g'),'$1?v=showdown-ramp-20261116')}for(const name of ['core/plot.js','menu/verify.js','menu/skills/algebra1-linear-equations-slope.js']){const escaped=name.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');s=s.replace(new RegExp('('+escaped+')(?:\\?v=[^"\\s<>]*)?(?=")','g'),'$1?v=secondary-stats-20261115')}if(s.includes('</body>')&&!s.includes('level-labels.js')){const base=path.relative(path.dirname(f),out).split(path.sep).join('/');s=s.replace('</body>','<script src="'+(base?base+'/':'')+'level-labels.js?v=labels-20261116b"></script></body>')}}fs.writeFileSync(f,s)}}}
// Pinned Grade 4 copies get the approved labels by ID. Future questions retain
// their pending status until they receive their own review.
const reviewedGrade4=new Set(read(path.resolve('scripts/review-status/approved-grade4-ids.json')));
function reviewImported(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);if(entry.isDirectory())reviewImported(file);else if(entry.name.endsWith('.json')){const text=fs.readFileSync(file,'utf8');if(text.includes('Awaiting human review')){const data=JSON.parse(text);let changed=false;function visit(v){if(!v||typeof v!=='object')return;if(reviewedGrade4.has(v.id)&&typeof v.sourceNotes==='string'&&v.sourceNotes.includes('Awaiting human review')){v.sourceNotes=v.sourceNotes.replaceAll('Awaiting human review','Teacher reviewed 2026-11-15');changed=true}for(const value of Object.values(v))if(typeof value==='object')visit(value)}visit(data);if(changed)write(file,data)}}}}
reviewImported(out);
walk(out);
console.log('Classroom content overlays: '+appended+' question copies, '+edits+' metadata edits.');
