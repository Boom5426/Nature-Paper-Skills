"""The results-analysis worked example must follow its printed means and SDs.

A pooled equal-n two-sample t-test on those means, SDs, and n = 5 is what the
example claims to have run. Both copies of the statistics — the analysis-report
table and the results-draft sentence — have to show that result.
"""
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USAGE = ROOT / "skills/research/results-analysis/USAGE.md"

# Two-tailed 0.001 critical value of t on df = 8.
T_CRIT_001 = 5.041


class ResultsAnalysisExampleTests(unittest.TestCase):
    def test_worked_example_matches_pooled_t_from_printed_means(self):
        n = 5
        our, our_sd = 93.5, 0.23
        baseline, baseline_sd = 86.2, 0.21
        bert, bert_sd = 91.3, 0.18

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

        text = USAGE.read_text(encoding="utf-8")
        table = text[text.index("### 主要对比"):text.index("### 多重比较校正")]
        draft = text[text.index("With five independent runs"):text.index("α' = 0.017).") + len("α' = 0.017).")]

        self.assertIn("| Our Method vs Baseline | t(8) = 52.41 | p < 0.001 | d = 33.15 |", table)
        self.assertIn("| Our Method vs BERT-base | t(8) = 16.84 | p < 0.001 | d = 10.65 |", table)
        self.assertIn(
            "by 7.3 points (two-sample t-test, t(8) = 52.41, P < 0.001, Cohen's d = 33.15) "
            "and BERT-base by 2.2 points (t(8) = 16.84, P < 0.001, Cohen's d = 10.65)",
            draft,
        )
        self.assertIn("Bonferroni correction for three comparisons (α' = 0.017)", draft)
        for copy in (table, draft):
            for stale in ("5.67", "3.59", "3.21", "2.03", "0.012"):
                self.assertNotIn(stale, copy)


if __name__ == "__main__":
    unittest.main()
