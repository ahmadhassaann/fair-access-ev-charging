"""Save results/figures/evolution_F0_vs_F2.png and any comparison charts."""

import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from game_theory.evolutionary import path


def make_evolution_figure(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    steps = list(range(31))
    path_f0 = path(fee=0, x0=0.5, n=30)
    path_f2 = path(fee=2, x0=0.5, n=30)

    plt.figure(figsize=(8, 5))
    plt.plot(steps, path_f0, 'o-', color='#e74c3c', linewidth=2, label="F = 0 (No Fee, P0)")
    plt.plot(steps, path_f2, 's-', color='#2ecc71', linewidth=2, label="F = 2 (Idle Fee, P1)")

    plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.6, label="Initial x0 = 0.5")
    plt.title("Replicator Dynamics of Cooperation Share x Over 30 Updates", fontsize=13, fontweight='bold')
    plt.xlabel("Update Step t", fontsize=11)
    plt.ylabel("Cooperate Share x(t)", fontsize=11)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=10, loc='center right')
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved evolutionary figure to {output_path}")


def make_comparison_figures(results_dir):
    figures_dir = os.path.join(results_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    # Check if results exist
    import json
    comp_file = os.path.join(results_dir, "comparisons", "aggregated_summary.json")
    if not os.path.exists(comp_file):
        print("Aggregated summary not found, skipping comparison bar charts.")
        return

    with open(comp_file, "r") as f:
        summary = json.load(f)

    demands = ["low", "medium", "high"]
    wait_changes = [summary[d]["mean"]["avg_waiting"] for d in demands]
    energy_changes = [summary[d]["mean"]["total_energy"] for d in demands]

    plt.figure(figsize=(7, 4.5))
    bars = plt.bar(demands, wait_changes, color=['#3498db', '#e67e22', '#e74c3c'], width=0.5)
    plt.axhline(0, color='black', linewidth=1)
    plt.title("Average Waiting Slot Change (P1 - P0) Across Demand Levels", fontsize=12, fontweight='bold')
    plt.xlabel("Demand Level", fontsize=11)
    plt.ylabel("Change in Avg Waiting Slots", fontsize=11)
    plt.grid(axis='y', linestyle=':', alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -12),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    chart_path = os.path.join(figures_dir, "waiting_change_comparison.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Saved comparison chart to {chart_path}")


def main():
    base_dir = Path(__file__).resolve().parents[1]
    fig_dir = base_dir / "results" / "figures"
    make_evolution_figure(str(fig_dir / "evolution_F0_vs_F2.png"))
    make_comparison_figures(str(base_dir / "results"))


if __name__ == "__main__":
    main()
