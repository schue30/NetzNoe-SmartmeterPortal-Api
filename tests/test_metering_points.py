import pytest

from netznoe_smartmeter_portal_api.api import NetzNoeSmartmeterPortalDataError


def test_get_metering_points(api, response):
    response.get(
        'https://smartmeter.netz-noe.at/orchestration/User/GetAccountIdByBussinespartnerId', 'data_account_id_1'
    )
    response.get(
        'https://smartmeter.netz-noe.at/orchestration/User/GetMeteringPointByAccountId', 'data_metering_point'
    )
    result = api.get_metering_points()
    assert len(result) == 1
    assert result[0].metering_point_id == 'AT0020000000000000000000100123456'


def test_get_account_ids(api, response):
    response.get(
        'https://smartmeter.netz-noe.at/orchestration/User/GetAccountIdByBussinespartnerId', 'data_account_id_2'
    )
    result = api._get_account_ids()
    assert len(result) == 2


def test_get_account_ids_api_error(api, response):
    response.get(
        'https://smartmeter.netz-noe.at/orchestration/User/GetAccountIdByBussinespartnerId',
        'data_account_id_2', status=999
    )
    with pytest.raises(NetzNoeSmartmeterPortalDataError) as excinfo:
        api._get_account_ids()
    assert str(excinfo.value) == 'Fetching account id data failed'


def test_get_metering_point(api, response):
    response.get(
        'https://smartmeter.netz-noe.at/orchestration/User/GetMeteringPointByAccountId', 'data_metering_point'
    )
    result = api._get_metering_point_by_account_id('12345678')
    assert len(result) == 1


def test_get_metering_point_api_error(api, response):
    response.get(
        'https://smartmeter.netz-noe.at/orchestration/User/GetMeteringPointByAccountId',
        'data_metering_point', status=999
    )
    with pytest.raises(NetzNoeSmartmeterPortalDataError):
        api._get_metering_point_by_account_id('12345678')
