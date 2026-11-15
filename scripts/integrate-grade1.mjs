import { addAsteroidBlaster } from './asteroid-resources.mjs';
import { addMultipleDrop } from './multiple-drop-resources.mjs';
import { addMatchingGames } from './matching-resources.mjs';
// Assemble Grade 1 from FinancialAlgebra into the public Classroom artifact.
// This runs only in the Classroom production workflow after Grade 2.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const source=path.resolve(process.env.GRADE1_SOURCE_DIR||'_course_sources/grade1');
const out=path.resolve('_site');
const fail=message=>{throw Error('Grade 1 release: '+message);};
const m=JSON.parse(fs.readFileSync(path.join(source,'manifest.json'),'utf8'));
const banks=m.banks.filter(b=>b.courseId==='math1');
if(banks.length!==12||new Set(banks.map(b=>b.unitId)).size!==12||banks.some(b=>b.preview!==true||b.approved!==false))fail('expected twelve verified Grade 1 source banks');
const assembler=path.join(source,'tools/grade1-authoring/staging/assemble-grade1.mjs');
if(!fs.existsSync(assembler))fail('staging assembler missing');
const {grade1Ready,assembleGrade1}=await import(pathToFileURL(assembler).href);
if(!grade1Ready(source))fail('source not ready');
const course=assembleGrade1({source,out});
if(course.units.length!==12)fail('expected twelve units');
addMultipleDrop(course);
addAsteroidBlaster(course);
addMatchingGames(course);
const skills=course.skills;
delete course.skills;
const bridge='(function(G){var course='+JSON.stringify(course)+',skills='+JSON.stringify(skills)+';'+
'var L=G.LIBRARY;if(!L||!L.courses)throw Error("Grade 1 library missing");'+
'L.courses=L.courses.filter(function(c){return c.id!=="grade1"});L.courses.push(course);'+
'var C=G.MK_COURSE_CATALOG,old=C.getSkills,records=C.getSkillRecords;'+
'C.getSkills=function(c,u){return c==="grade1"&&skills[u]?skills[u].slice():old(c,u)};'+
'C.getSkillRecords=function(c,u){return c==="grade1"&&skills[u]?skills[u].map(function(n,i){return {id:u+"-skill-"+String(i+1).padStart(2,"0"),name:n,index:i+1}}):records(c,u)};'+
'})(window);\n';
fs.writeFileSync(path.join(out,'grade1-main-catalog.js'),bridge);
const index=path.join(out,'index.html');let html=fs.readFileSync(index,'utf8');
// Version public assets whenever a course is released. The long-lived old
// scripts otherwise remain cached even after GitHub Pages deploys new source.
const version='grade1-release-20261114';
for(const name of ['app.js','integrated-student-share.js','student-share-cards.js']){
 html=html.replaceAll(name+'?v=',name+'?v='+version+'-');
}

const anchor='<script src="app.js';
if(!html.includes(anchor))fail('homepage script anchor missing');
html=html.replace(anchor,'<script src="grade1-main-catalog.js?v=grade1-release"></script>\n'+anchor);
fs.writeFileSync(index,html);
const appFile=path.join(out,'app.js');let app=fs.readFileSync(appFile,'utf8');
const patch=(oldPart,newPart,label)=>{if(!app.includes(oldPart))fail('missing '+label+' anchor');app=app.replace(oldPart,newPart);};
patch("['grade2','grade3','grade4','grade5','financial-algebra'].includes(it.c.id)","['grade1','grade2','grade3','grade4','grade5','financial-algebra'].includes(it.c.id)",'thumbnail');
patch("['grade2','grade3','grade4','grade5'].includes(c.id)) return algebraUnitView(c, u)","['grade1','grade2','grade3','grade4','grade5'].includes(c.id)) return algebraUnitView(c, u)",'unit renderer');
patch("'grade2', 'grade3', 'grade4', 'grade5', 'financial-algebra'].indexOf(c.id)","'grade1', 'grade2', 'grade3', 'grade4', 'grade5', 'financial-algebra'].indexOf(c.id)",'course label');
// Grade 4's release build already deduplicates coming-soon placeholders.
if(!app.includes('SOON.filter(function(c){return !L.courses.some(function(p){return p.id===c.id;});})'))fail('missing course deduplication');
const genCourse="(c && ['grade2','grade3','grade4','grade5'].includes(c.id) && c.units[0] ? c.units[0].artifacts : [])";
if(app.includes(genCourse))app=app.replace(genCourse,"(c && ['grade1','grade2','grade3','grade4','grade5'].includes(c.id) && c.units[0] ? c.units[0].artifacts : [])");
fs.writeFileSync(appFile,app);
for(const page of fs.readdirSync(path.join(out,'worksheet-generator')).filter(name=>name.endsWith('.html')&&fs.readFileSync(path.join(out,'worksheet-generator',name),'utf8').includes('../course-catalog.js'))){
 const f=path.join(out,'worksheet-generator',page);if(!fs.existsSync(f))fail('missing '+page);
 let h=fs.readFileSync(f,'utf8'),anchor='<script src="../grade3-main-catalog.js';
 if(!h.includes(anchor))fail('Grade 3 course catalog anchor missing in '+page);
 h=h.replace(anchor,'<script src="../grade1-main-catalog.js?v=grade1-release"></script>\n'+anchor);
 if(page==='lesson-planner.html')h=h.replace('planner/planner-ui.js?v=','planner/planner-ui.js?v='+version+'-');
 fs.writeFileSync(f,h);
}
const manifestFile=path.join(out,'question-banks/manifest.json');
const native=JSON.parse(fs.readFileSync(manifestFile,'utf8'));
native.banks=native.banks.filter(b=>b.courseId!=='grade1');
for(const unit of course.units){
 const entry=banks.find(b=>b.unitId===unit.id);
 if(!entry)fail('missing bank for '+unit.id);
 const src=JSON.parse(fs.readFileSync(path.join(source,entry.path),'utf8'));
 if(src.questions.length<1)fail('empty bank for '+unit.id);
 src.courseId='grade1';
 for(const q of src.questions)if(q.diagram?.spec?.src){
  const rel=q.diagram.spec.src;
  if(!/^[a-z0-9/_-]+\.png$/i.test(rel)||rel.startsWith('/')||rel.includes('..'))fail('unsafe diagram '+rel);
  const target='question-banks/assets/grade1/'+rel;
  fs.mkdirSync(path.dirname(path.join(out,target)),{recursive:true});
  fs.copyFileSync(path.join(source,rel),path.join(out,target));
  q.diagram.spec.src=target;
 }
 const target='question-banks/grade1/'+unit.id+'.json';
 fs.mkdirSync(path.dirname(path.join(out,target)),{recursive:true});
 fs.writeFileSync(path.join(out,target),JSON.stringify(src));
 native.banks.push({courseId:'grade1',unitId:unit.id,path:target,approved:true,teacherUse:true});
}
fs.writeFileSync(manifestFile,JSON.stringify(native,null,2)+'\n');
console.log('Grade 1 assembled: 12 units from FinancialAlgebra, using existing Classroom generators and Grade 1 players.');


// Attach Classroom-owned content to this newly assembled course.
{const f=path.join(out,"grade1-main-catalog.js");fs.appendFileSync(f,"\nif(window.MK_CONTENT_UPDATES)window.MK_CONTENT_UPDATES.attach();\n");}
