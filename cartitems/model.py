from db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class CartItemsOrm(Base):
    __tablename__ = "CartItems"

    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity:Mapped[int] = mapped_column(default=1)


    user = relationship(
        "CreateUserOrm",
        back_populates="cartitem"
    )