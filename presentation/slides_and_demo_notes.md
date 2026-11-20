# Presentation & Demonstration Plan (8–10 Minutes)

## Presentation Overview
- **Total Duration:** 8–10 minutes presentation + 3–5 minutes individual viva.
- **Presenter Role Distribution:** 
  - Speaker 1: Problem definition, research question, and mini case validation (2 mins).
  - Speaker 2: Game-theoretic foundations (extensive form, repeated games, Bayesian screening) (2.5 mins).
  - Speaker 3: Simulator architecture, matched-seed results, and the limit experiment (2.5 mins).
  - Speaker 4: Evolutionary replicator dynamics, dashboard demonstration, and policy takeaways (2 mins).

---

## Slide-by-Slide Outline

### Slide 1: Title & The Core Dilemma (1 min)
- **Title:** Fair Access to Shared EV Chargers: A Game-Theoretic and Queueing Investigation.
- **Problem:** When an EV finishes charging, drivers frequently leave their car plugged in to avoid parking relocation. Subsequent drivers wait.
- **Research Question:** Does an idle penalty reduce waiting, and how does it affect drivers with asymmetric private urgency?
- **Policies Tested:** $P_0$ (FCFS, fee $= 0$) vs. $P_1$ (FCFS, idle fee $F=2$ points/slot).

### Slide 2: Checkpoint 2: Deterministic Mini Case Validation (1.5 mins)
- **Setup:** 1 charger, 16 slots, 3 drivers ($A, B, C$).
- **Scenario 1 (All Release):** Starts at slots $(0, 2, 3)$, total wait $= 4$, energy $= 15\text{ kWh}$, utility $= 25.0$.
- **Scenario 2 ($A$ Holds 1 Slot):** Starts at slots $(0, 3, 4)$, total wait $= 6$, energy $= 15\text{ kWh}$, utility $= 23.0$.
- **Takeaway:** Establishes exact mathematical and algorithmic verification of queue allocation and utility logic.

### Slide 3: Game Theory Insights: Normal, Extensive & Bayesian Games (2 mins)
- **Normal Form:** Prisoner's Dilemma. $(H,H)$ is the unique dominant-strategy Nash equilibrium ($1,1$) despite $(C,C)$ yielding social optimum ($4,4$).
- **Extensive Form & Information Sets:** Backward induction SPE path is $(H,H)$. Hiding $P_1$'s move yields an identical normal-form game under Kuhn's theorem.
- **Bayesian Screening ($F=1.5, \pi=0.30$):**
  - Urgent playing $C$: $1.20$ vs. deviate to $H$: $1.00 \implies$ chooses $C$.
  - Flexible playing $H$: $2.00$ vs. deviate to $C$: $1.20 \implies$ chooses $H$.
  - Confirms a strict Bayesian Nash Equilibrium $(\text{Urgent} \to C, \text{Flexible} \to H)$.

### Slide 4: Simulation Results across 30 Main Runs (2 mins)
- **Experimental Matrix:** $2 \text{ policies} \times 3 \text{ demand levels} \times 5 \text{ seeds} = 30$ runs (60 days each).
- **Low Demand:** Minimal congestion; fee has negligible effect.
- **Medium Demand:** Waiting time cut by $>50\%$ (from $0.21$ to $0.09$ slots).
- **High Demand:** Waiting drops by $46.1\%$ (from $1.06$ to $0.57$ slots). Zero unserved requests.
- **Distributional Impact:** Urgent drivers gain significantly ($+18\%$ net utility). Flexible drivers face a tradeoff between lost parking convenience and reduced queue delays.

### Slide 5: The Limit Run: When the Fee Does Not Help (1.5 mins)
- **Hypothesis:** What if drivers cannot or will not change behavior?
- **Experiment:** 10 runs with all 40 drivers locked into fixed `Hold` at medium demand.
- **Result:** Waiting time is identical under $P_0$ and $P_1$ ($0.578$ slots). 
- **Finding:** Under price-inelastic behavior, the fee fails to relieve congestion and simply extracts a deadweight financial penalty (utility drops from $16.02$ to $9.64$).

### Slide 6: Evolutionary Replicator Dynamics & Live Demo (2 mins)
- **Replicator Equation:** $x_{t+1} = x_t + 0.05 x_t (1 - x_t) (f_C - f_H)$.
- **Hand Check Verified:** Step 1 under $F=0$ yields $x_1 = 0.48125$.
- **Graph:** $F=0$ rapidly decays to 0 (all Hold); $F=2$ converges monotonically to 1 (all Cooperate).
- **Live Streamlit Demo:**
  - Launch `python -m streamlit run src/app/results_screen.py`.
  - Toggle between $P_0$ and $P_1$ at medium/high demand to display real-time matched seed metrics and the evolutionary plot.

---

## Demonstration Script & Viva Talking Points

1. **How does the queue guarantee FIFO fairness?**
   - At each slot boundary, waiting drivers are sorted by `(arrival_time, driver_id)` before assignment to free chargers.
2. **Why does $P_1$ have zero idle slots in the main runs?**
   - Under $F=2$, Fee-Aware drivers evaluate $(h - F)O = (2 - 2)O = 0$. Since tie-breaking defaults to Release, holding yields zero net gain and they choose to unplug.
3. **What is the significance of the discount factor threshold $\delta \ge 0.40$?**
   - In an infinitely repeated game, cooperation can only be sustained if drivers value tomorrow's retaliation at least $40\%$ as much as today's temptation payoff.
4. **How do you defend using synthetic data?**
   - Synthetic data allows controlled isolation of specific behavioral rules and demand densities. We explicitly acknowledge in Section 6 that real ACN traces contain confounding variables (battery degradation, unobserved driver schedules) that our controlled study intentionally isolates.
