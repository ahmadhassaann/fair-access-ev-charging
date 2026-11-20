# 4A Repeated Games

## 1. Stage Game and Assumptions
We analyze the repeated interaction between two drivers using the Section 3 baseline payoff matrix under Policy $P_0$ (no idle fee):

| $P_1$ \ $P_2$ | Cooperate ($C$) | Hold ($H$) |
| :---: | :---: | :---: |
| **Cooperate ($C$)** | $(4, 4)$ | $(0, 6)$ |
| **Hold ($H$)** | $(6, 0)$ | $(1, 1)$ |

- In each period $t$, players simultaneously choose an action from $\{C, H\}$.
- At the end of each round, both players observe the realized action pair.
- Let $\delta \in [0, 1)$ denote the common discount factor, representing the weight placed on payoffs received one round later.

---

## 2. Finitely Repeated Game ($T = 3$ Rounds)

Consider repeating the game for exactly $T = 3$ known rounds.

### Backward Induction Analysis
1. **Round 3 (Final Round):**
   - There is no future round to punish defection or reward cooperation.
   - The game is strategically identical to the one-shot stage game.
   - For both players, $H$ strictly dominates $C$ ($6 > 4$ and $1 > 0$).
   - The unique Nash equilibrium in Round 3 is $(H, H)$ with payoffs $(1, 1)$.

2. **Round 2:**
   - Both players know that regardless of the action profile in Round 2, the outcome in Round 3 is fixed at $(H, H)$ with payoff $1$.
   - The continuation payoff cannot be conditioned on Round 2 behavior.
   - Round 2 reduces to the static stage game.
   - The unique equilibrium is $(H, H)$ with payoffs $(1, 1)$.

3. **Round 1:**
   - By identical logic, continuation payoffs are predetermined.
   - Unique equilibrium is $(H, H)$ with payoffs $(1, 1)$.

### Conclusion for Finite Horizon
- The unique subgame perfect equilibrium dictates that both players choose **Hold ($H$) in all three rounds**.
- Total undiscounted payoff: $3 \times 1 = \mathbf{3}$ per player.
- Undiscounted joint welfare: $6$ (compared to potential cooperative total of $24$).
- Cooperation cannot be sustained in any round of a finitely repeated game with a unique stage Nash equilibrium.

---

## 3. Infinitely Repeated Game with Discounting

### Grim Trigger Strategy
Each player adopts the following trigger strategy:
- Start by playing $C$ in round $t = 0$.
- In round $t \ge 1$, play $C$ if all past outcomes were $(C, C)$.
- If either player ever played $H$ in any prior round, play $H$ in every subsequent round forever.

### Payoff Derivations
1. **Payoff from Cooperating Forever:**
   Both players play $C$ in every period $t = 0, 1, 2, \dots$:
   $$V_{\text{coop}} = 4 + 4\delta + 4\delta^2 + 4\delta^3 + \dots = \sum_{t=0}^{\infty} 4\delta^t = \frac{4}{1 - \delta}$$

2. **Payoff from Deviating to $H$ at $t = 0$:**
   Suppose Player 1 deviates by playing $H$ at $t = 0$ while Player 2 plays $C$.
   - In period 0, Player 1 earns the defection payoff $6$.
   - In period $t \ge 1$, Player 2 triggers permanent punishment, playing $H$ forever.
   - Player 1's best response against $H$ is $H$, earning $1$ per period from $t = 1$ onwards:
   $$V_{\text{dev}} = 6 + 1\cdot\delta + 1\cdot\delta^2 + 1\cdot\delta^3 + \dots = 6 + \frac{\delta}{1 - \delta}$$

### Discount Factor Threshold Derivation
Cooperation is sustainable in a Subgame Perfect Equilibrium (SPE) if and only if no player has an incentive to deviate:
$$V_{\text{coop}} \ge V_{\text{dev}}$$
$$\frac{4}{1 - \delta} \ge 6 + \frac{\delta}{1 - \delta}$$
Subtracting $\frac{\delta}{1 - \delta}$ from both sides:
$$\frac{4 - \delta}{1 - \delta} \ge 6$$
Since $\delta < 1$, multiply both sides by $(1 - \delta)$:
$$4 - \delta \ge 6(1 - \delta)$$
$$4 - \delta \ge 6 - 6\delta$$
$$5\delta \ge 2 \implies \mathbf{\delta \ge \frac{2}{5} = 0.40}$$

---

## 4. Evaluation at Specific Discount Factors

### Case 1: Low Patience ($\delta = 0.2 < 0.4$)
- $V_{\text{coop}} = \frac{4}{1 - 0.2} = \frac{4}{0.8} = \mathbf{5.00}$
- $V_{\text{dev}} = 6 + \frac{0.2}{1 - 0.2} = 6 + \frac{0.2}{0.8} = 6 + 0.25 = \mathbf{6.25}$
- Since $V_{\text{dev}} = 6.25 > 5.00 = V_{\text{coop}}$, drivers place insufficient weight on future retaliation. Defection is profitable; **cooperation cannot be sustained**.

### Case 2: High Patience ($\delta = 0.5 > 0.4$)
- $V_{\text{coop}} = \frac{4}{1 - 0.5} = \frac{4}{0.5} = \mathbf{8.00}$
- $V_{\text{dev}} = 6 + \frac{0.5}{1 - 0.5} = 6 + 1.00 = \mathbf{7.00}$
- Since $V_{\text{coop}} = 8.00 > 7.00 = V_{\text{dev}}$, the long-term benefit of sustained cooperation outweighs the one-shot gain from defecting. **Cooperation is sustainable as an SPE**.

### Credibility of Punishment (Best Response Check)
During the punishment phase, the opponent plays $H$ in every round.
- If the player responds with $C$: immediate payoff is $0$.
- If the player responds with $H$: immediate payoff is $1$.
Since $1 > 0$, $H$ is the stage game best response. Playing $H$ forever yields $\frac{1}{1-\delta}$, which strictly dominates any strategy playing $C$ in any punishment round. Hence, the punishment threats are **credible and subgame perfect**.

---

## 5. Optional Extension: Cooperate Twice, Then Deviate

Consider a player who cooperates in rounds $t = 0$ and $t = 1$, and then deviates to $H$ in round $t = 2$:
$$V_{\text{dev}}^{(2)} = 4 + 4\delta + 6\delta^2 + \sum_{t=3}^{\infty} 1 \cdot \delta^t = 4 + 4\delta + 6\delta^2 + \frac{\delta^3}{1 - \delta}$$

Comparing this with cooperating forever:
$$V_{\text{coop}} - V_{\text{dev}}^{(2)} = \sum_{t=0}^{\infty} 4\delta^t - \left(4 + 4\delta + 6\delta^2 + \frac{\delta^3}{1 - \delta}\right)$$
$$= \delta^2 \left( 4 + 4\delta + 4\delta^2 + \dots \right) - \left( 6\delta^2 + \frac{\delta^3}{1 - \delta} \right)$$
$$= \delta^2 \left[ \frac{4}{1 - \delta} - \left(6 + \frac{\delta}{1 - \delta}\right) \right] = \delta^2 \left[ \frac{4 - \delta - 6(1 - \delta)}{1 - \delta} \right] = \frac{\delta^2 (5\delta - 2)}{1 - \delta}$$

- For $\delta \ge 0.4$, this difference is $\ge 0$, confirming that delaying defection does not generate a profitable deviation.
- The threshold $\delta^* = 0.40$ remains universally binding across all possible deviation periods.
