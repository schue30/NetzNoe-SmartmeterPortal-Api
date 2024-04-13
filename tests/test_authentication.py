import pytest

from netznoe_smartmeter_portal_api.api import NetzNoeSmartmeterPortalAuthError


def test_login(api, response):
    response.post('https://smartmeter.netz-noe.at/orchestration/Authentication/Login', 'data_login')
    api.do_login()


def test_login_backend_error(api, response):
    response.post('https://smartmeter.netz-noe.at/orchestration/Authentication/Login', 'data_login', status=999)

    with pytest.raises(NetzNoeSmartmeterPortalAuthError) as excinfo:
        api.do_login()
    assert str(excinfo.value) == 'Login to Smartmeter-Portal failed'


def test_logout(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/Authentication/Logout', 'data_logout')
    api.do_logout()


def test_logout_backend_error(api, response):
    response.get('https://smartmeter.netz-noe.at/orchestration/Authentication/Logout', 'data_logout', status=999)

    with pytest.raises(NetzNoeSmartmeterPortalAuthError) as excinfo:
        api.do_logout()
    assert str(excinfo.value) == 'Logout of Smartmeter-Portal failed'
