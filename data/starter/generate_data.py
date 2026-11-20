"""Generate synthetic EV charging requests and private driver properties."""

import argparse
import csv
import os
import random


RULES = ["Release", "Hold", "Reciprocal", "Fee_aware"]
DEMANDS = {
    "low": (720, 12),       # (total requests, requests per day over 60 days)
    "medium": (1440, 24),
    "high": (2160, 36)
}


def generate(seed, output_dir, urgent_prior=0.30):
    os.makedirs(output_dir, exist_ok=True)
    rng = random.Random(seed)

    # 1. Generate 40 drivers
    drivers = []
    num_drivers = 40
    for i in range(num_drivers):
        driver_id = f"D{i:02d}"
        is_urgent = rng.random() < urgent_prior
        dtype = "Urgent" if is_urgent else "Flexible"
        rule = rng.choice(RULES)
        v = 3 if is_urgent else 2
        w = 3 if is_urgent else 1
        h = 1 if is_urgent else 2
        drivers.append({
            "driver_id": driver_id,
            "type": dtype,
            "v": v,
            "w": w,
            "h": h,
            "private_strategy": rule
        })

    drivers_file = os.path.join(output_dir, "drivers_private.csv")
    with open(drivers_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["driver_id", "type", "v", "w", "h", "private_strategy"])
        writer.writeheader()
        writer.writerows(drivers)

    # 2. Generate sessions for low, medium, high
    sessions = []
    for demand, (total_reqs, reqs_per_day) in DEMANDS.items():
        for day in range(60):
            # Select random drivers for this day
            active_dids = rng.sample([d["driver_id"] for d in drivers], reqs_per_day)
            for did in active_dids:
                # Arrival slot in 0..13
                arrival = rng.randint(0, 13)
                # Departure slot in arrival+2..16
                departure = rng.randint(arrival + 2, 16)
                # Requested energy: 3, 6, or 9 kWh
                # Must be feasible to charge at 3 kWh/slot within (departure - arrival)
                max_possible_slots = departure - arrival
                max_kwh = min(9, max_possible_slots * 3)
                possible_kwh = [k for k in [3, 6, 9] if k <= max_kwh]
                if not possible_kwh:
                    possible_kwh = [3]
                    departure = min(16, arrival + 1)
                req_kwh = rng.choice(possible_kwh)

                sessions.append({
                    "driver_id": did,
                    "demand": demand,
                    "day": day,
                    "arrival": arrival,
                    "departure": departure,
                    "requested_kwh": float(req_kwh)
                })

    sessions_file = os.path.join(output_dir, "sessions_public.csv")
    with open(sessions_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["driver_id", "demand", "day", "arrival", "departure", "requested_kwh"])
        writer.writeheader()
        writer.writerows(sessions)

    print(f"Generated {len(drivers)} drivers and {len(sessions)} sessions in {output_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--seed", type=int, default=0, help="Random seed")
    parser.add_argument("--urgent-prior", type=float, default=0.30, help="Urgent driver prior probability")
    args = parser.parse_args()

    generate(args.seed, args.output, args.urgent_prior)


if __name__ == "__main__":
    main()
