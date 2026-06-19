import streamlit as st
import pandas as pd
import plotly.express as px
from utils.components import (page_setup, sidebar, kpi_card,
                              section_title, recommendation_badge, empty_state)
from utils.state import require_auth

page_setup("Dashboard", "📊")
require_auth()
sidebar("dashboard")

rankings = st.session_state.get("rankings") or []
interviews = st.session_state.get("interviews") or []

st.markdown("## 📊 Recruitment Dashboard")
st.caption("Overview of your hiring pipeline")

# ---- KPIs ----
total = len(rankings)
shortlisted = sum(1 for r in rankings if r.get("ats_score", 0) >= 70)
scheduled = len(interviews)
avg = round(sum(r.get("ats_score", 0) for r in rankings) / total, 1) if total else 0

c1, c2, c3, c4 = st.columns(4)
with c1: kpi_card("Total Candidates", total, "👥", "#6366f1")
with c2: kpi_card("Shortlisted", shortlisted, "⭐", "#10b981")
with c3: kpi_card("Interviews", scheduled, "📅", "#3b82f6")
with c4: kpi_card("Avg ATS Score", f"{avg}%", "🎯", "#f59e0b")

st.write("")

if not rankings:
    empty_state("📭", "No data yet",
                "Run an ATS analysis to populate your dashboard.",
                "pages/4_ATS_Analysis.py", "Run ATS Analysis", "🚀")
    st.stop()

df = pd.DataFrame(rankings)

left, right = st.columns([1.4, 1])

# ---- ATS distribution ----
with left:
    section_title("ATS Score Distribution", "📈")
    fig = px.histogram(df, x="ats_score", nbins=10,
                       color_discrete_sequence=["#6366f1"])
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10),
                      bargap=0.08, yaxis_title="Candidates",
                      xaxis_title="ATS Score")
    st.plotly_chart(fig, use_container_width=True)

# ---- Recent activity ----
with right:
    section_title("Recent Activity", "🕒")
    acts = st.session_state.get("activities") or []
    if not acts:
        st.caption("No recent activity.")
    for a in acts[:6]:
        st.markdown(
            f"<div class='activity-item'>{a['icon']} {a['text']}"
            f"<span class='activity-time'>{a['time']}</span></div>",
            unsafe_allow_html=True,
        )

# ---- Top candidates ----
section_title("Top Candidates", "🏆")
top = sorted(rankings, key=lambda r: r.get("ats_score", 0), reverse=True)[:5]
for r in top:
    cols = st.columns([0.5, 3, 2, 1.5])
    cols[0].markdown(f"**#{r.get('rank', '-')}**")
    cols[1].markdown(f"**{r.get('candidate_name', 'Unknown')}**")
    cols[2].progress(min(int(r.get("ats_score", 0)), 100))
    cols[3].markdown(recommendation_badge(r.get("ats_score", 0)),
                     unsafe_allow_html=True)
