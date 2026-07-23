from fastapi import HTTPException
from users.utils import get_current_user
from .sql_handler import CartItemsDTO
from fastapi import Request



class CartItemService:
    @staticmethod
    def add_new_item(product_id:int, request:Request):
        my_id = get_current_user(request=request)

        if not my_id:
            raise HTTPException(
                status_code=404,
                detail="Незнайдено користувача"
            )

        product_id = CartItemsDTO.get_product_id(id=product_id)

        if not product_id:
            raise HTTPException(
                status_code=404,
                detail="Товар неіснує"
            )

        adding = CartItemsDTO.add_to_cart(user_id=my_id, product_id=product_id)

        if not adding["added"]:
            raise HTTPException(
                status_code=400,
                detail="Неможна додати в кошик"
            )

        return adding
        

    @staticmethod
    def get_all_items():
        the_items = CartItemsDTO.get_all_with_cartitems()

        print(the_items)

        if not the_items:
            raise HTTPException(
                status_code=404,
                detail="Кошик пустий"
            )

        return the_items