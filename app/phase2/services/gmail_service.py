import base64
import re
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

TOKEN_PATH = "token.json"
CREDS_PATH = "credentials.json"


def _get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


def get_gmail_service():
    return build("gmail", "v1", credentials=_get_credentials())


def _header(payload, name):
    for h in payload.get("headers", []):
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def _extract_body(payload) -> str:
    """Recursively pull plain-text body from a Gmail message payload."""
    if payload.get("mimeType") == "text/plain":
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", "ignore")
    for part in payload.get("parts", []) or []:
        text = _extract_body(part)
        if text:
            return text
    # Fallback to top-level body
    data = payload.get("body", {}).get("data")
    if data:
        return base64.urlsafe_b64decode(data).decode("utf-8", "ignore")
    return ""


def _parse_sender(raw: str):
    """'John Doe <john@gmail.com>' -> ('John Doe', 'john@gmail.com')"""
    match = re.match(r"(.*)<(.+?)>", raw)
    if match:
        return match.group(1).strip().strip('"'), match.group(2).strip()
    return raw, raw


def read_unread_emails(max_results: int = 5):
    """Return first N unread emails as structured dicts."""
    service = get_gmail_service()
    resp = service.users().messages().list(

    userId="me",

    q='is:unread newer_than:7d subject:"HR-AI"',

    maxResults=max_results

).execute()
    messages = resp.get("messages", [])

    results = []
    for m in messages:
        full = service.users().messages().get(
            userId="me", id=m["id"], format="full").execute()
        payload = full["payload"]
        sender_raw = _header(payload, "From")
        name, email = _parse_sender(sender_raw)
        results.append({
            "id": m["id"],
            "thread_id": full.get("threadId"),
            "candidate_name": name,
            "candidate_email": email,
            "subject": _header(payload, "Subject"),
            "body": _extract_body(payload).strip(),
        })
    return results


def mark_as_read(message_id: str):
    get_gmail_service().users().messages().modify(
        userId="me", id=message_id,
        body={"removeLabelIds": ["UNREAD"]}).execute()


def send_email(to: str, subject: str, body_text: str, thread_id: str = None):
    service = get_gmail_service()
    msg = MIMEText(body_text)
    msg["to"] = to
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    payload = {"raw": raw}
    if thread_id:
        payload["threadId"] = thread_id  # keeps reply in same conversation
    return service.users().messages().send(userId="me", body=payload).execute()
