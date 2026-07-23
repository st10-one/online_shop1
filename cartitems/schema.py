from pydantic import BaseModel, Field


class CartItem(BaseModel):
    id:int = Field(ge=0)
    user_id:int = Field(ge=0)
    product_id:int = Field(ge=0)
    quantity:int = Field(ge=0)

    model_config = {'from_attributes':True}
