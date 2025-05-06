from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(128))
    account_balance = Column(Float, nullable=False)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")

