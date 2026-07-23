from fastapi import HTTPException
from fastapi import Request
from fastapi import Response

from auth.schemas import ShowUser
from .sql_handler import UserDTO
from .utils import get_current_user


class UserService:
    @staticmethod
    def get_me_by_id(request:Request) -> ShowUser | Exception:
        my_id = get_current_user(request=request)

        if not my_id:
            raise HTTPException(
                status_code=404,
                detail="id незнайдено!"
            )
        
        my_user = UserDTO.get_current_user_by_id(current_id=my_id)

        if not my_id:
            raise HTTPException(
                status_code=404,
                detail="користувача неіснує!"
            )
        
        return ShowUser.model_validate(my_user)


    def logout(response:Response, request:Request) -> bool | Exception:
        token = request.cookies.get(
            "access_token"
        )
        if token is None:
            raise HTTPException(
                status_code=401,
                detail="Ви вже вийшли або незареєстровані"
            )

        response.delete_cookie('access_token')

        return True

    def delete_user(user_id:int):
        deleted_user = UserDTO.delete_user_by_id(user_id=user_id)

        if not deleted_user:
            raise HTTPException(
                status_code=404,
                detail="користувача неіснує"
            )

        return {"id": deleted_user}