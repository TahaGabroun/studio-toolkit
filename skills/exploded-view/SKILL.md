---
name: exploded-view
description: Create labelled 3D exploded-view inserts from a layered phone template or authored geometry. Use for device teardowns and technical layer reveals.
---

# Exploded view animation

Read [spec and template controls](references/spec.md) and the shared [animation workflow](../studio-toolkit/references/animation-workflows.md) before building. Resolve STUDIO to the actual studio-toolkit sibling skill, or the extracted package root, and RUNTIME to STUDIO/references/animation-runtime.

1. Obtain the actual text/data/labels needed by the linked spec. Preserve evidence and mark estimates/illustration explicitly.
2. Write a project-local JSON spec. For geometry changes copy its runtime template into the project; installed source stays reusable.
3. Run `python3 "$STUDIO/scripts/animation.py" build exploded-view SPEC.json --snap 0.5,3.5`; inspect the composition, then run without --snap for the MP4 and safe-area sheet. A shorter minimal motif may need earlier snapshot times.
4. Inspect labels, final state and transition frames; report actual output dimensions/duration, automated QA and creative-review status. Invalid specs, missing assets, browser errors and failed media checks block a success claim.

Inputs are the linked spec and optional authored template; outputs are editable HTML/assets, snapshots, MP4, contact sheet and QA JSON. Defaults and error recovery are in the shared workflow. Use studio-toolkit for full research/script/narration/publishing, and motion-design or Remotion for longer edits and other aspect ratios. New narration uses ElevenLabs. Scientific/mechanism geometry uses Anatomy where appropriate.
