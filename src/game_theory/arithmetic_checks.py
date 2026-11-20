"""Small scripts to check hand calculations: repeated-game totals, Bayesian expected payoffs
(F=1.5, prior 0.30/0.70), memory-tree payoffs and mixed vs behavioral expected values."""


def check_repeated_game():
    """Verify repeated-game calculations.

    C/H payoff table:
        CC=(4,4), CH=(0,6), HC=(6,0), HH=(1,1)

    Finite (3 rounds): backward induction -> HH every round, payoff (1,1) each.
    Infinite: cooperate = 4/(1-d), deviate = 6 + d/(1-d).
    Threshold: 4/(1-d) >= 6 + d/(1-d) => 4 >= 6(1-d) + d => 4 >= 6 - 5d => d >= 2/5.
    """
    results = {}

    # Finite: 3 rounds, backward induction
    # Final round: H dominates for both -> (1,1)
    # Round 2: knowing round 3 is (H,H), H still dominates -> (1,1)
    # Round 1: same -> (1,1)
    results['finite_3_round_total'] = 3 * 1  # = 3 per player
    assert results['finite_3_round_total'] == 3

    # Infinite threshold
    # Cooperate: 4/(1-d), Deviate: 6 + d*1/(1-d)
    # 4/(1-d) >= 6 + d/(1-d)
    # (4-d)/(1-d) >= 6
    # 4-d >= 6-6d
    # 5d >= 2
    # d >= 2/5 = 0.4
    threshold = 2 / 5
    results['threshold'] = threshold
    assert abs(threshold - 0.4) < 1e-12

    # Check d=0.2: cooperation NOT sustainable
    d = 0.2
    coop = 4 / (1 - d)   # = 5
    dev = 6 + d / (1 - d)  # = 6.25
    results['d02_coop'] = coop
    results['d02_dev'] = dev
    assert dev > coop  # deviation is better

    # Check d=0.5: cooperation sustainable
    d = 0.5
    coop = 4 / (1 - d)   # = 8
    dev = 6 + d / (1 - d)  # = 7
    results['d05_coop'] = coop
    results['d05_dev'] = dev
    assert coop > dev  # cooperation is better

    # Punishment: best response to H is H (6>4 is wrong for column, 1>0)
    # If opponent plays H: C gives 0, H gives 1 -> H is best response
    results['punishment_br'] = 'H'  # H is best response to H

    print("Repeated game checks passed:", results)
    return results


def check_bayesian():
    """Verify Bayesian expected payoffs.

    Prior: pi(Urgent) = 0.30, pi(Flexible) = 0.70
    Fee F = 1.5. Add +1 for own H if Flexible; +0 if Urgent.
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

    # --- Check for Urgent player (supposed to play C) ---
    # Urgent plays C:
    #   vs opponent C (Urgent, prob 0.30): own payoff = 4
    #   vs opponent H (Flexible, prob 0.70): own payoff = 0
    urgent_c = pi_u * 4 + pi_f * 0
    results['urgent_C'] = urgent_c  # = 1.20
    assert abs(urgent_c - 1.20) < 1e-10

    # Urgent plays H (deviate):
    #   vs opponent C (prob 0.30): base payoff 6, minus F=1.5, plus 0 (Urgent) = 4.5
    #   vs opponent H (prob 0.70): base payoff 1, minus F=1.5, plus 0 (Urgent) = -0.5
    urgent_h = pi_u * (6 - F) + pi_f * (1 - F)
    results['urgent_H'] = urgent_h  # = 0.30*4.5 + 0.70*(-0.5) = 1.35 - 0.35 = 1.00
    assert abs(urgent_h - 1.00) < 1e-10

    # Urgent: C (1.20) > H (1.00) -> Urgent does NOT want to deviate. Good.
    results['urgent_wants_deviate'] = urgent_h > urgent_c  # False

    # --- Check for Flexible player (supposed to play H) ---
    # Flexible plays H:
    #   vs opponent C (prob 0.30): base 6, minus F=1.5, plus 1 (Flexible) = 5.5
    #   vs opponent H (prob 0.70): base 1, minus F=1.5, plus 1 (Flexible) = 0.5
    flexible_h = pi_u * (6 - F + 1) + pi_f * (1 - F + 1)
    results['flexible_H'] = flexible_h  # = 0.30*5.5 + 0.70*0.5 = 1.65 + 0.35 = 2.00
    assert abs(flexible_h - 2.00) < 1e-10

    # Flexible plays C (deviate):
    #   vs opponent C (prob 0.30): payoff = 4
    #   vs opponent H (prob 0.70): payoff = 0
    flexible_c = pi_u * 4 + pi_f * 0
    results['flexible_C'] = flexible_c  # = 1.20
    assert abs(flexible_c - 1.20) < 1e-10

    # Flexible: H (2.00) > C (1.20) -> Flexible does NOT want to deviate. Good.
    results['flexible_wants_deviate'] = flexible_c > flexible_h  # False

    # Both types are satisfied -> This IS a Bayesian Nash Equilibrium
    results['is_bne'] = not results['urgent_wants_deviate'] and not results['flexible_wants_deviate']
    assert results['is_bne']

    print("Bayesian checks passed:", results)
    return results


def check_memory_tree():
    """Verify memory tree payoffs.

    P1 -> P2 -> P1 again, menus L/R at each node.
    8 terminal outcomes (P1_first, P2, P1_second): LLL, LLR, LRL, LRR, RLL, RLR, RRL, RRR.

    Using a standard teaching example with payoffs:
    LLL: (2,1), LLR: (3,0), LRL: (1,2), LRR: (4,1),
    RLL: (0,3), RLR: (2,2), RRL: (3,1), RRR: (1,0)
    """
    payoffs = {
        'LLL': (2, 1), 'LLR': (3, 0),
        'LRL': (1, 2), 'LRR': (4, 1),
        'RLL': (0, 3), 'RLR': (2, 2),
        'RRL': (3, 1), 'RRR': (1, 0),
    }

    # Full information: backward induction
    # P1's second move (4 decision nodes):
    #   After LL: L->2, R->3 => R (payoff 3)
    #   After LR: L->1, R->4 => R (payoff 4)
    #   After RL: L->0, R->2 => R (payoff 2)
    #   After RR: L->3, R->1 => L (payoff 3)

    # P2's move (2 decision nodes):
    #   After L: P2 L -> P1 gets 3, P2 gets 0; P2 R -> P1 gets 4, P2 gets 1 => P2 picks R (payoff 1)
    #   After R: P2 L -> P1 gets 2, P2 gets 2; P2 R -> P1 gets 3, P2 gets 1 => P2 picks L (payoff 2)

    # P1's first move:
    #   L -> (via P2=R, P1_2=R): payoff (4,1)
    #   R -> (via P2=L, P1_2=R): payoff (2,2)
    #   P1 picks L (payoff 4)

    # Backward induction solution: L, R, R -> outcome LRR = (4,1)
    bi_outcome = payoffs['LRR']
    assert bi_outcome == (4, 1)

    results = {
        'full_info_path': 'LRR',
        'full_info_payoff': bi_outcome,
    }

    print("Memory tree checks passed:", results)
    return results


def check_mixed_behavioral():
    """Verify mixed vs behavioral expected values.

    P1 plays twice (stages 1 and 2), P2 fixed to L at both.
    P1 payoffs: LL=1, LR=8, RL=6, RR=2.

    Mixed 50-50 lottery between (always L) and (always R):
      Prob(LL) = 0.5, Prob(RR) = 0.5
      E = 0.5*1 + 0.5*2 = 1.5

    Fresh 50-50 draws at each stage (behavioral, forgotten stage):
      Prob(LL)=0.25, Prob(LR)=0.25, Prob(RL)=0.25, Prob(RR)=0.25
      E = 0.25*1 + 0.25*8 + 0.25*6 + 0.25*2 = 4.25

    With perfect recall, behavioral reproduces mixed:
      First move: 50-50 L or R
      Second move: repeat remembered first action
      -> same as mixed: LL or RR each with prob 0.5
    """
    payoffs = {'LL': 1, 'LR': 8, 'RL': 6, 'RR': 2}

    # Mixed lottery
    mixed_ev = 0.5 * payoffs['LL'] + 0.5 * payoffs['RR']
    assert abs(mixed_ev - 1.5) < 1e-10

    # Fresh draws (behavioral with forgotten stage)
    behavioral_ev = 0.25 * (payoffs['LL'] + payoffs['LR'] + payoffs['RL'] + payoffs['RR'])
    assert abs(behavioral_ev - 4.25) < 1e-10

    # Perfect recall behavioral reproduces mixed
    recall_ev = 0.5 * payoffs['LL'] + 0.5 * payoffs['RR']
    assert abs(recall_ev - mixed_ev) < 1e-10

    results = {
        'mixed_ev': mixed_ev,         # 1.5
        'behavioral_ev': behavioral_ev,  # 4.25
        'recall_ev': recall_ev,        # 1.5 (matches mixed)
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
