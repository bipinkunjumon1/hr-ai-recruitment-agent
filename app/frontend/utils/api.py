import requests
import streamlit as st
from config import API_BASE, ENDPOINTS, MIME_MAP

TIMEOUT = 60


def _headers(extra: dict | None = None) -> dict:
    h = {}
    token = st.session_state.get("token")
    if token:
        h["Authorization"] = f"Bearer {token}"
    if extra:
        h.update(extra)
    return h


def _url(key: str) -> str:
    return f"{API_BASE}{ENDPOINTS[key]}"


def login_request(username: str, password: str):
    try:
        r = requests.post(
            _url("login"),
            data={
                "grant_type": "password",
                "username": username,
                "password": password,
                "scope": "",
                "client_id": "string",
                "client_secret": "string",
            },
            timeout=TIMEOUT,
        )
        return r.status_code, _safe_json(r)
    except requests.RequestException as e:
        return 0, {"detail": f"Connection error: {e}"}


def _file_payload(uploaded_file):
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    mime = MIME_MAP.get(ext, "application/octet-stream")
    return {"file": (uploaded_file.name, uploaded_file.getvalue(), mime)}


def upload_jd(uploaded_file):
    return _post_file("upload_jd", uploaded_file)


def upload_resume(uploaded_file):
    return _post_file("upload_resume", uploaded_file)


def _post_file(key, uploaded_file):
    try:
        r = requests.post(
            _url(key),
            files=_file_payload(uploaded_file),
            headers=_headers(),
            timeout=TIMEOUT,
        )
        return r.status_code, _safe_json(r)
    except requests.RequestException as e:
        return 0, {"detail": f"Connection error: {e}"}


def run_ats():
    try:
        r = requests.post(_url("analyze"), headers=_headers(), timeout=TIMEOUT)
        return r.status_code, _safe_json(r)
    except requests.RequestException as e:
        return 0, {"detail": f"Connection error: {e}"}


def schedule_interview(candidate_id, start_time, end_time):
    try:
        r = requests.post(
            _url("schedule"),
            headers=_headers(),
            json={
                "candidate_id": candidate_id,
                "start_time": start_time,
                "end_time": end_time,
            },
            timeout=TIMEOUT,
        )
        return r.status_code, _safe_json(r)
    except requests.RequestException as e:
        return 0, {"detail": f"Connection error: {e}"}


def _safe_json(resp):
    try:
        return resp.json()
    except ValueError:
        return {"detail": resp.text or "Empty response"}
