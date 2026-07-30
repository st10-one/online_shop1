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