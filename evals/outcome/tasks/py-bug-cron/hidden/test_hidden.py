from datetime import datetime

import pytest

from cronlite import matches, parse_field


def test_step_range_start():
    assert parse_field("7-30/10", 0, 59) == {7, 17, 27}


def test_step_from_start():
    assert parse_field("5/15", 0, 59) == {5, 20, 35, 50}


def test_step_star_still_ok():
    assert parse_field("*/15", 0, 59) == {0, 15, 30, 45}
    assert parse_field("*/10", 1, 31) == {1, 11, 21, 31}


def test_step_in_list():
    assert parse_field("1,10-20/5,40", 0, 59) == {1, 10, 15, 20, 40}


def test_bad_step():
    with pytest.raises(ValueError):
        parse_field("*/0", 0, 59)


def test_plain_range_and_single():
    assert parse_field("3-5", 0, 59) == {3, 4, 5}
    assert parse_field("3", 0, 59) == {3}


def test_still_validates_range():
    with pytest.raises(ValueError):
        parse_field("5-70", 0, 59)
    with pytest.raises(ValueError):
        parse_field("5/10-3", 0, 59)


def test_generic_parse_field_has_no_weekday_magic():
    with pytest.raises(ValueError):
        parse_field("7", 0, 6)


SUN = datetime(2024, 3, 3, 9, 0)  # Sunday
FRI = datetime(2024, 3, 8, 9, 0)
FRI13 = datetime(2024, 9, 13, 9, 0)
MON13 = datetime(2024, 5, 13, 9, 0)
TUE = datetime(2024, 3, 5, 9, 0)


def test_sunday_as_seven():
    assert matches("0 9 * * 7", SUN)
    assert matches("0 9 * * 0", SUN)
    assert not matches("0 9 * * 7", TUE)


def test_seven_in_list_and_range():
    assert matches("0 9 * * 1,7", SUN)
    assert matches("0 9 * * 5-7", SUN)
    assert matches("0 9 * * 5-7", FRI)
    assert not matches("0 9 * * 5-7", TUE)


def test_dom_and_dow_or_semantics():
    assert matches("0 9 13 * 5", FRI13)
    assert matches("0 9 13 * 5", FRI)
    assert matches("0 9 13 * 5", MON13)
    assert not matches("0 9 13 * 5", TUE)


def test_only_dom_restricted():
    assert matches("0 9 13 * *", MON13)
    assert not matches("0 9 13 * *", FRI)


def test_only_dow_restricted():
    assert matches("0 9 * * 5", FRI)
    assert not matches("0 9 * * 5", MON13)


def test_other_fields_still_and():
    assert not matches("30 9 13 * 5", FRI13)
    assert not matches("0 9 13 6 5", FRI13)


def test_existing_behaviour():
    assert matches("30 9 * * *", datetime(2024, 3, 5, 9, 30))
    assert not matches("30 9 * * *", datetime(2024, 3, 5, 9, 31))
    with pytest.raises(ValueError):
        matches("* * * *", TUE)
