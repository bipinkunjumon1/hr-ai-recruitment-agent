import streamlit as st
from pathlib import Path
from config import APP_NAME, APP_TAGLINE
from utils.state import logout

_CSS_PATH = Path(__file__).parent.parent / "assets" / "styles.css"


def load_css():
    if _CSS_PATH.exists():
        st.markdown(f"<style>{_CSS_PATH.read_text()}</style>",
                    unsafe_allow_html=True)


def page_setup(title="TalentFlow", icon="🎯"):
    st.set_page_config(page_title=f"{APP_NAME} · {title}",
                       page_icon=icon, layout="wide",
                       initial_sidebar_state="expanded")
    load_css()


def brand_header():
    st.markdown(
        f"""
        <div class="brand">
            <div class="brand-logo">🎯</div>
            <div>
                <div class="brand-name">{APP_NAME}</div>
                <div class="brand-tag">{APP_TAGLINE}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar(active: str = ""):
    """Renders brand, nav links and user/logout block."""
    with st.sidebar:
        brand_header()
        st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
        st.page_link("pages/2_JD_Upload.py", label="Job Description", icon="📄")
        st.page_link("pages/3_Resume_Upload.py", label="Resumes", icon="📁")
        st.page_link("pages/4_ATS_Analysis.py", label="ATS Analysis", icon="🚀")
        st.page_link("pages/5_Candidate_Rankings.py",
                     label="Rankings", icon="🏆")
        st.page_link("pages/6_Interview_Scheduling.py",
                     label="Interviews", icon="📅")
        st.page_link("pages/7_Reschedule_Requests.py",
                     label="Reschedule", icon="🔄")
        st.markdown("---")

        st.markdown("---")
        user = st.session_state.get("user") or {}
        st.markdown(
            f"**👤 {user.get('name', 'HR Manager')}**  \n"
            f"<span style='opacity:.7;font-size:.8rem'>"
            f"{user.get('role', 'Recruiter')}</span>",
            unsafe_allow_html=True,
        )
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.switch_page("app.py")


def kpi_card(label, value, icon, bg, delta=None, delta_up=True):
    cls = "up" if delta_up else "down"
    arrow = "▲" if delta_up else "▼"
    delta_html = (f"<div class='kpi-delta {cls}'>{arrow} {delta}</div>"
                  if delta else "")
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background:{bg}22;color:{bg}">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def progress_bar(percent: float):
    p = max(0, min(100, percent))
    st.markdown(
        f"<div class='tf-progress'><span style='width:{p}%'></span></div>",
        unsafe_allow_html=True,
    )


def badge(text, kind="info"):
    return f"<span class='badge badge-{kind}'>{text}</span>"


def recommendation_badge(score: float):
    if score >= 80:
        return badge("✅ Strong Match", "success")
    if score >= 60:
        return badge("👍 Good Fit", "info")
    if score >= 40:
        return badge("⚠️ Maybe", "warning")
    return badge("❌ Low Match", "danger")


def empty_state(icon, title, subtitle, page=None, link_label=None, link_icon=None):
    st.markdown(
        f"""<div class='empty-state'>
            <div class='icon'>{icon}</div>
            <h3>{title}</h3><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )
    if page:
        st.page_link(page, label=link_label, icon=link_icon)


def section_title(text, emoji=""):
    st.markdown(f"#### {emoji} {text}")
