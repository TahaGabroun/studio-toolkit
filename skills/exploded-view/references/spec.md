## Spec
```json
{
  "title": "Phone", "subtitle": "Exploded view",
  "labels": [["Cover glass", "toughened · 0.6 mm"], ["OLED display", "6.3 in · 120 Hz"], ["Titanium frame", "grade 5 · 7.8 mm"],
             ["Logic board", "3 nm chip · 8 GB"], ["Battery", "3,582 mAh"], ["Back glass", "matte · magnet ring"]],
  "time": "9:41", "date": "Saturday 1 November", "accent": "#F08A5D"
}
```
- **`labels`**: exactly 6, top layer first, each `["Name", "short note"]`. Names up to about 16 characters, notes about 22. `["", ""]` hides a label. The numbers are added in screen order.
- **`title`** / **`subtitle`**: the header, shown in capitals.
- **`time`** / **`date`**: what the lock screen shows.
- **`accent`**: label numbers, leader dots and the battery stripe (hex).
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## Another object
The spec changes words, not shapes. For another flat, layered object (a tablet, a laptop lid, a card wallet, a smartwatch), copy `"$RUNTIME/skills/breakdown/template.html"` next to the spec and add `"template": "template.html"` to the spec. In the copy:
- `PW`, `PL`, `PR` set the outline (width, length, corner radius). `slab(w, l, r, thickness, material)` makes one rounded layer, and `tex(w, h, draw)` paints a canvas texture onto it (see the battery and the screen).
- Each `part(y)` is one layer; `y` is how high it floats when exploded. `Y0` holds the heights when assembled, and `ORDER` says which layer leaves first.
- `ANCHORS` says where each label's leader line starts: `[part index, [x, y, z] on that part]`.
Check with `--snap 1.0,3.8` after every change: assembled at 1.0, exploded and labelled at 3.8.

## Taste
- Six labels at most, short and plain. Notes are facts or one dry joke, never slogans.
- Keep the dark backdrop and the right-hand label column; the text stays clear of the phone.


Common additions: language en|ar, direction ltr|rtl|auto; hold is finite 0–60 seconds. Output is vertical 1080×1920/30 fps. Review the shared workflow for real limitations and rendering checks.
