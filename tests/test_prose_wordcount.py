"""Check file expansion/count boundaries; real detex coverage when installed."""
import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'skills/core/draft-marker-discipline/scripts/prose_wordcount.py'
SPEC = importlib.util.spec_from_file_location('nps_wordcount', SCRIPT)
words = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(words)


class ProseWordcountTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def write(self, name, content):
        path = self.base/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_repeated_inputs_are_expanded_each_time(self):
        self.write('shared.tex', 'Alpha beta.')
        main = self.write('main.tex', '\\input{shared}\n\\input{shared}')
        self.assertEqual(words.resolve_inputs(main).split(), ['Alpha', 'beta.', 'Alpha', 'beta.'])

    def test_nested_inputs_use_manuscript_root(self):
        main = self.write('main.tex', r'\input{sections/a}')
        self.write('sections/a.tex', r'Alpha \input{sections/b}')
        self.write('sections/b.tex', 'beta gamma.')
        self.assertEqual(words.resolve_inputs(main).split(), ['Alpha', 'beta', 'gamma.'])

    def test_commented_inputs_are_never_followed(self):
        main = self.write('main.tex', '% \\input{does-not-exist}\nAlpha % \\input{also-missing}\nbeta.')
        self.assertEqual(words.resolve_inputs(main).split(), ['Alpha', 'beta.'])

    def test_comments_do_not_mark_later_valid_inputs_as_seen(self):
        self.write('shared.tex', 'Alpha beta.')
        main = self.write('main.tex', '% \\input{shared}\n\\input{shared}')
        self.assertEqual(words.resolve_inputs(main).split(), ['Alpha', 'beta.'])

    def test_cycles_and_missing_inputs_fail_the_count(self):
        main = self.write('main.tex', r'\input{main}')
        with self.assertRaisesRegex(SystemExit, 'cyclic input'):
            words.resolve_inputs(main)
        main.write_text(r'\input{missing}')
        with self.assertRaisesRegex(SystemExit, 'word count incomplete'):
            words.resolve_inputs(main)

    def test_percent_escaping_and_continuation(self):
        text = '50\\% useful. % hidden\n Next.\\\\% hidden\nLast.'
        self.assertEqual(words.strip_comments(text), '50\\% useful. Next.\\\\Last.')

    def test_existing_non_tex_extension_is_preserved(self):
        self.write('shared.ltx', 'Alpha beta.')
        main = self.write('main.tex', r'\input{shared.ltx}')
        self.assertEqual(words.resolve_inputs(main).split(), ['Alpha', 'beta.'])

    def test_extra_is_excluded_with_default_or_explicit_order(self):
        sections = self.base/'sections'
        self.write('sections/00-abstract.tex', 'Abstract words.')
        self.write('sections/01-body.tex', 'Three body words.')
        # External renderer double for plain-text fixtures; checks main's totals.
        def renderer(argv, **kwargs):
            return subprocess.CompletedProcess(argv, 0, kwargs['input'], '')
        for extra_args in ([], ['--order', '00-abstract,01-body']):
            with self.subTest(extra_args=extra_args):
                output = io.StringIO()
                with patch.object(words.shutil, 'which', return_value='/detex'), \
                     patch.object(words.subprocess, 'run', side_effect=renderer), \
                     contextlib.redirect_stdout(output):
                    code = words.main(['--sections', str(sections), '--extra', '00-abstract', *extra_args])
                self.assertEqual(code, 0)
                self.assertRegex(output.getvalue(), r'body total\s+3\b')
                self.assertRegex(output.getvalue(), r'00-abstract\s+2\s+\(outside')

    @unittest.skipUnless(shutil.which('detex'), 'detex is an optional dependency')
    def test_real_detex_cli_counts_repeated_commented_nested_and_extra_inputs(self):
        self.write('shared.tex', 'Alpha beta.')
        repeat = self.write('repeat.tex', '\\input{shared}\n\\input{shared}')
        self.write('hidden.tex', 'Secret hidden text.')
        comment = self.write('comment.tex', '% \\input{hidden}\nVisible words.')
        nested = self.write('main.tex', '\\documentclass{article}\n\\begin{document}\n\\input{sections/a}\n\\end{document}')
        self.write('sections/a.tex', r'Alpha \input{sections/b}')
        self.write('sections/b.tex', 'beta gamma.')
        for path, expected in [(repeat, 4), (comment, 2), (nested, 3)]:
            with self.subTest(path=path):
                result = subprocess.run([sys.executable, str(SCRIPT), '--file', str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertRegex(result.stdout, rf'body total\s+{expected}\b')
        self.write('budget/00-abstract.tex', 'Abstract words.')
        self.write('budget/01-body.tex', 'Three body words.')
        result = subprocess.run([sys.executable, str(SCRIPT), '--sections', str(self.base/'budget'), '--extra', '00-abstract'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r'body total\s+3\b')
