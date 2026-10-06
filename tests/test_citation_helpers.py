"""Exercise citation extraction, bibliography structure and input completeness."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/'skills/core/citation-verifier/scripts'
SPEC = importlib.util.spec_from_file_location('citation_syntax', SCRIPTS/'citation_syntax.py')
syntax = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(syntax)

VALID_BIB = '@article{known, author={Doe}, title={A Study}, journal={J}, year={2026}}\n'


class CitationHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.bib = self.write('refs.bib', VALID_BIB)
        self.tex = self.write('main.tex', r'\cite{known}')

    def write(self, name, text):
        path = self.base/name
        path.write_text(text, encoding='utf-8')
        return path

    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(SCRIPTS/script), *map(str, args)],
                              capture_output=True, text=True)

    def audit(self, text=None, *extra):
        if text is not None:
            self.bib.write_text(text)
        return self.run_script('audit_bib.py', '--bib', self.bib, '--tex', self.tex, *extra)

    def test_optional_arguments_and_wrapped_keys_are_scanned(self):
        self.tex.write_text('\\citep[see][p.~2]{first,\nsecond}\n\\citet*{third}')
        result = self.run_script('scan_citations.py', self.tex)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('cite_keys: 3', result.stdout)

    def test_comments_preserve_original_line_numbers_and_key_continuations(self):
        text = '% \\cite{ignored}\n\\citep[see]{fir% continuation\n st, second}\n'
        self.assertEqual(list(syntax.iter_citations(text)), [(2, 'first'), (2, 'second')])

    def test_escaped_percent_is_not_a_comment(self):
        text = r'50\% agrees with \cite{known}. % \cite{ignored}'
        self.assertEqual(list(syntax.iter_citations(text)), [(1, 'known')])
        text = '\\\\% real comment \\cite{ignored}\n\\cite{known}'
        self.assertEqual(list(syntax.iter_citations(text)), [(2, 'known')])

    def test_escaped_commands_and_line_break_before_citation(self):
        self.assertEqual(list(syntax.iter_citations(r'\\cite{literal}')), [])
        self.assertEqual(list(syntax.iter_citations(r'\\\cite{known}')), [(1, 'known')])

    def test_scanner_and_auditor_extract_same_common_forms(self):
        self.tex.write_text('\\citep[see][p.~2]{known,\nundefined}\n% \\cite{ignored}')
        scan = self.run_script('scan_citations.py', self.tex)
        audit = self.audit()
        self.assertIn('cite_keys: 2', scan.stdout)
        self.assertEqual(audit.returncode, 1)
        self.assertIn('\\cite{undefined} has no entry', audit.stdout)
        self.assertNotIn('\\cite{ignored} has no entry', audit.stdout)

    def test_scanner_missing_input_fails_even_with_other_files(self):
        for paths in [(self.base/'missing.tex',), (self.tex, self.base/'missing.tex')]:
            with self.subTest(paths=paths):
                result = self.run_script('scan_citations.py', *paths)
                self.assertEqual(result.returncode, 2)
                self.assertIn('incomplete', result.stderr)
                self.assertNotIn('Summary', result.stdout)

    def test_empty_scan_directory_is_incomplete(self):
        directory = self.base/'empty'
        directory.mkdir()
        result = self.run_script('scan_citations.py', directory)
        self.assertEqual(result.returncode, 2)
        self.assertIn('incomplete', result.stderr)

    def test_valid_bibliography_has_no_blocking_problem(self):
        result = self.audit()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('BLOCKING problems : 0', result.stdout)

    def test_unclosed_entry_and_field_are_blocking(self):
        for text in (VALID_BIB.rstrip()[:-1], VALID_BIB.replace('year={2026}', 'year={2026')):
            with self.subTest(text=text):
                result = self.audit(text)
                self.assertEqual(result.returncode, 1)
                self.assertIn('Unclosed', result.stdout)
                self.assertNotIn('No blocking problem', result.stdout)

    def test_quoted_fields_and_numeric_year_are_accepted(self):
        result = self.audit('@article{known, author="Doe", title="A {Nested} Study", journal="J", year=2026}\n')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_nested_and_escaped_braces_are_not_truncated(self):
        text = r'@article{known, author={Doe}, title={A {Nested} Study with \{literal\}}, journal={J}, year={2026}}'
        result = self.audit(text)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_entry_like_text_inside_value_is_not_another_entry(self):
        text = r'@article{known, author={Doe}, title={A @article{fake, title={Example}}}, journal={J}, year={2026}}'
        result = self.audit(text)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(': 1 entries', result.stdout)

    def test_unsupported_values_and_malformed_fields_fail_explicitly(self):
        for text in (
            '@article(known, title={A})',
            '@article{known, title=some_macro}',
            '@article{known, title={A} # {B}}',
            '@article{known, title={A} year={2026}}',
            '@article{known, title="Unclosed}',
            'This is not a bibliography',
        ):
            with self.subTest(text=text):
                result = self.audit(text)
                self.assertEqual(result.returncode, 1)
                self.assertIn('BLOCKING', result.stdout)

    def test_partially_missing_tex_inputs_are_blocking(self):
        result = self.audit(None, '--tex', self.base/'missing.tex')
        self.assertEqual(result.returncode, 1)
        self.assertIn('scan incomplete', result.stdout)
        self.assertNotIn('every cited key is defined', result.stdout)

    def test_empty_requested_glob_is_blocking(self):
        result = self.audit(None, '--tex', str(self.base/'missing-*.tex'))
        self.assertEqual(result.returncode, 1)
        self.assertIn('No file matches requested', result.stdout)

    def test_omitting_tex_deliberately_skips_citation_comparison(self):
        result = self.run_script('audit_bib.py', '--bib', self.bib)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('skipped: no --tex given', result.stdout)
