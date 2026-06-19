from pydantic import BaseModel


class CandidateRanking(BaseModel):

    candidate_name: str

    ats_score: float

    rank: int

    skill_match_score: float

    experience_score: float

    education_score: float

    project_score: float

    summary: str

    selection_reason: str

    matched_skills: list

    missing_skills: list

    recommendation: str