"""Tests for skills/figure/nature-figure/scripts/figure_source_data.py.

The point of that module is what it *refuses*, so most of these tests assert on
refusal paths: a bad value must stop the run and name the row, and it must never
be quietly dropped from the data a panel is drawn from.

Standard library only: the CI runner is a bare python 3.11 with no pip step.
"""

import ast
import hashlib
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "figure" / "nature-figure" / "scripts" / "figure_source_data.py"


def load_module():
    """Load the script as a module without leaving a __pycache__ beside it.

    `importlib` would write bytecode into the skill's scripts/ directory, which
    tests/test_license_shipping.py reads as a file the ATTRIBUTION notice says is
    absent. Compiling the source here keeps the skill tree clean.
    """
    module = types.ModuleType("figure_source_data")
    module.__file__ = str(SCRIPT)
    sys.modules[module.__name__] = module
    exec(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec"), module.__dict__)
    return module


fsd = load_module()


class TempFileMixin(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def write(self, name, text, *, binary=None):
        path = self.dir / name
        if binary is not None:
            path.write_bytes(binary)
        else:
            path.write_text(text, encoding="utf-8")
        return path

    def run_cli(self, *argv):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *[str(item) for item in argv]],
            check=False,
            capture_output=True,
            text=True,
        )


class ReadTableTests(TempFileMixin):
    def test_reads_csv_and_hashes_the_exact_bytes(self):
        path = self.write("d.csv", "gene,value\nA,1.5\nB,2.5\n")
        table = fsd.read_table(path)

        self.assertEqual(table.columns, ("gene", "value"))
        self.assertEqual(table.rows_input, 2)
        self.assertEqual(table.sha256, hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual([r.number for r in table.records], [1, 2])
        self.assertEqual([r.line for r in table.records], [2, 3])

    def test_reads_tsv_by_suffix(self):
        path = self.write("d.tsv", "gene\tvalue\nA\t1\n")
        self.assertEqual(fsd.read_table(path).records[0].values, {"gene": "A", "value": "1"})

    def test_unknown_suffix_is_blocked_not_guessed(self):
        path = self.write("d.dat", "gene,value\nA,1\n")
        with self.assertRaises(fsd.SourceDataBlocked) as ctx:
            fsd.read_table(path)
        self.assertIn("--delimiter", str(ctx.exception))

    def test_missing_file_is_blocked(self):
        with self.assertRaises(fsd.SourceDataBlocked):
            fsd.read_table(self.dir / "absent.csv")

    def test_undecodable_bytes_are_blocked(self):
        path = self.write("d.csv", "", binary=b"gene,value\n\xff\xfe,1\n")
        with self.assertRaises(fsd.SourceDataBlocked) as ctx:
            fsd.read_table(path)
        self.assertIn("UTF-8", str(ctx.exception))

    def test_empty_file_is_refused(self):
        with self.assertRaises(fsd.SourceDataRefused):
            fsd.read_table(self.write("d.csv", ""))

    def test_duplicate_columns_are_refused(self):
        path = self.write("d.csv", "value,value\n1,2\n")
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            fsd.read_table(path)
        self.assertIn("duplicate column names", str(ctx.exception))

    def test_ragged_row_is_refused_and_named(self):
        path = self.write("d.csv", "gene,value\nA,1\nB\nC,3\n")
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            fsd.read_table(path)
        message = str(ctx.exception)
        self.assertIn("record 2 (line 3)", message)
        self.assertIn("header has 2", message)


class RequireColumnsTests(TempFileMixin):
    def test_names_every_missing_column(self):
        table = fsd.read_table(self.write("d.csv", "gene,value\nA,1\n"))
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            fsd.require_columns(table, ["gene", "padj", "log2fc"])
        message = str(ctx.exception)
        self.assertIn("padj", message)
        self.assertIn("log2fc", message)
        self.assertNotIn("missing required column(s): gene", message)

    def test_accepts_a_complete_set(self):
        table = fsd.read_table(self.write("d.csv", "gene,value\nA,1\n"))
        self.assertIsNone(fsd.require_columns(table, ["gene", "value"]))


class CoerceNumericRefusalTests(TempFileMixin):
    """The core contract: bad numeric cells stop the run, they are not dropped."""

    def coerce(self, body, columns=("value",)):
        table = fsd.read_table(self.write("d.csv", "gene,value\n" + body))
        return fsd.coerce_numeric(table.records, columns, source=table.name)

    def test_empty_cell_is_refused_and_named(self):
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            self.coerce("A,1\nB,\nC,3\n")
        message = str(ctx.exception)
        self.assertIn("record 2 (line 3)", message)
        self.assertIn("empty", message)

    def test_nan_is_refused(self):
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            self.coerce("A,1\nB,nan\n")
        self.assertIn("non-finite", str(ctx.exception))
        self.assertIn("record 2", str(ctx.exception))

    def test_inf_is_refused(self):
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            self.coerce("A,1\nB,inf\n")
        self.assertIn("non-finite", str(ctx.exception))

    def test_non_numeric_text_is_refused(self):
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            self.coerce("A,1\nB,high\n")
        self.assertIn("not a number", str(ctx.exception))

    def test_bad_rows_are_never_returned_as_a_shortened_table(self):
        # If this module ever degrades to dropping, it would return the two good
        # rows instead of raising, and n would silently fall from 3 to 2.
        with self.assertRaises(fsd.SourceDataRefused):
            self.coerce("A,1\nB,nan\nC,3\n")

    def test_every_offending_row_is_listed_not_only_the_first(self):
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            self.coerce("A,nan\nB,2\nC,\n")
        message = str(ctx.exception)
        self.assertIn("record 1 (line 2)", message)
        self.assertIn("record 3 (line 4)", message)
        self.assertIn("2 missing or non-finite", message)

    def test_long_lists_are_truncated_with_a_count(self):
        body = "".join(f"G{index},nan\n" for index in range(20))
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            self.coerce(body)
        self.assertIn("and 8 more", str(ctx.exception))

    def test_clean_table_coerces_to_floats(self):
        rows = self.coerce("A,1\nB,2.5\n")
        self.assertEqual([row.values["value"] for row in rows], [1.0, 2.5])

    def test_zero_rows_is_refused(self):
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            self.coerce("")
        self.assertIn("zero rows", str(ctx.exception))


class ExclusionTests(TempFileMixin):
    """figure-style section 1.1: an excluded row enters no summary statistic."""

    TABLE = (
        "sample,value,qc\n"
        "S1,10,\n"
        "S2,20,\n"
        "S3,9000,failed QC\n"
        "S4,30,0\n"
    )

    def test_flagged_rows_are_partitioned_out_with_their_reason(self):
        table = fsd.read_table(self.write("d.csv", self.TABLE))
        kept, excluded = fsd.partition_excluded(table, "qc")

        self.assertEqual([row.values["sample"] for row in kept], ["S1", "S2", "S4"])
        self.assertEqual(len(excluded), 1)
        self.assertEqual(excluded[0].number, 3)
        self.assertEqual(excluded[0].reason, "qc=failed QC")

    def test_excluded_value_never_reaches_the_summary(self):
        table = fsd.read_table(self.write("d.csv", self.TABLE))
        kept, _ = fsd.partition_excluded(table, "qc")
        used = fsd.coerce_numeric(kept, ["value"], source=table.name)
        summary = fsd.summarize(used, "value")

        self.assertEqual(summary["n"], 3)
        self.assertEqual(summary["mean"], 20.0)
        self.assertEqual(summary["max"], 30.0)

    def test_an_excluded_row_may_hold_a_blank_value_without_refusing(self):
        # The excluded row is removed before coercion, so its empty cell is not
        # a reason to refuse the whole table.
        table = fsd.read_table(self.write("d.csv", "sample,value,qc\nS1,10,\nS2,,dropped\n"))
        kept, excluded = fsd.partition_excluded(table, "qc")
        used = fsd.coerce_numeric(kept, ["value"], source=table.name)
        self.assertEqual(len(used), 1)
        self.assertEqual(len(excluded), 1)

    def test_a_blank_value_in_a_kept_row_still_refuses(self):
        table = fsd.read_table(self.write("d.csv", "sample,value,qc\nS1,,\nS2,2,dropped\n"))
        kept, _ = fsd.partition_excluded(table, "qc")
        with self.assertRaises(fsd.SourceDataRefused):
            fsd.coerce_numeric(kept, ["value"], source=table.name)

    def test_missing_flag_column_is_refused(self):
        table = fsd.read_table(self.write("d.csv", "sample,value\nS1,1\n"))
        with self.assertRaises(fsd.SourceDataRefused):
            fsd.partition_excluded(table, "qc")

    def test_summarize_refuses_uncoerced_records(self):
        table = fsd.read_table(self.write("d.csv", "sample,value\nS1,1\n"))
        with self.assertRaises(fsd.SourceDataRefused) as ctx:
            fsd.summarize(table.records, "value")
        self.assertIn("coerce_numeric", str(ctx.exception))

    def test_sd_is_none_at_n_one_rather_than_zero(self):
        table = fsd.read_table(self.write("d.csv", "sample,value\nS1,1\n"))
        used = fsd.coerce_numeric(table.records, ["value"])
        self.assertIsNone(fsd.summarize(used, "value")["sd"])


class FirstSeenTests(unittest.TestCase):
    def test_preserves_order_and_removes_duplicates(self):
        self.assertEqual(fsd.first_seen(["b", "a", "b", "c"]), ["b", "a", "c"])


class QaPrefixTests(TempFileMixin):
    def test_strips_figure_and_qa_suffixes(self):
        self.assertEqual(fsd.qa_prefix(self.dir / "fig1.svg").name, "fig1")
        self.assertEqual(fsd.qa_prefix(self.dir / "fig1.qa.json").name, "fig1")
        self.assertEqual(fsd.qa_prefix(self.dir / "fig1").name, "fig1")


class CliTests(TempFileMixin):
    CLEAN = "sample,value,group,qc\nS1,10,a,\nS2,20,a,\nS3,9000,b,failed QC\nS4,30,b,0\n"

    def qa_from(self, prefix):
        return json.loads((self.dir / f"{prefix}.qa.json").read_text())

    def test_clean_run_writes_a_traceable_qa_record(self):
        source = self.write("d.csv", self.CLEAN)
        result = self.run_cli(
            "--input", source,
            "--output", self.dir / "fig1",
            "--require", "sample,value",
            "--numeric", "value",
            "--exclude-column", "qc",
            "--summarize", "value",
            "--category", "group",
            "--figure", "Figure 1a",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        qa = self.qa_from("fig1")

        self.assertEqual(qa["status"], "ok")
        self.assertEqual(qa["figure"], "Figure 1a")
        self.assertEqual(qa["rows_input"], 4)
        self.assertEqual(qa["rows_used"], 3)
        self.assertEqual(qa["rows_excluded"], 1)
        self.assertEqual(qa["rows_input"], qa["rows_used"] + qa["rows_excluded"])
        self.assertEqual(qa["exclusions"][0]["reason"], "qc=failed QC")
        self.assertEqual(qa["source"]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
        self.assertEqual(qa["source"]["file"], "d.csv")
        self.assertEqual(qa["summaries"]["value"]["n"], 3)
        self.assertEqual(qa["summaries"]["value"]["mean"], 20.0)
        self.assertEqual(qa["categories"]["group"], ["a", "b"])

    def test_qa_hash_changes_when_the_source_changes(self):
        source = self.write("d.csv", self.CLEAN)
        self.run_cli("--input", source, "--output", self.dir / "f", "--numeric", "value",
                     "--exclude-column", "qc", "--quiet")
        first = self.qa_from("f")["source"]["sha256"]
        source.write_text(self.CLEAN.replace("S1,10", "S1,11"), encoding="utf-8")
        self.run_cli("--input", source, "--output", self.dir / "f", "--numeric", "value",
                     "--exclude-column", "qc", "--quiet")
        self.assertNotEqual(first, self.qa_from("f")["source"]["sha256"])

    def test_refusal_exits_two_and_overwrites_a_stale_passing_record(self):
        good = self.write("good.csv", "sample,value\nS1,1\nS2,2\n")
        ok = self.run_cli("--input", good, "--output", self.dir / "fig2", "--numeric", "value", "--quiet")
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertEqual(self.qa_from("fig2")["status"], "ok")

        bad = self.write("bad.csv", "sample,value\nS1,1\nS2,nan\n")
        result = self.run_cli("--input", bad, "--output", self.dir / "fig2", "--numeric", "value")
        self.assertEqual(result.returncode, 2)
        qa = self.qa_from("fig2")
        self.assertEqual(qa["status"], "refused")
        self.assertEqual(qa["rows_used"], 0)
        self.assertIn("non-finite", qa["error"])
        self.assertIn("record 2", qa["error"])

    def test_missing_column_exits_two_and_names_it(self):
        source = self.write("d.csv", "sample,value\nS1,1\n")
        result = self.run_cli("--input", source, "--output", self.dir / "f", "--require", "padj")
        self.assertEqual(result.returncode, 2)
        self.assertIn("padj", result.stderr)
        self.assertEqual(self.qa_from("f")["status"], "refused")

    def test_unreadable_source_exits_three_and_records_blocked_not_a_pass(self):
        result = self.run_cli(
            "--input", self.dir / "absent.csv", "--output", self.dir / "f", "--numeric", "value"
        )
        self.assertEqual(result.returncode, 3)
        qa = self.qa_from("f")
        self.assertEqual(qa["status"], "blocked")
        self.assertNotEqual(qa["status"], "ok")
        self.assertIsNone(qa["rows_input"])
        self.assertTrue(any("not a pass" in note for note in qa["notes"]))

    def test_explicit_delimiter_unblocks_an_unknown_suffix(self):
        source = self.write("d.dat", "sample\tvalue\nS1\t1\nS2\t2\n")
        blocked = self.run_cli("--input", source, "--output", self.dir / "f", "--numeric", "value")
        self.assertEqual(blocked.returncode, 3)
        allowed = self.run_cli("--input", source, "--output", self.dir / "g", "--numeric", "value",
                               "--delimiter", "\\t", "--quiet")
        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(self.qa_from("g")["rows_used"], 2)

    def test_all_rows_excluded_is_refused(self):
        source = self.write("d.csv", "sample,value,qc\nS1,1,drop\n")
        result = self.run_cli("--input", source, "--output", self.dir / "f",
                              "--numeric", "value", "--exclude-column", "qc")
        self.assertEqual(result.returncode, 2)
        self.assertIn("nothing left to plot", result.stderr)


class StandardLibraryOnlyTests(unittest.TestCase):
    def test_module_imports_only_the_standard_library(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
        roots.discard("__future__")
        outside = sorted(root for root in roots if root not in sys.stdlib_module_names)
        self.assertEqual(outside, [], f"non-stdlib imports would break bare-python CI: {outside}")

    def test_module_does_not_import_a_plotting_stack(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for banned in ("import matplotlib", "import numpy", "import pandas"):
            self.assertNotIn(banned, text)


if __name__ == "__main__":
    unittest.main()
