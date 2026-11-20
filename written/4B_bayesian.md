# 4B Bayesian Game

## 1. Game Formulation and Private Types

### Setting
Consider two drivers, Player 1 and Player 2, randomly matched at a shared charging point.
- Each player is privately assigned a type $\theta_i \in \{\text{Urgent}, \text{Flexible}\}$.
- Prior distribution:
  $$\pi(\text{Urgent}) = 0.30, \quad \pi(\text{Flexible}) = 0.70$$
- Drivers know their own type, but only hold the prior belief regarding their opponent's type.
- Actions available to each driver: Cooperate/Release ($C$) or Hold ($H$).

### Payoff Adjustments under Teaching Fee $F = 1.5$
Starting from the Section 3 baseline table:
- Base matrix: $CC = (4, 4)$, $CH = (0, 6)$, $HC = (6, 0)$, $HH = (1, 1)$.
- If a player plays $C$: base payoffs remain unchanged.
- If a player plays $H$: 
  - Subtract idle fee $F = 1.5$.
  - Add type-specific private holding benefit:
    - **Urgent type:** benefit $= 0$ (net adjustment to own $H$ payoff: $-1.5$).
    - **Flexible type:** benefit $= +1$ (net adjustment to own $H$ payoff: $-1.5 + 1.0 = -0.5$).

### Effective Payoffs for Own Action vs. Opponent's Action

#### For an Urgent Player:
- Playing $C$ vs. opponent $C$: $4$
- Playing $C$ vs. opponent $H$: $0$
- Playing $H$ vs. opponent $C$: $6 - 1.5 = \mathbf{4.5}$
- Playing $H$ vs. opponent $H$: $1 - 1.5 = \mathbf{-0.5}$

#### For a Flexible Player:
- Playing $C$ vs. opponent $C$: $4$
- Playing $C$ vs. opponent $H$: $0$
- Playing $H$ vs. opponent $C$: $6 - 1.5 + 1.0 = \mathbf{5.5}$
- Playing $H$ vs. opponent $H$: $1 - 1.5 + 1.0 = \mathbf{0.5}$

---

## 2. Testing the Proposed Plan

**Proposed Strategy Profile $s^*$:**
$$\text{Urgent drivers choose } C, \quad \text{Flexible drivers choose } H$$

Since the game is symmetric, each player faces an opponent whose action is:
- $C$ with probability $\pi(\text{Urgent}) = 0.30$
- $H$ with probability $\pi(\text{Flexible}) = 0.70$

---

## 3. The Four Expected-Payoff Calculations

### Calculation 1: Urgent Player Choosing $C$ (Prescribed Action)
$$E[U \mid \text{Urgent}, C] = 0.30 \times u_{\text{Urgent}}(C, C) + 0.70 \times u_{\text{Urgent}}(C, H)$$
$$E[U \mid \text{Urgent}, C] = 0.30 \times 4 + 0.70 \times 0 = 1.20 + 0 = \mathbf{1.20}$$
*(This exactly matches the starter verification check provided in the project brief).*

### Calculation 2: Urgent Player Choosing $H$ (Deviation)
$$E[U \mid \text{Urgent}, H] = 0.30 \times u_{\text{Urgent}}(H, C) + 0.70 \times u_{\text{Urgent}}(H, H)$$
$$E[U \mid \text{Urgent}, H] = 0.30 \times 4.5 + 0.70 \times (-0.5) = 1.35 - 0.35 = \mathbf{1.00}$$

**Comparison for Urgent Type:**
$$E[U \mid \text{Urgent}, C] = 1.20 > 1.00 = E[U \mid \text{Urgent}, H]$$
The Urgent type strictly prefers $C$ over $H$. There is **no incentive for an Urgent driver to deviate**.

---

### Calculation 3: Flexible Player Choosing $H$ (Prescribed Action)
$$E[U \mid \text{Flexible}, H] = 0.30 \times u_{\text{Flexible}}(H, C) + 0.70 \times u_{\text{Flexible}}(H, H)$$
$$E[U \mid \text{Flexible}, H] = 0.30 \times 5.5 + 0.70 \times 0.5 = 1.65 + 0.35 = \mathbf{2.00}$$

### Calculation 4: Flexible Player Choosing $C$ (Deviation)
$$E[U \mid \text{Flexible}, C] = 0.30 \times u_{\text{Flexible}}(C, C) + 0.70 \times u_{\text{Flexible}}(C, H)$$
$$E[U \mid \text{Flexible}, C] = 0.30 \times 4 + 0.70 \times 0 = 1.20 + 0 = \mathbf{1.20}$$

**Comparison for Flexible Type:**
$$E[U \mid \text{Flexible}, H] = 2.00 > 1.20 = E[U \mid \text{Flexible}, C]$$
The Flexible type strictly prefers $H$ over $C$. There is **no incentive for a Flexible driver to deviate**.

---

## 4. Equilibrium Conclusion

| Player Type | Action Evaluated | Expected Payoff | Optimal Choice? |
| :---: | :---: | :---: | :---: |
| **Urgent** | **$C$ (Prescribed)** | **$1.20$** | **Yes** ($1.20 > 1.00$) |
| Urgent | $H$ (Deviation) | $1.00$ | No |
| **Flexible** | **$H$ (Prescribed)** | **$2.00$** | **Yes** ($2.00 > 1.20$) |
| Flexible | $C$ (Deviation) | $1.20$ | No |

### Conclusion:
Because neither type of either player can strictly improve their expected payoff by unilaterally altering their choice, the proposed strategy profile:
$$s^* = (\text{Urgent} \to C, \; \text{Flexible} \to H)$$
is a strict **Bayesian Nash Equilibrium (BNE)**.

### Economic and Policy Interpretation
The teaching penalty $F = 1.5$ effectively screens types:
- It raises the cost of holding enough to discourage Urgent drivers (who gain no private idle surplus) from blocking the charger, inducing them to cooperate.
- It is low enough that Flexible drivers (who value parking convenience at $+1.0$) are willing to absorb the net fee ($-0.5$) to retain the charging stall.
- The fee functions as an effective **Pigouvian mechanism**, decentralizing efficient charger allocation based on private valuation of time versus convenience.
