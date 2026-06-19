from services.jd_service import JDService
from services.resume_service import ResumeService
from services.ats_service import ATSService
import json
import os

jd_service = JDService()

resume_service = ResumeService()

ats_service = ATSService()

def process_jd_node(state):

    print("PROCESS JD NODE")

    if not state.get("jd_data"):
        raise ValueError("JD data missing")

    return state

def process_resumes_node(state):

    print("PROCESS RESUMES NODE")

    resumes = state.get("resumes", [])

    if not resumes:
        raise ValueError("No resumes found")

    return state




def ranking_node(state):

    print("RANKING NODE")

    rankings = ats_service.rank_candidates(
        state["jd_data"],
        state["resumes"]
    )

    state["rankings"] = rankings

    os.makedirs(
        "uploads/rankings",
        exist_ok=True
    )

    with open(
        "uploads/rankings/ranking.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            rankings,
            f,
            indent=4,
            ensure_ascii=False
        )

    return state



def finalize_node(state):

    print("FINALIZE NODE")

    state["status"] = "completed"

    return state