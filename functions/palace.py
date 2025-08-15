#!/usr/bin/env python3
"""Display information about the enemy boss's lair."""
#TODO: palace function

from functions.__csv_loader import DataStore


def main(session=None):
    """Describe's the palace."""
    
    if session is None:
        print("This command requires an active session.")
        return None
    
    palace_name = session.getter("sin")["palace_name"]
    palace_description = session.getter("sin")["palace_description"]