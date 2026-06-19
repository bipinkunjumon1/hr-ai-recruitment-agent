import requests
import streamlit as st
from utils.components import page_setup, sidebar, empty_state
from utils.state import require_auth, log_activity
from utils.api import _headers
from config import API_BASE

page_setup("Reschedule Requests", "🔄")
require_auth()
sidebar()

CHECK = f"{API_BASE}/api/reschedule/check-mails"
PENDING = f"{API_BASE}/api/reschedule/pending"
APPROVE = f"{API_BASE}/api/reschedule/approve"
REJECT = f"{API_BASE}/api/reschedule/reject"

st.markdown("## 🔄 Reschedule Requests")
st.caption("AI-detected interview reschedule requests awaiting your approval.")

col1, _ = st.columns([1, 4])
with col1:
    if st.button("📥 Check Inbox", use_container_width=True):
        with st.spinner("🤖 Reading inbox & classifying emails…"):
            try:
                r = requests.post(CHECK, headers=_headers(), timeout=60)
            except requests.RequestException as e:
                r = None
                st.error(f"Connection error: {e}")
        if r is not None and r.status_code == 200:
            data = r.json()
            st.success(f"Processed {data['processed']} email(s) · "
                       f"{len(data['reschedule_requests'])} reschedule(s) found")
            with st.expander("🔍 Classification details (debug)"):
                st.json(data.get("debug", []))
            log_activity("🔄", "Checked inbox for reschedules")
        elif r is not None:
            st.error(r.text)

# ---- Fetch pending ----
try:
    resp = requests.get(PENDING, headers=_headers(), timeout=30)
    pending = resp.json() if resp.status_code == 200 else []
except requests.RequestException as e:
    pending = []
    st.error(f"Could not load pending requests: {e}")

if not pending:
    empty_state("📭", "No pending requests",
                "Click 'Check Inbox' to scan for new reschedule emails. "
                "If emails were processed but none matched, expand the "
                "classification details above to see why.")
    st.stop()

st.markdown(f"#### 📋 {len(pending)} request(s) awaiting action")

for req in pending:
    with st.container():
        st.markdown(
            f"""<div class='tf-card'>
                <h4>👤 {req['candidate_name']}
                <span class='badge badge-warning'>Pending</span></h4>
                <p>📧 {req['candidate_email']}</p>
                <p>📝 <b>Reason:</b> {req.get('reason', '—')}</p>
            </div>""",
            unsafe_allow_html=True,
        )
        with st.expander("✉️ Original email"):
            st.write(f"**Subject:** {req.get('subject', '')}")
            st.write(req.get("body", ""))

        a, b, _ = st.columns([1, 1, 3])
        if a.button("✅ Approve", key=f"app{req['request_id']}",
                    use_container_width=True):
            try:
                r = requests.post(APPROVE,
                                  json={"request_id": req["request_id"]},
                                  headers=_headers(), timeout=60)
                if r.ok:
                    st.success("Approved & email sent")
                    st.rerun()
                else:
                    st.error(r.text)
            except requests.RequestException as e:
                st.error(f"Connection error: {e}")

        if b.button("❌ Reject", key=f"rej{req['request_id']}",
                    use_container_width=True):
            try:
                r = requests.post(REJECT,
                                  json={"request_id": req["request_id"]},
                                  headers=_headers(), timeout=60)
                if r.ok:
                    st.success("Rejected & email sent")
                    st.rerun()
                else:
                    st.error(r.text)
            except requests.RequestException as e:
                st.error(f"Connection error: {e}")
