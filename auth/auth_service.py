from fastapi import HTTPException, Request, Response

from .schemas import BaseUser, ShowUser, UserRegistrations, TokenInfo
from .utils import create_access_token, verify_user, create_refresh_token, decoded_refresh_token
from depends import get_active_user


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

            refresh_token = create_refresh_token(
                data={
                    "user_id": new_user.id
                }
            )

            response.set_cookie(
                key="access_token",
                value=f"Bearer {token}",
                httponly=True,
                samesite="lax"
            )

            response.set_cookie(
                key="refresh_token",
                value=f"Bearer {refresh_token}",
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
                detail="Неправильний email або пароль"
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
                detail="Неправильний email або пароль"
            )
        
        token_payload = {
            "id": users.id,
            "sub": users.username,
            "email": users.email
            }

        access_token = create_access_token(
                data=token_payload,
                expire_time=15
            )


        refresh_token = create_refresh_token(
            data={
                "user_id": users.id
            }
        )

        response.set_cookie(
                key="access_token",
                value=f"Bearer {access_token}",
                httponly=True,
                samesite="lax"
            )

        response.set_cookie(
                key="refresh_token",
                value=f"Bearer {refresh_token}",
                httponly=True,
                samesite="lax"
            )

        return TokenInfo(
            access_token=access_token,
            token_type="Bearer"
        )


    @staticmethod
    def update_access_token(user_id:int, response:Response):
        active_user = get_active_user(user_id=user_id)
        
        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )

        if user_id is None:
            raise HTTPException(
                status_code=404,
                detail="user_id not found"
            )

        users = AuthRepo.find_user_by_id(user_id=user_id)

        if users is None:
            raise HTTPException(
                status_code=404,
                detail="user not found"
            )


        token_payload = {
                    "id": users.id,
                    "sub": users.username,
                    "email": users.email
                    }
        
        update_access_token = create_access_token(
                    data=token_payload,
                    expire_time=15
                )

        response.set_cookie(
                key="access_token",
                value=f"Bearer {update_access_token}",
                httponly=True,
                samesite="lax"
            )

        return TokenInfo(
            access_token=update_access_token,
            token_type="Bearer"
        )