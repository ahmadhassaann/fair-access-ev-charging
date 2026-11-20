"""Slot loop. Event order each boundary:
1. Finish energy from previous interval; remove drivers whose departure has arrived.
2. Take release/hold choice from newly completed drivers who can stay; end expired holds.
3. Add arrivals; allocate free chargers by arrival time then driver ID; charge next interval.
No interval after boundary 16.
"""

from .charger_queue import ChargerQueue
from .driver_rules import choose_action
from .utility import utility


SLOTS_PER_DAY = 16
KWH_PER_SLOT = 3  # each charger supplies up to 3 kWh per full slot


def run_day(requests, drivers, policy, state):
    """Simulate one day of charging.

    Args:
        requests: list of dicts, each with keys:
            'driver_id', 'arrival', 'departure', 'requested_kwh'
        drivers: dict mapping driver_id -> driver info dict with keys:
            'type', 'v', 'w', 'h', 'rule'
        policy: dict with key 'fee' (0 for P0, 2 for P1)
        state: dict with:
            'queue': ChargerQueue instance
            'last_visits': dict driver_id -> last visit info
            'n_chargers': int

    Returns:
        (visits, state): visits is a list of visit record dicts; state is updated.
    """
    fee = policy['fee']
    queue = state['queue']
    last_visits = state.get('last_visits', {})
    queue.reset()

    # Build per-request tracking
    active = {}   # driver_id -> active record
    waiting = []  # list of request dicts waiting for a charger
    visits = []   # completed visit records

    # Group requests by arrival slot
    arrivals_by_slot = {}
    for req in requests:
        slot = req['arrival']
        arrivals_by_slot.setdefault(slot, []).append(req)

    # Track charging state: driver_id -> {energy_delivered, start_slot, ...}
    charging = {}  # driver_id -> charging state dict
    holding = {}   # driver_id -> slots remaining in hold

    for boundary in range(SLOTS_PER_DAY + 1):  # 0..16

        # === STEP 1: Finish energy from previous interval; remove departures ===
        if boundary > 0:
            # Deliver energy for the interval that just finished (boundary-1 to boundary)
            for did in list(charging.keys()):
                if did in holding:
                    continue  # holding drivers don't get energy
                rec = active[did]
                remaining = rec['requested_kwh'] - rec['energy_delivered']
                delivered = min(KWH_PER_SLOT, remaining)
                rec['energy_delivered'] += delivered

            # Remove drivers whose departure has arrived
            for did in list(active.keys()):
                rec = active[did]
                if rec['departure'] <= boundary:
                    # Driver must leave now
                    cid = queue.find_charger(did)
                    if cid is not None:
                        queue.free_charger(cid)
                    if did in charging:
                        del charging[did]
                    if did in holding:
                        del holding[did]
                    _finalize_visit(rec, drivers, fee, last_visits, visits, boundary)
                    del active[did]

        # === STEP 2: Release/hold from newly completed; end expired holds ===
        if boundary > 0:
            # Check for newly completed drivers who can stay
            for did in list(charging.keys()):
                if did in holding:
                    continue
                rec = active.get(did)
                if rec is None:
                    continue
                if rec['energy_delivered'] >= rec['requested_kwh']:
                    # Fully charged - ask for hold/release decision
                    rec['charge_end_slot'] = boundary
                    dep = rec['departure']
                    slots_before_departure = dep - boundary
                    legal_hold_max = min(2, slots_before_departure)

                    if legal_hold_max <= 0:
                        # Completion at departure forces release
                        cid = queue.find_charger(did)
                        if cid is not None:
                            queue.free_charger(cid)
                        del charging[did]
                        _finalize_visit(rec, drivers, fee, last_visits, visits, boundary)
                        del active[did]
                    else:
                        driver = drivers[did]
                        last_v = last_visits.get(did)
                        hold_slots = choose_action(
                            driver['rule'], driver, fee, legal_hold_max, last_v
                        )
                        if hold_slots == 0:
                            # Release
                            cid = queue.find_charger(did)
                            if cid is not None:
                                queue.free_charger(cid)
                            del charging[did]
                            _finalize_visit(rec, drivers, fee, last_visits, visits, boundary)
                            del active[did]
                        else:
                            # Hold
                            rec['idle_slots'] = hold_slots
                            rec['hold_end'] = boundary + hold_slots
                            holding[did] = hold_slots
                            del charging[did]

            # End expired holds
            for did in list(holding.keys()):
                rec = active.get(did)
                if rec is None:
                    continue
                if rec.get('hold_end', 0) <= boundary:
                    cid = queue.find_charger(did)
                    if cid is not None:
                        queue.free_charger(cid)
                    del holding[did]
                    _finalize_visit(rec, drivers, fee, last_visits, visits, boundary)
                    del active[did]

        # === STEP 3: Add arrivals; allocate; charge next interval ===
        # Add arrivals for this boundary
        if boundary in arrivals_by_slot:
            for req in arrivals_by_slot[boundary]:
                did = req['driver_id']
                rec = {
                    'driver_id': did,
                    'arrival': req['arrival'],
                    'departure': req['departure'],
                    'requested_kwh': req['requested_kwh'],
                    'energy_delivered': 0.0,
                    'start_slot': None,
                    'charge_end_slot': None,
                    'idle_slots': 0,
                    'hold_end': None,
                }
                active[did] = rec
                waiting.append(req)

        # Also add previously waiting drivers who are still waiting
        # (waiting list maintained below after allocation)

        if boundary < SLOTS_PER_DAY:
            # Allocate free chargers to waiting drivers
            still_waiting = []
            for w in waiting:
                did = w['driver_id']
                if did in active and active[did]['start_slot'] is None:
                    still_waiting.append(w)
            waiting_to_allocate = sorted(still_waiting, key=lambda d: (d['arrival'], d['driver_id']))

            free = queue.free_chargers()
            new_waiting = []
            for w in waiting_to_allocate:
                did = w['driver_id']
                if free:
                    cid = free.pop(0)
                    queue.assign(cid, did)
                    active[did]['start_slot'] = boundary
                    charging[did] = True
                else:
                    new_waiting.append(w)
            waiting = new_waiting

            # Charge during next interval happens at next boundary (step 1)

    # End of day: finalize any remaining active drivers
    for did in list(active.keys()):
        rec = active[did]
        cid = queue.find_charger(did)
        if cid is not None:
            queue.free_charger(cid)
        if did in charging:
            del charging[did]
        if did in holding:
            del holding[did]
        _finalize_visit(rec, drivers, fee, last_visits, visits, SLOTS_PER_DAY)
        del active[did]

    state['last_visits'] = last_visits
    return visits, state


def _finalize_visit(rec, drivers, fee, last_visits, visits, end_boundary):
    """Create a visit record and update last_visits."""
    did = rec['driver_id']
    driver = drivers[did]

    arrival = rec['arrival']
    start = rec['start_slot']
    energy = rec['energy_delivered']
    idle = rec['idle_slots']
    requested = rec['requested_kwh']

    if start is not None:
        wait_slots = start - arrival
    else:
        # Never served
        wait_slots = rec['departure'] - arrival

    fully_served = (energy >= requested)

    v = driver['v']
    w = driver['w']
    h = driver['h']

    util_before, util_after = utility(v, w, h, fee, energy, wait_slots, idle)

    visit = {
        'driver_id': did,
        'type': driver['type'],
        'arrival': arrival,
        'departure': rec['departure'],
        'start': start,
        'requested_kwh': requested,
        'energy_kwh': energy,
        'wait_slots': wait_slots,
        'idle_slots': idle,
        'fully_served': fully_served,
        'utility_before': util_before,
        'utility_after': util_after,
        'rule': driver['rule'],
    }
    visits.append(visit)

    # Update last visit for Reciprocal rule
    last_visits[did] = {
        'fully_served': fully_served,
        'wait_slots': wait_slots,
    }


def run_simulation(all_requests, drivers, policy, n_chargers, n_days):
    """Run the full simulation across multiple days.

    Args:
        all_requests: list of all request dicts with 'day' field
        drivers: dict mapping driver_id -> driver info
        policy: dict with 'fee' key
        n_chargers: int
        n_days: int

    Returns:
        list of all visit records across all days
    """
    state = {
        'queue': ChargerQueue(n_chargers),
        'last_visits': {},
        'n_chargers': n_chargers,
    }

    all_visits = []
    for day in range(n_days):
        day_requests = [r for r in all_requests if r['day'] == day]
        day_visits, state = run_day(day_requests, drivers, policy, state)
        for v in day_visits:
            v['day'] = day
        all_visits.extend(day_visits)

    return all_visits
