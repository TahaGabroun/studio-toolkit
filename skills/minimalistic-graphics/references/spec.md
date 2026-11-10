## Spec
```json
{"lines": ["every step feels small.", "until you look back."], "steps": 5, "light": false}
```
- **`lines`**: 1 or 2 lines. Line two appears when the dot reaches the top.
- **`steps`**: 3 to 7. More steps hop faster, and the video gets a little longer (3.8 s with 5 steps).
- **`light`**: black lines on white.
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## Taste
- Quiet and plain. Lowercase, no emojis, no bold, no exclamation marks.
- The idea should be about steady progress (habits, compounding, patience), because the picture is a dot climbing steps.
- For another motif (a maze, a line that wanders, a circle that fills), copy `$RUNTIME/skills/minimalistic-graphics/template.html` and change the shapes. Keep the rules: pure black, hairline white strokes, one solid white dot, one line of text.


Common additions: language en|ar, direction ltr|rtl|auto; hold is finite 0–60 seconds. Output is vertical 1080×1920/30 fps. Review the shared workflow for real limitations and rendering checks.
