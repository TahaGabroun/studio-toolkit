# Anatomy and ElevenLabs workflow update — 2026-11-10

The supplied Anatomy skill is the preferred construction system for biological/anatomical diagrams, crafted technical cutaways and mechanism explainers. It is retained under integrations/anatomy with its original drawing kit, examples, references and MIT notice. Installation can include it with `bash install.sh install --global --with-anatomy`; the nine canonical Studio skills retain their IDs. New production narration uses ElevenLabs with an explicitly selected voice and real provider timing data.

New projects persist these preferences in production-config.json. Diagram preflight checks actual skill metadata and uses the supplied pinned distribution by default. Explicit project paths remain available. Motion specialists and the orchestrator read the shared production preferences. For biological work, the supplied skill's legacy cell schematic is not a recommended geometry template; its biological-figures and gallery-quality guidance controls the new design.

The ElevenLabs helper uses continuous script narration, an environment-held key, an explicit voice, the official timestamp endpoint, validated MP3 bytes and measured original-text character alignment. It creates review candidates rather than replacing approved narration, captions or timelines. Completed responses are reused for unchanged text/voice/model/output format. Renaming semantic cues creates another candidate from the same audio; corrected response imports preserve cache history. No automatic billable retry is made.

## Executed checks

- 57 Python tests passed, including production preferences, dependency/credential preflight, installer lifecycle, Arabic/English cue mapping, cache reuse, corrected-import recovery, semantic cue renaming, duration boundaries and preservation of approved artifacts.
- 36 supplied Anatomy model/geometry tests passed across the process model, audit cache/order, profile, projection, sliding-clearance and taper checks. This is not a claim that every supplied browser or visual evaluation ran.
- The supplied archive's 127 files remain byte-identical in integrations/anatomy. Its MIT notice and pinned upstream provenance were preserved. Credential/private-path inspection found no matches in the supplied archive.
- Standalone package extraction, Anatomy discovery, preserved integration bytes and relative references passed independent forward testing. The package retains exactly one SKILL.md; Anatomy is a complete supporting guide with its original resources.
- The existing 4-second HTML production ran through rendering, audio mux, caption validation and media QA with the new preferences/checkpoint behavior. Existing demo regression tests passed with the updated toolkit.
- The supplied dial-indicator example built successfully in an isolated workspace. Its own browser capture helper was blocked by this host's Chrome SUID sandbox configuration. That failure was retained; no browser-security bypass or claimed Anatomy browser pass was substituted. No new Anatomy illustration or full scientific visual approval is claimed by this setup update.

## Setup still required for live voice

No ElevenLabs plugin connection, ELEVENLABS_API_KEY or voice selection was available in this session. The provider integration was tested with stubbed HTTP and locally generated MP3 fixtures; no live ElevenLabs speech request was sent or charged. Configure the account key in the environment and choose an authorized voice before production synthesis. Listening, pronunciation, anatomy and final creative approval still apply to each future production.

See the production-preferences reference for commands and the exact candidate/timing handoff. GitHub Actions results are verified separately after pushing the update.
