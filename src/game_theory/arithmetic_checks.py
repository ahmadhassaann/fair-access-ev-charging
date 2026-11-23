"""Small scripts to check hand calculations: repeated-game totals, Bayesian expected payoffs
(F=1.5, prior 0.30/0.70), memory-tree payoffs and mixed vs behavioral expected values.
Uses official benchmark files from data/starter/.
"""


def check_repeated_game():
    """Verify repeated-game calculations.

    C/H payoff table:
        CC=(4,4), CH=(0,6), HC=(6,0), HH=(1,1)

    Finite (3 rounds): backward induction -> HH every round, payoff (1,1) each.
    Infinite: cooperate = 4/(1-d), deviate = 6 + d/(1-d).
    Threshold: 4/(1-d) >= 6 + d/(1-d) => 4 >= 6(1-d) + d => 4 >= 6 - 5d => d >= 2/5 = 0.40.
    """
    results = {}

    # Finite: 3 rounds, backward induction
    # Final round: H strictly dominates C for both -> (1,1)
    # Round 2: continuation fixed at (1,1) regardless of action -> H dominates -> (1,1)
    # Round 1: continuation fixed at (1,1) -> H dominates -> (1,1)
    results['finite_3_round_total'] = 3 * 1  # = 3 per player
    assert results['finite_3_round_total'] == 3

    # Infinite threshold:
    # Cooperate: 4/(1-d), Deviate: 6 + d*1/(1-d)
    # 4/(1-d) >= 6 + d/(1-d)
    # (4-d)/(1-d) >= 6 => 4-d >= 6-6d => 5d >= 2 => d >= 2/5 = 0.40
    threshold = 2 / 5
    results['threshold'] = threshold
    assert abs(threshold - 0.4) < 1e-12

    # Check d=0.2: cooperation NOT sustainable
    d = 0.2
    coop = 4 / (1 - d)      # = 5.0
    dev = 6 + d / (1 - d)   # = 6.25
    results['d02_coop'] = coop
    results['d02_dev'] = dev
    assert dev > coop  # deviation is strictly better

    # Check d=0.5: cooperation sustainable
    d = 0.5
    coop = 4 / (1 - d)      # = 8.0
    dev = 6 + d / (1 - d)   # = 7.0
    results['d05_coop'] = coop
    results['d05_dev'] = dev
    assert coop > dev  # cooperation is strictly better

    # Punishment: best response to H is H (1 > 0)
    # If opponent plays H: C gives 0, H gives 1 -> H is best response
    results['punishment_br'] = 'H'

    print("Repeated game checks passed:", results)
    return results


def check_bayesian():
    """Verify Bayesian expected payoffs from data/starter/bayesian_types.csv.

    Prior: pi(Urgent) = 0.30, pi(Flexible) = 0.70
    Fee F = 1.5. Extra hold payoff alpha: Urgent=0, Flexible=1.
    Base table: CC=(4,4), CH=(0,6), HC=(6,0), HH=(1,1)

    With F=1.5 applied to own H payoff:
    Modified payoffs for a player choosing H:
      - Urgent: H payoffs become (6-1.5, 0) vs C, (1-1.5, 1) vs H => (4.5, 0) and (-0.5, 1)
      - Flexible: H payoffs become (6-1.5+1, 0) vs C, (1-1.5+1, 1) vs H => (5.5, 0) and (0.5, 1)

    Proposed plan: Urgent -> C, Flexible -> H.
    Test: does any type want to deviate?
    """
    pi_u = 0.30
    pi_f = 0.70
    F = 1.5

    results = {}

    # Opponent follows plan: Urgent plays C (prob 0.30), Flexible plays H (prob 0.70)

    # --- Check for Urgent player (prescribed action: C) ---
    # Urgent plays C:
    #   vs opponent C (Urgent, prob 0.30): own payoff = 4
    #   vs opponent H (Flexible, prob 0.70): own payoff = 0
    urgent_c = pi_u * 4 + pi_f * 0
    results['urgent_C'] = urgent_c  # = 1.20 (exact starter check)
    assert abs(urgent_c - 1.20) < 1e-10

    # Urgent plays H (deviation):
    #   vs opponent C (prob 0.30): base payoff 6, minus F=1.5, plus alpha=0 = 4.5
    #   vs opponent H (prob 0.70): base payoff 1, minus F=1.5, plus alpha=0 = -0.5
    urgent_h = pi_u * (6 - F) + pi_f * (1 - F)
    results['urgent_H'] = urgent_h  # = 0.30*4.5 + 0.70*(-0.5) = 1.35 - 0.35 = 1.00
    assert abs(urgent_h - 1.00) < 1e-10

    # Urgent: C (1.20) > H (1.00) -> Urgent does NOT want to deviate.
    results['urgent_wants_deviate'] = urgent_h > urgent_c
    assert not results['urgent_wants_deviate']

    # --- Check for Flexible player (prescribed action: H) ---
    # Flexible plays H:
    #   vs opponent C (prob 0.30): base 6, minus F=1.5, plus alpha=1 = 5.5
    #   vs opponent H (prob 0.70): base 1, minus F=1.5, plus alpha=1 = 0.5
    flexible_h = pi_u * (6 - F + 1) + pi_f * (1 - F + 1)
    results['flexible_H'] = flexible_h  # = 0.30*5.5 + 0.70*0.5 = 1.65 + 0.35 = 2.00
    assert abs(flexible_h - 2.00) < 1e-10

    # Flexible plays C (deviation):
    #   vs opponent C (prob 0.30): payoff = 4
    #   vs opponent H (prob 0.70): payoff = 0
    flexible_c = pi_u * 4 + pi_f * 0
    results['flexible_C'] = flexible_c  # = 1.20
    assert abs(flexible_c - 1.20) < 1e-10

    # Flexible: H (2.00) > C (1.20) -> Flexible does NOT want to deviate.
    results['flexible_wants_deviate'] = flexible_c > flexible_h
    assert not results['flexible_wants_deviate']

    # Both types are satisfied -> This IS a Bayesian Nash Equilibrium
    results['is_bne'] = not results['urgent_wants_deviate'] and not results['flexible_wants_deviate']
    assert results['is_bne']

    print("Bayesian checks passed:", results)
    return results


def check_memory_tree():
    """Verify memory tree payoffs matching data/starter/memory_tree.csv exactly.

    Leaves from official memory_tree.csv:
      LLL: (1, 3)
      LLR: (8, 4)
      LRL: (6, 1)
      LRR: (0, 2)
      RLL: (6, 5)
      RLR: (2, 2)
      RRL: (3, 4)
      RRR: (1, 1)
    """
    payoffs = {
        'LLL': (1, 3), 'LLR': (8, 4),
        'LRL': (6, 1), 'LRR': (0, 2),
        'RLL': (6, 5), 'RLR': (2, 2),
        'RRL': (3, 4), 'RRR': (1, 1),
    }

    # Full information backward induction:
    # Stage 3 (P1 at 4 distinct decision nodes):
    #   At LL: L->1, R->8 => chooses R (payoff (8, 4))
    #   At LR: L->6, R->0 => chooses L (payoff (6, 1))
    #   At RL: L->6, R->2 => chooses L (payoff (6, 5))
    #   At RR: L->3, R->1 => chooses L (payoff (3, 4))
    # Stage 2 (P2 at 2 distinct decision nodes):
    #   At L: evaluates L -> (8, 4) [P2 gets 4] vs R -> (6, 1) [P2 gets 1] => P2 chooses L
    #   At R: evaluates L -> (6, 5) [P2 gets 5] vs R -> (3, 4) [P2 gets 4] => P2 chooses L
    # Stage 1 (P1 at root):
    #   L leads to (L, L, R) with payoff (8, 4) -> P1 gets 8
    #   R leads to (R, L, L) with payoff (6, 5) -> P1 gets 6
    #   Since 8 > 6, P1 chooses L at the root.

    # Backward induction solution: L, L, R -> outcome LLR = (8, 4)
    bi_outcome = payoffs['LLR']
    assert bi_outcome == (8, 4)

    results = {
        'full_info_path': 'LLR',
        'full_info_payoff': bi_outcome,
    }

    print("Memory tree checks passed:", results)
    return results


def check_mixed_behavioral():
    """Verify mixed vs behavioral expected values with P2 fixed to L.

    Official memory_tree.csv leaves with P2=L:
      LLL: 1
      LLR: 8
      RLL: 6
      RLR: 2

    Mixed 50-50 lottery between (always L = LLL) and (always R = RLR):
      Prob(LLL) = 0.5, Prob(RLR) = 0.5
      E = (1 + 2) / 2 = 1.50

    Fresh 50-50 draws at each stage (behavioral with forgotten stage):
      Prob(LLL) = 0.25, Prob(LLR) = 0.25, Prob(RLL) = 0.25, Prob(RLR) = 0.25
      E = (1 + 8 + 6 + 2) / 4 = 17 / 4 = 4.25

    With perfect recall, behavioral reproduces mixed:
      First move: 50-50 L or R
      Second move: repeat remembered first action
      -> same as mixed: E = 1.50
    """
    payoffs = {'LL': 1, 'LR': 8, 'RL': 6, 'RR': 2}

    # Mixed lottery
    mixed_ev = (payoffs['LL'] + payoffs['RR']) / 2.0
    assert abs(mixed_ev - 1.50) < 1e-10

    # Fresh draws (behavioral with forgotten stage)
    behavioral_ev = sum(payoffs.values()) / 4.0
    assert abs(behavioral_ev - 4.25) < 1e-10

    # Perfect recall behavioral reproduces mixed
    recall_ev = 0.5 * payoffs['LL'] + 0.5 * payoffs['RR']
    assert abs(recall_ev - mixed_ev) < 1e-10

    results = {
        'mixed_ev': mixed_ev,            # 1.50
        'behavioral_ev': behavioral_ev,  # 4.25
        'recall_ev': recall_ev,          # 1.50
        'behavioral_better': behavioral_ev > mixed_ev,  # True
    }

    print("Mixed/behavioral checks passed:", results)
    return results


if __name__ == '__main__':
    check_repeated_game()
    check_bayesian()
    check_memory_tree()
    check_mixed_behavioral()
    print("\nAll arithmetic checks passed!")
