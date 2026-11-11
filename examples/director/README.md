# Planning cases

Use these as interpreted requirement examples, not automatic creative approval. Initialize a project with its actual format/runtime/language, then run:

```bash
.venv/bin/python scripts/studio.py plan PROJECT --requirements examples/director/scientific.json
.venv/bin/python scripts/studio.py next PROJECT
```

scientific.json routes structural design through Anatomy and uses real narration/cue review. cartoon.json keeps the requested 3D character style but requires a native-resolution/layout proof because upscale is not permitted. Neither case calls an API. Fill real claims, scenes and assumptions from the user's brief rather than copying the example text as facts.

The executable landscape insert is `examples/run_director_example.py`:

```bash
.venv/bin/python examples/run_director_example.py --output /tmp/directed-film --phase prepare
# Inspect the brief/data and record an actual content review with studio.py review.
.venv/bin/python examples/run_director_example.py --output /tmp/directed-film --phase proof
# Inspect style-frame.png, mobile-preview.png and motion-test.mp4; record the real look review.
.venv/bin/python examples/run_director_example.py --output /tmp/directed-film --phase finish
# Inspect encoded QA and final media, then record finish/delivery reviews.
```

The script never supplies passing observations for you. It refuses proof/finish when earlier reviews are not current. For this four-second insert the approved full-length visual proof can be reused as the master without rendering identical frames again. Its data are explicitly calibration samples, and its intentional silence does not imply a production voice. Set CHROMIUM to an existing compatible browser when needed.
