import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulator.charger_queue import ChargerQueue
from simulator.engine import run_day
from simulator.policies import POLICIES


def test_mini_case_all_release():
    base_dir = Path(__file__).resolve().parents[1]
    expected_file = base_dir / "data" / "starter" / "mini_case_expected.json"
    if not expected_file.exists():
        expected_file = base_dir / "data" / "mini_case_expected.json"

    with open(expected_file, "r") as f:
        expected = json.load(f)["all_release"]

    policy = POLICIES["P0"]
    requests = [
        {"driver_id": "A", "arrival": 0, "departure": 4, "requested_kwh": 6.0},
        {"driver_id": "B", "arrival": 0, "departure": 5, "requested_kwh": 3.0},
        {"driver_id": "C", "arrival": 1, "departure": 6, "requested_kwh": 6.0},
    ]
    drivers = {
        "A": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
        "B": {"type": "Urgent", "v": 3, "w": 3, "h": 1, "rule": "Release"},
        "C": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
    }
    state = {"queue": ChargerQueue(1), "last_visits": {}, "n_chargers": 1}
    visits, _ = run_day(requests, drivers, policy, state, day_slots=6)
    by_driver = {v["driver_id"]: v for v in visits}

    for did in ["A", "B", "C"]:
        v = by_driver[did]
        e = expected[did]
        assert v["start"] == e["start"]
        assert v["finish"] == e["finish"]
        assert v["release"] == e["release"]
        assert v["wait_slots"] == e["wait_slots"]
        assert v["utility_after"] == e["utility"]

    assert sum(v["wait_slots"] for v in visits) == expected["total_wait_slots"]
    assert sum(v["energy_kwh"] for v in visits) == expected["delivered_kwh"]
    assert sum(v["utility_after"] for v in visits) == expected["total_utility"]


def test_mini_case_a_holds_one_slot():
    base_dir = Path(__file__).resolve().parents[1]
    expected_file = base_dir / "data" / "starter" / "mini_case_expected.json"
    if not expected_file.exists():
        expected_file = base_dir / "data" / "mini_case_expected.json"

    with open(expected_file, "r") as f:
        expected = json.load(f)["A_holds_one_slot"]

    policy = POLICIES["P0"]
    requests = [
        {"driver_id": "A", "arrival": 0, "departure": 4, "requested_kwh": 6.0},
        {"driver_id": "B", "arrival": 0, "departure": 5, "requested_kwh": 3.0},
        {"driver_id": "C", "arrival": 1, "departure": 6, "requested_kwh": 6.0},
    ]
    drivers = {
        "A": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Hold 1"},
        "B": {"type": "Urgent", "v": 3, "w": 3, "h": 1, "rule": "Release"},
        "C": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
    }
    state = {"queue": ChargerQueue(1), "last_visits": {}, "n_chargers": 1}
    visits, _ = run_day(requests, drivers, policy, state, day_slots=6)
    by_driver = {v["driver_id"]: v for v in visits}

    for did in ["A", "B", "C"]:
        v = by_driver[did]
        e = expected[did]
        assert v["start"] == e["start"]
        assert v["finish"] == e["finish"]
        assert v["release"] == e["release"]
        assert v["wait_slots"] == e["wait_slots"]
        assert v["utility_after"] == e["utility"]

    assert sum(v["wait_slots"] for v in visits) == expected["total_wait_slots"]
    assert sum(v["energy_kwh"] for v in visits) == expected["delivered_kwh"]
    assert sum(v["utility_after"] for v in visits) == expected["total_utility"]
