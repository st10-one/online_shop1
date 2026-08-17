from fastapi import HTTPException
from fastapi import Request
from fastapi import Response

from auth.schemas import ShowUser
from .sql_handler import UserDTO
from core_utils import change_user_active


class UserService:
    @staticmethod
    def get_me_by_id(user:dict) -> ShowUser | Exception:
        my_user = UserDTO.get_current_user_by_id(current_id=user.id)
        return ShowUser.model_validate(my_user)


    def logout(response:Response, request:Request, user:dict) -> bool | Exception:
        token = request.cookies.get(
            "access_token"
        )

        refresh_token = request.cookies.get(
            "refresh_token"
        )

        if token is None and refresh_token is None:
            raise HTTPException(
                status_code=401,
                detail="Ви вже вийшли або незареєстровані"
            )
        
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')


        logout_user_id = change_user_active(
            is_active=False,
            user_id=user.id
        )

        return {
            "message": "user logout",
            "user_id":logout_user_id
        }


    def delete_user(user_id:int):
        deleted_user = UserDTO.delete_user_by_id(user_id=user_id)

        if not deleted_user:
            raise HTTPException(
                status_code=404,
                detail="користувача неіснує"
            )

        return {"id": deleted_user}