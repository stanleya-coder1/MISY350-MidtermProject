import streamlit as st

from ui.login_ui import show_login_page, show_register_page
from ui.attendee_ui import (show_attendee_home, show_browse_events, show_my_tickets)
from ui.admin_ui import (show_admin_home, show_create_event, show_manage_my_events, show_browse_all_events)
from ui.sidebar_ui import show_sidebar

st.set_page_config(page_title="Event Manager", layout="wide", initial_sidebar_state="expanded") 

#session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

# sidebar
if st.session_state.logged_in:
    show_sidebar()

page = st.session_state["page"]

if page == "login":
    show_login_page()

elif page == "register":
    show_register_page()

# attendee pages
elif page == "attendee_home":
    show_attendee_home()

elif page == "browse_events":
    show_browse_events()

elif page == "my_tickets":
    show_my_tickets()