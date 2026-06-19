import streamlit as st


def init_state():
    defaults = {
        "token": None,
        "user": None,
        "theme": "light",
        "rankings": [],
        "jd_data": None,
        "resumes": [],
        "interviews": [],
        "activities": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def is_authenticated() -> bool:
    return bool(st.session_state.get("token"))


def login(token: str, user: dict | None = None):
    st.session_state.token = token
    st.session_state.user = user or {"name": "HR Manager", "role": "Recruiter"}


def logout():
    for k in ["token", "user", "rankings", "jd_data", "resumes",
              "interviews", "activities"]:
        st.session_state[k] = None if k in ("token", "user") else []


def log_activity(icon: str, text: str):
    from datetime import datetime
    st.session_state.activities = (
        [{"icon": icon, "text": text,
          "time": datetime.now().strftime("%H:%M")}]
        + st.session_state.get("activities", [])
    )[:10]


def require_auth():
    """Guard for protected pages."""
    init_state()
    if not is_authenticated():
        st.warning("🔒 Please log in to access this page.")
        st.page_link("app.py", label="Go to Login", icon="🔑")
        st.stop()
