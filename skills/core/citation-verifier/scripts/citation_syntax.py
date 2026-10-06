"""Shared static LaTeX citation scanning; does not expand user-defined macros."""
import re


CITE_PATTERN = re.compile(
    r"\\[Cc]ite[a-zA-Z]*\*?\s*(?:\[[^\]]*\]\s*)*\{([^{}]*)\}"
)


def strip_tex_comments(text: str, preserve_positions: bool = False) -> str:
    """Respect escaped percent signs; optionally retain offsets and newlines."""
    out = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            out.append(text[i:i + 2])
            i += 2
        elif text[i] == "%":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            if preserve_positions:
                out.append(" " * (end - i))
            elif end < len(text):
                end += 1
                while end < len(text) and text[end] in " \t":
                    end += 1
            i = end
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def iter_citations(text: str, tex: bool = True):
    searchable = strip_tex_comments(text, preserve_positions=True) if tex else text
    for match in CITE_PATTERN.finditer(searchable):
        # An even preceding slash run is real TeX (e.g. line break + citation).
        start = match.start()
        while start > 0 and searchable[start - 1] == "\\":
            start -= 1
        if (match.start() - start) % 2:
            continue
        raw_keys = text[match.start(1):match.end(1)]
        keys = strip_tex_comments(raw_keys) if tex else raw_keys
        lineno = text.count("\n", 0, match.start()) + 1
        for key in keys.split(","):
            if key.strip():
                yield lineno, key.strip()
