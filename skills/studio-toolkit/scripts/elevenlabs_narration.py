#!/usr/bin/env python3
"""Generate continuous ElevenLabs narration with cached, provider-measured timings.

No automatic network retries, voice cloning, or edits to approved narration/timeline.
Uses Python stdlib and the existing FFprobe dependency; credentials stay in env.
"""
from __future__ import annotations
import argparse
import base64
import binascii
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from studio import digest, local, probe, production_config, read, schema_errors, write

API_ROOT = "https://api.elevenlabs.io/v1/text-to-speech"

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")

def request_plan(root, voice_id=None):
    config = production_config(root)["narration"]
    voice_id = voice_id or config["voice_id"] or os.environ.get("ELEVENLABS_VOICE_ID")
    if not voice_id or not re.fullmatch(r"[A-Za-z0-9_-]+", voice_id):
        raise ValueError("Choose a valid ElevenLabs voice_id in production-config.json, --voice-id, or ELEVENLABS_VOICE_ID")
    script = read(Path(root) / "script.json")
    errors = schema_errors("script", script)
    if errors: raise ValueError("; ".join(errors))
    ids = [scene["id"] for scene in script["scenes"]]
    if len(ids) != len(set(ids)): raise ValueError("Duplicate script scene IDs")
    scenes = []
    text = ""
    for scene in script["scenes"]:
        spoken = scene["narration"].strip()
        if not spoken: raise ValueError(f"Empty narration: {scene['id']}")
        if text: text += "\n\n"
        start = len(text); text += spoken
        scenes.append({"id": scene["id"], "text": spoken, "start_character": start, "end_character": len(text)})
    # One continuous generation preserves prosody; split long-form into approved chapters explicitly.
    if config["model_id"] == "eleven_multilingual_v2" and len(text) > 10000:
        raise ValueError("Multilingual v2 request exceeds 10,000 characters; prepare chapter-sized scripts and retain measured offsets")
    payload = {"text": text, "model_id": config["model_id"], "apply_text_normalization": "auto"}
    # multilingual_v2 does not accept language_code; Arabic/English is carried by the script.
    request = {"voice_id": voice_id, "output_format": config["output_format"], "body": payload}
    return {"request": request, "request_sha256": hashlib.sha256(canonical(request)).hexdigest(), "scenes": scenes}

def alignment_segments(response, plan):
    """Map scene and word spans to measured original-text character times, never guessed time."""
    text = plan["request"]["body"]["text"]
    alignment = None
    for name in ["alignment", "normalized_alignment"]:
        candidate = response.get(name)
        if isinstance(candidate, dict) and isinstance(candidate.get("characters"), list):
            chars = candidate["characters"]
            if all(isinstance(c, str) and c for c in chars) and "".join(chars) == text:
                alignment = candidate; break
    if alignment is None:
        raise ValueError("Provider alignment does not match the approved script. Keep the cached response and review/import real timestamps; do not guess a normalization mapping")
    chars = alignment["characters"]; starts = alignment.get("character_start_times_seconds"); ends = alignment.get("character_end_times_seconds")
    if not isinstance(starts, list) or not isinstance(ends, list) or not len(chars) == len(starts) == len(ends):
        raise ValueError("Mismatched ElevenLabs character/timestamp arrays")
    previous_start = previous_end = 0
    character_indices = []
    for index, (char, start, end) in enumerate(zip(chars, starts, ends)):
        if any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or t < 0 for t in [start, end]):
            raise ValueError("Invalid provider timestamp")
        if end < start or start < previous_start or end < previous_end: raise ValueError("Provider character timestamps are out of order")
        previous_start, previous_end = start, end
        character_indices.extend([index] * len(char))
    def span(start, end):
        first, last = character_indices[start], character_indices[end - 1]
        if ends[last] <= starts[first]: raise ValueError("Provider span has no measured duration")
        return starts[first], ends[last]
    segments = []; previous = 0
    for scene in plan["scenes"]:
        start, end = span(scene["start_character"], scene["end_character"])
        if start < previous: raise ValueError("Overlapping scene cues require timestamp review")
        segments.append({"id": scene["id"], "start_s": start, "end_s": end, "text": scene["text"]})
        previous = end
    words = []
    for index, match in enumerate(re.finditer(r"\S+", text)):
        start, end = span(match.start(), match.end())
        words.append({"id": f"word-{index+1}", "start_s": start, "end_s": end, "text": match.group()})
    return {"method": "provider-unreviewed", "cue_ids": "script scene IDs; map timeline events explicitly", "segments": segments}, {"method": "provider-unreviewed", "segments": words}

def acquire_response(root, plan, imported=None, transport=None):
    cache = local(root, ".studio-cache/elevenlabs/" + plan["request_sha256"] + ".json")
    if cache.is_file() and imported is None:
        saved = read(cache)
        if saved.get("request_sha256") != plan["request_sha256"] or saved.get("response_sha256") != hashlib.sha256(canonical(saved.get("response"))).hexdigest():
            raise ValueError("Cached ElevenLabs response changed; review it explicitly before any paid regeneration")
        return saved["response"], True
    if imported is not None:
        response = read(imported)
    else:
        key = os.environ.get("ELEVENLABS_API_KEY")
        if not key: raise ValueError("ELEVENLABS_API_KEY is not configured; no request was sent")
        request = plan["request"]
        endpoint = f"{API_ROOT}/{quote(request['voice_id'], safe='')}/with-timestamps?output_format={request['output_format']}"
        req = Request(endpoint, data=canonical(request["body"]), headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"}, method="POST")
        try:
            with (transport or urlopen)(req, timeout=180) as connection:
                response = json.loads(connection.read().decode("utf-8"))
        except HTTPError as error:
            # Never echo provider error bodies, headers or credentials; don't auto-retry billable work.
            raise ValueError(f"ElevenLabs HTTP {error.code}; check access/quota/input. No automatic retry was made") from None
        except (URLError, TimeoutError):
            raise ValueError("ElevenLabs connection failed; check request history before retrying potentially billed work") from None
    if not isinstance(response, dict) or not isinstance(response.get("audio_base64"), str):
        raise ValueError("ElevenLabs response has no audio_base64")
    # Cache a completed response before downstream alignment checks so a review doesn't buy speech twice.
    if cache.is_file():
        # An explicit corrected import must be usable, while the original paid response is preserved.
        old = read(cache)
        old_sha = hashlib.sha256(canonical(old)).hexdigest()
        history = cache.parent / "history" / f"{plan['request_sha256']}-{old_sha}.json"
        if not history.exists(): write(history, old)
    write(cache, {"request_sha256": plan["request_sha256"], "response_sha256": hashlib.sha256(canonical(response)).hexdigest(), "response": response})
    return response, False

def generate(root, voice_id=None, imported=None, transport=None):
    root = Path(root).resolve()
    if (root/'production-plan.json').is_file():
        import director
        direction=director.current(root)
        if direction['narration']['mode']!='generate':raise ValueError('Production direction does not request new speech; preserve the supplied recording or intentional silence')
        if director.state(root,direction)[0]['status']!='pass':raise ValueError('Review content before production speech; no provider request was sent')
    plan = request_plan(root, voice_id)
    if shutil.which("ffprobe") is None: raise ValueError("ffprobe is required to validate generated speech; no request was sent")
    response, cached = acquire_response(root, plan, imported, transport)
    segments, words = alignment_segments(response, plan)
    try: audio = base64.b64decode(response["audio_base64"], validate=True)
    except (binascii.Error, ValueError): raise ValueError("Invalid base64 provider audio; cached response retained") from None
    if not audio: raise ValueError("Empty provider audio")
    # Cue labels/scene boundaries can change without buying identical speech again.
    mapping_sha = hashlib.sha256(canonical(plan["scenes"])).hexdigest()
    response_sha = hashlib.sha256(canonical(response)).hexdigest()
    candidate_sha = hashlib.sha256(canonical([mapping_sha, response_sha])).hexdigest()
    output = local(root, "assets/elevenlabs/" + plan["request_sha256"] + "/" + candidate_sha)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Validate the actual bytes before publishing candidate outputs; approved project artifacts are untouched.
    with tempfile.TemporaryDirectory(prefix=".elevenlabs-", dir=output.parent) as temporary:
        candidate = Path(temporary) / "narration.mp3"; candidate.write_bytes(audio)
        media = probe(candidate); stream = next((s for s in media["streams"] if s.get("codec_type") == "audio"), None)
        if stream is None or stream.get("codec_name") != "mp3": raise ValueError("Provider output is not the requested MP3 audio")
        duration = float(media["format"]["duration"])
        if not math.isfinite(duration) or segments["segments"][-1]["end_s"] > duration + .001:
            raise ValueError("Provider timestamps exceed audio duration")
    files = {"narration.mp3": audio, "segments.json": canonical(segments) + b"\n", "words.json": canonical(words) + b"\n"}
    metadata = {"provider": "elevenlabs", "request_sha256": plan["request_sha256"], "scene_mapping_sha256": mapping_sha, "response_sha256": response_sha, "audio_sha256": hashlib.sha256(audio).hexdigest(), "voice_id": plan["request"]["voice_id"], "model_id": plan["request"]["body"]["model_id"], "duration_seconds": duration, "review": "pending listening, scientific pronunciation and cue review", "usage_rights": "Verify the account's ElevenLabs usage rights; no CC0 or commercial entitlement is inferred"}
    files["generation.json"] = canonical(metadata) + b"\n"
    for name, data in files.items():
        target = output / name
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f"Candidate was edited: {name}; preserve/review the edit instead of overwriting it")
    output.mkdir(exist_ok=True)
    for name, data in files.items():
        if not (output / name).exists(): (output / name).write_bytes(data)
    return {"provider": "elevenlabs", "cache_hit": cached, "audio": str(output / "narration.mp3"), "segments": str(output / "segments.json"), "words": str(output / "words.json"), "metadata": str(output / "generation.json"), "review": "pending; approved narration.json, captions and timeline were not changed"}

def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("project"); parser.add_argument("--voice-id"); parser.add_argument("--import-response", type=Path); parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        if args.dry_run:
            plan = request_plan(args.project, args.voice_id)
            result = {"provider": "elevenlabs", "request_sha256": plan["request_sha256"], "characters": len(plan["request"]["body"]["text"]), "scenes": len(plan["scenes"]), "api_key_configured": bool(os.environ.get("ELEVENLABS_API_KEY")), "network_request_sent": False}
        else: result = generate(args.project, args.voice_id, args.import_response)
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
