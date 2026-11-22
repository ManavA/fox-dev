"""A tiny arithmetic expression evaluator (recursive descent)."""
from __future__ import annotations

import math
import re
from typing import Mapping, Optional

TOKEN = re.compile(r"\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-z_]\w*)|(\*\*|.))")


class CalcError(Exception):
    """Raised for malformed input or arithmetic errors."""

    def __init__(self, message: str, position: int = 0) -> None:
        super().__init__(message)
        self.position = position


Token = tuple[str, str, int]  # kind, text, position


def tokenize(src: str) -> list[Token]:
    """Return ``(kind, text, position)`` triples; kind is ``num``, ``name`` or ``op``."""
    out: list[Token] = []
    pos = 0
    while pos < len(src):
        m = TOKEN.match(src, pos)
        if m is None or m.end() == pos:
            break
        pos = m.end()
        if m.group(1) is not None:
            out.append(("num", m.group(1), m.start(1)))
        elif m.group(2) is not None:
            out.append(("name", m.group(2), m.start(2)))
        elif m.group(3) is not None and not m.group(3).isspace():
            out.append(("op", m.group(3), m.start(3)))
    return out


FUNCS = {"min": (1, None), "max": (1, None), "abs": (1, 1), "sqrt": (1, 1), "round": (1, 2)}


class Parser:
    def __init__(self, tokens: list[Token], src: str, variables: Mapping[str, float]) -> None:
        self.tokens = tokens
        self.src = src
        self.vars = variables
        self.i = 0

    def peek(self) -> Optional[Token]:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self) -> Token:
        tok = self.peek()
        if tok is None:
            raise CalcError("unexpected end of input", len(self.src))
        self.i += 1
        return tok

    def at_op(self, ops: str) -> Optional[Token]:
        tok = self.peek()
        return tok if tok and tok[0] == "op" and tok[1] in ops.split() else None

    def expr(self) -> float:
        value = self.term()
        while tok := self.at_op("+ -"):
            self.take()
            rhs = self.term()
            value = value + rhs if tok[1] == "+" else value - rhs
        return value

    def term(self) -> float:
        value = self.unary()
        while tok := self.at_op("* / %"):
            self.take()
            rhs = self.unary()
            if tok[1] == "*":
                value = value * rhs
            elif rhs == 0:
                raise CalcError("division by zero", tok[2])
            else:
                value = value / rhs if tok[1] == "/" else value % rhs
        return value

    def unary(self) -> float:
        if self.at_op("-"):
            self.take()
            return -self.unary()
        return self.power()

    def power(self) -> float:
        base = self.atom()
        if self.at_op("**"):
            self.take()
            return base ** self.unary()
        return base

    def args(self) -> list[float]:
        out = [self.expr()]
        while self.at_op(","):
            self.take()
            out.append(self.expr())
        return out

    def call(self, name: str, pos: int) -> float:
        self.take()  # (
        values = self.args()
        close = self.take()
        if close[1] != ")":
            raise CalcError("expected )", close[2])
        lo, hi = FUNCS[name]
        if len(values) < lo or (hi is not None and len(values) > hi):
            raise CalcError(f"wrong number of arguments for {name}", pos)
        if name == "min":
            return min(values)
        if name == "max":
            return max(values)
        if name == "abs":
            return abs(values[0])
        if name == "sqrt":
            if values[0] < 0:
                raise CalcError("sqrt of negative number", pos)
            return math.sqrt(values[0])
        return float(round(values[0], int(values[1])) if len(values) == 2 else round(values[0]))

    def atom(self) -> float:
        kind, text, pos = self.take()
        if kind == "num":
            return float(text)
        if kind == "name":
            nxt = self.peek()
            if nxt and nxt[1] == "(" and nxt[0] == "op":
                if text not in FUNCS:
                    raise CalcError(f"unknown function {text}", pos)
                return self.call(text, pos)
            if text not in self.vars:
                raise CalcError(f"unknown variable {text}", pos)
            return float(self.vars[text])
        if text == "(":
            value = self.expr()
            close = self.take()
            if close[1] != ")":
                raise CalcError("expected )", close[2])
            return value
        raise CalcError(f"unexpected {text!r}", pos)


def evaluate(src: str, variables: Optional[Mapping[str, float]] = None) -> float:
    """Evaluate an arithmetic expression."""
    p = Parser(tokenize(src), src, variables or {})
    value = p.expr()
    if p.peek() is not None:
        raise CalcError(f"unexpected {p.peek()[1]!r}", p.peek()[2])
    return value
