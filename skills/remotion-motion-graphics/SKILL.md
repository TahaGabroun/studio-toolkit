---
name: remotion-motion-graphics
description: "Create reusable Remotion typography, diagrams, infographics, editorial highlights, authentic terminal inserts and continuous camera compositions. Use for specialist motion graphics, overlays or explanatory inserts."
---

# Studio Remotion Graphics — identity-accurate overlays

Use for **editor-insert graphics** rather than a full film. Pair with `claude-motion-adapted` for visual grammar and `remotion-video` for integration into the master edit.

## Scope and visual contract

1. Establish aspect ratio, pixel size, duration, FPS, intended editing software and final surface. For transparent overlays, confirm the requested alpha workflow; MP4/H.264 does not normally preserve alpha.
2. Collect authentic logos, screenshots, datasets and quotes from the user or authoritative sources. For named products, do not create fake UI/screenshots or invent operational metrics. Label demonstrative values `Illustrative`.
3. Choose a visual mechanism: logo/identity, infographics, editorial highlight, terminal demo or a continuous-world camera scene. Use motion to explain causal flow and keep strong eye guidance.
4. Text should complement narration, not replicate it word for word unless a caption is the actual requirement. Critical labels must be readable on mobile; maintain platform safe areas.
5. Use a consistent theme, well-chosen local fonts (with Arabic glyph support if needed), restrained accent colors, natural springs/staggers and visual holds. No default neon, generic glow, random dashboard cards or gratuitous effects.
6. Keep animation deterministic, driven by frame/time and explicit data, with stable semantic keys and render-safe React patterns. Avoid hooks inside loops, `.map()` or conditional branches.

## Alpha and QA

- Choose a codec/container/sequence that actually carries alpha. A PNG RGBA image sequence or a correctly configured/validated ProRes 4444 workflow is acceptable; verify with `ffprobe` and actual compositing over contrasting test backgrounds.
- Render preview MP4 separately where useful; never label an opaque MP4 as transparent.
- Inspect stills for missing glyphs, flashing frames, wrong clipping, skewed text, safe-zone violations and inaccurate logo/UI geometry.
- For a terminal insert, render real or clearly marked example commands and output, not fabricated terminal success logs masquerading as real operations.

## Deliverable

Composition source, identity/asset provenance, preview, editor-compatible output (if rendered), alpha verification, contact sheet and concise visual review report. Do not declare `final` merely because the render command exited successfully; inspect it.

## Native execution contract

Read [graphics mechanisms](references/graphics-mechanisms.md). Inputs: a narration beat, exact visible referent, authentic source assets, requested background and format. Outputs: composition source, evidence manifest, representative frames, rendered insert and review notes. Use [scripts/evidence.py](scripts/evidence.py) to hash source assets and candidate renders; a byte hash proves identity, not authenticity or approval. The default is a restrained warm-paper world; user style choices win. Integrate into `remotion-video` or export a separately verified alpha sequence.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.
