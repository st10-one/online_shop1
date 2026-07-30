from datetime import datetime

from db import Base

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped


class MakeOrderOrm(Base):
    __tablename__ = "orders"

    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    adderss:Mapped[str]
    phone:Mapped[str]
    order_status:Mapped[str] = mapped_column(CheckConstraint("order_status IN 'SUCCESSED', 'CANCELED'", name="order_status_check"))
    created_at:Mapped[datetime] = mapped_column(
        server_default=func.now()
    )



class DetailOrderOrm(Base):
    __tablename__ = "detail_order"

    id:Mapped[int] = mapped_column(primary_key=True)
    order_id:Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity:Mapped[int]
    price:Mapped[float]
