"""The results-analysis worked example must follow its printed means and SDs.

A pooled equal-n two-sample t-test on those means, SDs, and n = 5 is what the
example claims to have run. Both copies of the statistics — the analysis-report
table and the results-draft sentence — have to show that result.
"""
import csv
import math
import re
import statistics
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USAGE = ROOT / "skills/research/results-analysis/USAGE.md"

# Two-tailed 0.001 critical value of t on df = 8.
T_CRIT_001 = 5.041


class ResultsAnalysisExampleTests(unittest.TestCase):
    def test_worked_example_matches_pooled_t_from_printed_means(self):
        text = USAGE.read_text(encoding="utf-8")
        with (USAGE.parent / "examples/usage-runs.csv").open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        summaries = {}
        counts = []
        for model in ("Our Method", "Baseline LSTM", "BERT-base"):
            match = re.search(r"^- " + re.escape(model)
                              + r": ([0-9.]+)% ± ([0-9.]+)%$", text, re.MULTILINE)
            self.assertIsNotNone(match, model)
            observations = [float(row["accuracy"]) for row in rows
                            if row["model"] == model]
            counts.append(len(observations))
            self.assertEqual(counts[-1], 5)
            mean = statistics.mean(observations)
            sd = statistics.stdev(observations)
            self.assertEqual(float(match[1]), round(mean, 1))
            self.assertEqual(float(match[2]), round(sd, 2))
            summaries[model] = (mean, sd)
        self.assertEqual(len(set(counts)), 1)
        n = counts[0]
        our, our_sd = summaries["Our Method"]
        baseline, baseline_sd = summaries["Baseline LSTM"]
        bert, bert_sd = summaries["BERT-base"]

        baseline_sp = math.sqrt((our_sd ** 2 + baseline_sd ** 2) / 2)
        baseline_gap = our - baseline
        baseline_t = baseline_gap / (baseline_sp * math.sqrt(2 / n))
        baseline_d = baseline_gap / baseline_sp
        bert_sp = math.sqrt((our_sd ** 2 + bert_sd ** 2) / 2)
        bert_gap = our - bert
        bert_t = bert_gap / (bert_sp * math.sqrt(2 / n))
        bert_d = bert_gap / bert_sp

        self.assertEqual((round(baseline_t, 2), round(baseline_d, 2)), (52.41, 33.15))
        self.assertEqual((round(bert_t, 2), round(bert_d, 2)), (16.84, 10.65))
        self.assertGreater(abs(baseline_t), T_CRIT_001)
        self.assertGreater(abs(bert_t), T_CRIT_001)
        self.assertEqual(round(baseline_gap, 1), 7.3)
        self.assertEqual(round(bert_gap, 1), 2.2)

        table = re.search(r"### analysis-report\.md\s+```markdown\n(.*?)```", text, re.DOTALL)
        draft = re.search(r"### results-draft\.md\s+```markdown\n(.*?)```", text, re.DOTALL)
        self.assertIsNotNone(table)
        self.assertIsNotNone(draft)
        table = table[1]
        draft = " ".join(draft[1].split())

        self.assertIn("| Our Method vs Baseline LSTM | t(8) = 52.41 | p = 1.95e-11 | d = 33.15 |", table)
        self.assertIn("| Our Method vs BERT-base | t(8) = 16.84 | p = 1.56e-7 | d = 10.65 |", table)
        self.assertIn(
            "by 7.3 percentage points (equal-variance two-sided two-sample "
            "t-test, t(8) = 52.41, P = 1.95e-11, Cohen's d = 33.15) "
            "and BERT-base by 2.2 percentage points "
            "(t(8) = 16.84, P = 1.56e-07, Cohen's d = 10.65)",
            draft,
        )
        self.assertIn("Bonferroni correction over the three predefined pairwise comparisons", draft)
        for copy in (table, draft):
            for stale in ("5.67", "3.59", "3.21", "2.03", "0.012"):
                self.assertNotIn(stale, copy)


if __name__ == "__main__":
    unittest.main()
