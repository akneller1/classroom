// Assemble approved Financial Algebra from its separate development repository.
// Only the generated Pages artifact changes; no course source files are copied into Classroom Git.
import fs from 'node:fs';
import path from 'node:path';

const source=path.resolve(process.env.FINANCIAL_ALGEBRA_SOURCE_DIR||'_course_sources/grade5');
const output=path.resolve('_site');
const dest=path.join(output,'financial-algebra');
const assert=(condition,message)=>{if(!condition)throw Error(message);};
assert(fs.existsSync(path.join(output,'index.html')),'Build Classroom site before course assembly');
assert(fs.existsSync(path.join(source,'financial/resources.json')),'Financial Algebra source checkout missing');
const manifest=JSON.parse(fs.readFileSync(path.join(source,'financial/resources.json'),'utf8'));
assert(manifest.courseId==='financial-algebra'&&manifest.units.length===10,'Financial Algebra release manifest must have exactly ten units');
assert(manifest.units.every(u=>u.resources&&Array.isArray(u.resources.games)&&u.resources.games.length),'Missing approved unit games/resources');
function copyDir(from,to){
 assert(fs.existsSync(from),'Missing approved source directory: '+from);
 fs.mkdirSync(to,{recursive:true});
 for(const item of fs.readdirSync(from,{withFileTypes:true})){
  if(['.git','node_modules','__pycache__','.DS_Store'].includes(item.name))continue;
  const a=path.join(from,item.name),b=path.join(to,item.name);
  if(item.isDirectory())copyDir(a,b);
  else if(item.isFile()&&!/\.(?:md|py|pyc)$/i.test(item.name))fs.copyFileSync(a,b);
 }
}
fs.rmSync(dest,{recursive:true,force:true});fs.mkdirSync(dest,{recursive:true});
// Copy only Financial Algebra production resources, not unapproved elementary courses.
copyDir(path.join(source,'financial'),path.join(dest,'financial'));
copyDir(path.join(source,'question-banks','financial-algebra'),path.join(dest,'question-banks','financial-algebra'));
copyDir(path.join(source,'thumbs','financial-algebra'),path.join(dest,'thumbs','financial-algebra'));
const artifacts=path.join(source,'artifacts');
const artifactDest=path.join(dest,'artifacts');
fs.mkdirSync(artifactDest,{recursive:true});
for(const item of fs.readdirSync(artifacts,{withFileTypes:true})){
 if(item.isDirectory()&&item.name.startsWith('financial-algebra-'))copyDir(path.join(artifacts,item.name),path.join(artifactDest,item.name));
}
for(const file of ['styles.css','site-overrides.css'])if(fs.existsSync(path.join(source,file)))fs.copyFileSync(path.join(source,file),path.join(dest,file));
// Financial Algebra course shell is already designed for Classroom navigation.
let html=fs.readFileSync(path.join(output,'financial-algebra.html'),'utf8');
html=html.replace(/href="index\.html"/g,'href="../index.html"')
 .replace(/href="financial-algebra\.html"/g,'href="./"');
fs.writeFileSync(path.join(dest,'index.html'),html);
// Compile course routing module from CURRENT development source, not a stale Classroom copy.
fs.copyFileSync(path.join(source,'src','site.js'),path.join(dest,'financial','classroom-site.mjs'));
fs.copyFileSync(path.join(source,'src','course.js'),path.join(dest,'financial','course.js'));
// Course-page CSS remains the same Classroom style sheet already used by the production shell.
fs.copyFileSync(path.join(output,'financial','course-site.css'),path.join(dest,'financial','course-site.css'));
const required=['index.html','financial/classroom-site.mjs','financial/course.js','financial/resources.json','financial/games/index.html','financial/generators/index.html','financial/practice/index.html','financial/flashcards/index.html','financial/decision-lab/index.html','financial/banks/income.json','question-banks/financial-algebra/income.json'];
for(const file of required)assert(fs.existsSync(path.join(dest,file)),'Missing Financial Algebra production file: '+file);
// Check every published resource target against the actual assembled artifact.
const toLocal=(url)=>String(url).split(/[?#]/)[0].replace(/^\/+/, '');
let checked=0;
for(const unit of manifest.units){
 const r=unit.resources;
 const paths=[r.lessonPlan,r.worksheet,r.assessment,r.practiceTest,r.flashcards,r.cheatSheet,r.decisionLab?.path,r.decisionLab?.teacherPath,...r.projects.map(p=>p.path),...r.games.map(g=>g.path)];
 for(const p of paths){
  assert(typeof p==='string'&&p.length,'Missing resource path for '+unit.unitId);
  const local=toLocal(p);
  assert(fs.existsSync(path.join(dest,local)),'Broken Financial Algebra resource: '+p);
  checked++;
 }
}
const sitemap=path.join(output,'sitemap.xml');let xml=fs.readFileSync(sitemap,'utf8');
if(!xml.includes('https://mrksclassroom.com/financial-algebra/'))xml=xml.replace('</urlset>','  <url><loc>https://mrksclassroom.com/financial-algebra/</loc></url>\n</urlset>');
fs.writeFileSync(sitemap,xml);
console.log('Financial Algebra approved: '+manifest.units.length+' units, '+checked+' resource targets. Built _site/financial-algebra/ from separate repository.');
