from db import session
from .schemas import Orders
from sqlalchemy import select, delete
from cartitems.model import CartItemsOrm
from .models import MakeOrderOrm, DetailOrderOrm
from products.model import CreateProductOrm 



class OrderDTO:
    @staticmethod
    def add_order(user_id:int, data:Orders):
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

                if not get_product:
                    print('продукту нема')
                    return None

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
            else:
                print("я підор")