from fastapi import APIRouter
from fastapi import Request
from fastapi import Response
from .user_service import UserService



user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get('/me')
def get_me(requ:Request):
    return UserService.get_me_by_id(request=requ)


@user_router.post('/logout')
def exit_with_acconunt(resp:Response, request:Request):
    return UserService.logout(resp, request)