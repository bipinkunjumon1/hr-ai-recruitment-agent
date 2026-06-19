from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from services.resume_service import (
    ResumeService
)

from auth.security import (
    verify_token
)

router = APIRouter()

resume_service = ResumeService()


@router.post("/upload-resume")
async def upload_resume(

    file: UploadFile = File(...),

    user=Depends(
        verify_token
    )
):

    try:

        allowed_extensions = [

            ".pdf",

            ".docx",

            ".png",

            ".jpg",

            ".jpeg"
        ]

        if not any(

            file.filename
            .lower()
            .endswith(ext)

            for ext in allowed_extensions
        ):

            raise HTTPException(

                status_code=400,

                detail=(
                    "Supported formats: "
                    "PDF, DOCX, PNG, JPG, JPEG"
                )
            )

        result = await resume_service.upload_and_process(
            file
        )

        return result

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )