"""Illustrative geometric canopy shading; not a solar-path or ray-tracing study.

The height-based shadow length is computed for a user-selected solar elevation.
Orientation, solar azimuth, sun position by hour, diffuse light, and nearby buildings
are NOT represented. The resulting shading factor is a stress-test assumption,
not an energy prediction.
"""
from dataclasses import dataclass
from math import radians, tan, isfinite

@dataclass(frozen=True)
class CanopyGeometry:
    clearance_m: float = 2.7
    solar_elevation_deg: float = 35.0
    shadow_interception_fraction: float = 0.35
    affected_generation_fraction: float = 0.25
    loss_when_shaded_fraction: float = 0.50

def shadow_length_m(height_m: float, solar_elevation_deg: float) -> float:
    if not isfinite(height_m) or height_m < 0 or not isfinite(solar_elevation_deg) or not 0 < solar_elevation_deg <= 90:
        raise ValueError("Height must be nonnegative and solar elevation in (0, 90]")
    return 0.0 if solar_elevation_deg == 90 else height_m / tan(radians(solar_elevation_deg))

def shade_stress_factor(g: CanopyGeometry) -> float:
    """Illustrative annual loss fraction applied only to modeled canopy production.

    Multiplying these independent user assumptions is not a physical shade model.
    """
    fractions = (g.shadow_interception_fraction, g.affected_generation_fraction,
                 g.loss_when_shaded_fraction)
    if any(not isfinite(v) or not 0 <= v <= 1 for v in fractions):
        raise ValueError("Shading fractions must be in [0, 1]")
    return fractions[0] * fractions[1] * fractions[2]

def canopy_shadow_summary(g: CanopyGeometry) -> dict:
    return {"clearance_m": g.clearance_m,
            "shadow_length_m": shadow_length_m(g.clearance_m, g.solar_elevation_deg),
            "canopy_generation_loss_fraction": shade_stress_factor(g)}
