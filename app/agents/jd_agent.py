import json

from services.groq_service import GroqService


class JDAgent:

    def __init__(self):

        self.llm = GroqService()

    def process(self, jd_text: str):

        prompt = f"""
You are an ATS Job Description Extraction Agent.

Extract information from the Job Description.

Return ONLY valid JSON.

Schema:

{{
    "job_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "good_to_have_skills": [],
    "soft_skills": [],
    "education": [],
    "min_experience": 0,
    "max_experience": 0,
    "responsibilities": [],
    "summary": ""
}}

Job Description:

{jd_text}
"""

        response = self.llm.generate(prompt)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(response)