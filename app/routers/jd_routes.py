from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from services.jd_service import (
    JDService
)

from auth.security import (
    verify_token
)

router = APIRouter()

jd_service = JDService()


@router.post("/upload-jd")
async def upload_jd(

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

        result = await jd_service.upload_and_process(
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