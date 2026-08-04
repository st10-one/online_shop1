from .schemas import Orders, ShowOrder
from fastapi import Request, HTTPException

from .sql_handler import OrderDTO
from depends import get_current_user, get_active_user


class OrderService:
    @staticmethod
    def make_order(data:Orders, request:Request):
        my_id = get_current_user(request=request)

        if not my_id:
            raise HTTPException(
                status_code=404
            )

        active_user = get_active_user(user_id=my_id)

        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )

        my_order = OrderDTO.add_order(
            user_id=my_id,
            data=data
        )

        if not my_order:
            raise HTTPException(
                status_code=400,
                detail="Кошик пустий"
            )

        return ShowOrder.model_validate(my_order)

    @staticmethod
    def cancel_order(order_id:int, request:Request):
        my_id = get_current_user(request=request)

        if not my_id:
            raise HTTPException(
                status_code=404
            )

        active_user = get_active_user(user_id=my_id)
        
        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )


        cancel_order = OrderDTO.cancel_order_by_id(
            order_id=order_id,
            user_id=my_id
        )

        if cancel_order is None:
            raise HTTPException(
                status_code=400,
                detail="Замовлення вже було скасовано"
            )

        return cancel_order
