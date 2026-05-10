import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config("Event Manager", layout="wide", initial_sidebar_state="expanded")


#session state stuff

if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

#loading the users

users_file = Path("users.json")
if users_file.exists():
   with open(users_file, "r") as f:
        users = json.load(f)
else:
    users = [
     {
    "id": "1",
    "email": "admin@event.edu",
    "full_name": "System Admin",
    "password": "123ssag@43AE",
    "role": "Admin"
    }
] 

#loading the events
events_file = Path("events.json")
if events_file.exists():
   with open(events_file, "r") as f:
        events = json.load(f)
else:
    events = [
  {
    "id": "1",
    "name": "Graduation",
    "date": "5-24-2026",
    "time": "10:00 AM",
    "location": "Newark",
    "description": "Graduation ceremony for the 2026 class.",
    "tickets": 500,
    "reserved": 120
  },
  {
    "id": "2",
    "name": "Music Festival",
    "date": "6-1-2026",
    "time": "8:00 PM",
    "location": "Philadelphia",
    "description": "Live music and entertainment.",
    "tickets": 100,
    "reserved": 50
  }
]
    
#sidebar ?
if st.session_state["logged_in"]:
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

if st.session_state["page"] == "login":
    st.title("Event Portal Login")

    email_input = st.text_input("Email")
    pass_input = st.text_input("Password", type="password")

    if st.button("Login", type="primary", use_container_width=True):
        with st.spinner("Logging in..."):
            time.sleep(2)
            found_user = None
            for user in users:
                if user["email"].lower() == email_input.lower() and user["password"] == pass_input:
                    found_user = user

            if found_user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = found_user
                st.session_state["role"] = found_user["role"]
                st.session_state["page"] = "dashboard"
                st.success("Welcome!")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.divider()

    if st.button("Create an Account", use_container_width=True):
        st.session_state["page"] = "register"
        st.rerun()

#registration 
if st.session_state["page"] == "register":
    col1,col2,col3 = st.columns([1,3,1])
    with col2:
        with st.container(border=True):

            st.header("Create Account")
            st.divider()

            email_input = st.text_input("Email", key="reg_email")
            name_input = st.text_input("Full Name", key="reg_name")
            pass_input = st.text_input("Password", type="password", key="reg_password")
            role_input = st.radio("Role", ["Attendee", "Admin"], key="reg_role")

            duplicate_email = False
            for u in users:
                if u["email"].lower() == email_input.lower():
                    duplicate_email = True

            if st.button("Register", type="primary", use_container_width=True):

                if not email_input or not name_input or not pass_input:
                    st.warning("Please fill in all fields")

                elif duplicate_email:
                    st.error("Account already exists")

                else:
                    with st.spinner("Creating account..."):
                        users.append({
                            "id": str(uuid.uuid4()),
                            "email": email_input,
                            "full_name": name_input,
                            "password": pass_input,
                            "role": role_input
                        })

                        with open(users_file, "w") as f:
                            json.dump(users, f)

                        st.success("Account created!")
                        time.sleep(2)
                        st.session_state["page"] = "login"
                        st.rerun()

            st.divider()

            if st.button("Back to Login", use_container_width=True):
                st.session_state["page"] = "login"
                st.rerun()
#admin

if st.session_state["page"] == "dashboard" and st.session_state["role"] == "Admin":
    st.title("Admin Dashboard")
    col1,col2,col3 = st.columns([2,3,2])
    st.divider()

# admin metrics ?
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("### Total Events")
        st.markdown(f"## {len(events)}")

    sold_out = 0
    for event in events:
        if event["reserved"] >= event["tickets"]:
            sold_out += 1

    with col2:
        st.markdown("### Sold Out")
        st.markdown(f"## {sold_out}")



    selected_event = None
    col1,col2 = st.columns([4,2])

    with col1:
        event_table = st.dataframe(events, on_select="rerun", selection_mode="single-row")
        selection = event_table.get("selection")
        rows = selection.get("rows", []) if selection else []

        if rows:
            selected_event = events[rows[0]]

    # details 
    with col2:

        if selected_event:
            st.markdown(f"**Name:** {selected_event['name']}")
            st.markdown(f"**Date:** {selected_event['date']}")
            st.markdown(f"**Tickets:** {selected_event['reserved']} / {selected_event['tickets']}")

            new_name = st.text_input("Event Name", selected_event["name"])
            new_tickets = st.number_input("Tickets", value=selected_event["tickets"], min_value=1)

            if st.button("Save Changes", type="primary", use_container_width=True):
                for event in events:
                    if event["id"] == selected_event["id"]:
                        event["name"] = new_name
                        event["tickets"] = new_tickets

                with open(events_file, "w") as f:
                    json.dump(events, f)

                st.success("Event Updated")
                time.sleep(2)
                st.rerun()

    tab1, tab2= st.tabs(["Create Event", "View and Update Event"])
    with tab1:
        st.subheader("Create New Event")
        name_input = st.text_input("Event Name", key="create_name")
        date_input = st.text_input("Date", key="create_date")
        time_input= st.text_input("Time", key="create_time")
        location_input = st.text_input("Location", key="create_location")
        description_input = st.text_area("Description", key="create_description")
        tickets_input = st.number_input("Tickets", min_value=1, key="create_ticket")

        if st.button("Create Event", type="primary", use_container_width=True, key="create_event"):
            events.append({
                "id": str(uuid.uuid4()),
                "name": name_input,
                "date": date_input,
                "time": time_input,
                "location": location_input,
                "description": description_input,
                "tickets": tickets_input,
                "reserved": 0
            })
            with open(events_file, "w") as f:
               json.dump(events, f, indent=4)

            st.success("Event created")
            time.sleep(2)
            st.rerun()



#attendee
if st.session_state["page"] == "events" and st.session_state["role"] == "Attendee":

    col1,col2,col3 = st.columns([2,3,2])
    
    st.header("Browse Events")

    st.divider()

    selected_event = None
    col1,col2 = st.columns([4,2])

    with col1:
        event_table = st.dataframe(events, on_select="rerun", selection_mode="single-row")
        selection = event_table.get("selection")
        rows = selection.get("rows", []) if selection else []

        if rows:
            selected_event = events[rows[0]]

    with col2:
        if selected_event:
            st.markdown(f"**Event:** {selected_event['name']}")
            st.markdown(f"Tickets Left: {selected_event['tickets'] - selected_event['reserved']}")

            if st.button("Reserve Ticket", type="primary", use_container_width=True):
                if selected_event["reserved"] < selected_event["tickets"]:
                    selected_event["reserved"] += 1
                    with open(events_file, "w") as f:
                        json.dump(events, f)
                    st.success("Ticket Reserved")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Sold Out")