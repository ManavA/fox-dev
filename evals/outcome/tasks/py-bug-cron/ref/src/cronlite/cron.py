"""Minimal 5-field cron expression matching: minute hour day-of-month month day-of-week."""
from __future__ import annotations

from datetime import datetime

# (min, max) for each field
RANGES = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 7)]


def parse_field(expr: str, lo: int, hi: int) -> set[int]:
    """Expand one cron field such as ``*``, ``5``, ``1-5``, ``*/15`` or ``1,3,5`` into a set of ints."""
    values: set[int] = set()
    for part in expr.split(","):
        step = 1
        has_step = "/" in part
        if has_step:
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
            start = int(part)
            end = hi if has_step else start
        if start < lo or end > hi or start > end:
            raise ValueError(f"value out of range in {expr!r}")
        values.update(range(start, end + 1, step))
    return values


def matches(expr: str, when: datetime) -> bool:
    """True if ``when`` satisfies the 5-field cron expression ``expr``."""
    fields = expr.split()
    if len(fields) != 5:
        raise ValueError("expected 5 fields")
    minute, hour, dom, month, dow = (parse_field(f, lo, hi) for f, (lo, hi) in zip(fields, RANGES))
    if 7 in dow:
        dow = (dow - {7}) | {0}
    weekday = (when.weekday() + 1) % 7  # cron: Sunday=0
    if fields[2] != "*" and fields[4] != "*":
        day_ok = when.day in dom or weekday in dow
    else:
        day_ok = when.day in dom and weekday in dow
    return when.minute in minute and when.hour in hour and when.month in month and day_ok
