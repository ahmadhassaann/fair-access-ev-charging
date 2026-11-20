"""Driver rules after a full charge: Release, Hold, Reciprocal, Fee aware.
Legal actions: Release, Hold 1, Hold 2 (must fit before departure; completion at departure forces release).
Reciprocal: release on first visit; later release if last visit fully served with <=2 waiting slots,
otherwise Hold 1 if legal else Release.
Fee aware: choose idle slots O maximizing (h - F) * O; release if tied.
"""


def choose_action(rule, driver, fee, legal_hold_max, last_visit):
    """Choose how many idle slots to hold after a full charge.

    Args:
        rule: str - 'Release', 'Hold', 'Reciprocal', or 'Fee_aware'
        driver: dict with keys including 'h' (idle benefit per slot), 'type', etc.
        fee: float - idle penalty per slot (F)
        legal_hold_max: int - max slots the driver can legally hold (0, 1, or 2)
        last_visit: dict or None - info about driver's last visit
            (keys: 'fully_served', 'wait_slots')

    Returns:
        int: 0 = Release, 1 = Hold 1, 2 = Hold 2
    """
    if legal_hold_max <= 0:
        return 0

    rule_lower = rule.lower().replace('_', ' ').strip()

    if rule_lower == 'release':
        return 0

    elif rule_lower in ('hold 1', 'hold_1', 'hold1'):
        return min(legal_hold_max, 1)

    elif rule_lower in ('hold 2', 'hold_2', 'hold2'):
        return min(legal_hold_max, 2)

    elif rule_lower == 'hold':
        # Choose the largest legal hold, up to 2
        return min(legal_hold_max, 2)

    elif rule_lower == 'reciprocal':
        if last_visit is None:
            # First visit: release
            return 0
        # Later: release if last visit was fully served with at most 2 waiting slots
        if last_visit.get('fully_served', False) and last_visit.get('wait_slots', 0) <= 2:
            return 0
        else:
            # Hold 1 if legal, else Release
            return min(1, legal_hold_max)

    elif rule_lower in ('fee_aware', 'feeaware', 'fee aware'):
        h = driver.get('h', 0)
        best_o = 0
        best_val = 0  # value of releasing (O=0)
        for o in range(1, legal_hold_max + 1):
            val = (h - fee) * o
            if val > best_val:
                best_val = val
                best_o = o
            # Release if tied (val == best_val and best_o == 0 stays 0)
        return best_o

    else:
        # Unknown rule defaults to release
        return 0
