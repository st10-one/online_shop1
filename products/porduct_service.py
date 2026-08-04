from fastapi import HTTPException, Request

from .sql_handler import ProductRepo
from depends import get_active_user, get_current_user
from .schemas import (
    CreateProduct,
    ShowProduct,
    ReturnProductTabulation
)



class ProductService:
    @staticmethod
    def add_product(prod:CreateProduct, request:Request):
        my_id = get_current_user(request=request)        

        active_user = get_active_user(user_id=my_id)

        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )

        new_product = ProductRepo.create_new_product(product_data=prod)

        if not new_product:
            raise HTTPException(
                status_code=400,
                detail="Product is not exist"
            )
        
        return ShowProduct.model_validate(new_product)
    
    @staticmethod
    def get_all_the_products(tabul:ReturnProductTabulation) -> ShowProduct | Exception:
        db_products = ProductRepo.get_all_products_from_db_tabulation(
            limit=tabul.limit,
            offset=tabul.offset
        )

        if not db_products:
            raise HTTPException(
                status_code=404,
                detail="products not found"
            )
        
        get_valid_data = [ShowProduct.model_validate(product) for product in db_products]

        return get_valid_data
        
    
    @staticmethod
    def get_one_product_by_id(prod_id:int):
        db_product = ProductRepo.find_one_product_by_id(prod_id=prod_id)

        if not db_product:
            raise HTTPException(
                status_code=404,
                detail="products not found"
            )
        
        return ShowProduct.model_validate(db_product)
    

    @staticmethod
    def update_product(product_id:int, new_data:CreateProduct, request:Request):
        my_id = get_current_user(request=request)       
        active_user = get_active_user(user_id=my_id)

        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )

        id_product_edited = ProductRepo.update_product_data_by_id(
            prod_id=product_id,
            data=new_data
        ) 

        if not id_product_edited:
            raise HTTPException(
                status_code=400,
                detail="happen the error"
            )

        return {
            "edited_id": id_product_edited
        }

    @staticmethod
    def delete_product(prod_id:int, request:Request):
        my_id = get_current_user(request=request)       
        active_user = get_active_user(user_id=my_id)

        if not active_user:
            raise HTTPException(
                status_code=403,
                detail="User is not active"
            )

        id_product_deleted = ProductRepo.delete_product_by_id(
            prod_id=prod_id,
        ) 

        if not id_product_deleted:
            raise HTTPException(
                status_code=400,
                detail="happen the error"
            )

        return {
            "edited_id": id_product_deleted
        }