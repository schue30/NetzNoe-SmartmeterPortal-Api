import csv
import logging
from dataclasses import fields
from datetime import date, datetime
from pathlib import Path
from typing import Union

from pendulum import DateTime, Date, period, instance

from netznoe_smartmeter_portal_api import NetzNoeSmartmeterPortalApi, SmartmeterResult, SmartmeterResultYearly

logging.basicConfig(format='%(asctime)s [%(levelname)6s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
LOGGER = logging.getLogger('main')


def native_datetime_to_pendulum(timestamp: Union[date, datetime]) -> Union[Date, DateTime]:
    if isinstance(timestamp, date):
        return Date(timestamp.year, timestamp.month, timestamp.day)
    elif isinstance(timestamp, datetime):
        return instance(timestamp)
    else:
        raise ValueError('Unknown timestamp type passed in')


def save_as_csv(output_path: Path, filename_prefix: str,
                api_data: Union[SmartmeterResult, SmartmeterResultYearly]) -> None:
    if not output_path.exists():
        output_path.mkdir(parents=True)
    for field in fields(api_data):
        values = getattr(api_data, field.name)
        if len(values) > 0:
            with Path(output_path / f'{filename_prefix}_{field.name}.csv').open('w') as fp:
                writer = csv.DictWriter(fp, extrasaction='ignore', fieldnames=['date', 'time', 'value'])
                writer.writeheader()
                for timestamp, value in values.items():
                    timestamp = native_datetime_to_pendulum(timestamp)  # <--
                    writer.writerow({
                        'date': timestamp.format('DD.MM.YYYY'),
                        'time': timestamp.format('HH:mm:ss') if isinstance(timestamp, DateTime) else '',
                        'value': value
                    })


if __name__ == '__main__':
    csv_output_dir = Path('../output')
    csv_output_dir_daily = csv_output_dir / 'daily'
    csv_output_dir_monthly = csv_output_dir / 'monthly'
    csv_output_dir_daily.mkdir(parents=True, exist_ok=True)
    csv_output_dir_monthly.mkdir(parents=True, exist_ok=True)

    meter_id = 'AT0020000000000000000000020xxxxxx'
    api = NetzNoeSmartmeterPortalApi(username='username', password='password')
    api.do_login()

    # ---
    # API Methods:

    # returns all metering points (meter_ids) of the user
    metering_points = api.get_metering_points()
    # meter_id = metering_points[0].metering_point_id  # get meter_id dynamically via API

    # returns monthly aggregated data
    yearly_values = api.get_year(meter_id, year=2023)

    # returns daily aggregated data for the requested month
    monthly_values = api.get_month(meter_id, year=2023, month=3)

    # returns daily aggregated data for the requested time range
    weekly_values = api.get_week(meter_id, start_date=Date(2023, 1, 2), end_date=Date(2023, 1, 8))

    # returns 15min values of the requested day
    daily_values = api.get_day(meter_id, day=Date(2023, 4, 1))

    # ---
    # Usage examples:

    # fetch daily aggregated values from 1.1.2023 till 1.3.2023 and save them as csv
    for start_day in period(start=DateTime(2023, 1, 1), end=DateTime(2023, 3, 1)).range('months'):
        LOGGER.info(f'Fetching month {start_day.format("MM.YYYY")}')
        save_as_csv(
            output_path=csv_output_dir_monthly, filename_prefix=start_day.format('YYYY-MM'),
            api_data=api.get_month(meter_id, year=start_day.year, month=start_day.month)
        )

    # fetch 15min values of the days from 1.2.2023 till 1.3.2023 and save them as csv
    for day in period(start=DateTime(2023, 1, 1), end=DateTime(2023, 3, 1)).range('days'):
        LOGGER.info(f'Fetching day {day.format("DD.MM.YYYY")}')
        save_as_csv(
            output_path=csv_output_dir_daily, filename_prefix=day.format('YYYY-MM-DD'),
            api_data=api.get_day(meter_id, day)
        )

    # logout of the api
    api.do_logout()
