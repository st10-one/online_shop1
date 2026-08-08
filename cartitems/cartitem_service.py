from fastapi import HTTPException
from depends import get_current_user, get_active_user
from .sql_handler import CartItemsDTO
from fastapi import Request



class CartItemService:
    @staticmethod
    def add_new_item(product_id:int, my_id:int):
        if not my_id:
            raise HTTPException(
                status_code=404,
                detail="Незнайдено користувача"
            )


        active_user = get_active_user(user_id=my_id)

        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
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
    def get_all_items_for_specific_user(my_id:int):
        active_user = get_active_user(user_id=my_id)

        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )        

        the_items = CartItemsDTO.get_all_with_cartitems(
            user_id=my_id
        )


        if not the_items:
            raise HTTPException(
                status_code=404,
                detail="Кошик пустий"
            )

        return the_items


    @staticmethod
    def delete_product_from_cartitem(product_id:int, my_id:int):
        active_user = get_active_user(user_id=my_id)

        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )
        
        id_deleted_of_product = CartItemsDTO.delete_from_cart_by_id(prod_id=product_id, user_id=my_id)

        if not id_deleted_of_product:
            raise HTTPException(
                status_code=404,
                detail= f"Товару з id {product_id} в кошику нема"
            )

        return {
            "id": id_deleted_of_product,
            "status": "success",
            "code": 204
        }