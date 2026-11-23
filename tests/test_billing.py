import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from billing import calculate_bill, bill_after_solar


def test_protected_100_units():
    # 50 x 5 + 50 x 10 = 250 + 500 = 750
    bill = calculate_bill(100)
    assert bill["protected"] is True
    assert bill["energy_charge_pkr"] == 750
    assert sum(s["units"] for s in bill["breakdown"]) == 100


def test_protected_200_units():
    # 50 x 5 + 50 x 10 + 100 x 15 = 250 + 500 + 1500 = 2250
    bill = calculate_bill(200)
    assert bill["energy_charge_pkr"] == 2250


def test_non_protected_600_units():
    # 100x10 + 100x15 + 100x20 + 100x25 + 100x30 + 100x35 = 13500
    bill = calculate_bill(600)
    assert bill["protected"] is False
    assert bill["energy_charge_pkr"] == 13500
    assert sum(s["units"] for s in bill["breakdown"]) == 600


def test_zero_units():
    assert calculate_bill(0)["energy_charge_pkr"] == 0


def test_negative_units_raises():
    try:
        calculate_bill(-10)
    except ValueError:
        return
    raise AssertionError("Expected ValueError for negative units")


def test_bill_after_solar():
    result = bill_after_solar(600, 600)
    assert result["net_units"] == 0
    assert result["bill_after_pkr"] == 0
    assert result["saving_pkr"] == 13500
