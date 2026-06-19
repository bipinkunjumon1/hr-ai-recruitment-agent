from typing import List

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

router = APIRouter()


@router.post("/process")
async def process_recruitment(
    jd_file: UploadFile = File(...),
    resumes: List[UploadFile] = File(...)
):

    return {
        "jd": jd_file.filename,
        "resumes": [r.filename for r in resumes]
    }