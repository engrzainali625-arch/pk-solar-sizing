import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sizing import size_system, is_protected


def test_lahore_600_units():
    r = size_system(600)
    assert r["panels"] == 9
    assert r["installed_kwp"] == 5.26  # 9 x 585W = 5.265 kWp, rounded to 2dp
    assert 7300 <= r["annual_generation_kwh"] <= 7450


def test_protected_boundary():
    assert is_protected(200) is True
    assert is_protected(201) is False
    assert is_protected(100) is True
