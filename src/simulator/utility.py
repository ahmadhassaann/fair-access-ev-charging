"""Utility = v * kWh - w * waiting_slots + h * idle_slots - F * idle_slots.
Types: Urgent (v=3, w=3, h=1), Flexible (v=2, w=1, h=2).
Report utility before and after penalties separately.
"""


def utility(v, w, h, fee, kwh, wait_slots, idle_slots):
    before = v * kwh - w * wait_slots + h * idle_slots
    return before, before - fee * idle_slots
