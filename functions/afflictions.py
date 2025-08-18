#!/usr/bin/env python3
"""Display current afflictions affecting players in the session."""

def main(session=None):
    """Show all active afflictions grouped by player."""

    if session is None:
        print("Session is required to view afflictions.")
        return

    current_afflictions = session.getter("afflictions")

    if not current_afflictions:
        print("No afflictions are currently active.")
        return

    print("\n Active Afflictions:")
    for player, affliction_list in current_afflictions.items():
        if affliction_list:
            afflict_str = ", ".join(affliction_list)
            print(f"  {player}: {afflict_str}")
        else:
            print(f"  {player}: No afflictions")

    print("\nUse 'sin afflict' to apply new ones.")
