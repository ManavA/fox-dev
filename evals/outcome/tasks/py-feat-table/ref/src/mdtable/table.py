"""Render GitHub-flavoured markdown tables."""
from __future__ import annotations

from typing import Optional, Sequence

MIN_WIDTH = 3
ALIGNMENTS = ("left", "right", "center")


def _cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _pad(text: str, width: int, align: str) -> str:
    if align == "right":
        return text.rjust(width)
    if align == "center":
        left = (width - len(text)) // 2
        return " " * left + text + " " * (width - len(text) - left)
    return text.ljust(width)


def _separator(width: int, align: Optional[str]) -> str:
    if align is None:
        return "-" * width
    if align == "left":
        return ":" + "-" * (width - 1)
    if align == "right":
        return "-" * (width - 1) + ":"
    return ":" + "-" * (width - 2) + ":"


def render_table(
    headers: Sequence[object],
    rows: Sequence[Sequence[object]],
    align: Optional[Sequence[str]] = None,
) -> str:
    """Return a markdown table with padded columns.

    Every row must have as many cells as there are headers.
    """
    head = [_cell(h) for h in headers]
    body = []
    for row in rows:
        if len(row) != len(head):
            raise ValueError(f"row has {len(row)} cells, expected {len(head)}")
        body.append([_cell(c) for c in row])

    if align is not None:
        if len(align) > len(head):
            raise ValueError("more alignments than columns")
        for a in align:
            if a not in ALIGNMENTS:
                raise ValueError(f"invalid alignment: {a!r}")
        aligns: list[Optional[str]] = list(align) + ["left"] * (len(head) - len(align))
    else:
        aligns = [None] * len(head)

    widths = [max([MIN_WIDTH, len(h)] + [len(r[i]) for r in body]) for i, h in enumerate(head)]

    def line(cells: Sequence[str]) -> str:
        return "| " + " | ".join(_pad(c, w, a or "left") for c, w, a in zip(cells, widths, aligns)) + " |"

    sep = "| " + " | ".join(_separator(w, a) for w, a in zip(widths, aligns)) + " |"
    return "\n".join([line(head), sep] + [line(r) for r in body])
