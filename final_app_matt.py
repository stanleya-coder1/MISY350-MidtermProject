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
