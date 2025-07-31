#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the Permanent NPC: Demon. It will endand save the running session to a CSV file.
"""
import csv, os
from functions.__csv_loader import DataStore


def main(*args, session=None):
    if session is None:
        print("No session to save.")
        return
    
    # Save to previous_sessions.csv (append)
    prev_path = os.path.join(os.path.dirname(__file__), '../data/previous_sessions.csv')
    prev_path = os.path.abspath(prev_path)
    fieldnames = list(session.SesDetails.keys())

    # Check if file exists to write header
    write_header = not os.path.exists(prev_path) or os.stat(prev_path).st_size == 0

    with open(prev_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(session.SesDetails)

    # Optionally, clear current_session.csv
    curr_path = os.path.join(os.path.dirname(__file__), '../data/current_session.csv')
    curr_path = os.path.abspath(curr_path)
    with open(curr_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # Empty file with header

    print("Session saved to previous_sessions.csv and current_session.csv cleared.")
    
    
def save_current_session(session):
    curr_path = os.path.join(os.path.dirname(__file__), '../data/current_session.csv')
    curr_path = os.path.abspath(curr_path)
    fieldnames = list(session.SesDetails.keys())
    with open(curr_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(session.SesDetails)