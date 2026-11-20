"""Run the mini case under P0. Must reproduce 4 / 15 / 25 (all release) and 6 / 15 / 23 (A holds one slot)."""

import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulator.charger_queue import ChargerQueue
from simulator.engine import run_day
from simulator.policies import POLICIES


def run_mini_case():
    policy = POLICIES["P0"]

    # Common requests
    requests = [
        {"driver_id": "A", "arrival": 0, "departure": 16, "requested_kwh": 6.0},
        {"driver_id": "B", "arrival": 0, "departure": 16, "requested_kwh": 3.0},
        {"driver_id": "C", "arrival": 1, "departure": 16, "requested_kwh": 6.0},
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
    visits_rel, _ = run_day(requests, drivers_rel, policy, state_rel)

    # Sort visits by driver_id
    visits_rel = sorted(visits_rel, key=lambda v: v["driver_id"])
    starts_rel = {v["driver_id"]: v["start"] for v in visits_rel}
    wait_rel = sum(v["wait_slots"] for v in visits_rel)
    energy_rel = sum(v["energy_kwh"] for v in visits_rel)
    util_rel = sum(v["utility_after"] for v in visits_rel)

    print("--- Scenario 1: All Release ---")
    print(f"Starts: {starts_rel} (expected A:0, B:2, C:3)")
    print(f"Waiting slots: {wait_rel} (expected 4)")
    print(f"Delivered energy: {energy_rel} (expected 15)")
    print(f"Total utility: {util_rel} (expected 25)")

    assert starts_rel == {"A": 0, "B": 2, "C": 3}, f"Starts mismatch: {starts_rel}"
    assert wait_rel == 4, f"Waiting mismatch: {wait_rel}"
    assert energy_rel == 15.0, f"Energy mismatch: {energy_rel}"
    assert util_rel == 25.0, f"Utility mismatch: {util_rel}"

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
    visits_hold, _ = run_day(requests, drivers_hold, policy, state_hold)

    visits_hold = sorted(visits_hold, key=lambda v: v["driver_id"])
    starts_hold = {v["driver_id"]: v["start"] for v in visits_hold}
    wait_hold = sum(v["wait_slots"] for v in visits_hold)
    energy_hold = sum(v["energy_kwh"] for v in visits_hold)
    util_hold = sum(v["utility_after"] for v in visits_hold)

    print("\n--- Scenario 2: A Holds One Slot ---")
    print(f"Starts: {starts_hold} (expected A:0, B:3, C:4)")
    print(f"Waiting slots: {wait_hold} (expected 6)")
    print(f"Delivered energy: {energy_hold} (expected 15)")
    print(f"Total utility: {util_hold} (expected 23)")

    assert starts_hold == {"A": 0, "B": 3, "C": 4}, f"Starts mismatch: {starts_hold}"
    assert wait_hold == 6, f"Waiting mismatch: {wait_hold}"
    assert energy_hold == 15.0, f"Energy mismatch: {energy_hold}"
    assert util_hold == 23.0, f"Utility mismatch: {util_hold}"

    print("\n[SUCCESS] Mini case passed all assertions!")
    return True


if __name__ == "__main__":
    run_mini_case()
