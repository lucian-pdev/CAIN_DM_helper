#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains the Permanent NPC: Demon. It will endand save the running session to a CSV file.
"""

import csv, os
from functions.__csv_loader import DataStore
from pathlib import Path


def main(*args, session=None):
    if session is None:
        print("No session to save.")
        return
    
    # Save to previous_sessions.csv (append)
    prev_path = Path(__file__).parent.parent / 'data' / 'previous_sessions.csv'
    fieldnames = list(session.SesDetails.keys())

    # Check if file exists to write header
    write_header = not prev_path.exists() or prev_path.stat().st_size == 0
    try:
        with open(prev_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(session.SesDetails)
    except IOError as e:
        print(f"Error writing to previous_sessions.csv:{e.strerror(e.errno)}")
        return

    # Clear current_session.csv
    curr_path = Path(__file__).parent.parent / 'data' / 'current_session.csv'
    try:
        with open(curr_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()  # Empty file with header
    except IOError as e:
        print(f"Error writing to current_session.csv:{e.strerror(e.errno)}")
        return

    # Flair text for the end of a loop.
    output = f"""\n\n There's a feeling inside of you. Foreign, invading, and overwhelming.\n
    There is no sound, no smell, no pain, or vision that could describe it.\n
    It is grasping your soul, crushing and consuming bits and parts of it, anything that has been stained by it.\n
    You mind blanks out, and your body is consumed by the darkness.\n\n
    """
    print(output)
    print("Session saved to previous_sessions.csv and current_session.csv has been cleared.\n")
    
def save(session):  # save_current_session
    curr_path = Path(__file__).parent.parent / 'data' / 'current_session.csv'
    fieldnames = list(session.SesDetails.keys())
    with open(curr_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(session.SesDetails)