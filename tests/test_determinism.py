import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulator.engine import run_simulation
from simulator.io import load_inputs
from simulator.policies import POLICIES


def test_simulation_determinism():
    seed_dir = Path(__file__).resolve().parents[1] / "data" / "data_seed_0"
    requests, drivers = load_inputs(str(seed_dir))
    policy = POLICIES["P0"]

    # Filter to 3 days for quick test
    reqs = [r for r in requests if r.get("demand") == "low" and r["day"] < 3]

    res1 = run_simulation(reqs, drivers, policy, n_chargers=6, n_days=3)
    res2 = run_simulation(reqs, drivers, policy, n_chargers=6, n_days=3)

    assert len(res1) == len(res2)
    for v1, v2 in zip(res1, res2):
        assert v1["driver_id"] == v2["driver_id"]
        assert v1["start"] == v2["start"]
        assert v1["energy_kwh"] == v2["energy_kwh"]
        assert v1["wait_slots"] == v2["wait_slots"]
        assert v1["idle_slots"] == v2["idle_slots"]
        assert v1["utility_after"] == v2["utility_after"]
