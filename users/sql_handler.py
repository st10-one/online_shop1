from auth.models import CreateUserOrm
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from db import session


class UserDTO:
    @staticmethod
    def get_current_user_by_id(current_id:int):
        sql_query = select(CreateUserOrm).where(CreateUserOrm.id == current_id)

        try:
            with session() as s:
                result = s.execute(sql_query)
                if result:
                    return result.scalar_one_or_none()
                return None
        except SQLAlchemyError as e:
            raise e


    @staticmethod
    def delete_user_by_id(user_id:int) -> CreateUserOrm:
        sql_query = delete(CreateUserOrm).where(CreateUserOrm.id == user_id).returning(CreateUserOrm.id)

        try:
            with session() as s:
                result = s.execute(sql_query).scalar_one_or_none()
                s.commit()

                if not result:
                    return None

                return result
        except SQLAlchemyError as e:
            print(e)
            raise e
