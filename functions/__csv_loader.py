#!/usr/bin/env python3
import csv
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).parent.parent / 'data'

@lru_cache(maxsize=None)
def load_csv(filename: str) -> list[dict]:
    """
    Load and cache the CSV file specified as argument.
    Subsequent calls with the same filename return the cached data.
    """
    path = DATA_DIR / f"{filename}.csv"
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))

class DataStore:
    spirals             = load_csv('spirals')
    sins                = load_csv('sins')
    decrees             = load_csv('decrees')
    events              = load_csv('events')
    current_session     = load_csv('current_session')
    previous_sessions   = load_csv('previous_sessions')
    reactions           = load_csv('reactions')
    afflictions         = load_csv('afflictions')
    traces              = load_csv('traces')

# Testing functions below   
def _test(a,b,c):
   file = a
   database = load_csv(file)
   print(f"{database[b][c]}")
   
def _find_sin(sin_type):
    _sins = load_csv('sins')
    for sin in _sins:
        if sin['sin_type'] == sin_type:
            return sin
        
        
class Session:
    def __init__(self):
        self.SesDetails = {'spiral':None, 'sin':None, 'PCs':None, 'events': [], 'decrees_counter':0, 'afflictions': {}, 'traces': {}}
        
    def __str__(self):
        return f"Session Details: {self.SesDetails}"
        
    def setter(self, key, value):
        if key not in self.SesDetails or self.SesDetails[key] is None:
            self.SesDetails[key] = value
        elif isinstance(self.SesDetails[key], dict):
            if isinstance(value, dict):
                self.SesDetails[key].update(value)
            else:
                print(f"Skipped update: expected dict for '{key}', got {type(value).__name__}")
        elif isinstance(self.SesDetails[key], list):
            self.SesDetails[key].append(value)
        elif isinstance(self.SesDetails[key], (str, int)):
            self.SesDetails[key] = value

    def deleter(self, key):
        del self.SesDetails[key]
        
    def getter(self, key):
        return self.SesDetails[key]
    
    def register_individual_PC(self, PC):
        self.SesDetails['PCs'].append(PC)
    
    def event_count(self):
        '''Return the number of events in the session'''
        return len(self.SesDetails['events'])
    
    def add_event(self, event):
        self.SesDetails['events'].append(event)
        
    def add_affliction(self, PC, affliction):
        '''Add key=PC, value=affliction'''
        self.SesDetails['afflictions'][PC] = affliction
        
    def add_trace(self, trace, execution):
        '''Add key=trace, execution=value'''
        self.SesDetails['traces'][trace] = execution
    
    
if __name__ == "__main__":
    print(f"Static test:{_test("spirals",3,"spiral_name")}")
    print(f"Static test:{_test("sins",5,"title")}")
    print(f"Static test:{_test("decrees",2,"effect")}")
        # conclusions: the csv loader creates a list of dictionaries
        # where each dictionary represents a row in the CSV file
        # as such, the first index is the row number (0-based)
        # and the second index is a key: the column header.
    
    import random
    _spirals = load_csv('spirals')
    spiral = random.choice(_spirals)
    sin = _find_sin(spiral['sin_type'])
    print(f"Random test:: spiral:{spiral['spiral_name']}, Sin type:{sin['sin_type']}, Sin's traces:{sin["trace_name"]}")
    