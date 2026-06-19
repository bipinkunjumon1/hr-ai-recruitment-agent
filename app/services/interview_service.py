from agents.scheduling_agent import (
    SchedulingAgent
)

import json


class InterviewService:

    def __init__(self):

        self.agent = (
            SchedulingAgent()
        )

    def schedule(

        self,

        candidate_id,

        start_time,

        end_time
    ):

        with open(

            "uploads/rankings/ranking.json",

            "r"

        ) as f:

            candidates = json.load(f)

        candidate = None

        for c in candidates:

            if c["candidate_id"] == candidate_id:

                candidate = c

                break

        if candidate is None:

            raise Exception(
                "Candidate not found"
            )

        candidate_name = (
            candidate["candidate_name"]
        )

        candidate_email = (
            candidate["candidate_email"]
        )

        result = self.agent.schedule(

            candidate_name,

            candidate_email,

            start_time,

            end_time
        )

        return result