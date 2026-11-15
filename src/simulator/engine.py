"""Slot loop. Event order each boundary:
1. Finish energy from previous interval; remove drivers whose departure has arrived.
2. Take release/hold choice from newly completed drivers who can stay; end expired holds.
3. Add arrivals; allocate free chargers by arrival time then driver ID; charge next interval.
No interval after boundary 16.
"""


def run_day(requests, drivers, policy, state):
    raise NotImplementedError
