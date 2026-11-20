"""Load inputs (public sessions, private drivers) and write visit-level CSV, settings and summary JSON."""

import csv
import json
import os


def load_inputs(seed_dir):
    """Load sessions_public.csv and drivers_private.csv from a seed directory.

    Args:
        seed_dir: path to seed data directory

    Returns:
        (requests, drivers):
            requests: list of dicts with 'driver_id', 'day', 'arrival', 'departure',
                      'requested_kwh', 'demand'
            drivers: dict mapping driver_id -> dict with 'type', 'v', 'w', 'h', 'rule'
    """
    # Load sessions
    sessions_path = os.path.join(seed_dir, 'sessions_public.csv')
    requests = []
    with open(sessions_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            req = {
                'driver_id': row.get('driver_id', row.get('driver', '')),
                'day': int(row.get('day', 0)),
                'arrival': int(row.get('arrival', 0)),
                'departure': int(row.get('departure', 0)),
                'requested_kwh': float(row.get('requested_kwh', row.get('request_kwh', 0))),
            }
            if 'demand' in row:
                req['demand'] = row['demand']
            requests.append(req)

    # Load drivers
    drivers_path = os.path.join(seed_dir, 'drivers_private.csv')
    drivers = {}
    type_params = {
        'Urgent': {'v': 3, 'w': 3, 'h': 1},
        'Flexible': {'v': 2, 'w': 1, 'h': 2},
    }
    with open(drivers_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            did = row.get('driver_id', row.get('driver', ''))
            dtype = row.get('type', 'Flexible')
            rule = row.get('private_strategy', row.get('rule', 'Release'))
            params = type_params.get(dtype, {'v': 2, 'w': 1, 'h': 2})
            drivers[did] = {
                'type': dtype,
                'v': params['v'],
                'w': params['w'],
                'h': params['h'],
                'rule': rule,
            }

    return requests, drivers


def save_results(output_dir, visits, settings, summary):
    """Save visit-level CSV, settings JSON, and summary JSON.

    Args:
        output_dir: directory to write to (created if needed)
        visits: list of visit record dicts
        settings: dict of run settings
        summary: dict of summary metrics
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save visits CSV
    if visits:
        fieldnames = [
            'driver_id', 'type', 'day', 'arrival', 'departure', 'start',
            'requested_kwh', 'energy_kwh', 'wait_slots', 'idle_slots',
            'fully_served', 'utility_before', 'utility_after', 'rule'
        ]
        visits_path = os.path.join(output_dir, 'visits.csv')
        with open(visits_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(visits)

    # Save settings
    settings_path = os.path.join(output_dir, 'settings.json')
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)

    # Save summary
    def _json_default(obj):
        if hasattr(obj, 'item'):
            return obj.item()
        return str(obj)

    summary_path = os.path.join(output_dir, 'summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=_json_default)


def load_results(output_dir):
    """Load saved results from a directory.

    Returns:
        (visits_df_or_list, settings, summary)
    """
    import pandas as pd

    visits_path = os.path.join(output_dir, 'visits.csv')
    settings_path = os.path.join(output_dir, 'settings.json')
    summary_path = os.path.join(output_dir, 'summary.json')

    visits = pd.read_csv(visits_path) if os.path.exists(visits_path) else pd.DataFrame()

    with open(settings_path, 'r') as f:
        settings = json.load(f)

    with open(summary_path, 'r') as f:
        summary = json.load(f)

    return visits, settings, summary
