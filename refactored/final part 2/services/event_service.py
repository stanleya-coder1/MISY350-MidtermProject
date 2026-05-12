#for events
import uuid
from pathlib import Path
from data.data_manager import (load_data, save_data, events_file)


def get_all_events():
    return load_data(events_file)


#admin view events
def get_events_by_admin(admin_id):
    events = load_data(events_file)
    return [
        event
        for event in events
        if event.get("created_by") == admin_id
    ]

#admin CRUD - create (create event)
def create_event(name, date, time, location, description, tickets, admin_user):
    events = load_data(events_file)

    new_event = {
        "id": str(uuid.uuid4()),
        "name": name,
        "date": str(date),
        "time": str(time),
        "location": location,
        "description": description,
        "tickets": tickets,
        "created_by": admin_user["id"],
        "created_by_name": admin_user["full_name"],
        "status": "Upcoming",
        "reservations": []
    }

    events.append(new_event)
    save_data(events_file, events)


#attendee CRUD - create (reserve ticket)
def reserve_ticket(event_id, user):
    events = load_data(events_file)

    for event in events:
        if event["id"] == event_id:
            if "reservations" not in event:
                event["reservations"] = []

            already_reserved = False

            for reservation in event["reservations"]:
                if reservation["user_id"] == user["id"]:
                    already_reserved = True

            if already_reserved:
                return "already_reserved"

            if len(event["reservations"]) >= event["tickets"]:
                return "sold_out"

            event["reservations"].append({
                "user_id": user["id"],
                "user_name": user["full_name"]
            })

            save_data(events_file, events)
            
            return "success"


#cancel ticket - attendee (CRUD - update/delete)
def cancel_ticket(event_id, user_id):
    events = load_data(events_file)

    for event in events:
        if event["id"] == event_id:
            event["reservations"] = [
                reservation
                for reservation in event.get("reservations", [])
                if reservation["user_id"] != user_id
            ]

    save_data(events_file, events)