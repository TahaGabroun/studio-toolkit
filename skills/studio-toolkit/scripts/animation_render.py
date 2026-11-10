#!/usr/bin/env python3
"""Render the adopted animation engines from their deterministic time functions.

Uses the toolkit's Python Playwright, local HTTP and FFmpeg. No model or API call.
"""
from contextlib import contextmanager
from functools import partial
import hashlib
import io
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
from threading import Thread


def pixel_difference(first, second):
    from PIL import Image, ImageChops
    difference = ImageChops.difference(Image.open(io.BytesIO(first)).convert('RGB'), Image.open(io.BytesIO(second)).convert('RGB'))
    extrema = difference.getextrema()
    return {'changed_pixels': sum(1 for pixel in difference.getdata() if max(pixel)), 'max_channel_delta': max(high for low, high in extrema)}


@contextmanager
def serve(root):
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(root)))
    thread = Thread(target=server.serve_forever, daemon=True); thread.start()
    try: yield f'http://127.0.0.1:{server.server_port}'
    finally: server.shutdown(); server.server_close(); thread.join()


def inspect_media(video, width, height, fps, frames, audio=False):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)], check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    stream = next(s for s in data['streams'] if s['codec_type'] == 'video')
    if (stream['width'], stream['height']) != (width, height): raise ValueError('Rendered resolution differs from request')
    if int(stream['nb_frames']) != frames: raise ValueError('Rendered frame count differs from request')
    rate = stream['avg_frame_rate'].split('/')
    if abs(int(rate[0]) / int(rate[1]) - fps) > 1e-6: raise ValueError('Rendered frame rate differs from request')
    if abs(float(stream['duration']) - frames / fps) > .001: raise ValueError('Rendered duration differs from frame clock')
    if audio and not any(s['codec_type'] == 'audio' for s in data['streams']): raise ValueError('Missing muxed audio')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-f', 'null', '-'], check=True, capture_output=True)
    return {'width': width, 'height': height, 'fps': fps, 'frames': frames, 'duration_seconds': frames / fps, 'full_decode': 'pass', 'audio_present': any(s['codec_type'] == 'audio' for s in data['streams'])}


def capture(root, kind, output=None, times=None, duration=None, fps=30, audio=None, replace=False):
    from playwright.sync_api import sync_playwright
    root = Path(root).resolve()
    if kind not in ['quick', 'stick-figure', 'cartoon-animation']: raise ValueError('Unknown animation engine')
    if fps != 30: raise ValueError('Adopted engines currently use 30 fps')
    entry = 'web/index.html' if kind == 'stick-figure' else 'index.html'
    if not (root / entry).is_file(): raise ValueError(f'Missing {entry}')
    output = Path(output).resolve() if output else root / 'render/silent.mp4'
    if not times and output.exists() and not replace: raise ValueError('Output exists; use another path or --replace')
    native = (720, 1280) if kind == 'cartoon-animation' else (1080, 1920)
    errors = []
    with serve(root) as url, sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM') or None)
        try:
            page = browser.new_page(viewport={'width': native[0], 'height': native[1]}, device_scale_factor=1)
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('requestfailed', lambda request: errors.append('Failed asset: ' + request.url))
            page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status >= 400 and not response.url.endswith('favicon.ico') else None)
            page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(url + '/') or route.request.url.startswith(('data:', 'blob:')) else route.abort())
            page.goto(url + '/' + entry + '?render=1', wait_until='load')
            if kind == 'quick':
                # GSAP Timeline is thenable; return a boolean rather than awaiting a paused timeline.
                page.wait_for_function('!!(window.__studioReady || window.__timelines?.main)')
                seek = '(t) => { if(typeof window.seek === "function") window.seek(t); else if(window.__timelines?.main) { window.__timelines.main.totalTime(0, false); window.__timelines.main.totalTime(t, false); } else window.dispatchEvent(new CustomEvent("hf-seek", {detail:{time:t}})); }'
                measured = page.eval_on_selector('[data-duration]', 'el => Number(el.dataset.duration)')
            elif kind == 'stick-figure':
                page.wait_for_function('typeof window.renderFrame === "function"')
                seek = '(t) => window.renderFrame(Math.round(t * 30))'
                measured = page.evaluate('window.TOTAL_FRAMES / 30')
            else:
                page.wait_for_function('window.renderAt && window.ready')
                page.evaluate('window.ready')
                seek = '(t) => window.renderAt(t)'
                measured = page.evaluate('window.DURATION')
            page.evaluate('document.fonts.ready')
            page.evaluate('Promise.all([...document.fonts].map(font => font.load()))')
            if not math.isfinite(measured) or measured <= 0: raise ValueError('Invalid authored animation duration')
            if duration is None: duration = measured
            if not math.isfinite(duration) or duration <= 0 or duration > measured + 1e-6: raise ValueError('Requested duration exceeds the authored animation; retime shots first')
            frames = math.ceil(duration * fps - 1e-9)
            if frames > 36000: raise ValueError('Over 36,000 frames; render reviewed chapters separately')
            if audio:
                data = json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-of','json',str(audio)],check=True,capture_output=True,text=True).stdout)
                if float(data['format']['duration']) > frames / fps + .05: raise ValueError('Narration exceeds authored shots; retime the edit before rendering')
            def frame(t):
                page.evaluate(seek, t)
                page.evaluate('new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')
                if errors: raise RuntimeError('; '.join(errors))
                return page.screenshot(type='png', animations='disabled')
            # A seek must not depend on previously rendered poses or playback history.
            frame(0)  # Initialize lazy GSAP styles and GPU/SVG resources before comparing pixels.
            a = frame(duration * .2); frame(duration * .8); b = frame(duration * .2)
            delta = pixel_difference(a, b)
            # Chromium SVG path rasterization can differ by a few antialiasing pixels.
            # Limit this exception to the graph, and report it instead of claiming identical hashes.
            graph = kind == 'quick' and page.locator('path#line').count() == 1
            if delta['changed_pixels'] and not (graph and delta['changed_pixels'] <= 32 and delta['max_channel_delta'] <= 16): raise ValueError(f'Out-of-order seeking changed pixels: {delta}; fix stateful shot updates')
            evidence = {'engine': kind, 'native_width': native[0], 'native_height': native[1], 'determinism': 'pass-with-svg-raster-tolerance' if delta['changed_pixels'] else 'pass-exact-pixels', 'seek_pixel_difference': delta, 'agent_visual_review': 'pending', 'human_approval': 'pending'}
            if times is not None:
                if not times or any(not math.isfinite(t) or not 0 <= t < measured for t in times): raise ValueError('Snapshot times must be within authored duration')
                output.mkdir(parents=True, exist_ok=True)
                targets = [output / f't_{t:.3f}.png' for t in times]
                if not replace and any(p.exists() for p in targets): raise ValueError('Snapshot exists; choose another folder or --replace')
                for t, target in zip(times, targets): target.write_bytes(frame(t))
                return {**evidence, 'stills': [str(p) for p in targets]}
            output.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='.studio-animation-', dir=output.parent) as temporary:
                candidate = Path(temporary) / 'video.mp4'
                cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'png', '-i', '-']
                if audio: cmd += ['-i', str(Path(audio).resolve()), '-map', '0:v', '-map', '1:a', '-af', 'apad,loudnorm=I=-16:TP=-1.5:LRA=9', '-c:a', 'aac', '-b:a', '192k']
                cmd += ['-vf', 'scale=1080:1920:flags=lanczos', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-t', str(frames / fps), '-movflags', '+faststart', str(candidate)]
                with tempfile.TemporaryFile() as log:
                    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=log)
                    try:
                        for number in range(frames):
                            process.stdin.write(frame(number / fps))
                            if number % 30 == 0: print(f'Animation frame {number}/{frames}', flush=True)
                        process.stdin.close()
                        if process.wait() != 0:
                            log.seek(0); raise RuntimeError(log.read().decode(errors='replace')[-3000:])
                    finally:
                        if process.poll() is None: process.kill(); process.wait()
                evidence.update(inspect_media(candidate, 1080, 1920, fps, frames, bool(audio)))
                evidence['video_sha256'] = hashlib.sha256(candidate.read_bytes()).hexdigest()
                candidate.replace(output)
            output.with_suffix('.qa.json').write_text(json.dumps(evidence, indent=2) + '\n')
            return {**evidence, 'video': str(output)}
        finally: browser.close()
