"""Pakistan Rooftop Solar Sizing - core sizing (estimate, not 100% accurate).

Formulas:
  annual generation per kWp = PSH * 365 * PR   (IEC 61724-1, PR 0.75-0.85)
  Lahore PSH = 4.93 h/day, PR = 0.78  -> ~1,404 kWh/kWp/year
  Panels are rounded UP, so installed kWp is panels * panel wattage.
"""
import math

PSH_LAHORE = 4.93
PR_DEFAULT = 0.78
PANEL_WATT_DEFAULT = 585


def annual_generation_per_kwp(psh=PSH_LAHORE, pr=PR_DEFAULT):
    return psh * 365 * pr


def size_system(monthly_units, psh=PSH_LAHORE, pr=PR_DEFAULT,
                panel_watt=PANEL_WATT_DEFAULT):
    """Size a system from monthly bill units. Returns a dict."""
    annual_units = monthly_units * 12
    gen_per_kwp = annual_generation_per_kwp(psh, pr)
    required_kwp = annual_units / gen_per_kwp
    panels = math.ceil(required_kwp * 1000 / panel_watt)
    installed_kwp = panels * panel_watt / 1000
    annual_generation = installed_kwp * gen_per_kwp
    return {
        "monthly_units": monthly_units,
        "annual_units": annual_units,
        "required_kwp": round(required_kwp, 2),
        "panels": panels,
        "panel_watt": panel_watt,
        "installed_kwp": round(installed_kwp, 2),
        "annual_generation_kwh": round(annual_generation),
    }


def is_protected(monthly_units):
    """Protected consumer boundary: 200 units/month or less."""
    return monthly_units <= 200


if __name__ == "__main__":
    result = size_system(600)
    print("Lahore 600 units/month:")
    print(f"  Panels: {result['panels']} x {result['panel_watt']}W")
    print(f"  Installed: {result['installed_kwp']} kWp")
    print(f"  Annual generation: {result['annual_generation_kwh']} kWh/year")
    print(f"  Protected (<=200 units)? {is_protected(600)}")
    print(f"  Protected (200 units)? {is_protected(200)}")
