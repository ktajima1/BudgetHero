from sqlalchemy import Column, Integer, String
from backend.database import Base

class User(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, autoincrement=True)