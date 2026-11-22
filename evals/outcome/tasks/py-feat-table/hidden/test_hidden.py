import pytest

from mdtable import render_table


def test_example_from_issue():
    out = render_table(["Name", "Qty"], [["apple", "3"], ["kiwi", "12"]], align=["left", "right"])
    assert out == "\n".join(
        ["| Name  | Qty |", "| :---- | --: |", "| apple |   3 |", "| kiwi  |  12 |"]
    )


def test_none_is_unchanged():
    assert render_table(["a"], [["b"]], align=None) == "| a   |\n| --- |\n| b   |"
    assert render_table(["a"], [["b"]]) == "| a   |\n| --- |\n| b   |"


def test_center_odd_space_goes_right_and_min_width():
    out = render_table(["a", "bcd"], [["x", "yz"]], align=["center", "center"])
    assert out.split("\n") == ["|  a  | bcd |", "| :-: | :-: |", "|  x  | yz  |"]


def test_center_wider():
    out = render_table(["head"], [["ab"]], align=["center"])
    assert out.split("\n") == ["| head |", "| :--: |", "|  ab  |"]


def test_center_header_padding():
    out = render_table(["a", "long header"], [["1", "2"]], align=["center", "center"])
    lines = out.split("\n")
    assert lines[0] == "|  a  | long header |"
    assert lines[1] == "| :-: | :---------: |"


def test_short_align_defaults_left_with_markers():
    out = render_table(["a", "b"], [["1", "2"]], align=["right"])
    assert out.split("\n") == ["|   a | b   |", "| --: | :-- |", "|   1 | 2   |"]


def test_empty_align_sequence_marks_everything_left():
    out = render_table(["a"], [["1"]], align=[])
    assert out.split("\n")[1] == "| :-- |"


def test_too_many_alignments():
    with pytest.raises(ValueError):
        render_table(["a"], [["1"]], align=["left", "right"])


def test_bad_alignment_value():
    with pytest.raises(ValueError):
        render_table(["a"], [["1"]], align=["middle"])


def test_row_length_still_checked_with_align():
    with pytest.raises(ValueError):
        render_table(["a", "b"], [["1"]], align=["left"])


def test_tuple_align_ok():
    out = render_table(["a"], [["1"]], align=("right",))
    assert out.split("\n")[1] == "| --: |"
