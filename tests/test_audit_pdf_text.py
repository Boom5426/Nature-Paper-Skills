"""Behaviour tests for `skills/figure/nature-figure/scripts/audit_pdf_text.py`.

The script answers one question: how large is this PDF's text *on paper*. A
``Tf`` operand is not that number. Every fixture here is built inline from bytes,
so the suite runs on a bare interpreter with no third-party packages and no
binary files committed to the repository.

The three cases that matter:

* a ``cm`` scale in the same stream shrinks the text (raw scan gives a false PASS);
* a text matrix carries the real size while ``Tf`` says 1 pt, which is what the
  cairo backend emits (raw scan gives a false FAIL);
* a Form XObject drawn under a scale hides the shrink entirely, which is what
  ``\\includegraphics`` does during composite assembly, and the only honest
  answer is NOT AUDITABLE.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills/figure/nature-figure/scripts/audit_pdf_text.py"

_spec = importlib.util.spec_from_file_location("audit_pdf_text", SCRIPT)
assert _spec is not None and _spec.loader is not None
audit_pdf_text = importlib.util.module_from_spec(_spec)
# Register before executing: dataclasses resolves annotations through
# sys.modules[cls.__module__]. Keep bytecode out of the vendored skill tree,
# which ATTRIBUTION.md declares free of __pycache__.
_write_bytecode = sys.dont_write_bytecode
sys.dont_write_bytecode = True
sys.modules[_spec.name] = audit_pdf_text
try:
    _spec.loader.exec_module(audit_pdf_text)
finally:
    sys.dont_write_bytecode = _write_bytecode


# --------------------------------------------------------------------------- #
# minimal PDF construction
# --------------------------------------------------------------------------- #

def build_pdf(objects: list[bytes]) -> bytes:
    """Assemble numbered objects into a PDF with a classic cross-reference table."""
    out = bytearray(b"%PDF-1.5\n")
    offsets: list[int] = []
    for index, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % index + body + b"\nendobj\n"
    xref = len(out)
    count = len(objects) + 1
    out += b"xref\n0 %d\n0000000000 65535 f \n" % count
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (count, xref)
    return bytes(out)


def stream_object(payload: bytes, extra: bytes = b"", compress: bool = False) -> bytes:
    if compress:
        payload = zlib.compress(payload)
        extra = extra + b"/Filter /FlateDecode "
    return (b"<< /Length %d " % len(payload)) + extra + b">>\nstream\n" + payload + b"\nendstream"


HELVETICA = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"


def single_page_pdf(content: bytes, compress: bool = False) -> bytes:
    """One page, one font resource, `content` as its content stream."""
    return build_pdf(
        [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] "
            b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
            stream_object(content, compress=compress),
            HELVETICA,
        ]
    )


def form_xobject_pdf(page_content: bytes, form_content: bytes, form_extra: bytes = b"") -> bytes:
    """A page that draws Form XObject /Fm1, whose own stream holds the text."""
    return build_pdf(
        [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] "
            b"/Resources << /XObject << /Fm1 5 0 R >> >> /Contents 4 0 R >>",
            stream_object(page_content),
            stream_object(
                form_content,
                b"/Type /XObject /Subtype /Form /BBox [0 0 200 100] "
                + form_extra
                + b"/Resources << /Font << /F1 6 0 R >> >> ",
            ),
            HELVETICA,
        ]
    )


TEXT_7PT = b"BT /F1 7 Tf 10 10 Td (Hi) Tj ET\n"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

class AuditCase(unittest.TestCase):
    def audit(self, data: bytes, minimum_pt: float = 5.0) -> dict:
        return audit_pdf_text.audit_pdf(data, minimum_pt=minimum_pt)

    def run_cli(self, data: bytes, *args: str) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False) as handle:
            handle.write(data)
            path = Path(handle.name)
        self.addCleanup(path.unlink)
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path), *args],
            check=False,
            capture_output=True,
            text=True,
        )


# --------------------------------------------------------------------------- #
# FIX 1: the transform must be applied
# --------------------------------------------------------------------------- #

class SameStreamTransformTests(AuditCase):
    """`q 0.4 ... cm` wrapping a `7 Tf` prints at 2.8 pt, not 7 pt."""

    CONTENT = b"q 0.4 0 0 0.4 0 0 cm " + TEXT_7PT + b"Q\n"

    def test_effective_size_is_the_scaled_size(self) -> None:
        result = self.audit(single_page_pdf(self.CONTENT))

        self.assertAlmostEqual(result["minimum_effective_pt"], 2.8, places=6)
        self.assertEqual(result["minimum_raw_tf_pt"], 7.0)

    def test_verdict_is_fail_not_pass(self) -> None:
        result = self.audit(single_page_pdf(self.CONTENT))

        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["below_minimum_count"], 1)

    def test_cli_exits_one_and_prints_both_sizes(self) -> None:
        completed = self.run_cli(single_page_pdf(self.CONTENT))

        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        self.assertIn("2.8 pt", completed.stdout)
        self.assertIn("7 Tf", completed.stdout)

    def test_transform_is_popped_by_capital_q(self) -> None:
        content = b"q 0.4 0 0 0.4 0 0 cm Q " + TEXT_7PT

        result = self.audit(single_page_pdf(content))

        self.assertEqual(result["verdict"], "PASS")
        self.assertAlmostEqual(result["minimum_effective_pt"], 7.0, places=6)

    def test_nested_transforms_multiply(self) -> None:
        content = b"q 0.5 0 0 0.5 0 0 cm q 0.5 0 0 0.5 0 0 cm " + TEXT_7PT + b"Q Q\n"

        result = self.audit(single_page_pdf(content))

        self.assertAlmostEqual(result["minimum_effective_pt"], 1.75, places=6)

    def test_flate_compressed_content_stream_is_read(self) -> None:
        result = self.audit(single_page_pdf(self.CONTENT, compress=True))

        self.assertAlmostEqual(result["minimum_effective_pt"], 2.8, places=6)
        self.assertEqual(result["verdict"], "FAIL")

    def test_rotation_does_not_shrink_text(self) -> None:
        content = b"q 0 1 -1 0 0 0 cm " + TEXT_7PT + b"Q\n"

        result = self.audit(single_page_pdf(content))

        self.assertAlmostEqual(result["minimum_effective_pt"], 7.0, places=6)
        self.assertEqual(result["verdict"], "PASS")

    def test_anisotropic_transform_reports_the_smaller_axis(self) -> None:
        content = b"q 1 0 0 0.5 0 0 cm " + TEXT_7PT + b"Q\n"

        result = self.audit(single_page_pdf(content))

        self.assertAlmostEqual(result["minimum_effective_pt"], 3.5, places=6)
        self.assertTrue(any("anisotropic" in warning for warning in result["warnings"]))


class ScaledFormXObjectTests(AuditCase):
    """The composite case: the shrink lives outside the stream holding the text."""

    PAGE = b"q 0.4 0 0 0.4 0 0 cm /Fm1 Do Q\n"

    def test_scaled_form_is_not_auditable(self) -> None:
        result = self.audit(form_xobject_pdf(self.PAGE, TEXT_7PT))

        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        self.assertFalse(result["auditable"])
        self.assertTrue(
            any("Form XObject" in reason for reason in result["blocked_reasons"]),
            result["blocked_reasons"],
        )

    def test_scaled_form_never_reports_a_pass(self) -> None:
        completed = self.run_cli(form_xobject_pdf(self.PAGE, TEXT_7PT))

        self.assertEqual(completed.returncode, 4, completed.stdout + completed.stderr)
        self.assertNotIn("verdict: PASS", completed.stdout)
        self.assertIn("per-panel", completed.stdout)

    def test_unscaled_form_is_audited_in_its_own_space(self) -> None:
        # Markers and hatches are placed by translation only; that is not a composite.
        page = b"q 1 0 0 1 20 30 cm /Fm1 Do Q\n"

        result = self.audit(form_xobject_pdf(page, TEXT_7PT))

        self.assertEqual(result["verdict"], "PASS")
        self.assertAlmostEqual(result["minimum_effective_pt"], 7.0, places=6)

    def test_form_matrix_scaling_is_caught_too(self) -> None:
        page = b"q 1 0 0 1 0 0 cm /Fm1 Do Q\n"

        result = self.audit(form_xobject_pdf(page, TEXT_7PT, b"/Matrix [0.4 0 0 0.4 0 0] "))

        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        self.assertTrue(
            any("/Matrix" in reason for reason in result["blocked_reasons"]),
            result["blocked_reasons"],
        )


class ObjectStreamCompositeTests(AuditCase):
    """pdfTeX puts page dictionaries in an /ObjStm; the guard must still fire.

    The fixture exercises the object-stream reader, not full PDF validity: the
    scanner resolves objects by scanning, so a classic trailer is enough here.
    """

    def build(self) -> bytes:
        # Object 7, the page dictionary, lives inside object 6, the object stream.
        page = (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] "
            b"/Resources << /XObject << /Im1 4 0 R >> >> /Contents 3 0 R >>"
        )
        header = b"7 0 "
        return build_pdf(
            [
                b"<< /Type /Catalog /Pages 2 0 R >>",
                b"<< /Type /Pages /Kids [7 0 R] /Count 1 >>",
                stream_object(b"q .78745 0 0 .78745 0 0 cm /Im1 Do Q\n"),
                stream_object(
                    TEXT_7PT,
                    b"/Type /XObject /Subtype /Form /BBox [0 0 200 100] "
                    b"/Resources << /Font << /F1 5 0 R >> >> ",
                ),
                HELVETICA,
                stream_object(
                    header + page,
                    b"/Type /ObjStm /N 1 /First %d " % len(header),
                    compress=True,
                ),
            ]
        )

    def test_page_inside_an_object_stream_is_resolved(self) -> None:
        result = self.audit(self.build())

        self.assertGreaterEqual(result["content_streams_walked"], 2)

    def test_scaled_include_is_not_auditable(self) -> None:
        result = self.audit(self.build())

        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        self.assertTrue(
            any("0.7874" in reason for reason in result["blocked_reasons"]),
            result["blocked_reasons"],
        )


# --------------------------------------------------------------------------- #
# FIX 2: the text matrix carries the size in cairo output
# --------------------------------------------------------------------------- #

class TextMatrixTests(AuditCase):
    """Cairo emits `6 0 0 -6 x y Tm` then `/f-0-0 1 Tf`; that is 6 pt, not 1 pt."""

    CONTENT = (
        b"1 0 0 -1 0 100 cm\n"
        b"BT\n6 0 0 -6 42.6 135.7 Tm\n/F1 1 Tf\n(1.00) Tj\nET\n"
    )

    def test_one_point_font_scaled_by_the_text_matrix_passes(self) -> None:
        result = self.audit(single_page_pdf(self.CONTENT))

        self.assertEqual(result["minimum_raw_tf_pt"], 1.0)
        self.assertAlmostEqual(result["minimum_effective_pt"], 6.0, places=6)
        self.assertEqual(result["verdict"], "PASS")

    def test_report_shows_the_raw_operand_and_the_printed_size(self) -> None:
        completed = self.run_cli(single_page_pdf(self.CONTENT), "--show-all")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("smallest raw Tf operand: 1 pt", completed.stdout)
        self.assertIn("1 Tf -> 6 pt printed", completed.stdout)

    def test_text_matrix_below_the_floor_still_fails(self) -> None:
        content = b"BT\n4 0 0 4 10 10 Tm\n/F1 1 Tf\n(x) Tj\nET\n"

        result = self.audit(single_page_pdf(content))

        self.assertEqual(result["verdict"], "FAIL")
        self.assertAlmostEqual(result["minimum_effective_pt"], 4.0, places=6)

    def test_text_matrix_and_cm_compose(self) -> None:
        content = b"q 0.5 0 0 0.5 0 0 cm BT 6 0 0 6 10 10 Tm /F1 1 Tf (x) Tj ET Q\n"

        result = self.audit(single_page_pdf(content))

        self.assertAlmostEqual(result["minimum_effective_pt"], 3.0, places=6)

    def test_bt_resets_the_text_matrix(self) -> None:
        content = (
            b"BT 2 0 0 2 0 0 Tm /F1 1 Tf (a) Tj ET\n"
            b"BT /F1 6 Tf (b) Tj ET\n"
        )

        result = self.audit(single_page_pdf(content))

        # The second block must not inherit the 2x matrix from the first.
        effective = sorted(run["effective_pt"] for run in result["runs"])
        self.assertEqual(effective, [2.0, 6.0])


# --------------------------------------------------------------------------- #
# third state: a checker that cannot check says so
# --------------------------------------------------------------------------- #

class BlockedStateTests(AuditCase):
    def test_pdf_without_text_is_not_auditable(self) -> None:
        result = self.audit(single_page_pdf(b"0 0 100 50 re f\n"))

        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        self.assertEqual(result["text_run_count"], 0)

    def test_encrypted_pdf_is_not_auditable(self) -> None:
        data = single_page_pdf(TEXT_7PT).replace(
            b"/Size", b"/Encrypt 9 0 R /Size", 1
        )

        result = self.audit(data)

        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        self.assertTrue(any("/Encrypt" in reason for reason in result["blocked_reasons"]))

    def test_unsupported_filter_blocks_rather_than_passes(self) -> None:
        data = build_pdf(
            [
                b"<< /Type /Catalog /Pages 2 0 R >>",
                b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
                b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] "
                b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
                stream_object(b"garbage", b"/Filter /LZWDecode "),
                HELVETICA,
            ]
        )

        result = self.audit(data)

        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        self.assertTrue(
            any("LZWDecode" in reason for reason in result["blocked_reasons"]),
            result["blocked_reasons"],
        )

    def test_cli_exit_code_four_for_blocked(self) -> None:
        completed = self.run_cli(single_page_pdf(b"0 0 100 50 re f\n"))

        self.assertEqual(completed.returncode, 4, completed.stdout + completed.stderr)
        self.assertIn("NOT AUDITABLE", completed.stdout)


# --------------------------------------------------------------------------- #
# operator handling that would otherwise produce phantom violations
# --------------------------------------------------------------------------- #

class OperatorHandlingTests(AuditCase):
    def test_invisible_text_is_excluded(self) -> None:
        # Tr is graphics state, not text-block state, so the fixture resets it
        # the way a real OCR layer does.
        content = b"BT 3 Tr /F1 1 Tf (ocr layer) Tj ET\nBT 0 Tr /F1 6 Tf (real) Tj ET\n"

        result = self.audit(single_page_pdf(content))

        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["text_run_count"], 1)
        self.assertTrue(any("invisible" in warning for warning in result["warnings"]))

    def test_inline_image_bytes_are_skipped(self) -> None:
        content = (
            b"q BI /W 2 /H 2 /CS /G /BPC 8 ID \x00\x01 1 Tf \x02\x03 EI Q\n" + TEXT_7PT
        )

        result = self.audit(single_page_pdf(content))

        self.assertEqual(result["text_run_count"], 1)
        self.assertAlmostEqual(result["minimum_effective_pt"], 7.0, places=6)

    def test_min_pt_is_honoured(self) -> None:
        result = self.audit(single_page_pdf(TEXT_7PT), minimum_pt=8.0)

        self.assertEqual(result["verdict"], "FAIL")

    def test_runs_are_counted_per_show_operator(self) -> None:
        content = b"BT /F1 6 Tf (a) Tj (b) Tj [(c)] TJ ET\n"

        result = self.audit(single_page_pdf(content))

        self.assertEqual(result["text_run_count"], 3)


class MatrixMathTests(unittest.TestCase):
    def test_identity_scale_is_one(self) -> None:
        smallest, largest = audit_pdf_text.singular_values(audit_pdf_text.IDENTITY)

        self.assertAlmostEqual(smallest, 1.0, places=9)
        self.assertAlmostEqual(largest, 1.0, places=9)

    def test_uniform_scale(self) -> None:
        smallest, largest = audit_pdf_text.singular_values((0.4, 0, 0, 0.4, 0, 0))

        self.assertAlmostEqual(smallest, 0.4, places=9)
        self.assertAlmostEqual(largest, 0.4, places=9)

    def test_flip_keeps_magnitude(self) -> None:
        smallest, _ = audit_pdf_text.singular_values((6.0, 0, 0, -6.0, 0, 0))

        self.assertAlmostEqual(smallest, 6.0, places=9)

    def test_multiplication_matches_pdf_convention(self) -> None:
        scaled = audit_pdf_text.multiply((2, 0, 0, 2, 0, 0), (1, 0, 0, 1, 10, 20))

        self.assertEqual(scaled, (2, 0, 0, 2, 10, 20))


if __name__ == "__main__":
    unittest.main()
