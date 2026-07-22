from fastapi import HTTPException

from db import session
from .models import CreateUserOrm
from .schemas import BaseUser
from .utils import hash_password
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select



class AuthRepo:
    @staticmethod
    def create_new_user_in_db(user_data:BaseUser) -> CreateUserOrm:
        try:
            with session() as s:
                user_obj = CreateUserOrm(
                    username = user_data.username,
                    email = user_data.email,
                    password = hash_password(user_data.password)
                )

                s.add(user_obj)
                s.commit()
                s.refresh(user_obj)

                return user_obj
        except IntegrityError:
            raise HTTPException(status_code=400,  detail="Такий користувач вже існує")
        except SQLAlchemyError:
            raise HTTPException(400)

    @staticmethod
    def find_user_by_email(email:str) -> CreateUserOrm | None:
        query = select(CreateUserOrm).where(CreateUserOrm.email == email)

        with session() as s:
            get_user = s.execute(statement=query)            
            return get_user.scalar_one_or_none()
            
