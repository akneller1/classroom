// Run after content overlays: their historical version tags must not retain stale generator code.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const out=path.resolve(process.argv[2]||'_site');
const targets=new Set([
 'worksheet-generator/core/math-display.js',
 'worksheet-generator/core/render.js',
 'worksheet-generator/plot-practice.js',
 'worksheet-generator/menu/app.js','worksheet-generator/menu/engine.js',
 'worksheet-generator/menu/render.js','worksheet-generator/menu/verify.js',
 'worksheet-generator/menu/skills/algebra1-expressions-equations.js',
 'worksheet-generator/menu/skills/geometry-right-triangles-trigonometry.js',
 'worksheet-generator/menu/skills/geometry-transformations.js'
].map(p=>path.join(out,p)));
const hashes=new Map();
for(const file of targets)if(fs.existsSync(file))hashes.set(file,crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex').slice(0,16));
let count=0;
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){
 const file=path.join(dir,e.name);
 if(e.isDirectory()){if(!['vendor','node_modules'].includes(e.name))walk(file);continue;}
 if(!e.name.endsWith('.html'))continue;
 const html=fs.readFileSync(file,'utf8');
 const updated=html.replace(/(<script\b[^>]*\bsrc=["'])([^"']+)(["'])/gi,(all,lead,src,quote)=>{
  if(/^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(src))return all;
  const [url]=src.split(/[?#]/),target=url.startsWith('/')?path.join(out,url):path.resolve(path.dirname(file),url);
  const hash=hashes.get(target);if(!hash)return all;
  count++;return lead+url+'?v='+hash+quote;
 });
 if(updated!==html)fs.writeFileSync(file,updated);
}}
walk(out);
console.log('Versioned '+count+' generator script references from final asset contents.');
