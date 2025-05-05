from backend.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, unique=True, nullable=False) # Names should be unique and case-insensitive
    description = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="category")