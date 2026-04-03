import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time




st.set_page_config(page_title="Event Manager", layout="centered")
st.title("Login")



if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None 
if "page" not in st.session_state:
    st.session_state["page"] = "login"

users = [
     {
    "id": "1",
    "email": "admin@event.edu",
    "full_name": "System Admin",
    "password": "123ssag@43AE",
    "role": "Admin",
    "registered_at": "..."
    }
] 

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

json_path = Path("event.json")
if json_path.exists(): 
    with open(json_path, "r") as f:
        event = json.load(f)


users_file = Path("users.json")
events_file = Path("events.json")

users = json.load(open(users.file)) 
if users_file.exists():
   with open(users_file, "r") as f:
        user = json.load(f)

events = json.load(open(events.file)) 
if events_file.exists():
   with open(events.file, "r") as f:
     event = json.load(f)
    tab1, tab2 = st.tabs(["Login", "Registration"])
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
            
        if st.button("Login"):
            with st.spinner("Logging in..."):
                time.sleep(2)
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email.strip().lower() and user["password"] == password:
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
        new_email = st.text_input("New Email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            users.append({
                "id": str(uuid.uuid4()),
                "email": new_email,
                "password": new_pass,
                "role": "Attendee"
            })
            with open(json_path, "w") as f:
                json.dump(users, f, indent=4)
            st.success("Account created!")
            st.rerun()


if st.session_state["role"] == "Admin":
    if st.session_state["page"] == "home":
        st.markdown("welcome! This is the Admin Dashboard")
        if st.button("Dashboard", key="dashboard_view_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["Create Event", "View Event", "Update Event"])


#login 
else:
    st.title("Event Manager App")

    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email", key="login_email")
        password_input = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Log In", type="secondary", use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2) 
                # Find user
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
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
        



    # --- REGISTRATION ---
    st.subheader("New Admin Account")
    with st.container(border=True):
        new_email = st.text_input("Email Address", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        
        if st.button("Create Account", type="secondary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2) # Fake backend delay
                # ... (Assume validation logic here) ...
                users.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Admin"
                })
                with open(json_path, "w") as f:
                    json.dump(users, f, indent=4)
                st.success("Account created!")
                st.rerun()

    st.write("---")
#REMOVE THIS BEFORE SUBMISSION
    st.dataframe(users)

    #i dont know if this is useful
    with st.sidebar:
        st.markdown("Sidebar")
        if st.session_state["logged_in"] == True:
            user = st.session_state["user"]
            st.markdown(f"Logged User Email: {user['email']}")



           

if st.session_state["role"] == "Attendee":
    if st.session_state["page"] == "home":
        st.markdown("welcome! View Upcoming Events!")
        if st.button("Event Portal", key="view_events_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "Attendee"
            st.rerun()

 
else:
    st.title("See Events")

    event_names = []

    for event in events:
        event_names.append(event["name"])

    selected_event_name = st.selectbox("Select Event", event_names)

    selected_event = None
    for event in events:
        if event["name"] == selected_event_name:
            selected_event = event

    if selected_event:
        st.markdown(f"Event: {selected_event["name"]}")
        st.write(f" Date/Time: {selected_event["date"]} at {selected_event["time"]}")
        st.write(f"Location:{selected_event["location"]}")
        st.write(f"{selected_event["description"]}")
        st.write(f"Tickets Left: {selected_event["tickets"] - selected_event["reserved"]}")

        if st.button("Reserve Ticket"):
            if selected_event["reserved"] < selected_event["tickets"]:
                selected_event["reserved"] += 1
                st.success("Ticket reserved!")
            else:
                st.error("Sold out")

                