"""Explicitly guessed design inputs for the four-family Delhi home.

These are NOT measurements, vendor bids, certified loads or BRPL approvals.
Keep guesses centralized to make them easy to replace with survey results.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class DesignGuesses:
    family_floors:int=4
    # Principal-room inventory excludes halls/dressers and other rooms.
    conditioned_area_sqft_per_floor:float=2500.0
    # 250-400 sqft/TR is a rough concept-stage range, not a heat load calculation.
    design_sqft_per_tr:float=275.0
    extra_ventilation_and_solar_margin_fraction:float=.10
    annual_cooling_equivalent_full_load_hours:float=924.0
    family_non_ac_kwh_per_year:float=12000.0
    common_kwh_per_year:float=4000.0
    # Portal's 10m²/kW area benchmark, instead of earlier optimistic 8m²/kW.
    area_per_solar_kw_m2:float=10.0
    furnished_roof_usable_m2:float=100.0
    alternate_roof_usable_m2:float=140.0
    canopy_footprint_m2:float=40.0
    canopy_coverage_fraction:float=.75
    avoided_tariff_inr_kwh:float=9.0
    # Not a forecast of future connection charges or fixed demand charges.
    provisional_sanctioned_load_kva:float=100.0

    @property
    def total_conditioned_sqft(self):
        return self.family_floors*self.conditioned_area_sqft_per_floor

    @property
    def concept_peak_tr(self):
        return self.total_conditioned_sqft/self.design_sqft_per_tr*(1+self.extra_ventilation_and_solar_margin_fraction)

    @property
    def rounded_concept_tr(self):
        return round(self.concept_peak_tr/5)*5

    @property
    def furnished_solar_kw(self):
        return self.furnished_roof_usable_m2/self.area_per_solar_kw_m2

    @property
    def alternate_solar_kw(self):
        return self.alternate_roof_usable_m2/self.area_per_solar_kw_m2

    @property
    def canopy_solar_kw(self):
        return self.canopy_footprint_m2*self.canopy_coverage_fraction/self.area_per_solar_kw_m2

DEFAULT=DesignGuesses()
