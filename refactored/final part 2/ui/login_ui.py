import streamlit as st
from services.authentication_service import (login, register_user)

#login
def show_login_page():
    st.title("Event Portal Login")
    st.divider()

    col1, col2 = st.columns(2)
    # test credentials
    with col1:
        st.info("Admin Login")
        st.caption("Email: admin@event.edu")
        st.caption("Password: 123ssag@43AE")
    with col2:
        st.info("Attendee Login")
        st.caption("Email: attendee@test.com")
        st.caption("Password: password123")
    st.divider()

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary", use_container_width=True):
        user = login(email, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.session_state["role"] = user["role"]

            if user["role"] == "Admin":
                st.session_state["page"] = "admin_home"
            else:
                st.session_state["page"] = "attendee_home"

            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.divider()

    if st.button("Create Account", use_container_width=True):
        st.session_state["page"] = "register"
        st.rerun()
 


#registertration
def show_register_page():
    st.title("Create Account")

    with st.form("register_form"):
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Attendee", "Admin"])
        submitted = st.form_submit_button("Register", type="primary", use_container_width=True)

        if submitted:
            if not email or not full_name or not password:
                st.warning("Please complete all fields")
            else:
                result = register_user(email, full_name, password, role)
                if result == "duplicate":
                    st.error("Account already exists")
                else:
                    st.success("Account created")
                    st.session_state["page"] = "login"

                    st.divider()

    if st.button("Back to Login", use_container_width=True):
        st.session_state["page"] = "login"
        st.rerun()    