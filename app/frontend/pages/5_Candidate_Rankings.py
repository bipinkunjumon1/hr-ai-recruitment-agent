import streamlit as st
import pandas as pd
from utils.components import (page_setup, sidebar, section_title,
                              recommendation_badge, empty_state, progress_bar)
from utils.state import require_auth

page_setup("Rankings", "🏆")
require_auth()
sidebar()

st.markdown("## 🏆 Candidate Rankings")
st.caption("Leaderboard of candidates by ATS score.")

rankings = st.session_state.get("rankings") or []
if not rankings:
    empty_state("🏅", "No rankings available",
                "Run an ATS analysis to generate rankings.",
                "pages/4_ATS_Analysis.py", "Run ATS Analysis", "🚀")
    st.stop()

ranked = sorted(rankings, key=lambda r: r.get("ats_score", 0), reverse=True)
medals = {0: "🥇", 1: "🥈", 2: "🥉"}

# ---- Export ----
col1, col2 = st.columns([4, 1])
with col2:
    csv = pd.DataFrame(ranked).to_csv(index=False).encode()
    st.download_button("⬇️ Export CSV", csv,
                       "rankings.csv", "text/csv",
                       use_container_width=True)

# ---- Leaderboard ----
section_title("Leaderboard", "📋")
for i, r in enumerate(ranked):
    score = r.get("ats_score", 0)
    medal = medals.get(i, f"#{i+1}")
    c1, c2, c3, c4 = st.columns([0.6, 2.5, 2, 1.6])
    c1.markdown(f"<div class='rank-medal'>{medal}</div>",
                unsafe_allow_html=True)
    c2.markdown(f"**{r.get('candidate_name', 'Unknown')}**  \n"
                f"<span style='color:#94a3b8;font-size:.8rem'>"
                f"{r.get('email', '')}</span>", unsafe_allow_html=True)
    with c3:
        progress_bar(score)
        st.caption(f"{score}% ATS")
    c4.markdown(recommendation_badge(score), unsafe_allow_html=True)

    with st.expander(f"🔍 View details · {r.get('candidate_name', '')}"):
        d1, d2 = st.columns(2)
        d1.markdown("**✅ Matched**")
        d1.write(", ".join(r.get("matched_skills",
                 r.get("skills_matched", []))) or "—")
        d2.markdown("**❌ Missing**")
        d2.write(", ".join(r.get("missing_skills", [])) or "—")
        st.json(r)
