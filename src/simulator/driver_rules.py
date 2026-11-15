"""Driver rules after a full charge: Release, Hold, Reciprocal, Fee aware.
Legal actions: Release, Hold 1, Hold 2 (must fit before departure; completion at departure forces release).
Reciprocal: release on first visit; later release if last visit fully served with <=2 waiting slots,
otherwise Hold 1 if legal else Release.
Fee aware: choose idle slots O maximizing (h - F) * O; release if tied.
"""


def choose_action(rule, driver, fee, legal_hold_max, last_visit):
    raise NotImplementedError
