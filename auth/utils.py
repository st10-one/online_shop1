import jwt
import bcrypt

from fastapi import HTTPException, Request

from datetime import datetime, timezone, timedelta
from jwt.exceptions import InvalidKeyError, InvalidAlgorithmError,ExpiredSignatureError, InvalidTokenError

from config import settings



def create_access_token(data:dict, expire_time:int|None = None) -> str | None:
    to_encode = data.copy()

    if expire_time:
        exp = datetime.now(timezone.utc) + timedelta(minutes=expire_time)
    else:
        exp = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": exp})


    try:
        access_token = jwt.encode(
            payload=to_encode,
            algorithm="HS256",
            key=settings.SECRET_JWT
        )
        return access_token
    except (InvalidAlgorithmError, InvalidKeyError) as a:
        return None



def hash_password(my_password:str):
    return bcrypt.hashpw(
        password=my_password.encode(),
        salt=bcrypt.gensalt()
    )


def verify_user(my_password:str, hs_password:bytes) -> bool:
    return bcrypt.checkpw(
        password=my_password.encode(encoding="utf-8"),
        hashed_password=hs_password
    )


def get_token_by_cookies(request:Request) -> bool | None:
    token = request.cookies.get(
        "access_token"
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Токен незнайдено"
        )


    if token.startswith("Bearer "):
        token = token.split()[1]

    try:
        jwt.decode(
            jwt=token,
            key=settings.SECRET_JWT,
            algorithms=["HS256"]
        )
        return True
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Токен згорів"
        )
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Токен підроблений або неправельний"
        )


