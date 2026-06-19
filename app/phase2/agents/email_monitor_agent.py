from phase2.services.gmail_service import read_unread_emails, mark_as_read
from phase2.services.reschedule_service import add_request, list_requests
from phase2.agents.email_classifier_agent import classify_email


def monitor_inbox(max_results: int = 5):
    emails = read_unread_emails(max_results)
    created = []
    debug = []
    existing_requests = list_requests()

    for e in emails:
        thread_id = e.get("thread_id")

        # Skip emails already turned into a request
        duplicate = any(
    r.get("message_id") == e["id"]
    for r in existing_requests
)
        if duplicate:
            debug.append({
                "from": e["candidate_email"],
                "subject": e["subject"],
                "classified_as": "skipped",
                "reason": "Duplicate thread (already a request)",
            })
            mark_as_read(e["id"])
            continue

        result = classify_email(e["subject"], e["body"])

        debug.append({
            "from": e["candidate_email"],
            "subject": e["subject"],
            "body_preview": (e["body"][:200] + "…") if e["body"] else "(empty)",
            "classified_as": result.get("email_type"),
            "confidence": result.get("confidence"),
            "reason": result.get("reason"),
        })

        if result.get("email_type") == "reschedule":
            req = add_request({
    "candidate_name": e["candidate_name"],
    "candidate_email": e["candidate_email"],
    "subject": e["subject"],
    "body": e["body"],
    "reason": result.get("reason", ""),
    "confidence": result.get("confidence", 0),

    # NEW
    "message_id": e["id"],
    "thread_id": thread_id,
})
            created.append(req)

        mark_as_read(e["id"])

    return {
        "processed": len(emails),
        "reschedule_requests": created,
        "debug": debug,
    }
