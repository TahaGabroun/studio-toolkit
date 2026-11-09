#!/usr/bin/env python3
"""Coarse onset BPM and full/low-band energy, adapted from Howseen (MIT)."""
import argparse,json,subprocess
import numpy as np

def analyze(path):
    sr=22050;hop=256
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar',str(sr),'-f','f32le','-'])
    x=np.frombuffer(raw,np.float32);frames=len(x)//hop
    if frames<16:raise ValueError('Need at least 0.2 seconds of audio')
    env=np.sqrt(np.mean(x[:frames*hop].reshape(-1,hop)**2,axis=1));on=np.maximum(0,np.diff(np.log(env+1e-6)));on-=on.mean()
    window=on[:6000];ac=np.correlate(window,window,'full')[len(window)-1:]
    lo,hi=max(1,round(.33*sr/hop)),min(len(ac),round(1.0*sr/hop))
    bpm=None if hi<=lo or float(np.max(np.abs(on)))<1e-9 else round(60*sr/hop/(lo+int(np.argmax(ac[lo:hi]))),2)
    lp=np.convolve(x,np.ones(60)/60,'same');energy=[]
    for i in range(0,len(x),sr):
        seg=x[i:i+sr];low=lp[i:i+sr]
        energy.append({'start_s':i/sr,'full_db':round(float(10*np.log10(np.mean(seg**2)+1e-12)),2),'low_db':round(float(10*np.log10(np.mean(low**2)+1e-12)),2)})
    return {'duration_s':len(x)/sr,'estimated_bpm':bpm,'warning':'Coarse estimate; inspect real drop and half/double-time ambiguity','energy':energy}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('audio');a=p.parse_args()
    try:print(json.dumps(analyze(a.audio),indent=2))
    except (ValueError,subprocess.CalledProcessError) as e:raise SystemExit(str(e))
