from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class CreateProduct(BaseModel):
    name:str
    price:float = Field(ge=0.01)
    quantity:int = Field(ge=0)
    description:str
    image_url:str

    model_config = {'from_attributes':True}


class ShowProduct(CreateProduct):
    id:int
    create_at:datetime

    model_config = {'from_attributes':True}


class ReturnProductTabulation(BaseModel):
    limit:int = Field(ge=0)
    offset:int = Field(ge=0)

    