#!/usr/bin/env python3
"""Build six adopted animation workflows and import measured narration for cartoon engines."""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from animation_render import capture

SKILL = Path(__file__).resolve().parents[1]
RUNTIME = SKILL / 'references/animation-runtime'
QUICK = {'animated-graph': 'graph', 'minimalistic-graphics': 'minimalistic-graphics', 'map-route': 'map-route', 'exploded-view': 'breakdown'}
ENGINES = {'stick-figure': 'stick-figure', 'cartoon-animation': 'zach-d-films'}


def read(path):
    def reject(value): raise ValueError('Nonfinite JSON value: ' + value)
    return json.loads(Path(path).read_text(), parse_constant=reject)


def write(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def init(kind, root, example=False):
    root = Path(root).resolve()
    if root.exists(): raise ValueError('Animation project must be a new directory; existing work is preserved')
    if kind not in ENGINES: raise ValueError('init supports stick-figure or cartoon-animation; quick skills consume JSON specs')
    source = RUNTIME / 'skills' / ENGINES[kind] / 'engine'
    shutil.copytree(source / 'template' if kind == 'stick-figure' else source, root)
    if kind == 'cartoon-animation':
        (root / 'node_modules').symlink_to(RUNTIME / 'kit/node_modules', target_is_directory=True)
    if not example:
        # An original visual calibration, not inherited scientific claims or synthesized speech.
        write(root / 'script.json', [])
        if kind == 'stick-figure':
            (root / 'web/words.js').write_text('window.WORDS = [];\n')
            (root / 'web/warp.js').write_text('window.WARP = null;\n')
            (root / 'web/shots.js').write_text((RUNTIME / 'starters/stick-shots.js').read_text())
            for name in ['words_ref.json', 'warp.json']: (root / 'audio' / name).unlink(missing_ok=True)
        else:
            (root / 'src/shots.js').write_text((RUNTIME / 'starters/cartoon-shots.js').read_text())
            (root / 'src/caption-data.js').write_text('export const CAPTIONS = [];\n')
    write(root / 'animation-project.json', {'schema_version': 1, 'engine': kind, 'fps': 30, 'output_width': 1080, 'output_height': 1920, 'example': example, 'narration': 'not supplied; use ElevenLabs or an approved recording', 'review': 'draft'})
    return {'project': str(root), 'engine': kind, 'example': example}


def measured_words(value):
    items = value.get('segments') if isinstance(value, dict) else value
    if not isinstance(items, list) or not items: raise ValueError('Nonempty measured word cues required')
    words = []; previous = 0
    for item in items:
        if not isinstance(item, dict): raise ValueError('Invalid word cue')
        text = item.get('text', item.get('w'))
        start = item.get('start_s', item.get('s')); end = item.get('end_s', item.get('e'))
        if not isinstance(text, str) or not text.strip() or len(text.split()) != 1: raise ValueError('Each cue must contain exactly one measured word')
        if any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) for t in [start, end]): raise ValueError('Word timestamps must be finite numbers')
        if start < previous or end <= start: raise ValueError('Word cues overlap, are out of order or have no duration')
        words.append({'w': text, 's': start, 'e': end, 'line': item.get('line', 0)})
        previous = end
    return words


def warp(reference, words, old_end, new_end):
    if [w['w'] for w in reference] != [w['w'] for w in words]: raise ValueError('Reference words differ; retime shots for the revised script')
    if old_end < reference[-1]['e'] or new_end < words[-1]['e']: raise ValueError('Warp endpoints precede speech')
    anchors = [[a['s'], b['s']] for a, b in zip(reference, words)]
    if anchors[0] != [0, 0] and anchors[0][0] > 0 and anchors[0][1] > 0: anchors.insert(0, [0, 0])
    if anchors[-1][0] < old_end and anchors[-1][1] < new_end: anchors.append([old_end, new_end])
    if any(b[0] <= a[0] or b[1] <= a[1] for a, b in zip(anchors, anchors[1:])): raise ValueError('Warp anchors must increase in both takes')
    return {'anchors': anchors, 'old_end': old_end, 'new_end': new_end}


def sync(root, words_path, audio, method, reference=None, replace=False):
    root = Path(root).resolve(); config = read(root / 'animation-project.json')
    value = read(words_path)
    if isinstance(value, dict) and value.get('method') and value['method'] != method: raise ValueError('Cue method differs from declared provenance')
    words = measured_words(value)
    script = read(root / 'script.json')
    if script and [w['w'] for w in words] != ' '.join(script).split(): raise ValueError('Measured words differ from script.json; review the spoken take before importing')
    # Decode without trimming silence, speeding speech or shifting provider cues.
    with tempfile.TemporaryDirectory(prefix='studio-voice-') as temporary:
        wav = Path(temporary) / 'vo.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(Path(audio).resolve()), '-ac', '1', '-ar', '44100', str(wav)], check=True)
        info = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-of', 'json', str(wav)], check=True, capture_output=True, text=True).stdout)
        duration = float(info['format']['duration'])
        if words[-1]['e'] > duration + .001: raise ValueError('Word cues exceed decoded narration duration')
        files = {'audio/vo.wav': wav.read_bytes(), 'audio/words_new.json': (json.dumps(words, ensure_ascii=False) + '\n').encode()}
    if reference:
        old_value = read(reference); old = measured_words(old_value)
        old_end = old_value.get('duration_seconds', old[-1]['e']) if isinstance(old_value, dict) else old[-1]['e']
        timing = warp(old, words, old_end, duration)
    else: timing = None
    if config['engine'] == 'stick-figure':
        files['web/words.js'] = ('window.WORDS = ' + json.dumps(words, ensure_ascii=False) + ';\n').encode()
        files['web/warp.js'] = ('window.WARP = ' + json.dumps(timing) + ';\n').encode()
    else:
        if reference: raise ValueError('Automatic take warping is a stick-figure feature; retime 3D shots explicitly')
        # Reuse the original caption grouping while serializing JS safely and retaining end times.
        spec = importlib.util.spec_from_file_location('cartoon_captions', RUNTIME / 'skills/zach-d-films/engine/captions.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        captions = [[group[0]['s'], ' '.join(x['w'] for x in group), group[-1]['e']] for group in module.chunks(words)]
        files['src/caption-data.js'] = ('export const CAPTIONS = ' + json.dumps(captions, ensure_ascii=False) + ';\n').encode()
    metadata = {'method': method, 'duration_seconds': duration, 'audio_sha256': hashlib.sha256(files['audio/vo.wav']).hexdigest(), 'word_count': len(words), 'review': 'reviewed timestamps' if method == 'manual-reviewed' else 'pending listening and pronunciation review', 'warped': bool(reference)}
    files['timing.json'] = (json.dumps(metadata, indent=2) + '\n').encode()
    # A generated starter has empty caption files, which may be replaced on its first cue import.
    protected = ['audio/vo.wav', 'audio/words_new.json', 'timing.json']
    if not replace and any((root / name).exists() for name in protected): raise ValueError('Timing/audio already exists; use a fresh project or --replace after review')
    for name, data in files.items():
        target = root / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    p = sub.add_parser('init'); p.add_argument('kind', choices=ENGINES); p.add_argument('project'); p.add_argument('--example', action='store_true')
    p = sub.add_parser('build'); p.add_argument('kind', choices=QUICK); p.add_argument('spec'); p.add_argument('--snap'); p.add_argument('--replace', action='store_true')
    p = sub.add_parser('sync'); p.add_argument('project'); p.add_argument('--words', required=True); p.add_argument('--audio', required=True); p.add_argument('--reference'); p.add_argument('--method', choices=['provider-unreviewed', 'manual-reviewed', 'asr-unreviewed', 'synthetic-test'], required=True); p.add_argument('--replace', action='store_true')
    p = sub.add_parser('render'); p.add_argument('project'); p.add_argument('--out'); p.add_argument('--snap'); p.add_argument('--duration', type=float); p.add_argument('--audio'); p.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'doctor':
            result = {'runtime': str(RUNTIME), 'commands': {x: bool(shutil.which(x)) for x in ['node', 'npm', 'ffmpeg', 'ffprobe']}, 'node_packages': {x: (RUNTIME / 'kit/node_modules' / x).is_dir() for x in ['gsap', 'three', 'playwright']}, 'elevenlabs_key_configured': bool(os.environ.get('ELEVENLABS_API_KEY')), 'voice_id_configured': bool(os.environ.get('ELEVENLABS_VOICE_ID'))}
        elif args.command == 'init': result = init(args.kind, args.project, args.example)
        elif args.command == 'sync': result = sync(args.project, args.words, args.audio, args.method, args.reference, args.replace)
        elif args.command == 'build':
            command = [sys.executable, str(RUNTIME / 'skills' / QUICK[args.kind] / 'build.py'), args.spec]
            if args.snap: command += ['--snap', args.snap]
            if args.replace: command += ['--replace']
            subprocess.run(command, check=True); return 0
        else:
            root = Path(args.project).resolve(); kind = read(root / 'animation-project.json')['engine']
            audio = args.audio or (str(root / 'audio/vo.wav') if (root / 'audio/vo.wav').is_file() else None)
            result = capture(root, kind, args.out, [float(t) for t in args.snap.split(',')] if args.snap else None, args.duration, audio=audio, replace=args.replace)
        print(json.dumps(result, indent=2)); return 0
    except Exception as error:
        print(f'ERROR: {error}', file=sys.stderr); return 1


if __name__ == '__main__': raise SystemExit(main())
