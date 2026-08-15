from fastapi import Depends

from S3 import MinioStorage
from S3.base import Storage
from config import settings
from products.porduct_service import ProductService


def get_storage() -> Storage:
    return MinioStorage(config=settings)


def get_product_service(
        storage:Storage = Depends(get_storage)
    ):
    return ProductService(storage=storage)
    