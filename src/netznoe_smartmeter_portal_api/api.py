import logging
import typing
from datetime import date, datetime, timedelta
from typing import Dict, List, Union
from zoneinfo import ZoneInfo

import itertools
from requests import Session

from .models import (
    SmartmeterDataQuality,
    SmartmeterEnergyCommunity,
    SmartmeterMeteringPoint,
    SmartmeterResult,
    SmartmeterResultYearly,
)

LOGGER = logging.getLogger('NetzNoeSmartmeterPortalApi')


class NetzNoeSmartmeterPortalAuthError(Exception):
    pass


class NetzNoeSmartmeterPortalDataError(Exception):
    pass


class NetzNoeSmartmeterPortalApi:
    __user_agent = 'fetched by https://github.com/schue30/NetzNoe-SmartmeterPortal-Api'
    __domain = 'https://smartmeter.netz-noe.at'

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        self.__session = Session()
        self.__session.headers.update({'User-Agent': self.__user_agent})

    def do_login(self):
        resp = self.__session.post(f'{self.__domain}/orchestration/Authentication/Login',
                                   json={'user': self.__username, 'pwd': self.__password})
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalAuthError('Login to Smartmeter-Portal failed')

    def do_logout(self):
        resp = self.__session.get(f'{self.__domain}/orchestration/Authentication/Logout')
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalAuthError('Logout of Smartmeter-Portal failed')

    def get_day_per_energy_community(self, meter_id: str, day: date) -> Dict[str, SmartmeterResult]:
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Day',
                                  params={'meterId': meter_id, 'day': day.strftime('%Y-%-m-%-d')})
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalDataError('Fetching daily data failed')

        base_time = datetime(day.year, day.month, day.day, hour=0, minute=15, tzinfo=ZoneInfo('Europe/Vienna'))
        return dict(map(
            lambda e: (
                e.get('ec_id') if e.get('ec_id') else 'total',
                self.__to_smartmeter_result(base_time, e, time_increase={'minutes': 15})
            ), resp.json()
        ))

    def get_day(self, meter_id: str, day: date) -> SmartmeterResult:
        return self.get_day_per_energy_community(meter_id, day)['total']

    def get_week_per_energy_community(self, meter_id: str,
                                      start_date: date, end_date: date) -> Dict[str, SmartmeterResult]:
        params: Dict[str, str] = {'meterId': meter_id, 'startDate': start_date.strftime('%Y-%-m-%-d'),
                                  'endDate': end_date.strftime('%Y-%-m-%-d')}
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Week', params=params)
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalDataError('Fetching weekly data failed')

        base_time = date(start_date.year, start_date.month, start_date.day)
        return dict(map(
            lambda e: (
                e.get('ec_id') if e.get('ec_id') else 'total',
                self.__to_smartmeter_result(base_time, e, time_increase={'days': 1})
            ), resp.json()
        ))

    def get_week(self, meter_id: str, start_date: date, end_date: date) -> SmartmeterResult:
        return self.get_week_per_energy_community(meter_id, start_date, end_date)['total']

    def get_month_per_energy_community(self, meter_id: str, year: int, month: int) -> Dict[str, SmartmeterResult]:
        if not 2000 <= year <= 2999 or not 1 <= month <= 12:
            raise ValueError('year or month not in valid range')
        params: Dict[str, Union[str, int]] = {'meterId': meter_id, 'year': year, 'month': month}
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Month', params=params)
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalDataError('Fetching monthly data failed')

        base_time = date(year, month, 1)
        return dict(map(
            lambda e: (
                e.get('ec_id') if e.get('ec_id') else 'total',
                self.__to_smartmeter_result(base_time, e, time_increase={'days': 1})
            ), resp.json()
        ))

    def get_month(self, meter_id: str, year: int, month: int) -> SmartmeterResult:
        return self.get_month_per_energy_community(meter_id, year, month)['total']

    def get_year_per_energy_community(self, meter_id: str, year: int) -> Dict[str, SmartmeterResultYearly]:
        if not 2000 <= year <= 2999:
            raise ValueError('year not in valid range')
        params: Dict[str, Union[str, int]] = {'meterId': meter_id, 'year': year}
        resp = self.__session.get(f'{self.__domain}/orchestration/ConsumptionRecord/Year', params=params)
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalDataError('Fetching yearly data failed')

        base_time = date(year, 1, 1)
        return dict(map(
            lambda e: (
                e.get('ec_id') if e.get('ec_id') else 'total',
                self.__to_smartmeter_result_yearly(base_time, e, time_increase={'months': 1})
            ), resp.json()
        ))

    def get_year(self, meter_id: str, year: int) -> SmartmeterResultYearly:
        return self.get_year_per_energy_community(meter_id, year)['total']

    def get_metering_points(self) -> List[SmartmeterMeteringPoint]:
        account_ids = self._get_account_ids()
        return list(itertools.chain.from_iterable(
            map(lambda account_id: self._get_metering_point_by_account_id(account_id), account_ids)
        ))

    def _get_account_ids(self) -> List[str]:
        params: Dict[str, int] = {'context': 2}
        resp = self.__session.get(f'{self.__domain}/orchestration/User/GetAccountIdByBussinespartnerId', params=params)
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalDataError('Fetching account id data failed')
        return list(filter(None, map(lambda account: account.get('accountId'), resp.json())))

    def _get_metering_point_by_account_id(self, account_id: str) -> List[SmartmeterMeteringPoint]:
        account_params: Dict[str, Union[str, int]] = {'accountId': account_id, 'context': 2}
        resp = self.__session.get(f'{self.__domain}/orchestration/User/GetMeteringPointByAccountId',
                                  params=account_params)
        if resp.status_code != 200:
            raise NetzNoeSmartmeterPortalDataError(
                'Fetching metering point for account id "%s" failed', account_id
            )
        return list(map(lambda meter: SmartmeterMeteringPoint(
            account_id=account_id,
            metering_point_id=meter.get('meteringPointId'),
            type_of_relation=meter.get('typeOfRelation'),
            energy_communities=list(map(lambda ec: SmartmeterEnergyCommunity(
                id=ec.get('ecid'),
                name=ec.get('name')
            ), meter.get('energyCommunities', [])))
        ), resp.json()))

    @staticmethod
    def __get_values(data: dict, field: str, base_time: Union[date, datetime],
                     time_increase: Dict[str, int]) -> Dict[Union[date, datetime], Union[float, SmartmeterDataQuality]]:
        results: Dict[Union[date, datetime], Union[float, SmartmeterDataQuality]] = {}
        for value in data.get(field, []):
            if value is not None:
                if value in ('L1', 'L2', 'L3'):
                    results[base_time] = SmartmeterDataQuality(value)
                else:
                    results[base_time] = value

            # increase base_time for next value
            if 'months' in time_increase and isinstance(base_time, date):
                if base_time.month < 12:
                    base_time = date(base_time.year, base_time.month + time_increase['months'], base_time.day)
            else:
                base_time += timedelta(**time_increase)
        return results

    @staticmethod
    def __process_peak_demand(data: dict, field: str) -> Dict[datetime, Union[float, SmartmeterDataQuality]]:
        results: Dict[datetime, Union[float, SmartmeterDataQuality]] = {}
        for cnt, value in enumerate(data.get(field, [])):
            if value is not None:
                timestamp = datetime.strptime(
                    data['peakDemandTimes'][cnt], '%Y-%m-%dT%H:%M:%S'
                ).replace(tzinfo=ZoneInfo('Europe/Vienna'))

                if value in ('L1', 'L2', 'L3'):
                    results[timestamp] = SmartmeterDataQuality(value)
                else:
                    results[timestamp] = value
        return results

    @typing.no_type_check
    def __to_smartmeter_result(self, base_time: Union[date, datetime], data: dict,
                               time_increase: dict) -> SmartmeterResult:
        return SmartmeterResult(
            metered=self.__get_values(data, 'meteredValues', base_time, time_increase),
            estimated=self.__get_values(data, 'estimatedValues', base_time, time_increase),
            estimated_qualities=self.__get_values(data, 'estimatedQualities', base_time, time_increase),
            grid_usage_leftover=self.__get_values(data, 'gridUsageLeftoverValues', base_time, time_increase),
            quality_ec=self.__get_values(data, 'qualityEC', base_time, time_increase),
            self_coverage=self.__get_values(data, 'selfCoverageValues', base_time, time_increase),
            joint_tenancy_proportion=self.__get_values(data, 'jointTenancyProportionValues', base_time, time_increase),
            metered_peak_demands=self.__process_peak_demand(data, 'meteredPeakDemands'),
            estimated_peak_demands=self.__process_peak_demand(data, 'estimatedPeakDemands'),
            peak_demand_data_qualities=self.__process_peak_demand(data, 'peakDemandDataQualities'),
            self_coverage_renewable_energy=self.__get_values(data, 'selfCoverageRenewableEnergyValue',
                                                             base_time, time_increase),
            blind_consumption=self.__get_values(data, 'blindConsumptionValue', base_time, time_increase),
            blind_power_feed=self.__get_values(data, 'blindPowerFeedValue', base_time, time_increase)
        )

    @typing.no_type_check
    def __to_smartmeter_result_yearly(self, base_time: date, data: dict, time_increase: dict) -> SmartmeterResultYearly:
        return SmartmeterResultYearly(
            values=self.__get_values(data, 'values', base_time, time_increase),
            grid_usage_leftover=self.__get_values(data, 'gridUsageLeftoverValues', base_time, time_increase),
            blind_consumption=self.__get_values(data, 'blindConsumptionValue', base_time, time_increase),
            blind_power_feed=self.__get_values(data, 'blindPowerFeedValue', base_time, time_increase),
            self_coverage=self.__get_values(data, 'selfCoverageValues', base_time, time_increase),
            joint_tenancy_proportion=self.__get_values(data, 'jointTenancyProportionValues', base_time, time_increase),
            self_coverage_renewable_energy=self.__get_values(data, 'selfCoverageRenewableEnergyValue',
                                                             base_time, time_increase),
            peak_demands=self.__process_peak_demand(data, 'peakDemands'),
        )
