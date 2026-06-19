from pydantic import BaseModel

class JDResponse(BaseModel):
    job_title: str
    required_skills: list
    preferred_skills: list
    good_to_have_skills: list
    soft_skills: list
    education: list
    min_experience: int
    max_experience: int
    responsibilities: list
    summary: str