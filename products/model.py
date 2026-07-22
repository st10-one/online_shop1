from sqlalchemy.orm import Mapped
from sqlalchemy import func
from sqlalchemy.orm import mapped_column

from datetime import datetime

from db import Base


class CreateProductOrm(Base):
    __tablename__ = "products"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    price:Mapped[float]
    quantity:Mapped[int]
    description:Mapped[str]
    image_url:Mapped[str] = mapped_column(nullable=False)

    create_at:Mapped[datetime] = mapped_column(server_default=func.now())



