from pydantic import BaseModel


class ResumeResponse(BaseModel):
    full_name: str
    email: str
    phone: str

    technical_skills: list[str]
    soft_skills: list[str]

    education: list[str]

    total_experience_years: float

    work_experience: list[str]

    projects: list[str]

    certifications: list[str]

    summary: str