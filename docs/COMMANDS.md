# Command reference

Run using the repository .venv Python; resolve installed skill scripts through their symlink target. The canonical runtime is skills/studio-toolkit/scripts.

```bash
python scripts/studio.py doctor
python scripts/studio.py init PROJECT --title "Title" --format landscape --fps 30 --duration 60 --language en
python scripts/studio.py validate PROJECT
python scripts/studio.py status PROJECT
python scripts/studio.py workflow-check PROJECT --anatomical --generate-narration
python skills/studio-toolkit/scripts/elevenlabs_narration.py PROJECT --voice-id VOICE_ID --dry-run
python skills/studio-toolkit/scripts/elevenlabs_narration.py PROJECT --voice-id VOICE_ID
python scripts/studio.py script-check PROJECT/script.json
python scripts/studio.py complete PROJECT idea
python scripts/studio.py align PROJECT --audio assets/narration.mp3 --segments timestamps.json --method manual-reviewed
python skills/studio-toolkit/scripts/media.py test-audio PROJECT
python skills/studio-toolkit/scripts/media.py mix PROJECT
python skills/studio-toolkit/scripts/media.py mux silent.mp4 PROJECT/render/mix.wav PROJECT/render/final.mp4
python skills/studio-toolkit/scripts/media.py qa PROJECT PROJECT/render/final.mp4
python skills/studio-toolkit/scripts/media.py qa PROJECT calibration-video.mp4 --calibration
python skills/motion-design/scripts/render_html.py scene.html silent.mp4 --duration 6 --check-determinism
python scripts/validate_repository.py
python scripts/package_chatgpt.py
```

Stage names: idea, research, strategy, script, storyboard, design, assets, animation, narration, audio, render, qa, publication. A complete call fails when predecessors or outputs are missing. A valid draft may report pending artifacts. QA exits nonzero for critical schema/media failures. Loudness outside the speech target is a review warning; missing audio, invalid dimensions, duration/stream skew and decode failures are errors. Calibration checks generated pulse peaks against event times and are not semantic or phoneme accuracy measurements.

Legacy tools/ entrypoints are compatibility wrappers to the native runtime; tools/analyze_retention.py remains the archive's descriptive CSV analyzer. The qa_video.py wrapper uses the new media.py subcommands. Use the preserved per-skill utilities through their documented --help and local export inputs.

`workflow-check` reports anatomy/ElevenLabs dependencies without generation. `elevenlabs_narration.py` uses cached responses when the approved text, voice, model and output format match; --dry-run never sends a request. --import-response FILE accepts an actual exported ElevenLabs response without using the API. Candidate scene IDs become cue IDs; update timeline mappings and measured scene boundaries before `align --method provider-unreviewed`. These provider timings still require listening and scientific-pronunciation review. No automatic billable retry or production fallback voice is used.

To install, validate, list, update or uninstall the supplied Anatomy integration together with the canonical skills, add --with-anatomy to the matching install.sh/uninstall.sh command. `workflow-check --diagrams` is an alias for --anatomical and applies to technical mechanism diagrams as well as biological figures.

## Adopted animation runtime

`python scripts/animation.py doctor` reports dependency/credential presence without exposing credentials. `build SKILL SPEC [--snap TIMES]` runs four JSON-driven templates. `init stick-figure|cartoon-animation DIR [--example]` creates a fresh local engine project. `sync DIR --words FILE --audio FILE --method METHOD` imports measured narration; --reference supports matching-word take warps in the stick engine. `render DIR [--snap TIMES] [--out PATH] [--audio MIX]` captures frames or a full MP4. --replace is explicit for existing generated timing/media. Read the shared animation workflow for constraints and review.
