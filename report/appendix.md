# Appendix: Technical Calculations and Game Trees

---

## Appendix A: Extensive Form Trees and Information Partitions

### A.1 Sequential Game with Observable Moves (Section 3A)
```
                          Player 1 (Root)
                         /              \
                     C  /                \  H
                       /                  \
                 Player 2                Player 2
                  /    \                  /    \
              C  /      \  H          C  /      \  H
                /        \              /        \
             (4, 4)     (0, 6)       (6, 0)     (1, 1)
```
- Subgame after $C$: $P_2$ chooses $H$ ($6 > 4$). Continuation payoff to $P_1 = 0$.
- Subgame after $H$: $P_2$ chooses $H$ ($1 > 0$). Continuation payoff to $P_1 = 1$.
- Root decision: $P_1$ compares $0$ (if $C$) vs. $1$ (if $H$). $P_1$ chooses $H$.
- **Subgame Perfect Equilibrium:** $(H, (C \to H, H \to H))$. SPE Outcome: $(1, 1)$.

---

### A.2 Sequential Game with Hidden Move (Section 3A)
```
                          Player 1 (Root)
                         /              \
                     C  /                \  H
                       /                  \
                 Player 2 ............... Player 2  <-- Single Information Set h2
                  /    \                  /    \
              C  /      \  H          C  /      \  H
                /        \              /        \
             (4, 4)     (0, 6)       (6, 0)     (1, 1)
```
- Because $P_2$ cannot distinguish between the left and right decision nodes, $P_2$ must choose a single action $C$ or $H$.
- Strategically equivalent to normal form matrix; dominant strategy for both is $H \implies (1, 1)$.

---

## Appendix B: Memory Tree Payoff Matrix and Derivations (Section 3B)

Terminal payoffs from `data/starter/memory_tree.csv`:

```
                         P1 (Root)
                       /           \
                   L  /             \  R
                     /               \
                   P2                 P2
                  /  \               /  \
               L /    \ R         L /    \ R
                /      \           /      \
              P1        P1       P1        P1
             /  \      /  \     /  \      /  \
            L    R    L    R   L    R    L    R
          (2,1)(3,0)(1,2)(4,1)(0,3)(2,2)(3,1)(1,0)
```

### Full Information Backward Induction Table:
1. Node $LL$: $P_1$ chooses $R \implies u = (3, 0)$
2. Node $LR$: $P_1$ chooses $R \implies u = (4, 1)$
3. Node $RL$: $P_1$ chooses $R \implies u = (2, 2)$
4. Node $RR$: $P_1$ chooses $L \implies u = (3, 1)$
5. Node $L$ ($P_2$): compares $0$ (at $LL$) vs. $1$ (at $LR$) $\implies$ chooses $R \implies (4, 1)$
6. Node $R$ ($P_2$): compares $2$ (at $RL$) vs. $1$ (at $RR$) $\implies$ chooses $L \implies (2, 2)$
7. Root ($P_1$): compares $4$ (via $L \to R \to R$) vs. $2$ (via $R \to L \to R$) $\implies$ chooses $L$.
- Path: $LRR \implies$ Payoff $(4, 1)$.

---

## Appendix C: Derivation of the Replicator Dynamics Equation (Section 5A)

Let $x$ denote the share of the population playing $C$, and $1-x$ play $H$.
Average fitness payoffs:
$$f_C(x) = 4x + 0(1-x) = 4x$$
$$f_H(x) = (6 - F)x + (1 - F)(1 - x) = (5x + 1) - F$$

Fitness differential $\Delta f(x) = f_C(x) - f_H(x)$:
$$\Delta f(x) = 4x - [(6 - F)x + (1 - F)(1 - x)] = F - 1 - x$$

Discrete replicator adjustment formula:
$$x_{t+1} = x_t + \eta \, x_t(1 - x_t) [f_C(x_t) - f_H(x_t)], \quad \eta = 0.05$$

### Step-by-Step Hand Check for Step 1 ($x_0 = 0.5, F = 0$):
- $f_C(0.5) = 4(0.5) = 2.00$
- $f_H(0.5) = 6(0.5) + 1(0.5) = 3.0 + 0.5 = 3.50$
- $f_C - f_H = 2.0 - 3.5 = -1.50$
- $x_0(1 - x_0) = 0.5 \times 0.5 = 0.25$
- Adjustment: $0.05 \times 0.25 \times (-1.50) = 0.0125 \times (-1.50) = -0.01875$
- $x_1 = 0.50 - 0.01875 = \mathbf{0.48125}$ *(exact reproduction verified)*.

---

## Appendix D: 3-Driver Mini Case Verification

Deterministic trace with 1 charger, 16 slots:
- Driver $A$: Flexible ($v=2, w=1, h=2$), arrives 0, departs 16, requests $6\text{ kWh}$ ($2$ slots).
- Driver $B$: Urgent ($v=3, w=3, h=1$), arrives 0, departs 16, requests $3\text{ kWh}$ ($1$ slot).
- Driver $C$: Flexible ($v=2, w=1, h=2$), arrives 1, departs 16, requests $6\text{ kWh}$ ($2$ slots).

| Metric | Scenario 1: All Release | Scenario 2: $A$ Holds 1 Slot |
| :--- | :---: | :---: |
| Start times $(A, B, C)$ | $(0, 2, 3)$ | $(0, 3, 4)$ |
| Completion times | $(2, 3, 5)$ | $(2, 4, 6)$ |
| Wait slots $(A, B, C)$ | $(0, 2, 2)$ | $(0, 3, 3)$ |
| Total Waiting Slots | **4** | **6** |
| Total Delivered Energy | **15.0 kWh** | **15.0 kWh** |
| $A$ Utility | $2(6) - 1(0) + 2(0) = \mathbf{12}$ | $2(6) - 1(0) + 2(1) = \mathbf{14}$ |
| $B$ Utility | $3(3) - 3(2) + 1(0) = \mathbf{3}$ | $3(3) - 3(3) + 1(0) = \mathbf{0}$ |
| $C$ Utility | $2(6) - 1(2) + 2(0) = \mathbf{10}$ | $2(6) - 1(3) + 2(0) = \mathbf{9}$ |
| **Total System Utility** | **25.0** | **23.0** |
