## Spec
```json
{
  "destination": "Iron Yard Gym", "minutes": 9, "distance": 2.8, "unit": "km",
  "places": ["North Quay", "Botanic Gardens", "Market Hall", "Elm Park", "The Canal"],
  "accent": "#2f7cf6", "seed": 7
}
```
- **`destination`**, **`minutes`**, **`distance`**: required. **`unit`**: `"km"` or `"mi"`.
- **`places`**: 5 small grey labels at fixed spots on the map. In order: near the start, a park at the far left, a block mid-route, a park at the far right, the river. Use names that fit the user's city, or `""` to hide one. They are decoration, not real geography.
- **`accent`**: the route, the moving dot and the ETA icon (hex). The pin stays red.
- **`seed`**: a different whole number gives a different arrangement of buildings and parks.
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## Changing the route
The route shape is fixed: up, right, up, right, ending at the pin. To change it, copy `"$RUNTIME/skills/map-route/template.html"` next to the spec, edit `WP` in the copy (`[x, z]` points; every corner must sit on a street, which run along multiples of 4; `x` from -36 to 36, `z` from -88 to 24, and north is negative `z`), and add `"template": "template.html"` to the spec. The camera's final pull-back target (`new THREE.Vector3(3, 0, -27)`) and the label spots (`LBL`) are tuned for the default route, so move them with it and check with `--snap`.

## Taste
- Short, real-sounding names. The destination card holds about 26 characters.
- Keep it calm: one route, one pin, no extra arrows or callouts.


Common additions: language en|ar, direction ltr|rtl|auto; hold is finite 0–60 seconds. Output is vertical 1080×1920/30 fps. Review the shared workflow for real limitations and rendering checks.
