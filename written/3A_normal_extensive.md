# 3A Normal and Extensive Form Games

## 1. Normal Form Representation and Pure Nash Equilibrium

### Payoff Matrix
Consider two drivers, Player 1 ($P_1$) and Player 2 ($P_2$), sharing an electric vehicle charging station. Each driver can either cooperate by releasing the charger immediately after service is complete ($C$) or hold the charger for an idle slot ($H$).

| $P_1$ \ $P_2$ | $P_2$: Cooperate ($C$) | $P_2$: Hold ($H$) |
| :--- | :---: | :---: |
| **$P_1$: Cooperate ($C$)** | $(4, 4)$ | $(0, 6)$ |
| **$P_1$: Hold ($H$)** | $(6, 0)$ | $(1, 1)$ |

*(Payoffs are given as $(u_1, u_2)$).*

### Best Response Analysis
- **For Player 1:**
  - If $P_2$ plays $C$: $u_1(H, C) = 6 > u_1(C, C) = 4$. Best response is $H$.
  - If $P_2$ plays $H$: $u_1(H, H) = 1 > u_1(C, H) = 0$. Best response is $H$.
  - Therefore, **Hold ($H$) is a strictly dominant strategy** for Player 1.
- **For Player 2:**
  - By symmetry, if $P_1$ plays $C$, $u_2(C, H) = 6 > u_2(C, C) = 4$. Best response is $H$.
  - If $P_1$ plays $H$, $u_2(H, H) = 1 > u_2(H, C) = 0$. Best response is $H$.
  - Therefore, **Hold ($H$) is a strictly dominant strategy** for Player 2.

### Pure Nash Equilibrium vs. Joint Optimum
- **Unique Pure Nash Equilibrium:** $(H, H)$ with payoff vector $(1, 1)$.
- **Social / Joint Optimum:** $(C, C)$ with payoff vector $(4, 4)$ and total welfare $8$.
- **Why they differ:** 
  This game represents a classic **Prisoner's Dilemma**. While mutual cooperation $(C, C)$ Pareto-dominates mutual defection $(H, H)$, individual rationality leads both drivers to defect. When one driver releases, the other driver gains private convenience by holding ($+2$ extra points). If both drivers hold, charging availability is severely restricted and each receives only $1$. Free-riding incentives undermine social efficiency.

---

## 2. Extensive Form: Sequential Moves with Full Information

Suppose $P_1$ moves first, choosing $C$ or $H$. $P_2$ observes $P_1$'s move before making their own choice.

```
                  P1
                /    \
            C  /      \  H
              /        \
            P2          P2
           /  \        /  \
        C /    \ H  C /    \ H
         /      \    /      \
      (4,4)   (0,6)(6,0)   (1,1)
```

### Complete Strategies
- **Player 1 strategy space:** $\{C, H\}$ (2 pure strategies).
- **Player 2 strategy space:** A contingency plan mapping $P_1$'s action to an action in $\{C, H\}$. There are $2^2 = 4$ complete strategies:
  1. $s_2^{(1)} = (C \to C, H \to C)$ [denoted $CC$]
  2. $s_2^{(2)} = (C \to C, H \to H)$ [denoted $CH$]
  3. $s_2^{(3)} = (C \to H, H \to C)$ [denoted $HC$]
  4. $s_2^{(4)} = (C \to H, H \to H)$ [denoted $HH$]

### Backward Induction Solution
1. **At decision node after $P_1 = C$:** $P_2$ compares $u_2(C, C) = 4$ vs. $u_2(C, H) = 6$. Since $6 > 4$, $P_2$ chooses $H$.
2. **At decision node after $P_1 = H$:** $P_2$ compares $u_2(H, C) = 0$ vs. $u_2(H, H) = 1$. Since $1 > 0$, $P_2$ chooses $H$.
3. **Player 1's choice at the root:** Anticipating $P_2$'s choices:
   - If $P_1$ plays $C \implies P_2$ plays $H \implies u_1 = 0$.
   - If $P_1$ plays $H \implies P_2$ plays $H \implies u_1 = 1$.
   - Since $1 > 0$, $P_1$ chooses $H$.

- **Subgame Perfect Equilibrium (SPE):** $(H, s_2^{(4)})$ where $s_2^{(4)} = (C \to H, H \to H)$.
- **Equilibrium Path:** $P_1$ plays $H$, and $P_2$ plays $H$.
- **Equilibrium Payoffs:** $(1, 1)$.

---

## 3. Extensive Form with Hidden Move: Imperfect Information with Perfect Recall

Now assume $P_1$ moves first, but $P_1$'s move is hidden from $P_2$.

```
                  P1
                /    \
            C  /      \  H
              /        \
            P2..........P2   <-- Information Set h_2
           /  \        /  \
        C /    \ H  C /    \ H
         /      \    /      \
      (4,4)   (0,6)(6,0)   (1,1)
```

### Information Sets and Strategic Equivalence
- Because $P_2$ cannot observe whether $P_1$ chose $C$ or $H$, both of $P_2$'s decision nodes belong to a **single information set** $h_2 = \{n_C, n_H\}$.
- $P_2$ must choose a single action ($C$ or $H$) without knowing which node has been reached.
- Strategically, this game is equivalent to the simultaneous normal-form game analyzed in Section 1.

### Why This is Imperfect Information with Perfect Recall
1. **Imperfect Information:** A game has imperfect information whenever at least one information set contains more than one decision node. Here, $h_2$ contains two nodes, so $P_2$ lacks full information about prior history.
2. **Perfect Recall:** A game exhibits perfect recall (as formalized by Kuhn, 1953) if players never forget any information they once knew, nor do they forget their own past actions. 
   - $P_1$ makes only one choice.
   - $P_2$ never knew $P_1$'s move, so $P_2$ has not "forgotten" anything.
   - All information sets of both players are compatible with their own memory of past actions and knowledge.
   - Hence, this is a standard game of **imperfect information with perfect recall**.
