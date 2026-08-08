from fastapi import APIRouter, Request
from fastapi import Depends
from .schemas import CreateProduct, ReturnProductTabulation
from auth.utils import get_token_by_cookies
from depends import get_current_user
from .porduct_service import ProductService

product_router = APIRouter(prefix="/products", tags=["Products🔌"])


@product_router.post("")
def create_new_product(new_product:CreateProduct, user_id:int = Depends(get_current_user)):
    return ProductService.add_product(
        prod=new_product,
        my_id=user_id
    )


@product_router.get("")
def get_all_products(tab:ReturnProductTabulation = Depends()):
    return ProductService.get_all_the_products(
        tabul=tab,
    )

@product_router.get("/{product_id}")
def get_one_products(product_id:int):
    return ProductService.get_one_product_by_id(prod_id=product_id)


@product_router.put("/{product_id}")
def update_products_data(product_id:int, new_data:CreateProduct, user_id:int = Depends(get_current_user)):
    return ProductService.update_product(
        product_id=product_id,
        new_data=new_data,
        my_id=user_id
    )

@product_router.delete("/{product_id}")
def delete_products(prod_id:int, user_id:int = Depends(get_current_user)):
    return ProductService.delete_product(
        prod_id=prod_id, 
        my_id=user_id
    )