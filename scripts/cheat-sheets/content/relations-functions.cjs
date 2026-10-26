/* The unit-pack cheat sheet (content in scripts/unit-packs/relations-functions.cjs), so `build.cjs all` rebuilds every cheat sheet in one style. */
const C = require('../../unit-packs/relations-functions.cjs');
module.exports = { name: C.prefix || C.unit, course: C.course, unitNo: C.unitNo, unitName: C.unitName, focus: C.cheat.focus, morefocus: C.cheat.morefocus, front: C.cheat.front, back: C.cheat.back };
