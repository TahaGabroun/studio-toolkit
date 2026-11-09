# Motion and sound

Timing derives from named frame events. Start with ease-out cubic (0.16,1,0.3,1) on entrances and a faster ease-in exit; use restrained physical springs for objects, not for scientific quantities. Stagger causal dependencies, then hold text still to be read. A persistent object can transform roles through a scene. Constant motion, grain and glow are optional; calm teaching moments often need stillness.

The retained sound engine uses Python stdlib at 48 kHz, seeded noise, generators, placement, panning, integrated loudness estimation and peak-constrained mastering:

```bash
cd scripts
python3 -m sfx --list
python3 -m sfx path/to/cues.py --timeline path/to/timeline.json --out path/to/sfx.wav
```

A cue file defines score(mix, tl). Import click, pop, whoosh, chime, riser, impact or pad from sfx.synth. Set start time to event.start_frame / tl.fps; use duration_frames / fps for total duration. Mix.put(time, samples, gain, pan) places mono audio; put_stereo accepts a stereo pair. Sparse effects may remain quieter than the target; do not crush them to match a loudness number. Never call an SFX generator “narration”. Re-measure final encoded audio with FFmpeg and mix below speech. At most one hero sound per explanatory climax; avoid a whoosh on every label.

For simulation/3D, implement a closed-form renderer or seeded analytical paths rather than mutable physics advanced one frame at a time. The upstream's web-simulation kit and beat-analysis ideas are represented by the seek(t) pipeline and shared frame event contract. Separate preview clocks from deterministic frame rendering.
