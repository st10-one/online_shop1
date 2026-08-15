from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from decimal import Decimal


class CreateProduct(BaseModel):
    name:str
    price:Decimal = Field(ge=0.1)
    quantity:int = Field(ge=0)
    description:str

    model_config = {'from_attributes':True}


class ShowProduct(CreateProduct):
    id:int
    image_url:str
    create_at:datetime

    model_config = {'from_attributes':True}


class ReturnProductTabulation(BaseModel):
    limit:int = Field(ge=0)
    offset:int = Field(ge=0)

    