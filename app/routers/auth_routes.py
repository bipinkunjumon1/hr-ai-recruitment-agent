from fastapi import APIRouter

from fastapi import Depends

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from auth.jwt_handler import (
    create_access_token
)

router = APIRouter()


@router.post("/login")
def login(

    form_data: OAuth2PasswordRequestForm = Depends()
):

    if (

        form_data.username == "admin"

        and

        form_data.password == "admin123"
    ):

        token = create_access_token(

            {
                "sub":
                form_data.username
            }
        )

        return {

            "access_token":
            token,

            "token_type":
            "bearer"
        }

    return {

        "message":
        "Invalid Credentials"
    }