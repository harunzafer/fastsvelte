from datetime import datetime, timezone

from app.util.quota_util import get_current_quota_period


def dt(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)


def test_same_month():
    anchor = dt("2025-07-01")
    now = dt("2025-07-15")
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-07-01")
    assert end == dt("2025-08-01")


def test_rollover_month():
    anchor = dt("2025-04-10")
    now = dt("2025-06-15")
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-06-10")
    assert end == dt("2025-07-10")


def test_day_before_anchor_rolls_back():
    anchor = dt("2025-01-20")
    now = dt("2025-04-19")  # < 20th → previous window
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-03-20")
    assert end == dt("2025-04-20")


def test_day_on_or_after_anchor():
    anchor = dt("2025-01-20")
    now = dt("2025-04-20")  # = anchor day → current window
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-04-20")
    assert end == dt("2025-05-20")


def test_february_rollover_from_jan_31_second_period():
    anchor = dt("2025-01-31")
    now = dt("2025-02-28")
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-02-28")
    assert end == dt("2025-03-28")


def test_february_rollover_from_jan_31_first_period():
    anchor = dt("2025-01-31")
    now = dt("2025-02-27")
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-01-31")
    assert end == dt("2025-02-28")


def test_precise_time_rollover_first_period():
    anchor = dt("2025-01-31T16:30:00")
    now = dt("2025-02-28T16:29:59")  # last second int the first period
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-01-31T16:30:00")
    assert end == dt("2025-02-28T16:30:00")


def test_precise_time_rollover_second_period():
    anchor = dt("2025-01-31T16:30:00")
    now = dt("2025-02-28T17:00:00")  # 30 min into second period
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-02-28T16:30:00")
    assert end == dt("2025-03-28T16:30:00")


def test_precise_time_rollover_second_period_2():
    anchor = dt("2025-01-31T16:30:00")
    now = dt("2025-03-01T10:00:00")
    start, end = get_current_quota_period(anchor, now=now)
    assert start == dt("2025-02-28T16:30:00")
    assert end == dt("2025-03-28T16:30:00")
