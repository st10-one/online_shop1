from fastapi import HTTPException, Response

from .schemas import BaseUser, ShowUser, UserRegistrations
from .utils import create_access_token, verify_user


from .sql_handler import AuthRepo


class AuthService:
    @staticmethod
    def registrations_user(response:Response, usr:BaseUser):
        new_user = AuthRepo.create_new_user_in_db(user_data=usr)

        if new_user:
            token_payload = {
                "id": new_user.id,
                "sub": new_user.username,
                "email": new_user.email
            }

            token = create_access_token(
                data=token_payload,
                expire_time=15
            )

            response.set_cookie(
                key="access_token",
                value=f"Bearer {token}",
                httponly=True,
                samesite="lax"
            )

            return ShowUser.model_validate(new_user)
    
        raise HTTPException(
            status_code=400,
            detail="Сталася помилка"
        )

    @staticmethod
    def login_user(registrations_data:UserRegistrations, response:Response):
        users = AuthRepo.find_user_by_email(email=registrations_data.email)

        if not users:
            raise HTTPException(
                status_code=404,
                detail="Користувача не знайдено!"
            )

        user_password = registrations_data.password
        db_user_password = users.password


        if isinstance(db_user_password, str) and db_user_password.startswith('\\x'):
            db_user_password = bytes.fromhex(db_user_password[2:])


        verifty = verify_user(
            my_password=user_password,
            hs_password=db_user_password
        )

        if not verifty:
            raise HTTPException(
                status_code=404,
                detail="Неправильний пароль"
            )
        
        token_payload = {
            "id": users.id,
            "sub": users.username,
            "email": users.email
            }

        token = create_access_token(
                data=token_payload,
                expire_time=15
            )

        response.set_cookie(
                key="access_token",
                value=f"Bearer {token}",
                httponly=True,
                samesite="lax"
            )


        return {
            "token": token,
            "type": "Bearer"
        }


