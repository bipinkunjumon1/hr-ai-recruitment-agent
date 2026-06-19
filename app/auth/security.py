from jose import (
    jwt,
    JWTError
)

from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import (
    OAuth2PasswordBearer
)

from auth.jwt_handler import (
    SECRET_KEY,
    ALGORITHM
)


from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)

def verify_token(

    token: str = Depends(
        oauth2_scheme
    )
):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[
                ALGORITHM
            ]
        )

        return payload

    except JWTError:

        raise HTTPException(

            status_code=401,

            detail="Invalid Token"
        )