# Cartoon and template animation workflows

Use these six adopted workflows for original code-drawn cartoon scenes or self-contained animated inserts. Resolve `STUDIO` to this studio-toolkit skill directory, then `RUNTIME="$STUDIO/references/animation-runtime"`. In the portable ChatGPT package these paths are inside the one extracted studio-toolkit folder; specialist instructions live under references/specialists. Do not assume Claude slash commands, tools or home directories.

## Runtime and first use

Use the host's permitted filesystem/shell. Required: Python 3.10+, toolkit requirements (including Python Playwright), FFmpeg/ffprobe, Node/npm and Chromium. Check before installing:

```bash
python3 "$STUDIO/scripts/animation.py" doctor
bash "$RUNTIME/kit/setup.sh"
# If no compatible browser is available, install through Python Playwright:
python3 -m playwright install chromium
# Or export CHROMIUM to a compatible existing Chromium executable.
```

The kit uses pinned npm dependencies and npm ci. It does not install packages globally, buy speech or fetch models as a build side effect. Set npm_config_cache to a writable task cache if the host's usual npm cache is read-only. GSAP, Three.js and Playwright retain their own terms; font OFL notices are adjacent to the files. No paid API is needed for silent graphics or approved supplied narration. Offline Kokoro/Parakeet remain opt-in English calibration tools; setup-offline-voice.sh --download-models downloads about 1 GB and uses a kit-local venv. They are never a fallback for your ElevenLabs production preference.

ChatGPT must have code execution, filesystem access and these dependencies to actually render. In a host without them, produce the spec, code and runnable commands and mark rendering unverified. Attaching the archive as a chat reference is not persistent skill installation. No account import, plugin marketplace publication or live ElevenLabs generation is implied by this package.

## Four JSON-driven inserts

`animated-graph`, `minimalistic-graphics`, `map-route` and `exploded-view` use their linked spec reference. Example:

```bash
python3 "$STUDIO/scripts/animation.py" build animated-graph film.graph.json --snap 0.5,3.5
python3 "$STUDIO/scripts/animation.py" build animated-graph film.graph.json
```

Outputs: MP4, safe-area contact sheet, machine-readable media QA, and a generated .work folder with editable HTML/local assets. Snapshots go to a sibling .snaps directory. Defaults are 1080×1920, 30 fps, about four seconds; hold adds 0–60 seconds. Output paths resolve relative to the spec. Unknown/invalid fields fail. Existing media is retained unless --replace is explicit; a replacement is published only after encoding/decoding succeeds.

Copy a template beside the spec and set `template` to its relative path to change geometry. Keep the JSON field names, paused timeline/seek contract and readiness signal. Do not edit installed source to change a project. These templates are vertical inserts; other aspect ratios need an authored layout revision or the existing motion-design/Remotion workflows. Resizing a vertical render is not a landscape composition.

A graph uses supplied data, not invented growth. Map scenery is seeded illustrative geography, not geocoding, real routing or live travel-time data. The exploded-view default is a generic six-layer phone, not measured CAD, device-specific specifications or an anatomy model. Consult Anatomy for crafted scientific/mechanism structures; cartoon characters supplement those explanations.

## Two cartoon engines

```bash
python3 "$STUDIO/scripts/animation.py" init stick-figure PROJECT/animation
# Or:
python3 "$STUDIO/scripts/animation.py" init cartoon-animation PROJECT/animation
```

The destination must be new. Default starters are original four-second silent visual calibrations. Write the real script and edit the shots. `--example` instead copies the inherited pirate/armour worked example source without redistributing its voice; inherited claims and scripts require fresh factual review. The cartoon-animation alias replaces upstream zach-d-films; there is no endorsement or creator affiliation.

- Stick figures: web/lib.js has easing/keyframes, shapes, camera and deterministic random; chars.js has expressive faces, stick rigs, hats, arm IK; env.js has the bright cartoon environment and reusable props; main.js composes captions, grain and cut/whip transitions. shots.js defines `SHOTS` with start/end seconds and draw(ctx, localTime, absoluteTime). Extend props rather than replacing the rig with static icons. Preserve enough time for causal motion, expressions and the mechanism.
- 3D cartoons: src/human.js has poseable procedural people, clothing and armour; props.js has meshes, projectiles, sparks, morphs and a force-ripple shader. anim.js has easing/keyframes, camera, shake and two-bone IK. textures/materials produce the source's crafted surfaces. main.js handles lighting, sky, depth of field, bloom and color grade. src/shots.js exports SHOTS, FADES and DURATION; each build returns scene, camera, update(localTime). Captions come from src/caption-data.js. Native rendering remains 720×1280 with a verified Lanczos upscale to 1080×1920, not native 1080 detail.

Use a truthful hook, causally connected examples, a clear mechanism and an earned payoff. Most shots can last 2–4 seconds, with longer mechanism shots. Pacing follows the measured take rather than a mandated number of cuts. Keep faces/key props clear of captions and interface overlays. Impacts, camera motion and effects explain events; constant shake, whips or glow are not required. Prefer original visual direction and characters over a creator's name as a design instruction.

## Narration and timing handoff

Use the Studio script/production-config and the existing cached ElevenLabs helper described in [production preferences](production-preferences.md). New production speech needs ELEVENLABS_API_KEY plus an explicitly selected authorized voice. Never put credentials into a project or invoke an uncached second speech helper. Approved user recordings remain supported.

The helper produces candidate narration.mp3 and words.json with method/provider-measured word cues. Review speech, pronunciation and rights, then pass the measured files to the project-local engine:

```bash
python3 "$STUDIO/scripts/animation.py" sync PROJECT/animation \
  --audio CANDIDATE/narration.mp3 --words CANDIDATE/words.json \
  --method provider-unreviewed
```

For a supplied recording, use reviewed word cues (`manual-reviewed`) or explicitly unreviewed ASR (`asr-unreviewed`). `synthetic-test` is for calibration signals, not speech. Accepted input is Studio's `{method, segments:[{text,start_s,end_s}]}` or the upstream list `[{w,s,e,line?}]`. A cue is exactly one word. Sync validates order, finite times, script equality and actual decoded duration. It decodes to WAV without trimming silence, warping audio or shifting timestamps. It writes timing.json, audio/words_new.json and engine caption inputs. It does not edit the parent's approved narration.json, storyboard, timeline or captions.

When a script.json sentence list is populated, words must match it exactly. Copy the approved Studio scene narration into that list; punctuation/mixed-language terminology must match the spoken take. Retain upstream raw ASR artifacts when using the optional recognizer: its respelling/interpolation is an estimate, not forced alignment, and its English normalization is unsuitable for Arabic. Never use that estimated output as provider timing.

For the stick engine only, --reference measured-old.words.json builds strictly increasing old→new anchors if the words match exactly. Review the resulting poses and SFX; a changed script needs authored retiming. Each audio/words import requires --replace when timing/audio already exists. Protect manual engine caption edits in version control before an intentional replacement. The 3D engine requires authored shot retiming; it does not claim automatic 3D take warping.

Times in these engines are seconds derived from measured narration. Convert to the parent's integer frame clock with Studio's half-up rule; keep semantic scene/target IDs in storyboard.json/timeline.json. After retiming, update those artifacts and revalidate. Do not independently estimate caption, SFX and scene clocks.

## Render and review

```bash
python3 "$STUDIO/scripts/animation.py" render PROJECT/animation \
  --snap 0.5,2.5 --out PROJECT/qa/animation-stills
python3 "$STUDIO/scripts/animation.py" render PROJECT/animation \
  --out PROJECT/render/cartoon.mp4
```

The imported audio/vo.wav is included automatically. `--audio` can instead use an explicitly mixed track. A full-length render rejects narration that exceeds authored shots; retime the edit rather than truncating voice. `--duration` renders a shorter authored visual test, and must not cut a supplied audio track. Pad an audio tail to the video clock and normalize to -16 LUFS/-1.5 dBTP. For a finished music/SFX mix use the toolkit mixer and listen; peak targeting is not a substitute for final loudness/listening QA.

The inherited stick audio.py retains procedural plucks, underscore, wave/impact/whip/chime effects and reference-time cue placement. Install its pinned optional packages with `python3 -m pip install -r "$RUNTIME/kit/requirements-audio.txt"`. It needs project-local numpy/scipy/soundfile and is a worked example, not a generic soundtrack for every topic. Edit its cues and scene-specific duration before running it; pass the resulting mixed WAV via --audio. The core kit's requirements and renderer do not need the optional ASR models or these audio extras.

Capture uses a loopback-only server, waits for fonts/readiness, fails on missing assets/JavaScript errors and blocks remote page requests. It checks out-of-order pixels before rendering. The numeric graph permits at most 32 changed antialiasing pixels with channel deltas up to 16/255; its actual delta and pass-with-svg-raster-tolerance state are reported explicitly. Other modes require exact pixels. It checks FFmpeg exit status, probes resolution/frame count/fps/duration/audio and fully decodes the result. QA JSON separates automated evidence from agent visual inspection and human approval. Inspect opening, peak action, transitions, key labels and final hold; use kit/anim.py sheet VIDEO SHEET for contact sheets. The red safe area is a conservative composition guide, not a guarantee against every platform's interface.

For Arabic use a real Arabic-capable font, direction-aware text and isolated scientific Latin runs. Noto Sans Arabic/OFL is included as a fallback; mixed Arabic/English captions still require actual frame review, line-length and pronunciation checks. Do not reverse Arabic strings. Exact source fonts/caption bands differ between the engines.

If browser/WebGL/asset capture fails, preserve stderr and identify the dependency; do not return a stale MP4 or claim success. Do not disable browser security as a recovery shortcut. If seeking is stateful, calculate poses from time and rerun representative out-of-order checks. If fonts change after frame one, preload them before capture. Supplied code and upstream limitations are recorded in the repository SOURCES.md.
