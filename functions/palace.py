 #!/usr/bin/env python3
"""Displays the Palace of the Sin in the CAIN system."""

from functions.draw_event import format_paragraph

def main(session=None):
    """Prints the palace name, description, and spiral effects."""

    if session is None:
        print("No active session found.")
        return

    sin = session.getter("sin")
    if not sin:
        print("No Sin data found in session.")
        return

    palace_name = sin.get("palace_name", "Unknown Palace").strip()
    palace_description = sin.get("palace_description", "No description available.")
    spiral_effects = sin.get("spiral_effects", "None recorded.")
    emotion = session.getter("spiral")["emotion"].upper()

    print(f"\nTHE LAIR OF {emotion}")
    print("=" * 40)
    print(f"Name: {palace_name.upper()}")
    print("\nDescription:")
    print(f"   {format_paragraph(palace_description.strip())}")
    print("\nSpiral Effects:")
    print(f"   {format_paragraph(spiral_effects.strip())}")
    print("=" * 40)
    print("The final confrontation draws near. Prepare your PCs for the descent into madness.\n")

    return session
