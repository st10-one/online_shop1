from sqlalchemy.orm import Mapped
from sqlalchemy import func, Enum
from sqlalchemy.orm import mapped_column, relationship

from datetime import datetime

from .utils import Roles
from db import Base


class CreateUserOrm(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str] = mapped_column(nullable=True)
    role:Mapped[Roles] = mapped_column(Enum(Roles, native_enum=False), nullable=False)
    is_active:Mapped[bool] = mapped_column(nullable=True)
    create_at:Mapped[datetime] = mapped_column(server_default=func.now())

    cartitem = relationship(
        "CartItemsOrm",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        passive_updates=True
    )
    
