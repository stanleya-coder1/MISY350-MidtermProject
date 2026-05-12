import streamlit as st

from ui.login_ui import show_login_page, show_register_page
from ui.attendee_ui import (show_attendee_home, show_browse_events, show_my_tickets)
from ui.admin_ui import (show_admin_home, show_create_event, show_manage_my_events, show_browse_all_events)
from ui.sidebar_ui import show_sidebar

st.set_page_config(page_title="Event Manager", layout="wide", initial_sidebar_state="expanded") 