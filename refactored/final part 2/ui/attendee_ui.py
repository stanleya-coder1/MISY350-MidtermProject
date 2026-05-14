import streamlit as st

from services.event_service import (get_all_events, reserve_ticket, cancel_ticket, get_tickets_left, user_has_ticket, get_reservation_status)

# attendee dahsboard/home
def show_attendee_home():
    st.title("Attendee Dashboard")
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


#atendee CRUD - browse/review events(R), reserve ticket (C)
def show_browse_events():
    st.title("Browse Events")

    events = get_all_events()
    search = st.text_input("Search Events")

    if search:
        events = [event for event in events if search.lower() in event["name"].lower()]

    cols = st.columns(2)
    column_list = 0

    for event in events:
        with cols[column_list]:
            with st.container(border=True):
                st.subheader(event["name"])
                st.write(f"Date: {event['date']}")
                st.write(f"Time: {event['time']}")
                st.write(f"Location: {event['location']}")
                st.caption(f"Hosted by {event['created_by_name']}")
                st.write(event["description"])
                st.metric("Tickets Left", get_tickets_left(event))
                result = None

            #CRUD create reservation
                if st.button("Reserve Ticket", key=event["id"]):
                    result = reserve_ticket(event["id"], st.session_state["user"])
                if result == "success":
                    st.success("Ticket Reserved")
                elif result == "sold_out":
                    st.error("Sold Out")
                elif result == "already_reserved":
                    st.warning("Already Reserved")

        column_list += 1
        if column_list > 1:
            column_list = 0


# my tickets CRUD - review (R) and cancel (D)
def show_my_tickets():
    st.title("My Tickets")
    current_user = st.session_state["user"]
    events = get_all_events()
    user_events = [
        event for event in events
        if user_has_ticket(event, current_user["id"])
    ]

    if not user_events:
        st.info("No reservations yet")
        return

    cols = st.columns(2)
    column_list = 0
    for event in user_events:
        status = get_reservation_status(event, current_user["id"])

        with cols[column_list]:
            with st.container(border=True):
                st.subheader(event["name"])
                st.write(event["date"])
                st.write(event["time"])
                st.write(event["location"])
                st.caption(f"Hosted by {event['created_by_name']}")

                #status button
                if status == "Reserved":
                    st.success("Reserved")
                elif status == "Past":
                    st.info("Past")
                elif status == "Cancelled":
                    st.error("Cancelled")
                elif status == "Cancelled Event":
                    st.error("Event Cancelled")

                if status == "Reserved":
                    if st.button("Cancel Reservation", key=f"cancel_{event['id']}"):
                        cancel_ticket(event["id"], current_user["id"])
                        st.success("Reservation Cancelled")
                        st.rerun()

        column_list += 1
        if column_list > 1:
            column_list = 0


# AI / FAQ Section
def show_event_help():
    st.title("Event Help Chatbot Assistant")
    st.divider()
    events = get_all_events()
    total_events = len(events)

    st.error("Open AI Key Not Active")
    st.divider()
    st.subheader("Frequently Asked Questions")

    # Question 1
    if st.button("What events are currently available?"):
        if not events:
            st.info("There are currently no events available.")
        else:
            for event in events:
                with st.container(border=True):
                    st.subheader(event["name"])
                    st.write(f"Date: {event['date']}")
                    st.write(f"Location: {event['location']}")
    # Question 2
    if st.button("How many total events are available?"):
        st.success(f"There are currently {total_events} events available.")
    # Question 3
    if st.button("How do I know who is hosting the event?"):
        st.info("When you look at ticket reservations, it will tell you who is the host for the event selected.")
    # Question 4
    if st.button("How do I reserve a ticket?"):
        st.info(
            "Go to the Browse Events page and click the 'Reserve Ticket' button.")
    # Question 5
    if st.button("How do I cancel my reservation?"):
        st.info(
            "Go to the My Tickets page and click 'Cancel Reservation'.")