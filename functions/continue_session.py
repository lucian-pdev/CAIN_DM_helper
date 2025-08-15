#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Load and continue from a saved file."""

import csv
from functions.__csv_loader import  Session
from pathlib import Path

def main(*args, session=None):
    curr_path = Path(__file__).parent.parent / 'data' / 'current_session.csv'
    try:
        with open(curr_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                print("File has errors in the data rows.")
                return
            
            # Check session object's state
            if session is not None:
                del session
            
            # Make session and establish the data of the previous session
            last_session = rows[-1]
            session = Session()
            
            # try to eval lists/dicsts, else keep as string
            for k,v in last_session.items():
                try:
                    session.SesDetails[k] = eval(v)
                except:
                    session.SesDetails[k] = v
            
            print('Loaded ongoing session.')
            return session
        
    except FileNotFoundError:
        print("No ongoing session file found.")
    except IOError as e:
        print(f"Error writing to current_session.csv:{e.strerror(e.errno)}")
        return
            
            