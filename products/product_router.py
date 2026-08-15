from fastapi import APIRouter
from fastapi import Depends
from .schemas import CreateProduct, ReturnProductTabulation
from core_utils import get_current_user, ProductImage, get_product_data
from dependencies import get_product_service
from .porduct_service import ProductService

product_router = APIRouter(prefix="/products", tags=["Products🔌"])


@product_router.post("")
def create_new_product(photo:ProductImage, new_product:CreateProduct = Depends(get_product_data), product_service:ProductService = Depends(get_product_service), user:dict = Depends(get_current_user)):
    return product_service.add_product(
        prod=new_product,
        photo=photo,
        user=user
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
def update_products_data(product_id:int, new_data:CreateProduct, user:dict = Depends(get_current_user)):
    return ProductService.update_product(
        product_id=product_id,
        new_data=new_data,
        user=user
    )

@product_router.delete("/{product_id}")
def delete_products(prod_id:int, user:dict = Depends(get_current_user)):
    return ProductService.delete_product(
        prod_id=prod_id, 
        user=user
    )