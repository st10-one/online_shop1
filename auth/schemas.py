from pydantic import BaseModel, EmailStr
from pydantic import Field

from datetime import datetime


class UserRegistrations(BaseModel):
    email:EmailStr
    password:str = Field(
        min_length=6
    )

    model_config = {'from_attributes':True}


class ShowUser(BaseModel):
    id:int
    username:str
    email:EmailStr
    create_at:datetime

    model_config = {'from_attributes':True}
    


class BaseUser(BaseModel):
    username:str
    email:EmailStr
    password:str = Field(
        min_length=6
    )

    model_config = {'from_attributes':True}
    


    






