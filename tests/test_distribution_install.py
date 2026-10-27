"""Portable helpers must survive Hermes' reserved machine-state exclusions."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DistributionInstall(unittest.TestCase):
    def test_helpers_survive_distribution_copy_and_execute_offline(self):
        # Hermes excludes these root directories during distribution install.
        # This deterministic regression supplements the native install smoke.
        reserved = {'.git', 'tools', 'cache', 'installs'}
        self.assertFalse((ROOT / 'tools').exists())
        with tempfile.TemporaryDirectory() as tmp:
            installed = Path(tmp) / 'profile'
            shutil.copytree(ROOT, installed,
                            ignore=lambda path, names: reserved if Path(path) == ROOT else set())
            helper = installed / 'helpers/evidence_lineage_check.py'
            self.assertTrue(helper.is_file())
            result = subprocess.run(
                [sys.executable, '-B', str(helper),
                 str(installed / 'examples/research-run-source-lineage.json'), '--json'],
                cwd=tmp, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for program in (ROOT / 'helpers').glob('*.py'):
                self.assertEqual(program.read_bytes(),
                                 (installed / 'helpers' / program.name).read_bytes())


if __name__ == '__main__':
    unittest.main()
