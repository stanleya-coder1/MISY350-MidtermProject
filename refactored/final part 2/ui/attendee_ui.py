import streamlit as st
from services.event_service import (get_all_events, reserve_ticket, cancel_ticket, get_tickets_left, user_has_ticket)

# attendee dahsboard/home
def show_attendee_home():
    st.title("Attendee Home")
    st.divider()

    events = get_all_events()
    current_user = st.session_state["user"]
    reserved_count = 0

    for event in events:
        if user_has_ticket(event, current_user["id"]):
            reserved_count += 1

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Events Available", len(events))
    with col2:
        st.metric("My Reservations", reserved_count)
    st.divider()

    st.subheader("Featured Events")
    for event in events[:3]: #3 most recet events
        with st.container(border=True):
            st.subheader(event["name"])
            st.write(event["date"])
            st.write(event["location"])
            st.caption(f"Hosted by {event['created_by_name']}")
