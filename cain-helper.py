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
and Windows (via setuptools console_script or .bat stub).
"""
import sys
import importlib
import os
import shlex
from functions.__csv_loader import DataStore

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

def dispatch(cmd, argv):
    """
    cmd: string, name of the command (e.g. 'draw_event')
    argv: list of strings, remaining command line arguments
    """
    if cmd == "help":  # If the user asks for help
        print(f"Available commands: {', '.join(commands)}")
        return
    elif cmd not in commands and cmd != 'help':
        print(f"Unknown command: {cmd}")
        print(f"Available commands: {', '.join(commands)}")
        sys.exit(1)
        

    # Import the module dynamically
    module = importlib.import_module(f'functions.{cmd}')
    
    # Call the main function of the module with remaining arguments
    if hasattr(module, 'main'):
        module.main(*argv)
    else:
        print(f"Module '{cmd}' does not have a main function.")
        sys.exit(1)
        
def repl():
    """ Interactive prompt loop. """
    os.system('clear' if os.name == 'posix' else 'cls')
    print(" "*3,"Welcome to the CAIN Helper REPL!")
    print("""Type 'help' for available commands or 'exit' to quit.\nThe structure I desgned for these CAIN sessions is:\n
          1) draw_spiral - to start a new spiral, this also gives your players the initial sin information.and decrees.
          2) draw_event - to draw an event from the spiral. I designed for 2 events per spiral, then the palace reveals itself for the boss fight.
                          But you can add more events if you like by running the draw_event command again.
          3) draw_decree - to draw a decree when the players complete an event.
          4) palace - to show the palace information in prepration for the boss fight.
          5) sin - to show the sin information,\n
          Mid-game commands: talisman, hook, traces, afflictions, show-status (of the session).
          Make use of 'chatter' and 'reactions' to add flavor to your game.\n
          6) demon - this will print the ending screen and close the loop.
          [OPTIONAL] You can continue an incomplete session with the 'continue_session' command.\n
          """)
    
    while True:
        try:
            user_input = input("> ")
            if user_input.strip().lower() in ['exit', 'quit']:
                break
            
            parts = shlex.split(user_input)
            cmd = parts[0]
            args = parts[1:]
            
            dispatch(cmd, args)
            
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
    # If this file is imported, we can still use the dispatch function
    # but we won't run the main() function automatically.
    print("cain-helper module loaded. Use dispatch() to call commands.")
    
# This allows for easy testing and importing without executing main()
# You can import this module in other scripts and use the dispatch function
# to call specific commands programmatically.