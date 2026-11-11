---
name: motion-design
description: "Create deterministic HTML/CSS/SVG/JavaScript animations and render them with Chromium, Playwright and FFmpeg. Use for browser-based video scenes, simulations and narration-driven educational diagrams."
---

# Studio Motion HTML — seekable browser timeline

Choose this engine when SVG/HTML diagrams, simulations, text/layout or existing browser interactives are easier to animate than React. It produces video from frames; it **does not replace** delivering real interactive HTML when interactivity is the requested final product.

## Engine contract

- Implement a stable document containing `window.seek = async (seconds) => { ... }`. It must render the complete visual state for **any** input second independently of previous calls.
- Use declared timing data, pure interpolation/easing, seeded randomness and frame-time calculations. Avoid CSS transitions, requestAnimationFrame loops, mutable integration between frames, `Date.now()` and network dependencies during rendering.
- Ensure fonts/images are loaded before capture. Embed or locally package licensed assets. Do not silently hotlink images or fonts.
- Use semantic layers to highlight the exact diagram region while softening/dimming neighbors. Maintain crisp text; for Arabic use a font with proper shaping and test bidi/RTL.
- Keep HTML canvas/simulation controls separate from rendering if needed. Browser screenshots capture the frame, not functional interactions.

## Production path

1. Write brief, duration/FPS/resolution, scene table and time-bound visual referents.
2. Prepare one or more style frames and inspect before rendering the whole timeline.
3. Implement `window.seek(t)`, and verify seeking to times **out of order** gives identical frames.
4. Resolve MOTION to this skill directory and STUDIO to the actual studio-toolkit directory. With Python Playwright/Chromium and FFmpeg installed, render using the project’s real duration/FPS/dimensions. Example for a six-second landscape scene:
   ```bash
   python3 "$MOTION/scripts/render_html.py" PROJECT/scene.html PROJECT/render/silent.mp4 --duration 6 --fps 30 --width 1920 --height 1080 --check-determinism
   ```
   In the single-skill package MOTION is references/specialists/motion-design; STUDIO is the package root. Use the short proof and director review flow before a full production.
5. Mux actual sound where required, then run `python3 "$STUDIO/scripts/media.py" qa PROJECT PROJECT/render/final.mp4`. An intentionally soundless insert uses `--silent`; this flag cannot suppress missing narration in a project that declares it. QA creates PROJECT/qa/contact-sheet.jpg. Inspect opening, transitions, dense labels and the ending at full/mobile size; check flashes, off-screen labels, directionality and narrated referents.

6. If sound is separate, mux it at measured timestamps with FFmpeg; verify final mux duration and listen to head/middle/tail. Do not truncate narration unintentionally.

## Failure policy

When the host lacks a browser or encoder, provide HTML source and a tested command line plus a clear `render not run` status. Never pretend the MP4 exists. If the result must stay interactive, preserve or supply the original HTML separately.

## Native execution contract

Read [browser production](references/browser-production.md). Inputs: storyboard and shared timeline plus local assets; outputs: seekable HTML, measured audio mix, rendered video and contact sheet. Execute [scripts/render_html.py](scripts/render_html.py) with explicit duration, FPS and dimensions. It waits for fonts/images, settles two browser frames, detects page errors, and optionally verifies out-of-order seeking. Use the orchestrator media utility for speech-first mixing, muxing and QA. `claude-motion-adapted` supplies direction; `remotion-video` is the alternative React engine.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.

## Production providers

For anatomical, biological or physical mechanism diagrams, use the actual anatomy skill before implementing the animation; preserve its recognizable structures and semantic layers. Newly generated production narration uses ElevenLabs with a selected voice and measured provider cues. Read [production preferences](../studio-toolkit/references/production-preferences.md). Report missing anatomy/voice access instead of substituting generic diagrams or a local test voice. Preserve supplied approved recordings and explicit user overrides.
