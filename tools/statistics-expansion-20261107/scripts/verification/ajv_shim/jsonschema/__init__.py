"""Minimal offline stand-in for `jsonschema.Draft202012Validator` used ONLY so that
validate-reference.py can run where the real package is unavailable. It delegates to
Ajv 6 through scripts/verification/ajv_validate.cjs. Prefer the real jsonschema package."""
import json, os, subprocess, tempfile
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ValidationError(Exception):
    pass

class Draft202012Validator:
    def __init__(self, schema):
        self.schema = schema
    def validate(self, instance):
        with tempfile.TemporaryDirectory() as d:
            s, i = os.path.join(d, 's.json'), os.path.join(d, 'i.json')
            with open(s, 'w') as f:
                json.dump(self.schema, f)
            with open(i, 'w') as f:
                json.dump(instance, f)
            r = subprocess.run(['node', os.path.join(HERE, 'ajv_validate.cjs'), s, i], capture_output=True, text=True)
            if r.returncode != 0:
                raise ValidationError(r.stdout + r.stderr)
