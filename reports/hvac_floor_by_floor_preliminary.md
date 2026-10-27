# Preliminary floor-by-floor HVAC zone schedule

## Scope and source
Based on **Final Plan (1).pdf**, architectural sheets dated 30 March 2026: stilt p1, ground p2, first p3, second p4, third p5, terrace p6. **A11_8VV-Model (1).pdf** is a different architectural alternative and is **not merged** with the furnished room schedule. Both PDFs are private and intentionally not uploaded to this public repository.

Machine-readable room-by-room transcription: `data/hvac_room_schedule_preliminary.csv`; aggregation: `src/hvac_room_schedule.py`. Dimensions are labeled room sizes rounded to whole square feet; fractional-inch typography was imperfectly extracted and should be checked against the actual CAD drawings.

## Documented room areas — lower-bound partial inventory

| Floor | Sum of listed conditioned bedrooms/living/dining (sq ft) | Kitchen listed separately (sq ft) | Status |
|---|---:|---:|---|
| Ground | 1,415 | 219 | Four bedrooms plus combined drawing/dining; hallways, foyer, dressers, bathrooms and other zones omitted |
| First | 1,622 | 200 | Four bedrooms and separate drawing/dining; corridors, foyer and other zones omitted |
| Second | 1,622 | 200 | Repeated first-floor layout provisionally transcribed; verify all rooms against CAD |
| Third | 699 | 197 | Only three bedrooms legible in current extraction; master bedroom and drawing/dining **not counted**, so total is substantially incomplete |

These sums are **NOT total conditioned floor areas**. They should not be compared with total plot area or used to select a TR rating. Kitchens are separately flagged because whether they are actively air-conditioned, and how cooking exhaust/make-up air is handled, must be decided. Dressing rooms, foyers, halls, staff rooms, toilets, lobbies, lifts, balconies, stairs, stilt parking and basement require individual classification. Toilets and kitchens require ventilation treatment even if not cooled.

The alternative A11_8VV model labels the plot as 63 × 90 ft (5,670 sq ft); this is **plot area**, not conditioned area. The alternate drawing includes basement mechanical ventilation and should be independently assessed if selected.

## Proposed design zones
- Four family-floor zones, with room-level control for bedrooms and living/dining.
- One combined building electricity meter, **subject to BRPL acceptance**, for HVAC, lifts, pumps and all family loads.
- VRF/VRV: compare independently controlled indoor zones and modular outdoor units; obtain refrigerant safety, ventilation, piping-length and service-access design.
- Ducted inverter splits: quote separately zoned systems per floor as a competitive alternative.
- Central chiller: request a comparison only once the calculated design cooling load and central plant space are known.
- Outdoor-unit/chiller siting must be coordinated with the PV canopy, maintenance access, noise and solar shading.

## Engineering information required before sizing
1. CAD-derived **net conditioned area per room**, including all omitted circulation, dressing and study spaces, and confirm which third-floor rooms are present.
2. Envelope: window sizes, orientations, glass SHGC/U-value, shading, roof and wall assemblies, infiltration.
3. Occupancy and schedules by floor, indoor design temperatures, fresh-air quantities, kitchen exhaust and make-up air.
4. Delhi outdoor design conditions, sensible and latent loads, peak diversity, ventilation loads, duct static pressure and equipment performance at design temperatures.
5. Equipment-level whole-system seasonal COP including outdoor fans, indoor fans, pumps and controls; quotes from multiple suppliers.
6. Electrical maximum demand, power-factor and sanctioned-load review with BRPL, and hourly cooling profiles for PV economics.

**No engineering cooling-capacity recommendation is made here.** The earlier 40 TR example is an illustrative scenario only, not a result from these drawings. The previous 2,500–3,500 sq ft/floor range was also a placeholder, not a measurement.

## Next modeling milestone
Once the architect supplies room area schedules and the HVAC consultant supplies design loads, populate a complete room inventory with room sensible/latent peak kW, system allocation, cooling-season hourly profiles, and installed electrical input kW. Feed those hourly loads into the existing PV-generation workflow; do not estimate PV self-consumption solely from annual kWh.
