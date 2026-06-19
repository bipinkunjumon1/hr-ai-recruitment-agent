import streamlit as st
from datetime import datetime, timedelta, date, time as dtime
from utils.components import page_setup, sidebar, section_title, empty_state
from utils.state import require_auth, log_activity
from utils.api import schedule_interview

page_setup("Interviews", "📅")
require_auth()
sidebar()

st.markdown("## 📅 Schedule Interview")
st.caption("Book interviews and auto-generate Google Meet links.")

rankings = st.session_state.get("rankings") or []
if not rankings:
    empty_state("📅", "No candidates to schedule",
                "Run an ATS analysis first.",
                "pages/4_ATS_Analysis.py", "Run ATS Analysis", "🚀")
    st.stop()

options = {f"#{c.get('rank', i+1)} · {c.get('candidate_name', 'Unknown')} "
           f"({c.get('ats_score', 0)}%)": c
           for i, c in enumerate(rankings)}

with st.form("schedule_form"):
    section_title("Interview Details", "📝")
    sel = st.selectbox("Select Candidate", list(options.keys()))
    c1, c2, c3 = st.columns(3)
    d = c1.date_input("Date", min_value=date.today())
    t = c2.time_input("Time", value=dtime(10, 0))
    dur = c3.number_input("Duration (min)", 15, 120, 30, 15)
    submit = st.form_submit_button("📨 Schedule Interview",
                                   use_container_width=True)

if submit:
    cand = options[sel]
    start_dt = datetime.combine(d, t)
    end_dt = start_dt + timedelta(minutes=int(dur))
    with st.spinner("📡 Creating calendar event & Meet link…"):
        status, data = schedule_interview(
            cand.get("candidate_id"),
            start_dt.isoformat(),
            end_dt.isoformat(),
        )
    if status == 200:
        st.session_state.interviews.append({
            "candidate": cand.get("candidate_name"),
            "start": start_dt.isoformat(),
            "link": data.get("hangoutLink"),
        })
        log_activity("📅", f"Scheduled: {cand.get('candidate_name')}")
        st.success("✅ Interview scheduled successfully!")
        # st.balloons()

        meet = data.get("hangoutLink")
        if meet:
            st.markdown(
                f"""<div class='tf-card'>
                    <h4>🎥 Google Meet</h4>
                    <p>{cand.get('candidate_name')} ·
                       {start_dt.strftime('%b %d, %Y at %I:%M %p')}</p>
                </div>""", unsafe_allow_html=True)
            st.link_button("🔗 Open Google Meet", meet,
                           use_container_width=False)
        with st.expander("🔍 Raw response"):
            st.json(data)
    else:
        st.error(data.get("detail", "Scheduling failed"))

# ---- Timeline ----
if st.session_state.get("interviews"):
    section_title("Scheduled Interviews", "🗓️")
    for iv in sorted(st.session_state.interviews,
                     key=lambda x: x["start"]):
        when = datetime.fromisoformat(iv["start"]).strftime("%b %d · %I:%M %p")
        link = (f" · <a href='{iv['link']}' target='_blank'>Join</a>"
                if iv.get("link") else "")
        st.markdown(
            f"<div class='activity-item'>📌 <b>{iv['candidate']}</b>"
            f"<span class='activity-time'>{when}{link}</span></div>",
            unsafe_allow_html=True)
