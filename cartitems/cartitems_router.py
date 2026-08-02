from fastapi import APIRouter
from .cartitem_service import CartItemService
from fastapi import Request


b_router = APIRouter(prefix="/cartitems", tags=["Cartitems 🛒"])


@b_router.post("")
def adding_to_basket(product_id:int, request:Request):
    return CartItemService.add_new_item(
        product_id=product_id,
        request=request
    )

@b_router.get("")
def get_all_items(request:Request):
    return CartItemService.get_all_items_for_specific_user(request=request)


@b_router.delete('/{product_id}')
def delete_from_cart(product_id:int):
    return CartItemService.delete_product_from_cartitem(product_id=product_id)