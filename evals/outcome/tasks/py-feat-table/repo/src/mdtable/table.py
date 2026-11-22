"""Render GitHub-flavoured markdown tables."""
from __future__ import annotations

from typing import Sequence

MIN_WIDTH = 3


def _cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_table(headers: Sequence[object], rows: Sequence[Sequence[object]]) -> str:
    """Return a markdown table with padded columns.

    Every row must have as many cells as there are headers.
    """
    head = [_cell(h) for h in headers]
    body = []
    for row in rows:
        if len(row) != len(head):
            raise ValueError(f"row has {len(row)} cells, expected {len(head)}")
        body.append([_cell(c) for c in row])

    widths = [max([MIN_WIDTH, len(h)] + [len(r[i]) for r in body]) for i, h in enumerate(head)]

    def line(cells: Sequence[str]) -> str:
        return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"

    sep = "| " + " | ".join("-" * w for w in widths) + " |"
    return "\n".join([line(head), sep] + [line(r) for r in body])
