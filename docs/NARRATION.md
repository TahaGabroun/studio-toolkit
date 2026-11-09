# Narration, timing and Arabic

Accept existing WAV, MP3 or M4A. Probe actual duration and retain the original bytes. Transcription and forced alignment are different: local faster-whisper produces ASR with estimated word timestamps, not a guaranteed forced alignment of an exact user transcript. This toolkit imports reviewed timestamps and labels ASR drafts honestly.

```json
{"segments":[{"id":"cue-1","start_s":0.4,"end_s":2.1,"text":"The vessel wall becomes more permeable."}]}
```

Create timeline events with cue_id cue-1 and a storyboard target such as venular-wall. align imports timestamps, hashes the audio, updates event frame boundaries and regenerates SRT. Segment long text at measured word boundaries; do not evenly divide words by duration. Review waveform/speech at every semantic transition and tune timestamps when needed. Replacing audio bytes invalidates alignment. If narration exceeds the project duration, extend the project/scenes explicitly; muxing never uses -shortest to hide a mismatch.

Optional ASR: install requirements-transcription.txt in a venv and run scripts/transcribe.py AUDIO draft.json --language ar. The first use downloads an open model and needs storage/network. Review Arabic scientific terms and English switches carefully before importing. No ASR inference was claimed in the baseline validation.

Arabic projects set direction rtl and load a local Arabic font. Preserve connected glyphs, avoid tracking Arabic letters, use generous line height and test punctuation/numbers. In DOM text use bdi or an LTR span for CO₂, DNA and English terms; never reverse strings manually. SRT text remains logical Unicode order. The vertical demo tests Arabic text mixed with CO2 and source narration generated locally. Generated speech and its pronunciation still need human listening approval.

The educational demo measures each generated speech phrase separately, adds known silent gaps, and schedules semantic focus to phrase onset. This is phrase-level generated-audio synchronization, not word-level forced alignment of spontaneous speech. Calibration pulses additionally test encoded audio/event alignment within one frame. Biological events overlap and unfold over longer times than the film's compressed teaching sequence.
