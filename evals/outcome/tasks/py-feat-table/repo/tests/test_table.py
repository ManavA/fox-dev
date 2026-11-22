import pytest

from mdtable import render_table


def test_basic():
    out = render_table(["Name", "Qty"], [["apple", 3], ["kiwi", 12]])
    assert out == "\n".join(
        [
            "| Name  | Qty |",
            "| ----- | --- |",
            "| apple | 3   |",
            "| kiwi  | 12  |",
        ]
    )


def test_min_width():
    assert render_table(["a"], [["b"]]) == "| a   |\n| --- |\n| b   |"


def test_pipe_and_newline_are_escaped():
    out = render_table(["x"], [["a|b\nc"]])
    assert "a\\|b c" in out


def test_row_length_checked():
    with pytest.raises(ValueError):
        render_table(["a", "b"], [["only one"]])
