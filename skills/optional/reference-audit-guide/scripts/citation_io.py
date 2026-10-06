"""Shared local input handling for the two citation audit CLIs."""
from pathlib import Path
import re


def bibtex_blocks(text):
    """Locate top-level blocks so legacy parsers cannot silently skip a tail."""
    blocks, pos = [], 0
    header = re.compile(r"@\s*([a-z]+)\s*([({])", re.I)
    while match := header.search(text, pos):
        kind, opening = match.groups()
        kind = kind.lower()
        level = 1 if opening == "{" else 0
        depth, quoted, escaped = level, False, False
        end = match.end()
        while end < len(text):
            char = text[end]
            end += 1
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"' and depth == level and kind != "comment":
                quoted = not quoted
            elif not quoted:
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                if (opening == "{" and depth == 0) or (opening == "(" and char == ")" and depth == 0):
                    break
        else:
            raise ValueError(f"未闭合的 BibTeX 块: @{kind}")
        blocks.append((kind, match.start(), end))
        pos = end
    return blocks


def load_bibtex(path):
    """Return the same entry dictionaries with bibtexparser 1.x and 2.x."""
    try:
        import bibtexparser
    except ImportError as exc:
        raise ImportError("需要安装 bibtexparser: pip install bibtexparser") from exc
    text = Path(path).read_text(encoding="utf-8-sig")
    blocks = bibtex_blocks(text)
    expected = sum(kind not in {"comment", "preamble", "string"} for kind, _, _ in blocks)
    try:
        if hasattr(bibtexparser, "parse_string"):
            library = bibtexparser.parse_string(text)
            if library.failed_blocks:
                raise ValueError(f"{len(library.failed_blocks)} failed blocks")
            entries = [dict(entry) for entry in library.entries]
        else:
            from bibtexparser.bparser import BibTexParser
            # Legacy @comment handling can misread nested entry-like text.
            for kind, start, end in reversed(blocks):
                if kind == "comment":
                    text = text[:start] + " " * (end - start) + text[end:]
            database = BibTexParser(common_strings=True, ignore_nonstandard_types=False).parse(text, partial=False)
            entries = database.entries
            for kind, start, end in blocks:
                if kind == "string":
                    name = re.match(r"@\s*string\s*[({]\s*([\w-]+)\s*=", text[start:end], re.I)
                    if not name or name.group(1).lower() not in database.strings:
                        raise ValueError("Unparsed @string block")
            if len(database.preambles) != sum(kind == "preamble" for kind, _, _ in blocks):
                raise ValueError("Unparsed @preamble block")
        if len(entries) != expected:
            raise ValueError("Unparsed or duplicate bibliography entries")
    except Exception as exc:
        raise ValueError(f"无法解析 BibTeX 文件: {path}: {exc}") from exc
    if not entries:
        raise ValueError(f"BibTeX 文件中没有引用条目: {path}")
    return entries


def without_comments(text):
    return re.sub(r"(?m)(?<!\\)%.*$", "", text)


def latex_citations(text):
    commands = r"(?:cite(?:[tp]|alp|alt|author|year|yearpar)?|[aA]utocite|[pP]arencite|[tT]extcite|[sS]martcite|[fF]ootcite|nocite)"
    matches = re.findall(r"\\" + commands + r"\*?\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]+)\}", without_comments(text))
    return sorted({key.strip() for match in matches for key in match.split(",") if key.strip()})


def resolve_inputs(input_file, bib_files=None, tex_file=None, check_latex=False):
    """Resolve literal bibliography declarations relative to the .tex file."""
    source = Path(input_file)
    bibs = [Path(p) for p in (bib_files or [])]
    tex = Path(tex_file) if tex_file else None
    if source.suffix.lower() == ".bib":
        bibs.insert(0, source)
        if check_latex and tex is None:
            tex = source.with_suffix(".tex")
    elif source.suffix.lower() == ".tex":
        tex = source
        if not bibs:
            content = without_comments(tex.read_text(encoding="utf-8-sig"))
            for declaration in re.findall(r"\\(?:bibliography|addbibresource(?:\[[^\]]*\])?)\s*\{([^}]+)\}", content):
                for raw in declaration.split(","):
                    path = Path(raw.strip())
                    if path.suffix.lower() != ".bib":
                        path = path.with_suffix(".bib")
                    bibs.append(tex.parent / path)
            if not bibs:
                raise ValueError("没有找到 bibliography/addbibresource；请用 --bib 指定 .bib 文件")
    else:
        raise ValueError("输入文件必须是 .bib 或 .tex")
    if tex is not None and not tex.is_file():
        raise FileNotFoundError(f"LaTeX 文件不存在: {tex}")
    return list(dict.fromkeys(bibs)), tex


def fix_common_text(text):
    """Preserve source text except explicit DOI URL and page-range fixes."""
    # Only field names at an entry's outer level may be edited. A multiline
    # title or @comment can itself contain a line that looks like `doi = ...`.
    field_positions = set()
    depth, quoted, escaped, kind, closing = 0, False, False, "", "}"
    pos = 0
    while pos < len(text):
        char = text[pos]
        if depth == 0:
            entry = re.match(r"@\s*([a-z]+)\s*([({])", text[pos:], re.I)
            if entry:
                kind = entry.group(1).lower()
                closing = "}" if entry.group(2) == "{" else ")"
                depth = 1
                pos += entry.end()
                continue
        elif not escaped:
            if not quoted and depth == 1 and kind not in {"comment", "preamble", "string"}:
                field_positions.add(pos)
            if char == '"' and depth == 1:
                quoted = not quoted
            elif not quoted:
                if char == "{":
                    depth += 1
                elif char == "}" and depth > 1:
                    depth -= 1
                elif char == closing and depth == 1:
                    depth = 0
        escaped = char == "\\" and not escaped
        pos += 1
    pattern = re.compile(r'(?im)^(\s*(doi|pages)\s*=\s*)([{\"])([^{}\"\n]*)([}\"])')
    def fix(match):
        if match.start(2) not in field_positions:
            return match.group()
        prefix, field, opening, value, closing = match.groups()
        if (opening, closing) not in {('{', '}'), ('"', '"')}:
            return match.group()
        if field.lower() == "doi":
            value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
        else:
            value = re.sub(r"(?<=\d)\s*[-–]\s*(?=\d)", "--", value)
        return prefix + opening + value + closing
    return pattern.sub(fix, text)
