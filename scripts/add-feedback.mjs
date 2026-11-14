// Share the report dialog across built pages, including isolated student links.
// This modifies only the deployment artifact, never authored math resources.
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(process.env.SITE_DIR||'_site');let count=0;
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,e.name);if(e.isDirectory())walk(file);else if(/\.html?$/.test(e.name)){
 let html=fs.readFileSync(file,'utf8');if(!/<\/body>/i.test(html))continue;
 const src=path.relative(path.dirname(file),path.join(root,'feedback.js')).split(path.sep).join('/');
 html=html.replace(/<script[^>]+src=["'][^"']*feedback\.js[^"']*["'][^>]*><\/script>/gi,'');
 html=html.replace(/href="https:\/\/github\.com\/akneller1\/classroom\/issues\/new[^"<>]*"/g,'href="mailto:akneller@gmail.com" data-feedback-chooser');
 html=html.replace(/<\/body>/i,'<script src="'+src+'?v=audit-followup-20261114"></script>\n</body>');
 fs.writeFileSync(file,html);count++;
}}}walk(root);console.log('Shared feedback dialog: '+count+' pages');
