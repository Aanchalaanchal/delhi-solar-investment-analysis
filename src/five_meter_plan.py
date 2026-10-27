"""Proposed five-meter electrical model: four family accounts plus shared plant.

Illustrative annual allocation only. The common meter may directly consume PV
energy, but surplus credit transfer to other account holders requires BRPL approval.
"""
from dataclasses import dataclass
from src.central_ac_load import CentralAC, future_building_load

@dataclass(frozen=True)
class FiveMeterPlan:
    family_annual_kwh: tuple[float,float,float,float]
    central_ac: CentralAC
    common_other_annual_kwh: float

    def summary(self):
        loads=future_building_load(self.family_annual_kwh,self.central_ac,self.common_other_annual_kwh)
        return {
            "Family 1":self.family_annual_kwh[0],
            "Family 2":self.family_annual_kwh[1],
            "Family 3":self.family_annual_kwh[2],
            "Family 4":self.family_annual_kwh[3],
            "Common meter (central AC + lifts/pumps/lighting)":loads["central_ac_kwh"]+loads["other_common_kwh"]
        }

def solar_credit_allocation(meter_loads:dict[str,float],annual_pv_kwh:float,
                            common_meter_name="Common meter (central AC + lifts/pumps/lighting)",
                            approved_vnm=False, family_shares=(.25,.25,.25,.25)):
    """Illustrative common-meter self-use first; optional surplus sharing.

    This is NOT a BRPL settlement calculation. Annual matching overstates
    self-consumption relative to hourly demand/generation and is for sensitivity
    analysis only. VNM allocation is conditional on written BRPL approval.
    """
    if len(meter_loads)!=5 or common_meter_name not in meter_loads or any(v<0 for v in meter_loads.values()):
        raise ValueError("Expected five nonnegative meter loads")
    if annual_pv_kwh<0:
        raise ValueError("PV energy cannot be negative")
    common_used=min(meter_loads[common_meter_name],annual_pv_kwh)
    remaining=max(0.0,annual_pv_kwh-common_used)
    credited={key:0.0 for key in meter_loads}
    credited[common_meter_name]=common_used
    if approved_vnm:
        if len(family_shares)!=4 or any(x<0 for x in family_shares) or abs(sum(family_shares)-1)>1e-8:
            raise ValueError("Four nonnegative shares summing to 100% required")
        families=[k for k in meter_loads if k!=common_meter_name]
        for family,share in zip(families,family_shares):
            credited[family]=min(meter_loads[family],remaining*share)
    return {"credited_kwh_by_meter":credited,
            "total_modeled_credited_kwh":sum(credited.values()),
            "unallocated_or_unvalued_kwh":max(0.0,annual_pv_kwh-sum(credited.values())),
            "vnm_assumed_approved":approved_vnm}
