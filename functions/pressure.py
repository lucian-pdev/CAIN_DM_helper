#!/usr/bin/env python3
"""Handles pressure escalation in the CAIN system."""

def pressure(session=None):
    """Increase pressure, boost Sin HP, and trigger a major action."""

    if session is None:
        print("No active session found.")
        return

    # Increase pressure
    current_pressure = session.getter("pressure")
    new_pressure = current_pressure + 1
    session.setter("pressure", new_pressure)

    # Boost Sin HP
    sin_hp = session.getter("sin_HP")
    session.setter("sin_HP", sin_hp + 1)

    # Trigger major action
    print("\nThe Sin must act!")
    print(f"Pressure is now {new_pressure}. Sin HP increased to {sin_hp + 1}.")

    # Evolution check
    if new_pressure >= 6:
        sin = session.getter("sin")
        if sin:
            category = sin.get("category", "Unknown")
            print(f"\nThe Sin evolves into its next category: {category.upper()}!")
            print("The situation is dire. You are out of time.")

    return session
