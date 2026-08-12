from fastapi import APIRouter
from fastapi import Request, Depends
from dependency import get_current_user
from fastapi import Response

from .user_service import UserService



user_router = APIRouter(prefix="/users", tags=["Users👤"])


@user_router.get('/me')
def get_me(user:dict = Depends(get_current_user)):
    return UserService.get_me_by_id(user=user)


@user_router.post('/logout')
def exit_with_acconunt(resp:Response, request:Request, user:dict = Depends(get_current_user)):
    return UserService.logout(resp, request, user)


@user_router.delete("/{user_id}")
def delete_users(user_id: int, user:dict = Depends(get_current_user)):
    return UserService.delete_user(user_id=user_id, user=user)