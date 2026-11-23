# pk-solar-sizing

Pakistan Rooftop Solar Sizing & Net-Billing Payback Calculator (Python).

## What it does
From a home's monthly bill units, it sizes a rooftop solar system:
monthly units -> kWp -> panel count -> annual generation.

Worked example, Lahore, 600 units/month:
- 9 panels x 585W = 5.26 kWp installed
- About 7,390 kWh/year generation

Same 600 units/month in other cities (PSH: solarposition.org, NASA POWER):
- Quetta (6.02): 8 panels, 4.68 kWp, about 8,021 kWh/year
- Karachi (5.66): 8 panels, 4.68 kWp, about 7,541 kWh/year
- Multan / Peshawar (5.12): 9 panels, 5.26 kWp, about 7,675 kWh/year
- Islamabad (4.96): 9 panels, 5.26 kWp, about 7,435 kWh/year
- Faisalabad (4.85): 9 panels, 5.26 kWp, about 7,270 kWh/year

## Bill engine (example rates only)
`src/billing.py` calculates an energy-only bill slab by slab from
`data/tariffs_example.json`. The rates in that file are EXAMPLE placeholder
numbers, NOT NEPRA rates — replace them with verified rates from
nepra.org.pk before using it for a real bill. Fixed charges, taxes and
fuel adjustments are not included.

Example months, example rates:
- 600 units: Rs 13,500 energy charge
- 550 units: Rs 11,750 energy charge
- 620 units: Rs 14,300 energy charge
- 200 units (protected): Rs 2,250 energy charge
This is an **estimate, not 100% accurate**. Generation varies ±10-15% with
weather, shading, dust and temperature. NEPRA slab rates and the net-billing
buyback rate are NOT hard-coded here — check nepra.org.pk before publishing
any tariff number as fact. A site survey and DISCO approval are still needed
for a final design.

## Run it
```bash
python3 src/sizing.py
python3 -m pytest tests/ -q
```

## Status
Day 12, 23 Nov 2026: city-wise solar yield added — 9 cities, Karachi and
Quetta need 8 panels for 600 units/month vs 9 in Lahore. Bill engine added
with EXAMPLE rates only (no real bill was available, so no NEPRA rates are
claimed) — replace data/tariffs_example.json with verified rates before a
real bill. Next: cable check + Streamlit UI (Days 18-22).
