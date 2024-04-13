# NetzNÖ Smartmeter Portal API

This project is an unofficial implementation of the NetzNÖ Smartmeter Portal API (https://smartmeter.netz-noe.at/).
It cleans up any null values from the API response and maps it to usable Python objects.

Supports: **Python 3.9+**

## Installation

```bash
pip3 install netznoe-smartmeter-portal-api
```

## Usage example

```python
from pendulum import Date

from netznoe_smartmeter_portal_api import NetzNoeSmartmeterPortalApi

meter_id = 'AT0020000000000000000000020xxxxxx'
api = NetzNoeSmartmeterPortalApi(username='username', password='password')
api.do_login()

# ---
# API Methods:

# returns monthly aggregated data
yearly_values = api.get_year(meter_id, 2023)
# SmartmeterResultYearly(
#   values={
#     datetime.date(2023, 1, 1): 100.001,
#     ...
#   },
#   peak_demands={
#     datetime.datetime(2023, 2, 18, 17, 15, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Vienna')): 2.101, 
#     ...
#   },
#   self_coverage={},
#   self_coverage_renewable_energy={},
#   grid_usage_leftover={},
#   joint_tenancy_proportion={}
#   blind_consumption={},
#   blind_power_feed={},
# )

# returns daily aggregated data for the requested month
monthly_values = api.get_month(meter_id, 2023, 3)
# SmartmeterResult(
#   metered={
#     datetime.date(2023, 3, 1): 1.810, 
#     ...
#   },
#   metered_peak_demands={
#     datetime.datetime(2023, 3, 1, 22, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Vienna')): 0.012,
#     ...
#   },
#   peak_demand_data_qualities={
#     datetime.datetime(2023, 3, 1, 22, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Vienna')): SmartmeterDataQuality.L1,
#   },
#   estimated={},
#   estimated_qualities={},
#   estimated_peak_demands={},
#   self_coverage={}, 
#   self_coverage_renewable_energy={}, 
#   grid_usage_leftover={},
#   joint_tenancy_proportion={}, 
#   quality_ec={},
#   blind_consumption={},
#   blind_power_feed={}
# )

# returns daily aggregated data for the requested time range
weekly_values = api.get_week(meter_id, start_date=Date(2023, 1, 2), end_date=Date(2023, 1, 8))

# returns 15min values of the requested day
daily_values = api.get_day(meter_id, day=Date(2023, 4, 1))

# logout of the api
api.do_logout()
```

## Mapping between API fields and model fields

For easier usage and more meaningful naming of the fields provided by the NetzNÖ Smartmeter Portal API they have been
renamed in the implemented Python models.

For description, unit and field mapping see comments in file `src/netznoe_smartmeter_portal_api/models.py`.

## Legal

Disclaimer: This is not affiliated, endorsed or certified by Netz NÖ. This is an independent and unofficial API.
Provided as is. Use at your own risk.