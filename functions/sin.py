#!/usr/bin/env python3
"""Display information about the enemy boss."""

import random, time
from functions.__csv_loader import DataStore
from functions.draw_event import format_paragraph

def main(session=None):
    """Print boss name - type - HP - Ability names"""
    
    if session is None:
        print("This command requires an active session.")
        return None
    
    sname = session.getter("sin")["sin_name"]
    stitle = session.getter("sin")["title"]
    stype = session.getter("sin")["sin_type"]
    shp   = session.getter("sin_HP")
    scategory = session.getter("sin")("category")
    domain_1 = session.getter("sin")["domain_1"]
    domain_2 = session.getter("sin")["domain_2"]
    domain_3 = session.getter("sin")["domain_3"]
    
    buffer = sname + "--" + stitle
    print("\n")
    print(buffer.center(100))
    buffer = stype + " : CAT " + scategory
    print(buffer.center(100))
    buffer = "Execution Talisman: " + shp
    print(buffer.center(100))
    print(f"-"*100, "\n", sep = "")
    buffer = "Domains: " + domain_1 + ", " + domain_2 + ", " + domain_3
    print(f"-"*100, "\n", sep = "")
    
    print("Sin command arguments: show, hp, act, attack, threat, severe, afflict, trace, question.")
    return None

def show(session=None):
    """Print descriptions about the host"""
    
    if session is None:
        print("This command requires an active session.")
        return None
    
    host_description = session.getter("sin")["host_description"]
    form = session.getter("sin")["form"]
    
    print(
        f"""Born of {host_description.lower()}.\n
        This sin is of Type {form}"""
        )

    return None

def hp(session, value):
    """Modify boss's hp value, from damage or pressure."""
    
    if session is None:
        print("This command requires an active session.")
        return None

    session.sin_hp(value)
        
    return session

def act(session=None, roll=6):
    """The action engine for the boss's turn. Uses risk die to determine behavior."""

    if session is None:
        print("This command requires an active session.")
        return None

    sin_data = session.getter("sin")
    if not sin_data:
        print("No sin is set.")
        return None

    # Validate roll
    try:
        roll = int(roll)
    except ValueError:
        print("Risk die roll must be an integer.")
        return None

    if roll < 1 or roll > 6:
        print("Risk die must be between 1 and 6.")
        return None

    # Define action pools by roll value
    action_table = {
        1: ["severe", "trace"],
        2: ["domain", "afflict"],
        3: ["threat", "domain"],
        4: ["attack", "trace"],
        5: ["attack", "afflict"],
        6: ["trace", "afflict"]
    }

    available_actions = action_table.get(roll, [])
    if not available_actions:
        print("No actions available for this roll.")
        return None

    chosen_action = random.choice(available_actions)
    print(f"\nRisk Die Rolled: {roll}")
    print(f"Boss chooses to: {chosen_action.upper()}")

    time.sleep(3) # Give the user time to read the previous line
    
    # Execute the chosen action
    if chosen_action == "attack":
        attack(session)
    elif chosen_action == "threat":
        threat(session)
    elif chosen_action == "severe":
        severe(session)
    elif chosen_action == "afflict":
        afflict(session=session)  # Show affliction options
    elif chosen_action == "trace":
        trace(session=session)    # Show trace options

    return session


def attack(session=None):
    """Print stats of the boss's normal attacks"""
    
    if session is None:
        print("This command requires an active session.")
        return None

    attacks = session.getter("sin")["attacks"]
    attacks = attacks.split("; ")
    complications = session.getter("sin")["complications"]

    print("Attacks: " + attacks[0] + "\n" + attacks[1], sep="")
    print("Complications: " + format_paragraph(complications) + "\n")
    
    return None

def threat(session=None):
    """Print stats of the boss's threat attacks"""
    
    if session is None:
        print("This command requires an active session.")
        return None
    
    threats = session.getter("sin")["threats"]
    print("Threaths: " + format_paragraph(threats) + "\n")
    
    return None

def severe(session=None):
    """Print stats of the boss's severe attacks"""
    
    if session is None:
        print("This command requires an active session.")
        return None

    severe_attack_name = session.getter("sin")["severe_attack_name"]
    severe_attack_questions = session.getter("sin")["severe_attack_questions"]
    severe_attack_questions = severe_attack_questions.split(";")
    severe_attack_effects = session.getter("sin")["severe_attack_effects"]

    print(severe_attack_name.center(50))
    print(
        "Ask them: " + severe_attack_questions[0] + "\n"
          + severe_attack_questions[1] + "\n"
          + severe_attack_questions[2] + "\n\n"
          )
    print(format_paragraph(severe_attack_effects()) + "\n")

    return None


def afflict(player=None, affliction_index=None, session=None):
    """Inflict a debuff on the player. If no index is given, show available afflictions."""

    if session is None:
        print("This command requires an active session.")
        return

    sin_data = session.getter("sin")
    if not sin_data:
        print("No sin is set.")
        return

    afflictions = sin_data.get("afflictions", "")
    afflictions = [aff.strip() for aff in afflictions.split("; ") if aff.strip()]

    if not afflictions:
        print("No afflictions found for this sin.")
        return

    # Show afflictions if no index is provided
    if affliction_index is None or player is None:
        print(f"\nAvailable afflictions for sin type: {sin_data.get('sin_type', 'Unknown')}")
        for i, aff in enumerate(afflictions):
            print(f"  [{i}] {aff}")
        print("\nTo afflict: afflict(player_name, affliction_index)")
        return

    # Validate player name
    valid_players = session.getter("PCs") or []

    if player not in valid_players:
        print(f"Player '{player}' not found in session PCs.")
        print(f"Available players: {', '.join(valid_players) if valid_players else 'None'}")
        return
    
    # Validate index
    try:
        index = int(affliction_index)
    except ValueError:
        print("Affliction index must be an integer.")
        return

    if index < 0 or index >= len(afflictions):
        print("Affliction index out of range.")
        return

    affliction = afflictions[index]
    
    # Apply affliction to player in session
    afflicted_players = session.getter("afflictions") or {}

    if player not in afflicted_players:
        afflicted_players[player] = []

    afflicted_players[player].append(affliction)
    session.setter("afflictions", afflicted_players)

    print(f"{player} is now afflicted with: {affliction}")


    return session

def trace(index_for_name=None, value_for_talisman=None, session=None):
    """Summon a trace by index and HP value, or show options if no input is given."""

    if session is None:
        print("Session is required.")
        return

    current_sin = session.getter("sin")
    if not current_sin:
        print("No sin is set.")
        return

    sin_type = session.getter("sin")["sin_type"]
    matched_traces = [trace for trace in DataStore.traces if trace["sin_type"] == sin_type]

    if not matched_traces:
        print("No traces found for this sin type.")
        return

    # Show options if no input is provided
    if index_for_name is None or value_for_talisman is None:
        print(f"\nAvailable traces for sin type: {sin_type}")
        for i, trace in enumerate(matched_traces):
            name = trace["trace_name"]
            hp_pool = [int(hp.strip()) for hp in trace["talisman"].split(";") if hp.strip().isdigit()]
            print(f"  [{i}] {name} — HP tiers: {hp_pool}")
        print("\nTo summon: trace(index_for_name, value_for_talisman)")
        return

    # Validate index and talisman
    try:
        index = int(index_for_name)
        hp = int(value_for_talisman)
    except ValueError:
        print("Invalid input. Both index and talisman must be integers.")
        return

    if index < 0 or index >= len(matched_traces):
        print("Index out of range.")
        return

    trace_obj = matched_traces[index]
    name = trace_obj["trace_name"]
    hp_pool = [int(hp.strip()) for hp in trace_obj["talisman"].split(";") if hp.strip().isdigit()]

    if hp not in hp_pool:
        print(f"Invalid HP value. Choose from: {hp_pool}")
        return

    session.setter("traces", {name: hp})
    print(f"Summoned trace: {name} with HP {hp}")
    
    return session


def question(session=None):
    """Prints Trauma Questions and answers related to Boss"""
    
    if session is None:
        print("This command requires an active session.")
        return None
    
    print(session.getter("sin")["question_1"])
    print(session.getter("sin")["question_1_answer"])
    print(session.getter("sin")["question_2"])
    print(session.getter("sin")["question_2_answer"])
    print(session.getter("sin")["question_3"])
    print(session.getter("sin")["question_3_answer"])
    
    return None
