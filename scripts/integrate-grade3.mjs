// Assemble Grade 3 from FinancialAlgebra into the public Classroom artifact.
// This runs only in the Classroom production workflow after Grade 4.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const source=path.resolve(process.env.GRADE3_SOURCE_DIR||'_course_sources/grade3');
const out=path.resolve('_site');
const fail=message=>{throw Error('Grade 3 release: '+message);};
const m=JSON.parse(fs.readFileSync(path.join(source,'manifest.json'),'utf8'));
const banks=m.banks.filter(b=>b.courseId==='math3');
if(banks.length!==11||banks.some(b=>b.preview!==true&&b.approved!==true))fail('expected eleven verified Grade 3 source banks');
const assembler=path.join(source,'tools/grade3-authoring/staging/assemble-grade3.mjs');
if(!fs.existsSync(assembler))fail('staging assembler missing');
const {grade3Ready,assembleGrade3}=await import(pathToFileURL(assembler).href);
if(!grade3Ready(source))fail('source not ready');
const course=assembleGrade3({source,out});
if(course.units.length!==11)fail('expected eleven units');
const skills=course.skills;
delete course.skills;
const bridge='(function(G){var course='+JSON.stringify(course)+',skills='+JSON.stringify(skills)+';'+
'var L=G.LIBRARY;if(!L||!L.courses)throw Error("Grade 3 library missing");'+
'L.courses=L.courses.filter(function(c){return c.id!=="grade3"});L.courses.push(course);'+
'var C=G.MK_COURSE_CATALOG,old=C.getSkills,records=C.getSkillRecords;'+
'C.getSkills=function(c,u){return c==="grade3"&&skills[u]?skills[u].slice():old(c,u)};'+
'C.getSkillRecords=function(c,u){return c==="grade3"&&skills[u]?skills[u].map(function(n,i){return {id:u+"-skill-"+String(i+1).padStart(2,"0"),name:n,index:i+1}}):records(c,u)};'+
'})(window);\n';
fs.writeFileSync(path.join(out,'grade3-main-catalog.js'),bridge);
const index=path.join(out,'index.html');let html=fs.readFileSync(index,'utf8');
// Version public assets whenever a course is released. The long-lived old
// scripts otherwise remain cached even after GitHub Pages deploys new source.
const version='elementary-parity-20261113';
for(const name of ['app.js','integrated-student-share.js','student-share-cards.js']){
 const exp=new RegExp('('+name.replace(/\\./g,'\\\\.')+')\\\\?v=[^"\\\\s]+','g');
 html=html.replace(exp,'$1?v='+version);
}

const anchor='<script src="app.js';
if(!html.includes(anchor))fail('homepage script anchor missing');
html=html.replace(anchor,'<script src="grade3-main-catalog.js?v=grade3-release"></script>\n'+anchor);
fs.writeFileSync(index,html);
const appFile=path.join(out,'app.js');let app=fs.readFileSync(appFile,'utf8');
const patch=(oldPart,newPart,label)=>{if(!app.includes(oldPart))fail('missing '+label+' anchor');app=app.replace(oldPart,newPart);};
patch("['grade4','grade5','financial-algebra'].includes(it.c.id)","['grade3','grade4','grade5','financial-algebra'].includes(it.c.id)",'thumbnail');
patch("['grade4','grade5'].includes(c.id)) return algebraUnitView(c, u)","['grade3','grade4','grade5'].includes(c.id)) return algebraUnitView(c, u)",'unit renderer');
patch("'grade4', 'grade5', 'financial-algebra'].indexOf(c.id)","'grade3', 'grade4', 'grade5', 'financial-algebra'].indexOf(c.id)",'course label');
patch("(['grade4','grade5'].includes(c.id) ? category('projects', 'Projects', ['other']) : '')","(['grade3','grade4','grade5'].includes(c.id) ? category('projects', 'Projects', ['other']) : '')",'project category');
// Grade 4's release build already deduplicates coming-soon placeholders.
if(!app.includes('SOON.filter(function(c){return !L.courses.some(function(p){return p.id===c.id;});})'))fail('missing course deduplication');
const genCourse="(c && c.id === 'grade5' && c.units[0] ? c.units[0].artifacts : [])";
if(app.includes(genCourse))app=app.replace(genCourse,"(c && ['grade3','grade4','grade5'].includes(c.id) && c.units[0] ? c.units[0].artifacts : [])");
fs.writeFileSync(appFile,app);
for(const page of ['worksheet.html','menu-assessment.html','lesson-planner.html','printables.html','vocabulary.html']){
 const f=path.join(out,'worksheet-generator',page);if(!fs.existsSync(f))fail('missing '+page);
 let h=fs.readFileSync(f,'utf8'),anchor='<script src="../grade4-main-catalog.js';
 if(!h.includes(anchor))fail('Grade 4 course catalog anchor missing in '+page);
 h=h.replace(anchor,'<script src="../grade3-main-catalog.js?v=grade3-release"></script>\\n'+anchor);
 if(page==='lesson-planner.html')h=h.replace(/planner\\/planner-ui\\.js\\?v=[^"]+/,'planner/planner-ui.js?v='+version);
 fs.writeFileSync(f,h);
}
const manifestFile=path.join(out,'question-banks/manifest.json');
const native=JSON.parse(fs.readFileSync(manifestFile,'utf8'));
native.banks=native.banks.filter(b=>b.courseId!=='grade3');
for(const unit of course.units){
 const entry=banks.find(b=>b.unitId===unit.id);
 if(!entry)fail('missing bank for '+unit.id);
 const src=JSON.parse(fs.readFileSync(path.join(source,entry.path),'utf8'));
 if(src.questions.length<1)fail('empty bank for '+unit.id);
 src.courseId='grade3';
 for(const q of src.questions)if(q.diagram?.spec?.src){
  const rel=q.diagram.spec.src;
  if(!/^[a-z0-9/_-]+\.png$/i.test(rel)||rel.startsWith('/')||rel.includes('..'))fail('unsafe diagram '+rel);
  const target='question-banks/assets/grade3/'+rel;
  fs.mkdirSync(path.dirname(path.join(out,target)),{recursive:true});
  fs.copyFileSync(path.join(source,rel),path.join(out,target));
  q.diagram.spec.src=target;
 }
 const target='question-banks/grade3/'+unit.id+'.json';
 fs.mkdirSync(path.dirname(path.join(out,target)),{recursive:true});
 fs.writeFileSync(path.join(out,target),JSON.stringify(src));
 native.banks.push({courseId:'grade3',unitId:unit.id,path:target,approved:true,teacherUse:true});
}
fs.writeFileSync(manifestFile,JSON.stringify(native,null,2)+'\n');
console.log('Grade 3 assembled: 11 units from FinancialAlgebra, using existing Classroom generators and Grade 3 players.');
