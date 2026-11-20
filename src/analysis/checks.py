"""Invariants: no charger serves two drivers at once; no energy before arrival, after departure or during
a hold; energy <= request; unserved drivers still pay waiting cost; identical inputs give identical results."""

import pandas as pd


def check_no_double_booking(visits_df, n_chargers):
    """Check that no charger serves two drivers at the same time.

    For each day, verify that at most n_chargers drivers are actively charging
    in any given slot.
    """
    df = visits_df.copy()
    if df.empty:
        return True

    for day in df['day'].unique() if 'day' in df.columns else [0]:
        day_df = df[df['day'] == day] if 'day' in df.columns else df
        for slot in range(16):
            # Count drivers occupying a charger during this slot
            # A driver occupies from start to (start + charging_slots + idle_slots)
            count = 0
            for _, row in day_df.iterrows():
                start = row.get('start')
                if pd.isna(start) or start is None:
                    continue
                start = int(start)
                energy = float(row.get('energy_kwh', 0))
                idle = int(row.get('idle_slots', 0))
                # Charging slots = ceil(energy / 3) approximately
                import math
                charge_slots = math.ceil(energy / 3) if energy > 0 else 0
                end = start + charge_slots + idle
                if start <= slot < end:
                    count += 1
            if count > n_chargers:
                return False
    return True


def check_energy_timing(visits_df):
    """Check that energy is never delivered before arrival or after departure."""
    df = visits_df.copy()
    if df.empty:
        return True

    for _, row in df.iterrows():
        arrival = int(row['arrival'])
        departure = int(row['departure'])
        start = row.get('start')
        energy = float(row.get('energy_kwh', 0))

        if energy > 0:
            if pd.isna(start) or start is None:
                return False  # energy without a start time
            start = int(start)
            if start < arrival:
                return False  # started before arrival
            import math
            charge_slots = math.ceil(energy / 3)
            charge_end = start + charge_slots
            if charge_end > departure:
                return False  # charging extends past departure
    return True


def check_energy_cap(visits_df):
    """Check that delivered energy never exceeds the request."""
    df = visits_df.copy()
    if df.empty:
        return True

    for _, row in df.iterrows():
        energy = float(row.get('energy_kwh', 0))
        requested = float(row.get('requested_kwh', 0))
        if energy > requested + 0.001:  # small tolerance for float
            return False
    return True


def check_unserved_waiting_cost(visits_df):
    """Check that an unserved driver still has a waiting cost."""
    df = visits_df.copy()
    if df.empty:
        return True

    for _, row in df.iterrows():
        energy = float(row.get('energy_kwh', 0))
        start = row.get('start')
        wait = int(row.get('wait_slots', 0))
        arrival = int(row['arrival'])
        departure = int(row['departure'])

        if (pd.isna(start) or start is None) and energy == 0:
            # Unserved driver: waiting should be arrival to departure
            expected_wait = departure - arrival
            if wait != expected_wait:
                return False
    return True


def run_all_checks(visits_df, n_chargers=6):
    """Run all invariant checks.

    Returns:
        dict of check_name -> bool (True = passed)
    """
    return {
        'no_double_booking': check_no_double_booking(visits_df, n_chargers),
        'energy_timing': check_energy_timing(visits_df),
        'energy_cap': check_energy_cap(visits_df),
        'unserved_waiting_cost': check_unserved_waiting_cost(visits_df),
    }
