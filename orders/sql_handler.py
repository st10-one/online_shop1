from db import session
from .schemas import Orders
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update
from cartitems.model import CartItemsOrm
from .models import MakeOrderOrm, DetailOrderOrm
from products.model import CreateProductOrm 



class OrderDTO:
    @staticmethod
    def add_order(user_id:int, data:Orders):
        try:
            one_query = select(CartItemsOrm).where(CartItemsOrm.user_id == user_id)

            with session() as s:
                cart_items = s.execute(one_query).scalars().all()


                if not cart_items:
                    print("кошик пустий")
                    return None


                new_order = MakeOrderOrm(
                    user_id = user_id,
                    adderss=data.address,
                    phone=data.phone,
                    order_status="SUCCESS"
                )

                s.add(new_order)
                s.flush()


                for item in cart_items:
                    two_query = select(CreateProductOrm).where(CreateProductOrm.id == item.product_id)
                    get_product = s.execute(two_query).scalar_one_or_none()

                    detail = DetailOrderOrm(
                        order_id = new_order.id,
                        product_id = item.product_id,
                        quantity = item.quantity,
                        price = get_product.price
                    )

                    s.add(detail)
                    s.flush()

                    s.execute(delete(CartItemsOrm).where(CartItemsOrm.user_id == user_id).returning(CartItemsOrm.id))

                s.commit()
                s.refresh(new_order)
                s.refresh(detail)

                return detail
        except SQLAlchemyError as e:
            raise e


    @staticmethod
    def cancel_order_by_id(order_id:int, user_id:int):
        get_detail_order_query = select(DetailOrderOrm).where(DetailOrderOrm.order_id == order_id)

        try:
            with session() as s:
                get_detail_order = s.execute(get_detail_order_query).scalar_one_or_none()

                if get_detail_order is None:
                    return None

                update_status_query = update(MakeOrderOrm).where(
                    MakeOrderOrm.id == get_detail_order.order_id,
                    MakeOrderOrm.user_id == user_id,
                    MakeOrderOrm.order_status == "SUCCESS"
                ).values(
                    order_status = "CANCELED"
                ).returning(
                    MakeOrderOrm.order_status
                )

                get_update_data = s.execute(update_status_query).scalar_one_or_none()

                s.flush()

                if get_update_data is None or get_update_data == "SUCCESS":
                    return {
                        "message": "happen the error",
                        "order_status": get_update_data
                    }

                s.commit()

                return {
                    "current_status":get_update_data,
                    "status":"success"
                }

        except SQLAlchemyError as e:
            raise e


    @staticmethod
    def get_my_orders(user_id:int):
        get_all_the_orders = select(MakeOrderOrm).where(MakeOrderOrm.user_id == user_id)

        try:
            with session() as s:
                results = s.execute(get_all_the_orders).scalars().all()

                if results is None:
                    return None

                return results
        except SQLAlchemyError as e:
            raise e