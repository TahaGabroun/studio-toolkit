import base64
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/studio-toolkit/scripts"))
import studio
import elevenlabs_narration as voice

def fixture_script():
    return {"title": "Timing fixture", "promise": "Explain a labelled mechanism", "language": "ar", "scenes": [
        {"id": "vessel", "role": "hook", "narration": "الوعاء CO2.", "visual": "Identify the fixture vessel", "source_ids": ["fixture"]},
        {"id": "cell", "role": "payoff", "narration": "Then a cell.", "visual": "Track the fixture cell", "source_ids": ["fixture"]}
    ]}

class ProductionDefaults(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name) / "film"
        studio.init(self.root, "Future film")
    def tearDown(self): self.temp.cleanup()
    def test_new_project_records_requested_preferences(self):
        config = studio.production_config(self.root)
        self.assertEqual(config["narration"]["provider"], "elevenlabs")
        self.assertEqual(config["diagrams"]["preferred_skill"], "anatomy")
        self.assertTrue(config["diagrams"]["required_for_diagram_scenes"])
        self.assertFalse(studio.validate(self.root)["errors"])
    def test_existing_project_without_preferences_remains_valid(self):
        (self.root / "production-config.json").unlink()
        self.assertFalse(studio.validate(self.root)["errors"])
        self.assertEqual(studio.production_config(self.root)["narration"]["provider"], "elevenlabs")
    def test_explicit_anatomy_skill_is_discovered_and_missing_path_blocks(self):
        skill = Path(self.temp.name) / "anatomy"; skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: anatomy\ndescription: Test anatomical design fixture\n---\n")
        config = studio.production_config(self.root); config["diagrams"]["skill_path"] = str(skill)
        studio.write(self.root / "production-config.json", config)
        result = studio.workflow_check(self.root, anatomical=True)
        self.assertTrue(result["anatomy"]["available"]); self.assertEqual(result["errors"], [])
        (skill / "SKILL.md").unlink()
        self.assertIn("missing", str(studio.workflow_check(self.root, anatomical=True)["errors"]))
    def test_credentials_preflight_reports_state_without_secret(self):
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-only-secret", "ELEVENLABS_VOICE_ID": "test_voice"}):
            result = studio.workflow_check(self.root, generate_narration=True)
        self.assertTrue(result["narration"]["rest_key_configured"]); self.assertNotIn("test-only-secret", json.dumps(result))
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "", "ELEVENLABS_VOICE_ID": ""}):
            self.assertEqual(len(studio.workflow_check(self.root, generate_narration=True)["errors"]), 2)
    def test_invalid_skill_metadata_does_not_pass_preflight(self):
        fake = Path(self.temp.name) / "invalid-skill"; fake.mkdir(); (fake / "SKILL.md").write_text("Plain text is not a skill manifest")
        config = studio.production_config(self.root); config["diagrams"]["skill_path"] = str(fake)
        studio.write(self.root / "production-config.json", config)
        result = studio.workflow_check(self.root, anatomical=True)
        self.assertFalse(result["anatomy"]["available"]); self.assertTrue(result["errors"])
    def test_supplied_anatomy_is_available_from_checkout(self):
        result = studio.workflow_check(self.root, anatomical=True)
        self.assertTrue(result["anatomy"]["available"]); self.assertEqual(result["errors"], [])
        self.assertIn("integrations/anatomy/SKILL.md", result["anatomy"]["path"])
    def test_installer_manages_anatomy_without_changing_canonical_inventory(self):
        target = Path(self.temp.name) / "skills"
        command = [sys.executable, str(ROOT / "scripts/manage_skills.py")]
        installed = subprocess.run(command + ["install", "--dest", str(target), "--with-anatomy"], check=True, capture_output=True, text=True)
        expected = {item['id'] for item in json.loads((ROOT / 'manifest.json').read_text())['skills']} | {'anatomy'}
        self.assertEqual({item['skill'] for item in json.loads(installed.stdout)}, expected)
        self.assertEqual((target / "anatomy").resolve(), (ROOT / "integrations/anatomy").resolve())
        subprocess.run(command + ["uninstall", "--dest", str(target), "--with-anatomy"], check=True, capture_output=True)
        self.assertFalse((target / "anatomy").exists())
    def test_preferences_cannot_embed_an_api_key(self):
        config = studio.production_config(self.root); config["narration"]["api_key"] = "unwanted"
        studio.write(self.root / "production-config.json", config)
        self.assertTrue(studio.validate(self.root)["errors"])
    def test_preference_change_reuses_writing_but_invalidates_visual_checkpoint(self):
        studio.write(self.root / "script.json", fixture_script()); (self.root / "script.md").write_text("Approved fixture narration")
        studio.write(self.root / "storyboard.json", {"scenes": [{"id": "vessel", "composition": "Original vessel", "targets": ["vessel"], "focus": "vessel", "transition": "hold"}]})
        for stage in ["idea", "research", "strategy", "script", "storyboard"]: studio.complete(self.root, stage)
        config = studio.production_config(self.root); config["narration"]["voice_id"] = "test_voice"
        studio.write(self.root / "production-config.json", config)
        state = studio.statuses(self.root)
        self.assertEqual(state["script"], "complete"); self.assertEqual(state["storyboard"], "stale")

class VoiceFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name) / "film"
        studio.init(self.root, "Timing fixture"); studio.write(self.root / "script.json", fixture_script())
        self.plan = voice.request_plan(self.root, "test_voice")
    def tearDown(self): self.temp.cleanup()
    def response(self, audio=b"fixture-not-real-audio"):
        text = self.plan["request"]["body"]["text"]
        return {"audio_base64": base64.b64encode(audio).decode(), "alignment": {"characters": list(text), "character_start_times_seconds": [i / 100 for i in range(len(text))], "character_end_times_seconds": [(i+1) / 100 for i in range(len(text))]}}

class ProviderTiming(VoiceFixture):
    def test_arabic_and_scientific_terms_use_provider_character_times(self):
        segments, words = voice.alignment_segments(self.response(), self.plan)
        self.assertEqual([c["id"] for c in segments["segments"]], ["vessel", "cell"])
        co2 = next(c for c in words["segments"] if c["text"] == "CO2.")
        position = self.plan["request"]["body"]["text"].index("CO2.")
        self.assertEqual(co2["start_s"], position / 100); self.assertEqual(co2["end_s"], (position+4) / 100)
        self.assertEqual(segments["method"], "provider-unreviewed")
    def test_normalized_original_mismatch_never_guesses(self):
        response = self.response(); response["normalized_alignment"] = response.pop("alignment")
        response["normalized_alignment"]["characters"] = list("rewritten numbers")
        with self.assertRaisesRegex(ValueError, "does not match"): voice.alignment_segments(response, self.plan)
    def test_original_alignment_wins_over_normalized_text(self):
        response = self.response(); response["normalized_alignment"] = {"characters": list("other spoken normalization")}
        segments, _ = voice.alignment_segments(response, self.plan)
        self.assertEqual(segments["segments"][0]["text"], "الوعاء CO2.")
    def test_malformed_or_nonfinite_timestamps_reject(self):
        response = self.response(); response["alignment"]["character_start_times_seconds"][0] = float("inf")
        with self.assertRaisesRegex(ValueError, "Invalid provider"): voice.alignment_segments(response, self.plan)
        response = self.response(); response["alignment"]["character_end_times_seconds"].pop()
        with self.assertRaisesRegex(ValueError, "Mismatched"): voice.alignment_segments(response, self.plan)
    def test_voice_and_text_changes_invalidate_speech_cache(self):
        other = voice.request_plan(self.root, "another_voice")
        self.assertNotEqual(other["request_sha256"], self.plan["request_sha256"])
        script = fixture_script(); script["scenes"][0]["narration"] += " Revised."
        studio.write(self.root / "script.json", script)
        self.assertNotEqual(voice.request_plan(self.root, "test_voice")["request_sha256"], self.plan["request_sha256"])
    def test_missing_key_never_sends_a_network_request(self):
        calls = []
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": ""}):
            with self.assertRaisesRegex(ValueError, "no request was sent"):
                voice.acquire_response(self.root, self.plan, transport=lambda *a, **k: calls.append(a))
        self.assertEqual(calls, [])
    def test_bad_alignment_is_cached_without_touching_approved_artifacts(self):
        originals = {name: b"approved fixture bytes" for name in ["narration.json", "captions.srt", "timeline.json"]}
        for name, data in originals.items(): (self.root / name).write_bytes(data)
        response = self.response(); response["alignment"]["characters"][0] = "x"
        imported = self.root / "response.json"; studio.write(imported, response)
        with self.assertRaisesRegex(ValueError, "does not match"): voice.generate(self.root, "test_voice", imported)
        self.assertTrue(all((self.root / name).read_bytes() == data for name, data in originals.items()))
        cached, hit = voice.acquire_response(self.root, self.plan)
        self.assertTrue(hit); self.assertEqual(cached, response)

@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg needed for real media fixture")
class ProviderAudio(VoiceFixture):
    def test_mocked_api_real_mp3_and_verified_cache_reuse(self):
        audio_file = self.root / "fixture.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=2", "-c:a", "libmp3lame", str(audio_file)], check=True)
        response = self.response(audio_file.read_bytes()); calls = []
        def transport(request, timeout):
            calls.append(request)
            self.assertTrue(request.full_url.startswith("https://api.elevenlabs.io/v1/text-to-speech/test_voice/with-timestamps"))
            self.assertEqual(json.loads(request.data)["text"], self.plan["request"]["body"]["text"])
            return io.BytesIO(json.dumps(response).encode())
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-only-secret"}): first = voice.generate(self.root, "test_voice", transport=transport)
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": ""}): second = voice.generate(self.root, "test_voice", transport=transport)
        self.assertEqual(len(calls), 1); self.assertFalse(first["cache_hit"]); self.assertTrue(second["cache_hit"])
        self.assertEqual(studio.digest(first["audio"]), studio.digest(audio_file))
        self.assertNotIn("test-only-secret", json.dumps(studio.read(first["metadata"])))
        self.assertFalse((self.root / "narration.json").exists())
        Path(first["audio"]).write_bytes(b"edited")
        with self.assertRaisesRegex(ValueError, "was edited"): voice.generate(self.root, "test_voice")
    def test_corrupt_cache_does_not_trigger_a_billable_retry(self):
        response = self.response(); path = self.root / "response.json"; studio.write(path, response)
        voice.acquire_response(self.root, self.plan, imported=path)
        cache = self.root / ".studio-cache/elevenlabs" / (self.plan["request_sha256"] + ".json")
        saved = studio.read(cache); saved["response"]["audio_base64"] = "tampered"; studio.write(cache, saved)
        with self.assertRaisesRegex(ValueError, "Cached ElevenLabs response changed"):
            voice.acquire_response(self.root, self.plan, transport=lambda *a, **k: self.fail("Unexpected network call"))
    def test_corrected_response_import_preserves_old_response(self):
        bad = self.response(); bad["alignment"]["characters"][0] = "X"
        source = self.root / "bad.json"; studio.write(source, bad)
        voice.acquire_response(self.root, self.plan, imported=source)
        corrected = self.response(); source = self.root / "corrected.json"; studio.write(source, corrected)
        response, hit = voice.acquire_response(self.root, self.plan, imported=source)
        self.assertFalse(hit); self.assertEqual(response, corrected)
        history = list((self.root / ".studio-cache/elevenlabs/history").glob("*.json")); self.assertEqual(len(history), 1)
        self.assertEqual(studio.read(history[0])["response"], bad)
    def test_renamed_cues_reuse_audio_and_get_distinct_candidate(self):
        path = self.root / "fixture.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=duration=2", "-c:a", "libmp3lame", str(path)], check=True)
        imported = self.root / "response.json"; studio.write(imported, self.response(path.read_bytes()))
        first = voice.generate(self.root, "test_voice", imported=imported)
        script = fixture_script(); script["scenes"][0]["id"] = "renamed-vessel"; studio.write(self.root / "script.json", script)
        second = voice.generate(self.root, "test_voice")
        self.assertTrue(second["cache_hit"]); self.assertNotEqual(first["segments"], second["segments"])
        self.assertEqual(studio.digest(first["audio"]), studio.digest(second["audio"]))
        self.assertEqual(studio.read(second["segments"])["segments"][0]["id"], "renamed-vessel")
    def test_provider_cue_cannot_exceed_import_duration_tolerance(self):
        path = self.root / "fixture.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=duration=2", "-c:a", "libmp3lame", str(path)], check=True)
        response = self.response(path.read_bytes()); duration = float(studio.probe(path)["format"]["duration"])
        response["alignment"]["character_end_times_seconds"][-1] = duration + .03
        imported = self.root / "response.json"; studio.write(imported, response)
        with self.assertRaisesRegex(ValueError, "exceed audio duration"): voice.generate(self.root, "test_voice", imported=imported)

if __name__ == "__main__": unittest.main()
