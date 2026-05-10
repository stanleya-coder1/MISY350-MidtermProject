import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(
    page_title="Event Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

#session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "login"

#files
users_file = Path("users.json")
events_file = Path("events.json")


def load_users():
    if users_file.exists():
        with open(users_file, "r") as f:
            return json.load(f)

    return []


def save_users(users):
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)


def load_events():
    if events_file.exists():
        with open(events_file, "r") as f:
            return json.load(f)

    return []


def save_events(events):
    with open(events_file, "w") as f:
        json.dump(events, f, indent=4)


users = load_users()
events = load_events()


def login_user(email, password):
    for user in users:

        if (
            user["email"].lower() == email.lower() and user["password"] == password):
            return user
    return None


def get_reserved_count(event):
    return len(event.get("reservations", []))


def get_tickets_left(event):
    return event["tickets"] - get_reserved_count(event)


def user_has_ticket(event, user_id):
    for reservation in event.get("reservations", []):
        if reservation["user_id"] == user_id:
            return True
    return False


#sidebar
if st.session_state.logged_in:
    with st.sidebar:
        st.title("Event Manager")

        st.success(
            f"Logged in as: "f"{st.session_state.user['full_name']}")

        st.caption(f"Role: {st.session_state.role}")

        st.divider()

        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("Find Events", use_container_width=True):
            st.session_state.page = "events"
            st.rerun()

        if st.button("My Tickets", use_container_width=True):
            st.session_state.page = "tickets"
            st.rerun()

        st.divider()

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.page = "login"
            st.rerun()


#login
if st.session_state.page == "login":
    st.title("Event Manager Login")



    with st.container(border=True):
        st.subheader("Login")

        email_input = st.text_input("Email")

        password_input = st.text_input("Password", type="password")

        if st.button("Login", type="primary",use_container_width=True):
            if not email_input or not password_input:
                    st.error("Please complete all fields")
        else:
            with st.spinner("Logging in..."):
                time.sleep(1)

                found_user = login_user(email_input,password_input)

                if found_user:
                    st.session_state.logged_in = True
                    st.session_state.user = found_user
                    st.session_state.role = found_user["role"]
                    st.session_state.page = "dashboard"

                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
else:
    st.error("Invalid credentials")

#Adfmin Dashboard
if (st.session_state.page == "dashboard" and st.session_state.role == "Admin"):
    st.title("Admin Dashboard")

    total_reserved = sum(get_reserved_count(event) for event in events)

    sold_out = len([e for e in events if get_tickets_left(e) == 0])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Events", len(events))

    with col2:
        st.metric("Tickets Reserved", total_reserved)

    with col3:
        st.metric("Sold Out Events", sold_out)

    st.divider()

    tab1, tab2 = st.tabs([
        "Manage Events",
        "Create Event"
    ])

    #manage event
    with tab1:
        search = st.text_input("Search Events")

        filtered_events = []

        for event in events:
            if search.lower() in event["name"].lower():
                filtered_events.append(event)

        cols = st.columns(2)

        for i, event in enumerate(filtered_events):
            with cols[i % 2]:
                with st.container(border=True):
                    st.subheader(event["name"])
                    st.caption(
                        f"{event['date']}"
                        f"{event['time']}"
                    )

                    st.write(event["description"])
                    remaining = get_tickets_left(event)
                    st.metric("Tickets Left",remaining)

                    if remaining == 0:
                        st.error("Sold Out")

                    elif remaining <= 10:
                        st.warning("Almost Full")

                    else:
                        st.success("Available")

                    with st.expander("Edit Event"):

                        with st.form(
                            f"edit_form_{event['id']}"
                        ):

                            new_name = st.text_input("Event Name", value=event["name"])
                            new_location = st.text_input("Location",value=event["location"])
                            new_description = st.text_area("Description",value=event["description"])
                            new_tickets = st.number_input("Ticket Capacity", min_value=1, value=event["tickets"])

                            save_btn = st.form_submit_button("Save Changes")

                            if save_btn:
                                if not new_name.strip():
                                    st.error("Event name required")
                                else:
                                    event["name"] = new_name
                                    event["location"] = new_location
                                    event["description"] = new_description
                                    event["tickets"] = new_tickets

                                    save_events(events)

                                    st.success("Event updated!")

                                    st.rerun()

                    if st.button("Delete Event", key=f"delete_{event['id']}"):
                        events = [
                            e for e in events
                            if e["id"] != event["id"]
                        ]

                        save_events(events)

                        st.success("Event deleted")

                        st.rerun()

    #create event
    with tab2:
        st.subheader("Create New Event")
        with st.form("create_event_form"):
            name = st.text_input("Event Name")
            event_date = st.date_input("Event Date")
            event_time = st.time_input("Event Time")
            location = st.text_input("Location")
            description = st.text_area("Description")
            tickets = st.number_input("Ticket Amount", min_value=1, step=1)

            submitted = st.form_submit_button("Create Event")

            if submitted:
                if name == "":
                    st.error("Event name required")
                elif location == "":
                    st.error("Location required")
                else:
                    new_event = {
                        "id": str(uuid.uuid4()),
                        "name": name,
                        "date": str(event_date),
                        "time": str(event_time),
                        "location": location,
                        "description": description,
                        "tickets": tickets,
                        "reservations": []
                    }

                    events.append(new_event)

                    save_events(events)

                    st.success(
                        "Event created successfully!"
                    )

                    st.rerun()


#find/search events
if (st.session_state.page == "events" and st.session_state.role == "Attendee"):
    st.title("Search Events")

    search = st.text_input("Search Events")

    filtered_events = []

    for event in events:
        if search.lower() in event["name"].lower():
            filtered_events.append(event)

    cols = st.columns(2)
    for i, event in enumerate(filtered_events):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(event["name"])
                st.caption(
                    f"{event['date']} • "
                    f"{event['time']}"
                )

                st.write(f"{event['location']}")
                st.write(event["description"])

                remaining = get_tickets_left(event)

                st.metric("Tickets Left", remaining)

                if remaining == 0:
                    st.error("Sold Out")
                elif remaining <= 10:
                    st.warning("Almost Full")
                else:
                    st.success("Available")

                already_reserved = user_has_ticket(event, st.session_state.user["id"])

                if already_reserved:
                    st.write("You already reserved this event")
                else:
                    if st.button("Reserve Ticket", key=f"reserve_{event['id']}", use_container_width=True):
                        if remaining > 0:
                            reservation = {
                                "user_id": (
                                    st.session_state.user["id"]
                                ),
                                "email": (
                                    st.session_state.user["email"]
                                ),
                                "reserved_at": str(
                                    datetime.now()
                                )
                            }

                            if "reservations" not in event:
                                event["reservations"] = []

                            event["reservations"].append(reservation)
                            save_events(events)

                            st.success("Ticket reserved!")
                            st.rerun()
                        else:
                            st.error("Event sold out")


# my tickets
if (st.session_state.page == "tickets" and st.session_state.role == "Attendee"):
    st.title("My Tickets")

    current_user = st.session_state.user

    user_events = []

    for event in events:
        for reservation in event.get("reservations", []):
            if (reservation["user_id"] == current_user["id"]):
                user_events.append(event)

    if not user_events:
        st.info("You have not reserved any tickets yet.")

    else:
        cols = st.columns(2)
        for i, event in enumerate(user_events):
            with cols[i % 2]:
                with st.container(border=True):
                    st.subheader(event["name"])

                    st.write(f"{event['date']}")
                    st.write(f"{event['time']}")
                    st.write(f"{event['location']}")

                    st.success("Reservation Confirmed")