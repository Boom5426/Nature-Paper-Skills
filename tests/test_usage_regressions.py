"""Regression cases from the project usage audit, with no live API requests."""
import base64
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
FIGURE = ROOT / "skills/figure/nature-figure/scripts"
ANALYZER = ROOT / "skills/research/paper-analyzer/scripts"
REFERENCES = ROOT / "skills/optional/reference-audit-guide/scripts"


def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(path.parent))
    try:
        exec(compile(path.read_text(), str(path), "exec"), module.__dict__)
    finally:
        sys.path.pop(0)
        sys.dont_write_bytecode = previous
    return module


class ScratchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_cli(self, script, *args):
        return subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                              text=True, capture_output=True, cwd=self.root)


class NoteAndGraphTests(ScratchTests):
    def test_existing_note_and_link_target_remain_unchanged(self):
        target = self.root / "reviewed.md"
        target.write_text("Reviewed analysis, preserve this.")
        for output in [target, self.root / "linked.md"]:
            if output != target:
                output.symlink_to(target.name)
            result = self.run_cli(ANALYZER / "generate_note.py", "--output", output, "--title", "Paper")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(target.read_text(), "Reviewed analysis, preserve this.")

    def test_default_note_path_refuses_second_generation(self):
        command = (ANALYZER / "generate_note.py", "--vault", self.root, "--title", "Paper")
        self.assertEqual(self.run_cli(*command).returncode, 0)
        note = self.root / "20_Research/Papers/其他/Paper.md"
        note.write_text("My edited analysis")
        self.assertEqual(self.run_cli(*command).returncode, 1)
        self.assertEqual(note.read_text(), "My edited analysis")

    def test_frontmatter_preserves_quotes_newlines_unicode_and_colons(self):
        output = self.root / "new.md"
        values = {"paper_id": 'id"\\test', "title": 'A "quoted" title\n下一行',
                  "authors": "O'Brien: A\\B", "domain": "Field: subfield"}
        args = [arg for key, value in values.items() for arg in ("--" + key.replace("_", "-"), value)]
        result = self.run_cli(ANALYZER / "generate_note.py", "--output", output, *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        metadata = output.read_text().split("---", 2)[1]
        # JSON quoted strings are YAML-compatible; also verify actual YAML when installed.
        for key, value in values.items():
            row = next(line for line in metadata.splitlines() if line.startswith(key + ":"))
            self.assertEqual(json.loads(row.split(":", 1)[1]), value)
        if importlib.util.find_spec("yaml"):
            import yaml
            parsed = yaml.safe_load(metadata)
            for key, value in values.items():
                self.assertEqual(parsed[key], value)
            self.assertEqual(parsed["tags"][-1], values["domain"])

    def test_duplicate_related_ids_create_one_edge_and_repeat_is_idempotent(self):
        args = (ANALYZER / "update_graph.py", "--vault", self.root, "--paper-id", "2401.00001",
                "--title", "Paper", "--domain", "Field", "--related", "2402.00002", "2402.00002")
        for _ in range(2):
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            graph = json.loads((self.root / "20_Research/PaperGraph/graph_data.json").read_text())
            self.assertEqual(len(graph["edges"]), 1)
            self.assertEqual(graph["edges"][0]["target"], "2402.00002")


class PdfStateTests(unittest.TestCase):
    def setUp(self):
        self.audit = load(FIGURE / "audit_pdf_text.py", "usage_pdf")

    def test_scale_and_font_persist_between_page_content_streams(self):
        from test_audit_pdf_text import build_pdf, stream_object, HELVETICA
        data = build_pdf([
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] "
            b"/Resources << /Font << /F1 6 0 R >> >> /Contents [4 0 R 5 0 R] >>",
            stream_object(b"0.5 0 0 0.5 0 0 cm BT /F1 7 Tf ET"),
            stream_object(b"BT 10 10 Td (Tiny) Tj ET"), HELVETICA])
        result = self.audit.audit_pdf(data)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["minimum_effective_pt"], 3.5)
        self.assertEqual(result["content_streams_walked"], 2)

    def test_q_Q_restore_font_size(self):
        from test_audit_pdf_text import single_page_pdf
        result = self.audit.audit_pdf(single_page_pdf(
            b"BT /F1 2 Tf ET q BT /F1 10 Tf (Large) Tj ET Q BT (Tiny) Tj ET"))
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["minimum_effective_pt"], 2)
        self.assertEqual(result["text_run_count"], 2)

    def test_q_Q_restore_visible_rendering_mode(self):
        from test_audit_pdf_text import single_page_pdf
        result = self.audit.audit_pdf(single_page_pdf(
            b"BT /F1 2 Tf ET q BT 3 Tr (Hidden) Tj ET Q BT (Visible) Tj ET"))
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["text_run_count"], 1)

    def test_missing_one_page_stream_cannot_pass(self):
        from test_audit_pdf_text import single_page_pdf
        data = single_page_pdf(b"BT /F1 7 Tf (Valid) Tj ET").replace(b"/Contents 4 0 R", b"/Contents [4 0 R 99 0 R]")
        self.assertEqual(self.audit.audit_pdf(data)["verdict"], "NOT AUDITABLE")

    def test_sizes_agree_with_independent_pdf_renderer_when_available(self):
        try:
            import pymupdf as fitz
        except ImportError:
            self.skipTest("independent PDF verification requires PyMuPDF (optional CI installs it)")
        from test_audit_pdf_text import single_page_pdf
        data = single_page_pdf(b"BT /F1 2 Tf ET q BT /F1 10 Tf 10 30 Td (Large) Tj ET Q BT 10 10 Td (Tiny) Tj ET")
        with fitz.open(stream=data, filetype="pdf") as document:
            spans = [span for block in document[0].get_text("dict")["blocks"]
                     for line in block.get("lines", []) for span in line["spans"]]
        self.assertEqual(sorted(round(span["size"], 2) for span in spans), [2, 10])
        self.assertEqual(self.audit.audit_pdf(data)["minimum_effective_pt"], min(span["size"] for span in spans))


class CsvTests(ScratchTests):
    def test_unclosed_quote_is_blocked_before_summary(self):
        source = self.root / "data.csv"
        source.write_text('value,group\n1,"control\n2,treatment\n')
        module = load(FIGURE / "figure_source_data.py", "usage_csv")
        with self.assertRaises(module.SourceDataBlocked):
            module.read_table(source)

    def test_valid_quoted_multiline_field_retains_all_rows(self):
        source = self.root / "data.csv"
        source.write_text('value,group\n1,"control\ncontinued"\n2,treatment\n')
        module = load(FIGURE / "figure_source_data.py", "usage_csv_valid")
        self.assertEqual(module.read_table(source).rows_input, 2)


class SchematicOutputTests(ScratchTests):
    def setUp(self):
        super().setUp()
        self.module = load(FIGURE / "generate_openrouter_schematic.py", "usage_image")
        self.args = types.SimpleNamespace(outdir=str(self.root), basename="figure", output_format="png", timeout=1)
        self.item = {"b64_json": base64.b64encode(b"image fixture").decode(), "media_type": "image/png"}

    def save(self, response):
        with contextlib.redirect_stdout(io.StringIO()):
            self.module.save_outputs(response, {}, self.args)

    def test_empty_response_and_empty_bytes_fail_without_metadata(self):
        for response in [{}, {"data": []}, {"data": [{"b64_json": ""}]}]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                self.save(response)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_image_or_metadata_is_never_overwritten(self):
        for name in ["figure.png", "figure_request_metadata.json"]:
            with self.subTest(name=name):
                folder = self.root / name.replace(".", "_")
                folder.mkdir()
                target = folder / name
                target.write_bytes(b"reviewed work")
                self.args.outdir = str(folder)
                with self.assertRaises(FileExistsError):
                    self.save({"data": [self.item]})
                self.assertEqual(target.read_bytes(), b"reviewed work")
                self.assertEqual(list(folder.iterdir()), [target])

    def test_multiple_images_preflight_and_bad_second_payload_create_nothing(self):
        target = self.root / "figure_02.png"
        target.write_bytes(b"existing second panel")
        with self.assertRaises(FileExistsError):
            self.save({"data": [self.item, self.item]})
        self.assertFalse((self.root / "figure_01.png").exists())
        self.args.basename = "new"
        with self.assertRaises(ValueError):
            self.save({"data": [self.item, {}]})
        self.assertEqual(list(self.root.iterdir()), [target])

    def test_default_names_do_not_collide_in_same_second(self):
        self.args.basename = None
        with patch.object(self.module.time, "strftime", return_value="fixed-second"):
            self.save({"data": [self.item]})
            self.save({"data": [self.item]})
        self.assertEqual(len(list(self.root.glob("*.png"))), 2)
        self.assertEqual(len(list(self.root.glob("*.json"))), 2)

    def test_cli_empty_response_returns_nonzero(self):
        with patch.object(self.module, "parse_args", return_value=types.SimpleNamespace(dry_run=False)), \
             patch.object(self.module, "build_payload", return_value={}), \
             patch.object(self.module, "request_images", return_value={"data": []}), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.module.main(), 1)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.module = load(ROOT / "skills/review/paper-reviewer/scripts/check_coverage.py", "usage_coverage")

    def test_no_change_rationale_does_not_need_manuscript_keyword_match(self):
        block = self.module.Block("R1", {}, "", "Add experiments", "No manuscript change. Extrapolation is unsupported.", 1)
        findings = []
        self.module.check_pointers([block], [("main.tex", "unrelated manuscript")], findings)
        self.assertEqual(findings, [])

    def test_keyword_miss_is_advisory_for_changed_manuscript(self):
        block = self.module.Block("R1", {}, "", "Clarify", "We revised the Discussion to explain generalization and extrapolation.", 1)
        findings = []
        self.module.check_pointers([block], [("main.tex", "unrelated manuscript")], findings)
        self.assertTrue(findings)
        self.assertEqual(findings[0]["code"], "POINTER_UNRESOLVED")
        self.assertFalse(findings[0]["blocking"])


class RMarkdownTests(ScratchTests):
    def setUp(self):
        super().setUp()
        self.module = load(FIGURE / "validate_figure.py", "usage_rmd")

    def test_prose_and_other_languages_are_excluded_for_rmd_and_qmd(self):
        source = "---\ntitle: Study's figure\n---\nThe study's data (\n```{python}\nprint('bad\n```\n```{r fig}\nplot(1:3)\n```\n"
        for suffix in [".Rmd", ".qmd"]:
            path = self.root / ("plot" + suffix)
            path.write_text(source)
            result = self.run_cli(FIGURE / "validate_figure.py", path, "--json")
            payload = json.loads(result.stdout)
            syntax = next(f for f in payload["findings"] if f["check_id"] == "SOURCE-SYNTAX")
            self.assertEqual(syntax["level"], "WARN", syntax)

    def test_unbalanced_r_code_still_fails(self):
        code = self.module.extract_r_chunks("```{r}\nplot(1:3\n```\n")
        self.assertEqual(self.module.check_syntax(code, "r").level, "FAIL")

    def test_no_r_or_unclosed_r_fence_is_an_explicit_input_error(self):
        for source in ["Just prose", "```{r}\nplot(1:3)\n"]:
            with self.assertRaises(ValueError):
                self.module.extract_r_chunks(source)


HAVE_BIB = importlib.util.find_spec("bibtexparser") is not None


class ReferenceSchemaTests(unittest.TestCase):
    def test_common_fixes_preserve_field_like_text_inside_titles_and_comments(self):
        module = load(REFERENCES / "citation_io.py", "usage_fix_scope")
        text = ('@comment{\n doi={https://doi.org/10.1/comment}\n}\n'
                '@article{test,\n title={Multiline literal:\n doi={https://doi.org/10.1/title}\n},\n'
                ' doi={https://doi.org/10.1234/actual}\n}\n')
        expected = text.replace(' doi={https://doi.org/10.1234/actual}', ' doi={10.1234/actual}')
        self.assertEqual(module.fix_common_text(text), expected)

    def test_raw_crossref_schema_is_normalized_before_matching(self):
        module = load(REFERENCES / "verify-citations.py", "usage_crossref")
        message = {"title": ["A verified paper"], "author": [{"given": "Jane", "family": "Doe"}],
                   "published": {"date-parts": [[2020, 1, 1]]}, "DOI": "10.1234/test"}
        response = types.SimpleNamespace(status_code=200, json=lambda: {"message": message})
        module.requests = types.SimpleNamespace(get=lambda *a, **kw: response)
        args = types.SimpleNamespace(api_only=False, format_only=False, threshold=0.85)
        result = module.verify_citation({"ID": "test", "ENTRYTYPE": "article", "title": "A verified paper",
                                        "author": "Jane Doe", "year": "2020", "journal": "Journal", "doi": "10.1234/test"}, args)
        self.assertEqual(result.status, "verified")
        self.assertEqual(result.match_score, 1)

    def test_empty_results_can_be_summarized_without_division_by_zero(self):
        module = load(REFERENCES / "verify-citations.py", "usage_summary")
        with contextlib.redirect_stdout(io.StringIO()):
            module.print_summary([])


@unittest.skipUnless(HAVE_BIB, "optional CLI tests require bibtexparser (CI tests both 1.x and 2.x)")
class ReferenceCliTests(ScratchTests):
    VALID = '@article{valid,\n title={A paper},\n author={Jane Doe},\n year={2020},\n journal={Journal}\n}\n'

    def bib(self, text):
        path = self.root / "references.bib"
        path.write_text(text)
        return path

    def test_both_clis_accept_valid_bib_and_reject_empty_malformed_missing(self):
        for script, extra in [("format-checker.py", []), ("verify-citations.py", ["--format-only"])]:
            good = self.run_cli(REFERENCES / script, self.bib(self.VALID), *extra)
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            for text in ["", "@article{broken, title={unfinished",
                         self.VALID + "@article{broken, title={unfinished",
                         self.VALID + "@article{broken, title=bad ## x}"]:
                bad = self.run_cli(REFERENCES / script, self.bib(text), *extra)
                self.assertNotEqual(bad.returncode, 0)
                self.assertNotIn("Traceback", bad.stderr)
            missing = self.run_cli(REFERENCES / script, self.root / "missing.bib", *extra)
            self.assertNotEqual(missing.returncode, 0)

    def test_format_errors_set_failure_code_and_appear_in_report(self):
        bib = self.bib('@article{broken, title={A paper}}')
        for script, extra in [("format-checker.py", []), ("verify-citations.py", ["--format-only"])]:
            report = self.root / (script + ".md")
            result = self.run_cli(REFERENCES / script, bib, *extra, "--output", report)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("author", report.read_text())
            self.assertIn("broken", report.read_text())

    def test_tex_resources_and_undefined_keys_are_checked_by_both_clis(self):
        folder = self.root / "paper"
        folder.mkdir()
        bib = folder / "refs.bib"
        bib.write_text(self.VALID)
        tex = folder / "main.tex"
        for script, extra in [("format-checker.py", []), ("verify-citations.py", ["--format-only"])]:
            tex.write_text(r'\bibliography{refs}' + '\n' + r'\citet{valid} % \cite{fake}' + '\n')
            good = self.run_cli(REFERENCES / script, tex, "--check-latex", *extra)
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            tex.write_text(r'\addbibresource{refs.bib}\autocite{undefined}')
            bad = self.run_cli(REFERENCES / script, tex, "--check-latex", *extra)
            self.assertEqual(bad.returncode, 1, bad.stdout + bad.stderr)
            self.assertIn("undefined", bad.stdout)

    def test_missing_latex_or_no_bibliography_cannot_silently_pass(self):
        bib = self.bib(self.VALID)
        tex = self.root / "paper.tex"
        tex.write_text(r'\cite{valid}')
        for script, extra in [("format-checker.py", []), ("verify-citations.py", ["--format-only"])]:
            self.assertNotEqual(self.run_cli(REFERENCES / script, bib, "--check-latex", *extra).returncode, 0)
            self.assertNotEqual(self.run_cli(REFERENCES / script, tex, *extra).returncode, 0)
            self.assertEqual(self.run_cli(REFERENCES / script, tex, "--bib", bib, *extra).returncode, 0)

    def test_strict_mode_changes_warning_exit_and_reports_are_exclusive(self):
        bib = self.bib(self.VALID.replace('year={2020}', 'year={1899}'))
        ordinary = self.run_cli(REFERENCES / "format-checker.py", bib)
        strict = self.run_cli(REFERENCES / "format-checker.py", bib, "--strict")
        self.assertEqual(ordinary.returncode, 0)
        self.assertEqual(strict.returncode, 1)
        for script, extra in [("format-checker.py", []), ("verify-citations.py", ["--format-only"])]:
            report = self.root / (script + ".md")
            report.write_text("Existing report")
            result = self.run_cli(REFERENCES / script, bib, *extra, "--output", report)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(report.read_text(), "Existing report")

    def test_fix_common_writes_a_new_copy_and_preserves_original(self):
        original = self.VALID.replace('journal={Journal}', 'journal={Journal},\n doi={https://doi.org/10.1234/test},\n pages={12-34}')
        bib = self.bib(original)
        fixed = self.root / "fixed.bib"
        result = self.run_cli(REFERENCES / "format-checker.py", bib, "--fix-common", "--fixed-output", fixed)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(bib.read_text(), original)
        self.assertIn("doi={10.1234/test}", fixed.read_text())
        self.assertIn("pages={12--34}", fixed.read_text())
        again = self.run_cli(REFERENCES / "format-checker.py", bib, "--fix-common", "--fixed-output", fixed)
        self.assertNotEqual(again.returncode, 0)


if __name__ == "__main__":
    unittest.main()
