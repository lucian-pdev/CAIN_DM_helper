#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Randomly choose a spiral and begin the loop.
"""
import random
from functions.__csv_loader import DataStore, Session
import functions.draw_decrees

# Load ONCE
_spirals = DataStore.spirals
_sins = DataStore.sins

def _find_spiral():
    spiral_name = input("Enter the name of the spiral you're looking for: ")
    for spiral in _spirals:
        if spiral['spiral_name'] == spiral_name:
            print(spiral)
            return
    print("Spiral not found.")


def main(*args, session=None):
    """
    Usage:
        draw spiral # random pick
        draw spiral <spiral_name> # specific spiral
    """
    
    # Randomly pick a spiral
    if not args:
        spiral = random.choice(_spirals)        
        
    # Specific spiral by ID
    elif len(args) == 1:
        spiral_name = args[0]
        spiral = _find_spiral(spiral_name)
        
        # Failsafe
        if not spiral:
            print(f"""Spiral {spiral_name} not found. Note: It's case-sensitive.\n
                  Options: {', '.join(s['spiral_name'] for s in _spirals)}""")
            return None
        
    sin = _sins[int(spiral['id'])-1]
    
    # REPL buffer for first phase of the game
    buffer = spiral["spiral_name"] + " and " + spiral["emotion"]
    print("\n")
    print(buffer.center(100))
    buffer = "NPCs: Player(s), Herald"
    print(buffer.center(100))
    print(f"-"*100, "\n", sep = "") 
    buffer = f"""\nLight shines into your eyes. A cave of dust, walls covered in featureless faces.\n The void in their mouths speaks:\n\n 
    \"The realm is engulfed by {spiral["spiral_name"]}, {spiral["world_twisting"]}\n Do you think you can handle: {spiral["trauma_themes"]}?\n"""
    buffer += f""" The monster you will hunt is categorized as {spiral["sin_type"]}.\n It is called {sin["sin_name"]} - {sin['title']}\n
    Pry open it's heart with blades of thought and whisper!\n
    The Questions to guide you shall be:\n{sin['question_1']}\n{sin['question_2']}\n{sin['question_3']}\n\n"""
    buffer += f"It seeks you too, but if you can corner it before it's ready, fate will be at your back.\n"
    buffer += f'Who will challenge the Spiral?\n'
    print(buffer)
    
    # Create the session object
    if session is None:
        session = Session()
    else:
        session = session
    
    # Assign values to the object
    session.setter('spiral', spiral)
    session.setter('sin', sin)
    session.setter('sin_HP', sin["initial_HP"])
    
    # Add the PCs to the session
    list_of_PCs = []
    # Make sure no PC names corrupt the code
    sanitize = lambda name: ''.join(c for c in name if c.isalnum() or c in [' ', '_', '-', "'"])


    # Loop for adding PCs
    while True:
        PC = sanitize(str(input("Enter a PC name: ").strip()))
        if not PC:
            if list_of_PCs:
                print(f"{len(list_of_PCs)} PC(s) added.")
            break
        list_of_PCs.append(PC)
    session.setter('PCs', list_of_PCs)
    
    # Call for a decree choice to get the players started
    buffer = f"\nTake this token, it will help you on your way.\n"
    print(buffer)
    functions.draw_decrees.main(session)  
    
    return session # return session object to carry on progress
