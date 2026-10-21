"""Installer behavior in disposable roots; never write the real agent directories."""
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

K = Path(__file__).resolve().parents[1]
S = K.parents[1]
spec = importlib.util.spec_from_file_location('suite_installer', S / 'scripts/install_skills.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallSkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='armbian-install-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_installer(self, *args):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = installer.main(args)
        return code, output.getvalue(), errors.getvalue()

    def test_user_roots_match_each_agent_without_repurposing_home(self):
        with patch.object(installer.Path, 'home', return_value=self.root):
            roots = installer.destinations('both', 'user', None, None)
        self.assertEqual(roots, [('codex', self.root / '.agents/skills'),
                                 ('claude', self.root / '.claude/skills')])

    def test_both_agents_install_complete_independent_copies_from_any_cwd(self):
        result = subprocess.run(['bash', str(S / 'install.sh'), '--agent', 'both', '--scope', 'project',
                                 '--project-dir', str(self.root / 'project with spaces')],
                                cwd=self.root, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        for folder in ['.agents', '.claude']:
            for name in installer.NAMES:
                dest = self.root / 'project with spaces' / folder / 'skills' / name
                self.assertEqual(installer.fingerprint(dest), installer.fingerprint(S / 'skills' / name))
                fixture = K / 'fixtures/rk3588-gpu.json'
                run = subprocess.run([sys.executable, '-I', str(dest / 'scripts/reference-match/match.py'),
                                      '--input', str(fixture), '--kind', 'board'],
                                     cwd=self.root, capture_output=True, text=True, timeout=15)
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_existing_late_member_prevents_all_copies(self):
        target = self.root / 'skills' / installer.NAMES[-1]
        target.mkdir(parents=True)
        (target / 'keep').write_text('original')
        code, _, _ = self.run_installer('--agent', 'codex', '--dest', str(target.parent))
        self.assertEqual(code, 1)
        self.assertEqual(list(target.parent.iterdir()), [target])
        self.assertEqual((target / 'keep').read_text(), 'original')

    def test_dry_run_creates_no_directories(self):
        code, output, error = self.run_installer('--agent', 'both', '--scope', 'project',
                                               '--project-dir', str(self.root / 'not-created'), '--dry-run')
        self.assertEqual(code, 0, error)
        self.assertIn('no files changed', output)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_replace_preserves_old_install_outside_discovery_and_removes_stale_files(self):
        dest = self.root / 'skills'
        name = installer.NAMES[0]
        old = dest / name
        old.mkdir(parents=True)
        (old / 'obsolete').write_text('preserved content')
        code, output, error = self.run_installer('--agent', 'claude', '--dest', str(dest),
                                               '--skill', name, '--replace')
        self.assertEqual(code, 0, error)
        self.assertFalse((old / 'obsolete').exists())
        backups = list((self.root / 'armbian-skills-backups').glob('*/' + name + '/obsolete'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'preserved content')
        self.assertEqual(installer.fingerprint(old), installer.fingerprint(S / 'skills' / name))
        self.assertIn('Previous installation backup:', output)

    def test_failed_second_publish_rolls_back_new_and_old_directories(self):
        dest = self.root / 'skills'
        old = dest / installer.NAMES[0]
        old.mkdir(parents=True)
        (old / 'keep').write_text('original')
        real_replace = installer.os.replace
        def fail_second(source, target):
            if target == dest / installer.NAMES[1]:
                raise OSError('simulated publish failure')
            return real_replace(source, target)
        with patch.object(installer.os, 'replace', side_effect=fail_second):
            code, _, error = self.run_installer('--agent', 'codex', '--dest', str(dest),
                                               '--skill', installer.NAMES[0], '--skill', installer.NAMES[1], '--replace')
        self.assertEqual(code, 1)
        self.assertIn('simulated publish failure', error)
        self.assertEqual((old / 'keep').read_text(), 'original')
        self.assertFalse((old / 'SKILL.md').exists())
        self.assertFalse((dest / installer.NAMES[1]).exists())

    def test_existing_symlink_and_source_overlap_are_not_replaced(self):
        dest = self.root / 'skills'
        dest.mkdir()
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'keep').write_text('original')
        (dest / installer.NAMES[0]).symlink_to(outside, target_is_directory=True)
        code, _, _ = self.run_installer('--agent', 'codex', '--dest', str(dest), '--replace')
        self.assertEqual(code, 1)
        self.assertEqual((outside / 'keep').read_text(), 'original')
        code, _, _ = self.run_installer('--agent', 'codex', '--dest', str(S / 'skills'), '--replace', '--dry-run')
        self.assertEqual(code, 1)

    def test_ambiguous_custom_destination_is_rejected_without_writes(self):
        code, _, _ = self.run_installer('--agent', 'both', '--dest', str(self.root / 'skills'))
        self.assertEqual(code, 1)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
