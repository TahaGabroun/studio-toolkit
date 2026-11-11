# Browser production

Expose async window.seek(seconds). Set every property from time, including the hidden state, so out-of-order seeks produce identical screenshots. Use local fonts and assets; await fonts.ready and image decoding. No live CSS transitions, Date.now, unseeded random or integration from the previous frame. For footage, await seeked. For WebGL, select a working browser renderer and verify actual non-black frames. Preview controls can use requestAnimationFrame but must call the same seek(t).

```bash
python3 scripts/render_html.py scene.html silent.mp4 --duration 6 --fps 30 --width 1920 --height 1080 --check-determinism
```

Use --browser /path/to/chromium or CHROMIUM when browser downloads are unavailable. Width and height are real encoded dimensions; set 3840×2160 explicitly for 4K. The renderer fails on page errors, missing image decoding or encoder errors. Probe style frames before a long render. The primary renderer does not implement motion-blur accumulation; if needed sample a shutter interval without blending across hard cuts, then verify frame count and seams.

Audio: orchestrator media.py mix PROJECT reads mix.json, ducks music under speech and applies measured two-pass normalization. media.py mux SILENT AUDIO OUTPUT rejects duration mismatch instead of silently truncating narration. media.py qa PROJECT OUTPUT decodes full media and creates a contact sheet. Explicitly soundless inserts use --silent; projects declaring narration cannot use it to hide a missing voice stream. Use the retained analyze_song.py for coarse onset/BPM and low-band energy; manually verify a music drop. svgl_logos.py and mixkit_sfx_search.py are optional network discovery helpers; source availability and rights remain external, so do not treat a download as a redistribution license.

Camera uses one spatial world, smooth focal position, log-space zoom and stable reading holds. Morph shared elements where it clarifies continuity. Capture key frames around seams; for loops compare both position and entering/exiting velocity. For reference remakes, use only rights-cleared reference media, extract a shot/cut table with scripts/reference_video.py, design original assets, and compare synchronized contact sheets. Never copy private logos, faces, music or a branded gallery automatically.
