"""Read exact skill records through the site's own MK_COURSE_CATALOG.getSkillRecords."""
import json, os, subprocess
REPO = os.environ.get("PA8_REPO", "/home/claude/repo_src/classroom-main")
_cache = {}
JS = r"""
const fs=require('fs'),vm=require('vm'),path=require('path');const root=process.argv[1];
const ctx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(root,'data.js'),'utf8'),ctx);
vm.runInNewContext(fs.readFileSync(path.join(root,'course-catalog.js'),'utf8'),ctx);
const c=ctx.window.LIBRARY.courses.find(c=>c.id==='prealgebra');const out={};
for(const u of c.units)out[u.id]=ctx.window.MK_COURSE_CATALOG.getSkillRecords('prealgebra',u.id);
console.log(JSON.stringify(out));
"""


def records(course, unit):
    if not _cache:
        out = subprocess.run(["node", "-e", JS, REPO], capture_output=True, text=True, check=True).stdout
        _cache.update(json.loads(out))
    return _cache[unit]
