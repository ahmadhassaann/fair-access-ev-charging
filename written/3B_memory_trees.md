# 3B Memory Trees (`memory_tree.csv`)

## 1. Tree Structure and Terminal Payoffs
The game follows a three-stage sequential sequence:
1. $P_1$ chooses between Left ($L$) and Right ($R$) at the root.
2. $P_2$ observes and chooses between Left ($L$) and Right ($R$).
3. $P_1$ moves again, choosing between Left ($L$) and Right ($R$).

The terminal payoffs $(u_1, u_2)$ recorded in the official `data/starter/memory_tree.csv` are:

| History | $P_1$ Stage 1 | $P_2$ Stage 2 | $P_1$ Stage 3 | Terminal Payoff $(u_1, u_2)$ |
| :--- | :---: | :---: | :---: | :---: |
| $h_1$ | $L$ | $L$ | $L$ | $(1, 3)$ |
| $h_2$ | $L$ | $L$ | $R$ | $(8, 4)$ |
| $h_3$ | $L$ | $R$ | $L$ | $(6, 1)$ |
| $h_4$ | $L$ | $R$ | $R$ | $(0, 2)$ |
| $h_5$ | $R$ | $L$ | $L$ | $(6, 5)$ |
| $h_6$ | $R$ | $L$ | $R$ | $(2, 2)$ |
| $h_7$ | $R$ | $R$ | $L$ | $(3, 4)$ |
| $h_8$ | $R$ | $R$ | $R$ | $(1, 1)$ |

---

## 2. Setting 1: Full Information (All Nodes Separate)

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
          (1,3)(8,4)(6,1)(0,2)(6,5)(2,2)(3,4)(1,1)
```

### Backward Induction Solution
1. **Stage 3 ($P_1$'s final choice at 4 distinct nodes):**
   - After $(L, L)$: $P_1$ compares $L \to 1$ vs. $R \to 8$. Chooses **$R$** (payoff $(8, 4)$).
   - After $(L, R)$: $P_1$ compares $L \to 6$ vs. $R \to 0$. Chooses **$L$** (payoff $(6, 1)$).
   - After $(R, L)$: $P_1$ compares $L \to 6$ vs. $R \to 2$. Chooses **$L$** (payoff $(6, 5)$).
   - After $(R, R)$: $P_1$ compares $L \to 3$ vs. $R \to 1$. Chooses **$L$** (payoff $(3, 4)$).

2. **Stage 2 ($P_2$'s choice at 2 distinct nodes):**
   - At node $L$: $P_2$ evaluates $L \implies (8, 4)$ (payoff 4) vs. $R \implies (6, 1)$ (payoff 1). Chooses **$L$** ($4 > 1$).
   - At node $R$: $P_2$ evaluates $L \implies (6, 5)$ (payoff 5) vs. $R \implies (3, 4)$ (payoff 4). Chooses **$L$** ($5 > 4$).

3. **Stage 1 ($P_1$ at the root):**
   - Choosing $L$ leads to $P_2=L$, $P_1=R \implies u_1 = 8$.
   - Choosing $R$ leads to $P_2=L$, $P_1=L \implies u_1 = 6$.
   - Since $8 > 6$, $P_1$ chooses **$L$**.

- **Backward Induction Path:** $L \to L \to R$ (History $LLR$).
- **Equilibrium Payoffs:** **$(8, 4)$** ($P_1$ earns $8$, $P_2$ earns $4$).

---

## 3. Setting 2: Forget Own First Action

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
- But $P_1$ cannot distinguish whether it previously chose $L$ (terminal payoffs $(1,3)$ or $(8,4)$) or $R$ (terminal payoffs $(6,5)$ or $(2,2)$).
- A single action across $I_{1, L}$ must be selected based on $P_1$'s beliefs about its own initial move.

At $I_{1, R}$, $P_1$ knows:
- $P_2$ chose $R$.
- Payoffs for choosing $L$: $6$ if past was $L$, $3$ if past was $R$.
- Payoffs for choosing $R$: $0$ if past was $L$, $1$ if past was $R$.
- Notice that choosing $L$ strictly dominates choosing $R$ regardless of belief ($6 > 0$ and $3 > 1$).

---

## 4. Setting 3: Forget the Stage (Absentminded Driver)

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
- It cannot determine whether it is opening the session or making the second move.
- This is an instance of **imperfect recall** (as in Piccione & Rubinstein, 1997).
- If $P_2$ is fixed to $L$, $P_1$ faces a choice between a mixed commitment lottery ($E=1.50$) and independent behavioral draws ($E=4.25$, as detailed in Section 3C).
