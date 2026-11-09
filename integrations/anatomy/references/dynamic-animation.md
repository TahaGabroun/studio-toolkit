# Dynamic animation that explains

Read before implementing interactive output. Use `motion.md` for kit recipes; this document governs playback, timing, user control, and testing. The older examples demonstrate techniques, not mandatory tour behavior.

## Storyboard cause and consequence

Use the observed gallery patterns in `gallery-lessons.md`: coupled working parts, inspectable layers, localized material effects, and a result that changes the object. One input may legitimately drive many visible parts.

Specify the action, physical change, observable result, and useful resting pose. A sequence has observable transitions, not merely text swapped over a travelling dot. Use one main action and supporting motion that follows from it: a valve opens, flow changes, and a gauge responds. Use coupling equations or state dependencies rather than independent decorative loops.

For each phase, note moving parts, constraints, material identity, entry/exit events, and what stays continuous. Preserve attachments and topology: a carrier detaches only after budding and cargo enters a target only through a valid delivery event. Separate camera motion from object motion so one cannot disguise an incorrect trajectory.

Make timing legible. Short transitions may settle in roughly 150–400 ms; a teaching step often benefits from a longer dwell. These are presentation starting points, not physical constants. Show a speed control only when useful and label time scaling. Use overshoot only where it makes physical sense; a valve stop, count, or compartment boundary must not overshoot a hard limit.

## State ownership

Use explicit states suited to the mechanism, for example ready, playing, paused, complete, and reduced-motion inspection. Maintain current time/state, input targets, and render state separately.

| Event | Expected behavior |
|---|---|
| Play | Continue the current state; after completion, replay from the defined start |
| Pause | Freeze model time and effects without resetting selection or camera |
| Step or scrub | Stop playback, derive the requested state, synchronize all consequences |
| Reset | Clear pending events, accumulator, velocities, and transient effects consistently |
| Direct input during demo | Take ownership from the state currently visible; stop the tour |
| Hidden/offscreen | Suspend work and reset the frame timestamp; preserve the user's play/pause intention |
| Reduced motion enabled | Stop continuous playback and camera travel; expose meaningful static steps |
| Reduced motion disabled | Remain still until the user plays again if motion was stopped explicitly |

An idle demo is optional. If used, provide a visible pause control, stop it on deliberate interaction, and never resume while a control has focus or after the user explicitly paused. Do not make hover the only way to operate a mechanism. Respect touch scrolling and pointer cancellation. Never capture global arrow/space keys while the user is editing a native control.

## Two clocks, one truth

Measure elapsed foreground time from `requestAnimationFrame` timestamps. Do not advance by a constant per frame.

- For a pure timeline, evaluate `stateAt(simTime)` with time advancing by elapsed time × selected speed. Seeking backward evaluates the same function, rather than attempting to undo side effects. Random effects should be seeded or derived deterministically from time.
- For a numerical simulation, accumulate elapsed simulation time and integrate with a fixed stable step; render an interpolated state if needed. Bound catch-up work to prevent a stalled frame spiralling. Document any deliberate time dilation or discarded backlog.
- UI easing may clamp its integration delta for stability. Do not also clamp the domain clock to 1/30 s and advertise real-second rates: at 15 fps that would run at half speed. Hidden educational simulations normally pause; actual wall-clock simulations recompute elapsed time explicitly.
- Use one controller/RAF owner for a figure. Update the model once, then SVG, shaders, visible readout, and semantic phase from that snapshot. Display easing cannot change domain truth.

For circular motion, retain unwrapped angles through multiple turns and wrap only for a readout. For path motion, use world-space paths and arc-length parametrization when constant speed is the lesson. A uniformly changing Bézier parameter does not imply uniform physical speed.

## Rendering and lifecycle

Precompute static paths, cache element refs, and write only changed attributes. Rebuild only deforming shapes. Re-sort moving depth only when required, and mutate DOM order only when the order changes. Avoid per-frame layout reads and React renders. Keep a stable-size readout with tabular numbers where appropriate; throttle text updates independently of the physical state.

Fit the camera to the full motion envelope or use a deliberate focus transition. A zoom must not change the semantic selection or restart the process. Keep model-to-SVG and model-to-shader coordinates registered during resize and device pixel ratio changes.

Stop RAF, observers, timers, event listeners, and WebGL resources on teardown. Cancel pending callbacks on reset when they could replay old events. Handle context loss with an intelligible static fallback, and restore effects only from current state. A fallback should communicate the phenomenon, not simply erase it (for example, a static flame and the current flame-state label).

Measure representative busy transitions on desktop and a narrow viewport, recording device/browser, throttling, duration, and frame-time distribution. A 60 fps target allows about 16.7 ms total per frame; a 30 fps target about 33.3 ms. Reduce effect resolution, particle density, or decorative detail before dropping semantic steps. Claim achieved performance only when measured.

## Motion verification

Inspect start, middle, end, and just before/after every phase boundary. Check both opening/closing and interrupted reversals. A slowed contact sheet helps find visual pops but does not establish real-time performance or actual timestamp spacing.

Test pause/resume in every phase, reset mid-event, rapid repeated input, backward seek when supported, input during a tour, hide/show, resize, pointer cancel, and reduced-motion changes at runtime. Under reduced motion every meaningful state must remain reachable without waiting through animation. Paused means shader time, particles, CSS animations, and secondary mechanisms also stop.

Compare trajectories/readouts at equal simulation times using 30, 60, and 120 Hz timestamp schedules plus a slower schedule and a dropped-frame case. Position and domain outcomes should agree within a justified tolerance; integration methods may have bounded numerical differences. Check boundary position and velocity where continuity is intended, and exact discrete state at thresholds. Do not hide physical discontinuities with an opacity fade.

## Depth is part of the behavior

A static SVG can have correct painter order while its animation is wrong. Define motion slots relative to actual assemblies, not one final overlay for every moving part. A carried object may need splitting, clipping, re-sorting, or a dedicated sectional view to respect a compartment or housing. Check the crossing frame as well as the start/end poses. A selection glow or an opacity fade does not correct an impossible intersection.

For objects rotating within a fixed plane, project the rotated world geometry or use a correct plane transform. A screen-space CSS rotation distorts an oblique gear, dial, or blade. Use the 3D runtime when the surface normals and visible faces must change; reserve CSS transforms for operations that preserve the intended projection.
