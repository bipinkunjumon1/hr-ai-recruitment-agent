import json

from services.groq_service import GroqService


class ResumeAgent:

    def __init__(self):
        self.llm = GroqService()

    def process(self, resume_text: str):

        prompt = f"""
You are an ATS Resume Extraction Agent.

Extract information from the resume.

Return ONLY valid JSON.

Schema:

{{
    "full_name": "",
    "email": "",
    "phone": "",

    "technical_skills": [],
    "soft_skills": [],

    "education": [],

    "total_experience_years": 0,

    "work_experience": [],

    "projects": [],

    "certifications": [],

    "summary": ""
}}

Instructions:
- Extract the candidate's full name.
- Extract email and phone number.
- Extract all technical skills.
- Extract soft skills if available.
- Calculate total years of experience.
- Extract education details.
- Extract work experience details.
- Extract projects.
- Extract certifications.
- Generate a concise professional summary in 2-3 sentences.
- Return ONLY valid JSON.
- Do not include markdown or explanations.

Resume:

{resume_text}
"""

        response = self.llm.generate(prompt)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(response)