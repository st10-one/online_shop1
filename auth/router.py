from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi import Body
from fastapi.security import OAuth2PasswordBearer
from .schemas import UserRegistrations, BaseUser
from .auth_service import AuthService
from .utils import get_token_by_cookies



oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/auth", tags=["registration and auth"])

@router.post("/login")
def login(resp:Response, login_data:UserRegistrations = Body(embed=True)):
    return AuthService.login_user(
        registrations_data=login_data,
        response=resp
    )


@router.post("/registration")
def create_user(resp:Response, registration_data:BaseUser = Body(embed=True)):
    return AuthService.registrations_user(
        usr=registration_data,
        response=resp
    )
router.post("/protect_router", dependencies=[Depends(get_token_by_cookies)])
def i():
    return {"Secret": "abc"}