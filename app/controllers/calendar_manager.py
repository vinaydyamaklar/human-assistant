import datetime

# A simple in-memory "database" for the demo
CALENDAR_EVENTS = [
    {"title": "Project Meeting", "date": "2025-09-02", "time": "10:00"},
    {"title": "Demo with Client", "date": "2025-09-03", "time": "14:30"},
]

def perform_calendar_action(action: str, data: dict) -> str:
    """
    Performs a specified action on the calendar.
    """
    if action == "add_event":
        return _add_event(data)
    elif action == "list_events":
        return _list_events()
    else:
        raise ValueError(f"Unknown calendar action: {action}")

def _add_event(event_data: dict) -> str:
    """Adds a new event to the calendar."""
    required_fields = ["title", "date", "time"]
    if not all(field in event_data for field in required_fields):
        raise ValueError("Missing required fields for adding an event.")
    
    try:
        datetime.datetime.strptime(event_data["date"], "%Y-%m-%d")
        datetime.datetime.strptime(event_data["time"], "%H:%M")
        CALENDAR_EVENTS.append(event_data)
        return f"Event '{event_data['title']}' added successfully for {event_data['date']} at {event_data['time']}."
    except ValueError as e:
        raise ValueError(f"Invalid date or time format: {e}")

def _list_events() -> str:
    """Lists all upcoming events."""
    if not CALENDAR_EVENTS:
        return "You have no upcoming events."
    
    events_list = [f"- {event['title']} on {event['date']} at {event['time']}" for event in CALENDAR_EVENTS]
    return "Here are your upcoming events:\n" + "\n".join(events_list)