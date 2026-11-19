import csv
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from unicode_confusable_list import scan

ROOT = Path(__file__).resolve().parent
FIX = ROOT / 'fixtures'


class ConfusableTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'unicode_confusable_list.py'), *map(str, args)],
                              text=True, capture_output=True)

    def fixture(self, name):
        return scan((FIX / name).read_text(encoding='utf-8'))

    def test_ascii_clean(self):
        self.assertEqual(self.fixture('clean.txt'), [])

    def test_cyrillic(self):
        rows = self.fixture('cyrillic.txt')
        self.assertEqual([r['ascii_target'] for r in rows], list('AaCc'))
        self.assertEqual([r['column'] for r in rows], [2, 5, 8, 11])
        self.assertEqual(rows[0]['codepoint'], 'U+0410')

    def test_greek(self):
        rows = self.fixture('greek.txt')
        self.assertEqual([r['ascii_target'] for r in rows], list('OoPp'))
        self.assertEqual(rows[0]['codepoint'], 'U+039F')

    def test_shared_group_and_latin_lookalike(self):
        rows = self.fixture('mixed.txt')
        self.assertEqual(rows[0]['group_codepoints'], rows[1]['group_codepoints'])
        self.assertEqual((rows[2]['line'], rows[2]['column'], rows[2]['offset']), (2, 6, 9))
        self.assertEqual(rows[2]['codepoint'], 'U+017F')

    def test_offsets_are_codepoints_not_bytes(self):
        rows = scan('\U0001f642\u0410\r\n\u0391')
        self.assertEqual([(r['line'], r['column'], r['offset']) for r in rows], [(1, 2, 1), (2, 1, 4)])

    def test_outside_subset_ignored(self):
        self.assertEqual(scan('\u2603\u00e9\u0301'), [])

    def test_cli_findings_success_and_no_mutation(self):
        path = FIX / 'mixed.txt'
        before = path.read_bytes()
        result = self.cli(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(csv.DictReader(io.StringIO(result.stdout)))), 3)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(result.stdout, self.cli(path).stdout)

    def test_bad_utf8_and_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.txt'
            path.write_bytes(b'\xff')
            self.assertNotEqual(self.cli(path).returncode, 0)
        self.assertNotEqual(self.cli(FIX / 'absent.txt').returncode, 0)

    def test_help_and_empty(self):
        self.assertEqual(self.cli('--help').returncode, 0)
        self.assertEqual(scan(''), [])


if __name__ == '__main__':
    unittest.main()
