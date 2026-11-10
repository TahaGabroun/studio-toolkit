#!/usr/bin/env python3
"""Shared helpers for the animation skills. Standard library only (plus the toolkit Python Playwright and FFmpeg).

A builder fills a skill's template.html with its spec and renders it with deterministic Playwright capture:
    anim.build(template, defaults, duration=lambda spec: 4.0, three=False)

From the command line:
    python3 kit/anim.py sheet <video.mp4> <out.jpg> [n]     # contact sheet; the red frame is Instagram's safe area
    python3 kit/anim.py still <video.mp4> <t> <out.jpg>     # one frame
"""
import copy
import math
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(KIT.parents[2] / 'scripts'))
from animation_render import capture
W, H, FPS = 1080, 1920, 30
SAFE_TOP, SAFE_BOTTOM, SAFE_SIDE = 220, 1500, 100      # Instagram covers the top ~220 px and the bottom ~420 px


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def duration(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(video)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def link(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy(src, dst)


def check_setup(three):
    missing = []
    if not (KIT / 'node_modules' / 'gsap' / 'dist' / 'gsap.min.js').exists():
        missing.append('GSAP')
    if three and not (KIT / 'node_modules' / 'three' / 'build' / 'three.module.js').exists():
        missing.append('three.js')
    if missing:
        sys.exit(f'{" and ".join(missing)} not found: run  bash "{KIT}/setup.sh"  once, then build again')


def load_spec(path, defaults):
    spec = json.loads(Path(path).read_text())
    if not isinstance(spec, dict): raise ValueError('Spec must be a JSON object')
    for k, v in defaults.items():
        spec.setdefault(k, copy.deepcopy(v))
    unknown = sorted(set(spec) - set(defaults) - {'out', 'hold', 'template', 'language', 'direction'})
    if unknown:
        raise ValueError(f'Unknown spec fields: {", ".join(unknown)}')
    return spec


def validate_spec(kind, spec):
    def number(value, minimum=0):
        return not isinstance(value, bool) and isinstance(value, (int,float)) and math.isfinite(value) and value >= minimum
    def strings(items): return isinstance(items,list) and all(isinstance(x,str) for x in items)
    for key in ['out','template','label','prefix','suffix','destination','title','subtitle','time','date']:
        if key in spec and spec[key] is not None and not isinstance(spec[key],str): raise ValueError(f'{key} must be text')
    for key in ['dark','light']:
        if key in spec and not isinstance(spec[key],bool): raise ValueError(f'{key} must be boolean')
    if spec.get('language','en') not in ['en','ar'] or spec.get('direction','auto') not in ['ltr','rtl','auto']: raise ValueError('language/direction must be en|ar and ltr|rtl|auto')
    if kind == 'graph':
        values = spec['values']
        if not isinstance(values,list) or not 2 <= len(values) <= 1000 or not all(number(x) for x in values) or max(values) <= 0: raise ValueError('values needs 2–1000 finite nonnegative numbers, at least one positive')
        if not strings(spec['labels']) or spec['labels'] and len(spec['labels']) != len(values): raise ValueError('labels must match values one-to-one')
        if spec['final'] is not None and (not number(spec['final']) or values[-1] == 0 and spec['final'] != 0): raise ValueError('final must be nonnegative; a zero last value cannot scale to a nonzero total')
        if type(spec['decimals']) is not int or not 0 <= spec['decimals'] <= 6: raise ValueError('decimals must be 0–6')
    elif kind == 'minimalistic-graphics':
        if type(spec['steps']) is not int or not 3 <= spec['steps'] <= 7: raise ValueError('steps must be 3–7')
        if not strings(spec['lines']) or not 1 <= len(spec['lines']) <= 2: raise ValueError('lines must contain one or two strings')
    elif kind == 'map-route':
        if not spec['destination'] or not number(spec['minutes'],.001) or not number(spec['distance']): raise ValueError('destination and finite positive minutes/nonnegative distance required')
        if spec['unit'] not in ['km','mi'] or type(spec['seed']) is not int: raise ValueError('unit must be km|mi; seed must be an integer')
        if not strings(spec['places']) or len(spec['places']) > 5: raise ValueError('places takes up to five text labels')
    elif kind == 'breakdown':
        if not isinstance(spec['labels'],list) or len(spec['labels']) != 6 or not all(strings(x) and 1 <= len(x) <= 2 for x in spec['labels']): raise ValueError('labels needs six [name,note] lists')
    if 'accent' in spec and (not isinstance(spec['accent'],str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',spec['accent'])): raise ValueError('accent must be a six-digit hex color')


def prepare(template, spec, dur, work, three=False):
    """writes the render folder: index.html with the spec filled in, fonts, GSAP and (if needed) three.js"""
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    html = Path(template).read_text()
    data = json.dumps(spec, ensure_ascii=False, allow_nan=False).replace('</', '<\\/')
    html = html.replace('lang="en"',f'lang="{spec.get("language","en")}" dir="{spec.get("direction","auto")}"')
    (work / 'index.html').write_text(html.replace('__SPEC__', data).replace('__DURATION__', f'{dur:.3f}'))
    for f in (KIT / 'fonts').glob('*.woff2'):
        link(f, work / 'fonts' / f.name)
    for f in (KIT / 'fonts').glob('*.ttf'):
        link(f, work / 'fonts' / f.name)
    link(KIT / 'node_modules/gsap/dist/gsap.min.js', work / 'vendor/gsap.min.js')
    if three:
        t = KIT / 'node_modules' / 'three'
        link(t / 'build' / 'three.module.js', work / 'vendor' / 'three' / 'three.module.js')
        for rel in ['environments/RoomEnvironment.js']:
            link(t / 'examples' / 'jsm' / rel, work / 'vendor' / 'three' / 'addons' / rel)


def render(work, out):
    dur = float(__import__('re').search(r'data-duration="([0-9.]+)"', (work/'index.html').read_text()).group(1))
    result = capture(work, 'quick', out, duration=dur, replace='--replace' in sys.argv)
    print(json.dumps(result, indent=2))


def snapshots(work, times, out_dir):
    print(json.dumps(capture(work, 'quick', out_dir, times=times, replace='--replace' in sys.argv), indent=2))


def sheet(video, out, n=6):
    """contact sheet of a finished video; the red frame is the part Instagram leaves uncovered"""
    tw, th = 270, 480
    k = tw / W
    draw = (f'drawbox=x={SAFE_SIDE * k:.0f}:y={SAFE_TOP * k:.0f}:w={(W - 2 * SAFE_SIDE) * k:.0f}:'
            f'h={(SAFE_BOTTOM - SAFE_TOP) * k:.0f}:color=red@0.8:t=2')
    rate = n / duration(video)
    run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vf', f'fps={rate:.5f},scale={tw}:{th},{draw},tile={n}x1',
         '-frames:v', '1', out])


def still(video, t, out):
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', out])


def build(template, defaults, duration=lambda spec: 4.0, three=False, check=None):
    """the whole builder CLI:  build.py <spec.json> [--snap 1.5,3.2]  ->  <spec>.mp4 + <spec>.sheet.jpg"""
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        sys.exit(f'usage: {Path(sys.argv[0]).name} <spec.json> [--snap 1.5,3.2]')
    spec_path = Path(args[0]).resolve()
    snap = None
    if '--snap' in args:
        snap = [float(x) for x in args[args.index('--snap') + 1].split(',')]
    check_setup(three)
    spec = load_spec(spec_path, defaults)
    validate_spec(Path(template).parent.name, spec)
    if check:
        check(spec)
    hold = spec.get('hold', 0)
    if isinstance(hold, bool) or not isinstance(hold, (int,float)) or not math.isfinite(hold) or not 0 <= hold <= 60: raise ValueError('hold must be between 0 and 60 seconds')
    dur = duration(spec) + hold
    out = Path(spec['out']) if spec.get('out') else spec_path.with_suffix('.mp4')
    if not out.is_absolute():
        out = spec_path.parent / out
    if spec.get('template'):                      # a customised copy of the skill's template, next to the spec
        template = (spec_path.parent / spec['template']).resolve()
    work = spec_path.parent / '.work' / out.stem
    if not snap and out.exists():
        if '--replace' not in args: raise ValueError('Output exists; use another path or --replace')
        # The renderer replaces only after encoding and media checks succeed.
    prepare(template, spec, dur, work, three)
    if snap:
        snapshots(work, snap, out.with_suffix('.snaps'))
        return
    render(work, out)
    sh = out.with_suffix('.sheet.jpg')
    sheet(out, sh)
    print(f'done: {out}\nsheet: {sh}')


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == 'sheet':
        sheet(a[1], a[2], int(a[3]) if len(a) > 3 else 6)
        print('wrote', a[2])
    elif len(a) == 4 and a[0] == 'still':
        still(a[1], float(a[2]), a[3])
        print('wrote', a[3])
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
