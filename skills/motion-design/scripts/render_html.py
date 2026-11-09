#!/usr/bin/env python3
"""Capture a deterministic window.seek(seconds) HTML animation and encode MP4."""
import argparse
import os
import hashlib
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def render(args):
    src=Path(args.html).expanduser().resolve()
    target=Path(args.output).expanduser().resolve()
    if not src.is_file(): raise ValueError(f'HTML file not found: {src}')
    if args.duration<=0 or args.fps<=0: raise ValueError('Duration and FPS must be positive')
    if args.width<2 or args.height<2: raise ValueError('Resolution too small')
    if args.width%2 or args.height%2: raise ValueError('MP4 H.264 needs even width/height')
    if shutil.which('ffmpeg') is None: raise RuntimeError('ffmpeg executable not installed')
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError('Python Playwright missing: pip install playwright && playwright install chromium') from e
    total=math.ceil(args.duration*args.fps)
    if total>36000 and not args.allow_large: raise ValueError('Over 36,000 frames; pass --allow-large to acknowledge resource usage')
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='studio-frames-') as tmp:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True, executable_path=args.browser or os.environ.get('CHROMIUM') or None)
            context=browser.new_context(viewport={'width':args.width,'height':args.height},device_scale_factor=args.scale)
            page=context.new_page()
            failures=[]
            page.on('pageerror',lambda e: failures.append(str(e)))
            page.on('requestfailed',lambda r: failures.append(r.url))
            page.goto(src.as_uri(),wait_until='load')
            page.evaluate('document.fonts.ready')
            page.evaluate("Promise.all([...document.images].map(i => i.decode()))")
            page.evaluate("document.getAnimations().forEach(a=>a.pause())")
            if not page.evaluate("typeof window.seek === 'function'"):
                raise RuntimeError('HTML must expose window.seek(seconds)')
            if args.check_determinism:
                stamps=[args.duration*.2,args.duration*.8,args.duration*.2]
                hashes=[]
                for t in stamps:
                    page.evaluate('(t)=>window.seek(t)',t)
                    page.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                    hashes.append(hashlib.sha256(page.screenshot()).hexdigest())
                if hashes[0]!=hashes[2]: raise RuntimeError('Out-of-order seeking is nondeterministic')
            for frame in range(total):
                page.evaluate('(t) => window.seek(t)',frame/args.fps)
                page.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                if failures: raise RuntimeError('; '.join(failures))
                page.screenshot(path=str(Path(tmp)/f'frame_{frame:06d}.png'))
                if frame%args.fps==0: print(f'Frame {frame}/{total}',flush=True)
            context.close();browser.close()
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(args.fps),'-i',str(Path(tmp)/'frame_%06d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf',str(args.crf),'-color_range','tv','-colorspace','bt709','-movflags','+faststart',str(target)]
        subprocess.run(cmd,check=True)
    print('Rendered:',target,'frames:',total,'size:',target.stat().st_size)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('html');p.add_argument('output');p.add_argument('--duration',type=float,required=True)
    p.add_argument('--fps',type=int,default=30);p.add_argument('--width',type=int,default=1920);p.add_argument('--height',type=int,default=1080)
    p.add_argument('--scale',type=float,choices=[1.0],default=1.0,help='Use width/height for 4K; scale stays 1')
    p.add_argument('--browser',help='Explicit Chromium executable')
    p.add_argument('--check-determinism',action='store_true')
    p.add_argument('--crf',type=int,default=18);p.add_argument('--allow-large',action='store_true')
    args=p.parse_args()
    try: render(args);return 0
    except Exception as e:  # Includes Playwright browser-install/launch errors with actionable messages.
        print(f'ERROR: {e}',file=sys.stderr);return 1
if __name__=='__main__': raise SystemExit(main())
