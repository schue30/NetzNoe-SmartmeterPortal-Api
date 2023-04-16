from dataclasses import dataclass
from typing import Dict, Union

from pendulum import Date, DateTime


@dataclass
class SmartmeterResult:
    consumption_metered: Dict[Union[Date, DateTime], float]
    consumption_estimated: Dict[Union[Date, DateTime], float]
    grid_usage_leftover: Dict[Union[Date, DateTime], float]
    self_coverage: Dict[Union[Date, DateTime], float]
    self_coverage_renewable_energy: Dict[Union[Date, DateTime], float]
    joint_tenancy_proportion: Dict[Union[Date, DateTime], float]
    peak_demands_metered: Dict[Union[Date, DateTime], float]
    peak_demands_estimated: Dict[Union[Date, DateTime], float]


@dataclass
class SmartmeterResultYearly:
    consumption: Dict[Union[Date, DateTime], float]
    grid_usage_leftover: Dict[Union[Date, DateTime], float]
    self_coverage: Dict[Union[Date, DateTime], float]
    self_coverage_renewable_energy: Dict[Union[Date, DateTime], float]
    joint_tenancy_proportion: Dict[Union[Date, DateTime], float]
    peak_demands: Dict[Union[Date, DateTime], float]
