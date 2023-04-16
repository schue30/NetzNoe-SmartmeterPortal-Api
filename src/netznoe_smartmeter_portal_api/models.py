from dataclasses import dataclass
from typing import Dict, Union

from pendulum import Date, DateTime


@dataclass
class SmartmeterResult:
    consumption_metered: Dict[Union[Date, DateTime], float]  # Verbrauch gemessen in kWh
    consumption_estimated: Dict[Union[Date, DateTime], float]  # Verbrauch geschaetzt in kWh
    grid_usage_leftover: Dict[Union[Date, DateTime], float]
    self_coverage: Dict[Union[Date, DateTime], float]
    self_coverage_renewable_energy: Dict[Union[Date, DateTime], float]
    joint_tenancy_proportion: Dict[Union[Date, DateTime], float]
    peak_demands_metered: Dict[Union[Date, DateTime], float]  # Leistung gemessen in kW
    peak_demands_estimated: Dict[Union[Date, DateTime], float]  # Leistung geschaetzt in kW


@dataclass
class SmartmeterResultYearly:
    consumption: Dict[Union[Date, DateTime], float]  # Verbrauch in kWh
    grid_usage_leftover: Dict[Union[Date, DateTime], float]
    self_coverage: Dict[Union[Date, DateTime], float]
    self_coverage_renewable_energy: Dict[Union[Date, DateTime], float]
    joint_tenancy_proportion: Dict[Union[Date, DateTime], float]
    peak_demands: Dict[Union[Date, DateTime], float]  # Leistung in kW
    # is_mixed -> don't know that this does (true or false)
