# Cartoon animation integration — 0.4.0

Six native skills adapt the pinned MIT/OFL claude-animation-skills runtime for Codex and the portable ChatGPT toolkit. The original nine IDs remain; Anatomy stays the preferred scientific/mechanism drawing system and new production narration stays ElevenLabs.

Canonical additions: cartoon-animation (upstream zach-d-films), stick-figure, minimalistic-graphics, animated-graph (graph), map-route, exploded-view (breakdown). All source procedures are rewritten for native discovery and actual host tools. The runtime retains character rigs, materials, textures, props, camera/keyframes/IK, templates, caption grouping and procedural sound source. The inherited voice recording is excluded. SOURCES.md and the runtime provenance manifest identify copied/adapted files, licenses and the pinned revision.

The shared CLI performs project-local initialization, JSON builds, measured-cue import, snapshots and MP4 production. Dependencies are pinned and installed locally. It never downloads models or generates speech implicitly. Sync preserves original audio timing, validates cues against the decoded take and labels review provenance. The portable package contains runtime source and dependency locks, not node_modules/models/caches.

## Executed validation

- Repository metadata, Markdown references, Python syntax, schema mirrors and pinned source notices passed.
- 76 Python tests passed, including cue integrity/provenance, script matching, existing-file protection, Arabic/scientific text, long-pause grouping, take-warp invariants and dependency-free package structure.
- All six skill manifests passed the official local skill validator. Fifteen toolkit skills plus Anatomy are installed; all six additions were found in the actual Codex CLI skill catalog.
- All six workflows rendered full 1080×1920/30 fps MP4s, with probed frame counts of 120 (graph), 114 (line art), 120 (map), 126 (device), 120 (stick) and 120 (3D cartoon). FFmpeg encoding, full decoding, duration and resolution checks passed. 3D source capture remains 720×1280 with an explicit upscale.
- Both engines separately imported synthetic timing cues, rendered four-second MP4s with audio, and displayed uppercase CO2 and Arabic لَم at the measured sampled cue windows. No caption appeared in the long pause. The signals are timing fixtures, not speech.
- Five modes passed exact out-of-order pixel comparison. The numeric graph reported 13 changed antialiasing pixels with a maximum 9/255 channel delta; this is within its explicit 32-pixel/16-channel SVG raster tolerance. It is not an identical-hash claim.
- Standalone package extraction and graph snapshot execution passed using the same lock-matched local dependencies. The package excludes node_modules/models/caches and contains one SKILL.md.
- Independent forward testing found and verified fixes for scientific casing/Arabic mark loss and invalid font declarations. Corrected graph typography, zero-ending data and timed captions were visually inspected. Agent inspection is not full human creative approval.
- The retained 37.4-second procedural soundtrack/SFX generator ran with a silent calibration take and produced finite stereo audio. Silent-input normalization and an extra audio tail were corrected. Optional Kokoro/Parakeet model inference was not run.
- The existing full HTML production and seven demo Node regression tests passed.

Published CI results are verified after pushing this version. No live ElevenLabs generation or ChatGPT account import is claimed. The default examples are silent visual calibrations; they do not prove narration pronunciation or scientific accuracy. The cartoon engine retains native 720×1280 capture with a 1080×1920 upscale. The other templates are vertical/30 fps; map geography and phone layers are illustrative.
