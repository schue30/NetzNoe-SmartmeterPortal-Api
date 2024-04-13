from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Union


@dataclass
class SmartmeterEnergyCommunity:
    id: str
    name: str


@dataclass
class SmartmeterMeteringPoint:
    account_id: str
    metering_point_id: str
    type_of_relation: str
    energy_communities: List[SmartmeterEnergyCommunity]


class SmartmeterDataQuality(str, Enum):
    L1 = "L1"  # G: Der Verbrauch/die Einspeisung wurde gemessen.
    L2 = "L2"  # E: Belastbarer Ersatzwert. Wird gebildet, wenn die Auslesung nicht möglich ist.
    L3 = "L3"  # F: Nicht belastbarer Ersatzwert. Im Unterschied zum belastbaren Ersatzwert wird dieser
    #               Verbrauch/diese Einspeisung nicht für die Verrechnung verwendet.


@dataclass
class SmartmeterResult:
    # Description:
    #   Production: Einspeisung gemessen
    #   Consumption: Verbrauch gemessen
    # Unit: kWh
    # API: meteredValues
    metered: Dict[Union[date, datetime], float]

    # Description: Ersatzwert
    #   Production: Einspeisung Ersatzwert
    #   Consumption: Verbrauch Ersatzwert
    # Unit: kWh
    # API: estimatedValues
    estimated: Dict[Union[date, datetime], float]

    # Description:
    # Unit:
    # API: estimatedQualities
    estimated_qualities: Dict[Union[date, datetime], SmartmeterDataQuality]

    # Description:
    #   Production: Gemeinschaftsüberschuss
    #   Consumption: Restnetzbezug
    # Unit: kWh
    # API: gridUsageLeftoverValues
    grid_usage_leftover: Dict[Union[date, datetime], float]

    # Description:
    # Unit:
    # API: qualityEC
    quality_ec: Dict[Union[date, datetime], SmartmeterDataQuality]

    # Description:
    #   Production: Eigendeckung Teilnehmer
    #   Consumption: Eigendeckung (kWh)
    #   Ren. Energy: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageValues
    self_coverage: Dict[Union[date, datetime], float]

    # Description: Ideeller Anteil
    # Unit: kWh
    # API: jointTenancyProportionValues
    joint_tenancy_proportion: Dict[Union[date, datetime], float]

    # Description: Leistung gemessen
    # Unit: kW
    # API: meteredPeakDemands
    metered_peak_demands: Dict[datetime, float]

    # Description: Leistung Ersatzwert
    # Unit: kW
    # API: estimatedPeakDemands
    estimated_peak_demands: Dict[datetime, float]

    # Description:
    # Unit:
    # API: peakDemandDataQualities
    peak_demand_data_qualities: Dict[Union[date, datetime], SmartmeterDataQuality]

    # Description: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageRenewableEnergyValue
    self_coverage_renewable_energy: Dict[Union[date, datetime], float]

    # Description: Blindverbrauch
    # Unit: kvarh
    # API: blindConsumptionValue
    blind_consumption: Dict[Union[date, datetime], float]

    # Description: Blindeinspeisung
    # Unit: kvarh
    # API: blindPowerFeedValue
    blind_power_feed: Dict[Union[date, datetime], float]

    # other API fields:
    #   ec_id, peakDemandTimes

    # deprecated: implemented for backward compatibility
    @property
    def consumption_metered(self) -> Dict[Union[date, datetime], float]:  # pragma: no cover
        return self.metered

    # deprecated: implemented for backward compatibility
    @property
    def consumption_estimated(self) -> Dict[Union[date, datetime], float]:  # pragma: no cover
        return self.estimated

    # deprecated: implemented for backward compatibility
    @property
    def peak_demands_metered(self) -> Dict[datetime, float]:  # pragma: no cover
        return self.metered_peak_demands

    # deprecated: implemented for backward compatibility
    @property
    def peak_demands_estimated(self) -> Dict[datetime, float]:  # pragma: no cover
        return self.estimated_peak_demands


@dataclass
class SmartmeterResultYearly:
    # Description:
    #   Production: Einspeisung
    #   Consumption: Verbrauch
    # Unit: kWh
    # API: values
    values: Dict[date, float]

    # Description:
    #   Production: Gemeinschaftsüberschuss
    #   Consumption: Restnetzbezug
    # Unit: kWh
    # API: gridUsageLeftoverValues
    grid_usage_leftover: Dict[date, float]

    # Description: Blindverbrauch
    # Unit: kvarh
    # API: blindConsumptionValue
    blind_consumption: Dict[date, float]

    # Description: Blindeinspeisung
    # Unit: kvarh
    # API: blindPowerFeedValue
    blind_power_feed: Dict[date, float]

    # Description:
    #   Production: Eigendeckung Teilnehmer
    #   Consumption: Eigendeckung (kWh)
    #   Ren. Energy: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageValues
    self_coverage: Dict[date, float]

    # Description: Ideeller Anteil
    # Unit: kWh
    # API: jointTenancyProportionValues
    joint_tenancy_proportion: Dict[date, float]

    # Description:
    # Unit: kW
    # API: peakDemands
    peak_demands: Dict[datetime, float]

    # Description: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageRenewableEnergyValue
    self_coverage_renewable_energy: Dict[date, float]

    # other API fields:
    #   ec_id, peakDemandTimes, isMixed

    # deprecated: implemented for backward compatibility
    @property
    def consumption(self) -> Dict[date, float]:  # pragma: no cover
        return self.values
