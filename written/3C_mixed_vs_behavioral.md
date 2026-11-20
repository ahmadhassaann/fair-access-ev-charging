# 3C Mixed vs. Behavioral Strategies

## 1. Setup and Payoffs
Player 1 ($P_1$) moves in two successive stages. Player 2 ($P_2$) is fixed to action $L$ in all circumstances.

Player 1's action sequences and resulting terminal payoffs:

| $P_1$ Action Pair | Terminal Payoff to $P_1$ |
| :---: | :---: |
| $LL$ | $1$ |
| $LR$ | $8$ |
| $RL$ | $6$ |
| $RR$ | $2$ |

---

## 2. Mixed Strategy Lottery vs. Fresh Behavioral Draws

### A. Mixed Strategy (Commitment Lottery Drawn Upfront)
A pure strategy for $P_1$ is a complete plan of action specifying what to do at both stages. The pure strategies are $s_{LL}, s_{LR}, s_{RL}, s_{RR}$.

Consider a **50–50 mixed strategy** between playing always $L$ ($s_{LL}$) and always $R$ ($s_{RR}$):
$$\sigma = 0.5 \cdot s_{LL} + 0.5 \cdot s_{RR}$$

- The random draw occurs once before the game begins.
- Outcome $LL$ occurs with probability $0.5$.
- Outcome $RR$ occurs with probability $0.5$.
- Outcomes $LR$ and $RL$ occur with probability $0$.

**Expected Payoff:**
$$E[U_{\text{mixed}}] = 0.5 \times u_1(LL) + 0.5 \times u_1(RR) = 0.5 \times 1 + 0.5 \times 2 = 0.5 + 1.0 = \mathbf{1.50}$$

---

### B. Fresh Draws at Each Visit (Behavioral Strategy with Forgotten Stage)
Suppose $P_1$ cannot distinguish stage 1 from stage 2 (as in Section 3B, Setting 3 where the stage is forgotten). $P_1$ must randomize independently with $50\%$ on $L$ and $50\%$ on $R$ at every visit.

Because the two decisions are independent:
- $\Pr(LL) = 0.5 \times 0.5 = 0.25$
- $\Pr(LR) = 0.5 \times 0.5 = 0.25$
- $\Pr(RL) = 0.5 \times 0.5 = 0.25$
- $\Pr(RR) = 0.5 \times 0.5 = 0.25$

**Expected Payoff:**
$$E[U_{\text{behavioral}}] = 0.25 \times 1 + 0.25 \times 8 + 0.25 \times 6 + 0.25 \times 2$$
$$E[U_{\text{behavioral}}] = 0.25 \times (1 + 8 + 6 + 2) = 0.25 \times 17 = \mathbf{4.25}$$

### Key Comparison
$$E[U_{\text{behavioral}}] = 4.25 > 1.50 = E[U_{\text{mixed}}]$$
The fresh independent draws dramatically outperform the mixed lottery because they reach the high-payoff off-diagonal outcomes $LR$ ($8$) and $RL$ ($6$). The mixed lottery correlates decisions across stages, locking $P_1$ into either strictly low-payoff $LL$ ($1$) or $RR$ ($2$).

---

## 3. Kuhn's Theorem and Behavioral Reproduction under Perfect Recall

### Reproduction of Mixed Strategy under Perfect Recall
Under Kuhn's Theorem (1953), in any finite extensive-form game with **perfect recall**, every mixed strategy has an equivalent behavioral strategy that induces the exact same probability distribution over terminal nodes.

To reproduce the mixed lottery $\sigma = 0.5 \cdot s_{LL} + 0.5 \cdot s_{RR}$ behaviorally:
1. **Stage 1:** $P_1$ randomizes: play $L$ with prob $0.5$, play $R$ with prob $0.5$.
2. **Stage 2:** $P_1$ uses its memory of Stage 1:
   - If Stage 1 was $L$: play $L$ with prob $1.0$, play $R$ with prob $0$.
   - If Stage 1 was $R$: play $R$ with prob $1.0$, play $L$ with prob $0$.

**Terminal Probabilities under this Behavioral Strategy:**
- $\Pr(LL) = 0.5 \times 1.0 = 0.5$
- $\Pr(LR) = 0.5 \times 0.0 = 0$
- $\Pr(RL) = 0.5 \times 0.0 = 0$
- $\Pr(RR) = 0.5 \times 1.0 = 0.5$

The resulting expected payoff is exactly:
$$E[U] = 0.5 \times 1 + 0.5 \times 2 = \mathbf{1.50}$$
This matches the mixed strategy lottery distribution and expected payoff identically.

---

## 4. Why the Forgotten-Stage Version Cannot Reproduce the Mixed Strategy
When $P_1$ forgets the stage:
- Both decision nodes belong to the **same information set**.
- A behavioral strategy assigns a single probability distribution $b = (p_L, 1 - p_L)$ to this information set.
- Consequently, the action chosen at Stage 2 is conditionally independent of Stage 1:
  $$\Pr(LL) = p_L^2, \quad \Pr(RR) = (1 - p_L)^2, \quad \Pr(LR) = \Pr(RL) = p_L(1 - p_L)$$
- To achieve $\Pr(LR) = 0$ (as required by the mixed strategy), we would require $p_L(1 - p_L) = 0$, which implies $p_L \in \{0, 1\}$. But if $p_L = 1$, $\Pr(LL) = 1 \ne 0.5$; if $p_L = 0$, $\Pr(RR) = 1 \ne 0.5$.
- Therefore, **no behavioral strategy can reproduce the correlated outcomes of the mixed strategy without memory of past choices**.
- This illustrates the fundamental breakdown of Kuhn's Theorem in games with imperfect recall.
