#handles reservations

import uuid
from pathlib import Path
from data.data_manager import (load_data, save_data, events_file)


#reserve ticket - attendee (CRUD - create)
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