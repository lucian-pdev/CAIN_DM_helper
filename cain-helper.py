#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cain-helper.py

CAIN GM Helper
© 2025 lucian-pdev, distributed under the MIT License.

Usage:
    cain-helper <command> [args]
    cain-helper           # enter interactive mode

This file is the entrypoint for both Linux/Mac (via the shebang)
and Windows (via setuptools console_script or the .bat script file)

Python3 is mandatory to be installed.
"""

import sys
import importlib
import os
import shlex
from functions.__csv_loader import DataStore, Session

# Setting up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
functions_dir = os.path.join(script_dir, 'functions')
csv_dir = os.path.join(script_dir, 'data')

# Available commands
commands = {
    mod[:-3] # strip .py extension
    for mod in os.listdir(functions_dir)
    if mod.endswith('.py') and not mod.startswith('_')  # Exclude dunder files
        and mod != 'cain_helper.py'  # Exclude this file
}

# Grab data directory
data = {
    file[:-4]  # strip .csv extension
    for file in os.listdir(csv_dir)
    if file.endswith('.csv') and not file.startswith('_')
}

# Initialize the session object, it will be passed to modules. 
session = Session()

def dispatch(cmd, argv):
    """
    cmd: string, name of the command (e.g. 'draw_event')
    argv: list of strings, remaining command line arguments
    """
    global session # Global variable to store the current session
    
    # Supporting subcommands
    mod_name = cmd
    if len(argv) > 0 and hasattr(importlib.import_module(f'functions.{cmd}'), argv[0]):
        func_name = argv[0] if len(argv) > 0 else 'main'
        func_args = argv[1:] if len(argv) > 1 else []
    else:
        func_name = 'main'
        func_args = argv
    
    # Check if user wants/needs help
    if mod_name == "help":
        print(f"Available commands: {', '.join(commands)}, register_1_PC.")
        return None
    elif mod_name == "register_1_PC":
        sanitize = lambda name: ''.join(c for c in name if c.isalnum() or c in [' ', '_', '-', "'"])
        PC = sanitize(str(input("Enter a PC name: ").strip()))
        session.register_individual_PC(PC)
    elif mod_name not in commands:
        print(f"Unknown command: {mod_name}")
        print(f"Available commands: {', '.join(commands)}, register_1_PC.")
        return None

    # Import the module dynamically
    try:
        module = importlib.import_module(f'functions.{mod_name}')
    except Exception as e:
        print(f"Failed to import module 'functions.{mod_name}':{e}.")
        sys.exit(1)
    
    # Call the requested function
    # also pass session object if module expects it
    if hasattr(module, func_name):
        func = getattr(module, func_name)
        
        if 'session' in func.__code__.co_varnames:
            result = func(*func_args, session=session)
        else:
            result = func(*func_args)
        
        if isinstance(result, Session):
            session = result
        return session
    
    else:
        print(f"Module '{mod_name}' does not have a '{func_name}'function.")
        sys.exit(1)
        
def repl():     # Read-Eval-Print Loop = REPL, who would've thunk it
    """ Interactive prompt loop. """
    
    global session
    tension_reminder = 0
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print('\n'," "*3,"Welcome to the CAIN Helper REPL!\n")
    print("""
    Type 'help' for available commands or 'exit' to quit. The structure I designed for these CAIN sessions is:\n\
        1) draw_spiral  - to start a new spiral, this also gives your players the initial sin information.and boosters.
        2) draw_event   - to draw an event from the spiral. I designed for 2 events per spiral, then the palace reveals itself for the boss fight.
                          But you can add more events if you like by running the draw_event command again.
        3) draw_booster - to draw a booster when the players complete an event.
        4) palace       - to show the information about the boss's lair.
        5) sin          - to show the boss information and additional functions.\n
    Mid-game commands: talisman, hook, traces, afflictions, status (of the session).
    Make use of 'chatter' and 'reactions' to add flavor to your game.\n
          6) demon      - this will print the ending screen and close the loop.
          [NOTE] Make use of 'tension' and 'pressure' to keep track of the hunt's progress.\n
          [OPTIONAL] You can continue an incomplete session with the 'continue_session' command.\n
          [OPTIONAL] The party registration is done durin draw_spiral, for individual sign-ups use 'register_1_PC'.
          """)
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.strip().lower() in ['exit', 'quit']:
                break
            
            parts = shlex.split(user_input)
            cmd = parts[0]
            args = parts[1:]
            
            temp_session = dispatch(cmd, args)
            
            # saving progress
            if temp_session is not None:
                session = temp_session
                # functions.demon.save(session)     #NOTE: uncomment to enable auto-saving
                tension_reminder += 1
                if tension_reminder >= 3:
                    print("\nTension reminder: did the scene change or a risk die rolled a 1?")
                    tension_reminder = 0

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)
        
        except Exception as e:
            print(f"Error: {e}")

def main():
   # if no subcommand, drop into REPL
    if len(sys.argv) == 1:
        repl()
        return
    else:
        # Otherwise, dispatch the command
        cmd = sys.argv[1]
        args = sys.argv[2:]
        dispatch(cmd, args)
        
        
if __name__ == "__main__":
    main()
else:
    print("cain-helper module loaded. Use dispatch() to call commands.")
    
# You can import this module in other scripts and use the dispatch function
# to call specific commands programmatically.