#for events
import uuid
from pathlib import Path
from datetime import datetime
from data.data_manager import (load_data, save_data, events_file)

def structured_event_date(event): #need to determine if event is past
    date_str = str(event.get("date", "")).strip()
    #mm-dd-yyyy
    if len(date_str) == 10 and date_str[4] == "-" and date_str[7] == "-":
        parts = date_str.split("-")
        if len(parts) == 3:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            return datetime(year, month, day).date()

    elif "-" in date_str:
        parts = date_str.split("-")
        if len(parts) == 3:
            month = int(parts[0])
            day = int(parts[1])
            year = int(parts[2])
            return datetime(year, month, day).date()
    return None


def get_event_status(event):
    if event.get("status") == "Cancelled":
        return "Cancelled"
    event_date = structured_event_date(event)
    if event_date and event_date < datetime.today().date():
        return "Past"
    return "Upcoming"


def get_reservation_status(event, user_id):
    for reservation in event.get("reservations", []):
        if reservation["user_id"] == user_id:
            # User canceled
            if reservation.get("status") == "Cancelled":
                return "Cancelled"
            # Event canceled
            if event.get("status") == "Cancelled":
                return "Cancelled Event"
            # Past
            if get_event_status(event) == "Past":
                return "Past"
            return "Reserved"
    return None


def get_tickets_left(event):
    return event["tickets"] - len(event.get("reservations", []))

def user_has_ticket(event, user_id):
    for reservation in event.get("reservations", []):
        if reservation["user_id"] == user_id:
            return True
    return False


# EVENT MANAGEMENT SYSTEM/ admin CRUD
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


#admin CRUD - read (get events by admin/user)
def get_events_by_admin(admin_id):
    events = load_data(events_file)
    return [
        event
        for event in events
        if event.get("created_by") == admin_id
    ]

def get_all_events():
    return load_data(events_file)



#admin CRUD - update (update event)
def update_event(event_id, updated_name, updated_tickets, updated_location, updated_description):
    events = load_data(events_file)

    for event in events:
        if event["id"] == event_id:
            event["name"] = updated_name
            event["tickets"] = updated_tickets
            event["location"] = updated_location
            event["description"] = updated_description

    save_data(events_file, events)


#admin CRUD - delete (delete event)
def delete_event(event_id):
    events = load_data(events_file)
    events = [event for event in events if event["id"] != event_id]
    save_data(events_file, events)


# RESERVATION SYSTEM/ attendee CRUD
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
                "user_name": user["full_name"],
                "user_email": user["email"]
            })

            save_data(events_file, events)
            return "success"


#attendee CRUD - delete (cancel reservation)
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

