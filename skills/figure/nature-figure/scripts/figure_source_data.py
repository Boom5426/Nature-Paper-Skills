#!/usr/bin/env python3
"""Source-data layer for nature-figure: load a table, refuse bad rows, record what happened.

Two rules in this repository are prose with no implementation. This module is
that implementation.

  1. `references/qa-contract.md` requires every quantitative panel to be
     traceable to a clean CSV/TSV/XLSX or script output. Here that means: a
     figure ships beside a `<figure>.qa.json` naming the source file, its
     SHA-256, and the exact row accounting behind the panel.
  2. `skills/figure/figure-style/SKILL.md` section 1.1 requires an excluded row
     never to enter a summary statistic plotted alongside the included rows.
     Here that means: exclusion happens once, before any numeric coercion, and
     `summarize()` can only ever see the kept records.

Stance. A missing or non-finite value in a column a panel plots is *refused*,
naming the offending rows, never dropped. Dropping silently shrinks n and moves
the mean, and nothing downstream can tell. The only way a row leaves the
analysis is an explicit exclusion flag that is present in the source data
itself, and every such row is written into the QA record with its reason.

Three outcomes, never two:

  ok      (exit 0) the table was read and satisfies the contract
  refused (exit 2) the table was read and violates the contract
  blocked (exit 3) the table could not be read, so nothing was checked

`blocked` is not a pass. A run that could not look at the data says so.

Standard library only: no matplotlib, no numpy, no pandas. This module does not
draw anything; it decides what a drawing is allowed to be made from.

CLI
    python3 figure_source_data.py --input data.csv --output fig1 \
        --require gene,log2fc,padj --numeric log2fc,padj \
        --exclude-column qc_exclude --summarize log2fc

    writes fig1.qa.json and prints it.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import statistics
import sys
from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "nature-figure/source-data/1"

STATUS_OK = "ok"
STATUS_REFUSED = "refused"
STATUS_BLOCKED = "blocked"

EXIT_OK = 0
EXIT_REFUSED = 2
EXIT_BLOCKED = 3

#: Suffix to delimiter. Anything else must be stated explicitly; guessing the
#: delimiter is the kind of silent fallback that turns one column into one row.
DELIMITER_BY_SUFFIX = {".csv": ",", ".tsv": "\t", ".tab": "\t"}

#: Figure-output suffixes stripped when deriving the QA path from an output name.
FIGURE_SUFFIXES = {".svg", ".pdf", ".eps", ".png", ".tif", ".tiff", ".jpg", ".jpeg"}

#: Values of an exclusion-flag column that mean "this row stays". Every other
#: non-blank value excludes the row and is recorded verbatim as the reason, so
#: a free-text column ("failed QC") works and nothing leaves without a trace.
KEEP_MARKERS = {"", "0", "false", "no", "n", "f", "keep", "include", "included"}

#: How many offending rows an error message names before it summarises the rest.
MAX_NAMED_ROWS = 12


class SourceDataError(Exception):
    """Base class: something stopped this table from backing a figure."""


class SourceDataBlocked(SourceDataError):
    """The table could not be read, so no statement about it can be made."""


class SourceDataRefused(SourceDataError):
    """The table was read and does not satisfy the source-data contract."""


@dataclass(frozen=True)
class Record:
    """One data row.

    `number` is the 1-based data-record number (the header is not a record).
    `line` is the 1-based physical line in the file where the record ends, which
    differs from `number + 1` only when a quoted field contains a newline. Error
    messages quote both so a person can find the row in an editor.
    """

    number: int
    line: int
    values: Mapping[str, Any]


@dataclass(frozen=True)
class Exclusion:
    """A row deliberately held out, and why."""

    number: int
    line: int
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {"record": self.number, "line": self.line, "reason": self.reason}


@dataclass(frozen=True)
class Table:
    """A parsed source file plus the identity that makes a figure traceable."""

    name: str
    sha256: str
    byte_size: int
    delimiter: str
    columns: tuple[str, ...]
    records: tuple[Record, ...]

    @property
    def rows_input(self) -> int:
        return len(self.records)


def describe_delimiter(delimiter: str) -> str:
    """Human-readable delimiter name for messages and the QA record."""
    return {",": "comma", "\t": "tab", ";": "semicolon", "|": "pipe"}.get(delimiter, repr(delimiter))


def read_table(path: Path, delimiter: str | None = None) -> Table:
    """Read a CSV/TSV file into records, hashing the exact bytes that were read.

    Raises `SourceDataBlocked` when the file cannot be read or parsed at all, and
    `SourceDataRefused` when it was read but is not a usable table (no header,
    duplicate column names, blank or ragged rows).
    """
    if not path.is_file():
        raise SourceDataBlocked(f"cannot read {path}: no such file")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SourceDataBlocked(f"cannot read {path}: {exc}") from exc

    if delimiter is None:
        delimiter = DELIMITER_BY_SUFFIX.get(path.suffix.lower())
        if delimiter is None:
            raise SourceDataBlocked(
                f"cannot tell how to parse {path.name}: expected a .csv, .tsv or .tab "
                "suffix, or pass an explicit --delimiter. Guessing is not offered."
            )
    if len(delimiter) != 1:
        raise SourceDataBlocked(f"delimiter must be exactly one character, got {delimiter!r}")

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise SourceDataBlocked(
            f"cannot read {path.name}: it is not valid UTF-8 ({exc}). Re-export it as UTF-8."
        ) from exc

    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter)
    try:
        header = next(reader)
    except StopIteration:
        raise SourceDataRefused(f"{path.name} is empty: there is no header row") from None
    except csv.Error as exc:
        raise SourceDataBlocked(f"cannot parse {path.name}: {exc}") from exc

    columns = [name.strip() for name in header]
    if not columns or not any(columns):
        raise SourceDataRefused(f"{path.name} has no usable header row")
    duplicates = sorted(name for name, count in Counter(columns).items() if count > 1)
    if duplicates:
        raise SourceDataRefused(
            f"{path.name} has duplicate column names: {', '.join(duplicates)}. "
            "A panel cannot be traced to a column that appears twice."
        )

    records: list[Record] = []
    ragged: list[str] = []
    try:
        for number, values in enumerate(reader, start=1):
            line = reader.line_num
            if not values:
                ragged.append(f"record {number} (line {line}): blank line")
                continue
            if len(values) != len(columns):
                ragged.append(
                    f"record {number} (line {line}): {len(values)} field(s), header has {len(columns)}"
                )
                continue
            records.append(Record(number=number, line=line, values=dict(zip(columns, values))))
    except csv.Error as exc:
        raise SourceDataBlocked(f"cannot parse {path.name}: {exc}") from exc

    if ragged:
        raise SourceDataRefused(
            f"{path.name} has {len(ragged)} malformed row(s); fix the source file:\n"
            + format_row_list(ragged)
        )

    return Table(
        name=path.name,
        sha256=hashlib.sha256(raw).hexdigest(),
        byte_size=len(raw),
        delimiter=delimiter,
        columns=tuple(columns),
        records=tuple(records),
    )


def format_row_list(lines: Sequence[str]) -> str:
    """Indent up to MAX_NAMED_ROWS detail lines and count the remainder."""
    shown = [f"  {line}" for line in lines[:MAX_NAMED_ROWS]]
    if len(lines) > MAX_NAMED_ROWS:
        shown.append(f"  ... and {len(lines) - MAX_NAMED_ROWS} more")
    return "\n".join(shown)


def require_columns(table: Table, required: Iterable[str]) -> None:
    """Refuse unless every named column exists, naming the ones that do not."""
    available = set(table.columns)
    missing = [name for name in required if name not in available]
    if missing:
        raise SourceDataRefused(
            f"{table.name} is missing required column(s): {', '.join(missing)}. "
            f"Columns present: {', '.join(table.columns)}"
        )


def partition_excluded(
    table: Table, exclude_column: str | None
) -> tuple[list[Record], list[Exclusion]]:
    """Split records into kept and explicitly excluded, before any coercion.

    Exclusion is driven only by a flag column that exists in the source data, so
    the decision is auditable in the file the QA record hashes. Excluded rows are
    never coerced and never reach `summarize()`, which is figure-style section
    1.1 expressed as control flow rather than as advice.
    """
    if exclude_column is None:
        return list(table.records), []
    require_columns(table, [exclude_column])

    kept: list[Record] = []
    excluded: list[Exclusion] = []
    for record in table.records:
        marker = str(record.values.get(exclude_column, "")).strip()
        if marker.lower() in KEEP_MARKERS:
            kept.append(record)
        else:
            excluded.append(
                Exclusion(
                    number=record.number,
                    line=record.line,
                    reason=f"{exclude_column}={marker}",
                )
            )
    return kept, excluded


def coerce_numeric(records: Sequence[Record], columns: Iterable[str], source: str = "") -> list[Record]:
    """Convert the named columns to float, refusing anything that is not finite.

    A blank cell, a non-numeric cell, `nan`, and `inf` are all refused with the
    offending record and line numbers. They are not dropped: dropping would
    shrink n and shift every summary statistic with no trace in the figure.
    """
    columns = list(columns)
    prefix = f"{source}: " if source else ""
    problems: list[str] = []
    coerced: list[Record] = []

    for record in records:
        values = dict(record.values)
        failed = False
        for column in columns:
            raw = record.values.get(column)
            if raw is None:
                problem = "column absent from this row"
            else:
                text = str(raw).strip()
                if not text:
                    problem = "empty"
                else:
                    try:
                        number = float(text)
                    except ValueError:
                        problem = f"not a number ({text!r})"
                    else:
                        problem = "" if math.isfinite(number) else f"non-finite ({text!r})"
                        if not problem:
                            values[column] = number
            if problem:
                failed = True
                problems.append(
                    f"record {record.number} (line {record.line}) column {column!r}: {problem}"
                )
        if not failed:
            coerced.append(replace(record, values=values))

    if problems:
        raise SourceDataRefused(
            f"{prefix}{len(problems)} missing or non-finite value(s) in the plotted numeric "
            "column(s). These rows are refused, not dropped: fix the source data, or mark "
            "them in an exclusion column so the QA record can name them.\n"
            + format_row_list(problems)
        )
    if not coerced:
        raise SourceDataRefused(
            f"{prefix}no rows remain to plot. A panel drawn from zero rows asserts more "
            "than its data supports."
        )
    return coerced


def first_seen(values: Iterable[Any]) -> list[str]:
    """Category order as the data presents it, duplicates removed.

    A stable, data-derived order is what lets a categorical axis in the figure be
    reproduced from the source file rather than from whatever the plotting
    library happened to do.
    """
    seen: set[str] = set()
    order: list[str] = []
    for value in values:
        text = str(value)
        if text not in seen:
            seen.add(text)
            order.append(text)
    return order


def summarize(records: Sequence[Record], column: str) -> dict[str, Any]:
    """Summary statistics over exactly the records handed in, and nothing else.

    Call it with the output of `coerce_numeric()`, which by construction holds no
    excluded row. `sd` is the sample standard deviation and is None at n = 1,
    where it is undefined rather than zero.
    """
    values: list[float] = []
    for record in records:
        raw = record.values.get(column)
        if not isinstance(raw, float):
            raise SourceDataRefused(
                f"summarize() needs coerce_numeric({column!r}) first; record "
                f"{record.number} still holds {raw!r}"
            )
        values.append(raw)
    if not values:
        raise SourceDataRefused(f"cannot summarise {column!r}: no rows")
    return {
        "n": len(values),
        "mean": statistics.fmean(values),
        "sd": statistics.stdev(values) if len(values) > 1 else None,
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
    }


def qa_prefix(output: Path) -> Path:
    """Normalise an output name to a prefix and make sure its directory exists."""
    text = str(output)
    if text.endswith(".qa.json"):
        output = Path(text[: -len(".qa.json")])
    elif output.suffix.lower() in FIGURE_SUFFIXES:
        output = output.with_suffix("")
    parent = output.parent
    if str(parent):
        parent.mkdir(parents=True, exist_ok=True)
    return output


def build_qa(
    table: Table,
    *,
    used: Sequence[Record],
    excluded: Sequence[Exclusion],
    required: Sequence[str],
    numeric: Sequence[str],
    exclude_column: str | None,
    summaries: Mapping[str, dict[str, Any]] | None = None,
    categories: Mapping[str, list[str]] | None = None,
    figure: str | None = None,
) -> dict[str, Any]:
    """Assemble the QA record for a table that passed the contract."""
    record = base_qa(STATUS_OK, figure)
    record["source"] = {
        "file": table.name,
        "sha256": table.sha256,
        "bytes": table.byte_size,
        "delimiter": describe_delimiter(table.delimiter),
        "columns": list(table.columns),
    }
    record["columns_used"] = {
        "required": list(required),
        "numeric": list(numeric),
        "exclusion_flag": exclude_column,
    }
    record["rows_input"] = table.rows_input
    record["rows_used"] = len(used)
    record["rows_excluded"] = len(excluded)
    record["exclusions"] = [item.as_dict() for item in excluded]
    if summaries:
        record["summaries"] = dict(summaries)
    if categories:
        record["categories"] = {name: list(order) for name, order in categories.items()}
    record["notes"] = [
        "rows_input = rows_used + rows_excluded; every excluded row is listed with its reason.",
        "Excluded rows were removed before numeric coercion, so they enter no summary statistic.",
        "Missing or non-finite values in the numeric columns are refused, never dropped.",
        "The source is identified by name and SHA-256 rather than by absolute path.",
    ]
    if summaries:
        record["notes"].append(
            "Summaries were computed over rows_used only (figure-style section 1.1)."
        )
    if record["rows_input"] != record["rows_used"] + record["rows_excluded"]:
        # Not an assert: `python -O` strips asserts, and this invariant is the
        # whole point of the record. A QA file whose arithmetic does not close
        # would let rows vanish between the source file and the panel.
        raise SourceDataRefused(
            f"row accounting does not close for {table.name}: "
            f"rows_input={record['rows_input']} but rows_used={record['rows_used']} "
            f"+ rows_excluded={record['rows_excluded']}"
        )
    return record


def base_qa(status: str, figure: str | None) -> dict[str, Any]:
    """Skeleton shared by the ok, refused and blocked records."""
    return {
        "schema": SCHEMA,
        "generated_by": "figure_source_data.py",
        "status": status,
        "figure": figure,
    }


def failure_qa(status: str, figure: str | None, source: Path, message: str) -> dict[str, Any]:
    """QA record for a run that produced no usable data.

    Written on purpose. Leaving the previous run's passing record beside a figure
    that failed to regenerate is how a stale pass gets shipped.
    """
    record = base_qa(status, figure)
    record["source"] = {"file": source.name}
    record["rows_input"] = None
    record["rows_used"] = 0
    record["rows_excluded"] = None
    record["exclusions"] = []
    record["error"] = message
    record["notes"] = [
        "refused: the source data was read and does not satisfy the contract."
        if status == STATUS_REFUSED
        else "blocked: the source data could not be read, so nothing was checked. "
        "This is not a pass.",
        "No figure should be published against this record.",
    ]
    return record


def write_qa(output: Path, record: Mapping[str, Any]) -> Path:
    """Write `<prefix>.qa.json` and return its path."""
    prefix = qa_prefix(output)
    path = prefix.with_name(prefix.name + ".qa.json")
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def split_columns(raw: str | None) -> list[str]:
    """Parse a comma-separated column list from the command line."""
    if not raw:
        return []
    return [name.strip() for name in raw.split(",") if name.strip()]


def unescape_delimiter(raw: str | None) -> str | None:
    r"""Allow `--delimiter '\t'` from a shell that will not send a real tab."""
    if raw is None:
        return None
    return {"\\t": "\t", "tab": "\t"}.get(raw, raw)


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Read, check and describe the table. Raises SourceDataError on failure."""
    required = split_columns(args.require)
    numeric = split_columns(args.numeric)
    summarize_columns = split_columns(args.summarize)
    category_columns = split_columns(args.category)

    table = read_table(args.input, unescape_delimiter(args.delimiter))
    require_columns(table, [*required, *numeric, *summarize_columns, *category_columns])

    kept, excluded = partition_excluded(table, args.exclude_column)
    if excluded and not kept:
        # Diagnose before coercing: "every row is flagged" is a different
        # problem from "the numbers are unusable", and saying so saves a hunt.
        raise SourceDataRefused(
            f"{table.name}: all {len(excluded)} row(s) are flagged excluded by "
            f"{args.exclude_column!r}; there is nothing left to plot."
        )
    coerce_targets = first_seen([*numeric, *summarize_columns])
    used = coerce_numeric(kept, coerce_targets, source=table.name) if coerce_targets else list(kept)
    if not used:
        raise SourceDataRefused(f"{table.name}: no rows remain to plot.")

    summaries = {column: summarize(used, column) for column in summarize_columns}
    categories = {
        column: first_seen(record.values[column] for record in used) for column in category_columns
    }
    return build_qa(
        table,
        used=used,
        excluded=excluded,
        required=required,
        numeric=coerce_targets,
        exclude_column=args.exclude_column,
        summaries=summaries,
        categories=categories,
        figure=args.figure,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check a figure's source table and write its <figure>.qa.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 ok, 2 refused (data violates the contract), "
        "3 blocked (data could not be read, nothing was checked).",
    )
    parser.add_argument("--input", type=Path, required=True, help="source CSV/TSV file")
    parser.add_argument("--output", type=Path, required=True, help="figure prefix; writes <prefix>.qa.json")
    parser.add_argument("--delimiter", help=r"override the delimiter, e.g. ';' or '\t'")
    parser.add_argument("--require", help="comma-separated columns that must exist")
    parser.add_argument("--numeric", help="comma-separated columns coerced to finite floats")
    parser.add_argument("--summarize", help="comma-separated numeric columns to summarise over used rows")
    parser.add_argument("--category", help="comma-separated categorical columns whose order to record")
    parser.add_argument("--exclude-column", help="source column flagging rows held out of the panel")
    parser.add_argument("--figure", help="figure or panel label recorded in the QA file")
    parser.add_argument("--quiet", action="store_true", help="write the QA file without printing it")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        record = run(args)
    except SourceDataError as exc:
        status = STATUS_BLOCKED if isinstance(exc, SourceDataBlocked) else STATUS_REFUSED
        record = failure_qa(status, args.figure, args.input, str(exc))
        print(f"{status}: {exc}", file=sys.stderr)
        try:
            path = write_qa(args.output, record)
        except OSError as write_error:
            print(f"warning: could not write the QA record: {write_error}", file=sys.stderr)
        else:
            print(f"wrote {path}", file=sys.stderr)
        return EXIT_BLOCKED if status == STATUS_BLOCKED else EXIT_REFUSED

    path = write_qa(args.output, record)
    if not args.quiet:
        print(json.dumps(record, indent=2, ensure_ascii=False))
    print(f"wrote {path}", file=sys.stderr)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
