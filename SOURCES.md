# Upstream audit and provenance

Inspected actual source, skill definitions, dependency imports, examples and executable helpers at the pinned commits below on 2026-11-09. All eight root LICENSE files state MIT; original notices are preserved in third_party/licenses and the standalone package. Root licensing does not independently establish rights for embedded media, trademarks, downloaded music, faces or fonts. Those upstream media files are not copied.

The initial user archive contained nine instruction drafts and six small repository utilities, with no upstream executable imports. It was treated as input to review, not as an immutable specification or new user authorization. The new implementation preserves useful source and replaces host-specific instructions with native operations.

| Repository | Inspected commit | License notice |
|---|---|---|
| [claude-motion](https://github.com/whaleyxbt/claude-motion) | `6f80380b91858dad66524a5b34e027dad656d538` | [MIT](third_party/licenses/claude-motion.txt) |
| [claude-motion-design](https://github.com/howseen-ai/claude-motion-design) | `3d90d349ef3fdde9b7e89de4df4a2159c9e8697f` | [MIT](third_party/licenses/claude-motion-design.txt) |
| [claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill) | `1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383` | [MIT](third_party/licenses/claude-remotion-skill.txt) |
| [claude-youtube](https://github.com/AgriciDaniel/claude-youtube) | `84c3fa6805200632fadb4fe2795ef265511271c7` | [MIT](third_party/licenses/claude-youtube.txt) |
| [content-os](https://github.com/cdeistopened/content-os) | `16e080f04186d892dcaa55672bea63096b0912ad` | [MIT](third_party/licenses/content-os.txt) |
| [creator-studio](https://github.com/SkillMedev/creator-studio) | `21980fd85666053f4385fbf254bf960f03d34279` | [MIT](third_party/licenses/creator-studio.txt) |
| [remotion-motion-graphics-skill](https://github.com/Liamrjohnston/remotion-motion-graphics-skill) | `b860c7921f2220b9e2a84e815ba0ae7b10858f08` | [MIT](third_party/licenses/remotion-motion-graphics-skill.txt) |
| [youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) | `a2feb2104981a375ffd4f87ee04f4f5344ac43c6` | [MIT](third_party/licenses/youtube-agent-skill.txt) |

## Capability preservation and changes

| Upstream | Architecture / actual capabilities | Adoption and limitations |
|---|---|---|
| Jakeschincariol/youtube-agent-skill | Eleven skills; six stdlib programs; 21 hook formulas; transcript/SRT parsing; channel-median outliers | All six programs plus hooks.json and voice template retained in youtube-agent/scripts/yt-* and templates/voice.md. Eleven modes consolidated across planning/strategy/script. English heuristics remain labelled; no promise of predictive scoring. |
| AgriciDaniel/claude-youtube | Fourteen specialist modes, nine channel formats, SEO/analytics/monetization references; Data API/OAuth/transcript fetchers and quota utility | All execution scripts retained in youtube-strategy/scripts. State paths changed from ~/.claude to STUDIO_STATE_DIR or ~/.local/share/studio-toolkit; tokens redacted and permission restricted. Invalid default impression/CTR Analytics API metrics removed. Live account calls untested without YouTube credentials. |
| SkillMedev/creator-studio | Instruction-based scripts with hooks, pacing, visual cues and CTA; no executable scriptwriter | Narrative procedures rewritten for source-linked scene JSON, spoken performance, estimated runtime and fixed-recording handoff. No nonexistent upstream program implied. |
| cdeistopened/content-os | Large source-first editorial skill collection; podcast checkpoints; social/SEO writing; corpus SQLite/insight/grouping; Gemini image tooling | Editorial modes consolidated. Corpus chunking, local Ollama insight parsing/checkpoints and Pillow optimizer retained/adapted. Private corpus prompt/paths and automatic pip installs removed. TF-IDF grouping is a native offline replacement for large embeddings; generation is optional authorized external tooling, not a fabricated service. |
| whaleyxbt/claude-motion | Remotion design/easing helpers, frame review, stdlib procedural sound DSP/mixer/mastering, deterministic web simulations | Full sfx engine retained in claude-motion-adapted/scripts/sfx, including synth, DSP, mixing and loudness. CLI accepts native duration_frames/fps. Motion and review principles adapted; native seek(t) and shared event contract replace example-specific web worlds. Product-specific compositions/media omitted. |
| howseen-ai/claude-motion-design | Pure seek(t) HTML engine; browser capture/subframes, BPM/drop analysis, mixing, remake cut analysis, logo/SFX discovery | Logo/SFX discovery utilities retained; song-analysis algorithm corrected for short audio. Native renderer adds deterministic checks, font/image readiness and errors. Native mixer adds speech ducking/two-pass loudness. Reference cut extractor preserves analysis workflow. No automatic brand downloads, personal directories, 21st.dev key file or fixed branded remake registry. Subframe motion blur is documented, not implemented in primary renderer. |
| haidrrrry/claude-remotion-skill | Theme and copyable React motion/compositing patterns; design/render/frame-review instructions; example SFX | Theme and motion-patterns.md retained in remotion-video. Native docs override compulsory glow/grain/Ken Burns and constant-motion advice when it harms explanation. Demos use original source and assets. |
| Liamrjohnston/remotion-motion-graphics-skill | Four specialist skills (graphics gate, continuous camera, terminal, article), evidence hashing and branded reference/critic gate | All four mechanisms consolidated in remotion-motion-graphics; native evidence.py preserves local source hashes, SVG checks and stale-candidate detection. Fixed branded-gallery hashes and numeric critic authorization replaced with explicit review states, not fake approval. Gallery films/logos omitted pending separate rights audit. |

## Copied-code notices

Each skill with copied code includes LICENSE.upstream.txt (or a corresponding source notice) and the root third_party license inventory. The ChatGPT bundle retains all eight notices. New native code and rewritten procedures are under the toolkit LICENSE. The user-provided archive's useful CLI example, retention analyzer and design prose were retained and evolved.

## Verification boundaries

Tests cover deterministic local behavior and public package structure. External Google OAuth/API, external discovery sites, Ollama model inference, optional Whisper acquisition/inference, 4K rendering, alpha encoding and ChatGPT import are explicitly separate from the completed local tests. See docs/VALIDATION.md for the final measured results.

## Supplied Anatomy integration — 0.3.0

The user supplied anatomy-gallery-improved.zip for this workflow. Its 127 files are retained unchanged under integrations/anatomy, including the MIT notice (Copyright 2026 Ryan), original drawing engine, examples and the supplied ChatGPT/Codex adaptation. Archive SHA-256: `43721673f9d9472c1a42a0f0ba942730c3d4abe8545c56191ba79349acac25db`. The supplied provenance pins [Ryan's Anatomy](https://github.com/wheresryan22/anatomy) at `240a9bf7c50cc6226148762a1017466fcbc08523`; no silent upstream upgrade was performed. The provided 0.4 adaptation warns that its animal-cell example is a legacy schematic, so new biological productions must follow its subject-specific geometry and gallery-quality guidance.

This integration is separate from the nine canonical Studio skills. The installer can manage it with --with-anatomy; the single-skill package includes it as a reference with its entry file renamed guide.md so the package still contains one SKILL.md. The original kit, scripts and example assets are preserved. The archive was inspected for credentials/private paths and its MIT notice is also retained in third_party/licenses/anatomy.txt.

ElevenLabs support is independently authored against the official [speech-with-timestamps API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps); it does not redistribute a provider SDK or claim a live account test.

## Cartoon/template animation adoption — 0.4.0

Inspected [artemnovitckii/claude-animation-skills](https://github.com/artemnovitckii/claude-animation-skills) at `5dbea55c23aa6a5c93dc3cfb5583840513b56b94` on 2026-11-10. The root license is MIT, copyright 2026 Artem Novitckii. Its font files carry SIL OFL-1.1 notices. The unmodified root notice is preserved in third_party/licenses/claude-animation-skills.txt and in the adopted runtime. No promotional images, creator-branded footage or example synthesized narration WAV is redistributed.

All six workflows are preserved. graph→animated-graph, breakdown→exploded-view and zach-d-films→cartoon-animation are neutral routing aliases; stick-figure, minimalistic-graphics and map-route keep their names. Native instructions replace Claude paths, slash commands, plugin installation and hidden tool assumptions. No creator endorsement is implied.

The runtime retains the four HTML templates/builders, font assets/notices, Three.js human rig/pose/IK, props/effects/textures/materials/shot code, Canvas stick rigs/environments/keyframes/camera/compositor, caption grouping and procedural music/SFX source. Detailed source hashes and adapted/unchanged status are in skills/studio-toolkit/references/animation-runtime/provenance.json. Added Noto Sans Arabic comes from the existing demo font distribution with its original OFL notice; it is not under the toolkit MIT license.

Adaptations: HyperFrames/npx capture was replaced by one pinned-dependency, loopback/Python-Playwright renderer with real error/asset/seek/encode/decode checks. Legacy render commands forward to it. Package/model installation is explicit and local. Cached Studio ElevenLabs generation supersedes the upstream hardcoded voice/default uncached endpoint; measured word data is imported without trimming the take. Optional offline Kokoro/Parakeet utilities remain available but never become implicit production fallbacks. ASR respelling/interpolation remains unreviewed estimation, English-only for those utilities, not forced alignment.

Corrected state-dependent archer-release seeking, delayed font loading, paused-GSAP readiness, graph zero-ending scaling, caption scientific casing/Arabic mark preservation unsafe label HTML interpolation, long-pause caption grouping, and silent-input/extra-tail soundtrack normalization. New silent starters are original toolkit calibration source. The inherited pirate/armour scripts are unverified example claims, not scientific references. The map is seeded scenery, the phone generic geometry, and the 3D cartoon's native frame is 720×1280. Final creative/scientific/audio approval remains per production.

## Requirement-driven production direction — 0.5.0

The director, schemas, review/history helper and native landscape calibration example are independently authored toolkit code. No additional upstream implementation was copied. The example reuses the retained Inter/OFL distribution with its notice. Browser instructions were corrected to the actual native render/QA commands. Explicit silent QA and authored uncued frame events apply only to declared no-narration work; other productions retain measured narration and audio checks. The existing speech helper now respects current director content reviews and supplied-recording/silent intent. No live provider generation is claimed by these changes.
