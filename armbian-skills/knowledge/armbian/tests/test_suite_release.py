"""Portable release checks; no historical workspace, device or SDK is required."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

import jsonschema
import yaml

K = Path(__file__).resolve().parents[1]
SUITE = K.parents[1]
spec = importlib.util.spec_from_file_location('suite_build', K / 'scripts/build_skills.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class SuiteReleaseTests(unittest.TestCase):
    def test_translations_share_metadata_without_duplicate_catalog_entries(self):
        root = K / 'references'
        catalog = json.loads((root / 'catalog.json').read_text())
        index = {entry['id']: entry for entry in catalog['entries']}
        self.assertEqual(len(index), len(catalog['entries']))
        for path in root.rglob('*.md'):
            if path.name.endswith('.zh-CN.md'):
                continue
            translated = path.with_name(path.stem + '.zh-CN.md')
            self.assertTrue(translated.is_file(), translated)
            canonical_metadata = yaml.safe_load(path.read_text().split('---\n', 2)[1])
            translated_metadata = yaml.safe_load(translated.read_text().split('---\n', 2)[1])
            self.assertEqual(canonical_metadata, translated_metadata)
            self.assertEqual(index[canonical_metadata['id']]['path'], str(path.relative_to(root)))
        self.assertFalse(any(entry['path'].endswith('.zh-CN.md') for entry in catalog['entries']))

    def test_translation_changes_are_covered_by_package_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / build.NAMES[0]
            shutil.copytree(SUITE / 'skills' / build.NAMES[0], package)
            translated = package / 'references/common/identity.zh-CN.md'
            translated.write_text(translated.read_text() + '\nModified translation.\n')
            with self.assertRaises(ValueError):
                build.verify_package(package)

    def test_source_lock_package_integrity_and_schemas(self):
        lock = yaml.safe_load((K / 'release.yaml').read_text())
        self.assertEqual(build.current_lock(), lock)
        manifests = [build.verify_package(SUITE / 'skills' / name, build.manifest_for(name, lock))
                     for name in build.NAMES]
        self.assertEqual(len({m['knowledge_digest'] for m in manifests}), 1)
        metadata = json.loads((K / 'schemas/reference-metadata.schema.json').read_text())
        for path in (K / 'references').rglob('*'):
            if path.suffix not in {'.md', '.yaml'} or path.name == 'catalog.yaml':
                continue
            text = path.read_text()
            data = yaml.safe_load(text.split('---\n', 2)[1]) if path.suffix == '.md' else yaml.safe_load(text)
            jsonschema.validate(data, metadata)
        facts = json.loads((K / 'schemas/task-facts.schema.json').read_text())
        for path in (K / 'fixtures').glob('*.json'):
            jsonschema.validate(json.loads(path.read_text()), facts)
        compatibility = json.loads((K / 'schemas/compatibility-case.schema.json').read_text())
        for path in (K / 'references/compatibility').glob('*.yaml'):
            for case in yaml.safe_load(path.read_text()).get('cases', []):
                jsonschema.validate(case, compatibility)
        release = json.loads((K / 'schemas/reference-release.schema.json').read_text())
        for manifest in manifests:
            jsonschema.validate(manifest, release)

    def test_independent_install_matches_each_board_with_stdlib_only(self):
        for name in build.NAMES:
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as tmp:
                package = Path(tmp) / name
                shutil.copytree(SUITE / 'skills' / name, package)
                for fixture, expected in [('rk3576-gpio.json', 'board.seeed.recomputer-rk3576-devkit'),
                                          ('rk3588-gpu.json', 'board.seeed.recomputer-rk3588-devkit')]:
                    run = subprocess.run([sys.executable, '-I', str(package / 'scripts/reference-match/match.py'),
                                          '--input', str(K / 'fixtures' / fixture), '--kind', 'board'],
                                         cwd=tmp, capture_output=True, text=True, timeout=15)
                    self.assertEqual(run.returncode, 0, run.stderr)
                    self.assertEqual([e['id'] for e in json.loads(run.stdout)['matches']], [expected])
                build.verify_package(package)

    def test_tampered_helper_and_mixed_release_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / build.NAMES[0]
            shutil.copytree(SUITE / 'skills' / build.NAMES[0], package)
            helper = package / 'scripts/reference-match/match.py'
            original = helper.read_bytes()
            helper.write_bytes(original + b'\n# tampered\n')
            with self.assertRaises(ValueError):
                build.verify_package(package)
            helper.write_bytes(original)
            path = package / 'reference-release.yaml'
            manifest = yaml.safe_load(path.read_text())
            manifest['knowledge_release'] = 'different-release'
            path.write_text(yaml.safe_dump(manifest))
            with self.assertRaises(ValueError):
                build.verify_package(package)

    def test_archives_match_packages_and_exclude_development_data(self):
        sums = {line.split()[1]: line.split()[0] for line in (SUITE / 'dist/SHA256SUMS').read_text().splitlines()}
        for name in build.NAMES:
            artifact = SUITE / 'dist' / (name + '.skill')
            self.assertEqual(hashlib.sha256(artifact.read_bytes()).hexdigest(), sums[artifact.name])
            with zipfile.ZipFile(artifact) as archive:
                expected = {name + '/' + rel for rel in build.files_under(SUITE / 'skills' / name)}
                self.assertEqual(set(archive.namelist()), expected)
                for rel in archive.namelist():
                    self.assertFalse(Path(rel).is_absolute() or '..' in Path(rel).parts)
                    self.assertFalse(set(Path(rel).parts) & {'docs', 'evaluation', 'evidence', 'reports', 'fixtures', '__pycache__'})
                for rel, path in build.files_under(SUITE / 'skills' / name).items():
                    self.assertEqual(archive.read(name + '/' + rel), path.read_bytes())

    def test_standalone_suite_rebuilds_outside_original_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkout = Path(tmp) / 'standalone-suite'
            shutil.copytree(SUITE, checkout,
                            ignore=shutil.ignore_patterns('dist', '__pycache__', '*.pyc', '.venv'))
            before = {str(p.relative_to(SUITE / 'dist')): p.read_bytes()
                      for p in (SUITE / 'dist').iterdir() if p.is_file()}
            for args in [['scripts/refresh_catalog.py', '--check'],
                         ['scripts/build_skills.py'], ['scripts/build_skills.py', '--check']]:
                run = subprocess.run([sys.executable, *args], cwd=checkout,
                                     capture_output=True, text=True, timeout=60)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            after = {str(p.relative_to(checkout / 'dist')): p.read_bytes()
                     for p in (checkout / 'dist').iterdir() if p.is_file()}
            self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
