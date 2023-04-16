# NetzNÖ Smartmeter Portal API

This project is an unofficial implementation of the NetzNÖ Smartmeter Portal API (https://smartmeter.netz-noe.at/).
It cleans up any null values from the API response and maps it to usable Python objects.

Supports: **Python 3.7+**

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
#   consumption={
#     Date(2023, 1, 1): 100.001,
#     ...
#   },
#   grid_usage_leftover={},
#   self_coverage={},
#   self_coverage_renewable_energy={},
#   joint_tenancy_proportion={},
#   peak_demands={
#     DateTime(2023, 2, 18, 17, 15, 0, tzinfo=Timezone('Europe/Vienna')): 2.101, 
#     ...
#   }
# )

# returns daily aggregated data for the requested month
monthly_values = api.get_month(meter_id, 2023, 3)
# SmartmeterResult(
#   consumption_metered={
#     Date(2023, 3, 1): 1.810, 
#     ...
#   },
#   consumption_estimated={}, 
#   grid_usage_leftover={}, 
#   self_coverage={}, 
#   self_coverage_renewable_energy={}, 
#   joint_tenancy_proportion={}, 
#   peak_demands_metered={
#     DateTime(2023, 3, 1, 22, 0, 0, tzinfo=Timezone('Europe/Vienna')): 0.012,
#     ...
#   },
#   peak_demands_estimated={}
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

### Python model "SmartmeterResult" (used by get_day(), get_week(), get_month()):

| API field                        | Python model field             | Unit |
|----------------------------------|--------------------------------|------|
| meteredValues                    | consumption_metered            | kWh  |
| estimatedValues                  | consumption_estimated          | kWh  |
| gridUsageLeftoverValues          | grid_usage_leftover            | kWh  |
| selfCoverageValues               | self_coverage                  | kWh  |
| selfCoverageRenewableEnergyValue | self_coverage_renewable_energy | kWh  |
| jointTenancyProportionValues     | joint_tenancy_proportion       | kWh  |
| meteredPeakDemands               | peak_demands_metered           | kW   |
| estimatedPeakDemands             | peak_demands_estimated         | kW   |

### Python model "SmartmeterResultYearly" (used by get_year()):

| API field                        | Python model field             | Unit |
|----------------------------------|--------------------------------|------|
| values                           | consumption                    | kWh  |
| gridUsageLeftoverValues          | grid_usage_leftover            | kWh  |
| selfCoverageValues               | self_coverage                  | kWh  |
| selfCoverageRenewableEnergyValue | self_coverage_renewable_energy | kWh  |
| jointTenancyProportionValues     | joint_tenancy_proportion       | kWh  |
| peakDemands                      | peak_demands                   | kW   |
| is_mixed                         | *< ignored >*                  |      |
