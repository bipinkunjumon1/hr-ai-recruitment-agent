import streamlit as st
from config import ALLOWED_TYPES
from utils.components import page_setup, sidebar, section_title
from utils.state import require_auth, log_activity
from utils.api import upload_resume

page_setup("Resumes", "📁")
require_auth()
sidebar()

st.markdown("## 📁 Upload Resumes")
st.caption("Upload one or more candidate resumes for parsing & scoring.")

files = st.file_uploader("Drag & drop resumes here",
                         type=ALLOWED_TYPES,
                         accept_multiple_files=True,
                         help="Supports PDF, DOCX, PNG, JPG, JPEG")

if files:
    st.info(f"📎 {len(files)} file(s) selected")

if st.button("⬆️ Upload All", use_container_width=False,
             disabled=not files):
    progress = st.progress(0, text="Starting upload…")
    results = []
    for i, f in enumerate(files):
        progress.progress((i) / len(files), text=f"Uploading {f.name}…")
        status, data = upload_resume(f)
        results.append((f.name, status, data))
        if status == 200:
            st.session_state.resumes.append(data)
            log_activity("📁", f"Uploaded resume: {f.name}")
    progress.progress(1.0, text="Done!")

    for name, status, data in results:
        if status == 200:
            cand = data.get("candidate") or data
            with st.container():
                st.markdown(
                    f"""<div class='tf-card'>
                        <h4>👤 {cand.get('name', name)}</h4>
                        <p>📧 {cand.get('email', '—')} &nbsp;|&nbsp;
                           📞 {cand.get('phone', '—')}</p>
                        <p>🛠️ {', '.join(cand.get('skills', [])[:8]) or 'No skills parsed'}</p>
                    </div>""",
                    unsafe_allow_html=True)
        else:
            st.error(f"❌ {name}: {data.get('detail', 'Upload failed')}")

# Existing resumes
if st.session_state.get("resumes"):
    section_title(f"Uploaded Resumes ({len(st.session_state.resumes)})", "🗂️")
    with st.expander("View all uploaded resumes"):
        st.json(st.session_state.resumes)
