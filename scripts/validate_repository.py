#!/usr/bin/env python3
"""Validate actual YAML metadata, links, schemas, source syntax and license snapshots."""
import ast
import json
import re
import sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]

def check(root=ROOT):
    errors=[];manifest=json.loads((root/'manifest.json').read_text());expected={x['id'] for x in manifest['skills']};found=set()
    for f in (root/'skills').glob('*/SKILL.md'):
        try:
            t=f.read_text();head=t.split('---',2)[1];meta=yaml.safe_load(head)
            if meta['name']!=f.parent.name or not re.fullmatch('[a-z0-9-]{1,64}',meta['name']):errors.append(f'Invalid skill name: {f}')
            if not isinstance(meta['description'],str) or not meta['description'].strip():errors.append(f'Missing description: {f}')
            found.add(meta['name'])
            ui=yaml.safe_load((f.parent/'agents/openai.yaml').read_text())
            if '$'+meta['name'] not in ui['interface']['default_prompt']:errors.append(f'Invocation mismatch: {f}')
        except (OSError,ValueError,KeyError,TypeError,yaml.YAMLError) as e:errors.append(f'{f}: {e}')
    if found!=expected:errors.append(f'Skill inventory mismatch {found ^ expected}')
    for f in root.rglob('*.md'):
        if any(x in f.parts for x in ['.venv','.git','node_modules']):continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',f.read_text()):
            if re.match(r'^(https?:|mailto:|#)',target):continue
            path=target.split('#')[0].replace('%20',' ')
            if not (f.parent/path).exists():errors.append(f'Broken link: {f.relative_to(root)} -> {target}')
    for f in root.rglob('*.py'):
        if any(x in f.parts for x in ['.venv','.git','node_modules']):continue
        try:ast.parse(f.read_text(),filename=str(f))
        except SyntaxError as e:errors.append(str(e))
    for f in (root/'schemas').glob('*.json'):
        try:
            data=json.loads(f.read_text());Draft202012Validator.check_schema(data)
            if data!=json.loads((root/'skills/studio-toolkit/references/schemas'/f.name).read_text()):errors.append(f'Schema distribution drift: {f.name}')
        except Exception as e:errors.append(f'Schema {f}: {e}')
    for source in json.loads((root/'upstreams.lock.json').read_text()):
        if 'MIT License' not in (root/source['license_file']).read_text():errors.append('Missing MIT notice')
    return errors
if __name__=='__main__':
    errors=check()
    for e in errors:print('ERROR:',e)
    print(f'Repository validation: {"FAIL" if errors else "PASS"}; {len(errors)} errors')
    raise SystemExit(bool(errors))
