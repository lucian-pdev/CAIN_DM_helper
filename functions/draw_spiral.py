#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Randomly choose a spiral and begin the loop.
"""
import random
from functions.__csv_loader import DataStore

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

def _find_sin():
    sin_type = input("Enter the type of sin you're looking for: ")
    for sin in _sins:
        if sin['sin_type'] == sin_type:
            print(sin)
            return
    print("Sin not found.")


def main(*args):
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
        
        if not spiral:
            print(f"""Spiral {spiral_name} not found. Note: It's case-sensitive.\n
                  Options: {', '.join(s['spiral_name'] for s in _spirals)}""")
            return
    sin = _sins[int(spiral['id'])-1]
    
    # REPL output for first phase of the game
    output = f"""Light shines into your eyes. A cave of dust, walls covered in featureless faces.\n The void in their mouths speaks:\n\n \"The realm is engulfed by a {spiral["spiral_name"]}, {spiral["world_twisting"]}\n Do you think you can handle {spiral["trauma_themes"]}?\n"""
    output += f""" The monster you will hunt is categorized as {spiral["sin_type"]}.\n It is called {sin["sin_name"]} - {sin['title']}\nPry open it's heart with blades of thought and whisper!\n
    The Questions to guide you shall be:\n{sin['question_1']}\n{sin['question_2']}\n{sin['question_3']}\n\n"""
    output += f"It seeks you too, but if you can corner it before it's ready, fate will be at your back.\n"
    output += f"Take this token, it will help you on your way.\n"
    decrees_count = 1
    
    print(output)
    return spiral, sin, decrees_count
