# Preliminary roof-plan comparison — illustrative only

## Design A: Final Plan (1).pdf

Source: terrace layout, page 6 of 6, dated March 30, 2026.

The drawing shows a substantial open terrace, but also a furnished lounge/seating area with kitchen counter, enclosed study, toilet, lift/stair lobby, multiple lift shafts, powder room, and staff room. These spaces are not assumed to be available for PV. The terrace is not dimensioned sufficiently in the PDF to establish a defensible net solar area without scaled CAD measurement and a roof-use decision.

**Initial model placeholder:** 100 m² usable PV area, **not measured**.

## Design B: A11_8VV-Model (1).pdf

Source: one-page building-plan sheet, terrace plan and site plan.

The terrace plan depicts a comparatively open roof, with lift/stair access, a small toilet, and parapet walls. The site plan states plot dimensions of 19.202 × 27.432 m (~526.8 m²), which **must not be used as solar roof area**. The terrace is different from Design A and cannot be assumed identical.

**Initial model placeholder:** 140 m² usable PV area, **not measured**.

## Shared modeling assumptions

- Illustrative area requirement: 8 m² per installed kW (adjustable)
- Default areas above are *scenario placeholders*, not architect-verified values
- Neither plan establishes actual roof structural capacity, final water tank/HVAC locations, electrical meter allocation, fire access, solar module layout, shading, orientation or mounting setbacks
- The financial engine still uses illustrative annual yield and retail offset assumptions, **not** verified Delhi tariffs or hourly generation

## Required before a bankable estimate

Obtain a dimensioned terrace CAD file or scaled PDF, confirm whether the furnished terrace must remain clear, survey rooftop obstructions and heights, and confirm separate/common electricity meters. Validate any derived solar array layout with a licensed installer and structural engineer.

**Privacy:** Original PDFs contain property-identifying details and are intentionally excluded from this public repository.


## Design A option: elevated canopy over part of the furnished terrace

A separate scenario models PV mounted above part of the leisure area, preserving potential activity space below. This is not part of the confirmed architectural design.

Illustrative defaults:
- Additional canopy footprint: 40 m², assumed non-overlapping with the 100 m² base usable roof
- PV coverage of canopy footprint: 75%
- Area requirement: 8 m²/kW
- Additional PV capacity ceiling: 3.75 kW
- Additional structural/mounting premium: ₹20,000 per canopy kW, unquoted
- Combined capacity ceiling: 16.25 kW (not a layout-verified or permitted capacity)

The dashboard's financial model allocates the premium only to the capacity above the base-roof ceiling. It assumes identical annual PV yield for base and canopy modules. It does not simulate canopy height, shading, airflow, solar azimuth, drainage, access, structural loading, waterproofing, wind uplift, permissions or usable clearance below. All require a design-stage assessment.

Do not add the canopy footprint to base area if the spaces overlap: that would double-count roof surface.


## Canopy height and shading sensitivity (model v0.3)

The dashboard now compares three cases: Final Plan regular rooftop PV; Final Plan rooftop PV plus elevated canopy; and A11_8VV Model regular rooftop PV.

Canopy clearance defaults to 2.7 m. The geometric shadow length is `clearance / tan(solar elevation)`, with a default illustrative sun elevation of 35°. This describes a shadow's reach **on the terrace**, not panel shading or annual energy loss. Neither the sun elevation nor the clearance is measured from the plans.

Separately, the dashboard has a user-selected annual loss on **canopy panel generation** from possible external obstructions (default 5%). The financial model applies this loss only to the capacity allocated to the canopy, not to base-roof panels. The canopy structural premium remains allocated only to canopy capacity.

This is a scenario stress test, not hourly solar-position modeling or 3D ray tracing. Shadow azimuth, module orientation, local obstacles, seasonal variations, neighboring buildings, electrical string effects, panel temperature and canopy wind uplift are not represented. In particular, shade on the occupied terrace underneath does not imply shade on panels above.

No property-identifying architectural PDFs are committed to the public repository.
