from src.no_bid_investment_analysis import CASES, HVACS, ROOFS, hvac_tco, solar_case, optimized_solar

def test_lifecycle_sensitivity():
    assert hvac_tco(HVACS[0], CASES[2])["discounted_15y_tco_inr"] > hvac_tco(HVACS[0], CASES[0])["discounted_15y_tco_inr"]

def test_zero_pv():
    result = solar_case(HVACS[0], ROOFS[0], CASES[1], 0)
    assert result["npv_25y_inr"] == 0
    assert result["pv_generation_kwh"] == 0

def test_optimized_capacity():
    result = optimized_solar(HVACS[0], ROOFS[1], CASES[1])
    assert 0 <= result["capacity_kw"] <= ROOFS[1][1]
    assert result["npv_25y_inr"] >= 0
