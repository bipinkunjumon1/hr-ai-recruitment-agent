from services.jd_service import JDService
from services.resume_service import ResumeService
from services.ats_service import ATSService
from graph.workflow import build_graph

import json
import os

from graph.workflow import build_graph

class WorkflowService:

    def __init__(self):
        self.graph = build_graph()

    async def process(self):

        with open(
            "uploads/jd/jd.json",
            "r"
        ) as f:
            jd_data = json.load(f)

        resumes = []

        for file in os.listdir(
            "uploads/resumes"
        ):

            if file.endswith(".json"):

                with open(
                    os.path.join(
                        "uploads/resumes",
                        file
                    ),
                    "r"
                ) as f:

                    resumes.append(
                        json.load(f)
                    )

        return self.graph.invoke({

            "jd_data": jd_data,

            "resumes": resumes,

            "rankings": [],

            "shortlisted_candidates": [],

            "interview_scheduled": False,

            "emails_sent": False,

            "status": "started"
        })