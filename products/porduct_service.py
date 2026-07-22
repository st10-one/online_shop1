from fastapi import HTTPException

from .sql_handler import ProductRepo
from .schemas import (
    CreateProduct,
    ShowProduct,
    ReturnProductTabulation
)



class ProductService:
    @staticmethod
    def add_product(prod:CreateProduct):
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
    
