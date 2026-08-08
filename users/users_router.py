from fastapi import APIRouter
from fastapi import Request, Depends
from depends import get_current_user
from fastapi import Response

from .user_service import UserService



user_router = APIRouter(prefix="/users", tags=["Users👤"])


@user_router.get('/me')
def get_me(requ:Request, user_id:int = Depends(get_current_user)):
    return UserService.get_me_by_id(user_id=user_id)


@user_router.post('/logout')
def exit_with_acconunt(resp:Response, request:Request):
    return UserService.logout(resp, request)


@user_router.delete("/{user_id}")
def delete_users(user_id: int):
    return UserService.delete_user(user_id=user_id)