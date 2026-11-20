import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from analysis.checks import run_all_checks
from simulator.engine import run_simulation
from simulator.io import load_inputs
from simulator.policies import POLICIES


def test_invariants_pass():
    seed_dir = Path(__file__).resolve().parents[1] / "data" / "data_seed_0"
    requests, drivers = load_inputs(str(seed_dir))
    policy = POLICIES["P1"]

    # Run 5 days of medium demand
    reqs = [r for r in requests if r.get("demand") == "medium" and r["day"] < 5]
    visits = run_simulation(reqs, drivers, policy, n_chargers=6, n_days=5)

    df = pd.DataFrame(visits)
    checks = run_all_checks(df, n_chargers=6)

    for check_name, passed in checks.items():
        assert passed, f"Invariant check failed: {check_name}"
