#!/usr/bin/env python3
"""Recompute the shipped synthetic examples; print JSON without writing files."""
import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
MODELS = ("Baseline LSTM", "BERT-base", "Our Method")
SEEDS = (42, 123, 456, 789, 1024)
DATASETS = ("IMDB", "SST-2", "AG News", "DBpedia")
PAIRS = (("Our Method", "Baseline LSTM"),
         ("Our Method", "BERT-base"),
         ("BERT-base", "Baseline LSTM"))


def read_runs(example):
    path = EXAMPLES / (example + "-runs.csv")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        metrics = tuple(key for key in reader.fieldnames if key not in ("model", "seed"))
        groups = {model: {} for model in MODELS}
        for row in reader:
            model, seed = row["model"], int(row["seed"])
            if model not in groups or seed in groups[model]:
                raise ValueError("Unknown model or duplicate model/seed")
            values = {key: float(row[key]) for key in metrics}
            if not all(math.isfinite(value) for value in values.values()):
                raise ValueError("Non-finite example value")
            groups[model][seed] = values
    if any(set(runs) != set(SEEDS) for runs in groups.values()):
        raise ValueError("Each model must have the five documented seed labels")
    return metrics, groups


def describe(values):
    return {"n": len(values), "mean": statistics.mean(values),
            "sd": statistics.stdev(values)}


def calculate(example):
    from scipy import stats

    metrics, groups = read_runs(example)
    summary = {}
    endpoints = {}
    for model, runs in groups.items():
        summary[model] = {
            metric: describe([runs[seed][metric] for seed in SEEDS])
            for metric in metrics
        }
        if example == "benchmark":
            # Preserve within-run covariance: average datasets within each run,
            # then calculate variation across the five independent model runs.
            endpoint = [statistics.mean(runs[seed][metric] for metric in DATASETS)
                        for seed in SEEDS]
            summary[model]["average"] = describe(endpoint)
        else:
            endpoint = [runs[seed]["accuracy"] for seed in SEEDS]
        endpoints[model] = endpoint
    comparisons = []
    for first, second in PAIRS:
        a, b = endpoints[first], endpoints[second]
        n1, n2 = len(a), len(b)
        df = n1 + n2 - 2
        pooled_sd = math.sqrt(((n1 - 1) * statistics.variance(a)
                              + (n2 - 1) * statistics.variance(b)) / df)
        result = stats.ttest_ind(a, b, equal_var=True, alternative="two-sided")
        comparisons.append({
            "first": first, "second": second, "df": df,
            "difference": statistics.mean(a) - statistics.mean(b),
            "t": float(result.statistic), "p": float(result.pvalue),
            "d": (statistics.mean(a) - statistics.mean(b)) / pooled_sd,
            "p_bonferroni": min(1.0, len(PAIRS) * float(result.pvalue)),
        })
    return {
        "example": example, "synthetic": True,
        "endpoint": "per-run mean across four datasets" if example == "benchmark" else "accuracy",
        "test": "independent, equal-variance, two-sided t-test",
        "alpha": 0.05, "family_size": len(PAIRS),
        "alpha_bonferroni": 0.05 / len(PAIRS),
        "summary": summary, "comparisons": comparisons,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example", choices=("usage", "benchmark"), required=True)
    args = parser.parse_args(argv)
    try:
        result = calculate(args.example)
    except ImportError:
        print("This example needs SciPy: python3 -m pip install scipy", file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
