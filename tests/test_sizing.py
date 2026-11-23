import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sizing import size_system, is_protected, size_system_for_city, city_comparison


def test_lahore_600_units():
    r = size_system(600)
    assert r["panels"] == 9
    assert r["installed_kwp"] == 5.26  # 9 x 585W = 5.265 kWp, rounded to 2dp
    assert 7300 <= r["annual_generation_kwh"] <= 7450


def test_protected_boundary():
    assert is_protected(200) is True
    assert is_protected(201) is False
    assert is_protected(100) is True


def test_karachi_600_units_needs_fewer_panels_than_lahore():
    # Karachi PSH 5.66 > Lahore 4.93, so same 600 units need fewer panels.
    r = size_system_for_city(600, "Karachi")
    assert r["city"] == "Karachi"
    assert r["panels"] == 8
    assert r["installed_kwp"] == 4.68  # 8 x 585W
    assert 7450 <= r["annual_generation_kwh"] <= 7600


def test_quetta_600_units_sunniest():
    r = size_system_for_city(600, "Quetta")
    assert r["panels"] == 8
    assert 7950 <= r["annual_generation_kwh"] <= 8100


def test_islamabad_600_units_same_as_lahore():
    # Islamabad PSH 4.96 is close to Lahore 4.93, so panel count matches.
    r = size_system_for_city(600, "Islamabad")
    assert r["panels"] == 9
    assert r["installed_kwp"] == 5.26


def test_unknown_city_raises():
    try:
        size_system_for_city(600, "Paris")
    except ValueError:
        return
    raise AssertionError("Expected ValueError for unknown city")


def test_city_comparison_sunniest_first():
    rows = city_comparison(600)
    assert rows[0]["city"] == "Quetta"
    assert rows[-1]["city"] == "Faisalabad"
    assert len(rows) == 9
