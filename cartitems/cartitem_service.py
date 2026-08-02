from fastapi import HTTPException
from depends import get_current_user
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
    def get_all_items_for_specific_user(request:Request):
        my_id = get_current_user(request=request)

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
    def delete_product_from_cartitem(product_id:int):
        id_deleted_of_product = CartItemsDTO.delete_from_cart_by_id(prod_id=product_id)

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