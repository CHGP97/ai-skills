#!/usr/bin/env python3
"""Build/check four independent skill bundles from a fixed reviewed lock."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile
import yaml

K = Path(__file__).resolve().parents[1]
WORKSPACE = K.parents[1]
REFERENCES = K / 'references'
SKILLS = WORKSPACE / 'skills'
DIST = WORKSPACE / 'dist'
NAMES = ('armbian-device-capabilities', 'armbian-hardware-application', 'armbian-application-deploy', 'armbian-application-verify')
LOCK = K / 'release.yaml'
sys.path.insert(0, str(K / 'scripts/reference-match'))
from match import validate_catalog, verify_files


def sha(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(files):
    return 'sha256:' + hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def files_under(root):
    return {str(p.relative_to(root)): p for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def safe_file(root, rel):
    path = root / rel
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Unsafe/missing file: ' + str(path))
    if any(p.is_symlink() for p in path.parents if p != root.parent):
        raise ValueError('Symlink parent: ' + str(path))
    return path


def current_lock():
    files = files_under(REFERENCES)
    for rel in files:
        if Path(rel).suffix not in {'.md', '.yaml', '.json', '.png', '.svg'}:
            raise ValueError('Unreviewed reference file type: ' + rel)
        safe_file(REFERENCES, rel)
    catalog = json.loads((REFERENCES / 'catalog.json').read_text())
    validate_catalog(catalog)
    verify_files(catalog, REFERENCES)
    if any(e.get('maturity') == 'draft' for e in catalog['entries']):
        raise ValueError('Draft entries cannot enter the reviewed bundle')
    return {'schema_version': '1', 'skill_version': '1.0.0', 'channel': 'stable',
            'knowledge_release': catalog['knowledge_release'],
            'documentation_languages': ['en', 'zh-CN'], 'default_documentation_language': 'en',
            'acceptance': {'publication_scope': 'static_references_and_workflows',
                           'hardware_validation_records': 'not_included',
                           'current_target_validation': 'required_per_task'},
            'knowledge_files': {rel: sha(path) for rel, path in files.items()},
            'helper_files': {'scripts/reference-match/match.py': sha(K / 'scripts/reference-match/match.py'),
                             'scripts/probe/probe_device.py': sha(K / 'scripts/probe_device.py')},
            'publication_policy': 'Static hardware/software references and workflows only; no proposals, evaluation reports, device captures, credentials, user measurements, task facts, build outputs or current target cache.'}


def expected_files(name, lock):
    base = SKILLS / name
    result = {rel: sha(base / rel) for rel in (
        'SKILL.md', 'SKILL.zh-CN.md', 'README.md', 'README.zh-CN.md',
        'CHANGELOG.md', 'CHANGELOG.zh-CN.md')}
    for rel, path in files_under(base / 'agents').items():
        result['agents/' + rel] = sha(path)
    result.update({'references/' + rel: digest for rel, digest in lock['knowledge_files'].items()})
    result['scripts/reference-match/match.py'] = lock['helper_files']['scripts/reference-match/match.py']
    if name == 'armbian-device-capabilities':
        result['scripts/probe/probe_device.py'] = lock['helper_files']['scripts/probe/probe_device.py']
    return result


def manifest_for(name, lock):
    catalog = json.loads((REFERENCES / 'catalog.json').read_text())
    return {'schema_version': '1', 'skill_name': name, 'skill_version': lock['skill_version'],
            'channel': lock['channel'], 'knowledge_release': lock['knowledge_release'],
            'documentation_languages': lock['documentation_languages'],
            'default_documentation_language': lock['default_documentation_language'],
            'knowledge_digest': canonical_digest(lock['knowledge_files']),
            'reference_ids': [e['id'] for e in catalog['entries']],
            'runtime_requirements': 'Python 3.9+ standard library for matching; target Python 3 for optional probe. Application language and dependencies are separate.',
            'acceptance': lock['acceptance'], 'files': expected_files(name, lock)}


def verify_package(base, expected=None):
    manifest = yaml.safe_load((base / 'reference-release.yaml').read_text())
    if expected is not None and manifest != expected:
        raise ValueError('Stale manifest: ' + str(base))
    files = manifest['files']
    actual = files_under(base)
    if set(actual) != set(files) | {'reference-release.yaml'}:
        raise ValueError('Unexpected or missing package files: ' + str(base))
    for rel, digest in files.items():
        if sha(safe_file(base, rel)) != digest:
            raise ValueError('Package digest mismatch: ' + str(base / rel))
    ref_files = {r[len('references/'):]: d for r, d in files.items() if r.startswith('references/')}
    if canonical_digest(ref_files) != manifest['knowledge_digest']:
        raise ValueError('Knowledge manifest mismatch')
    catalog = json.loads((base / 'references/catalog.json').read_text())
    if catalog['knowledge_release'] != manifest['knowledge_release']:
        raise ValueError('Knowledge release mismatch')
    index = validate_catalog(catalog)
    if sorted(index) != sorted(manifest['reference_ids']):
        raise ValueError('Reference ID manifest mismatch')
    verify_files(catalog, base / 'references')
    # Skill links must work after independent installation; no repository/sibling paths.
    for document in ('SKILL.md', 'SKILL.zh-CN.md', 'README.md', 'README.zh-CN.md',
                     'CHANGELOG.md', 'CHANGELOG.zh-CN.md'):
        text = (base / document).read_text()
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'^[a-z]+://', link) or link.startswith('#'):
                continue
            path = (base / link.split('#', 1)[0]).resolve()
            if not path.is_relative_to(base.resolve()) or not path.exists():
                raise ValueError('Broken/outside skill link: ' + document + ': ' + link)
    return manifest


def sync(name, lock):
    base = SKILLS / name
    if base.is_symlink() or not base.resolve().is_relative_to(SKILLS.resolve()):
        raise ValueError('Unsafe skill directory: ' + str(base))
    if any(p.is_symlink() for p in base.rglob('*')):
        raise ValueError('Generated skill must not contain symlinks: ' + str(base))
    old_path = base / 'reference-release.yaml'
    old = yaml.safe_load(old_path.read_text())['files'] if old_path.exists() else {}
    expected = expected_files(name, lock)
    managed = ('references/', 'scripts/')
    for rel, path in files_under(base).items():
        if rel.startswith(managed) and rel not in expected:
            if rel not in old:
                raise ValueError('Unmanaged file in generated directory: ' + str(path))
            path.unlink()
    for rel in lock['knowledge_files']:
        dest = base / 'references' / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(safe_file(REFERENCES, rel), dest)
    helpers = [('scripts/reference-match/match.py', K / 'scripts/reference-match/match.py')]
    if name == 'armbian-device-capabilities':
        helpers.append(('scripts/probe/probe_device.py', K / 'scripts/probe_device.py'))
    for rel, source in helpers:
        dest = base / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    for folder in ('references', 'scripts'):
        for path in sorted((base / folder).rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    manifest = manifest_for(name, lock)
    old_path.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False, width=110))
    verify_package(base, manifest)


def archive(name):
    DIST.mkdir(parents=True, exist_ok=True)
    dest = DIST / (name + '.skill')
    with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for rel, path in files_under(SKILLS / name).items():
            info = zipfile.ZipInfo(name + '/' + rel, date_time=(2026, 10, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update-lock', action='store_true', help='Explicitly review/freeze the complete current reference and helper file list')
    parser.add_argument('--check', action='store_true', help='Read-only validation of source lock and all generated packages')
    args = parser.parse_args()
    if args.update_lock and args.check:
        parser.error('--update-lock cannot be combined with --check')
    try:
        subprocess.run([sys.executable, str(K / 'scripts/refresh_catalog.py'), '--check'], check=True)
        fresh = current_lock()
        if args.update_lock:
            LOCK.write_text(yaml.safe_dump(fresh, allow_unicode=True, sort_keys=False, width=110))
        if not LOCK.exists() or yaml.safe_load(LOCK.read_text()) != fresh:
            raise ValueError('Source release lock is stale; review changes and use --update-lock')
        lock = yaml.safe_load(LOCK.read_text())
        for name in NAMES:
            if args.check:
                verify_package(SKILLS / name, manifest_for(name, lock))
            else:
                sync(name, lock)
        if not args.check:
            artifacts = [archive(name) for name in NAMES]
            (DIST / 'SHA256SUMS').write_text(''.join(f'{sha(p)[7:]}  {p.name}\n' for p in artifacts))
        print(f'OK: {len(NAMES)} independent {lock["channel"]} skills, {len(lock["knowledge_files"])} identical knowledge files, fixed lock and package digests')
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError, yaml.YAMLError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
