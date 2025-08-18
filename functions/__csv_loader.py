#!/usr/bin/env python3
import csv
from pathlib import Path
from functools import lru_cache

try:
    DATA_DIR = Path(__file__).parent.parent / 'data'    # Set the path to the data directory
except IOError as e:
    print(f"Error loading data directory: {e.strerror(e.errno)}")

@lru_cache(maxsize=None)          # This decorator caches the result of the function
def load_csv(filename: str) -> list[dict]:      # Return a list of dictionaries
    """
    Load and cache the CSV file specified as argument.
    Subsequent calls with the same filename return the cached data.
    """
    path = DATA_DIR / f"{filename}.csv"
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh)) # csv.DictReader(filehandler) reads every line and makes a dict using the first line as keys

class DataStore:    #WARNING: DataStore contains cached lists, not PATHs! DO NOT USE AS PATHS!
    """Each loac_csv call is cached by the decorator lru_cache; no doubling memory"""
    spirals             = load_csv('spirals')
    sins                = load_csv('sins')
    boosters            = load_csv('boosters')
    events              = load_csv('events')
    reactions           = load_csv('reactions')
    afflictions         = load_csv('afflictions')
    traces              = load_csv('traces')
    try:
        current_session     = load_csv('current_session')
        previous_sessions   = load_csv('previous_sessions')
    except FileNotFoundError:
        print("No save files found.")
        pass
    except:
        print("[Debug] A huge blunder happened in csv_loader.")
        pass


# This class is used to store the session details
class Session:      
    """A class to store the session details and pass it along to other functions."""
    def __init__(self):     # The main purpose of this object is to store these session details
        self.SesDetails = {'spiral':None, 'sin':None, 'sin_HP':0, 'PCs':None, 'events': [],
                           'boosters_counter':0, 'afflictions': {}, 'traces': {}, 'trackers': {},
                           "pressure":0, "tension":0}
        
    def __str__(self):
        return f"Session Details: {self.SesDetails}"
        
    def setter(self, key, value):
        '''Set the value of a key in the session details'''
        if key not in self.SesDetails or self.SesDetails[key] is None: # If the key's value doesn't exist
            self.SesDetails[key] = value
            
        elif isinstance(self.SesDetails[key], dict):    # If the key's value is a dictionary
            if isinstance(value, dict):                 # Failsafe, in case of wrong type
                self.SesDetails[key].update(value)
            else:                                          # Abandon if wrong type
                print(f"Skipped update: expected dict for '{key}', got {type(value).__name__}")
                
        elif isinstance(self.SesDetails[key], list):        # If the key's value is a list
            self.SesDetails[key].append(value)
            
        elif isinstance(self.SesDetails[key], (str, int)):  # If the key's value is a string or int
            self.SesDetails[key] = value

    def deleter(self, key):
        del self.SesDetails[key]
        
    def getter(self, key):
        return self.SesDetails[key]
    
    def register_individual_PC(self, PC):  # Use this only if you have to add a new PC after the session has started
        self.SesDetails['PCs'].append(PC)   # functions.draw_spiral will take care of the initial party
    
    def event_count(self):              # The game session is meant for 2-3 events, this will be used to keep track
        '''Return the number of events in the session'''
        return len(self.SesDetails['events'])
    
    def add_event(self, event):         # Keep a log of the events, to be able to maintain the narrative
        self.SesDetails['events'].append(event)
        
    def sin_hp(self, value):
        '''Modify the Hit Points of the boss'''
        try:
            self.SesDetails['sin_HP'] += int(value)
        except (ValueError, TypeError, ArithmeticError) as e:
            print("Error {e} has been detected, operation aborted.")
            pass
    
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

# Testing if called directly  
if __name__ == "__main__":
    print(f"Static test:{_test("spirals",3,"spiral_name")}")
    print(f"Static test:{_test("sins",5,"title")}")
    print(f"Static test:{_test("boosters",2,"effect")}")
        # conclusions: the csv loader creates a list of dictionaries
        # where each dictionary represents a row in the CSV file
        # as such, the first index is the row number (0-based)
        # and the second index is a key: the column header.
    
    import random
    _spirals = load_csv('spirals')
    spiral = random.choice(_spirals)
    sin = _find_sin(spiral['sin_type'])
    print(f"Random test:: spiral:{spiral['spiral_name']}, Sin type:{sin['sin_type']}, Sin's traces:{sin["trace_name"]}")
    