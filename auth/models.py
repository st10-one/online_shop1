from sqlalchemy.orm import Mapped
from sqlalchemy import func
from sqlalchemy.orm import mapped_column

from datetime import datetime

from db import Base


class CreateUserOrm(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str] = mapped_column(unique=True)
    create_at:Mapped[datetime] = mapped_column(server_default=func.now())

    
