import streamlit as st

from services.event_service import (get_all_events, get_events_by_admin, create_event, update_event, delete_event, get_tickets_left, get_event_status)

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

# admin CRUD - review all events
def show_browse_all_events():
    st.title("Browse All Events")
    events = get_all_events()
    search = st.text_input("Search Events")

    if search:
        events = [event for event in events if search.lower() in event["name"].lower()]
    for event in events:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(event["name"])
                st.write(f"Date: {event['date']}")
                st.write(f"Location: {event['location']}")
                st.caption(f"Hosted by {event['created_by_name']}")
            with col2:
                st.metric("Tickets Left", get_tickets_left(event))

#admin CRUD - update/delete events
def show_manage_my_events():
    st.title("Manage My Events")
    events = get_events_by_admin(st.session_state.user["id"])

    status = get_event_status(event)
    st.info(f"Status: {status}")

    if not events:
        st.info("No events created yet")
        return

    for event in events:
        with st.container(border=True):
            st.subheader(event["name"])
            st.info(f"Status: {event.get('status', 'Upcoming')}")
            col1, col2 = st.columns(2)

            with col1:
                updated_name = st.text_input("Event Name", value=event["name"], key=f"name_{event['id']}")
                updated_tickets = st.number_input("Tickets", min_value=1, value=event["tickets"], key=f"tickets_{event['id']}")
            with col2:
                updated_location = st.text_input("Location", value=event["location"], key=f"location_{event['id']}")
                updated_description = st.text_area("Description", value=event["description"], key=f"description_{event['id']}")

            st.metric("Tickets Left", get_tickets_left(event))

            button_col1, button_col2 = st.columns(2)
            with button_col1:

                if st.button("Save Changes", key=f"save_{event['id']}", use_container_width=True):
                    update_event(event["id"], updated_name, updated_tickets, updated_location, updated_description)
                    st.success("Event Updated")
                    st.rerun()

            with button_col2:
                if st.button("Cancel Event", key=f"delete_{event['id']}", use_container_width=True):
                    delete_event(event["id"])
                    st.success("Event Cancelled")
                    st.rerun()

