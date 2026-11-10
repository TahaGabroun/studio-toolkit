import importlib.util
import json
import re
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/studio-toolkit/scripts'
sys.path.insert(0, str(SCRIPTS))
import animation
from animation_render import pixel_difference


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result); return result


anim = module('anim_kit_test', animation.RUNTIME / 'kit/anim.py')


class Animation(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.root = Path(self.temporary.name)

    def tearDown(self): self.temporary.cleanup()

    def audio(self, duration=2):
        path = self.root / 'calibration.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', f'sine=frequency=1000:duration={duration}', str(path)], check=True)
        return path

    def project(self, kind='stick-figure'):
        target = self.root / kind; animation.init(kind, target); return target

    def words(self, text='مرحبا CO2'):
        path = self.root / 'words.json'
        animation.write(path, {'method': 'synthetic-test', 'segments': [{'text': w, 'start_s': .1 + i * .7, 'end_s': .5 + i * .7} for i, w in enumerate(text.split())]})
        return path

    def test_fresh_project_preserves_existing_work(self):
        target = self.project(); marker = target / 'mine'; marker.write_text('original')
        with self.assertRaises(ValueError): animation.init('stick-figure', target)
        self.assertEqual(marker.read_text(), 'original')

    def test_fresh_cartoon_has_no_inherited_speech(self):
        for kind in animation.ENGINES:
            target = self.project(kind)
            self.assertEqual(animation.read(target / 'script.json'), [])
            self.assertFalse(list(target.rglob('*.wav')))
            self.assertFalse(animation.read(target / 'animation-project.json')['example'])

    def test_word_data_rejects_invalid_time(self):
        for times in [(float('nan'), 1), (0, float('inf')), (True, 1), (1, 1), (2, 1), (-1, 1)]:
            with self.assertRaises(ValueError): animation.measured_words([{'w': 'word', 's': times[0], 'e': times[1]}])

    def test_word_data_rejects_overlap_and_multiword_segments(self):
        with self.assertRaises(ValueError): animation.measured_words([{'w': 'two words', 's': 0, 'e': 1}])
        with self.assertRaises(ValueError): animation.measured_words([{'w': 'a', 's': 0, 'e': 1}, {'w': 'b', 's': .5, 'e': 2}])

    def test_sync_preserves_mixed_language_and_audio_clock(self):
        target = self.project(); voice = self.audio()
        result = animation.sync(target, self.words(), voice, 'synthetic-test')
        self.assertAlmostEqual(result['duration_seconds'], 2)
        words = animation.read(target / 'audio/words_new.json')
        self.assertEqual([w['w'] for w in words], ['مرحبا', 'CO2'])
        self.assertAlmostEqual(words[0]['s'], .1); self.assertAlmostEqual(words[1]['s'], .8)
        self.assertFalse((target.parent / 'narration.json').exists())

    def test_sync_refuses_unreviewed_provenance_promotion(self):
        target = self.project()
        with self.assertRaises(ValueError): animation.sync(target, self.words(), self.audio(), 'manual-reviewed')
        self.assertFalse((target / 'audio/vo.wav').exists())

    def test_sync_refuses_audio_overrun_without_side_effect(self):
        target = self.project()
        with self.assertRaises(ValueError): animation.sync(target, self.words(), self.audio(.3), 'synthetic-test')
        self.assertFalse((target / 'audio/vo.wav').exists())

    def test_sync_requires_matching_script(self):
        target = self.project(); animation.write(target / 'script.json', ['A different script.'])
        with self.assertRaises(ValueError): animation.sync(target, self.words(), self.audio(), 'synthetic-test')

    def test_sync_preserves_existing_audio(self):
        target = self.project(); voice = self.audio(); words = self.words()
        animation.sync(target, words, voice, 'synthetic-test')
        before = (target / 'audio/vo.wav').read_bytes()
        with self.assertRaises(ValueError): animation.sync(target, words, voice, 'synthetic-test')
        self.assertEqual((target / 'audio/vo.wav').read_bytes(), before)

    def test_3d_captions_are_safe_js_and_have_measured_ends(self):
        target = self.project('cartoon-animation'); voice = self.audio()
        animation.sync(target, self.words('مرحبا CO2'), voice, 'synthetic-test')
        source = (target / 'src/caption-data.js').read_text()
        data = json.loads(source.removeprefix('export const CAPTIONS = ').removesuffix(';\n'))
        self.assertEqual(data[0][0], .1); self.assertEqual(data[-1][-1], 1.2)

    @unittest.skipUnless(shutil.which('node'), 'Node is optional for the Python core')
    def test_caption_chunks_split_long_speech_gaps_in_both_engines(self):
        words = [{'w': 'CO2', 's': .5, 'e': .7, 'line': 0}, {'w': 'لَم', 's': 2, 'e': 2.2, 'line': 0}]
        helper = module('caption_gap_test', animation.RUNTIME / 'skills/zach-d-films/engine/captions.py')
        self.assertEqual(len(helper.chunks(words)), 2)
        source = (animation.RUNTIME / 'skills/stick-figure/engine/template/web/main.js').read_text()
        expression = source[source.index('const CHUNKS = '):source.index('// Caption typography')]
        code = 'const WORDS=' + json.dumps(words) + ';' + expression + ';process.stdout.write(JSON.stringify(CHUNKS));'
        result = json.loads(subprocess.run(['node', '-e', code], check=True, capture_output=True, text=True).stdout)
        self.assertEqual([x['text'] for x in result], ['CO2', 'لَم'])
        self.assertLess(result[0]['e'], result[1]['s'])

    def test_take_warp_checks_words_and_endpoints(self):
        old = animation.measured_words([{'w': 'a', 's': .1, 'e': .5}, {'w': 'b', 's': .7, 'e': 1}])
        new = animation.measured_words([{'w': 'a', 's': .2, 'e': .6}, {'w': 'b', 's': 1, 'e': 1.5}])
        result = animation.warp(old, new, 1.1, 2)
        self.assertEqual(result['anchors'][0], [0, 0]); self.assertEqual(result['anchors'][-1], [1.1, 2])
        new[-1]['w'] = 'changed'
        with self.assertRaises(ValueError): animation.warp(old, new, 1.1, 2)

    def test_graph_rejects_fake_scaling_from_zero(self):
        graph = module('graph_build_test', animation.RUNTIME / 'skills/graph/build.py')
        spec = {**graph.DEFAULTS, 'values': [4, 9, 0]}
        anim.validate_spec('graph', spec)
        for key, value in [('values', [1, float('inf')]), ('values', [True, 1]), ('labels', ['A']), ('decimals', -1), ('final', 100)]:
            with self.assertRaises(ValueError): anim.validate_spec('graph', {**spec, key: value})

    def test_bad_map_and_label_data_rejected(self):
        builder = module('map_build_test', animation.RUNTIME / 'skills/map-route/build.py')
        spec = {**builder.DEFAULTS, 'destination': 'Park', 'minutes': 9, 'distance': 2}
        for key, value in [('minutes', -1), ('distance', float('nan')), ('unit', 'miles'), ('places', [42]), ('seed', True)]:
            with self.assertRaises(ValueError): anim.validate_spec('map-route', {**spec, key: value})
        with self.assertRaises(ValueError): anim.validate_spec('breakdown', {'labels': [[42]] * 6})

    def test_unknown_spec_fields_rejected(self):
        path = self.root / 'spec.json'; animation.write(path, {'typo': 1})
        with self.assertRaises(ValueError): anim.load_spec(path, {})

    @unittest.skipUnless(shutil.which('node'), 'Node is optional for the Python core')
    def test_caption_text_preserves_scientific_case_and_arabic_marks(self):
        source = animation.RUNTIME / 'skills/stick-figure/engine/template/web/main.js'
        expression = re.search(r'const capText = (.*);', source.read_text())[1]
        code = 'const fn=(' + expression + ');process.stdout.write(JSON.stringify(fn("CO2 لَم IL-1")));'
        result = subprocess.run(['node', '-e', code], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), 'CO2 لَم IL-1')

    def test_quick_font_faces_use_one_family_per_descriptor(self):
        for template in (animation.RUNTIME / 'skills').glob('*/template.html'):
            for face in re.findall(r'@font-face\s*\{([^}]+)', template.read_text()):
                family = re.search(r'font-family\s*:\s*([^;]+)', face)[1]
                self.assertNotIn(',', family, template.name)

    def test_pixel_comparison_measures_visual_changes(self):
        import io
        from PIL import Image
        first = Image.new('RGB', (10, 10), 'black'); second = first.copy(); second.putpixel((3, 4), (9, 9, 9))
        def png(image):
            output = io.BytesIO(); image.save(output, format='PNG'); return output.getvalue()
        self.assertEqual(pixel_difference(png(first), png(second)), {'changed_pixels': 1, 'max_channel_delta': 9})

    def test_bundle_has_six_specialists_and_excludes_installed_dependencies(self):
        package = module('animation_pack_test', ROOT / 'scripts/package_chatgpt.py')
        with zipfile.ZipFile(package.package(self.root / 'test.skill')) as archive:
            names = archive.namelist()
            self.assertEqual(sum(Path(n).name.lower() == 'skill.md' for n in names), 1)
            self.assertTrue(all('node_modules' not in Path(n).parts for n in names))
            self.assertTrue(all('/models/' not in n for n in names))
            self.assertLess(sum(f.file_size for f in archive.infolist()), 25 * 1024 * 1024)
            for name in list(animation.QUICK) + list(animation.ENGINES): self.assertIn('studio-toolkit/references/specialists/' + name + '.md', names)
            self.assertIn('studio-toolkit/references/animation-runtime/kit/package-lock.json', names)
            self.assertFalse(any(n.endswith('.wav') for n in names))


if __name__ == '__main__': unittest.main()
