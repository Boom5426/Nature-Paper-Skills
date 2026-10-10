"""Check the AI-tell detector shipped with scientific-prose-style."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'skills/core/scientific-prose-style/scripts/ai_tells.py'
SPEC = importlib.util.spec_from_file_location('nps_ai_tells', SCRIPT)
tells = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tells)


class AiTellsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def scan(self, content, name='draft.tex'):
        path = self.base/name
        path.write_text(content)
        return tells.scan([path])

    def counts(self, report):
        return {t['key']: t['count'] for t in report['tells']}

    def located(self, report, tell):
        return [loc for loc in report['locations'] if loc['tell'].startswith(tell)]

    def test_latex_comments_and_citations_are_not_scanned(self):
        report = self.scan('% delve into the pivotal tapestry\nThe model \\cite{delve2024} predicts responses.\n')
        self.assertEqual(sum(self.counts(report).values()), 0)

    def test_rare_tells_are_flagged_at_every_occurrence(self):
        report = self.scan('This is a decision problem in its own right. In this way, it works.\n')
        flags = {t['key']: t['flag'] for t in report['tells'] if t['count']}
        self.assertEqual(flags['in its own right'], 'check every occurrence')
        self.assertEqual(flags['In this way,'], 'check every occurrence')

    def test_common_tells_are_not_called_dense_in_a_short_passage(self):
        report = self.scan('Notably, A rose. Notably, B fell. Notably, C held.\n')
        flag = next(t['flag'] for t in report['tells'] if t['key'] == 'notably')
        self.assertFalse(flag.startswith('dense'))

    def test_common_tells_are_dense_only_well_above_the_corpus_rate(self):
        filler = ' '.join(['cells respond to perturbation'] * 400)
        report = self.scan(filler + ' Notably, A. Notably, B. Notably, C.\n')
        flag = next(t['flag'] for t in report['tells'] if t['key'] == 'notably')
        self.assertTrue(flag.startswith('dense'), flag)

    def test_coined_compounds_are_reported_once_with_their_count(self):
        report = self.scan('We use deployment-available priors and deployment-available labels.\n')
        hits = self.located(report, 'coined compound modifier')
        self.assertEqual(len(hits), 1)
        self.assertIn('x2', hits[0]['tell'])

    def test_bold_sentences_are_flagged_but_short_bold_terms_are_not(self):
        report = self.scan('\\textbf{Together these results extend our understanding of cells.} \\textbf{Note}\n')
        self.assertEqual(len(self.located(report, 'bold sentence')), 1)

    def test_more_than_one_semicolon_in_a_paragraph_is_flagged(self):
        report = self.scan('A rose; B fell.\n\nC rose; D fell; E held.\n')
        hits = self.located(report, 'semicolons in one paragraph')
        self.assertEqual([h['where'] for h in hits], ['draft.tex:3'])

    def test_latex_triple_hyphen_counts_as_em_dash(self):
        report = self.scan('The effect --- small but real --- held.\n')
        self.assertEqual(self.counts(report)['em dash'], 2)

    def test_rare_family_matches_the_rare_threshold(self):
        for tell in tells.TELLS:
            self.assertIsNotNone(tell.corpus_per_10k, tell.key)
            if tell.family == 'rare':
                self.assertLessEqual(tell.corpus_per_10k, tells.RARE_PER_10K, tell.key)

    def test_cli_refuses_to_overwrite_json_and_rejects_missing_files(self):
        draft = self.base/'draft.md'
        draft.write_text('Plain text.\n')
        existing = self.base/'report.json'
        existing.write_text('{}')
        for args in ([str(draft), '--json', str(existing)], [str(self.base/'missing.md')]):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                tells.main(args)
        out = self.base/'new.json'
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(tells.main([str(draft), '--json', str(out)]), 0)
        self.assertIn('tells', json.loads(out.read_text()))


if __name__ == '__main__':
    unittest.main()
