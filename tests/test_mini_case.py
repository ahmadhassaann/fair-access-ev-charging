import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulator.charger_queue import ChargerQueue
from simulator.engine import run_day
from simulator.policies import POLICIES


def test_mini_case_all_release():
    policy = POLICIES["P0"]
    requests = [
        {"driver_id": "A", "arrival": 0, "departure": 16, "requested_kwh": 6.0},
        {"driver_id": "B", "arrival": 0, "departure": 16, "requested_kwh": 3.0},
        {"driver_id": "C", "arrival": 1, "departure": 16, "requested_kwh": 6.0},
    ]
    drivers = {
        "A": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
        "B": {"type": "Urgent", "v": 3, "w": 3, "h": 1, "rule": "Release"},
        "C": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
    }
    state = {"queue": ChargerQueue(1), "last_visits": {}, "n_chargers": 1}
    visits, _ = run_day(requests, drivers, policy, state)
    visits = sorted(visits, key=lambda v: v["driver_id"])

    starts = {v["driver_id"]: v["start"] for v in visits}
    assert starts == {"A": 0, "B": 2, "C": 3}

    total_wait = sum(v["wait_slots"] for v in visits)
    assert total_wait == 4

    total_energy = sum(v["energy_kwh"] for v in visits)
    assert total_energy == 15.0

    total_utility = sum(v["utility_after"] for v in visits)
    assert total_utility == 25.0


def test_mini_case_a_holds_one_slot():
    policy = POLICIES["P0"]
    requests = [
        {"driver_id": "A", "arrival": 0, "departure": 16, "requested_kwh": 6.0},
        {"driver_id": "B", "arrival": 0, "departure": 16, "requested_kwh": 3.0},
        {"driver_id": "C", "arrival": 1, "departure": 16, "requested_kwh": 6.0},
    ]
    drivers = {
        "A": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Hold 1"},
        "B": {"type": "Urgent", "v": 3, "w": 3, "h": 1, "rule": "Release"},
        "C": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
    }
    state = {"queue": ChargerQueue(1), "last_visits": {}, "n_chargers": 1}
    visits, _ = run_day(requests, drivers, policy, state)
    visits = sorted(visits, key=lambda v: v["driver_id"])

    starts = {v["driver_id"]: v["start"] for v in visits}
    assert starts == {"A": 0, "B": 3, "C": 4}

    total_wait = sum(v["wait_slots"] for v in visits)
    assert total_wait == 6

    total_energy = sum(v["energy_kwh"] for v in visits)
    assert total_energy == 15.0

    total_utility = sum(v["utility_after"] for v in visits)
    assert total_utility == 23.0
