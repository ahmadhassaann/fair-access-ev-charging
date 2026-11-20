"""Average waiting (unserved included), share fully served, total energy, idle slots; by Urgent/Flexible."""

import pandas as pd


def compute_metrics(visits_df):
    """Compute summary metrics from a visits DataFrame.

    Args:
        visits_df: DataFrame with columns including 'wait_slots', 'energy_kwh',
                   'idle_slots', 'fully_served', 'type', 'utility_before', 'utility_after'

    Returns:
        dict with overall and per-type metrics
    """
    df = visits_df.copy()

    n = len(df)
    if n == 0:
        return _empty_metrics()

    metrics = {
        'n_visits': n,
        'avg_waiting': df['wait_slots'].mean(),
        'share_fully_served': df['fully_served'].mean() if 'fully_served' in df.columns else 0,
        'total_energy': df['energy_kwh'].sum(),
        'total_idle': df['idle_slots'].sum(),
        'avg_utility_before': df['utility_before'].mean() if 'utility_before' in df.columns else 0,
        'avg_utility_after': df['utility_after'].mean() if 'utility_after' in df.columns else 0,
    }

    # Per-type breakdown
    for dtype in ['Urgent', 'Flexible']:
        sub = df[df['type'] == dtype]
        prefix = dtype.lower()
        if len(sub) > 0:
            metrics[f'{prefix}_n'] = len(sub)
            metrics[f'{prefix}_avg_waiting'] = sub['wait_slots'].mean()
            metrics[f'{prefix}_share_fully_served'] = sub['fully_served'].mean()
            metrics[f'{prefix}_total_energy'] = sub['energy_kwh'].sum()
            metrics[f'{prefix}_total_idle'] = sub['idle_slots'].sum()
            metrics[f'{prefix}_avg_utility_before'] = sub['utility_before'].mean()
            metrics[f'{prefix}_avg_utility_after'] = sub['utility_after'].mean()
        else:
            metrics[f'{prefix}_n'] = 0
            metrics[f'{prefix}_avg_waiting'] = 0
            metrics[f'{prefix}_share_fully_served'] = 0
            metrics[f'{prefix}_total_energy'] = 0
            metrics[f'{prefix}_total_idle'] = 0
            metrics[f'{prefix}_avg_utility_before'] = 0
            metrics[f'{prefix}_avg_utility_after'] = 0

    return metrics


def _empty_metrics():
    m = {
        'n_visits': 0,
        'avg_waiting': 0,
        'share_fully_served': 0,
        'total_energy': 0,
        'total_idle': 0,
        'avg_utility_before': 0,
        'avg_utility_after': 0,
    }
    for prefix in ['urgent', 'flexible']:
        m[f'{prefix}_n'] = 0
        m[f'{prefix}_avg_waiting'] = 0
        m[f'{prefix}_share_fully_served'] = 0
        m[f'{prefix}_total_energy'] = 0
        m[f'{prefix}_total_idle'] = 0
        m[f'{prefix}_avg_utility_before'] = 0
        m[f'{prefix}_avg_utility_after'] = 0
    return m
