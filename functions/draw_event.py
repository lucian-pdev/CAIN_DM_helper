#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Draws an event from the spiral and updates session object."""

from functions.__csv_loader import DataStore
import random
import re


def populate_events(session=None):
    """Grab all entries in event.csv"""

    if session is None:
        print("This command is not compatible with direct calling.")
        return None

    available_events = []   # list of all available events based on the current spiral
            
    current_spiral = session.getter("spiral")["spiral_name"]
    existing_event_names = {event['event_name'] for event in session.getter('events')}
    
    available_events = [
        event for event in DataStore.events
        if event["spiral_name"] == current_spiral and event["event_name"] not in existing_event_names
    ]

    return available_events   # returns a list of all events


def format_paragraph(text, word_count=15):
    """Formats a single line text into a readable paragraphs using punctuation and word count."""
    
    # Normalize spacing
    text = re.sub(r'\s+', ' ', text.strip())

    # Insert line breaks after sentence-ending punctuation
    text = re.sub(r'([.!?])\s+', r'\1\n', text)

    # Split into lines based on punctuation breaks
    lines = text.split('\n')

    formatted_lines = []
    for line in lines:
        words = line.split()
        # Chunk long lines by word count
        for i in range(0, len(words), word_count):
            chunk = ' '.join(words[i:i+word_count])
            formatted_lines.append(chunk)

    return '\n'.join(formatted_lines)


def main(session=None):
    """Main function to draw an event"""
    
    # yoink 1 event from the list
    available_events = populate_events(session)
    if len(available_events) > 0:
        choice = random.choice(available_events) 
    else:
        print("No available events remaining.")
        return None
    
    # add to object
    session.add_event(choice)

    # display the event to user
    buffer = choice["spiral_name"] + " -- " + choice["event_name"]
    print("\n")
    print(buffer.center(100))
    buffer = "NPCs: " + choice["NPCs"]
    print(buffer.center(100))
    print(f"-"*100, "\n", sep = "")
    
    buffer = "Introduction: " + format_paragraph(choice["initial_description"])
    print(f"{buffer}\n\n")
    
    buffer = "Remember the whispers of the Warden: " + choice["trauma_question"] + "\n" + format_paragraph(choice["question_implementation"])
    print(f"{buffer}\n")
    
    buffer = "Task: " + format_paragraph(choice["task"])
    print(f"{buffer}\n\n")
    
    buffer = "Hurdles: " + format_paragraph(choice["issues"])
    print(f"{buffer}\n\n")
    
    print("""Reminder: on event success call 'draw_booster' to reward the player(s).\n
            If pressure increased or the Sin has been injured, use "sin hp" to track it's value,
          """)
    
    return session