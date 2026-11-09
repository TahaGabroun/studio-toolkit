# Remotion production

Pin all remotion/@remotion packages to the same exact version and retain package-lock.json. Use useCurrentFrame/useVideoConfig; no CSS animation, Date or unseeded randomness during capture. Convert cue seconds at ingestion, then use frame events everywhere. Render footage with OffthreadVideo, images with Img, local assets through staticFile. Wait for local fonts, and avoid on-demand font downloads during rendering.

A composition's duration/size/FPS comes from project.json. Use timeline scene intervals for sequence boundaries. For narration synchronization highlight an exact semantic target during its cue; captions follow measured segments. Do not claim estimated text timings are forced alignment. Use proper Arabic font shaping and LTR isolation for CO₂, scientific abbreviations and numbers.

```bash
npm ci
npm run typecheck
npx remotion still src/index.ts Main out/style.png --frame 30
npx remotion render src/index.ts Main out/master.mp4 --codec h264 --crf 18
```

CHROMIUM/--browser-executable can point to a local compatible browser. If rendering fails preserve source and report actual stderr. Use a cached render only when source, props, media and lockfile hashes match. A changed narration file invalidates timing and the render even if its filename is unchanged.

The component patterns preserve useful upstream JSX. Adapt their default mandatory mesh/grain/glow/Ken Burns advice to purpose: those effects are not required on scientific diagrams or text. Verify actual crop and resolution with ffprobe; duration checks must fail rather than print only a warning. Alpha delivery requires a PNG RGBA sequence or a tested alpha codec and contrasting-background composites, never opaque H.264 called transparent. Remotion has its own license; the toolkit's MIT license does not replace it. Check current eligibility at https://www.remotion.dev/docs/license.
