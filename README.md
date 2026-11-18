# pk-solar-sizing

Pakistan Rooftop Solar Sizing & Net-Billing Payback Calculator (Python).

## What it does
From a home's monthly bill units, it sizes a rooftop solar system:
monthly units -> kWp -> panel count -> annual generation.

Worked example, Lahore, 600 units/month:
- 9 panels x 585W = 5.26 kWp installed
- About 7,390 kWh/year generation

## Honest limits
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
Day 3, 13 Nov 2026: sizing core + tests done. Next: tariff/bill engine
(Days 5-10), then cable check + Streamlit UI (Days 18-22).
