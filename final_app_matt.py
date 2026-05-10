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
        if st.button("Dashboard", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
        if st.button("Browse Events", use_container_width=True):
            st.session_state["page"] = "events"
            st.rerun()
        if st.button("Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
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

#admin

if st.session_state["page"] == "dashboard" and st.session_state["role"] == "Admin":

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
        st.markdown("### Event Details")

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



#attendee
if st.session_state["page"] == "events" and st.session_state["role"] == "Attendee":

    col1,col2,col3 = st.columns([2,3,2])
    with col2:
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