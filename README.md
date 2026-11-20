# Fair Access to Shared EV Chargers

Game Theory semester project: a small charging-queue simulator comparing
P0 (first come first served, no penalty) with P1 (same queue, idle penalty of
2 points per idle slot), plus written game-theory work and one evolutionary graph.

## Setup
1. Put the supplied starter archive files in `data/starter/` (untouched) and
   the settings files (`config.json`, `chargers.csv`, `policies.csv`) in `config/`.
2. `pip install -r requirements.txt`

## Run
- Mini case check: `python scripts/run_mini_case.py`
- Generate seeds 0-4: `bash scripts/generate_all_seeds.sh`
- All 30 main runs + 10 fixed-Hold limit runs: `python scripts/run_all.py`
- Figures: `python scripts/make_figures.py`
- Tests: `pytest tests/`
- Results screen: `python -m streamlit run src/app/results_screen.py`

## Layout
See the folder tree: `src/` (code), `data/` (inputs, one folder per seed),
`results/` (saved outputs), `written/` (Sections 3-4), `report/`, `proposal/`, `presentation/`.

## Checkpoints
1. Proposal and input checks  2. Simulator passes mini case
3. Written tasks, evolutionary graph, saved results  4. Results screen, report, demo
