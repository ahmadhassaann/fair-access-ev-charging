"""Load inputs (public sessions, private drivers) and write visit-level CSV, settings and summary JSON."""

import csv
import json
import os


def load_inputs(seed_dir):
    """Load sessions_public.csv and drivers_private.csv from a seed directory.

    Supports both official schema (arrival_slot, departure_slot, scenario, private_type, private_strategy)
    and shorthand schema (arrival, departure, demand, type, rule).

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
    with open(sessions_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Arrival slot
            arr = row.get('arrival_slot', row.get('arrival', 0))
            # Departure slot
            dep = row.get('departure_slot', row.get('departure', 16))
            # Driver ID
            did = row.get('driver_id', row.get('driver', ''))
            # Day
            day_val = int(row.get('day', 1))
            # Requested kWh
            req_kwh = float(row.get('requested_kwh', row.get('request_kwh', 0)))
            # Demand scenario (low, medium, high)
            demand = row.get('scenario', row.get('demand', 'medium')).lower()

            req = {
                'driver_id': did,
                'day': day_val,
                'arrival': int(arr),
                'departure': int(dep),
                'requested_kwh': req_kwh,
                'demand': demand,
            }
            if 'request_id' in row:
                req['request_id'] = row['request_id']
            requests.append(req)

    # Load drivers
    drivers_path = os.path.join(seed_dir, 'drivers_private.csv')
    drivers = {}
    type_defaults = {
        'urgent': {'v': 3.0, 'w': 3.0, 'h': 1.0},
        'flexible': {'v': 2.0, 'w': 1.0, 'h': 2.0},
    }
    with open(drivers_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            did = row.get('driver_id', row.get('driver', ''))
            raw_type = row.get('private_type', row.get('type', 'flexible')).strip()
            dtype = raw_type.capitalize()
            rule = row.get('private_strategy', row.get('rule', 'release')).strip()

            # Values can be explicitly given in columns or inferred from type
            v_val = row.get('value_per_kwh', row.get('v'))
            w_val = row.get('wait_cost_per_slot', row.get('w'))
            h_val = row.get('idle_benefit_per_slot', row.get('h'))

            defaults = type_defaults.get(raw_type.lower(), {'v': 2.0, 'w': 1.0, 'h': 2.0})

            drivers[did] = {
                'driver_id': did,
                'type': dtype,
                'v': float(v_val) if v_val is not None and v_val != '' else defaults['v'],
                'w': float(w_val) if w_val is not None and w_val != '' else defaults['w'],
                'h': float(h_val) if h_val is not None and h_val != '' else defaults['h'],
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

    # Save visits CSV with complete specification fields:
    # arrival, start, finish, release, energy, waiting, action, idle slots, penalty, utility
    if visits:
        fieldnames = [
            'driver_id', 'type', 'day', 'arrival', 'departure', 'start',
            'finish', 'release', 'action', 'requested_kwh', 'energy_kwh',
            'wait_slots', 'idle_slots', 'penalty', 'fully_served',
            'utility_before', 'utility_after', 'rule'
        ]
        visits_path = os.path.join(output_dir, 'visits.csv')
        with open(visits_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(visits)

    # Save settings
    settings_path = os.path.join(output_dir, 'settings.json')
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)

    # Save summary
    def _json_default(obj):
        if hasattr(obj, 'item'):
            return obj.item()
        return str(obj)

    summary_path = os.path.join(output_dir, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, default=_json_default)


def load_results(output_dir):
    """Load saved results from a directory.

    Returns:
        (visits_df, settings, summary)
    """
    import pandas as pd

    visits_path = os.path.join(output_dir, 'visits.csv')
    settings_path = os.path.join(output_dir, 'settings.json')
    summary_path = os.path.join(output_dir, 'summary.json')

    visits = pd.read_csv(visits_path) if os.path.exists(visits_path) else pd.DataFrame()

    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)

    with open(summary_path, 'r', encoding='utf-8') as f:
        summary = json.load(f)

    return visits, settings, summary
