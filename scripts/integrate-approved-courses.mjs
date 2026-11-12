// Assemble the approved Grade 5 source into the public Classroom artifact.
// Source files stay in FinancialAlgebra; only the assembled _site/site directory changes.
// This is the ONLY Grade 5 assembler used by either public workflow.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const stage=path.resolve(process.env.GRADE5_SOURCE_DIR||'../FinancialAlgebra');
const out=path.resolve(process.env.GRADE5_OUTPUT_DIR||'_site');
const dst=path.join(out,'grade5');
function required(file){if(!fs.existsSync(file))throw Error('Missing approved Grade 5 source '+file);return file;}
if(!fs.existsSync(path.join(out,'index.html')))throw Error('Build main Classroom site before integrating Grade 5');
required(path.join(stage,'grade5.html'));
fs.rmSync(dst,{recursive:true,force:true});
fs.mkdirSync(dst,{recursive:true});
const copied=new Set();
function copyFile(rel){
 if(copied.has(rel))return;
 const from=required(path.join(stage,rel)),to=path.join(dst,rel);
 if(!from.startsWith(stage+path.sep)||!to.startsWith(dst+path.sep))throw Error('Grade 5 copy escapes approved folders: '+rel);
 fs.mkdirSync(path.dirname(to),{recursive:true});
 fs.copyFileSync(from,to);
 copied.add(rel);
}
function copyDir(rel){
 const source=required(path.join(stage,rel)),target=path.join(dst,rel);
 fs.mkdirSync(target,{recursive:true});
 for(const item of fs.readdirSync(source,{withFileTypes:true})){
  if(item.name==='.git'||item.name==='node_modules'||item.name==='__pycache__'||item.name==='.DS_Store')continue;
  const sub=path.posix.join(rel,item.name);
  if(item.isDirectory())copyDir(sub);
  else if(item.isFile()&&!/\.(?:md|py|pyc|zip)$/i.test(item.name))copyFile(sub);
 }
}
// Only the released Grade 5 page, data, tools and runtime are permitted here.
for(const f of ['grade5.html','grade5-resources.html','data.js','course-catalog.js',
 'grade5-resource-catalog.js','question-bank-adapter.js','question-bank-loader.js',
 'manifest.json','styles.css','site-overrides.css','assets/favicon.svg',
 'assets/course-icons/grade5.svg','course-outlines/grade5.json',
 'worksheet-generator/core/math-display.js','worksheet-generator/core/math-display.css',
 'worksheet-generator/games/skill-setup.js'])copyFile(f);
for(const f of fs.readdirSync(path.join(stage,'src')).filter(x=>/^grade5-.*\.js$/.test(x)))copyFile('src/'+f);
for(const f of fs.readdirSync(path.join(stage,'worksheet-generator')).filter(x=>/^grade5-.*\.html$/.test(x)))copyFile('worksheet-generator/'+f);
copyDir('worksheet-generator/grade5');
copyDir('math5');
if(fs.existsSync(path.join(stage,'assets/fonts')))copyDir('assets/fonts');
// Read the source data/catalog and keep the released math5 course only.
const context={window:{}};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(stage,'data.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(stage,'course-catalog.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(stage,'grade5-resource-catalog.js'),'utf8'),context);
const library=context.window.LIBRARY,course=library?.courses.find(c=>c.id==='math5');
const resources=context.window.MK_GRADE5_RESOURCES?.course;
if(!course||!resources||course.units.length!==11||resources.units.length!==11)throw Error('Expected eleven approved Grade 5 units');
library.courses=[course];
fs.writeFileSync(path.join(dst,'data.js'),'window.LIBRARY = '+JSON.stringify(library)+';\n');
// Only package activities actually linked by the approved Grade 5 resource catalog.
for(const unit of resources.units){
 for(const item of unit.artifacts){
  if(item.thumb&&item.thumb.startsWith('thumbs/math5-'))copyFile(item.thumb);
  if(/^math5-[a-z0-9-]+\//.test(item.path||'')){
   const dir=item.path.split('/')[0];
   if(!fs.existsSync(path.join(dst,dir)))copyDir(dir);
  }
 }
}
// Publish only approved Grade 5 manifest entries (no unpublished staging courses).
const manifest=JSON.parse(fs.readFileSync(path.join(stage,'manifest.json'),'utf8'));
const banks=manifest.banks.filter(b=>b.courseId==='math5'&&b.approved===true);
if(banks.length!==11)throw Error('Expected eleven approved Grade 5 bank entries');
fs.writeFileSync(path.join(dst,'manifest.json'),JSON.stringify({version:1,banks},null,2)+'\n');
// All diagrams are loaded from their exact path relative to Grade 5's root.
// In particular, 500+ volume/fraction diagrams have flat .png filenames.
let diagrams=0;
for(const entry of banks){
 const bank=JSON.parse(fs.readFileSync(required(path.join(stage,entry.path)),'utf8'));
 for(const question of bank.questions){
  const src=question.diagram?.spec?.src;
  if(!src)continue;
  if(!/^[a-z0-9/_-]+\.png$/i.test(src)||src.startsWith('/')||src.includes('..'))throw Error('Unsafe Grade 5 diagram path '+src);
  copyFile(src);
  diagrams++;
 }
}
// The source class is renamed to index.html so relative resource URLs remain valid.
let html=fs.readFileSync(path.join(dst,'grade5.html'),'utf8');
html=html.replace(/<title>[^<]*<\/title>/,"<title>5th Grade Math | Mr. K's Classroom</title>")
 .replace(/href="index\.html">Financial Algebra<\/a>/g,'href="../index.html">All courses</a>')
 .replace(/href="https:\/\/mrksclassroom\.com\/" target="_blank" rel="noopener">Main Classroom ↗<\/a>/g,'')
 .replace(/<a href="grade[1-4]\.html"[\s\S]*?<\/a>/g,'')
 .replace(/<span class="course-wip-label">[\s\S]*?<\/span>/g,'')
 .replace(/Grade 5 resources are being developed and tested here before transfer to the main Classroom site\. The original curriculum outline is preserved within the course page\./g,
 'Grade 5 mathematics: games, generators, printable resources, and understanding checks.')
 .replace(/href="grade5\.html"/g,'href="index.html"');
fs.writeFileSync(path.join(dst,'index.html'),html);
const alias='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow">'+
 "<title>Grade 5 | Mr. K's Classroom</title>"+
 '<meta http-equiv="refresh" content="0;url=./index.html">'+
 "<script>location.replace('./index.html'+location.search+location.hash);</script>"+
 '</head><body><a href="./index.html">5th Grade Math</a></body></html>\n';
fs.writeFileSync(path.join(dst,'grade5.html'),alias);
const siteJs=path.join(dst,'src','grade5-site.js');
if(fs.existsSync(siteJs)){
 const js=fs.readFileSync(siteJs,'utf8').replace(/\['Home','index\.html'\]/g,"['Home','../index.html']");
 fs.writeFileSync(siteJs,js);
}
const sitemap=path.join(out,'sitemap.xml');
if(fs.existsSync(sitemap)){
 let xml=fs.readFileSync(sitemap,'utf8');
 if(!xml.includes('https://mrksclassroom.com/grade5/'))xml=xml.replace('</urlset>','  <url><loc>https://mrksclassroom.com/grade5/</loc></url>\n</urlset>');
 fs.writeFileSync(sitemap,xml);
}
console.log('Grade 5 assembled: 11 approved units, '+diagrams+' question diagrams, '+copied.size+' released source files; no other staging pages.');
