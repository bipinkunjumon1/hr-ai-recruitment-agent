from graph.workflow import build_graph

graph = build_graph()

result = graph.invoke({
    "jd_data": {"skills": ["Python"]},
    "resumes": [
        {
            "full_name": "Test User",
            "skills": ["Python"]
        }
    ],
    "rankings": [],
    "shortlisted_candidates": [],
    "interview_scheduled": False,
    "emails_sent": False,
    "status": "started"
})