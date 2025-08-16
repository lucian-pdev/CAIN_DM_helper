#!/usr/bin/env python3
"""Manage detrimental progress trackers (hooks)."""

from functions.talisman import main as talisman_main

def main(task_name=None, max=3, progress=0, assigned="Party", result="Improvise, quickly!", session=None):
    """Create or update a hook tracker using the talisman system."""
    
    # Hooks are negative tasks — if filled, they trigger penalties
    return talisman_main(
        task_name=task_name,
        max=max,
        progress=progress,
        assigned=assigned,
        session=session,
        tracker_type="hook",
        result="Penalty triggered: " + result 
    )
