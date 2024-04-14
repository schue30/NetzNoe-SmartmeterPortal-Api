from datetime import datetime, date
from zoneinfo import ZoneInfo

import pytest


def test_dst_winter_to_summer(api, response):
    tz_utc = ZoneInfo('UTC')
    tz_vienna = ZoneInfo('Europe/Vienna')
    start_date = datetime(2024, 3, 31, 1, 15, tzinfo=tz_vienna).astimezone(tz_utc)
    test_datetimes = [
        '2024-03-31 01:30:00+01:00',
        '2024-03-31 01:45:00+01:00',
        '2024-03-31 03:00:00+02:00',
        '2024-03-31 03:15:00+02:00'
    ]
    for verify_datetime in test_datetimes:
        start_date = api._calc_next_datetime(start_date, {'minutes': 15})
        assert str(start_date.astimezone(tz_vienna)) == verify_datetime


def test_dst_summer_to_winter(api, response):
    tz_utc = ZoneInfo('UTC')
    tz_vienna = ZoneInfo('Europe/Vienna')
    start_date = datetime(2024, 10, 27, 1, 15, tzinfo=tz_vienna).astimezone(tz_utc)
    test_datetimes = [
        '2024-10-27 01:30:00+02:00',
        '2024-10-27 01:45:00+02:00',
        '2024-10-27 02:00:00+02:00',
        '2024-10-27 02:15:00+02:00',
        '2024-10-27 02:30:00+02:00',
        '2024-10-27 02:45:00+02:00',
        '2024-10-27 02:00:00+01:00',
        '2024-10-27 02:15:00+01:00',
        '2024-10-27 02:30:00+01:00',
        '2024-10-27 02:45:00+01:00',
        '2024-10-27 03:00:00+01:00',
        '2024-10-27 03:15:00+01:00'
    ]
    for verify_datetime in test_datetimes:
        start_date = api._calc_next_datetime(start_date, {'minutes': 15})
        assert str(start_date.astimezone(tz_vienna)) == verify_datetime


def test_months(api, response):
    test_datetimes = {
        date(2024, 1, 1): '2024-02-01',
        date(2024, 11, 1): '2024-12-01',
        date(2024, 12, 1): '2025-01-01'
    }
    for input_datetime, output_datetime in test_datetimes.items():
        assert str(api._calc_next_datetime(input_datetime, {'months': 1})) == output_datetime


def test_6_months(api, response):
    test_datetimes = {
        date(2024, 1, 1): '2024-07-01',
        date(2024, 11, 1): '2025-05-01',
        date(2024, 12, 1): '2025-06-01'
    }
    for input_datetime, output_datetime in test_datetimes.items():
        assert str(api._calc_next_datetime(input_datetime, {'months': 6})) == output_datetime


def test_days(api, response):
    test_datetimes = {
        date(2024, 1, 1): '2024-01-02',
        date(2024, 2, 29): '2024-03-01',
        date(2024, 11, 1): '2024-11-02'
    }
    for input_datetime, output_datetime in test_datetimes.items():
        assert str(api._calc_next_datetime(input_datetime, {'days': 1})) == output_datetime


def test_unimplemented_increment(api, response):
    with pytest.raises(ValueError) as excinfo:
        api._calc_next_datetime(date(2024, 1, 1), {'not_implemented': 1})
    assert str(excinfo.value) == 'Unsupported time_increase interval'
