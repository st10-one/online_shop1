from db import session

from .model import CreateProductOrm
from .schemas import CreateProduct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update


class ProductRepo:
    @staticmethod
    def create_new_product(product_data:CreateProduct) -> CreateProductOrm | None:
        try:
            with session() as s:
                new_product = CreateProductOrm(
                    name=product_data.name,
                    price=product_data.price,
                    quantity=product_data.quantity,
                    description=product_data.description,
                    image_url=product_data.image_url
                )

                s.add(new_product)
                s.commit()
                s.refresh(new_product)

                return new_product
        except SQLAlchemyError:
            s.rollback()
            return None
        

    def get_all_products_from_db_tabulation(
            limit:int,
            offset:int
    ):
        select_query = select(CreateProductOrm).limit(limit=limit).offset(offset=offset)

        try:
            with session() as s:
                results = s.execute(select_query)

                if results:
                    return results.scalars().all()
                
        except SQLAlchemyError as e:
            print(e)
            return None
        

    def find_one_product_by_id(prod_id:int) -> CreateProductOrm | None:
        find_by_id_query = select(CreateProductOrm).where(CreateProductOrm.id == prod_id)

        try:
            with session() as s:
                result = s.execute(find_by_id_query)
                
                if result:
                    return result.scalar_one_or_none()
                
        except SQLAlchemyError as e:
            print(e)
            return None


    def update_product_data_by_id(prod_id:int, data:CreateProduct):
        stmt = update(CreateProductOrm).where(CreateProductOrm.id == prod_id).values(
            name = data.name,
            description = data.description,
            quantity = data.quantity,
            price = data.price,
            image_url = data.image_url
        ).returning(CreateProductOrm.id)

        try:
            with session() as s:
                result = s.execute(stmt).scalar_one_or_none()
                s.commit()

            if not result:
                return None

            return result
        except SQLAlchemyError as e:
            s.rollback()

            print(e)

            