#!/usr/bin/env python3
"""Audit the *printed* size of text in a PDF figure.

Exit codes are the same across every audit tool in this skill:

    0  PASS            the check ran and the figure is acceptable
    1  FAIL            the check ran and found a blocking problem
    2  ERROR           usage or I/O problem; nothing was audited
    3  NOT RUN         a required dependency is absent; nothing was audited
    4  NOT AUDITABLE   the input cannot answer this question

Codes 2, 3 and 4 are not passes. A caller that treats "not 1" as success will
ship an unchecked figure.

A ``Tf`` operand is a font size in *text space*, not on paper. What reaches the
page is

    effective_pt = Tf_size x scale(text matrix) x scale(current transform)

so reading the raw ``Tf`` operand alone is wrong in both directions:

* **False PASS.** ``q 0.4 0 0 0.4 0 0 cm ... 7 Tf`` prints at 2.8 pt. This is
  what ``\\includegraphics[width=...]`` does to a panel PDF during composite
  assembly, and it is invisible to a raw ``Tf`` scan.
* **False FAIL.** Cairo-backed exports emit ``/f-0-0 1 Tf`` and carry the real
  size in the text matrix (``6 0 0 -6 ... Tm``). A raw scan calls a 6 pt label
  a 1 pt violation.

This script therefore walks the content streams, tracks the ``q``/``Q`` stack,
``cm`` and ``Tm``, and reports both the raw operand and the computed printed
size.

One transform it cannot follow is a **scaled Form XObject**: inside the form the
transform is the identity, so the text carries no record of the placement that
shrank it. When a page draws a Form XObject under a non-unit scale the verdict
is ``NOT AUDITABLE`` (exit 4), not a pass: audit the per-panel PDFs exported at
true print size instead.

Standard library only. Supports uncompressed and FlateDecode streams, and
objects held in object streams (``/ObjStm``), which is where pdfTeX puts page
dictionaries.

Exit codes: 0 pass, 1 below the floor, 2 not auditable or a usage error.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import zlib
from dataclasses import dataclass, field
from pathlib import Path

Matrix = tuple[float, float, float, float, float, float]

IDENTITY: Matrix = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

#: A placement scale within this of 1.0 is treated as "drawn at true size".
SCALE_TOLERANCE = 1e-4

#: Report a transform as anisotropic when its two singular values differ by more.
ANISOTROPY_TOLERANCE = 1.01

OBJECT_HEADER = re.compile(rb"(?<![0-9])(\d{1,10})[\x00\t\r\n\f ]+(\d{1,5})[\x00\t\r\n\f ]+obj\b")
STREAM_START = re.compile(rb"stream\r\n|stream\n|stream\r(?!\n)")
DIRECT_LENGTH = re.compile(rb"/Length[\x00\t\r\n\f ]+(\d+)(?![\x00\t\r\n\f ]*\d+[\x00\t\r\n\f ]+R)")
INDIRECT_LENGTH = re.compile(rb"/Length[\x00\t\r\n\f ]+(\d+)[\x00\t\r\n\f ]+(\d+)[\x00\t\r\n\f ]+R")
NAME_TO_REF = re.compile(rb"/([^\s/<>\[\]()%]+)[\x00\t\r\n\f ]+(\d+)[\x00\t\r\n\f ]+(\d+)[\x00\t\r\n\f ]+R")
SUBTYPE_FORM = re.compile(rb"/Subtype[\x00\t\r\n\f ]*/Form\b")
TYPE_PAGE = re.compile(rb"/Type[\x00\t\r\n\f ]*/Page(?![a-zA-Z])")
TYPE_OBJSTM = re.compile(rb"/Type[\x00\t\r\n\f ]*/ObjStm\b")
TF_OPERATOR = re.compile(rb"/([^\s/<>\[\]()%]+)[\x00\t\r\n\f ]+([-+]?(?:\d+(?:\.\d*)?|\.\d+))[\x00\t\r\n\f ]+Tf\b")
WHITESPACE = b"\x00\t\n\f\r "
DELIMITERS = b"()<>[]{}/%"


# --------------------------------------------------------------------------- #
# matrix helpers
# --------------------------------------------------------------------------- #

def multiply(first: Matrix, second: Matrix) -> Matrix:
    """Return ``first x second`` in PDF row-vector convention."""
    a1, b1, c1, d1, e1, f1 = first
    a2, b2, c2, d2, e2, f2 = second
    return (
        a1 * a2 + b1 * c2,
        a1 * b2 + b1 * d2,
        c1 * a2 + d1 * c2,
        c1 * b2 + d1 * d2,
        e1 * a2 + f1 * c2 + e2,
        e1 * b2 + f1 * d2 + f2,
    )


def singular_values(matrix: Matrix) -> tuple[float, float]:
    """Return (smallest, largest) singular value of the 2x2 part.

    For an isotropic scale both equal that scale; for a rotation both are 1.
    The smallest is the worst-case shrink of a glyph in any direction, which is
    the conservative number for a legibility floor.
    """
    a, b, c, d = matrix[0], matrix[1], matrix[2], matrix[3]
    frobenius = a * a + b * b + c * c + d * d
    determinant = a * d - b * c
    discriminant = max(frobenius * frobenius - 4.0 * determinant * determinant, 0.0)
    root = math.sqrt(discriminant)
    largest = math.sqrt(max((frobenius + root) / 2.0, 0.0))
    smallest = math.sqrt(max((frobenius - root) / 2.0, 0.0))
    return smallest, largest


# --------------------------------------------------------------------------- #
# object layer
# --------------------------------------------------------------------------- #

@dataclass
class PdfObject:
    number: int
    dictionary: bytes
    payload: bytes | None = None
    filters: bytes = b""


def _skip_whitespace(data: bytes, pos: int) -> int:
    while pos < len(data):
        char = data[pos : pos + 1]
        if char in (b"%",):
            while pos < len(data) and data[pos : pos + 1] not in (b"\n", b"\r"):
                pos += 1
        elif char and char[0] in WHITESPACE:
            pos += 1
        else:
            break
    return pos


def raw_value(dictionary: bytes, key: bytes) -> bytes | None:
    """Return the raw bytes of ``key``'s value from a shallow dictionary scan."""
    pattern = re.compile(re.escape(key) + rb"(?![a-zA-Z0-9])")
    match = pattern.search(dictionary)
    if match is None:
        return None
    pos = _skip_whitespace(dictionary, match.end())
    if pos >= len(dictionary):
        return None
    if dictionary[pos : pos + 2] == b"<<":
        depth = 0
        start = pos
        while pos < len(dictionary):
            if dictionary[pos : pos + 2] == b"<<":
                depth += 1
                pos += 2
            elif dictionary[pos : pos + 2] == b">>":
                depth -= 1
                pos += 2
                if depth == 0:
                    return dictionary[start:pos]
            else:
                pos += 1
        return dictionary[start:]
    if dictionary[pos : pos + 1] == b"[":
        depth = 0
        start = pos
        while pos < len(dictionary):
            if dictionary[pos : pos + 1] == b"[":
                depth += 1
            elif dictionary[pos : pos + 1] == b"]":
                depth -= 1
                if depth == 0:
                    return dictionary[start : pos + 1]
            pos += 1
        return dictionary[start:]
    end = pos
    while end < len(dictionary) and dictionary[end] not in WHITESPACE and dictionary[end] not in DELIMITERS:
        end += 1
    if dictionary[pos : pos + 1] == b"/":
        end = pos + 1
        while end < len(dictionary) and dictionary[end] not in WHITESPACE and dictionary[end] not in DELIMITERS:
            end += 1
        return dictionary[pos:end]
    token = dictionary[pos:end]
    reference = re.match(rb"(\d+)$", token)
    if reference:
        tail = re.match(rb"[\x00\t\r\n\f ]+(\d+)[\x00\t\r\n\f ]+R\b", dictionary[end:])
        if tail:
            return dictionary[pos : end + tail.end()]
    return token


def reference_number(value: bytes | None) -> int | None:
    if value is None:
        return None
    match = re.fullmatch(rb"(\d+)[\x00\t\r\n\f ]+\d+[\x00\t\r\n\f ]+R", value.strip())
    return int(match.group(1)) if match else None


def parse_objects(data: bytes) -> tuple[dict[int, PdfObject], list[str]]:
    """Collect indirect objects, then expand any ``/ObjStm`` containers."""
    objects: dict[int, PdfObject] = {}
    notes: list[str] = []
    seen: set[int] = set()
    for match in OBJECT_HEADER.finditer(data):
        number = int(match.group(1))
        if number in seen:
            notes.append(
                f"object {number} is defined more than once (incremental update?); "
                "the last definition in the file is the one audited"
            )
        seen.add(number)
        body_start = match.end()
        endobj = data.find(b"endobj", body_start)
        limit = endobj if endobj >= 0 else len(data)
        stream = STREAM_START.search(data, body_start, limit)
        if stream is None:
            objects[number] = PdfObject(number=number, dictionary=data[body_start:limit])
            continue
        dictionary = data[body_start : stream.start()]
        payload: bytes | None = None
        length_match = DIRECT_LENGTH.search(dictionary)
        if length_match is not None:
            declared = int(length_match.group(1))
            candidate_end = stream.end() + declared
            trailer = data[candidate_end : candidate_end + 20].lstrip(WHITESPACE)
            if trailer.startswith(b"endstream"):
                payload = data[stream.end() : candidate_end]
        if payload is None:
            end = data.find(b"endstream", stream.end())
            if end < 0:
                notes.append(f"object {number}: stream has no endstream marker")
                continue
            payload = data[stream.end() : end].rstrip(b"\r\n")
        filters = raw_value(dictionary, b"/Filter") or b""
        objects[number] = PdfObject(number, dictionary, payload, filters)

    # Resolve streams whose /Length was an indirect reference.
    for obj in list(objects.values()):
        if obj.payload is None:
            continue
        indirect = INDIRECT_LENGTH.search(obj.dictionary)
        if indirect is None:
            continue
        target = objects.get(int(indirect.group(1)))
        if target is None:
            continue
        declared = re.match(rb"[\x00\t\r\n\f ]*(\d+)", target.dictionary)
        if declared is None:
            continue
        obj.payload = obj.payload[: int(declared.group(1))]

    for obj in list(objects.values()):
        if obj.payload is None or not TYPE_OBJSTM.search(obj.dictionary):
            continue
        decoded, note = decode_stream(obj)
        if decoded is None:
            notes.append(f"object stream {obj.number}: {note}")
            continue
        count = raw_value(obj.dictionary, b"/N")
        first = raw_value(obj.dictionary, b"/First")
        if count is None or first is None:
            notes.append(f"object stream {obj.number}: missing /N or /First")
            continue
        try:
            n_objects, offset_base = int(count), int(first)
        except ValueError:
            notes.append(f"object stream {obj.number}: unreadable /N or /First")
            continue
        header = decoded[:offset_base].split()
        if len(header) < 2 * n_objects:
            notes.append(f"object stream {obj.number}: truncated header")
            continue
        entries = []
        for index in range(n_objects):
            try:
                entries.append((int(header[2 * index]), int(header[2 * index + 1])))
            except ValueError:
                notes.append(f"object stream {obj.number}: unreadable header entry")
                break
        for index, (number, offset) in enumerate(entries):
            start = offset_base + offset
            stop = offset_base + entries[index + 1][1] if index + 1 < len(entries) else len(decoded)
            if number not in objects:
                objects[number] = PdfObject(number=number, dictionary=decoded[start:stop])
    return objects, notes


def decode_stream(obj: PdfObject) -> tuple[bytes | None, str]:
    """Return the decoded payload, or ``(None, reason)`` when it cannot decode."""
    if obj.payload is None:
        return None, "object has no stream"
    if not obj.filters:
        return obj.payload, ""
    if b"/FlateDecode" not in obj.filters:
        return None, f"unsupported filter {obj.filters.decode('ascii', 'replace').strip()}"
    try:
        decoded = zlib.decompress(obj.payload)
    except zlib.error as exc:
        # A partial inflate is not a usable audit input: half a content stream
        # can hide the smallest label. Report the block rather than guess.
        engine = zlib.decompressobj()
        try:
            decoded = engine.decompress(obj.payload)
        except zlib.error:
            return None, f"FlateDecode failed: {exc}"
        if not engine.eof:
            return None, f"FlateDecode stream is truncated: {exc}"
    remaining = obj.filters.count(b"/") - 1
    if remaining > 0:
        return None, "stream uses a filter chain this scanner does not implement"
    if b"/DecodeParms" in obj.dictionary and b"/Predictor" in obj.dictionary:
        return None, "stream uses a FlateDecode predictor this scanner does not implement"
    return decoded, ""


# --------------------------------------------------------------------------- #
# content-stream walk
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class TextRun:
    context: str
    font: str
    raw_pt: float
    effective_pt: float
    scale: float
    anisotropic: bool


@dataclass
class WalkResult:
    runs: list[TextRun] = field(default_factory=list)
    scaled_forms: list[str] = field(default_factory=list)
    unresolved_xobjects: list[str] = field(default_factory=list)
    invisible_runs: int = 0
    horizontal_squeeze: bool = False
    notes: list[str] = field(default_factory=list)


def tokenize(stream: bytes):
    """Yield ``(kind, value)`` tokens; kinds are ``num``, ``name``, ``op``, ``other``."""
    pos, size = 0, len(stream)
    while pos < size:
        char = stream[pos : pos + 1]
        if stream[pos] in WHITESPACE:
            pos += 1
            continue
        if char == b"%":
            while pos < size and stream[pos : pos + 1] not in (b"\r", b"\n"):
                pos += 1
            continue
        if char == b"(":
            depth, pos = 1, pos + 1
            while pos < size and depth:
                byte = stream[pos : pos + 1]
                if byte == b"\\":
                    pos += 2
                    continue
                if byte == b"(":
                    depth += 1
                elif byte == b")":
                    depth -= 1
                pos += 1
            yield "other", None
            continue
        if stream[pos : pos + 2] in (b"<<", b">>"):
            pos += 2
            yield "other", None
            continue
        if char == b"<":
            end = stream.find(b">", pos)
            pos = size if end < 0 else end + 1
            yield "other", None
            continue
        if char in (b"[", b"]", b"{", b"}"):
            pos += 1
            yield "other", None
            continue
        if char == b"/":
            end = pos + 1
            while end < size and stream[end] not in WHITESPACE and stream[end] not in DELIMITERS:
                end += 1
            yield "name", stream[pos + 1 : end].decode("ascii", "replace")
            pos = end
            continue
        end = pos
        while end < size and stream[end] not in WHITESPACE and stream[end] not in DELIMITERS:
            end += 1
        token = stream[pos:end]
        pos = end if end > pos else pos + 1
        if not token:
            continue
        # A token that parses as a number is an operand; anything else is an
        # operator. Parse outside the yield so a consumer's ValueError is not
        # swallowed here.
        try:
            number = float(token)
        except ValueError:
            number = None
        if number is not None:
            yield "num", number
            continue
        operator = token.decode("ascii", "replace")
        if operator == "BI":
            marker = stream.find(b"ID", pos)
            if marker < 0:
                return
            search = marker + 2
            while True:
                end_marker = stream.find(b"EI", search)
                if end_marker < 0:
                    return
                before = stream[end_marker - 1] if end_marker else 0
                after = stream[end_marker + 2] if end_marker + 2 < size else 0x20
                if before in WHITESPACE and (after in WHITESPACE or after in DELIMITERS):
                    pos = end_marker + 2
                    break
                search = end_marker + 2
            continue
        yield "op", operator


def walk_content(
    stream: bytes,
    base_ctm: Matrix,
    context: str,
    xobjects: dict[str, int],
    form_numbers: set[int],
    result: WalkResult,
) -> None:
    ctm = base_ctm
    stack: list[Matrix] = []
    text_matrix = IDENTITY
    font_name: str | None = None
    font_size: float | None = None
    render_mode = 0
    operands: list[tuple[str, object]] = []

    def numbers(count: int) -> list[float] | None:
        values = [value for kind, value in operands[-count:] if kind == "num"]
        return values if len(values) == count else None

    for kind, value in tokenize(stream):
        if kind != "op":
            operands.append((kind, value))
            if len(operands) > 32:
                del operands[:-32]
            continue
        operator = value
        if operator == "q":
            stack.append(ctm)
        elif operator == "Q":
            ctm = stack.pop() if stack else ctm
        elif operator == "cm":
            values = numbers(6)
            if values:
                ctm = multiply(tuple(values), ctm)  # type: ignore[arg-type]
        elif operator == "BT":
            text_matrix = IDENTITY
        elif operator == "Tm":
            values = numbers(6)
            if values:
                text_matrix = tuple(values)  # type: ignore[assignment]
        elif operator == "Tf":
            values = numbers(1)
            names = [item for item in operands if item[0] == "name"]
            if values and names:
                font_name = str(names[-1][1])
                font_size = values[0]
        elif operator == "Tr":
            values = numbers(1)
            if values:
                render_mode = int(values[0])
        elif operator == "Tz":
            values = numbers(1)
            # Tz narrows glyphs horizontally only; the reported size is a height,
            # so flag it rather than fold it in.
            if values and abs(values[0] - 100.0) > 0.5:
                result.horizontal_squeeze = True
        elif operator in ("Tj", "TJ", "'", '"'):
            if font_size is None:
                result.notes.append(f"{context}: text shown before any Tf operator")
            elif render_mode in (3, 7):
                result.invisible_runs += 1
            elif font_size > 0:
                combined = multiply(text_matrix, ctm)
                smallest, largest = singular_values(combined)
                result.runs.append(
                    TextRun(
                        context=context,
                        font=font_name or "?",
                        raw_pt=font_size,
                        effective_pt=font_size * smallest,
                        scale=smallest,
                        anisotropic=largest > smallest * ANISOTROPY_TOLERANCE,
                    )
                )
        elif operator == "Do":
            names = [item for item in operands if item[0] == "name"]
            if not names:
                continue
            name = str(names[-1][1])
            target = xobjects.get(name)
            smallest, _ = singular_values(ctm)
            if target is None:
                if form_numbers:
                    result.unresolved_xobjects.append(f"{context}: /{name}")
            elif target in form_numbers and abs(smallest - 1.0) > SCALE_TOLERANCE:
                result.scaled_forms.append(f"{context}: /{name} drawn at {smallest:.4g}x")
        operands = []


# --------------------------------------------------------------------------- #
# audit
# --------------------------------------------------------------------------- #

def xobject_map(resources: bytes | None, objects: dict[int, PdfObject]) -> dict[str, int]:
    if resources is None:
        return {}
    reference = reference_number(resources)
    if reference is not None:
        target = objects.get(reference)
        if target is None:
            return {}
        resources = target.dictionary
    value = raw_value(resources, b"/XObject")
    if value is None:
        return {}
    reference = reference_number(value)
    if reference is not None:
        target = objects.get(reference)
        if target is None:
            return {}
        value = target.dictionary
    return {
        match.group(1).decode("ascii", "replace"): int(match.group(2))
        for match in NAME_TO_REF.finditer(value)
    }


def content_refs(page: bytes) -> list[int]:
    value = raw_value(page, b"/Contents")
    if value is None:
        return []
    single = reference_number(value)
    if single is not None:
        return [single]
    return [int(match.group(1)) for match in re.finditer(rb"(\d+)[\x00\t\r\n\f ]+\d+[\x00\t\r\n\f ]+R", value)]


def matrix_of(dictionary: bytes) -> Matrix:
    value = raw_value(dictionary, b"/Matrix")
    if value is None:
        return IDENTITY
    parts = re.findall(rb"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?", value)
    if len(parts) != 6:
        return IDENTITY
    return tuple(float(part) for part in parts)  # type: ignore[return-value]


def audit_pdf(data: bytes, minimum_pt: float = 5.0) -> dict[str, object]:
    warnings: list[str] = []
    blocked: list[str] = []

    if re.search(rb"/Encrypt[\x00\t\r\n\f ]", data):
        blocked.append("the PDF declares /Encrypt; content streams cannot be read")

    objects, notes = parse_objects(data)
    warnings.extend(notes)

    form_numbers = {
        number for number, obj in objects.items() if SUBTYPE_FORM.search(obj.dictionary)
    }
    result = WalkResult()

    walked = 0
    for number, obj in sorted(objects.items()):
        if not TYPE_PAGE.search(obj.dictionary):
            continue
        resources = raw_value(obj.dictionary, b"/Resources")
        mapping = xobject_map(resources, objects)
        for ref in content_refs(obj.dictionary):
            target = objects.get(ref)
            if target is None or target.payload is None:
                warnings.append(f"page {number}: content stream {ref} is missing")
                continue
            decoded, note = decode_stream(target)
            if decoded is None:
                blocked.append(f"page {number} content stream {ref}: {note}")
                continue
            walked += 1
            walk_content(decoded, IDENTITY, f"page {number}", mapping, form_numbers, result)

    for number in sorted(form_numbers):
        obj = objects[number]
        if obj.payload is None:
            continue
        decoded, note = decode_stream(obj)
        if decoded is None:
            blocked.append(f"form XObject {number}: {note}")
            continue
        form_matrix = matrix_of(obj.dictionary)
        smallest, _ = singular_values(form_matrix)
        if abs(smallest - 1.0) > SCALE_TOLERANCE:
            result.scaled_forms.append(f"form XObject {number}: /Matrix scales by {smallest:.4g}x")
        mapping = xobject_map(raw_value(obj.dictionary, b"/Resources"), objects)
        walked += 1
        walk_content(decoded, form_matrix, f"form XObject {number}", mapping, form_numbers, result)

    warnings.extend(result.notes)

    raw_tf_hits = 0
    for obj in objects.values():
        if obj.payload is None:
            continue
        decoded, _ = decode_stream(obj)
        if decoded:
            raw_tf_hits += len(TF_OPERATOR.findall(decoded))

    if walked == 0 and raw_tf_hits:
        blocked.append(
            f"no page or form content stream could be resolved, yet {raw_tf_hits} raw Tf "
            "operators exist somewhere in the file; their transform context is unknown"
        )
    if result.unresolved_xobjects:
        blocked.append(
            "an XObject name could not be resolved to an object while the file also "
            "contains Form XObjects: " + "; ".join(sorted(set(result.unresolved_xobjects))[:5])
        )

    composite = sorted(set(result.scaled_forms))
    if composite:
        blocked.append(
            "a Form XObject is drawn under a non-unit scale, so text inside it prints "
            "smaller than its Tf operand and the form itself carries no record of the "
            "placement: " + "; ".join(composite[:5])
        )

    runs = result.runs
    aggregated: dict[tuple[str, str, float, float], int] = {}
    for run in runs:
        key = (run.context, run.font, round(run.raw_pt, 4), round(run.effective_pt, 4))
        aggregated[key] = aggregated.get(key, 0) + 1

    below = [
        {
            "context": context,
            "font": font,
            "raw_tf_pt": raw,
            "effective_pt": effective,
            "count": count,
        }
        for (context, font, raw, effective), count in sorted(aggregated.items())
        if effective < minimum_pt
    ]
    below_count = sum(item["count"] for item in below)

    if not blocked and not runs:
        blocked.append("no text-showing operators were found in any resolved content stream")

    if blocked:
        verdict = "NOT AUDITABLE"
    elif below_count:
        verdict = "FAIL"
    else:
        verdict = "PASS"

    if any(run.anisotropic for run in runs):
        warnings.append(
            "at least one text transform is anisotropic or sheared; the effective size "
            "reported is the smaller axis"
        )
    if result.horizontal_squeeze:
        warnings.append(
            "a Tz horizontal-scaling operator is in use; the effective size reported "
            "is a height and does not include that horizontal narrowing"
        )
    if result.invisible_runs:
        warnings.append(
            f"{result.invisible_runs} text runs use an invisible rendering mode (Tr 3/7) "
            "and were excluded"
        )

    return {
        "verdict": verdict,
        "auditable": not blocked,
        "minimum_required_pt": minimum_pt,
        "minimum_effective_pt": min((run.effective_pt for run in runs), default=None),
        "minimum_raw_tf_pt": min((run.raw_pt for run in runs), default=None),
        "text_run_count": len(runs),
        "content_streams_walked": walked,
        "below_minimum_count": below_count,
        "below_minimum": below,
        "runs": [
            {
                "context": context,
                "font": font,
                "raw_tf_pt": raw,
                "effective_pt": effective,
                "count": count,
            }
            for (context, font, raw, effective), count in sorted(aggregated.items())
        ],
        "blocked_reasons": blocked,
        "warnings": warnings,
    }


# --------------------------------------------------------------------------- #
# reporting
# --------------------------------------------------------------------------- #

def render_text(path: Path, result: dict[str, object]) -> str:
    lines = [
        "Nature Figure PDF Text Audit",
        f"pdf: {path}",
        f"minimum required: {result['minimum_required_pt']:g} pt",
    ]
    if result["text_run_count"]:
        label = (
            "minimum effective"
            if result["auditable"]
            else "minimum effective over the streams that COULD be read (not a verdict)"
        )
        lines.extend(
            [
                f"{label}: {result['minimum_effective_pt']:g} pt"
                f"  (smallest raw Tf operand: {result['minimum_raw_tf_pt']:g} pt)",
                f"text runs: {result['text_run_count']}"
                f" in {result['content_streams_walked']} content streams",
                f"below minimum: {result['below_minimum_count']}",
            ]
        )
    lines.append(f"verdict: {result['verdict']}")
    for reason in result["blocked_reasons"]:
        lines.append(f"  blocked: {reason}")
    if result["verdict"] == "NOT AUDITABLE" and any(
        "Form XObject" in reason for reason in result["blocked_reasons"]
    ):
        lines.append(
            "  next step: audit the per-panel PDFs exported at true print size, "
            "not the assembled composite"
        )
    for item in result["below_minimum"]:
        lines.append(
            f"  - {item['context']}: /{item['font']} {item['raw_tf_pt']:g} Tf"
            f" -> {item['effective_pt']:g} pt printed  (x{item['count']})"
        )
    for warning in result["warnings"]:
        lines.append(f"warning: {warning}")
    lines.append(
        "note: this reports the printed size of text operators; it does not replace "
        "a visual check at true size, and it says nothing about text baked into "
        "raster images"
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit printed text size in a PDF figure.")
    parser.add_argument("pdf", type=Path, help="exported PDF figure")
    parser.add_argument(
        "--min-pt", type=float, default=5.0, help="minimum allowed printed font size in points"
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--show-all", action="store_true", help="list every text run, not only violations"
    )
    return parser


EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2
EXIT_NOT_AUDITABLE = 4


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.min_pt <= 0:
        print("error: --min-pt must be positive", file=sys.stderr)
        return EXIT_ERROR
    try:
        data = args.pdf.read_bytes()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_ERROR
    if not data.startswith(b"%PDF-"):
        print(f"error: not a PDF file: {args.pdf}", file=sys.stderr)
        return EXIT_ERROR
    result = audit_pdf(data, minimum_pt=args.min_pt)
    if args.json:
        print(json.dumps({"pdf": str(args.pdf), **result}, indent=2, ensure_ascii=False))
    else:
        report = render_text(args.pdf, result)
        if args.show_all:
            rows = [
                f"  * {run['context']}: /{run['font']} {run['raw_tf_pt']:g} Tf"
                f" -> {run['effective_pt']:g} pt printed  (x{run['count']})"
                for run in result["runs"]
            ]
            report = "\n".join([report, *rows])
        print(report)
    if result["verdict"] == "NOT AUDITABLE":
        return EXIT_NOT_AUDITABLE
    return EXIT_FAIL if result["below_minimum_count"] else EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())
