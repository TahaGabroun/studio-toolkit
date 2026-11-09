# Accuracy: claims, models, and images

Use this before geometry. A physical-looking object can communicate a false relationship more persuasively than a caption can correct it.

## Record what each important value means

For facts that determine geometry, motion, or a numeric readout, keep a short ledger in task notes:

| Claim or parameter | Kind | Evidence | Implementation consequence |
|---|---|---|---|
| Bucket capacity = 20 | User specification | Current request | Occupancy cannot exceed 20 |
| Refill = 5 tokens/s | User specification | Current request | Refill law uses simulated seconds |
| Gear ratio | Derived | Explicit tooth counts and meshing arrangement | Angles and velocities stay coupled |
| Carrier travel takes 3 seconds | Presentation choice | None; illustrative timing | Label as schematic, not measured kinetics |

Kinds are user parameter, sourced fact, derived quantity, or illustrative choice. Cite the actual page, section, equation, or figure inspected; never manufacture references. Use relevant primary research, standards, official technical documentation, or authoritative subject references. Browse for unfamiliar, time-sensitive, or consequential claims when tools permit. If evidence is unavailable, omit unsupported precision or identify the uncertainty and limit the depiction. User-selected hypothetical values remain hypothetical.

A source for one relationship does not validate an entire simulation. Match operating conditions, organism/cell type, scale, and date when relevant. Name a model schematic, qualitative, or quantitative according to what it actually implements. A more realistic shader does not make its physics more accurate.

## Keep three layers distinct

1. **Domain model:** values, relationships, conserved quantities, events, valid states.
2. **Presentation mapping:** drawing scale, exaggeration, cutaways, eased camera, symbolic colours, teaching time.
3. **Rendering:** projected paths, masks, shading, DOM and shader updates.

All renderers and readouts consume one model snapshot. If a gauge intentionally lags, label the measured/displayed quantity and derive both needle and its readout from that sensor model. Never infer pressure, temperature, flow, or energy from a decorative slider without a defensible mapping. Prefer a named qualitative state over invented numbers. Use uncertainty and significant figures consistent with the evidence.

## Test the lesson, not only its code

Select invariants that can catch a convincing but wrong output. Examples:

- Token bucket: `0 <= tokens <= capacity`; each accepted request consumes its defined cost; rejected requests consume none; overflow refill is discarded. State whether tokens refill continuously or in discrete increments.
- Connection pool: available + borrowed = configured capacity, and no connection has two simultaneous owners; queued work starts only when capacity exists.
- Cache: elapsed time and TTL have the same unit; define behavior exactly at expiry; a hit doesn't contact the origin in the stated model.
- Gears: engaged external gears rotate oppositely and satisfy the tooth-count ratio; do not independently ease their angles.
- Transport: preserve cargo identity, correct compartments, and entry/exit events. Schematic enlargement must not imply a new pathway or crossing through intact barriers.

Test extrema, threshold minus/at/plus epsilon, empty/full states, reset, and representative intermediate states. Use independent expected values or conservation relationships rather than reproducing the implementation in the test. Seed randomness when comparisons require reproducibility.

For state transitions, compare the left/right limits of position, orientation, visibility, identity, and attachment. Intentional discontinuities need a domain event or a clearly identified educational cut. Check scientifically significant relationships in rendered stills as well as in model assertions: a point can pass a numeric range test while visually lying outside the intended lumen.

## Geometry audit boundaries

Bundled audits inspect recorded shapes and selected poses using numerical tolerances. State what was sampled. Zero reported problems does not establish biological truth, complete containment, continuous collision freedom, or correctness of unrecorded markup. Keep contact exceptions explicit and physically justified. Increase local sampling around a detected narrow failure, instead of claiming a sparse sweep covers every possible interaction.

## Visible explanation

Place a brief caption under the figure stating what the mechanism shows and any consequential simplification (for example, not to scale or time compressed). Include a compact sources/details disclosure when useful. Keep engineering debug state out of the normal interface. Labels and units should help the audience understand the subject, not expose implementation details.
