import streamlit as st
from utils.components import page_setup, brand_header
from utils.state import init_state, login, is_authenticated, log_activity
from utils.api import login_request

page_setup("Login", "🔑")
init_state()

# Redirect if already logged in
if is_authenticated():
    st.switch_page("pages/1_Dashboard.py")

# Centered login card
_, mid, _ = st.columns([1, 1.1, 1])
with mid:
    st.write("")
    st.write("")
    brand_header()
    st.markdown("### Welcome back 👋")
    st.caption("Sign in to your recruitment workspace")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password",
                                 placeholder="••••••••")
        submitted = st.form_submit_button("Sign In →",
                                          use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please enter your username and password.")
        else:
            with st.spinner("Authenticating…"):
                status, data = login_request(username, password)
            if status == 200 and data.get("access_token"):
                login(data["access_token"],
                      {"name": username, "role": "Recruiter"})
                log_activity("🔑", "Signed in")
                st.success("Welcome! Redirecting…")
                st.switch_page("pages/1_Dashboard.py")
            else:
                detail = data.get("detail", "Invalid credentials")
                st.error(detail if isinstance(detail, str)
                         else "Invalid credentials")


    st.caption("🔒 Secured with JWT authentication")
