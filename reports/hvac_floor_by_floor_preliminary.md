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
| Third | 1,622 | 197 | Visual review of sheet p5 confirms master bedroom, drawing room and dining; approximate dimensions transcribed and require CAD check |

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

**No engineering cooling-capacity recommendation is made here.** The earlier 40 TR example is an illustrative scenario only, not a result from these drawings. A reproducible comparison using illustrative seasonal COPs and budgetary ₹/TR ranges is available in `src/hvac_comparison.py`. The previous 2,500–3,500 sq ft/floor range was also a placeholder, not a measurement.

## Next modeling milestone
Once the architect supplies room area schedules and the HVAC consultant supplies design loads, populate a complete room inventory with room sensible/latent peak kW, system allocation, cooling-season hourly profiles, and installed electrical input kW. Feed those hourly loads into the existing PV-generation workflow; do not estimate PV self-consumption solely from annual kWh.

## Updated coverage and comparison (concept only)

The third-floor sheet was visually checked: a fourth (master) bedroom, drawing room and dining room are visible. Approximate labeled dimensions have been added to the CSV. Principal-room inventory now totals **1,415 sq ft ground**, **1,622 sq ft first**, **1,622 sq ft second**, and **1,622 sq ft third**; kitchens are separately **219, 200, 200, 197 sq ft**. These are sums of selected room rectangles, **not** measured net air-conditioned floor areas; omitted foyers, dressers, halls, staff areas, etc. remain to be measured.

A provisional comparison is encoded in `src/hvac_comparison.py`: VRF seasonal COP 4.3 and ₹80k–₹150k/TR, air-cooled chiller COP 3.8 and ₹90k–₹170k/TR, ducted inverter split COP 3.3 and ₹55k–₹100k/TR. All are **unverified planning assumptions**, not Delhi supplier bids. At an *arbitrary* 40 TR, 924 equivalent full-load hours/year, and ₹9/kWh, cooling electricity is about 30,200 kWh/year (VRF), 34,200 (chiller), or 39,400 (ducted); respective budgetary installation ranges are ₹32–60 lakh, ₹36–68 lakh and ₹22–40 lakh. They exclude other building loads and do not establish actual installed TR.

**Unresolved before a complete engineered schedule:** CAD room polygons/areas and dimensions, glazing and envelope properties, ventilation, floor-specific solar exposures, occupancy, and HVAC consultant room-level sensible/latent loads. The architectural PDF cannot establish those engineering inputs, so the project must not label this an engineered equipment selection.
