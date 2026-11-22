"""A tiny arithmetic expression evaluator (recursive descent)."""
from __future__ import annotations

import re

TOKEN = re.compile(r"\s*(?:(\d+\.?\d*|\.\d+)|(.))")


class CalcError(Exception):
    """Raised for malformed input or arithmetic errors."""


def tokenize(src: str) -> list[tuple[str, str]]:
    """Return ``(kind, text)`` pairs; kind is ``num`` or ``op``."""
    out = []
    pos = 0
    while pos < len(src):
        m = TOKEN.match(src, pos)
        if m is None or m.end() == pos:
            break
        pos = m.end()
        if m.group(1) is not None:
            out.append(("num", m.group(1)))
        elif m.group(2) is not None and not m.group(2).isspace():
            out.append(("op", m.group(2)))
    return out


class Parser:
    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.i = 0

    def peek(self) -> tuple[str, str] | None:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self) -> tuple[str, str]:
        tok = self.peek()
        if tok is None:
            raise CalcError("unexpected end of input")
        self.i += 1
        return tok

    def expr(self) -> float:
        value = self.term()
        while (tok := self.peek()) and tok[1] in "+-":
            self.take()
            rhs = self.term()
            value = value + rhs if tok[1] == "+" else value - rhs
        return value

    def term(self) -> float:
        value = self.unary()
        while (tok := self.peek()) and tok[1] in "*/":
            self.take()
            rhs = self.unary()
            if tok[1] == "/":
                if rhs == 0:
                    raise CalcError("division by zero")
                value = value / rhs
            else:
                value = value * rhs
        return value

    def unary(self) -> float:
        tok = self.peek()
        if tok and tok[1] == "-":
            self.take()
            return -self.unary()
        return self.atom()

    def atom(self) -> float:
        kind, text = self.take()
        if kind == "num":
            return float(text)
        if text == "(":
            value = self.expr()
            if self.take()[1] != ")":
                raise CalcError("expected )")
            return value
        raise CalcError(f"unexpected {text!r}")


def evaluate(src: str) -> float:
    """Evaluate an arithmetic expression with + - * / unary minus and parentheses."""
    p = Parser(tokenize(src))
    value = p.expr()
    if p.peek() is not None:
        raise CalcError(f"unexpected {p.peek()[1]!r}")
    return value
