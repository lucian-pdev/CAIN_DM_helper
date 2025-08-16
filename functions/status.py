#!/usr/bin/env python3
"""Display a quick overview of the current session state."""

def status(session=None):
    """Show a formatted summary of all major session elements."""

    if session is None:
        print("This command requires an active session.")
        return

    sin = session.getter("sin") or {}
    spiral = session.getter("spiral") or {}
    pressure = session.getter("pressure")
    tension = session.getter("tension")
    boosters = session.getter("boosters_counter")
    afflictions = session.getter("afflictions") or {}
    traces = session.getter("traces") or {}
    events = session.getter("events") or []

    # Header
    print("\n" + "="*40)
    print("SESSION STATUS".center(40))
    print("="*40)

    # Core Info
    print(f"Spiral: {spiral.get('spiral_name', 'Unknown')}")
    print(f"Sin Type: {sin.get('sin_type', 'Unknown')} | Category: {sin.get('category', 'Unknown')}")
    print(f"Pressure: {pressure} | Tension: {tension}")
    print("-"*40)

    # Counters
    print(f"Boosters Used: {boosters}")
    print(f"Afflictions Active: {len(afflictions)}")
    print(f"Traces Summoned: {len(traces)}")
    print("-"*40)

    # Events
    if events:
        print("Events:")
        for i, event in enumerate(events):
            print(f"  [{i}] {event.get('event_name', 'Unnamed Event')}")
    else:
        print("Events: None")

    print("="*40)

    # Guidance
    print("\nFor detailed info:")
    print("  - Use sin to get info about the boss and associated commands.")
    print("  - Use afflictions, traces, talisman or hook to inspect status effects and trackers.")
    print("  - Use pressure and tension to update the hunt.")

    return None
