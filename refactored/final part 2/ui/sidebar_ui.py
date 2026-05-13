import streamlit as st


def show_sidebar():
    with st.sidebar:
        st.title("Event Manager")
        st.success(f"Logged in as: {st.session_state.user['full_name']}")
        st.caption(f"Role: {st.session_state["role"]}")
        st.divider()
        if st.session_state["role"] == "Attendee":
            if st.button("Dashboard", use_container_width=True):
                st.session_state["page"] = "attendee_home"
                st.rerun()

            if st.button("Browse Events", use_container_width=True):
                st.session_state["page"] = "browse_events"
                st.rerun()

            if st.button("My Tickets", use_container_width=True):
                st.session_state["page"] = "my_tickets"
                st.rerun()

            if st.button("AI Assistant", use_container_width=True):
                st.session_state["page"] = "assistant"
                st.rerun()

        #admin sidebar - turn tabs into seperate pages
        else:
            if st.button("Dashboard", use_container_width=True):
                st.session_state["page"] = "admin_home"
                st.rerun()

            if st.button("Create Event", use_container_width=True):
                st.session_state["page"] = "create_event"
                st.rerun()

            if st.button("Manage My Events", use_container_width=True):
                st.session_state["page"] = "manage_my_events"
                st.rerun()

            if st.button("Browse All Events", use_container_width=True):
                st.session_state["page"] = "browse_all_events"
                st.rerun()

        st.divider()

        if st.button("Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            st.rerun()
        st.divider()           