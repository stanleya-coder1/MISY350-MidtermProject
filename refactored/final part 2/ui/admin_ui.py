import streamlit as st

from services.event_service import (get_all_events, get_events_by_admin, create_event, update_event, delete_event, get_tickets_left)

#admin dashboard
def show_admin_home():
    st.title("Admin Dashboard")
    events = get_all_events()

    my_events = get_events_by_admin(st.session_state["user"]["id"])
    sold_out = 0

    for event in events:
        if get_tickets_left(event) == 0:
            sold_out += 1

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Events", len(events))
    with col2:
        st.metric("My Events", len(my_events))
    with col3:
        st.metric("Sold Out", sold_out)

    st.divider()

    st.subheader("My Recent Events")
    for event in my_events[:3]:
        with st.container(border=True):
            st.subheader(event["name"])
            st.write(event["date"])
            st.write(event["location"])

            st.caption(f"Hosted by {event['created_by_name']}")

# admin CRUD - create event
def show_create_event():
    st.title("Create Event")

    with st.form("create_event_form"):
        name = st.text_input("Event Name")
        date = st.date_input("Date")
        time = st.time_input("Time")
        location = st.text_input("Location")
        description = st.text_area("Description")
        tickets = st.number_input("Tickets", min_value=1, value=50)
        submitted = st.form_submit_button("Create Event", type="primary", use_container_width=True)

        if submitted:
            create_event(name, date, time, location, description, tickets, st.session_state["user"])
            st.success("Event created")

