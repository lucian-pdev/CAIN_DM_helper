#!/usr/bin/env python3
"""Handles tension escalation in the CAIN system."""

from functions.pressure import main as pressure

def main(session=None):
    """Increase tension and notify the user if the threshold is hit."""

    if session is None:
        print("No active session found.")
        return

    current_tension = session.getter("tension")
    if current_tension >= 3:
        print("\nTension is maxed out! Pressure must rise.")
        session = pressure(session)
        return session

    new_tension = current_tension + 1
    session.setter("tension", new_tension)

    print(f"\nTension rises... ({new_tension}/3)")
    if new_tension == 3:
        print("The air thickens. Pressure must now escalate.")
        session = pressure(session)
        session.setter("tension", 0)

    return session
