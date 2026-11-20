"""Local results screen: choose demand, P0/P1 and seed; show settings and input files used,
comparison table/chart (waiting, completion, energy, idle, by type) and the evolutionary graph.
Displayed numbers must match the saved files in results/.
"""

import json
import os
from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Root directory
BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = BASE_DIR / "results"
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="EV Charging Policy & Game Theory Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ Fair Access to Shared EV Chargers")
st.markdown(
    "Game-theoretic analysis and queue simulation comparing **Policy P0** (FCFS, No Penalty) "
    "with **Policy P1** (FCFS + Idle Penalty of 2 points per slot)."
)

# Sidebar options
st.sidebar.header("Run Selection")
run_type = st.sidebar.radio("Run Type", ["Main Run (Programmable Rules)", "Limit Check (All Fixed to Hold)"])

if run_type == "Main Run (Programmable Rules)":
    demand = st.sidebar.selectbox("Demand Level", ["low", "medium", "high"], index=1)
    policy = st.sidebar.selectbox("Policy", ["P0", "P1"], index=0)
    seed = st.sidebar.selectbox("Random Seed", [0, 1, 2, 3, 4], index=0)
    run_dir = RESULTS_DIR / "main" / f"{policy}_{demand}_seed_{seed}"
    alt_policy = "P1" if policy == "P0" else "P0"
    alt_dir = RESULTS_DIR / "main" / f"{alt_policy}_{demand}_seed_{seed}"
else:
    demand = "medium"
    policy = st.sidebar.selectbox("Policy", ["P0", "P1"], index=0)
    seed = st.sidebar.selectbox("Random Seed", [0, 1, 2, 3, 4], index=0)
    run_dir = RESULTS_DIR / "limit" / f"{policy}_medium_seed_{seed}"
    alt_policy = "P1" if policy == "P0" else "P0"
    alt_dir = RESULTS_DIR / "limit" / f"{alt_policy}_medium_seed_{seed}"

# Load files
if not run_dir.exists():
    st.warning(f"No saved results found at `{run_dir}`. Please run `python scripts/run_all.py` first.")
else:
    settings_path = run_dir / "settings.json"
    summary_path = run_dir / "summary.json"
    visits_path = run_dir / "visits.csv"

    with open(settings_path) as f:
        settings = json.load(f)
    with open(summary_path) as f:
        summary = json.load(f)
    df_visits = pd.read_csv(visits_path)

    # 1. Settings & Input files
    st.subheader("📋 Run Settings & Inputs")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Policy", settings["policy"], f"Fee: {settings['fee']} pts/slot")
    col2.metric("Demand", settings["demand"].capitalize())
    col3.metric("Seed", settings["seed"])
    col4.metric("Days Simulated", settings["n_days"])

    input_sessions = DATA_DIR / f"data_seed_{seed}" / "sessions_public.csv"
    input_drivers = DATA_DIR / f"data_seed_{seed}" / "drivers_private.csv"
    st.caption(f"**Input files:** `{input_sessions}` | `{input_drivers}`")

    # 2. Key Metrics
    st.subheader("📊 Key Performance Metrics")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Avg Waiting (slots)", f"{summary['avg_waiting']:.2f}")
    m2.metric("Fully Served Share", f"{summary['share_fully_served']*100:.1f}%")
    m3.metric("Total Energy (kWh)", f"{summary['total_energy']:.1f}")
    m4.metric("Total Idle Slots", f"{summary['total_idle']}")
    m5.metric("Avg Utility (Net)", f"{summary['avg_utility_after']:.2f}")

    # 3. Urgent vs Flexible breakdown
    st.subheader("👥 Performance by Driver Type")
    type_data = {
        "Metric": [
            "Visits Count",
            "Avg Waiting (slots)",
            "Fully Served Share",
            "Delivered Energy (kWh)",
            "Idle Slots Held",
            "Utility Before Penalty",
            "Net Utility After Penalty"
        ],
        "Urgent Drivers (v=3, w=3, h=1)": [
            str(summary.get("urgent_n", 0)),
            f"{float(summary.get('urgent_avg_waiting', 0)):.2f}",
            f"{float(summary.get('urgent_share_fully_served', 0))*100:.1f}%",
            f"{float(summary.get('urgent_total_energy', 0)):.1f}",
            str(summary.get("urgent_total_idle", 0)),
            f"{float(summary.get('urgent_avg_utility_before', 0)):.2f}",
            f"{float(summary.get('urgent_avg_utility_after', 0)):.2f}",
        ],
        "Flexible Drivers (v=2, w=1, h=2)": [
            str(summary.get("flexible_n", 0)),
            f"{float(summary.get('flexible_avg_waiting', 0)):.2f}",
            f"{float(summary.get('flexible_share_fully_served', 0))*100:.1f}%",
            f"{float(summary.get('flexible_total_energy', 0)):.1f}",
            str(summary.get("flexible_total_idle", 0)),
            f"{float(summary.get('flexible_avg_utility_before', 0)):.2f}",
            f"{float(summary.get('flexible_avg_utility_after', 0)):.2f}",
        ]
    }
    st.table(pd.DataFrame(type_data))

    # 4. Matched Policy Comparison (P0 vs P1)
    if alt_dir.exists():
        st.subheader(f"⚖️ Matched-Seed Comparison: {policy} vs {alt_policy}")
        with open(alt_dir / "summary.json") as f:
            alt_summary = json.load(f)

        c1, c2, c3, c4 = st.columns(4)
        wait_diff = summary['avg_waiting'] - alt_summary['avg_waiting']
        serv_diff = (summary['share_fully_served'] - alt_summary['share_fully_served']) * 100
        idle_diff = summary['total_idle'] - alt_summary['total_idle']
        util_diff = summary['avg_utility_after'] - alt_summary['avg_utility_after']

        c1.metric(f"Avg Wait Diff ({policy} - {alt_policy})", f"{wait_diff:+.2f} slots")
        c2.metric(f"Fully Served Diff", f"{serv_diff:+.1f}%")
        c3.metric(f"Idle Slots Diff", f"{idle_diff:+d}")
        c4.metric(f"Net Utility Diff", f"{util_diff:+.2f}")

    # 5. Evolutionary Dynamics Graph
    st.subheader("📈 Evolutionary Dynamics of Cooperation (F=0 vs F=2)")
    fig_path = RESULTS_DIR / "figures" / "evolution_F0_vs_F2.png"
    if fig_path.exists():
        st.image(str(fig_path), caption="Trajectory of Cooperation Share x over 30 updates from x0 = 0.5")
    else:
        st.info("Run `python scripts/make_figures.py` to view the saved figure.")

    # 6. Sample Visits Data
    with st.expander("🔍 View Raw Visit Logs (first 50 visits)"):
        # Format display dataframe for clean arrow serialization
        display_df = df_visits.head(50).copy()
        if 'start' in display_df.columns:
            display_df['start'] = display_df['start'].apply(lambda x: str(int(x)) if pd.notna(x) and x != '' else 'Unserved')
        st.dataframe(display_df)
