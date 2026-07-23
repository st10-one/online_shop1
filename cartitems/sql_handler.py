from db import session
from sqlalchemy import select, update
from .model import CartItemsOrm
from products.model import CreateProductOrm
from .schema import CartItem

from sqlalchemy.exc import SQLAlchemyError



class CartItemsDTO:
    @staticmethod
    def add_to_cart(user_id:int, product_id:int) -> dict:
        try:
            with session() as s:
                stmt = select(CartItemsOrm).where(
                    CartItemsOrm.product_id == product_id,
                    CartItemsOrm.user_id == user_id
                )

            existing_item = s.execute(stmt).scalar_one_or_none()

            if existing_item:
                update_stmt = update(CartItemsOrm).where(CartItemsOrm.product_id == product_id).values(quantity=CartItemsOrm.quantity + 1)
                s.execute(update_stmt)
                s.commit()

                return {
                    "status": "success",
                    "message": "Товар повторно додано",
                    "added": True
                }

            else:
                new_item = CartItemsOrm(
                    user_id = user_id,
                    product_id = product_id,
                )

                s.add(new_item)
                s.commit()
                s.refresh(new_item)

            return {
                "status": "success",
                "message": "товар додано до кошику",
                "added": True
            }
        
        except SQLAlchemyError as e:
            s.rollback()

            print(e)

            return {
                "status": "cancel",
                "message": f"Щось пішло не так. Причина: {e}",
                "added": False,
            }


    @staticmethod
    def get_product_id(id:int) -> int | None:
        stmt = select(CreateProductOrm).where(CreateProductOrm.id==id)

        try:
            with session() as s:
                res_id = s.execute(stmt).scalar_one_or_none()

                if res_id is None:
                    return None
                
                return res_id.id
            
        except SQLAlchemyError as e:
            raise e


    @staticmethod 
    def get_all_with_cartitems() -> list[CartItemsOrm] | list[None]:
        stmt = select(CartItemsOrm)

        try:
            with session() as s:
                all_items = s.execute(stmt).scalars().all()

            if not all_items:
                return []

            return [CartItem.model_validate(my_item) for my_item in all_items]
        except SQLAlchemyError as e:
            print(e)
            raise e