import logging
from typing import Dict, Union

from pendulum import Date, DateTime, from_format
from pendulum.tz.timezone import Timezone
from requests import Session

from .models import SmartmeterResult, SmartmeterResultYearly

LOGGER = logging.getLogger('NetzNoeSmartmeterPortalApi')


class NetzNoeSmartmeterPortalApi:
    __user_agent = 'fetched by https://github.com/schue30/NetzNoe-SmartmeterPortal-Api'
    __domain = 'https://smartmeter.netz-noe.at'
    __session = None

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password

    def do_login(self):
        self.__session = Session()
        self.__session.headers.update({'User-Agent': self.__user_agent})
        resp = self.__session.post(f'{self.__domain}/orchestration/Authentication/Login',
                                   json={'user': self.__username, 'pwd': self.__password})
        assert resp.status_code == 200, 'Login to Smartmeter-Portal failed'

    def do_logout(self):
        resp = self.__session.get(f'{self.__domain}/orchestration/Authentication/Logout')
        assert resp.status_code == 200, 'Logout of Smartmeter-Portal failed'

    def get_day(self, meter_id: str, day: Date) -> SmartmeterResult:
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Day',
                                  params={'meterId': meter_id, 'day': day.format('YYYY-M-D')})
        assert resp.status_code == 200, 'Fetching daily data failed'

        base_time = DateTime(day.year, day.month, day.day, 0, 15, tzinfo=Timezone('Europe/Vienna'))
        return self.__to_smartmeter_result(base_time, resp.json(), time_increase={'minutes': 15})

    def get_week(self, meter_id: str, start_date: Date, end_date: Date) -> SmartmeterResult:
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Week',
                                  params={'meterId': meter_id, 'startDate': start_date.format('YYYY-M-D'),
                                          'endDate': end_date.format('YYYY-M-D')})
        assert resp.status_code == 200, 'Fetching weekly data failed'

        base_time = Date(start_date.year, start_date.month, start_date.day)
        return self.__to_smartmeter_result(base_time, resp.json(), time_increase={'days': 1})

    def get_month(self, meter_id: str, year: int, month: int) -> SmartmeterResult:
        if not 2000 <= year <= 2999 or not 1 <= month <= 12:
            raise ValueError('year or month not in valid range')
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Month',
                                  params={'meterId': meter_id, 'year': year, 'month': month})
        assert resp.status_code == 200, 'Fetching monthly data failed'

        base_time = Date(year, month, 1)
        return self.__to_smartmeter_result(base_time, resp.json(), time_increase={'days': 1})

    def get_year(self, meter_id: str, year: int) -> SmartmeterResultYearly:
        if not 2000 <= year <= 2999:
            raise ValueError('year not in valid range')
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Year',
                                  params={'meterId': meter_id, 'year': year})
        assert resp.status_code == 200, 'Fetching yearly data failed'

        base_time = Date(year, 1, 1)
        return self.__to_smartmeter_result_yearly(base_time, resp.json(), time_increase={'months': 1})

    def __get_values(self, resp_data: dict, field: str, base_time: Union[Date, DateTime],
                     time_increase: Dict[str, int]) -> Dict[Union[Date, DateTime], float]:
        results = {}
        for value in resp_data.get(field, []):
            if value is not None:
                results[base_time] = value
            base_time = base_time.add(**time_increase)
        return results

    def __process_peak_demand(self, resp_data: dict, field: str) -> Dict[Date, float]:
        date_format = 'YYYY-MM-DDTHH:mm:ss'
        result = {}
        for cnt, value in enumerate(resp_data.get(field, [])):
            if value is not None:
                timestamp = from_format(resp_data.get('peakDemandTimes')[cnt], date_format, tz='Europe/Vienna')
                result[timestamp] = value
        return result

    def __to_smartmeter_result(self, base_time: Union[Date, DateTime], resp_data: dict, time_increase: dict):
        return SmartmeterResult(
            consumption_metered=self.__get_values(resp_data, 'meteredValues', base_time, time_increase),
            consumption_estimated=self.__get_values(resp_data, 'estimatedValues', base_time, time_increase),
            grid_usage_leftover=self.__get_values(resp_data, 'gridUsageLeftoverValues', base_time, time_increase),
            self_coverage=self.__get_values(resp_data, 'selfCoverageValues', base_time, time_increase),
            self_coverage_renewable_energy=self.__get_values(resp_data, 'selfCoverageRenewableEnergyValue', base_time,
                                                             time_increase),
            joint_tenancy_proportion=self.__get_values(resp_data, 'jointTenancyProportionValues', base_time,
                                                       time_increase),
            peak_demands_metered=self.__process_peak_demand(resp_data, 'meteredPeakDemands'),
            peak_demands_estimated=self.__process_peak_demand(resp_data, 'estimatedPeakDemands')
        )

    def __to_smartmeter_result_yearly(self, base_time: Union[Date, DateTime], resp_data: dict, time_increase: dict):
        return SmartmeterResultYearly(
            consumption=self.__get_values(resp_data, 'values', base_time, time_increase),
            grid_usage_leftover=self.__get_values(resp_data, 'gridUsageLeftoverValues', base_time, time_increase),
            self_coverage=self.__get_values(resp_data, 'selfCoverageValues', base_time, time_increase),
            self_coverage_renewable_energy=self.__get_values(resp_data, 'selfCoverageRenewableEnergyValue', base_time,
                                                             time_increase),
            joint_tenancy_proportion=self.__get_values(resp_data, 'jointTenancyProportionValues', base_time,
                                                       time_increase),
            peak_demands=self.__process_peak_demand(resp_data, 'peakDemands'),
        )
