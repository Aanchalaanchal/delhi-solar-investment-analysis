import pytest
from src.canopy_shading import CanopyGeometry, shadow_length_m, shade_stress_factor
from src.roof_scenarios import RoofScenario, analyze_elevated_canopy
from src.financial_model import Assumptions

def test_shadow_at_45_degrees_equals_height():
    assert shadow_length_m(3,45)==pytest.approx(3)

def test_overhead_sun_zero_shadow():
    assert shadow_length_m(3,90)==0

def test_low_sun_longer_shadow():
    assert shadow_length_m(3,20)>shadow_length_m(3,60)

def test_invalid_elevation():
    with pytest.raises(ValueError):
        shadow_length_m(3,0)

def test_loss_fraction():
    assert shade_stress_factor(CanopyGeometry(shadow_interception_fraction=.5,
        affected_generation_fraction=.4,loss_when_shaded_fraction=.5))==pytest.approx(.1)

def test_panel_shading_reduces_npv_for_canopy():
    roof=RoofScenario("x","X","",80,8)
    a=Assumptions()
    unshaded=analyze_elevated_canopy(roof,a,40,.75,20000,canopy_generation_loss_fraction=0)
    shaded=analyze_elevated_canopy(roof,a,40,.75,20000,canopy_generation_loss_fraction=.2)
    assert shaded["results"][-1]["npv_inr"]<unshaded["results"][-1]["npv_inr"]
    assert shaded["results"][0]["npv_inr"]==unshaded["results"][0]["npv_inr"]

def test_invalid_shading_loss():
    with pytest.raises(ValueError):
        analyze_elevated_canopy(RoofScenario("x","X","",80),Assumptions(),40,
                                canopy_generation_loss_fraction=1.2)
