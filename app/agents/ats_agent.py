import json

from services.groq_service import GroqService


class ATSAgent:

    def __init__(self):
        self.llm = GroqService()

    def evaluate_candidate(self, jd_data: dict, resume_data: dict):

        prompt = f"""
You are an ATS Recruitment Evaluation Agent.

Evaluate the candidate against the job description.

Scoring Criteria:

1. Required Skills Match (40%)
2. Preferred Skills Match (10%)
3. Experience Match (20%)
4. Education Match (10%)
5. Project Relevance (15%)
6. Overall JD Alignment (5%)

Return ONLY valid JSON.

Schema:

{{
    "candidate_name": "",
    "ats_score": 0,
    "skill_match_score": 0,
    "experience_score": 0,
    "education_score": 0,
    "project_score": 0,
    "summary": "",
    "selection_reason": "",
    "matched_skills": [],
    "missing_skills": [],
    "recommendation": ""
}}

JOB DESCRIPTION:

{jd_data}

CANDIDATE RESUME:

{resume_data}
"""

        response = self.llm.generate(prompt)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        result = json.loads(response)

        # Override with actual resume data

        result["candidate_name"] = (
            resume_data.get(
                "full_name",
                ""
            )
        )

        result["candidate_email"] = (
            resume_data.get(
                "email",
                ""
            )
        )

        return result