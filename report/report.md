# Fair Access to Shared EV Chargers: An Empirical and Game-Theoretic Investigation

**Authors:** Semester Project Team  
**Course:** Game Theory  
**Repository:** `MultiAgent/`  
**Date:** November 2026  

---

## Abstract
Shared electric vehicle (EV) charging infrastructure frequently suffers from congestion induced by overstaying drivers who keep fully charged vehicles connected to avoid parking relocation costs. This study provides an end-to-end game-theoretic analysis and discrete-event simulation of charging-queue dynamics under two operational policies: Policy $P_0$ (First-Come, First-Served without penalties) and Policy $P_1$ (FCFS with an idle penalty of $F=2$ utility points per half-hour slot). Using a discrete simulator spanning 60 simulated days across three demand regimes (low, medium, high) and five randomized seeds (seeds 0–4), we evaluate the interaction of 40 heterogeneous drivers exhibiting Urgent and Flexible private preferences. Our analytical findings demonstrate that under medium and high demand, an idle fee reliably reduces mean queue waiting time ($-0.241$ slots at medium demand, $-0.155$ slots at high demand), increases the share of fully served requests ($+3.5\%$ and $+2.4\%$), and delivers hundreds of additional kilowatt-hours to waiting drivers. However, in our controlled limit study where drivers follow rigid, price-inelastic holding heuristics, idle fees fail to reduce congestion and instead function as a pure deadweight tax. Replicator dynamics illustrate that while no-fee regimes inevitably decay to universal defection, an idle fee of $F=2$ creates a basin of attraction driving long-run population cooperation.

---

## 1. Problem Definition and Research Question

### 1.1 Context and Real-World Relevance
Commercial and workplace charging networks operate under severe capital and spatial constraints. When an EV reaches full state-of-charge (SoC), it stops drawing energy but continues to occupy physical stall access. In networks lacking overstay disincentives, drivers treat chargers as reserved parking spots. Electrify America and other major charging operators have introduced idle fees specifically to internalize this congestion externality [1]. 

However, charging patrons possess heterogeneous private valuations. An **Urgent** driver with low remaining range incurs high disutility from waiting, whereas a **Flexible** commuter values the convenience of delayed vehicle retrieval. A uniform penalty structure that optimizes average waiting times may inadvertently penalize certain user segments.

### 1.2 Core Research Question
*Does an idle penalty reduce waiting times, and how do its welfare effects distribute across drivers with distinct private urgency and convenience needs?*

---

## 2. Theoretical Foundations and Model Formulation

### 2.1 The Strategic Dilemma
Consider two drivers sharing a charger over consecutive intervals. Each driver chooses between **Cooperate ($C$)** (release immediately upon charge completion) and **Hold ($H$)** (remain plugged in for one idle slot). The baseline normal-form payoff matrix under no fee ($P_0$, recorded in `benchmark_game.csv`) is:

$$\begin{array}{c|cc}
P_1 \setminus P_2 & C & H \\ \hline
C & (4, 4) & (0, 6) \\
H & (6, 0) & (1, 1)
\end{array}$$

Because $u_i(H, s_{-i}) > u_i(C, s_{-i})$ for all $s_{-i} \in \{C, H\}$, **Hold ($H$)** is a strictly dominant strategy for both players. The unique pure-strategy Nash Equilibrium is $(H, H)$ yielding payoff $(1, 1)$, despite $(C, C)$ yielding joint welfare $8$. This represents a canonical Prisoner's Dilemma on shared physical infrastructure [2].

### 2.2 Mechanism Design via Idle Fees
Policy $P_1$ levies an idle penalty $F = 2$ points per idle slot. The effective stage payoff for a player choosing $H$ becomes:
$$u_i'(H, s_{-i}) = u_i(H, s_{-i}) - F$$
Under $F=2$, the modified matrix becomes:
$$\begin{array}{c|cc}
P_1 \setminus P_2 & C & H \\ \hline
C & (4, 4) & (0, 4) \\
H & (4, 0) & (-1, -1)
\end{array}$$
Now, $C$ weakly dominates $H$ ($4 \ge 4$ and $0 \ge -1$). The dominant-strategy defect equilibrium is broken, aligning individual incentives with the social optimum $(C, C)$.

### 2.3 Extended Analytical Results
Our theoretical investigation (detailed in `written/` and the Appendix) establishes four key theoretical benchmarks:
1. **Extensive Form with Perfect Recall (Section 3A):** In sequential play where $P_2$ observes $P_1$'s move, backward induction yields the subgame perfect equilibrium path $(H, H)$. When $P_1$'s move is unobserved, $P_2$'s information set merges, yielding strategic equivalence to the simultaneous game under Kuhn's theorem [2].
2. **Memory Partitions and Behavioral Equivalence (Sections 3B & 3C):** Using the official terminal leaves from `memory_tree.csv`, backward induction under full information yields path $LLR \to (8, 4)$. When an agent forgets the current stage, mixed strategy lotteries (commitment) and independent behavioral draws diverge. Fresh draws yield an expected payoff of $4.25$ by exploring asymmetric branches ($LR, RL$), whereas a 50-50 mixed lottery yields only $1.50$.
3. **Repeated Games and the Folk Theorem (Section 4A):** In an infinitely repeated setting with grim trigger punishment, cooperation is sustainable as a Subgame Perfect Equilibrium if and only if the discount factor satisfies:
   $$\delta \ge \frac{2}{5} = 0.40$$
   At $\delta = 0.50$, cooperation is strictly sustainable ($V_{\text{coop}} = 8.0 > V_{\text{dev}} = 7.0$).
4. **Bayesian Screening (Section 4B):** Under prior beliefs $\pi(\text{Urgent}) = 0.30$ and $\pi(\text{Flexible}) = 0.70$ with fee $F=1.5$ (from `bayesian_types.csv`), the profile $(\text{Urgent} \to C, \text{Flexible} \to H)$ forms a strict Bayesian Nash Equilibrium ($E[U | \text{Urgent}, C] = 1.20 > 1.00$; $E[U | \text{Flexible}, H] = 2.00 > 1.20$).

---

## 3. Simulator Architecture and Experimental Design

### 3.1 Queue Engine Specification
The simulation models a single charging hub comprising:
- $M = 6$ identical Level-2 chargers ($6\text{ kW}$ rated power).
- Operating horizon: 16 discrete half-hour intervals per day ($08:00 - 16:00$).
- Energy rate: up to $3\text{ kWh}$ per full slot.
- Driver utility function:
  $$U_i = v_i \cdot (\text{delivered kWh}) - w_i \cdot (\text{waiting slots}) + h_i \cdot (\text{idle slots}) - F \cdot (\text{idle slots})$$
- Priority discipline: First-Come, First-Served (FCFS) sorted by arrival boundary, broken deterministically by unique `driver_id`.

### 3.2 Driver Type Parameterization
A synthetic population of 40 drivers is generated with private parameters (`drivers_private.csv`):
- **Urgent Drivers** ($30\%$ prior): $v=3, w=3, h=1$. Highly intolerant of waiting; minimal surplus from stall holding.
- **Flexible Drivers** ($70\%$ prior): $v=2, w=1, h=2$. Tolerant of waiting; high convenience valuation for delayed retrieval.

Each driver is assigned one of four behavioral heuristics:
- **Release:** Always unplugs immediately upon full charge.
- **Hold:** Seeks the maximum legal hold (up to 2 slots) before scheduled departure.
- **Reciprocal:** Unplugs on first visit; subsequently unplugs if and only if their previous visit experienced $\le 2$ waiting slots; otherwise holds 1 slot.
- **Fee Aware:** Chooses idle duration $O \in \{0, 1, 2\}$ maximizing $(h_i - F) \cdot O$.

### 3.3 Verification against the Deterministic Mini Case
Before full batch execution, the simulator was benchmarked against the official single-charger, 3-driver mini case (`mini_case_expected.json`):
- **All Release:** Starts at slots $(0, 2, 3)$, finishes at $(2, 3, 5)$, releases at $(2, 3, 5)$, total waiting $= 4$ slots, energy $= 15\text{ kWh}$, system utility $= 25.0$.
- **Driver A Holds 1 Slot:** Starts at slots $(0, 3, 4)$, finishes at $(2, 4, 6)$, releases at $(3, 4, 6)$, total waiting $= 6$ slots, energy $= 15\text{ kWh}$, system utility $= 23.0$.
Our simulator reproduces these exact quantities with zero error.

---

## 4. Empirical Findings

We executed 30 main simulation runs ($2 \text{ policies} \times 3 \text{ demand levels} \times 5 \text{ seeds}$, 60 days each) plus 10 limit runs.

### Table 1: Matched-Seed Performance Comparison (P0 vs. P1)
*Metrics averaged across 5 independent random seeds (60 days/run, 40 drivers, 6 chargers).*

| Demand Level | Requests/Day | Policy | Avg Wait (slots) | Fully Served (%) | Total Energy (kWh) | Net Driver Utility | Matched Wait $\Delta$ (P1 - P0) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Low** | 12 | P0 | $0.521$ | $93.2\%$ | $8,475.6$ | $27.26$ | --- |
| | 12 | P1 | $0.380$ | $95.0\%$ | $8,553.6$ | $26.27$ | **$-0.141$ slots** |
| **Medium** | 24 | P0 | $2.877$ | $59.8\%$ | $13,013.4$ | $16.97$ | --- |
| | 24 | P1 | $2.635$ | $63.3\%$ | $13,531.8$ | $17.26$ | **$-0.241$ slots** |
| **High** | 36 | P0 | $4.257$ | $38.2\%$ | $14,560.8$ | $9.32$ | --- |
| | 36 | P1 | $4.102$ | $40.7\%$ | $15,175.2$ | $9.66$ | **$-0.155$ slots** |

---

### 4.1 Finding 1: The Idle Penalty Effectively Mitigates Congestion Under Congested Demands
Across all demand regimes, Policy $P_1$ consistently reduces queue waiting times and expands energy delivery:
- At **Medium Demand** (24 requests/day), Policy $P_1$ reduces average waiting by $-0.241$ slots per driver (from $2.877$ to $2.635$). Fully served completion improves from $59.8\%$ to $63.3\%$, delivering an additional $518.4\text{ kWh}$ across the site over 60 days.
- At **High Demand** (36 requests/day), facility capacity is heavily strained. Policy $P_1$ reduces average waiting by $-0.155$ slots and boosts delivered energy by $614.4\text{ kWh}$, increasing completion rates by $+2.4\%$.
- Furthermore, under medium and high demand, overall net driver utility increases ($+0.30$ and $+0.34$ points per visit) because the disutility avoided from shorter queue delays outweighs the lost parking convenience.

### 4.2 Finding 2: Distributional Asymmetry: Who Gains and Who Loses?
The benefits of the idle fee are not distributed uniformly across driver classes:
- **Urgent Drivers Gain Substantially:** Because Urgent drivers suffer a heavy waiting penalty ($w=3$) and derive minimal value from holding ($h=1$), Policy $P_1$ dramatically enhances their welfare. At medium demand, Urgent drivers gain $+0.94$ utility points on average per visit (compared to $+0.03$ for Flexible drivers).
- **Flexible Drivers Experience a Tradeoff:** Flexible drivers value holding at $h=2$. Under Policy $P_0$, they actively held stalls without financial penalty. Under $P_1$, their parking convenience is curtailed. Under low demand where chargers are rarely constrained, Flexible drivers' utility drops slightly (from $27.26$ to $26.27$) because queue delays were already minimal and the lost parking option value is not fully offset.

### 4.3 Finding 3: The Limit Experiment (When the Fee Fails)
In our 10 controlled **limit runs**, all 40 drivers were programmatically locked into the `Hold` heuristic regardless of pricing.
- At medium demand, both Policy $P_0$ and Policy $P_1$ produced **identical queue dynamics**:
  - Average waiting under $P_0$: **$3.215$ slots**.
  - Average waiting under $P_1$: **$3.215$ slots** (difference $= 0.000$).
  - Fully served share: **$54.0\%$** under both policies.
  - Delivered energy: **$12,183.6\text{ kWh}$** under both policies.
- However, net average driver utility under $P_1$ plummeted from $15.58$ to **$14.13$** points purely due to the unmitigated accumulation of $F \times \text{idle}$ fines.
- **Core Insight:** *A financial penalty mechanism only works to the extent that market participants are price-elastic.* If drivers face structural constraints (e.g. inability to leave a workplace meeting) that prevent vehicle relocation, idle fees act purely as a punitive deadweight tax without relieving queue congestion.

---

## 5. Evolutionary Dynamics of Norm Adoption

To investigate how driver behavioral norms evolve over generational timescales, we analyzed single-population replicator dynamics (`src/game_theory/evolutionary.py`):
$$x_{t+1} = x_t + \eta \, x_t(1 - x_t) [f_C(x_t) - f_H(x_t)]$$
where $\eta = 0.05$, $f_C(x) = 4x$, and $f_H(x) = (6 - F)x + (1 - F)(1 - x)$.

```
   Cooperation Share x(t) over 30 Updates:
   1.0 |                              ============ F = 2 (Cooperation Attractor)
   0.8 |                      ........
   0.6 |             .........
   0.5 | * Initial x0 = 0.50
   0.4 |             .........
   0.2 |                      ........
   0.0 |                              ============ F = 0 (Defection Attractor)
       +-----------------------------------------
         t=0           t=10          t=20        t=30
```

- **Under $F = 0$ ($P_0$):** $f_C - f_H = -1 - x < 0$ for all $x \in (0, 1)$. The first update steps from $x_0 = 0.50$ to $x_1 = 0.48125$, and the population rapidly converges to $x^* = 0$ (universal defection/holding).
- **Under $F = 2$ ($P_1$):** $f_C - f_H = 1 - x > 0$ for all $x \in (0, 1)$. The first update steps from $x_0 = 0.50$ to $x_1 = 0.50625$, steadily converging toward $x^* = 1$ (universal cooperation).
- This confirms that an idle fee of $F \ge 2$ transforms cooperation from an unstable state into an **Evolutionarily Stable Strategy (ESS)**.

---

## 6. Limitations of the Study

1. **Synthetic Data and Behavioral Assumptions:** Driver requests, arrival distributions, and type priors were generated synthetically. Real-world arrival patterns exhibit non-stationary morning and evening peaking that may amplify queue bottlenecks.
2. **Deterministic Heuristics:** Driver strategies were modeled as static programmed heuristics rather than dynamic stochastic reinforcement learners.
3. **Small Sample Size:** While five independent random seeds demonstrate clear statistical consistency across demand levels, five seeds do not constitute a formal statistical proof of universal performance.
4. **Binary Relocation Decision:** In reality, drivers can relocate vehicles to nearby non-charging stalls. The absence of secondary parking capacity in the model may overestimate holding durations.

---

## 7. Conclusion and Policy Recommendations

This investigation demonstrates that overstaying at shared EV chargers constitutes a classic tragedy of the commons that market forces alone cannot resolve. An idle fee of $F = 2$ points/slot successfully aligns private incentives with collective welfare, reducing queue delays, expanding total energy throughput by up to $614\text{ kWh}$, and establishing a sustainable evolutionary basin of cooperation. 

However, operators must exercise caution: idle fees are effective only when drivers possess the operational elasticity to move their vehicles. For captive commuters unable to relocate vehicles during peak hours, pricing penalties must be coupled with automated valet services, reserved charging windows, or progressive grace periods to prevent inequitable deadweight penalties.
