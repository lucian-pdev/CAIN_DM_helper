#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The command to issue a choice of decrees (power-ups) to the player."""

import random
from functions.__csv_loader import DataStore, Session

def populate_rarity_decrees():
    """Some decrees are more common than others."""
    common, rare, trade_off  = [], [], []
    
    for decree in DataStore.decrees:
        if decree['rarity'] == 'common':
            common.append(decree)
        elif decree['rarity'] == 'rare':
            rare.append(decree)
        elif decree['rarity'] == 'trade-off':
            trade_off.append(decree)

    return common, rare, trade_off

def randomize_decrees_by_rarity():
    """Randomize the choice of decrees by rarity."""
    common, rare, trade_off = populate_rarity_decrees()
    random.shuffle(common)
    random.shuffle(rare)
    random.shuffle(trade_off)
    
    # Calculate the chance to appear
    commons_chance = round(len(common) * (40/100))
    rares_chance = round(len(rare) * (30/100))
    
    # Create a pool of decrees to choose from
    pool = common[:commons_chance] + rare[:rares_chance] + trade_off[:rares_chance]
    random.shuffle(pool)
    
    return pool


def main(session=None, count=4):
    """Main function to draw decrees from the pool."""
    if session is None:        # If no session is provided, abort, this is not an independent command
        print("No session detected.")
        return
    
    # Randomize the choice of decrees by rarity
    pool = randomize_decrees_by_rarity()
    
    for i in range(count):    # Amount of decrees to offer as a choice to the players, default is 3
        name = str(pool[i]['name']).center(30)
        rarity_stackable = str("Rarity:" + pool[i]['rarity'] + "---" + "Stackable:" + pool[i]['stackable']).center(30)
        effect = "Effect: " + pool[i]['effect']
        downside = "Downside: " + pool[i]['downside'] if pool[i]['downside'] else "-"*30
        
        print(f"{name}\n{rarity_stackable}\n\n{effect}\n{downside}\n" 
              if i < 3 else 
              f"""\n Additional choice, for when a Player has one of the non-stackable options already:
              \n{name}\n{rarity_stackable}\n{effect}\n{downside}\n""")
    
    session.SesDetails['decrees_counter'] += 1
    
    return session  # Return session object to carry on progress