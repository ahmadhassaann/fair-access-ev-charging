# 3B Memory Trees (`memory_tree.csv`)

## Tree Structure and Payoffs
The game follows a three-stage sequence:
1. $P_1$ chooses between Left ($L$) and Right ($R$).
2. $P_2$ chooses between Left ($L$) and Right ($R$).
3. $P_1$ moves again, choosing between Left ($L$) and Right ($R$).

The terminal payoffs $(u_1, u_2)$ recorded in `data/starter/memory_tree.csv` are:

| History | $P_1$ Stage 1 | $P_2$ Stage 2 | $P_1$ Stage 3 | Terminal Payoff $(u_1, u_2)$ |
| :--- | :---: | :---: | :---: | :---: |
| $h_1$ | $L$ | $L$ | $L$ | $(2, 1)$ |
| $h_2$ | $L$ | $L$ | $R$ | $(3, 0)$ |
| $h_3$ | $L$ | $R$ | $L$ | $(1, 2)$ |
| $h_4$ | $L$ | $R$ | $R$ | $(4, 1)$ |
| $h_5$ | $R$ | $L$ | $L$ | $(0, 3)$ |
| $h_6$ | $R$ | $L$ | $R$ | $(2, 2)$ |
| $h_7$ | $R$ | $R$ | $L$ | $(3, 1)$ |
| $h_8$ | $R$ | $R$ | $R$ | $(1, 0)$ |

---

## Setting 1: Full Information (All Nodes Separate)

In this baseline setting, every decision node is in its own singleton information set. Both players observe all previous moves.

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

### Backward Induction Solution
1. **Stage 3 ($P_1$'s final choice at 4 distinct nodes):**
   - After $(L, L)$: $P_1$ compares $L \to 2$ vs. $R \to 3$. Chooses **$R$** (payoff $(3, 0)$).
   - After $(L, R)$: $P_1$ compares $L \to 1$ vs. $R \to 4$. Chooses **$R$** (payoff $(4, 1)$).
   - After $(R, L)$: $P_1$ compares $L \to 0$ vs. $R \to 2$. Chooses **$R$** (payoff $(2, 2)$).
   - After $(R, R)$: $P_1$ compares $L \to 3$ vs. $R \to 1$. Chooses **$L$** (payoff $(3, 1)$).

2. **Stage 2 ($P_2$'s choice at 2 distinct nodes):**
   - At node $L$: $P_2$ evaluates $L \implies (3, 0)$ (payoff 0) vs. $R \implies (4, 1)$ (payoff 1). Chooses **$R$** ($1 > 0$).
   - At node $R$: $P_2$ evaluates $L \implies (2, 2)$ (payoff 2) vs. $R \implies (3, 1)$ (payoff 1). Chooses **$L$** ($2 > 1$).

3. **Stage 1 ($P_1$ at the root):**
   - Choosing $L$ leads to $P_2=R$, $P_1=R \implies u_1 = 4$.
   - Choosing $R$ leads to $P_2=L$, $P_1=R \implies u_1 = 2$.
   - Since $4 > 2$, $P_1$ chooses **$L$**.

- **Backward Induction Path:** $L \to R \to R$ (History $LRR$).
- **Equilibrium Payoffs:** **$(4, 1)$**.

---

## Setting 2: Forget Own First Action

### Information Partition
- $P_1$ knows it is at Stage 3 and observes $P_2$'s action ($L$ or $R$).
- However, $P_1$ has forgotten whether its own first action was $L$ or $R$.
- Node grouping:
  - Root: Singleton $\{n_{\text{root}}\}$.
  - $P_2$'s nodes: $\{n_L\}, \{n_R\}$ are separate.
  - Final nodes after $P_2 = L$: $\{ (L, L), (R, L) \}$ are joined into information set $I_{1, L}$.
  - Final nodes after $P_2 = R$: $\{ (L, R), (R, R) \}$ are joined into information set $I_{1, R}$.

```
                         P1 (Root)
                       /           \
                   L  /             \  R
                     /               \
                   P2                 P2
                  /  \               /  \
               L /    \ R         L /    \ R
                /      \           /      \
              P1        P1.......P1        P1
             /  \      /  \     /  \      /  \
            L    R    L    R   L    R    L    R
            [-- I_{1,L} --]     [-- I_{1,R} --]
```

### Analysis of $P_1$'s Knowledge
At $I_{1, L}$, $P_1$ knows:
- $P_2$ chose $L$.
- The current stage is Stage 3.
- But $P_1$ cannot distinguish whether it previously chose $L$ (leading to terminal payoffs $(2,1)$ or $(3,0)$) or $R$ (leading to terminal payoffs $(0,3)$ or $(2,2)$).
$P_1$ must choose a single action across the information set. Choosing $R$ gives 3 if past was $L$ and 2 if past was $R$, which strictly dominates choosing $L$ (giving 2 if past was $L$ and 0 if past was $R$).

---

## Setting 3: Forget the Stage (Absentminded Driver)

### Information Partition
- $P_1$ sees no clock, no turn counter, no record of past moves, and does not observe $P_2$'s action.
- All five nodes belonging to $P_1$ are merged into a single information set:
  $$I_1 = \{ n_{\text{root}}, (L, L), (L, R), (R, L), (R, R) \}$$
- $P_2$ still has separate information sets observing $P_1$'s first move.

```
                         P1 (Root)  <---------------+
                       /           \                |
                   L  /             \  R            |
                     /               \              |
                   P2                 P2            |
                  /  \               /  \           |
               L /    \ R         L /    \ R        |
                /      \           /      \         |
              P1........P1..........P1.....P1 ------+
             /  \      /  \        /  \   /  \      (All P1 nodes in one Info Set)
```

### Analysis of $P_1$'s Knowledge
- $P_1$ knows only that it is called upon to move between $L$ and $R$.
- It cannot determine whether it is opening the session or playing the second move.
- This is an instance of **imperfect recall** (similar to the famous Absentminded Driver paradox of Piccione and Rubinstein, 1997).
- $P_1$ cannot condition its second action on having already played once; any stationary behavioral strategy must apply the identical probability distribution at all five decision points.
