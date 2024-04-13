from datetime import date

import pytest

from netznoe_smartmeter_portal_api.api import NetzNoeSmartmeterPortalDataError

METER_ID = 'ATxxTEST'


def test_fetch_year(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Year', 'data_year')
    result = api.get_year(METER_ID, year=2023)
    assert len(result.values) == 12
    assert len(result.peak_demands) == 12


def test_fetch_month(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Month', 'data_month')
    result = api.get_month(METER_ID, year=2023, month=3)
    assert len(result.metered) == 31
    assert len(result.metered_peak_demands) == 31


def test_fetch_week(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Week', 'data_week')
    result = api.get_week(METER_ID, start_date=date(2023, 3, 27), end_date=date(2023, 4, 3))
    assert len(result.metered) == 7
    assert len(result.metered_peak_demands) == 7


def test_fetch_day(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Day', 'data_day')
    result = api.get_day(METER_ID, day=date(2023, 4, 1))
    assert len(result.metered) == 95
    assert len(result.estimated) == 1
    assert len(result.estimated_qualities) == 1
    assert len(result.metered_peak_demands) == 96


def test_fetch_year_api_error(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Year', 'data_year', status=999)
    with pytest.raises(NetzNoeSmartmeterPortalDataError) as excinfo:
        api.get_year(METER_ID, year=2023)
    assert str(excinfo.value) == 'Fetching yearly data failed'


def test_fetch_month_api_error(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Month', 'data_month', status=999)
    with pytest.raises(NetzNoeSmartmeterPortalDataError) as excinfo:
        api.get_month(METER_ID, year=2023, month=3)
    assert str(excinfo.value) == 'Fetching monthly data failed'


def test_fetch_week_api_error(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Week', 'data_week', status=999)
    with pytest.raises(NetzNoeSmartmeterPortalDataError) as excinfo:
        api.get_week(METER_ID, start_date=date(2023, 3, 27), end_date=date(2023, 4, 3))
    assert str(excinfo.value) == 'Fetching weekly data failed'


def test_fetch_day_api_error(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/ConsumptionRecord/Day', 'data_day', status=999)
    with pytest.raises(NetzNoeSmartmeterPortalDataError) as excinfo:
        api.get_day(METER_ID, day=date(2023, 4, 1))
    assert str(excinfo.value) == 'Fetching daily data failed'


def test_fetch_year_value_error(api, response):
    with pytest.raises(ValueError) as excinfo:
        api.get_year(METER_ID, year=1900)
    assert str(excinfo.value) == 'year not in valid range'


def test_fetch_month_value_error(api, response):
    with pytest.raises(ValueError) as excinfo:
        api.get_month(METER_ID, year=1900, month=3)
    assert str(excinfo.value) == 'year or month not in valid range'

    with pytest.raises(ValueError) as excinfo:
        api.get_month(METER_ID, year=2023, month=13)
    assert str(excinfo.value) == 'year or month not in valid range'
