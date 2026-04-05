import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time




st.set_page_config(page_title="Event Manager", layout="centered")




if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None 
if "page" not in st.session_state:
    st.session_state["page"] = "login"




#json_path = Path("event.json")
#if json_path.exists(): 
#   with open(json_path, "r") as f:
#        event = json.load(f)


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


if not st.session_state["logged_in"]:
    st.title("Log in")

    tab1, tab2 = st.tabs(["Login", "Registration"])
    with tab1:
        st.subheader("Login")
        email_input = st.text_input("Email", key="login_email")
        pass_input = st.text_input("Password", type="password", key="login_password")
            
        if st.button("Login"):
            with st.spinner("Logging in..."):
                time.sleep(2)
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == pass_input:
                        found_user = user
                        break
                    
                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user["role"]
                    st.session_state["page"] = "home"
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    with tab2:
        st.subheader("Register")
        email_input = st.text_input("Email", key="reg_email")
        name_input = st.text_input("Full Name", key="reg_name")
        pass_input = st.text_input("Password", type="password", key="reg_password")
        role_input = st.selectbox("Role", ["Attendee", "Admin"], key="reg_role")

        if st.button("Create Account"):
            users.append({
                "id": str(uuid.uuid4()),
                "email": email_input,
                "full_name": name_input,
                "password": pass_input,
                "role": role_input
            })
            with open(users_file, "w") as f:
                json.dump(users, f, indent=4)
                with open(users_file, "r") as f:
                    users = json.load(f)
            st.success("Account created!")






if st.session_state["role"] == "Attendee":
    if st.session_state["page"] == "home":
        st.markdown("welcome! View Upcoming Events!")
        if st.button("Event Portal", key="view_events_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "attendee_portal"
            st.rerun()
 
    if st.session_state["page"] == "attendee_portal":

        st.title("Find Events")

        event_names = []
        for event in events:
            event_names.append(event["name"])

        selected_event_name = st.selectbox("Select Event", event_names)

        selected_event = None
        for event in events:
            if event["name"] == selected_event_name:
                selected_event = event

        if selected_event:
            st.markdown(f"Event: {selected_event['name']}")
            st.write(f" Date/Time: {selected_event['date']} at {selected_event['time']}")
            st.write(f"Location:{selected_event['location']}")
            st.write(f"{selected_event['description']}")
            st.write(f"Tickets Available: {selected_event['tickets'] - selected_event['reserved']}")

            if st.button("Reserve Ticket"):
                if selected_event["reserved"] < selected_event["tickets"]:
                    selected_event["reserved"] += 1
                    with open(events_file, "w") as f:
                        json.dump(events, f, indent=4)
                    with open(events_file, "r") as f:
                        events = json.load(f)
                    st.rerun()
                    st.success("Ticket reserved!")
                else:
                    st.error("Sold out")

                




if st.session_state["role"] == "Admin":
    if st.session_state["page"] == "home":
        st.markdown("welcome! This is the Admin Dashboard")
        if st.button("Dashboard", key="dashboard_view_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()

        if events_file.exists():
            with open(events_file, "r") as f:
                events = json.load(f)
        else:
            events = []
        

    tab1, tab2, tab3 = st.tabs(["Create Event", "View Events", "Update Event"])
    with tab1:
        st.subheader("Create New Event")
        name_input = st.text_input("Event Name", key="create_name")
        date_input = st.text_input("Date", key="create_date")
        time_input= st.text_input("Time", key="create_time")
        location_input = st.text_input("Location", key="create_location")
        description_input = st.text_area("Description", key="create_description")
        tickets_input = st.number_input("Tickets", min_value=1, key="create_ticket")

        if st.button("Create Event"):
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
               with open(users_file, "r") as f:
                    users = json.load(f)
            st.success("Event created")
            st.rerun()
            





    with tab3:
        st.subheader("View and Update Event")

        event_names = [event["name"] for event in events]
        selected_name = st.selectbox("Select Event", event_names)

        selected_event = None
        for event in events:
            if event["name"] == selected_name:
                selected_event = event

        if selected_event:
            new_name = st.text_input("Event Name", selected_event["name"])
            new_date = st.text_input("Date", selected_event["date"])
            new_time = st.text_input("Time", selected_event["time"])
            new_location = st.text_input("Location", selected_event["location"])
            new_description = st.text_area("Description", selected_event["description"])
            new_tickets = st.number_input("Tickets", value=selected_event["tickets"], min_value=1)

            if st.button("Save Changes"):

                for event in events:
                    if event["id"] == selected_event["id"]:
                        event["name"] = new_name
                        event["date"] = new_date
                        event["time"] = new_time
                        event["location"] = new_location
                        event["description"] = new_description
                        event["tickets"] = new_tickets
                        break

                with open(events_file, "w") as f:
                    json.dump(events, f, indent=4)

                st.success("Event updated!")
                st.rerun()

    if st.button("Log out", type="primary", use_container_width=True):
            with st.spinner("logging out..."):
                st.session_state["logged_in"] = False
                st.session_state["user"] = False
                st.session_state["role"] = False
                st.session_state["page"] = "login"
                time.sleep(4) 
                st.rerun()