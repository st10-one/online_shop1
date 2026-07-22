from auth.models import CreateUserOrm
from sqlalchemy import select
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