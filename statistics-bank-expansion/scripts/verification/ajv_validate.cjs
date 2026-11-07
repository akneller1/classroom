/* Offline JSON Schema check with Ajv 6 (draft-07 engine). The 2020-12 "$schema" tag is
   removed; every keyword this schema uses (type, enum, const, pattern, required,
   additionalProperties, minItems, minLength, items, allOf, if/then) exists in draft-07. */
'use strict';
const fs = require('fs');
const Ajv = require(process.env.AJV_PATH || '/opt/npm-tools/node_modules/ajv');
const schema = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); delete schema.$schema;
const ajv = new Ajv({ allErrors: true });
const validate = ajv.compile(schema);
let bad = 0;
for (const f of process.argv.slice(3)) {
  const ok = validate(JSON.parse(fs.readFileSync(f, 'utf8')));
  console.log((ok ? 'PASS ' : 'FAIL ') + f);
  if (!ok) { bad++; console.log(JSON.stringify(validate.errors.slice(0, 10), null, 1)); }
}
process.exit(bad ? 1 : 0);
