## The engine
| File | What |
|---|---|
| `src/shots.js` | **The edit.** `FADES` (dips to black), `DURATION`, one function per shot and the `SHOTS` list (`{start, end, build}`). A shot's `build({makeStage})` returns `{scene, camera, update(t)}`; `update` gets time inside the shot and may return `{dof, bloom, exposure}`. |
| `src/human.js` | `makeHuman(outfit)`: a poseable cartoon person (`'vest'`, `'chainmail'`, `'plate'`, `'knight'`, `'archer'`). `setPose({joint: [x, y, z]})` for `pelvis spine chest neck head lSh lEl lWr rSh rEl rWr lHip lKn lAn rHip rKn rAn` (+ `drop`), `setMouth(0..1)`, `lerpPose(a, b, t)`, `standArmor(kind)`. |
| `src/props.js` | `pistol`, `gunArm`, `bullet` (with a flatten morph), `sword`, `shield`, `mace`, `arrow`, `bow`, `stand`, `glowSprite`, `sparks`, `streak`, `rippleOverlay` (the red force ripple). |
| `src/anim.js` | `kf` keyframes, easings, `range`, `cam(fov)`, `place(camera, pos, look)`, `shake`, `ikArm` (2-bone arm IK so hands can grab things). |
| `src/textures.js`, `src/materials.js` | Canvas-made steel scratches, chain-mail rings, wood, fabric, skin, and the materials built on them. |
| `src/main.js` | Renderer, sky, lighting, depth of field, bloom, grade, and `window.renderAt(t)`; imported captions live in src/caption-data.js. |


Write SHOTS with half-open start/end seconds and a DURATION matching the measured narration and final hold. update(localTime) must be pure in time. The retained archer-release example recomputes its launch pose for each post-release seek. Read procedural props for actual geometry; do not imply a physical simulation or scientific accuracy from an effect shader. Bokeh/bloom, camera shake, ripples and slow motion are optional explanations, not mandatory decoration. Native capture is 720×1280 and is upscaled to 1080×1920.
