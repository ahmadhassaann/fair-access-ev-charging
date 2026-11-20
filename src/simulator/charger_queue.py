"""Queue and charger allocation: by arrival time, then driver ID.
(Named charger_queue.py to avoid clashing with Python's built-in `queue` module.)
"""


class ChargerQueue:
    """Manages a pool of chargers and a waiting queue of drivers."""

    def __init__(self, n_chargers):
        self.n_chargers = n_chargers
        # charger_id -> driver_id or None
        self.chargers = {i: None for i in range(n_chargers)}

    def free_charger(self, charger_id):
        """Release a charger so it becomes available."""
        self.chargers[charger_id] = None

    def free_chargers(self):
        """Return list of free charger IDs."""
        return [cid for cid, did in sorted(self.chargers.items()) if did is None]

    def num_free(self):
        return len(self.free_chargers())

    def assign(self, charger_id, driver_id):
        """Assign a driver to a specific charger."""
        self.chargers[charger_id] = driver_id

    def find_charger(self, driver_id):
        """Find which charger a driver is on, or None."""
        for cid, did in self.chargers.items():
            if did == driver_id:
                return cid
        return None

    def allocate_waiting(self, waiting_drivers):
        """Allocate free chargers to waiting drivers sorted by (arrival, driver_id).

        Args:
            waiting_drivers: list of dicts with at least 'driver_id' and 'arrival' keys.

        Returns:
            List of (driver_id, charger_id) assignments made.
        """
        free = self.free_chargers()
        if not free or not waiting_drivers:
            return []

        # Sort by arrival time, then driver_id for tie-breaking
        sorted_drivers = sorted(waiting_drivers, key=lambda d: (d['arrival'], d['driver_id']))

        assignments = []
        for driver in sorted_drivers:
            if not free:
                break
            cid = free.pop(0)
            self.assign(cid, driver['driver_id'])
            assignments.append((driver['driver_id'], cid))

        return assignments

    def active_drivers(self):
        """Return set of driver_ids currently on chargers."""
        return {did for did in self.chargers.values() if did is not None}

    def reset(self):
        """Reset all chargers to free."""
        self.chargers = {i: None for i in range(self.n_chargers)}
