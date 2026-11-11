#!/usr/bin/env python3
"""Studio Toolkit: validated artifacts, shared frame timing and resumable stage records."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
FORMATS = {"landscape": (1920, 1080), "vertical": (1080, 1920), "square": (1080, 1080), "4k": (3840, 2160)}
STAGES = {
    "idea": ["brief.md", "project.json"], "research": ["research.md"],
    "strategy": ["strategy.md"], "script": ["script.md", "script.json"],
    "storyboard": ["storyboard.json"], "design": ["design.md"],
    "assets": ["assets.json"], "animation": ["animation.md"],
    "narration": ["narration.json", "timeline.json", "captions.srt"],
    "audio": ["mix.json", "render/mix.wav"], "render": ["render-config.json", "render/final.mp4"],
    "qa": ["qa/automated.json", "qa-report.md"], "publication": ["publication.md"],
}

def read(path):
    def reject_constant(value):
        raise ValueError(f"Non-finite JSON number: {value}")
    def finite_float(raw):
        value = float(raw)
        if not math.isfinite(value): raise ValueError(f"Non-finite JSON number: {raw}")
        return value
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=reject_constant, parse_float=finite_float)

def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temp.replace(path)

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()

def local(root, name):
    p = (Path(root) / name).resolve()
    if not p.is_relative_to(Path(root).resolve()): raise ValueError(f"Path escapes project: {name}")
    return p

def frame(seconds, fps):
    return int((Decimal(str(seconds)) * Decimal(str(fps))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)], text=True))

def schema_errors(name, value):
    from jsonschema import Draft202012Validator
    validator = Draft202012Validator(read(SKILL / "references/schemas" / f"{name}.schema.json"))
    return [f"{name}:{'/'.join(map(str, e.path))}: {e.message}" for e in sorted(validator.iter_errors(value), key=lambda e: str(e.path))]

def init(directory, title, fmt="landscape", fps=30, duration=30, language="en"):
    root = Path(directory)
    if root.exists(): raise ValueError(f"Refusing existing directory: {root}")
    if not math.isfinite(duration) or duration <= 0 or fps not in range(1, 121): raise ValueError("Invalid duration/FPS")
    w, h = FORMATS[fmt]
    root.mkdir(parents=True)
    for d in ["assets", "render", "qa"]: (root / d).mkdir()
    write(root / "project.json", {"schema_version": 1, "title": title, "language": language, "direction": "rtl" if language.startswith("ar") else "ltr", "width": w, "height": h, "fps": fps, "duration_frames": max(1, frame(duration, fps)), "engine": "unselected"})
    write(root / "state.json", {"version": 1, "stages": {}})
    write(root / "assets.json", {"assets": []})
    write(root / "production-config.json", read(SKILL / "references/production-defaults.json"))
    for name, text in {"brief.md": f"# {title}\n\nAudience, promise, deliverable, runtime, rights and success criterion.\n", "research.md": "# Claim ledger\n\nRecord claim, source URL, date checked, limitation, scene ID.\n", "strategy.md": "# Strategy\n\nAudience question, differentiated evidence, packaging and experiment.\n", "design.md": "# Visual treatment\n\nPalette, local fonts, hierarchy, safe area and exact focus targets.\n"}.items():
        (root / name).write_text(text, encoding="utf-8")
    return root

def script_report(data, fps):
    errors = schema_errors("script", data)
    scenes = data.get("scenes", [])
    ids = [s["id"] for s in scenes]
    if len(ids) != len(set(ids)): errors.append("Duplicate script scene IDs")
    if scenes and scenes[0]["role"] != "hook": errors.append("First scene must establish the hook")
    if scenes and scenes[-1]["role"] != "payoff": errors.append("Final scene must answer the promise")
    spoken = " ".join(s["narration"] for s in scenes)
    words = len(spoken.split())
    return {"errors": errors, "words": words, "estimated_seconds": [round(words / 160 * 60, 1), round(words / 130 * 60, 1)], "estimate_basis": "English 130–160 wpm; calibrate Arabic using actual recording", "scene_count": len(scenes)}

def validate(root):
    root = Path(root)
    errors, warnings = [], []
    objects = {}
    for name in ["project", "production-requirements", "production-plan", "production-config", "script", "storyboard", "timeline", "assets", "narration", "render-config", "mix"]:
        p = root / f"{name}.json"
        if not p.exists():
            if name == "project": errors.append("Missing project.json")
            elif name not in ["production-config", "production-requirements", "production-plan"]:
                intent=objects.get('production-requirements',{})
                no_voice=isinstance(intent,dict) and isinstance(intent.get('narration'),dict) and intent['narration'].get('mode')=='none'
                if not (no_voice and name in ['script','narration','mix']):warnings.append(f"Pending artifact: {p.name}")
            continue
        try:
            objects[name] = read(p)
            errors.extend(schema_errors(name, objects[name]))
        except (ValueError, TypeError) as e: errors.append(f"{p.name}: {e}")
    if errors: return {"errors": errors, "warnings": warnings}
    p = objects["project"]; fps, duration = p["fps"], p["duration_frames"]
    no_voice=objects.get('production-requirements',{}).get('narration',{}).get('mode')=='none'
    t = objects.get("timeline")
    narration = objects.get("narration")
    if no_voice and narration:errors.append('Project declares no narration but narration.json is present; reconcile the production intent and artifacts')
    cues = narration["segments"] if narration else []
    cue_map = {c["id"]: c for c in cues}
    if len(cue_map) != len(cues): errors.append("Duplicate narration cue IDs")
    previous = 0
    for c in cues:
        if c["start_s"] < previous or c["end_s"] <= c["start_s"]: errors.append(f"Cue {c['id']}: overlap/nonpositive interval")
        if frame(c["end_s"], fps) > duration: errors.append(f"Cue {c['id']}: exceeds project")
        previous = c["end_s"]
    if narration:
        if not (root / "captions.srt").is_file(): errors.append("Missing captions.srt for narrated project")
        elif (root / "captions.srt").read_text(encoding="utf-8") != srt(cues): errors.append("Captions differ from narration timestamps/text; regenerate")
        if narration["method"] == "asr-unreviewed": warnings.append("ASR timestamps and transcript require review; not forced alignment")
        if narration["method"] == "provider-unreviewed": warnings.append("Provider-generated speech timestamps require listening and semantic review")
        audio = local(root, narration["audio"])
        if not audio.is_file(): errors.append("Missing narration audio")
        elif digest(audio) != narration["audio_sha256"]: errors.append("Narration audio changed; realign timestamps")
        else:
            measured = float(probe(audio)["format"]["duration"])
            if cues and cues[-1]["end_s"] > measured + 1 / fps: errors.append("Narration cue exceeds audio duration")
            if measured > duration / fps + 1 / fps: errors.append("Narration longer than project; extend timeline")
    if t:
        if t["fps"] != fps or t["duration_frames"] != duration: errors.append("Timeline timebase differs from project")
        previous = 0; ids = set()
        for s in t["scenes"]:
            if s["id"] in ids: errors.append("Duplicate timeline scene ID")
            ids.add(s["id"])
            if s["start_frame"] != previous or s["end_frame"] <= s["start_frame"]: errors.append(f"Scene {s['id']}: gap, overlap or empty scene")
            previous = s["end_frame"]
        if previous != duration: errors.append("Timeline does not cover full project duration")
        targets = set()
        sb = objects.get("storyboard", {}).get("scenes", [])
        for s in sb: targets.update(s["targets"])
        if sb and [s["id"] for s in sb] != [s["id"] for s in t["scenes"]]: errors.append("Storyboard/timeline scene IDs differ")
        if "script" in objects and sb and [s["id"] for s in objects["script"]["scenes"]] != [s["id"] for s in sb]: errors.append("Script/storyboard scene IDs differ")
        event_ids = set()
        for e in t["events"]:
            if e["id"] in event_ids: errors.append("Duplicate event ID")
            event_ids.add(e["id"])
            if e["target"] not in targets: errors.append(f"Unknown visual target: {e['target']}")
            cue = cue_map.get(e.get("cue_id"))
            if not e.get('cue_id') and no_voice: pass  # Intentionally authored frame event, not invented speech alignment.
            elif not e.get('cue_id'):errors.append(f"Event {e['id']}: narration cue_id required unless no narration is declared")
            elif not cue: errors.append(f"Unknown narration cue: {e['cue_id']}")
            elif abs(e["start_frame"] - frame(cue["start_s"], fps)) > 1: errors.append(f"Event {e['id']}: not aligned to narration cue")
            elif abs(e["end_frame"] - frame(cue["end_s"], fps)) > 1: errors.append(f"Event {e['id']}: end not aligned to narration cue")
            if not (0 <= e["start_frame"] < e["end_frame"] <= duration): errors.append(f"Event {e['id']}: out of bounds")
    assets = objects.get("assets", {}).get("assets", [])
    asset_ids = set()
    for a in assets:
        if a["id"] in asset_ids: errors.append("Duplicate asset ID")
        asset_ids.add(a["id"])
        f = local(root, a["path"])
        if not f.is_file(): errors.append(f"Missing asset: {a['path']}")
        elif digest(f) != a["sha256"]: errors.append(f"Asset changed: {a['path']}")
        if a["license"].lower() in ["unknown", "pending"]: errors.append(f"Uncleared asset: {a['id']}")
    config = objects.get("render-config")
    if config and any(config[k] != p[k] for k in ["width", "height", "fps", "duration_frames"]): errors.append("Render configuration differs from project")
    if config:
        for source in config["source_files"]:
            if not local(root, source).is_file(): errors.append(f"Missing renderer source: {source}")
    mix = objects.get("mix")
    if mix:
        for track in mix["tracks"]:
            if not local(root, track["path"]).is_file(): errors.append(f"Missing audio track: {track['path']}")
            if track["start_frame"] >= duration: errors.append("Audio track begins after project")
    return {"errors": errors, "warnings": warnings}

def timestamp(s):
    ms = frame(s, 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"

def srt(cues):
    return "\n".join(f"{i}\n{timestamp(c['start_s'])} --> {timestamp(c['end_s'])}\n{c['text']}\n" for i, c in enumerate(cues, 1))

def align(root, audio, segments, method):
    """Import measured timestamps; never invent word alignment from script length."""
    root = Path(root); p = read(root / "project.json")
    if (root/'production-requirements.json').exists() and read(root/'production-requirements.json').get('narration',{}).get('mode')=='none':raise ValueError('Project declares no narration; update its intent and real cue mapping before importing a voice')
    audio = local(root, audio)
    data = read(segments); cues = data["segments"] if isinstance(data, dict) else data
    clean = [{"id": c.get("id", f"cue-{i+1}"), "start_s": c.get("start_s", c.get("start")), "end_s": c.get("end_s", c.get("end")), "text": c["text"].strip()} for i, c in enumerate(cues)]
    n = {"audio": str(audio.relative_to(root.resolve())), "audio_sha256": digest(audio), "method": method, "segments": clean}
    errors = schema_errors("narration", n)
    if errors: raise ValueError("; ".join(errors))
    by = {c["id"]: c for c in clean}
    if len(by) != len(clean): raise ValueError("Duplicate narration cue IDs")
    previous = 0; measured = float(probe(audio)["format"]["duration"])
    for cue in clean:
        if cue["start_s"] < previous or cue["end_s"] <= cue["start_s"] or cue["end_s"] > min(measured, p["duration_frames"] / p["fps"]) + .001: raise ValueError("Invalid/overlapping/out-of-bounds cue")
        previous = cue["end_s"]
    t = None
    if (root / "timeline.json").exists():
        t = read(root / "timeline.json")
        if schema_errors("timeline", t): raise ValueError("Invalid timeline schema")
        if t["fps"] != p["fps"] or t["duration_frames"] != p["duration_frames"]: raise ValueError("Timeline/project timebase mismatch")
        if any(not e.get('cue_id') for e in t['events']):raise ValueError('Assign real cue_ids to timeline events before importing measured narration')
        unknown = {e["cue_id"] for e in t["events"]} - set(by)
        if unknown: raise ValueError(f"Timeline references absent cue IDs: {sorted(unknown)}; update cue mappings before import")
        for e in t["events"]:
            c = by[e["cue_id"]]
            e["start_frame"], e["end_frame"] = frame(c["start_s"], p["fps"]), max(frame(c["start_s"], p["fps"])+1, frame(c["end_s"], p["fps"]))
    # Complete validation and cue resolution before modifying any approved artifact.
    write(root / "narration.json", n)
    (root / "captions.srt").write_text(srt(clean), encoding="utf-8")
    if t is not None:
        write(root / "timeline.json", t)

def fingerprints(root, stage):
    """Hash every upstream artifact and render input, including actual media bytes."""
    names = []
    for s, outputs in STAGES.items():
        names += outputs
        if s == stage: break
    # Production preferences affect visual planning onward, not approved research/writing.
    if (root / "production-config.json").is_file() and list(STAGES).index(stage) >= list(STAGES).index("storyboard"):
        names.append("production-config.json")
    if list(STAGES).index(stage) >= list(STAGES).index("assets"):
        names += [str(f.relative_to(root)) for f in (root / "assets").rglob("*") if f.is_file()]
    # Renderer source can live outside project: declared files only, no hidden discovery.
    config = root / "render-config.json"
    if config.exists() and list(STAGES).index(stage) >= list(STAGES).index("animation"):
        names += read(config).get("source_files", [])
    return {n: digest(local(root, n)) for n in sorted(set(names)) if local(root, n).is_file()}

def statuses(root):
    root = Path(root); state = read(root / "state.json"); result = {}; stale = False
    for stage, files in STAGES.items():
        record = state["stages"].get(stage)
        valid = record and all(local(root, f).is_file() for f in files) and record["hashes"] == fingerprints(root, stage)
        result[stage] = "complete" if valid and not stale else ("stale" if record else "pending")
        if not valid: stale = True
    return result

def complete(root, stage):
    root = Path(root); order = list(STAGES); status = statuses(root)
    for prior in order[:order.index(stage)]:
        if status[prior] != "complete": raise ValueError(f"Finish/revalidate {prior} first ({status[prior]})")
    missing = [n for n in STAGES[stage] if not local(root, n).is_file() or not local(root, n).stat().st_size]
    if missing: raise ValueError(f"Missing stage outputs: {missing}")
    result = validate(root)
    if result["errors"]: raise ValueError("; ".join(result["errors"]))
    if stage == "qa":
        report = read(root / "qa/automated.json")
        if report["status"] != "pass": raise ValueError("Automated QA failed")
        if report.get("video_sha256") != digest(root / "render/final.mp4"): raise ValueError("QA evidence belongs to a different video; rerun QA")
        if report.get("input_hashes") != fingerprints(root, "render"): raise ValueError("QA inputs changed; rerun QA")
    state = read(root / "state.json")
    state["stages"][stage] = {"completed_at": datetime.now(timezone.utc).isoformat(), "hashes": fingerprints(root, stage), "approval": "not implied by stage completion"}
    write(root / "state.json", state)

def doctor():
    import importlib.util
    return {"python": sys.version.split()[0], "executables": {x: shutil.which(x) for x in ["ffmpeg", "ffprobe", "node", "npm", "gh"]}, "python_packages": {x: bool(importlib.util.find_spec(x)) for x in ["yaml", "jsonschema", "PIL", "numpy", "playwright", "faster_whisper"]}}

def production_config(root):
    path = Path(root) / "production-config.json"
    config = read(path if path.exists() else SKILL / "references/production-defaults.json")
    errors = schema_errors("production-config", config)
    if errors: raise ValueError("; ".join(errors))
    return config

def workflow_check(root, anatomical=False, generate_narration=False):
    """Check selected production dependencies without a model call or secret disclosure."""
    import os
    config = production_config(root); diagram = config["diagrams"]; voice = config["narration"]
    candidates = []
    if diagram["skill_path"]:
        explicit = Path(diagram["skill_path"]).expanduser()
        if not explicit.is_absolute(): explicit = Path(root) / explicit
        candidates.append(explicit if explicit.name == "SKILL.md" else explicit / "SKILL.md")
    else:
        # Prefer the user's pinned, bundled Anatomy distribution over a different global revision.
        candidates += [SKILL.parents[1] / "integrations" / diagram["preferred_skill"] / "SKILL.md", SKILL / "references/integrations" / diagram["preferred_skill"] / "guide.md"]
        roots = [Path(root) / ".agents/skills", Path(root) / ".codex/skills"]
        roots += [p / ".agents/skills" for p in Path(root).resolve().parents]
        roots += [Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills", Path.home() / ".agents/skills"]
        candidates += [p / diagram["preferred_skill"] / "SKILL.md" for p in roots]
    import yaml
    available = None; invalid = []
    for candidate in candidates:
        if not candidate.is_file(): continue
        try:
            text = candidate.read_text(encoding="utf-8")
            if not text.startswith("---\n") or "\n---\n" not in text[4:]: raise ValueError("frontmatter missing")
            meta = yaml.safe_load(text.split("---", 2)[1])
            if not isinstance(meta, dict) or meta.get("name") != diagram["preferred_skill"] or not isinstance(meta.get("description"), str) or not meta["description"].strip():
                raise ValueError("name/description metadata mismatch")
            available = candidate.resolve(); break
        except (OSError, ValueError, yaml.YAMLError): invalid.append(str(candidate))
    errors = []
    if anatomical and diagram["required_for_diagram_scenes"] and available is None:
        errors.append(f"Anatomy skill '{diagram['preferred_skill']}' is missing or invalid; resolve its actual repository/path before generating structured diagrams")
    rest_key = bool(os.environ.get("ELEVENLABS_API_KEY")); voice_set = bool(voice["voice_id"] or os.environ.get("ELEVENLABS_VOICE_ID"))
    if generate_narration:
        if not rest_key: errors.append("ElevenLabs REST key missing; use a confirmed connected ElevenLabs tool or configure ELEVENLABS_API_KEY")
        if not voice_set: errors.append("Choose an ElevenLabs voice_id in production-config.json or ELEVENLABS_VOICE_ID")
    return {"anatomy": {"preferred_skill": diagram["preferred_skill"], "available": available is not None, "path": str(available) if available else None, "invalid_candidates": invalid}, "narration": {"provider": voice["provider"], "rest_key_configured": rest_key, "voice_configured": voice_set}, "errors": errors}

def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("init"); a.add_argument("directory"); a.add_argument("--title", required=True); a.add_argument("--format", choices=FORMATS, default="landscape"); a.add_argument("--fps", type=int, default=30); a.add_argument("--duration", type=float, default=30); a.add_argument("--language", default="en")
    for cmd in ["validate", "status"]: sub.add_parser(cmd).add_argument("directory")
    a = sub.add_parser("complete"); a.add_argument("directory"); a.add_argument("stage", choices=STAGES)
    a = sub.add_parser("align"); a.add_argument("directory"); a.add_argument("--audio", required=True); a.add_argument("--segments", required=True); a.add_argument("--method", choices=["manual-reviewed", "asr-unreviewed", "synthetic-test", "provider-unreviewed"], required=True)
    a = sub.add_parser("script-check"); a.add_argument("script"); a.add_argument("--fps", type=int, default=30)
    sub.add_parser("doctor")
    a = sub.add_parser("plan"); a.add_argument("directory"); a.add_argument("--requirements"); a.add_argument("--replace", action="store_true")
    a = sub.add_parser("next"); a.add_argument("directory")
    a = sub.add_parser("review"); a.add_argument("directory"); a.add_argument("--record", required=True)
    a = sub.add_parser("workflow-check"); a.add_argument("directory"); a.add_argument("--diagrams", "--anatomical", dest="anatomical", action="store_true"); a.add_argument("--generate-narration", action="store_true")
    a = p.parse_args()
    try:
        if a.command == "init": print(init(a.directory, a.title, a.format, a.fps, a.duration, a.language)); return 0
        if a.command == "doctor": result = doctor()
        elif a.command in ["plan", "next", "review"]:
            import director
            if a.command == "plan": result = director.plan_project(a.directory, read(a.requirements) if a.requirements else None, a.replace)
            elif a.command == "next": result = director.next_action(a.directory)
            else: result = director.review(a.directory, read(a.record))
        elif a.command == "workflow-check": result = workflow_check(a.directory, a.anatomical, a.generate_narration)
        elif a.command == "validate": result = validate(a.directory)
        elif a.command == "status": result = statuses(a.directory)
        elif a.command == "complete": complete(a.directory, a.stage); result = statuses(a.directory)
        elif a.command == "align": align(a.directory, a.audio, a.segments, a.method); result = validate(a.directory)
        else: result = script_report(read(a.script), a.fps)
        print(json.dumps(result, ensure_ascii=False, indent=2)); return int(bool(result.get("errors")))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as e:
        print(f"ERROR: {e}", file=sys.stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
