# Quality bar from the Claude gallery

Read `gallery-lessons.md` for observed examples and the design/completion gates. Use this checklist during visual acceptance. Keep the original kit and its light palette; do not replace its material ramps with broad foreground/background mixes.

## Benchmarks

Treat gallery links as optional visual references. If access fails, use the bundled examples and state what was actually inspected. Do not delay a build indefinitely to fetch a benchmark.

Inspect the finished drawing and its response to input, not only the page description. These are public Anatomy creations credited to Claude by the author. Refer to `gallery-lessons.md` for what was actually inspected and the limits of those observations:

| Example | What to study | Transfer to a new subject |
| --- | --- | --- |
| [Watch movement](https://skills.wheresryan.sh/anatomy/collection/watch) | Layered bridges, recessed seats, gear teeth, clearances, soft shadows, a winding control, and an apart pose | Make internal structure legible at normal size; use small details that explain how the parts meet |
| [Turbofan](https://skills.wheresryan.sh/anatomy/collection/turbofan) | A removed quarter of the casing, different spool speeds, a thrust lever, and readouts coupled to the running engine | Reveal the working interior; make the input change a mechanism and its consequences together |
| [Binary search](https://skills.wheresryan.sh/anatomy/collection/binary-search) | A balance compares the sample to a middle weight; eliminated weights sink into seats | Put the reasoning in the object, so the outcome is visible before the caption is read |
| [Raptor engine](../examples/raptor-engine/raptor-engine-light.html) | Rounded profiles, pipe routing, registered effects, and an audited exploded view | Preserve surface continuity and occlusion at close range |

When available, consult the author's [making-of](https://skills.wheresryan.sh/anatomy/how-i-built-it) for the original failure-and-repair examples. Preserve the pinned local kit; gallery inspection is a design benchmark, not permission to silently upgrade dependencies or copy a finished object.

## Decide what the picture must prove

Before geometry, write four short answers in the task notes:

1. What real object or specimen should the reader recognise immediately?
2. What relationship must be visible without reading a paragraph?
3. What does the primary interaction physically change?
4. What does the same model update in the motion, selected state, and readout?

For an abstract concept, invent the physical mechanism. For a real engine, cell, molecule, or instrument, model its actual structure. Do not force a biological subject onto a machine base merely because the example has one. The legacy animal-cell example does not meet this target: do not copy its tray-like silhouette or global process overlay.

## Reject these outputs before polishing

- A large flat plate with objects distributed across it. Give the subject its actual enclosure, depth, internal boundaries, and asymmetry.
- A collection of recognisable icons without connected structure. Model how the parts meet and how material or information crosses their boundaries.
- A dropdown that changes a paragraph while the mechanism remains unchanged. Selection may locate a structure, but the explanatory interaction must also expose, move, deform, compare, or transport something meaningful.
- A bead that travels straight from one organelle or station to another. Model the change in the carrier and the source/target boundaries when those changes are the lesson.
- Darkening every face of the selected object. Preserve four-tone form; emphasise a relevant edge, local part, opening, or restrained light envelope.
- Thousands of paths offered as evidence of quality. Counts are not visual acceptance tests.
- Controls that require knowledge of hidden keyboard shortcuts. Provide a visible native equivalent and a concise hint; touch must work.
- A hero figure shrunk to a postage stamp to fit an inline limit. Use a complete standalone page and an appropriately scoped inline view or still.

## Review at three distances

**Normal size:** identify the subject, focal structure, and current action immediately. Keep outlines delicate, shade ramps close, contact shadows soft, and silhouettes clear. Leave space for the primary mechanism, not empty padding or a dashboard.

**Close-up:** inspect each selected subsystem, membrane or wall thickness, joints, openings, texture endings, and surface curvature. Add detail that distinguishes the real structure, not dots or grooves that merely occupy blank space.

**Phone:** preserve a useful overview and offer a native selection or focus control. Move the camera to a selected subsystem or show a larger detail when important features become too small. Do not solve a phone layout by reducing readable text or effective targets.

Compare a render directly with the closest benchmark. Name concrete faults in the task notes, fix them, and render again. Do not claim parity with Claude from a successful build, syntax check, path count, or unviewed image.

## Make interaction do explanatory work

Use one coherent explanatory mechanism per view; several coupled moving assemblies may be necessary. Couple the state to all visible consequences. For example:

- Pressure raises a plunger and moves its gauge needle.
- Winding changes the spring reserve and the watch keeps time from that reserve.
- A search comparison tips the balance and removes one half of the candidates.
- A cargo carrier buds, encloses cargo, travels, docks, and fuses; the compartment boundary changes with it.

Keep motion time-based. Use direct controls, an optional play/pause sequence when a process needs time, and stable resting poses under reduced motion. Stop offscreen. An idle tour can demonstrate the mechanism, but it must not compete with deliberate reading or selection.

Distinguish a schematic teaching sequence from measured physics or biological kinetics. Do not invent concentrations, throughput, ATP production, or rates to make the readout look active.

## Record what was actually verified

Keep build/logic checks, geometry checks, visual checks, and browser checks separate. A static renderer can inspect SVG art. A DOM adapter can inspect event-handler state transitions. Neither proves real browser layout, keyboard behavior, pointer hit testing, or WebGL.

If a browser is blocked, retain the failure and use the available static/geometry checks. Do not weaken the checks, bypass the restriction, or present that fallback as a complete browser pass. Keep the result useful and state the specific limitation.

## Professional finish

Use a consistent spacing and type scale, aligned control groups, concise sentence-case labels, and stable-width numeric readouts with units. Avoid fake interface text, redundant badges, and unexplained abbreviations. Use native controls with visible hover, focus, active and disabled states; retain readable contrast and generous touch targets (aim for about 44 CSS px where practical).

At 390 CSS px, inspect the actual visual footprint, not just the viewport setting: text must remain readable, controls wrap without clipping, and the mechanism keeps a usable focus view. Check browser zoom and long labels. Do not shrink the whole interface to fit a fixed card. A smooth surface, deliberate whitespace, or a simpler mechanism can be the professionally finished result.

Follow `accuracy.md` for claims and `dynamic-animation.md` for motion. Inspect requested themes and every additional theme actually shipped; do not expand a single-theme task solely to satisfy an old gallery convention.
