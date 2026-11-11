#!/usr/bin/env python3
"""Measured media QA, deterministic test audio and speech-first mixing."""
from __future__ import annotations
import argparse
import json
import math
import re
import subprocess
import sys
import wave
from pathlib import Path
import numpy as np
from studio import read, write, probe, validate, digest, local, fingerprints

def run(argv, **kwargs):
    return subprocess.run(argv, check=True, capture_output=True, **kwargs)

def pcm(path, sample_rate=48000):
    raw = run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sample_rate), "-f", "f32le", "-"], input=None).stdout
    return np.frombuffer(raw, np.float32)

def wav(path, samples, sr=48000):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((np.clip(samples, -.99, .99) * 32767).astype("<i2").tobytes())

def test_audio(root):
    """Clearly labelled calibration pulses, not synthetic speech."""
    root = Path(root); p, t = read(root / "project.json"), read(root / "timeline.json")
    sr = 48000; x = np.zeros(round(p["duration_frames"] / p["fps"] * sr), np.float32)
    markers = []
    for e in t["events"]:
        at = e["start_frame"] / p["fps"]; n = round(.05 * sr)
        env = np.sin(np.linspace(0, math.pi, n)) ** 2
        tone = .6 * env * np.sin(2 * math.pi * 1200 * np.arange(n) / sr)
        i = round(at * sr); count = min(n, len(x) - i)
        x[i:i+count] += tone[:count]
        markers.append({"event_id": e["id"], "start_s": at, "peak_s": at + .025})
    output = root / "assets/calibration.wav"; wav(output, x)
    write(root / "qa/calibration.json", {"kind": "synthetic timing pulses; not narration", "audio_sha256": digest(output), "markers": markers})
    return output

def loudness(path):
    result = run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "loudnorm=I=-16:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], text=True)
    matches = re.findall(r'\{\s*"input_i".*?\}', result.stderr, re.S)
    if not matches: raise ValueError("Unable to measure integrated loudness")
    return json.loads(matches[-1])

def normalize(src, dst, target=-16, peak=-1.5):
    data = loudness(src)
    if not all(math.isfinite(float(data[k])) for k in ["input_i", "input_tp", "input_lra", "input_thresh"]): raise ValueError("Silent/invalid audio cannot be loudness normalized")
    filt = f"loudnorm=I={target}:TP={peak}:LRA=11:measured_I={data['input_i']}:measured_TP={data['input_tp']}:measured_LRA={data['input_lra']}:measured_thresh={data['input_thresh']}:offset={data['target_offset']}:linear=true"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", filt, "-ar", "48000", str(dst)])

def mix(root):
    root = Path(root); p, config = read(root / "project.json"), read(root / "mix.json")
    errors = validate(root)["errors"]
    if errors: raise ValueError("; ".join(errors))
    sr=48000; count=round(p["duration_frames"] / p["fps"] * sr)
    tracks = []
    speech = np.zeros(count, np.float32)
    for item in config["tracks"]:
        x = pcm(local(root, item["path"])); start=round(item["start_frame"] / p["fps"] * sr)
        if start+len(x)>count+round(sr/p["fps"]): raise ValueError(f"Track would be truncated: {item['path']}")
        dest = np.zeros(count, np.float32); n=min(len(x),count-start)
        dest[start:start+n] = x[:n] * 10 ** (item["gain_db"] / 20)
        if item["role"] == "narration": speech += dest
        tracks.append((item["role"],dest))
    # 10 ms RMS detector, 150 ms release. Speech controls bed ducking, not a fixed time guess.
    hop=480; blocks=math.ceil(count/hop)
    padded=np.pad(speech,(0,blocks*hop-count)).reshape(blocks,hop)
    rms=np.sqrt(np.mean(padded*padded,axis=1)); envelope=np.zeros(blocks)
    for i,v in enumerate(rms): envelope[i]=max(v, envelope[i-1]*.935 if i else 0)
    gain=np.interp(np.arange(count)/hop,np.arange(blocks),np.where(envelope>.01,10**(-9/20),1))
    result=np.zeros(count,np.float32)
    for role,x in tracks: result += x*gain if role=='music' else x
    raw=root/'render/mix-raw.wav'; raw.parent.mkdir(exist_ok=True); wav(raw,result/max(1,float(np.max(np.abs(result)))/.95))
    output=root/'render/mix.wav'; normalize(raw,output,config['target_lufs'],config['true_peak_db'])
    write(root/'qa/mix.json',{'measurement':loudness(output),'duck_db':9,'status':'measured; listen before release'})
    return output

def mux(video, audio, output):
    v, a=probe(video),probe(audio)
    vd,ad=float(v['format']['duration']),float(a['format']['duration'])
    if abs(vd-ad)>.1: raise ValueError(f"Mux duration mismatch: video={vd}, audio={ad}; retime or pad explicitly")
    run(['ffmpeg','-v','error','-y','-i',str(video),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(output)])

def contact(video, output, duration, times=None):
    from PIL import Image, ImageDraw
    import tempfile
    times = times or [duration*i/12 for i in range(12)]
    tiles=[]
    with tempfile.TemporaryDirectory(prefix='studio-contact-') as tmp:
        for i,t in enumerate(times):
            path=Path(tmp)/f'{i}.png'
            run(['ffmpeg','-v','error','-ss',str(max(0,min(t,duration-.05))),'-i',str(video),'-frames:v','1','-vf','scale=480:-2',str(path)])
            with Image.open(path) as source: tile=source.convert('RGB')
            canvas=Image.new('RGB',(480,tile.height+28),'#eeeae2');canvas.paste(tile,(0,0));ImageDraw.Draw(canvas).text((8,tile.height+7),f'{t:.3f}s',fill='#222222');tiles.append(canvas)
    h=max(t.height for t in tiles);sheet=Image.new('RGB',(480*4,h*math.ceil(len(tiles)/4)),'#d8d2c8')
    for i,t in enumerate(tiles):sheet.paste(t,((i%4)*480,(i//4)*h))
    Path(output).parent.mkdir(parents=True,exist_ok=True);sheet.save(output)

def qa(root, video, calibration=False, silent=False):
    root=Path(root);p=read(root/'project.json'); report=validate(root)
    if silent:
        requirements=read(root/'production-requirements.json') if (root/'production-requirements.json').exists() else None
        if requirements is not None and (not isinstance(requirements,dict) or not isinstance(requirements.get('narration'),dict)):raise ValueError('Valid narration intent is required for silent QA')
        mix=read(root/'mix.json') if (root/'mix.json').exists() else {}
        if calibration or (root/'narration.json').exists() or any(t.get('role')=='narration' for t in mix.get('tracks',[])) or requirements and requirements['narration']['mode']!='none':raise ValueError('Silent QA conflicts with declared narration/calibration; do not hide a missing voice stream')
    data=probe(video);streams=data['streams'];v=next((s for s in streams if s['codec_type']=='video'),None);a=next((s for s in streams if s['codec_type']=='audio'),None)
    errors=report['errors'];warnings=report['warnings'];expected=p['duration_frames']/p['fps']
    if not v:errors.append('No video stream')
    else:
        if (v['width'],v['height'])!=(p['width'],p['height']):errors.append('Video dimensions mismatch')
        num,den=map(float,v['avg_frame_rate'].split('/'))
        if abs(num/den-p['fps'])>.001:errors.append('Video FPS mismatch')
        if 'nb_frames' in v and int(v['nb_frames'])!=p['duration_frames']:errors.append('Video frame count mismatch')
        if abs(float(v.get('duration',data['format']['duration']))-expected)>1/p['fps']+.002:errors.append('Video duration mismatch')
    if silent and a:errors.append('Explicitly silent output contains an audio stream')
    if not a and not silent:errors.append('No audio stream')
    elif a and v:
        if abs(float(a.get('start_time',0))-float(v.get('start_time',0)))>1/p['fps']:errors.append('Audio/video stream start skew')
        if abs(float(a.get('duration',0))-expected)>2/p['fps']+.01:errors.append('Audio duration mismatch')
    # Decode every frame/sample; successful probing alone does not verify the media.
    run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'])
    report.update({'video_sha256':digest(video),'input_hashes':fingerprints(root,'render'),'expected_seconds':expected,'probe':data,'audio_intent':'explicitly silent' if silent else 'audio required','visual_review':'pending human approval','semantic_narration_alignment':'not applicable to explicitly silent output' if silent else 'requires listening and representative frame review'})
    if a:
        measured=loudness(video);report['loudness']=measured
        if float(measured['input_tp'])>-.8:errors.append('True peak exceeds -0.8 dBTP')
        if not calibration and not -18<=float(measured['input_i'])<=-14:warnings.append('Integrated loudness outside speech default -18..-14 LUFS; review intent')
    if calibration:
        x=pcm(video);markers=read(root/'qa/calibration.json')['markers'];offsets=[]
        for marker in markers:
            at=marker['peak_s'];lo=max(0,round((at-.05)*48000));hi=min(len(x),round((at+.05)*48000))
            index=lo+int(np.argmax(np.abs(x[lo:hi])));offsets.append(index/48000-at)
        report['calibration_peak_offsets_s']=offsets
        if any(abs(v)>1/p['fps'] for v in offsets):errors.append('Calibration audio pulse differs from timeline by over one frame')
    out=root/'qa/contact-sheet.jpg';contact(video,out,expected)
    report['status']='fail' if errors else 'pass';write(root/'qa/automated.json',report)
    lines=['# QA report',f"\nAutomated status: {report['status']}",f'\nExpected duration: {expected:.3f}s; resolution: {p["width"]} × {p["height"]}; fps: {p["fps"]}.','\nHuman visual and listening approval: pending.','\n## Errors']+['- '+e for e in errors]+['\n## Warnings']+['- '+e for e in warnings]+['\nContact sheet: qa/contact-sheet.jpg. Inspect opening, every focus change, caption seam and final hold at desktop and 360 px width. Automated stream synchronization does not prove semantic or phoneme accuracy.']
    (root/'qa-report.md').write_text('\n'.join(lines)+'\n');return report

def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    for n in ['test-audio','mix']:s.add_parser(n).add_argument('project')
    a=s.add_parser('mux');a.add_argument('video');a.add_argument('audio');a.add_argument('output')
    a=s.add_parser('qa');a.add_argument('project');a.add_argument('video');a.add_argument('--calibration',action='store_true');a.add_argument('--silent',action='store_true',help='Intentionally soundless output; rejects projects declaring narration')
    a=p.parse_args()
    try:
        if a.command=='test-audio':print(test_audio(a.project))
        elif a.command=='mix':print(mix(a.project))
        elif a.command=='mux':mux(a.video,a.audio,a.output)
        else:
            r=qa(a.project,a.video,a.calibration,a.silent);print(json.dumps({k:r[k] for k in ['status','errors','warnings']},indent=2));return int(r['status']!='pass')
        return 0
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as e:
        print(f'ERROR: {e}',file=sys.stderr)
        if isinstance(e,subprocess.CalledProcessError):print(e.stderr.decode(errors='replace')[-1500:] if isinstance(e.stderr,bytes) else e.stderr,file=sys.stderr)
        return 1

if __name__=='__main__':raise SystemExit(main())
