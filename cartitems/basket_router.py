from fastapi import APIRouter
from .cartitem_service import CartItemService
from fastapi import Request


b_router = APIRouter(prefix="/basket", tags=["Basket"])


@b_router.post("")
def adding_to_basket(product_id:int, request:Request):
    return CartItemService.add_new_item(
        product_id=product_id,
        request=request
    )

@b_router.get("")
def get_all_items():
    return CartItemService.get_all_items()