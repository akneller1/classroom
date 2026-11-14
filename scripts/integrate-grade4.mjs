import { addMultipleDrop } from './multiple-drop-resources.mjs';
// Assemble the validated Grade 4 course from the separate FinancialAlgebra repository.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const source=path.resolve(process.env.GRADE4_SOURCE_DIR||'_course_sources/grade4');
const out=path.resolve('_site');
const modulePath=path.join(source,'tools/grade4-authoring/staging/assemble-grade4.mjs');
if(!fs.existsSync(modulePath))throw Error('Missing approved Grade 4 assembler');
const {grade4Ready,assembleGrade4}=await import(pathToFileURL(modulePath).href);
if(!grade4Ready(source))throw Error('Grade 4 banks are not approved');
const course=assembleGrade4({source,out});
if(course.units.length!==10)throw Error('Grade 4 release requires ten units');
addMultipleDrop(course);
const skills=course.skills;
const bridge='(function(G){var course='+JSON.stringify(course)+',skills='+JSON.stringify(skills)+';'+
'var L=G.LIBRARY;if(!L||!L.courses)throw Error("Grade 4 library missing");'+
'L.courses=L.courses.filter(function(c){return c.id!=="grade4"});L.courses.push(course);'+
'var C=G.MK_COURSE_CATALOG,old=C.getSkills,records=C.getSkillRecords;'+
'C.getSkills=function(c,u){return c==="grade4"&&skills[u]?skills[u].slice():old(c,u)};'+
'C.getSkillRecords=function(c,u){return c==="grade4"&&skills[u]?skills[u].map(function(n,i){return {id:u+"-skill-"+String(i+1).padStart(2,"0"),name:n,index:i+1}}):records(c,u)};'+
'})(window);\n';
fs.writeFileSync(path.join(out,'grade4-main-catalog.js'),bridge);
const index=path.join(out,'index.html');
let html=fs.readFileSync(index,'utf8');
const anchor='<script src="app.js';
if(!html.includes(anchor))throw Error('Grade 4 release: app.js script anchor missing');
html=html.replace(anchor,'<script src="grade4-main-catalog.js?v=grade4-release-20261113"></script>\n'+anchor);
fs.writeFileSync(index,html);
const appFile=path.join(out,'app.js');let app=fs.readFileSync(appFile,'utf8');
// Use the same compact unit view, thumbnails and direct resource routes as Grade 5.
app=app.replace("/^\\/grade5\\//.test(path)","/^\\/grade[45]\\//.test(path) || /^grade4\\//.test(path)");
app=app.replace("['grade5','financial-algebra'].includes(it.c.id)","['grade4','grade5','financial-algebra'].includes(it.c.id)");
app=app.replace("c.id === 'grade5') return algebraUnitView(c, u)","['grade4','grade5'].includes(c.id)) return algebraUnitView(c, u)");
app=app.replace("'grade5', 'financial-algebra'].indexOf(c.id)","'grade4', 'grade5', 'financial-algebra'].indexOf(c.id)");
// The homepage's legacy Coming Soon placeholders must not duplicate published courses.
const placeholder="SOON = SOON.concat([";
if(!app.includes(placeholder))throw Error('Grade 4 homepage placeholder anchor missing');
app=app.replace("var courses = L.courses.concat(SOON).slice().sort(function (a, b) {","var courses = L.courses.concat(SOON.filter(function(c){return !L.courses.some(function(p){return p.id===c.id;});})).slice().sort(function (a, b) {");
if(!app.includes('SOON.filter(function(c){return !L.courses.some(function(p){return p.id===c.id;});})'))throw Error('Published course deduplication missing');
for(const required of ["/^grade4\\//.test(path)","['grade4','grade5'].includes(c.id)) return algebraUnitView(c, u)"])if(!app.includes(required))throw Error('Grade 4 parity patch missing: '+required);
fs.writeFileSync(appFile,app);
for(const page of fs.readdirSync(path.join(out,'worksheet-generator')).filter(name=>name.endsWith('.html')&&fs.readFileSync(path.join(out,'worksheet-generator',name),'utf8').includes('../course-catalog.js'))){
 const f=path.join(out,'worksheet-generator',page);if(!fs.existsSync(f))continue;
 let h=fs.readFileSync(f,'utf8');
 const match=h.match(/<script src="\.\.\/course-catalog\.js[^"]*"><\/script>/);
 if(!match)throw Error('Grade 4 release: catalog anchor missing '+page);
 h=h.replace(match[0],match[0]+'\n<script src="../grade4-main-catalog.js?v=grade4-release-20261113"></script>');
 fs.writeFileSync(f,h);
}
const manifestFile=path.join(out,'question-banks/manifest.json');
const manifest=JSON.parse(fs.readFileSync(manifestFile,'utf8'));
manifest.banks=manifest.banks.filter(x=>x.courseId!=='grade4');
for(const unit of course.units){
 const src=JSON.parse(fs.readFileSync(path.join(source,'question-banks/math4',unit.id+'.json'),'utf8'));
 src.courseId='grade4';
 for(const q of src.questions)if(q.diagram?.spec?.src){
  const rel=q.diagram.spec.src;
  if(rel.startsWith('/')||rel.includes('..'))throw Error('Unsafe Grade 4 diagram '+rel);
  const target='question-banks/assets/grade4/'+rel;
  fs.mkdirSync(path.dirname(path.join(out,target)),{recursive:true});
  fs.copyFileSync(path.join(source,rel),path.join(out,target));q.diagram.spec.src=target;
 }
 const target='question-banks/grade4/'+unit.id+'.json';
 fs.mkdirSync(path.dirname(path.join(out,target)),{recursive:true});
 fs.writeFileSync(path.join(out,target),JSON.stringify(src));
 manifest.banks.push({courseId:'grade4',unitId:unit.id,path:target,approved:true,teacherUse:true});
}
fs.writeFileSync(manifestFile,JSON.stringify(manifest,null,2)+'\n');
console.log('Grade 4 release assembled: '+course.units.length+' units from separate source repository.');

