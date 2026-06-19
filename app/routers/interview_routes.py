from fastapi import (
    APIRouter
)

from pydantic import (
    BaseModel
)

from services.interview_service import (
    InterviewService
)

from fastapi import Depends

from auth.security import verify_token

router = APIRouter()

service = InterviewService()


from pydantic import BaseModel


class InterviewRequest(
    BaseModel
):

    candidate_id: int

    start_time: str

    end_time: str


@router.post("/schedule")
def schedule_interview(

    request: InterviewRequest,

    user=Depends(
        verify_token
    )
):

    return service.schedule(

        request.candidate_id,

        request.start_time,

        request.end_time
    )