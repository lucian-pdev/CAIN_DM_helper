#!/usr/bin/env python3
"""Display information about currently summoned enemy traces."""

def main(session=None):
    """Prints the status of currently existing traces from the session."""

    if session is None:
        print("Session is required to check trace status.")
        return

    active_traces = session.getter("traces")

    if not active_traces:
        print("No traces are currently summoned.")
        return

    print("\nActive Traces:")
    for i, trace in enumerate(active_traces):
        name = trace.get("trace_name", "Unknown")
        hp = trace.get("hp", "?")
        tier = trace.get("tier", "Unranked")
        status = trace.get("status", "Active")

        print(f"  [{i}] {name} — HP: {hp} | Tier: {tier} | Status: {status}")

    print("\n\n*Note: Use 'sin trace' to summon new ones.")
