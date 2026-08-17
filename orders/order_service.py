from .schemas import Orders, ShowOrder
from fastapi import HTTPException

from .sql_handler import OrderDTO


class OrderService:
    @staticmethod
    def make_order(data:Orders, user:dict):
        my_order = OrderDTO.add_order(
            user_id=user.id,
            data=data
        )

        if not my_order:
            raise HTTPException(
                status_code=400,
                detail="Кошик пустий"
            )

        return ShowOrder.model_validate(my_order)


    @staticmethod
    def cancel_order(order_id:int, user:dict):
        cancel_order = OrderDTO.cancel_order_by_id(
            order_id=order_id,
            user_id=user.id
        )

        if cancel_order is None:
            raise HTTPException(
                status_code=400,
                detail="Замовлення вже було скасовано"
            )

        return cancel_order


    @staticmethod
    def get_all_the_my_order(user:dict):
        get_orders = OrderDTO.get_my_orders(
            user_id=user.id
        )

        if get_orders is None:
            raise HTTPException(
                status_code=404,
                detail="Your orders is not found"
            )

        return {"my_orders": get_orders}