from fastapi import APIRouter
from fastapi import Response, Request
from fastapi import Body
from fastapi.security import OAuth2PasswordBearer
from .schemas import UserRegistrations, BaseUser, TokenInfo, ShowUser
from .auth_service import AuthService



oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/auth", tags=["registration and auth"])

@router.post("/login")
def login(resp:Response, login_data:UserRegistrations = Body(embed=True)) -> TokenInfo:
    return AuthService.login_user(
        registrations_data=login_data,
        response=resp
    )


@router.post("/registration")
def create_user(resp:Response, registration_data:BaseUser = Body(embed=True)) -> ShowUser:
    return AuthService.registrations_user(
        usr=registration_data,
        response=resp
    )


@router.post('/refresh')
def refresh_token(request:Request, response:Response) -> TokenInfo:
    return AuthService.update_access_token(
        request=request,
        response=response
    )