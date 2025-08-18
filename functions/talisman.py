#!/usr/bin/env python3
"""Create and track talismans across the session."""
       
def main(task_name=None, result="", progress=0, max=3, assigned="Party", session=None, tracker_type="talisman"):
    """Manage talismans as progress trackers."""

    if session is None:
        print("This command requires an ongoing session.")
        return None
    
    # Get current trackers
    trackers = session.getter("trackers") or {}

    # Display all trackers if no task name is given
    if task_name is None:
        if not trackers:
            print("""No active trackers.\n
            Create new talismans with 'talisman/hook <Task_Name> <Result> <Progress> <Max> <Assigned_To>'.\n
            If you need Task_name or result to have more than 1 word, surround them in single quotes ( '' ).""")
            return None

        print("\nCurrent Trackers:")
        for name, data in trackers.items():
            status = "Complete" if data["progress"] >= data["max"] else " In Progress"
            print(f"  {name} [{data['type']}] — {data['progress']}/{data['max']} | Assigned to: {data['assigned']} | {status}")
        print("\n[NOTE] You can remove trackers by signaling 'progress=999'.\n")
        return None

    # Safeties
    sanitize = lambda name: ''.join(c for c in name if c.isalnum() or c in [' ', '_', '-', "'"])
    task_name = sanitize(str(task_name.strip()))
    assigned = sanitize(str(assigned.strip()))
    result = sanitize(str(result.strip()))
    
    # Create or update the tracker
    if task_name not in trackers:
        # Create new tracker
        trackers[task_name] = {
            "type": tracker_type,
            "assigned": assigned,
            "progress": progress,
            "max": max,
            "result": result
        }
        session.setter("trackers", trackers)
        print(f"Created new {tracker_type}: {task_name} [{progress}/{max}]")
        return session

    # Increment progress if tracker exists
    if progress != 0 and progress != 999:
        trackers[task_name]["progress"] += progress
        session.setter("trackers", trackers)
        print(f"Progressed '{task_name}' to {trackers[task_name]['progress']}/{trackers[task_name]['max']}")

    # Check for completion
    if trackers[task_name]["progress"] >= trackers[task_name]["max"]:
        print(f"'{task_name}' is complete! Result: {trackers[task_name]['result']}")
        
    # Delete tracker if progress is 999
    if progress == 999:
        del trackers[task_name]
        session.setter("trackers", trackers)
        print(f"Removed tracker: {task_name}")
        return session

    return session
