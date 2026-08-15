from fastapi import APIRouter, Depends
from core_utils import get_current_user
from .cartitem_service import CartItemService


b_router = APIRouter(prefix="/cartitems", tags=["Cartitems 🛒"])


@b_router.post("")
def adding_to_basket(product_id:int, user:dict = Depends(get_current_user)):
    return CartItemService.add_new_item(
        product_id=product_id,
        user=user
    )


@b_router.get("")
def get_all_items(user:dict= Depends(get_current_user)):
    return CartItemService.get_all_items_for_specific_user(
        user=user
    )


@b_router.delete('/{product_id}')
def delete_from_cart(product_id:int, user:dict = Depends(get_current_user)):
    return CartItemService.delete_product_from_cartitem(product_id=product_id, user=user)