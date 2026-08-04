from pydantic import BaseModel
from datetime import datetime



class Orders(BaseModel):
    phone:str
    address:str


class ShowOrder(BaseModel):
    id:int
    order_id:int 
    product_id:int
    price:float
    quantity:int


    model_config = {"from_attributes":True}