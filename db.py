from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import DB_URL


engine = create_engine(
    url=DB_URL
)

session = sessionmaker(
    bind=engine,
)
    

class Base(DeclarativeBase):
    pass



    