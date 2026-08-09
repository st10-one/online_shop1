from fastapi import HTTPException
from fastapi import Request
from fastapi import Response

from auth.schemas import ShowUser
from .sql_handler import UserDTO
from depends import change_user_active, get_active_user


class UserService:
    @staticmethod
    def get_me_by_id(user_id:int) -> ShowUser | Exception:

        if not user_id:
            raise HTTPException(
                status_code=404,
                detail="id незнайдено!"
            )

        active_user = get_active_user(user_id=user_id)


        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )
        

        
        my_user = UserDTO.get_current_user_by_id(current_id=user_id)

        if not my_user:
            raise HTTPException(
                status_code=404,
                detail="користувача неіснує!"
            )

        if my_user.is_active is False:
            raise HTTPException(
                status_code=403,
                detail="User is not actived"
            )
        
        return ShowUser.model_validate(my_user)


    def logout(response:Response, request:Request, user_id:int) -> bool | Exception:
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
            user_id=user_id
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