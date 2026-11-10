## Spec
```json
{
  "label": "Followers",
  "values": [1.2, 2.1, 3.4, 5, 9, 24, 51, 78, 100],
  "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
  "final": 100000,
  "prefix": "", "suffix": "", "decimals": 0,
  "dark": false
}
```
- **`values`**: 2 or more numbers, 0 or above. The highest one touches the top gridline.
- **`labels`** (optional): one per value, shown under the axis. More than 12 shows every other one.
- **`final`** (optional): the number the count lands on. The count is the value under the tip times `final / last value`, so you can give `values` in thousands and `final` in full. Leave it out to count in the units of `values`.
- **`prefix`**, **`suffix`**, **`decimals`**: `"$"`, `"%"`, `" kg"`, and so on. The number shrinks itself if it gets long.
- **`dark`**: white line on black.
- **`hold`** (optional): extra seconds to hold the last frame. **`out`** (optional): the output path.

## Taste
- One number, one line. The label is a plain noun ("Followers", "Monthly revenue"), not a slogan.
- No callouts, no "83x growth" chips and no marketing words on the graphic.
- Values that grow late (slow, then steep) make the best curve, but show the real shape.


Common additions: language en|ar, direction ltr|rtl|auto; hold is finite 0–60 seconds. Output is vertical 1080×1920/30 fps. Review the shared workflow for real limitations and rendering checks.
