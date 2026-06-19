from typing import TypedDict

class RecruitmentState(TypedDict):
    jd_data: dict
    resumes: list

    rankings: list
    status: str