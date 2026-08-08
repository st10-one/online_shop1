from fastapi import APIRouter, Depends
from .order_service import OrderService
from depends import get_current_user
from .schemas import Orders


orders_router = APIRouter(prefix="/orders", tags=['Orders 📋'])


@orders_router.post("")
def make_order(data:Orders, user_id:int = Depends(get_current_user)):
    return OrderService.make_order(
        data=data,
        my_id=user_id
    )


@orders_router.post('/cancel/{order_id}')
def cancel_order(order_id:int, user_id:int = Depends(get_current_user)):
    return OrderService.cancel_order(
        order_id=order_id,
        my_id=user_id
    )


@orders_router.get('')
def get_my_orders(user_id:int = Depends(get_current_user)):
    return OrderService.get_all_the_my_order(
        my_id=user_id
    )