
from typing import Annotated

from fastapi import HTTPException, Request, File, UploadFile
import jwt

from config import settings


def get_current_user(request:Request) -> int | None:
    token = request.cookies.get(
        "access_token"
    )


    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Ви незареєстровані"
        )


    if token.startswith("Bearer "):
        token = token.split()[1]

    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.SECRET_JWT,
            algorithms=["HS256"]
        )
        
        my_id = payload.get("id")

        if my_id:
            return my_id
        
        return None
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Токен згорів"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Токен підроблений або неправельний"
        )


ProductImage = Annotated[UploadFile, File()]