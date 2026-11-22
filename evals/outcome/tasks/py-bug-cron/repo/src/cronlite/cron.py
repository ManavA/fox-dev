"""Minimal 5-field cron expression matching: minute hour day-of-month month day-of-week."""
from __future__ import annotations

from datetime import datetime

# (min, max) for each field
RANGES = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]


def parse_field(expr: str, lo: int, hi: int) -> set[int]:
    """Expand one cron field such as ``*``, ``5``, ``1-5``, ``*/15`` or ``1,3,5`` into a set of ints."""
    values: set[int] = set()
    for part in expr.split(","):
        step = 1
        if "/" in part:
            part, step_s = part.split("/")
            step = int(step_s)
            if step <= 0:
                raise ValueError(f"bad step: {step_s}")
        if part == "*":
            start, end = lo, hi
        elif "-" in part:
            a, b = part.split("-")
            start, end = int(a), int(b)
        else:
            start = end = int(part)
        if start < lo or end > hi or start > end:
            raise ValueError(f"value out of range in {expr!r}")
        values.update(v for v in range(lo, end + 1) if start <= v and v % step == 0)
    return values


def matches(expr: str, when: datetime) -> bool:
    """True if ``when`` satisfies the 5-field cron expression ``expr``."""
    fields = expr.split()
    if len(fields) != 5:
        raise ValueError("expected 5 fields")
    parsed = [parse_field(f, lo, hi) for f, (lo, hi) in zip(fields, RANGES)]
    minute, hour, dom, month, dow = parsed
    weekday = (when.weekday() + 1) % 7  # cron: Sunday=0
    return (
        when.minute in minute
        and when.hour in hour
        and when.day in dom
        and when.month in month
        and weekday in dow
    )
