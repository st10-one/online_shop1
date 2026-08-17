from fastapi import HTTPException

from .sql_handler import ProductRepo
from core_utils import get_active_user, check_admin, ProductImage

from io import BytesIO

from S3.base import Storage
from .schemas import (
    CreateProduct,
    ShowProduct,
    ReturnProductTabulation
)



class ProductService:
    def __init__(self, storage:Storage):
        self.storage = storage

    def add_product(self, prod:CreateProduct, photo:ProductImage):
        filename = photo.filename
        file_content = photo.file.read(1024)
        file_len = len(file_content)
        file_content_type = photo.content_type

        file_data = BytesIO(file_content)


        url = self.storage.upload(
            filename=filename,
            file_data=file_data,
            lenght=file_len,
            content_type=file_content_type
        )

        new_product = ProductRepo.create_new_product(product_data=prod, url=url)
        

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
    def update_product(product_id:int, new_data:CreateProduct):
        id_product_edited = ProductRepo.update_product_data_by_id(
            prod_id=product_id,
            data=new_data
        ) 

        if not id_product_edited:
            raise HTTPException(
                status_code=400,
                detail="такого продукту неіснує"
            )

        return {
            "edited_id": id_product_edited
        }

    def delete_product(self, prod_id:int):
        url = ProductRepo.delete_product_by_id(
            prod_id=prod_id,
        )

        if not url:
            raise HTTPException(
                status_code=404
            )

        self.storage.delete(url=url)

        return {
            "status": True
        }