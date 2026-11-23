"""Run the mini case under P0. Must reproduce 4 / 15 / 25 (all release) and 6 / 15 / 23 (A holds one slot)
as defined in data/mini_case_expected.json.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulator.charger_queue import ChargerQueue
from simulator.engine import run_day
from simulator.policies import POLICIES


def run_mini_case():
    base_dir = Path(__file__).resolve().parents[1]
    expected_file = base_dir / "data" / "starter" / "mini_case_expected.json"
    if not expected_file.exists():
        expected_file = base_dir / "data" / "mini_case_expected.json"

    with open(expected_file, "r") as f:
        expected = json.load(f)

    policy = POLICIES["P0"]

    # Mini case requests from mini_case_public.csv:
    # A: arrives 0, departs 4, requests 6 kWh
    # B: arrives 0, departs 5, requests 3 kWh
    # C: arrives 1, departs 6, requests 6 kWh
    requests = [
        {"driver_id": "A", "arrival": 0, "departure": 4, "requested_kwh": 6.0},
        {"driver_id": "B", "arrival": 0, "departure": 5, "requested_kwh": 3.0},
        {"driver_id": "C", "arrival": 1, "departure": 6, "requested_kwh": 6.0},
    ]

    # --- Scenario 1: All Release ---
    drivers_rel = {
        "A": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
        "B": {"type": "Urgent", "v": 3, "w": 3, "h": 1, "rule": "Release"},
        "C": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
    }
    state_rel = {
        "queue": ChargerQueue(1),
        "last_visits": {},
        "n_chargers": 1
    }
    visits_rel, _ = run_day(requests, drivers_rel, policy, state_rel, day_slots=6)

    by_driver_rel = {v["driver_id"]: v for v in visits_rel}
    exp_rel = expected["all_release"]

    print("=== SCENARIO 1: All Release ===")
    for did in ["A", "B", "C"]:
        v = by_driver_rel[did]
        e = exp_rel[did]
        print(f"Driver {did}: start={v['start']} (exp {e['start']}), finish={v['finish']} (exp {e['finish']}), release={v['release']} (exp {e['release']}), wait={v['wait_slots']} (exp {e['wait_slots']}), util={v['utility_after']} (exp {e['utility']})")
        assert v["start"] == e["start"]
        assert v["finish"] == e["finish"]
        assert v["release"] == e["release"]
        assert v["wait_slots"] == e["wait_slots"]
        assert v["utility_after"] == e["utility"]

    total_wait_rel = sum(v["wait_slots"] for v in visits_rel)
    total_energy_rel = sum(v["energy_kwh"] for v in visits_rel)
    total_util_rel = sum(v["utility_after"] for v in visits_rel)
    assert total_wait_rel == exp_rel["total_wait_slots"]
    assert total_energy_rel == exp_rel["delivered_kwh"]
    assert total_util_rel == exp_rel["total_utility"]
    print(f"Totals: wait={total_wait_rel}, energy={total_energy_rel}, utility={total_util_rel} -> MATCHED!")

    # --- Scenario 2: A holds one slot, B and C release ---
    drivers_hold = {
        "A": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Hold 1"},
        "B": {"type": "Urgent", "v": 3, "w": 3, "h": 1, "rule": "Release"},
        "C": {"type": "Flexible", "v": 2, "w": 1, "h": 2, "rule": "Release"},
    }
    state_hold = {
        "queue": ChargerQueue(1),
        "last_visits": {},
        "n_chargers": 1
    }
    visits_hold, _ = run_day(requests, drivers_hold, policy, state_hold, day_slots=6)

    by_driver_hold = {v["driver_id"]: v for v in visits_hold}
    exp_hold = expected["A_holds_one_slot"]

    print("\n=== SCENARIO 2: A Holds One Slot ===")
    for did in ["A", "B", "C"]:
        v = by_driver_hold[did]
        e = exp_hold[did]
        print(f"Driver {did}: start={v['start']} (exp {e['start']}), finish={v['finish']} (exp {e['finish']}), release={v['release']} (exp {e['release']}), wait={v['wait_slots']} (exp {e['wait_slots']}), util={v['utility_after']} (exp {e['utility']})")
        assert v["start"] == e["start"]
        assert v["finish"] == e["finish"]
        assert v["release"] == e["release"]
        assert v["wait_slots"] == e["wait_slots"]
        assert v["utility_after"] == e["utility"]

    total_wait_hold = sum(v["wait_slots"] for v in visits_hold)
    total_energy_hold = sum(v["energy_kwh"] for v in visits_hold)
    total_util_hold = sum(v["utility_after"] for v in visits_hold)
    assert total_wait_hold == exp_hold["total_wait_slots"]
    assert total_energy_hold == exp_hold["delivered_kwh"]
    assert total_util_hold == exp_hold["total_utility"]
    print(f"Totals: wait={total_wait_hold}, energy={total_energy_hold}, utility={total_util_hold} -> MATCHED!")

    print("\n[SUCCESS] Mini case exactly reproduced all values in mini_case_expected.json!")
    return True


if __name__ == "__main__":
    run_mini_case()
