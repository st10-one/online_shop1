from typing import Annotated

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from products.schemas import CreateProduct
from db import session
from auth.models import CreateUserOrm
from fastapi import HTTPException, Request, File, UploadFile
import jwt

from config import settings
from fastapi import Form
from decimal import Decimal

def get_product_data(
    name: str = Form(...),
    price: Decimal = Form(...),
    quantity: int = Form(...),
    description: str = Form(...),
) -> CreateProduct:

    return CreateProduct(
        name=name,
        price=price,
        quantity=quantity,
        description=description,
    )

def change_user_active(is_active:bool, user_id:int) -> bool:
    if not isinstance(is_active, bool):
        return "Incorect of the type"

    update_user_active_query = update(CreateUserOrm).where(CreateUserOrm.id == user_id).values(is_active = is_active).returning(CreateUserOrm.id)

    try:
        with session() as s:
            res = s.execute(update_user_active_query).scalar_one_or_none()
            s.commit()

            return res
    except SQLAlchemyError as e:
        s.rollback()
        raise e


def check_admin(user_data:dict) -> Exception | bool:
    if user_data["role"] != "ADMIN":
        return False
    return True

def get_current_user(request:Request) -> dict | None:
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

        if payload:
            return payload
        
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



def get_active_user(user_id:int) -> bool | None:
    active_query = select(CreateUserOrm).where(CreateUserOrm.id == user_id) # SELECT users.id FROM users WHERE id = user_id

    with session() as s:
        user = s.execute(active_query).scalar_one_or_none()

    if user is None:
        return None

    if not user.is_active:
        return None
    return True 


ProductImage = Annotated[UploadFile, File()]