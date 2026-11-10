#!/usr/bin/env python3
"""Exercise the retained procedural score/SFX with an explicitly silent voice fixture."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/studio-toolkit/scripts'))
import animation

def run(output):
    import numpy as np
    import soundfile as sf
    output=Path(output).resolve();animation.init('stick-figure',output,example=True)
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t','37.4',str(output/'audio/vo.wav')],check=True)
    subprocess.run([sys.executable,'-W','error','audio.py'],cwd=output,check=True)
    samples,rate=sf.read(output/'audio/mix.wav')
    if not np.isfinite(samples).all() or not np.any(samples):raise ValueError('Nonfinite or empty procedural audio')
    if abs(len(samples)/rate-37.4)>.001:raise ValueError('Soundtrack differs from authored edit duration')
    result={'status':'pass','duration_seconds':len(samples)/rate,'sample_rate':rate,'channels':samples.shape[1],'peak':float(np.max(np.abs(samples))),'input':'silent calibration; no speech generation','source_sha256':hashlib.sha256((output/'audio.py').read_bytes()).hexdigest()}
    (output/'audio-qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);run(parser.parse_args().output)
