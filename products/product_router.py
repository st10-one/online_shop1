from fastapi import APIRouter
from fastapi import Depends
from .schemas import CreateProduct, ReturnProductTabulation
from auth.utils import get_token_by_cookies
from .porduct_service import ProductService

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.post("", dependencies=[Depends(get_token_by_cookies)])
def create_new_product(new_product:CreateProduct):
    return ProductService.add_product(prod=new_product)


@product_router.get("")
def get_all_products(tab:ReturnProductTabulation = Depends()):
    return ProductService.get_all_the_products(tabul=tab)

@product_router.get("/{product_id}")
def get_one_product(product_id:int):
    return ProductService.get_one_product_by_id(prod_id=product_id)


@product_router.put("/{product_id}")
def update_product_data(product_id:int, new_data:CreateProduct):
    return ProductService.update_product(
        product_id=product_id,
        new_data=new_data
    )