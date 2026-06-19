from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from phase2.agents.email_monitor_agent import monitor_inbox
from phase2.services.reschedule_service import list_requests, update_status
from phase2.services.gmail_service import send_email

router = APIRouter()

APPROVE_MAIL = """Dear Candidate,

Thank you for informing us regarding your inability to attend the scheduled interview.

Your interview has been successfully rescheduled. We will share the updated interview invitation and Google Meet link shortly.

We appreciate your communication and look forward to speaking with you.

Best Regards,
HR Team"""

REJECT_MAIL = """Dear Candidate,

Thank you for your email.

Unfortunately, we are unable to accommodate a rescheduling request at this time. We kindly request that you attend the interview as originally scheduled.

If there are exceptional circumstances, please contact the HR team directly.

Best Regards,
HR Team"""


class ActionIn(BaseModel):
    request_id: int


@router.post("/check-mails")
def check_mails():
    return monitor_inbox(max_results=5)


@router.get("/pending")
def pending():
    return list_requests(status="pending")


@router.post("/approve")
def approve(payload: ActionIn):
    reqs = [r for r in list_requests() if r["request_id"] == payload.request_id]
    if not reqs:
        raise HTTPException(404, "Request not found")
    req = reqs[0]
    send_email(req["candidate_email"], "Interview Rescheduled",
               APPROVE_MAIL, req.get("thread_id"))
    update_status(payload.request_id, "approved")
    # TODO: call your scheduling_agent to create new Calendar event + Meet link
    return {"status": "approved", "request_id": payload.request_id}


@router.post("/reject")
def reject(payload: ActionIn):
    reqs = [r for r in list_requests() if r["request_id"] == payload.request_id]
    if not reqs:
        raise HTTPException(404, "Request not found")
    req = reqs[0]
    send_email(req["candidate_email"], "Interview Schedule",
               REJECT_MAIL, req.get("thread_id"))
    update_status(payload.request_id, "rejected")
    return {"status": "rejected", "request_id": payload.request_id}
