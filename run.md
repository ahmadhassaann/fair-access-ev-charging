# How to Run the Project

This guide provides step-by-step instructions to set up the environment, run verification tests, execute the simulation experiments, generate figures, and launch the interactive results dashboard.

---

## 1. Prerequisites & Environment Setup

Ensure you have **Python 3.10+** installed.

### Install Dependencies
From the project root directory (`MultiAgent/`), install the required packages:

```bash
pip install -r requirements.txt
```

*Installed dependencies:* `pandas`, `numpy`, `matplotlib`, `pytest`, `streamlit`.

---

## 2. Quick Verification Checks

Run these commands to verify that the environment, simulator logic, and theoretical checks are working properly:

### A. Run All Unit & Invariant Tests
Runs tests for determinism, evolutionary dynamics, simulator invariants, and the mini case:
```bash
python -m pytest tests/
```
*(Expected: `6 passed in ~0.6s`)*

### B. Run Mini Case Check
Verifies the deterministic 1-charger, 3-driver benchmark ($4 / 15 / 25$ under all release; $6 / 15 / 23$ when Driver A holds):
```bash
python scripts/run_mini_case.py
```
*(Expected: `[SUCCESS] Mini case passed all assertions!`)*

### C. Run Game Theory Arithmetic Checks
Verifies backward induction, repeated game threshold ($\delta^* = 0.40$), Bayesian Nash Equilibrium screening ($F=1.5$), memory trees, and Kuhn's theorem:
```bash
python src/game_theory/arithmetic_checks.py
```
*(Expected: `All arithmetic checks passed!`)*

---

## 3. Data Generation (Optional / Reproducibility)

Pre-generated datasets for seeds 0–4 and starter already exist in `data/`. If you want to re-generate them from scratch:

### On Linux / macOS / Git Bash:
```bash
bash scripts/generate_all_seeds.sh
```

### On Windows (PowerShell):
```powershell
python data/starter/generate_data.py --output data/starter --seed 42 --urgent-prior 0.30
for ($s=0; $s -le 4; $s++) {
    python data/starter/generate_data.py --output data/data_seed_$s --seed $s --urgent-prior 0.30
}
```

---

## 4. Run All Experiments (30 Main + 10 Limit Runs)

Execute the full suite of simulation runs:
- **30 Main Runs:** $2 \text{ policies } (P_0, P_1) \times 3 \text{ demand levels } (\text{low, medium, high}) \times 5 \text{ seeds } (0\text{–}4)$ covering 60 days each.
- **10 Limit Runs:** Medium demand, all 40 drivers locked into fixed `Hold` under both policies, seeds 0–4.
- **Matched Comparisons:** Automatically calculates $P_1 - P_0$ paired differences per seed, means, and spreads.

```bash
python scripts/run_all.py
```

### Output Files Generated:
- `results/main/{policy}_{demand}_seed_{seed}/`:
  - `visits.csv`: Complete visit-by-visit logs (arrival, start, energy, waiting, idle, utility).
  - `settings.json`: Configuration used for the run.
  - `summary.json`: Summary metrics overall and broken down by Urgent/Flexible.
- `results/limit/{policy}_medium_seed_{seed}/`: Same outputs for limit runs.
- `results/comparisons/`:
  - `matched_changes_{demand}.json`: Seed-by-seed and average metric changes ($P_1 - P_0$).
  - `aggregated_summary.json`: Aggregated comparative summary across all demands.

---

## 5. Generate Figures

Generate the evolutionary replicator dynamics graph and comparison charts:

```bash
python scripts/make_figures.py
```

### Saved Figures:
- `results/figures/evolution_F0_vs_F2.png`: Replicator dynamics showing convergence to universal defection ($F=0$) vs. universal cooperation ($F=2$).
- `results/figures/waiting_change_comparison.png`: Bar chart of average waiting time reduction $(P_1 - P_0)$ across demand levels.

---

## 6. Launch Interactive Results Screen (Streamlit App)

To inspect run outputs, view comparison metrics, examine driver type breakdowns, and explore raw visit logs in an interactive browser UI:

```bash
python -m streamlit run src/app/results_screen.py
```

*(This opens `http://localhost:8501` in your default web browser).*

### Features in Dashboard:
1. **Interactive Selectors:** Choose between Main Runs and Limit Checks, select Demand Level (low/medium/high), Policy ($P_0$/$P_1$), and Seed ($0\text{–}4$).
2. **Settings & Inputs:** Displays configuration, charger parameters, and active input CSV paths.
3. **Key Metrics Cards:** Shows average waiting slots, completion rate, delivered energy, total idle slots, and net utility.
4. **Driver Type Breakdown:** Comparative table showing performance of **Urgent** vs. **Flexible** drivers.
5. **Matched-Seed Delta:** Direct side-by-side comparison with the alternative policy ($P_1 - P_0$).
6. **Evolutionary Graph:** Displays the saved replicator dynamics plot.
7. **Raw Log Viewer:** Expandable table showing individual visit-level records.

---

## 7. Project Directory Structure Reference

```
MultiAgent/
├── README.md                      # Overview & project summary
├── run.md                         # How to run instructions (this file)
├── requirements.txt               # Python package dependencies
├── config/
│   ├── config.json                # Base facility settings
│   ├── run_settings.json          # Experiment settings
│   ├── chargers.csv               # 6 chargers mapping
│   └── policies.csv               # P0 and P1 definitions
├── data/
│   ├── starter/                   # Reference datasets & generator script
│   ├── mini_case/                 # Mini case input files & expected JSONs
│   └── data_seed_0/ ... seed_4/   # 5 random seed datasets
├── src/
│   ├── simulator/                 # Queue, engine, driver rules, I/O, utility
│   ├── analysis/                  # Metrics, policy comparison, invariant checks
│   ├── game_theory/               # Evolutionary dynamics, arithmetic proofs
│   └── app/                       # Streamlit results dashboard
├── scripts/
│   ├── run_mini_case.py           # Mini case verification
│   ├── run_all.py                 # 30 main + 10 limit experiment runner
│   ├── make_figures.py            # Figure generator
│   └── generate_all_seeds.sh      # Shell script to regenerate seeds
├── tests/                         # Pytest test suite (6 tests)
├── written/                       # Game theory solutions (3A, 3B, 3C, 4A, 4B)
├── report/                        # 6-8 page academic report, appendix, paper note
├── proposal/                      # One-page project proposal
├── presentation/                  # Slide outline & demo presentation notes
└── results/                       # Simulation outputs, figures, and comparisons
```
