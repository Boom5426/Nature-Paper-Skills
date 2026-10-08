"""Numerical contracts for statistical examples, independent of their generator."""
import csv
import importlib.util
import json
import math
import re
import statistics
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/research/results-analysis"
MODELS = ("Baseline LSTM", "BERT-base", "Our Method")
DATASETS = ("IMDB", "SST-2", "AG News", "DBpedia")
SEEDS = {42, 123, 456, 789, 1024}
PAIRS = (("Our Method", "Baseline LSTM"), ("Our Method", "BERT-base"),
         ("BERT-base", "Baseline LSTM"))
NUMBER = r"[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?"
HAVE_SCIPY = importlib.util.find_spec("scipy") is not None


def runs(example):
    with (SKILL / "examples" / (example + "-runs.csv")).open(newline="") as handle:
        return list(csv.DictReader(handle))


def values(rows, model, metric):
    return [float(row[metric]) for row in rows if row["model"] == model]


def endpoint(rows, model):
    return [statistics.mean(float(row[name]) for name in DATASETS)
            for row in rows if row["model"] == model]


def cells(text, model):
    for line in text.splitlines():
        parts = [cell.strip().replace("**", "") for cell in line.strip().strip("|").split("|")]
        if parts[0] == model:
            return parts[1:]
    raise AssertionError("Missing model row: " + model)


def pair_rows(text):
    result = {}
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        parts = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(parts) == 5 and parts[0] in [a + " vs " + b for a, b in PAIRS]:
            if parts[0] in result:
                raise AssertionError("Duplicate comparison row")
            result[parts[0]] = parts[1:]
    return result


def rounding_interval(token):
    # Preserve the declared decimal/scientific precision, including trailing zeros.
    mantissa, _, exponent = token.lower().partition("e")
    decimals = len(mantissa.partition(".")[2])
    unit = 10.0 ** ((int(exponent) if exponent else 0) - decimals)
    value = float(token)
    return value - unit / 2, value + unit / 2


class SourceDataTests(unittest.TestCase):
    def test_complete_finite_runs_preserve_seeds_and_metrics(self):
        for example, metrics in (("usage", ("accuracy", "f1_score", "training_time")),
                                 ("benchmark", DATASETS)):
            rows = runs(example)
            self.assertEqual(len(rows), 15)
            self.assertEqual({row["model"] for row in rows}, set(MODELS))
            for model in MODELS:
                selected = [row for row in rows if row["model"] == model]
                self.assertEqual(len(selected), 5)
                self.assertEqual({int(row["seed"]) for row in selected}, SEEDS)
                for metric in metrics:
                    self.assertTrue(all(math.isfinite(float(row[metric])) for row in selected))

    def assert_summary(self, token, data):
        match = re.fullmatch(r"(" + NUMBER + r")\s*±\s*(" + NUMBER + r")", token)
        self.assertIsNotNone(match, token)
        for printed, actual in zip(match.groups(),
                                   (statistics.mean(data), statistics.stdev(data))):
            lower, upper = rounding_interval(printed)
            self.assertLessEqual(lower - 1e-6, actual, token)
            self.assertLessEqual(actual, upper + 1e-6, token)

    def test_usage_table_matches_all_raw_metrics(self):
        text = (SKILL / "USAGE.md").read_text()
        rows = runs("usage")
        for model in MODELS:
            row = cells(text, model)
            self.assertEqual(len(row), 3)
            for token, metric in zip(row, ("accuracy", "f1_score", "training_time")):
                self.assert_summary(token, values(rows, model, metric))

    def test_benchmark_tables_use_variation_of_run_averages(self):
        rows = runs("benchmark")
        for model in MODELS:
            average_of_sd = statistics.mean(statistics.stdev(values(rows, model, name))
                                            for name in DATASETS)
            self.assertGreater(abs(statistics.stdev(endpoint(rows, model)) - average_of_sd), .1)
        for name in ("example-analysis-report.md", "example-results-section.md"):
            text = (SKILL / "examples" / name).read_text()
            for model in MODELS:
                row = cells(text, model)
                self.assertEqual(len(row), 5)
                for token, metric in zip(row[:4], DATASETS):
                    self.assert_summary(token, values(rows, model, metric))
                self.assert_summary(row[4], endpoint(rows, model))

    def test_descriptive_table_averages_deltas_and_resources(self):
        # Recompute every four-dataset mean/ablation delta, not rounded-column differences.
        for name in ("example-analysis-report.md", "example-results-section.md"):
            text = (SKILL / "examples" / name).read_text()
            for line in text.splitlines():
                parts = [part.strip().replace("**", "")
                         for part in line.strip().strip("|").split("|")]
                if len(parts) not in (6, 7):
                    continue
                if all(re.fullmatch(NUMBER, part) for part in parts[1:6]):
                    mean = statistics.mean(float(part) for part in parts[1:5])
                    lower, upper = rounding_interval(parts[5])
                    self.assertTrue(lower - 1e-8 <= mean <= upper + 1e-8, line)
                    if len(parts) == 7 and re.fullmatch("-" + NUMBER, parts[6]):
                        # Full-model mean is derived from the same raw benchmark runs.
                        full = statistics.mean(endpoint(runs("benchmark"), "Our Method"))
                        lower, upper = rounding_interval(parts[6].lstrip("-"))
                        self.assertTrue(lower - 1e-8 <= full - mean <= upper + 1e-8, line)
            time = {}
            for line in text.splitlines():
                parts = [part.strip() for part in line.strip().strip("|").split("|")]
                if (len(parts) >= 4 and parts[0] in MODELS
                        and re.fullmatch(NUMBER + "h", parts[1])):
                    time[parts[0]] = float(parts[1][:-1])
                    self.assertAlmostEqual(float(parts[3]), 4 * time[parts[0]])
            self.assertEqual(set(time), set(MODELS))
            reduction = 100 * (1 - time["Our Method"] / time["BERT-base"])
            reported = re.findall(r"训练时间减少\s*(" + NUMBER + r")%", text)
            self.assertTrue(reported)
            for token in reported:
                lower, upper = rounding_interval(token)
                self.assertTrue(lower <= reduction <= upper)

    def test_sd_se_example_has_correct_conversion(self):
        text = (SKILL / "references/common-pitfalls.md").read_text()
        sd = float(re.search(r"85\.3% ± (" + NUMBER + r")%（标准差，5 次运行）", text)[1])
        se = float(re.search(r"85\.3% ± (" + NUMBER + r")%（标准误，5 次运行", text)[1])
        self.assertAlmostEqual(se, sd / math.sqrt(5), delta=0.005)


@unittest.skipUnless(HAVE_SCIPY, "numerical P checks require SciPy (optional-helper CI installs it)")
class InferentialTests(unittest.TestCase):
    def assert_rounds_to(self, token, actual):
        lower, upper = rounding_interval(token)
        self.assertTrue(lower <= actual <= upper, (token, actual))

    def test_published_comparisons_and_helper_match_independent_raw_calculation(self):
        from scipy import stats
        for example, path in (("usage", SKILL / "USAGE.md"),
                              ("benchmark", SKILL / "examples/example-analysis-report.md")):
            rows = runs(example)
            table = pair_rows(path.read_text())
            self.assertEqual(set(table), {a + " vs " + b for a, b in PAIRS})
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts/example_statistics.py"),
                 "--example", example], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            actual_helper = json.loads(result.stdout)
            self.assertEqual(actual_helper["family_size"], len(PAIRS))
            self.assertEqual(actual_helper["alpha_bonferroni"], .05 / len(PAIRS))
            for pair, output in zip(PAIRS, actual_helper["comparisons"]):
                a, b = (endpoint(rows, pair[0]), endpoint(rows, pair[1])) if example == "benchmark" else (
                    values(rows, pair[0], "accuracy"), values(rows, pair[1], "accuracy"))
                expected = stats.ttest_ind(a, b, equal_var=True, alternative="two-sided")
                pooled = math.sqrt(((len(a) - 1) * statistics.variance(a)
                                    + (len(b) - 1) * statistics.variance(b))
                                   / (len(a) + len(b) - 2))
                d = (statistics.mean(a) - statistics.mean(b)) / pooled
                self.assertEqual((output["first"], output["second"]), pair)
                self.assertEqual(output["df"], len(a) + len(b) - 2)
                self.assertAlmostEqual(output["t"], expected.statistic, places=10)
                self.assertAlmostEqual(output["p"], expected.pvalue, places=12)
                self.assertAlmostEqual(output["d"], d, places=10)
                self.assertAlmostEqual(output["p_bonferroni"], min(1, 3 * expected.pvalue), places=12)
                for token, expected_number in zip(table[" vs ".join(pair)],
                                                 (expected.statistic, expected.pvalue, d,
                                                  min(1, 3 * expected.pvalue))):
                    self.assert_rounds_to(re.search(NUMBER + r"(?!.*" + NUMBER + ")", token)[0],
                                          expected_number)

    def test_prose_comparisons_use_the_same_data_as_their_tables(self):
        from scipy import stats
        for example, paths in (("usage", (SKILL / "USAGE.md",)),
                               ("benchmark", (SKILL / "examples/example-analysis-report.md",
                                              SKILL / "examples/example-results-section.md"))):
            rows = runs(example)
            endpoints = [values(rows, model, "accuracy") if example == "usage"
                         else endpoint(rows, model) for model in MODELS]
            expected = [stats.ttest_ind(endpoints[2], endpoints[i], equal_var=True)
                        for i in (0, 1)]
            for path in paths:
                text = path.read_text()
                # Upper-case P is used in the prose, lower-case p in the tables.
                matches = re.findall(r"t\(8\) = (" + NUMBER + r")[,，]\s*P = ("
                                     + NUMBER + r")", text)
                self.assertGreaterEqual(len(matches), 2, path)
                for index, (t, p) in enumerate(matches):
                    self.assert_rounds_to(t, expected[index % 2].statistic)
                    self.assert_rounds_to(p, expected[index % 2].pvalue)

    def test_summary_input_examples_recompute_t_and_p(self):
        from scipy import stats
        for name in ("common-pitfalls.md", "results-writing-guide.md"):
            text = (SKILL / "references" / name).read_text()
            line = next(line for line in text.splitlines() if "t(8) = 2.59" in line)
            # The example preserves means/SDs; it corrects the inferred significance.
            result = stats.ttest_ind_from_stats(85.3, 2.1, 5, 82.1, 1.8, 5, equal_var=True)
            t, p = re.search(r"t\(8\) = (" + NUMBER + r"), p = (" + NUMBER + r")", line).groups()
            self.assert_rounds_to(t, result.statistic)
            self.assert_rounds_to(p, result.pvalue)
        text = (SKILL / "references/statistical-methods.md").read_text()
        line = next(line for line in text.splitlines() if "t(18) = 3.66" in line)
        result = stats.ttest_ind_from_stats(85.3, 2.1, 10, 82.1, 1.8, 10, equal_var=True)
        t, p = re.search(r"t\(18\) = (" + NUMBER + r"), p = (" + NUMBER + r")", line).groups()
        self.assert_rounds_to(t, result.statistic)
        self.assert_rounds_to(p, result.pvalue)

    def test_repository_t_f_and_chisquare_p_values_respect_rounding(self):
        from scipy import stats
        patterns = [
            ("t", r"\bt\(("+NUMBER+r")\) = ("+NUMBER+r").*?\b[pP] ([=<]) ("+NUMBER+r")"),
            ("F", r"\bF\(("+NUMBER+r"), ("+NUMBER+r")\) = ("+NUMBER+r").*?\b[pP] ([=<]) ("+NUMBER+r")"),
            ("chi", r"(?:χ²|H)\(("+NUMBER+r")\) = ("+NUMBER+r").*?\b[pP] ([=<]) ("+NUMBER+r")"),
        ]
        checked = 0
        for folder in ("skills", "examples", "evals", "docs"):
            for path in (ROOT / folder).rglob("*.md"):
                for line_no, line in enumerate(path.read_text().splitlines(), 1):
                    for family, pattern in patterns:
                        for match in re.finditer(pattern, line):
                            groups = match.groups()
                            if family == "F":
                                df1, df2, statistic, operator, p = groups
                                tail = lambda value: stats.f.sf(value, float(df1), float(df2))
                            else:
                                df, statistic, operator, p = groups
                                tail = (lambda value: 2 * stats.t.sf(value, float(df))) if family == "t" else (
                                    lambda value: stats.chi2.sf(value, float(df)))
                            low_s, high_s = rounding_interval(statistic)
                            low_p, high_p = max(0.0, tail(high_s)), min(1.0, tail(low_s))
                            if operator == "<":
                                valid = low_p < float(p)
                            else:
                                printed_low, printed_high = rounding_interval(p)
                                valid = low_p <= printed_high and high_p >= printed_low
                            self.assertTrue(valid, f"{path}:{line_no}: {match[0]}")
                            checked += 1
        self.assertGreaterEqual(checked, 20)

    def test_exact_sign_test_tail_is_declared_correctly(self):
        from scipy import stats
        text = (SKILL / "references/statistical-methods.md").read_text()
        line = next(line for line in text.splitlines() if "精确双侧 Sign" in line)
        counts = re.search(r"在 (\d+) 个独立数据集中的 (\d+) 个", line)
        p = re.search(r"p = (" + NUMBER + ")", line)[1]
        self.assert_rounds_to(p, stats.binomtest(int(counts[2]), int(counts[1]), .5,
                                               alternative="two-sided").pvalue)

    def test_standard_error_and_mean_interval_follow_the_declared_inputs(self):
        from scipy import stats
        text = (SKILL / "references/statistical-methods.md").read_text()
        line = next(line for line in text.splitlines() if "标准误，n =" in line)
        se = re.search(r"± (" + NUMBER + r")%", line)[1]
        n = int(re.search(r"n = (\d+)", line)[1])
        sd = float(re.search(r"SD = (" + NUMBER + r")%", line)[1])
        self.assert_rounds_to(se, sd / math.sqrt(n))
        line = next(line for line in text.splitlines() if "95% CI:" in line)
        mean, lower, upper, sd, n = re.search(
            r'准确率为 (' + NUMBER + r')% \[95% CI: (' + NUMBER
            + r')%, (' + NUMBER + r')%\]（样本 SD = (' + NUMBER
            + r')%，n = (\d+)', line).groups()
        half_width = stats.t.ppf(.975, int(n)-1) * float(sd) / math.sqrt(int(n))
        self.assert_rounds_to(lower, float(mean) - half_width)
        self.assert_rounds_to(upper, float(mean) + half_width)

    def test_balanced_t_effect_size_interval(self):
        from scipy import stats, optimize
        path = ROOT / "skills/core/scientific-writing/references/imrad_structure.md"
        line = next(line for line in path.read_text().splitlines() if "t(48) = 3.21" in line)
        n = int(re.search(r"n = (\d+) per group", line)[1])
        t = float(re.search(r"t\(48\) = (" + NUMBER + ")", line)[1])
        d = re.search(r"Cohen's d = (" + NUMBER + ")", line)[1]
        interval = re.search(r"95% CI: (" + NUMBER + ")-(" + NUMBER + ")", line).groups()
        scale = math.sqrt(2 / n)
        self.assert_rounds_to(d, t * scale)
        for token, quantile in zip(interval, (.975, .025)):
            ncp = optimize.brentq(lambda value: stats.nct.cdf(t, 2*n-2, value) - quantile,
                                 -50, 50)
            self.assert_rounds_to(token, ncp * scale)


if __name__ == "__main__":
    unittest.main()
