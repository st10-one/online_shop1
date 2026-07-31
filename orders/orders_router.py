from fastapi import APIRouter, Request
from .order_service import OrderService
from .schemas import Orders


orders_router = APIRouter(prefix="/orders", tags=['orders'])


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