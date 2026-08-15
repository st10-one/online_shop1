from fastapi import APIRouter, Depends
from .order_service import OrderService
from core_utils import get_current_user
from .schemas import Orders


orders_router = APIRouter(prefix="/orders", tags=['Orders 📋'])


@orders_router.post("")
def make_order(data:Orders, user:dict = Depends(get_current_user)):
    return OrderService.make_order(
        data=data,
        user=user
    )


@orders_router.post('/cancel/{order_id}')
def cancel_order(order_id:int, user:dict= Depends(get_current_user)):
    return OrderService.cancel_order(
        order_id=order_id,
        user=user
    )


@orders_router.get('')
def get_my_orders(user:dict = Depends(get_current_user)):
    return OrderService.get_all_the_my_order(
        user=user
    )