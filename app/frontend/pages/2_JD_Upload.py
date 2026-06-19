import streamlit as st
from config import ALLOWED_TYPES
from utils.components import page_setup, sidebar, section_title
from utils.state import require_auth, log_activity
from utils.api import upload_jd

page_setup("Job Description", "📄")
require_auth()
sidebar()

st.markdown("## 📄 Upload Job Description")
st.caption("Upload a JD to extract role requirements and skills.")

jd_file = st.file_uploader("Drag & drop your JD here",
                           type=ALLOWED_TYPES,
                           help="Supports PDF, DOCX, PNG, JPG, JPEG")

col1, col2 = st.columns([1, 4])
with col1:
    go = st.button("⬆️ Upload JD", use_container_width=True,
                   disabled=jd_file is None)

if go and jd_file:
    with st.status("Processing job description…", expanded=True) as s:
        st.write("📤 Uploading file…")
        status, data = upload_jd(jd_file)
        if status == 200:
            st.write("🧠 Extracting requirements…")
            s.update(label="JD processed successfully!", state="complete")
            st.session_state.jd_data = data
            log_activity("📄", f"Uploaded JD: {jd_file.name}")
        else:
            s.update(label="Upload failed", state="error")
            st.error(data.get("detail", "Upload failed"))

# ---- Show extracted JD ----
jd = st.session_state.get("jd_data")
if jd:
    st.success("✅ Job Description ready")
    c1, c2 = st.columns([1.3, 1])
    with c1:
        section_title("JD Summary", "📝")
        st.markdown(
            f"<div class='tf-card'>{jd.get('summary', 'No summary available.')}"
            f"</div>", unsafe_allow_html=True)
    with c2:
        section_title("Required Skills", "🛠️")
        skills = jd.get("skills") or jd.get("required_skills") or []
        if skills:
            chips = " ".join(
                f"<span class='badge badge-info' style='margin:3px'>{s}</span>"
                for s in skills)
            st.markdown(f"<div class='tf-card'>{chips}</div>",
                        unsafe_allow_html=True)
        else:
            st.caption("No skills extracted.")
    with st.expander("🔍 Raw response"):
        st.json(jd)
