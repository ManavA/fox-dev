from datetime import datetime

import pytest

from cronlite import matches, parse_field


def test_star():
    assert parse_field("*", 0, 5) == {0, 1, 2, 3, 4, 5}


def test_list_and_range():
    assert parse_field("1,3-5", 0, 10) == {1, 3, 4, 5}


def test_star_step():
    assert parse_field("*/15", 0, 59) == {0, 15, 30, 45}


def test_out_of_range():
    with pytest.raises(ValueError):
        parse_field("70", 0, 59)


def test_matches_simple():
    assert matches("30 9 * * *", datetime(2024, 3, 5, 9, 30))
    assert not matches("30 9 * * *", datetime(2024, 3, 5, 9, 31))


def test_matches_weekday():
    # 2024-03-04 is a Monday
    assert matches("0 0 * * 1", datetime(2024, 3, 4, 0, 0))
    assert not matches("0 0 * * 2", datetime(2024, 3, 4, 0, 0))
