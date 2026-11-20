# Project Proposal: Fair Access to Shared EV Chargers

**Course:** Game Theory  
**Project Track:** Four-Week Semester Project  
**Team Scope:** Up to 4 Members  

---

## 1. Problem Statement & Research Question
As electric vehicle (EV) adoption accelerates, commercial and workplace charging depots face acute access bottlenecks. A recurring inefficiency arises when a driver completes their required energy replenishment but leaves their vehicle plugged in ("holding" the stall) to avoid the inconvenience of relocating the car. Subsequent drivers arriving at the facility are forced to wait in a queue, wasting productive time and reducing station throughput. Commercial charging operators (such as Electrify America) implement **idle fees** to penalize overstaying.

**Central Research Question:**  
*Does an idle penalty reduce waiting times, and how does it differentially affect drivers with heterogeneous private urgency and flexibility needs?*

---

## 2. Game-Theoretic Framework & Model Formulation

### A. Stage Game Abstraction
We model the interaction between consecutive charging drivers as a strategic normal-form game. Each driver chooses between **Cooperate ($C$)** (releasing immediately upon charge completion) and **Hold ($H$)** (retaining the charger for an idle slot).
Under no penalty ($P_0$), the game exhibits a Prisoner's Dilemma structure:
- Mutual cooperation $(C, C)$ yields high joint welfare $(4, 4)$.
- Holding yields private convenience ($6$ if opponent releases, $1$ if both hold).
- $(H, H)$ is the unique dominant-strategy Nash equilibrium, causing deadweight loss.

Under idle penalty policy ($P_1$), an idle fee $F=2$ points per slot internalizes the externality, shifting the best-response structure toward $(C, C)$.

### B. Extended Game Theory Analyses Planned
1. **Extensive Form & Information Sets (Section 3):**
   - Sequential moves with observable vs. hidden actions (backward induction vs. information sets under perfect recall).
   - Memory trees evaluating full recall vs. forgotten first actions vs. forgotten stage (absentmindedness).
   - Comparison of mixed commitment lotteries vs. fresh behavioral draws (Kuhn's theorem).
2. **Repeated Games (Section 4A):**
   - Finite horizon ($T=3$) backward induction unraveling.
   - Infinite horizon grim trigger cooperation with discount factor threshold $\delta^* = 2/5 = 0.40$.
3. **Bayesian Games with Incomplete Information (Section 4B):**
   - Prior distribution $\pi(\text{Urgent}) = 0.30, \pi(\text{Flexible}) = 0.70$.
   - Screening mechanism under fee $F=1.5$ testing Bayesian Nash Equilibrium $(\text{Urgent} \to C, \text{Flexible} \to H)$.
4. **Evolutionary Game Dynamics (Section 5A):**
   - Replicator dynamics over 30 updates comparing convergence under $F=0$ (defection attractor) vs. $F=2$ (cooperation attractor).

---

## 3. Simulator Architecture & Experimental Plan

### A. Discrete-Event Queue Simulator
- **Facility:** 1 charging site with $M=6$ identical $6\text{ kW}$ Level-2 chargers.
- **Horizon:** 16 half-hour slots per day ($08:00 - 16:00$), covering 60 simulated days per run.
- **Energy Transfer:** Up to $3\text{ kWh}$ per full slot.
- **Driver Pool:** 40 heterogeneous drivers categorized into:
  - **Urgent:** Value $v=3/\text{kWh}$, waiting cost $w=3/\text{slot}$, idle benefit $h=1/\text{slot}$.
  - **Flexible:** Value $v=2/\text{kWh}$, waiting cost $w=1/\text{slot}$, idle benefit $h=2/\text{slot}$.
- **Driver Rules:** Release, Hold (up to 2 slots), Reciprocal (tit-for-tat based on prior service delay), and Fee Aware (optimizing net surplus $(h-F)O$).

### B. Experimental Matrix
- **Policies:** $P_0$ ($F=0$) vs. $P_1$ ($F=2$).
- **Demand Levels:** Low (720 requests), Medium (1,440 requests), High (2,160 requests).
- **Random Seeds:** 5 independent replications (Seeds $0, 1, 2, 3, 4$).
- **Total Executions:** 30 main runs ($2 \times 3 \times 5$) + 10 limit runs (all drivers fixed to Hold at medium demand).

---

## 4. Checkpoints & Quality Verification Plan
1. **Checkpoint 1 (Week 1):** Proposal sign-off, schema validation, synthetic data generation.
2. **Checkpoint 2 (Week 2):** Simulator engine verified against deterministic 3-driver mini case ($4/15/25$ and $6/15/23$).
3. **Checkpoint 3 (Week 3):** Full batch execution across 40 runs, invariant tests (no double booking, energy timing), evolutionary plot.
4. **Checkpoint 4 (Week 4):** Streamlit interactive dashboard, 6–8 page academic report, viva demo.
