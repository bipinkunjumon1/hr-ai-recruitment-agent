import streamlit as st
import pandas as pd
import plotly.express as px
from utils.components import (page_setup, sidebar, section_title,
                              recommendation_badge, empty_state)
from utils.state import require_auth, log_activity
from utils.api import run_ats

page_setup("ATS Analysis", "🚀")
require_auth()
sidebar()

st.markdown("## 🚀 ATS Analysis")
st.caption("Score resumes against the job description with AI.")

if st.button("▶️ Run ATS Analysis", use_container_width=False):
    with st.spinner("🧠 Analyzing resumes against JD…"):
        status, data = run_ats()
    if status == 200:
        rankings = data.get("rankings", [])
        st.session_state.rankings = rankings
        log_activity("🚀", f"ATS analysis: {len(rankings)} candidates scored")
        st.success(f"✅ Analyzed {len(rankings)} candidates")
    else:
        st.error(data.get("detail", "Analysis failed"))

rankings = st.session_state.get("rankings") or []
if not rankings:
    empty_state("📊", "No analysis yet",
                "Upload a JD and resumes, then run the ATS analysis.")
    st.stop()

df = pd.DataFrame(rankings)

# ---- Results table ----
section_title("ATS Results", "📋")
display = df.copy()
if "ats_score" in display:
    st.dataframe(
        display,
        use_container_width=True,
        column_config={
            "ats_score": st.column_config.ProgressColumn(
                "ATS Score", min_value=0, max_value=100, format="%d%%"),
        },
    )

# ---- Comparison ----
section_title("Candidate Comparison", "⚖️")
names = [r.get("candidate_name", f"Candidate {i}")
         for i, r in enumerate(rankings)]
pick = st.multiselect("Compare candidates", names, default=names[:2])
chosen = [r for r in rankings if r.get("candidate_name") in pick]

for r in chosen:
    score = r.get("ats_score", 0)
    matched = r.get("matched_skills") or r.get("skills_matched") or []
    missing = r.get("missing_skills") or []
    with st.container():
        st.markdown(f"<div class='tf-card'><h4>👤 {r.get('candidate_name')} "
                    f"{recommendation_badge(score)}</h4>",
                    unsafe_allow_html=True)
        a, b = st.columns(2)
        with a:
            st.markdown("**✅ Matched Skills**")
            st.markdown(" ".join(
                f"<span class='badge badge-success' style='margin:2px'>{s}</span>"
                for s in matched) or "_None_", unsafe_allow_html=True)
        with b:
            st.markdown("**❌ Missing Skills**")
            st.markdown(" ".join(
                f"<span class='badge badge-danger' style='margin:2px'>{s}</span>"
                for s in missing) or "_None_", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---- Skill match chart ----
if chosen:
    section_title("Skill Match Overview", "📊")
    chart_df = pd.DataFrame([
        {"Candidate": r.get("candidate_name"),
         "ATS Score": r.get("ats_score", 0)} for r in chosen])
    fig = px.bar(chart_df, x="Candidate", y="ATS Score",
                 color="ATS Score",
                 color_continuous_scale=[[0, "#c7d2fe"], [1, "#4f46e5"]],
                 range_y=[0, 100])


    fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
