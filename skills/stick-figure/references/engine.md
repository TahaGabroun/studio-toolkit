# Stick engine controls

web/lib.js: `kf(t, [[time,value,easing?],...])`, ease functions, seeded rng, shape/text primitives, camera and shake. web/chars.js: drawStick(ctx, options), expressive faces, pose/limbs, arm IK, hats and eye patches. web/env.js: sky/clouds/sea/ships/deck/barrels/cannon/lantern and reusable props. Add new props in a project file and include it from web/index.html.

web/shots.js defines SHOTS entries `{start,end,tr,draw(ctx,localTime,absoluteTime)}`; tr is cut or whip. The compositor renders at integer 30 fps, handles caption timing and optional old→new take warps. A changed script invalidates the old reference; exact word matching is required before warping. Inspect timing and transitions rather than assuming a new voice preserves performance.

The inherited audio.py retains procedural music and whoosh/thud/clang/pluck/chime/pop/boing/tweet/riser/wave/heartbeat/scribble synthesis. Its cue placement was authored for the inherited pirate example. Install numpy/scipy/soundfile locally only if using it, rewrite its cues for your script, and measure/listen to the final mix. The shared renderer accepts the chosen mixed track with --audio.

Captions use short groups, Poppins with an Arabic fallback and measured word times. Case, punctuation, chunk length and typography are design decisions: retain scientific terms and readable Arabic/Latin runs rather than mechanically lowercasing every language. The default caption band is around y=1250–1420 on a 1080×1920 canvas; check every face/prop overlap.
