from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import List, Union, Tuple


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
    metered: List[Tuple[Union[date, datetime], float]]

    # Description: Ersatzwert
    #   Production: Einspeisung Ersatzwert
    #   Consumption: Verbrauch Ersatzwert
    # Unit: kWh
    # API: estimatedValues
    estimated: List[Tuple[Union[date, datetime], float]]

    # Description:
    # Unit:
    # API: estimatedQualities
    estimated_qualities: List[Tuple[Union[date, datetime], SmartmeterDataQuality]]

    # Description:
    #   Production: Gemeinschaftsüberschuss
    #   Consumption: Restnetzbezug
    # Unit: kWh
    # API: gridUsageLeftoverValues
    grid_usage_leftover: List[Tuple[Union[date, datetime], float]]

    # Description:
    # Unit:
    # API: qualityEC
    quality_ec: List[Tuple[Union[date, datetime], SmartmeterDataQuality]]

    # Description:
    #   Production: Eigendeckung Teilnehmer
    #   Consumption: Eigendeckung
    #   Ren. Energy: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageValues
    self_coverage: List[Tuple[Union[date, datetime], float]]

    # Description: Ideeller Anteil
    # Unit: kWh
    # API: jointTenancyProportionValues
    joint_tenancy_proportion: List[Tuple[Union[date, datetime], float]]

    # Description: Leistung gemessen
    # Unit: kW
    # API: meteredPeakDemands
    metered_peak_demands: List[Tuple[datetime, float]]

    # Description: Leistung Ersatzwert
    # Unit: kW
    # API: estimatedPeakDemands
    estimated_peak_demands: List[Tuple[datetime, float]]

    # Description:
    # Unit:
    # API: peakDemandDataQualities
    peak_demand_data_qualities: List[Tuple[Union[date, datetime], SmartmeterDataQuality]]

    # Description: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageRenewableEnergyValue
    self_coverage_renewable_energy: List[Tuple[Union[date, datetime], float]]

    # Description: Blindverbrauch
    # Unit: kvarh
    # API: blindConsumptionValue
    blind_consumption: List[Tuple[Union[date, datetime], float]]

    # Description: Blindeinspeisung
    # Unit: kvarh
    # API: blindPowerFeedValue
    blind_power_feed: List[Tuple[Union[date, datetime], float]]

    # other API fields:
    #   ec_id, peakDemandTimes


@dataclass
class SmartmeterResultYearly:
    # Description:
    #   Production: Einspeisung
    #   Consumption: Verbrauch
    # Unit: kWh
    # API: values
    values: List[Tuple[date, float]]

    # Description:
    #   Production: Gemeinschaftsüberschuss
    #   Consumption: Restnetzbezug
    # Unit: kWh
    # API: gridUsageLeftoverValues
    grid_usage_leftover: List[Tuple[date, float]]

    # Description: Blindverbrauch
    # Unit: kvarh
    # API: blindConsumptionValue
    blind_consumption: List[Tuple[date, float]]

    # Description: Blindeinspeisung
    # Unit: kvarh
    # API: blindPowerFeedValue
    blind_power_feed: List[Tuple[date, float]]

    # Description:
    #   Production: Eigendeckung Teilnehmer
    #   Consumption: Eigendeckung
    #   Ren. Energy: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageValues
    self_coverage: List[Tuple[date, float]]

    # Description: Ideeller Anteil
    # Unit: kWh
    # API: jointTenancyProportionValues
    joint_tenancy_proportion: List[Tuple[date, float]]

    # Description:
    # Unit: kW
    # API: peakDemands
    peak_demands: List[Tuple[datetime, float]]

    # Description: Eigendeckung erneuerbare Energie
    # Unit: kWh
    # API: selfCoverageRenewableEnergyValue
    self_coverage_renewable_energy: List[Tuple[date, float]]

    # other API fields:
    #   ec_id, peakDemandTimes, isMixed
