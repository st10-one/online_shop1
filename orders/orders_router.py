from fastapi import APIRouter, Request
from .order_service import OrderService
from .schemas import Orders


orders_router = APIRouter(prefix="/orders", tags=['Orders 📋'])


@orders_router.post("")
def make_order(data:Orders, request:Request):
    return OrderService.make_order(
        data=data,
        request=request
    )


@orders_router.post('/cancel/{order_id}')
def cancel_order(order_id:int, request:Request):
    return OrderService.cancel_order(
        order_id=order_id,
        request=request
    )


@orders_router.get('')
def get_my_orders(request:Request):
    return OrderService.get_all_the_my_order(
        request=request
    )