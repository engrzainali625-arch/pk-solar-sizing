"""Bill engine for pk-solar-sizing (estimate, not 100% accurate).

Rates are NOT hard-coded here. They are read from a JSON file, so the
user can replace them with verified NEPRA rates from nepra.org.pk.
The default file, data/tariffs_example.json, contains EXAMPLE rates
only — round placeholder numbers, NOT real NEPRA rates. Fixed charges,
taxes and fuel adjustments are NOT included in this calculation.
"""
import json
from pathlib import Path

from sizing import is_protected

DEFAULT_TARIFFS = Path(__file__).resolve().parents[1] / "data" / "tariffs_example.json"


def load_tariffs(path=DEFAULT_TARIFFS):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def calculate_bill(monthly_units, tariffs=None, protected=None):
    """Calculate an energy-only bill from monthly units.

    Returns a dict with the slab breakdown and the total energy charge.
    """
    if monthly_units < 0:
        raise ValueError("monthly_units cannot be negative")
    tariffs = tariffs or load_tariffs()
    if protected is None:
        protected = is_protected(monthly_units)
    category = "protected" if protected else "non_protected"
    slabs = tariffs[category]["slabs"]

    breakdown = []
    remaining = monthly_units
    prev_limit = 0
    total = 0
    for slab in slabs:
        if remaining <= 0:
            break
        limit = slab["up_to"]
        if limit is None:
            units_in_slab = remaining
        else:
            units_in_slab = min(remaining, limit - prev_limit)
        amount = units_in_slab * slab["rate"]
        breakdown.append({
            "from_unit": prev_limit + 1,
            "to_unit": limit,
            "units": units_in_slab,
            "rate_pkr_per_unit": slab["rate"],
            "amount_pkr": amount,
        })
        total += amount
        remaining -= units_in_slab
        if limit is not None:
            prev_limit = limit
    return {
        "monthly_units": monthly_units,
        "protected": protected,
        "category": category,
        "breakdown": breakdown,
        "energy_charge_pkr": total,
        "example_rates_only": True,
    }


def bill_after_solar(monthly_units, monthly_solar_kwh, tariffs=None):
    """Bill after solar, simplified: solar units offset bill units 1:1.

    Export / net-billing buyback is NOT modelled here yet.
    """
    net_units = max(0, monthly_units - monthly_solar_kwh)
    before = calculate_bill(monthly_units, tariffs=tariffs)
    after = calculate_bill(net_units, tariffs=tariffs)
    return {
        "monthly_units": monthly_units,
        "monthly_solar_kwh": monthly_solar_kwh,
        "net_units": net_units,
        "bill_before_pkr": before["energy_charge_pkr"],
        "bill_after_pkr": after["energy_charge_pkr"],
        "saving_pkr": before["energy_charge_pkr"] - after["energy_charge_pkr"],
    }


if __name__ == "__main__":
    print("EXAMPLE RATES ONLY - not NEPRA rates. See data/tariffs_example.json")
    for units in (600, 550, 620, 200, 100):
        bill = calculate_bill(units)
        print(f"{units} units ({bill['category']}): "
              f"Rs {bill['energy_charge_pkr']} energy charge")
    print()
    solar = bill_after_solar(600, 600)
    print(f"600 units, 600 kWh solar: bill Rs {solar['bill_before_pkr']} "
          f"-> Rs {solar['bill_after_pkr']}, saving Rs {solar['saving_pkr']}")
