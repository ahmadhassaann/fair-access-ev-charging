"""2 policies x 3 demand levels x 5 seeds = 30 main runs (60 days each),
plus 10 limit runs: medium demand, every driver fixed to Hold, both policies, seeds 0-4.
"""

import json
import os
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from analysis.compare import aggregate_comparisons, compare_policies
from analysis.metrics import compute_metrics
from simulator.engine import run_simulation
from simulator.io import load_inputs, save_results
from simulator.policies import POLICIES


DEMANDS = ["low", "medium", "high"]
SEEDS = [0, 1, 2, 3, 4]
POLICIES_LIST = ["P0", "P1"]
N_CHARGERS = 6
N_DAYS = 60


def run_all():
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    results_dir = base_dir / "results"

    print("=== Running 30 Main Experiments ===")
    main_summaries = {}

    for demand in DEMANDS:
        for seed in SEEDS:
            seed_dir = data_dir / f"data_seed_{seed}"
            raw_requests, base_drivers = load_inputs(str(seed_dir))
            demand_requests = [r for r in raw_requests if r.get("demand") == demand]

            for pol_name in POLICIES_LIST:
                policy = POLICIES[pol_name]
                # Drivers dictionary fresh copy
                drivers = {k: dict(v) for k, v in base_drivers.items()}

                visits = run_simulation(demand_requests, drivers, policy, N_CHARGERS, N_DAYS)
                df_visits = pd.DataFrame(visits)
                metrics = compute_metrics(df_visits)

                out_dir = results_dir / "main" / f"{pol_name}_{demand}_seed_{seed}"
                settings = {
                    "policy": pol_name,
                    "demand": demand,
                    "seed": seed,
                    "fee": policy["fee"],
                    "n_chargers": N_CHARGERS,
                    "n_days": N_DAYS,
                    "limit_run": False
                }
                save_results(str(out_dir), visits, settings, metrics)
                main_summaries[(pol_name, demand, seed)] = metrics
                print(f"  Saved main run: {pol_name} {demand} seed {seed} (avg wait: {metrics['avg_waiting']:.2f})")

    print("\n=== Running 10 Limit Runs (Medium Demand, All Hold) ===")
    limit_summaries = {}
    for seed in SEEDS:
        seed_dir = data_dir / f"data_seed_{seed}"
        raw_requests, base_drivers = load_inputs(str(seed_dir))
        demand_requests = [r for r in raw_requests if r.get("demand") == "medium"]

        for pol_name in POLICIES_LIST:
            policy = POLICIES[pol_name]
            drivers = {k: dict(v) for k, v in base_drivers.items()}
            for did in drivers:
                drivers[did]["rule"] = "Hold"

            visits = run_simulation(demand_requests, drivers, policy, N_CHARGERS, N_DAYS)
            df_visits = pd.DataFrame(visits)
            metrics = compute_metrics(df_visits)

            out_dir = results_dir / "limit" / f"{pol_name}_medium_seed_{seed}"
            settings = {
                "policy": pol_name,
                "demand": "medium",
                "seed": seed,
                "fee": policy["fee"],
                "n_chargers": N_CHARGERS,
                "n_days": N_DAYS,
                "limit_run": True,
                "forced_rule": "Hold"
            }
            save_results(str(out_dir), visits, settings, metrics)
            limit_summaries[(pol_name, seed)] = metrics
            print(f"  Saved limit run: {pol_name} medium seed {seed} (avg wait: {metrics['avg_waiting']:.2f})")

    print("\n=== Computing Matched-Seed Comparisons (P1 - P0) ===")
    comp_dir = results_dir / "comparisons"
    os.makedirs(comp_dir, exist_ok=True)
    all_agg = {}

    def _json_default(obj):
        if hasattr(obj, 'item'):
            return obj.item()
        return str(obj)

    for demand in DEMANDS:
        comparisons = []
        for seed in SEEDS:
            p0_m = main_summaries[("P0", demand, seed)]
            p1_m = main_summaries[("P1", demand, seed)]
            chg = compare_policies(p0_m, p1_m)
            chg["seed"] = seed
            chg["demand"] = demand
            comparisons.append(chg)

        agg = aggregate_comparisons(comparisons)
        all_agg[demand] = agg

        with open(comp_dir / f"matched_changes_{demand}.json", "w") as f:
            json.dump(agg, f, indent=2, default=_json_default)
        print(f"  Demand {demand}: Avg wait change = {agg['mean']['avg_waiting']:.3f} slots")

    with open(comp_dir / "aggregated_summary.json", "w") as f:
        json.dump(all_agg, f, indent=2, default=_json_default)

    print("\n[SUCCESS] Completed all 30 main + 10 limit runs and saved comparisons!")


if __name__ == "__main__":
    run_all()
